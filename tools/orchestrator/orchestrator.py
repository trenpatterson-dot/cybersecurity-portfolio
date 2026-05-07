#!/usr/bin/env python3
"""Read-only central workflow orchestrator.

The orchestrator chains local report-only wrappers when they exist:

1. evidence-validator
2. github-readiness
3. project-closeout

It does not stage, commit, push, move, delete, rename, publish, call external
APIs, run live scans, or read secret-like file contents.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


OVERALL_STATUSES = ("WORKFLOW READY", "NEEDS REVIEW", "BLOCKED", "PARTIAL TOOLCHAIN", "LOCAL ONLY")
BLOCKING_STATUSES = {
    "BLOCKED",
    "DO NOT PUBLISH",
    "SECURITY BLOCKED",
    "GITHUB BLOCKED",
    "EVIDENCE BLOCKED",
}
LOCAL_ONLY_STATUSES = {"KEEP LOCAL ONLY", "LOCAL ONLY"}
REVIEW_STATUSES = {"NEEDS ORGANIZATION", "NEEDS FIXES", "NEEDS WORK", "PRIVACY REVIEW NEEDED"}
READY_STATUSES = {"EVIDENCE READY", "READY FOR REVIEW", "CLOSEOUT READY"}


@dataclass(frozen=True)
class WrapperSpec:
    name: str
    script: Path


@dataclass
class WrapperRun:
    name: str
    available: bool
    status: str | None = None
    exit_code: int | None = None
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    stdout_json: dict | None = None
    stdout_markdown: str = ""
    stderr: str = ""
    script_path: str | None = None


@dataclass
class OrchestrationResult:
    status: str
    recommended_next_action: str
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    wrapper_runs: list[WrapperRun] = field(default_factory=list)
    report_paths: list[str] = field(default_factory=list)
    details: dict = field(default_factory=dict)


def run_command(args: list[str], cwd: Path) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(args, cwd=str(cwd), text=True, capture_output=True, check=False)
    except OSError as exc:
        return 127, "", str(exc)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def find_repo_root(start: Path) -> Path:
    code, stdout, _ = run_command(["git", "rev-parse", "--show-toplevel"], start)
    if code == 0 and stdout:
        return Path(stdout).resolve()
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def wrapper_specs(repo_root: Path) -> list[WrapperSpec]:
    return [
        WrapperSpec("evidence-validator", repo_root / "tools" / "evidence-validator" / "evidence_validator.py"),
        WrapperSpec("github-readiness", repo_root / "tools" / "github-readiness" / "github_readiness.py"),
        WrapperSpec("project-closeout", repo_root / "tools" / "project-closeout" / "project_closeout.py"),
    ]


def run_wrapper(spec: WrapperSpec, project_path: Path, repo_root: Path, capture_markdown: bool) -> WrapperRun:
    if not spec.script.exists():
        return WrapperRun(
            name=spec.name,
            available=False,
            warnings=[f"{spec.name} wrapper was not found"],
            script_path=rel(spec.script, repo_root),
        )

    json_code, json_stdout, json_stderr = run_command(
        [sys.executable, str(spec.script), "--project-path", str(project_path), "--json"],
        repo_root,
    )
    run = WrapperRun(
        name=spec.name,
        available=True,
        exit_code=json_code,
        stderr=json_stderr,
        script_path=rel(spec.script, repo_root),
    )
    if json_code != 0:
        run.blockers.append(f"{spec.name} exited with code {json_code}")
        return run
    try:
        parsed = json.loads(json_stdout)
    except json.JSONDecodeError:
        run.blockers.append(f"{spec.name} did not return valid JSON")
        return run

    run.stdout_json = parsed
    run.status = parsed.get("status")
    run.warnings.extend(str(item) for item in parsed.get("warnings", []))
    run.blockers.extend(str(item) for item in parsed.get("blockers", []))

    if capture_markdown:
        md_code, md_stdout, md_stderr = run_command(
            [sys.executable, str(spec.script), "--project-path", str(project_path)],
            repo_root,
        )
        if md_code == 0:
            run.stdout_markdown = md_stdout
        else:
            run.warnings.append(f"{spec.name} markdown report failed with code {md_code}")
            if md_stderr:
                run.stderr = "\n".join(part for part in [run.stderr, md_stderr] if part)
    return run


def determine_overall_status(wrapper_runs: list[WrapperRun]) -> tuple[str, str]:
    if any(not run.available for run in wrapper_runs):
        return "PARTIAL TOOLCHAIN", "One or more local wrappers are missing; review available reports before continuing."
    if any((run.status or "").upper() in LOCAL_ONLY_STATUSES for run in wrapper_runs):
        return "LOCAL ONLY", "At least one wrapper marked the project as local-only."
    if any((run.status or "").upper() in BLOCKING_STATUSES or run.blockers for run in wrapper_runs):
        return "BLOCKED", "At least one wrapper reported blockers."
    if any((run.status or "").upper() in REVIEW_STATUSES for run in wrapper_runs):
        # Evidence-validator can return NEEDS ORGANIZATION for local-only outputs
        # while GitHub readiness and closeout still pass. Keep that as ready if
        # downstream gates explicitly passed and no blockers exist.
        downstream_ready = {
            run.name: (run.status or "").upper()
            for run in wrapper_runs
            if run.name in {"github-readiness", "project-closeout"}
        }
        if downstream_ready.get("github-readiness") == "READY FOR REVIEW" and downstream_ready.get("project-closeout") == "CLOSEOUT READY":
            return "WORKFLOW READY", "All downstream gates passed; evidence warnings remain review notes."
        return "NEEDS REVIEW", "At least one wrapper needs review or organization."
    if all((run.status or "").upper() in READY_STATUSES for run in wrapper_runs):
        return "WORKFLOW READY", "All available wrappers reported ready statuses."
    return "NEEDS REVIEW", "Wrapper statuses need human review before any external action."


def orchestrate(project_path: Path, report_dir: Path | None = None) -> OrchestrationResult:
    project_path = project_path.resolve()
    repo_root = find_repo_root(project_path)
    capture_markdown = report_dir is not None
    runs = [run_wrapper(spec, project_path, repo_root, capture_markdown) for spec in wrapper_specs(repo_root)]

    warnings: list[str] = []
    blockers: list[str] = []
    for run in runs:
        warnings.extend(f"{run.name}: {item}" for item in run.warnings)
        blockers.extend(f"{run.name}: {item}" for item in run.blockers)

    status, action = determine_overall_status(runs)
    result = OrchestrationResult(
        status=status,
        recommended_next_action=action,
        warnings=sorted(set(warnings)),
        blockers=sorted(set(blockers)),
        wrapper_runs=runs,
        details={
            "project_path": str(project_path),
            "project_name": project_path.name,
            "repo_root": str(repo_root),
            "reviewed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "report_only": True,
            "external_actions": "not run",
        },
    )

    if report_dir is not None:
        result.report_paths = save_reports(result, report_dir)
    return result


def safe_report_name(name: str, suffix: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in name.lower())
    return f"{cleaned}{suffix}"


def save_reports(result: OrchestrationResult, report_dir: Path) -> list[str]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    target_dir = report_dir / timestamp
    target_dir.mkdir(parents=True, exist_ok=True)

    paths: list[Path] = []
    markdown_path = target_dir / "orchestration-report.md"
    markdown_path.write_text(render_markdown(result), encoding="utf-8")
    paths.append(markdown_path)

    json_path = target_dir / "orchestration-report.json"
    json_path.write_text(json.dumps(as_dict(result, include_report_paths=False), indent=2), encoding="utf-8")
    paths.append(json_path)

    for run in result.wrapper_runs:
        if run.stdout_markdown:
            path = target_dir / safe_report_name(run.name, ".md")
            path.write_text(run.stdout_markdown + "\n", encoding="utf-8")
            paths.append(path)
        if run.stdout_json is not None:
            path = target_dir / safe_report_name(run.name, ".json")
            path.write_text(json.dumps(run.stdout_json, indent=2), encoding="utf-8")
            paths.append(path)

    return [str(path) for path in paths]


def wrapper_as_dict(run: WrapperRun) -> dict:
    return {
        "name": run.name,
        "available": run.available,
        "status": run.status,
        "exit_code": run.exit_code,
        "warnings": run.warnings,
        "blockers": run.blockers,
        "script_path": run.script_path,
        "stderr": run.stderr,
    }


def as_dict(result: OrchestrationResult, include_report_paths: bool = True) -> dict:
    data = {
        "status": result.status,
        "recommended_next_action": result.recommended_next_action,
        "warnings": result.warnings,
        "blockers": result.blockers,
        "wrappers": [wrapper_as_dict(run) for run in result.wrapper_runs],
        **result.details,
    }
    if include_report_paths:
        data["report_paths"] = result.report_paths
    return data


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def render_markdown(result: OrchestrationResult) -> str:
    details = result.details
    wrappers = "\n".join(
        [
            f"- {run.name}: {'available' if run.available else 'missing'}"
            f"; status={run.status or 'not available'}"
            f"; blockers={len(run.blockers)}"
            f"; warnings={len(run.warnings)}"
            for run in result.wrapper_runs
        ]
    )
    report_paths = list_or_none(result.report_paths)
    return f"""# Central Orchestration Report

## Project

- Project name: {details.get("project_name")}
- Path: {details.get("project_path")}
- Reviewed at: {details.get("reviewed_at")}
- Reviewer workflow: read-only central orchestrator
- Overall orchestration status: {result.status}

## Summary

This report chained local wrappers in gate order: evidence-validator, github-readiness, and project-closeout. No files were staged, committed, pushed, moved, deleted, renamed, published, externally scanned, or sent to external APIs.

## Wrapper Execution Summary

{wrappers or "- None found"}

## Blockers

{list_or_none(result.blockers)}

## Warnings

{list_or_none(result.warnings)}

## Recommended Next Action

- {result.recommended_next_action}

## Generated Reports

{report_paths}

## Safety Boundary

- Report-only: yes
- Git actions run: no
- External APIs run: no
- Live scans run: no
- Project content modified: no
- Local-only artifacts treated as local-only: yes
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only central workflow orchestrator.")
    parser.add_argument("--project-path", required=True, help="Project folder to inspect.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown.")
    parser.add_argument("--report-dir", help="Optional directory where timestamped reports are saved.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = orchestrate(Path(args.project_path), Path(args.report_dir) if args.report_dir else None)
    if args.json:
        print(json.dumps(as_dict(result), indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
