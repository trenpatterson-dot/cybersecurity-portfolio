#!/usr/bin/env python3
"""Read-only project closeout wrapper.

This tool inspects local project files and local Git metadata only. It does not
stage, commit, push, move, delete, rename, publish, call external services, run
live scans, or read secret-like file contents.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import unquote, urlparse


DECISIONS = (
    "CLOSEOUT READY",
    "NEEDS WORK",
    "SECURITY BLOCKED",
    "GITHUB BLOCKED",
    "EVIDENCE BLOCKED",
    "KEEP LOCAL ONLY",
)
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
README_IMAGE_RE = re.compile(r"!\[[^\]]*]\(([^)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
SECRET_NAME_PATTERNS = (
    re.compile(r"(^|[._-])\.?env($|[._-])", re.IGNORECASE),
    re.compile(r"(secret|credential|token|apikey|api_key|access_key)", re.IGNORECASE),
    re.compile(r"(password|passwd|pwd|cookie)", re.IGNORECASE),
    re.compile(r"(^|[._-])id_rsa($|[._-])", re.IGNORECASE),
    re.compile(r"(^|[._-])private[_-]?key($|[._-])", re.IGNORECASE),
)
SECRET_EXTENSIONS = {".pem", ".p12", ".pfx", ".key"}
HANDOFF_RE = re.compile(r"handoff", re.IGNORECASE)
LINKEDIN_RE = re.compile(r"(linkedin|social[-_]post|post[-_]draft)", re.IGNORECASE)
GENERATED_DIR_NAMES = {"outputs", "output", "agent-output", "agent_outputs", "generated", "dist", "build"}
SKIP_DIR_NAMES = {".git", ".hg", ".svn", ".venv", "venv", "env", "node_modules", "__pycache__"}
CREDENTIALED_REMOTE_RE = re.compile(r"://[^/\s:@]+:[^@\s]+@")


@dataclass
class CloseoutResult:
    status: str
    reason: str
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    complete: list[str] = field(default_factory=list)
    missing: list[str] = field(default_factory=list)
    local_only_files: list[str] = field(default_factory=list)
    safe_files: list[str] = field(default_factory=list)
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


def is_secret_like(path: Path) -> bool:
    name = path.name
    if path.suffix.lower() in SECRET_EXTENSIONS:
        return True
    return any(pattern.search(name) for pattern in SECRET_NAME_PATTERNS)


def safe_walk(root: Path) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_DIR_NAMES and not is_secret_like(current_path / name)
        ]
        for filename in files:
            yield current_path / filename


def read_text_if_safe(path: Path) -> str:
    if is_secret_like(path):
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def parse_readme_image_refs(readme_text: str) -> list[str]:
    refs: list[str] = []
    refs.extend(README_IMAGE_RE.findall(readme_text))
    refs.extend(HTML_IMAGE_RE.findall(readme_text))
    cleaned: list[str] = []
    for ref in refs:
        target = ref.split()[0].strip("<>")
        if target:
            cleaned.append(target)
    return cleaned


def is_local_ref(ref: str) -> bool:
    parsed = urlparse(ref)
    return not parsed.scheme and not ref.startswith("#")


def ref_to_path(ref: str, readme_dir: Path) -> Path:
    target = unquote(ref.split("#", 1)[0].split("?", 1)[0])
    return (readme_dir / target).resolve()


def git_check_ignored(repo_root: Path, path: Path) -> bool:
    code, _, _ = run_command(["git", "check-ignore", "-q", str(path)], repo_root)
    return code == 0


def collect_files(project_path: Path, repo_root: Path) -> dict:
    all_files = sorted(safe_walk(project_path))
    image_files = [path for path in all_files if path.suffix.lower() in IMAGE_EXTENSIONS]
    public_screenshots = [
        path for path in image_files if "screenshots-public" in {part.lower() for part in path.parts}
    ]
    raw_screenshots = [
        path
        for path in image_files
        if "evidence" in {part.lower() for part in path.parts}
        and "screenshots" in {part.lower() for part in path.parts}
        and "screenshots-public" not in {part.lower() for part in path.parts}
    ]
    outputs = [
        path
        for path in all_files
        if any(part.lower() in GENERATED_DIR_NAMES for part in path.relative_to(project_path).parts)
    ]
    handoffs = [path for path in all_files if HANDOFF_RE.search(path.name) and path.suffix.lower() == ".md"]
    linkedin = [path for path in all_files if LINKEDIN_RE.search(path.as_posix())]
    secrets = [path for path in all_files if is_secret_like(path)]
    ignored = {path: git_check_ignored(repo_root, path) for path in all_files}
    return {
        "all_files": all_files,
        "public_screenshots": public_screenshots,
        "raw_screenshots": raw_screenshots,
        "outputs": outputs,
        "handoffs": handoffs,
        "linkedin": linkedin,
        "secrets": secrets,
        "ignored": ignored,
    }


def read_report_status(report_path: Path | None, project_path: Path, status_names: tuple[str, ...]) -> dict:
    if not report_path:
        return {"provided": False, "path": None, "status": None, "warnings": [], "blockers": []}
    candidate = report_path if report_path.is_absolute() else project_path / report_path
    if not candidate.exists() or not candidate.is_file():
        return {
            "provided": True,
            "path": str(candidate),
            "status": None,
            "warnings": [f"report was not found: {candidate}"],
            "blockers": [],
        }
    if is_secret_like(candidate):
        return {
            "provided": True,
            "path": str(candidate),
            "status": None,
            "warnings": [],
            "blockers": [f"report path is secret-like and was not read: {candidate.name}"],
        }
    text = read_text_if_safe(candidate)
    status = extract_status(text, status_names)
    return {"provided": True, "path": str(candidate), "status": status, "warnings": [], "blockers": []}


def extract_status(text: str, status_names: tuple[str, ...]) -> str | None:
    lowered = text.lower()
    for status in status_names:
        if status.lower() in lowered:
            return status
    return None


def run_evidence_validator(project_path: Path, repo_root: Path) -> dict:
    validator = repo_root / "tools" / "evidence-validator" / "evidence_validator.py"
    if not validator.exists():
        return {"available": False, "status": None, "warnings": ["evidence-validator was not found"], "blockers": []}
    code, stdout, stderr = run_command(
        [sys.executable, str(validator), "--project-path", str(project_path), "--json"],
        repo_root,
    )
    if code != 0:
        return {
            "available": True,
            "status": None,
            "warnings": [f"evidence-validator failed with exit code {code}"],
            "blockers": [],
            "stderr": stderr,
        }
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return {"available": True, "status": None, "warnings": ["evidence-validator output was not valid JSON"], "blockers": []}
    return {
        "available": True,
        "status": data.get("status"),
        "warnings": data.get("warnings", []),
        "blockers": data.get("blockers", []),
        "secret_like_files": data.get("secret_like_files", []),
        "missing_readme_refs": data.get("missing_readme_refs", []),
    }


def run_github_readiness(project_path: Path, repo_root: Path) -> dict:
    wrapper = repo_root / "tools" / "github-readiness" / "github_readiness.py"
    if not wrapper.exists():
        return {"available": False, "status": None, "warnings": ["github-readiness wrapper was not found"], "blockers": []}
    code, stdout, stderr = run_command(
        [sys.executable, str(wrapper), "--project-path", str(project_path), "--json"],
        repo_root,
    )
    if code != 0:
        return {
            "available": True,
            "status": None,
            "warnings": [f"github-readiness wrapper failed with exit code {code}"],
            "blockers": [],
            "stderr": stderr,
        }
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return {"available": True, "status": None, "warnings": ["github-readiness output was not valid JSON"], "blockers": []}
    return {
        "available": True,
        "status": data.get("status"),
        "warnings": data.get("warnings", []),
        "blockers": data.get("blockers", []),
        "safe_files": data.get("safe_files", []),
        "local_only_files": data.get("local_only_files", []),
    }


def determine_status(
    security_blockers: list[str],
    github_blockers: list[str],
    evidence_blockers: list[str],
    work_items: list[str],
) -> tuple[str, str]:
    if security_blockers:
        return "SECURITY BLOCKED", security_blockers[0]
    if github_blockers:
        return "GITHUB BLOCKED", github_blockers[0]
    if evidence_blockers:
        return "EVIDENCE BLOCKED", evidence_blockers[0]
    if work_items:
        return "NEEDS WORK", work_items[0]
    return "CLOSEOUT READY", "All required local closeout gates passed; final human approval is still required."


def review_project(
    project_path: Path,
    github_readiness_report: Path | None = None,
    evidence_report: Path | None = None,
) -> CloseoutResult:
    project_path = project_path.resolve()
    repo_root = find_repo_root(project_path)
    if not project_path.exists() or not project_path.is_dir():
        return CloseoutResult(
            status="KEEP LOCAL ONLY",
            reason=f"Project path does not exist or is not a directory: {project_path}",
            blockers=[f"project path does not exist or is not a directory: {project_path}"],
        )

    blockers: list[str] = []
    warnings: list[str] = []
    complete: list[str] = []
    missing: list[str] = []
    security_blockers: list[str] = []
    github_blockers: list[str] = []
    evidence_blockers: list[str] = []
    work_items: list[str] = []
    local_only_files: list[str] = []
    safe_files: list[str] = []

    readme_path = project_path / "README.md"
    docs_dir = project_path / "docs"
    queries_dir = project_path / "queries"
    closeout_report = docs_dir / "project-closeout-report.md"

    readme_exists = readme_path.exists() and readme_path.is_file() and not is_secret_like(readme_path)
    if readme_exists:
        complete.append("README.md exists")
        safe_files.append(rel(readme_path, repo_root))
    else:
        work_items.append("README.md is missing")
        missing.append("README.md")

    if docs_dir.exists() and docs_dir.is_dir():
        complete.append("docs/ exists")
        for path in sorted(docs_dir.glob("*.md")):
            if not is_secret_like(path):
                safe_files.append(rel(path, repo_root))
    else:
        work_items.append("docs/ folder is missing")
        missing.append("docs/")

    if queries_dir.exists() and queries_dir.is_dir():
        complete.append("queries/ exists")
        for path in sorted(queries_dir.glob("*")):
            if path.is_file() and not is_secret_like(path):
                safe_files.append(rel(path, repo_root))
    else:
        work_items.append("queries/ folder is missing")
        missing.append("queries/")

    if closeout_report.exists() and closeout_report.is_file() and not is_secret_like(closeout_report):
        complete.append("project-closeout-report.md exists")
    else:
        work_items.append("project-closeout-report.md should be created before final closeout")
        missing.append("docs/project-closeout-report.md")

    readme_text = read_text_if_safe(readme_path) if readme_exists else ""
    refs = parse_readme_image_refs(readme_text)
    valid_refs: list[str] = []
    missing_refs: list[str] = []
    raw_refs: list[str] = []
    for ref in refs:
        if not is_local_ref(ref):
            continue
        resolved = ref_to_path(ref, readme_path.parent)
        rel_ref = rel(resolved, project_path)
        if resolved.exists() and resolved.is_file():
            valid_refs.append(ref)
        else:
            missing_refs.append(ref)
        if "/screenshots/" in rel_ref or "\\screenshots\\" in rel_ref:
            raw_refs.append(ref)
    if missing_refs:
        evidence_blockers.append("README image references do not match local files")
    if raw_refs:
        github_blockers.append("README links to raw screenshots instead of public screenshots")

    files = collect_files(project_path, repo_root)
    ignored = files["ignored"]

    if files["public_screenshots"]:
        complete.append("public screenshots exist")
        for path in files["public_screenshots"]:
            if ignored.get(path, False):
                github_blockers.append("public screenshot is ignored by git")
            else:
                safe_files.append(rel(path, repo_root))
    else:
        work_items.append("public screenshots were not found")
        missing.append("evidence/screenshots-public/")

    for path in files["raw_screenshots"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            github_blockers.append("raw screenshot is not ignored/local-only")

    for path in files["outputs"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            github_blockers.append("outputs/ file is not ignored/local-only")

    for path in files["handoffs"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            github_blockers.append("HANDOFF file is not ignored/local-only")

    for path in files["linkedin"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            github_blockers.append("LinkedIn draft is not ignored/local-only")

    for path in files["secrets"]:
        security_blockers.append(f"secret-like filename found; contents were not read: {rel(path, repo_root)}")

    evidence = run_evidence_validator(project_path, repo_root)
    if evidence.get("blockers"):
        evidence_blockers.extend(f"evidence-validator: {item}" for item in evidence["blockers"])
    if evidence.get("secret_like_files"):
        security_blockers.append("evidence-validator found secret-like files")
    if evidence.get("missing_readme_refs"):
        evidence_blockers.append("evidence-validator found missing README image references")
    if evidence.get("warnings"):
        warnings.extend(f"evidence-validator: {item}" for item in evidence["warnings"])

    github_readiness = run_github_readiness(project_path, repo_root)
    github_status = github_readiness.get("status")
    if github_status in {"BLOCKED", "DO NOT PUBLISH"}:
        github_blockers.append(f"github-readiness status is {github_status}")
    elif github_status == "NEEDS FIXES":
        work_items.append("github-readiness status is NEEDS FIXES")
    if github_readiness.get("blockers"):
        github_blockers.extend(f"github-readiness: {item}" for item in github_readiness["blockers"])
    if github_readiness.get("warnings"):
        warnings.extend(f"github-readiness: {item}" for item in github_readiness["warnings"])

    supplied_github_report = read_report_status(
        github_readiness_report,
        project_path,
        ("READY FOR REVIEW", "NEEDS FIXES", "BLOCKED", "DO NOT PUBLISH"),
    )
    supplied_evidence_report = read_report_status(
        evidence_report,
        project_path,
        ("READY FOR GITHUB", "NEEDS ORGANIZATION", "BLOCKED"),
    )
    if supplied_github_report.get("blockers"):
        github_blockers.extend(supplied_github_report["blockers"])
    if supplied_github_report.get("warnings"):
        warnings.extend(supplied_github_report["warnings"])
    if supplied_github_report.get("status") in {"BLOCKED", "DO NOT PUBLISH"}:
        github_blockers.append(f"provided github-readiness report status is {supplied_github_report['status']}")
    if supplied_github_report.get("status") == "NEEDS FIXES":
        work_items.append("provided github-readiness report status is NEEDS FIXES")
    if supplied_evidence_report.get("blockers"):
        evidence_blockers.extend(supplied_evidence_report["blockers"])
    if supplied_evidence_report.get("warnings"):
        warnings.extend(supplied_evidence_report["warnings"])
    if supplied_evidence_report.get("status") == "BLOCKED":
        evidence_blockers.append("provided evidence report status is BLOCKED")

    remote_code, remote_stdout, _ = run_command(["git", "remote", "-v"], repo_root)
    credentialed_remotes: list[str] = []
    if remote_code == 0:
        for line in remote_stdout.splitlines():
            if CREDENTIALED_REMOTE_RE.search(line):
                credentialed_remotes.append(re.sub(CREDENTIALED_REMOTE_RE, "://<redacted>@", line))
    if credentialed_remotes:
        security_blockers.append("credentialed git remote detected")

    project_pathspec = rel(project_path, repo_root)
    status_code, status_stdout, _ = run_command(["git", "status", "--short", "--", project_pathspec], repo_root)
    git_status = status_stdout.splitlines() if status_code == 0 and status_stdout else []

    blockers.extend(security_blockers)
    blockers.extend(github_blockers)
    blockers.extend(evidence_blockers)
    blockers.extend(work_items)
    status, reason = determine_status(security_blockers, github_blockers, evidence_blockers, work_items)

    return CloseoutResult(
        status=status,
        reason=reason,
        blockers=sorted(set(blockers)),
        warnings=sorted(set(warnings)),
        complete=sorted(set(complete)),
        missing=sorted(set(missing)),
        local_only_files=sorted(set(local_only_files)),
        safe_files=sorted(set(safe_files)),
        details={
            "project_name": project_path.name,
            "project_path": str(project_path),
            "repo_root": str(repo_root),
            "reviewed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "readme_exists": readme_exists,
            "docs_exists": docs_dir.exists() and docs_dir.is_dir(),
            "queries_exists": queries_dir.exists() and queries_dir.is_dir(),
            "closeout_report_exists": closeout_report.exists() and closeout_report.is_file(),
            "readme_image_refs": refs,
            "valid_readme_refs": valid_refs,
            "missing_readme_refs": missing_refs,
            "public_screenshots": [rel(path, repo_root) for path in files["public_screenshots"]],
            "raw_screenshots": [rel(path, repo_root) for path in files["raw_screenshots"]],
            "git_status": git_status,
            "credentialed_remotes": credentialed_remotes,
            "git_remote_checked": remote_code == 0,
            "evidence_validator": evidence,
            "github_readiness": github_readiness,
            "provided_github_readiness_report": supplied_github_report,
            "provided_evidence_report": supplied_evidence_report,
        },
    )


def as_dict(result: CloseoutResult) -> dict:
    return {
        "status": result.status,
        "reason": result.reason,
        "blockers": result.blockers,
        "warnings": result.warnings,
        "complete": result.complete,
        "missing": result.missing,
        "local_only_files": result.local_only_files,
        "safe_files": result.safe_files,
        **result.details,
    }


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def render_markdown(result: CloseoutResult) -> str:
    details = result.details
    evidence = details.get("evidence_validator", {})
    readiness = details.get("github_readiness", {})
    github_report = details.get("provided_github_readiness_report", {})
    evidence_report = details.get("provided_evidence_report", {})
    return f"""# Project Closeout Report

## Project

- Name: {details.get("project_name")}
- Path: {details.get("project_path")}
- Reviewed at: {details.get("reviewed_at")}
- Reviewer: read-only project closeout wrapper

## Final Status

- Status: {result.status}
- Reason: {result.reason}

## What Is Complete

{list_or_none(result.complete)}

## What Is Missing

{list_or_none(result.missing)}

## Evidence Gate

- Status: {evidence.get("status") or "not available"}
- Evidence report provided: {yes_no(bool(evidence_report.get("provided")))}
- Evidence report status: {evidence_report.get("status") or "not provided"}
- Evidence validator available: {yes_no(bool(evidence.get("available")))}
- Blockers:
{list_or_none(evidence.get("blockers", []))}
- Warnings:
{list_or_none(evidence.get("warnings", []))}

## Screenshot Gate

- Status: {"pass" if details.get("public_screenshots") and not details.get("missing_readme_refs") else "needs review"}
- Public screenshot folder: evidence/screenshots-public
- Public screenshots:
{list_or_none(details.get("public_screenshots", []))}
- Raw screenshots:
{list_or_none(details.get("raw_screenshots", []))}
- README screenshot references:
{list_or_none(details.get("readme_image_refs", []))}
- Broken README references:
{list_or_none(details.get("missing_readme_refs", []))}

## README Gate

- Status: {"pass" if details.get("readme_exists") else "missing"}
- README path: README.md
- Recruiter-ready: requires human review
- Proof-aligned: requires human review
- Public-safe: requires human review

## Supervisor-Agent Outputs

- Status: local-only artifacts inspected by path
- Handoff/local-only items:
{list_or_none(result.local_only_files)}
- Notes: This wrapper does not run supervisor agents or publish drafts.

## Security Review

- Status: {"blocked" if result.status == "SECURITY BLOCKED" else "no filename-only blocker found"}
- Credentialed git remotes:
{list_or_none(details.get("credentialed_remotes", []))}
- Notes: Secret-like files are checked by filename only; contents are not read.

## GitHub Readiness

- Status: {readiness.get("status") or "not available"}
- Wrapper available: {yes_no(bool(readiness.get("available")))}
- Provided readiness report: {yes_no(bool(github_report.get("provided")))}
- Provided readiness report status: {github_report.get("status") or "not provided"}
- Safe files:
{list_or_none(result.safe_files)}
- Local-only files:
{list_or_none(result.local_only_files)}

## LinkedIn Draft Status

- Status: local-only required
- Local-only confirmed: {"yes" if result.local_only_files else "not applicable"}
- Notes: LinkedIn drafts must stay out of GitHub publishing guidance.

## Notion Update

- Status: manual copy/paste only
- Copy/paste-ready update exists: requires human review
- Suggested status: GitHub Ready if human review agrees with this report
- Notes: This wrapper does not call Notion.

## Git Status

{list_or_none(details.get("git_status", []))}

## Remaining Blockers

{list_or_none(result.blockers)}

## Warnings

{list_or_none(result.warnings)}

## Recommended Next Action

- Review this report manually before any git add, commit, push, publishing, LinkedIn posting, or Notion update.

## Supervisor-Agent Handoff

- CHATGPT HANDOFF: Project closeout wrapper produced a read-only local report.
- AGENT ROUTING RECOMMENDATION: No local agent is required for this wrapper result unless Tren requests deeper review.
- Remaining blockers: {result.reason if result.status != "CLOSEOUT READY" else "None found"}

## Final Human Approval Required

- Approval required before git actions: yes
- Approval required before publishing: yes
- Approval required before Notion API action: yes
- Approval required before LinkedIn posting: yes
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only project closeout wrapper.")
    parser.add_argument("--project-path", required=True, help="Project folder to inspect.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown.")
    parser.add_argument("--github-readiness-report", help="Optional GitHub readiness report path.")
    parser.add_argument("--evidence-report", help="Optional evidence report path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = review_project(
        Path(args.project_path),
        Path(args.github_readiness_report) if args.github_readiness_report else None,
        Path(args.evidence_report) if args.evidence_report else None,
    )
    if args.json:
        print(json.dumps(as_dict(result), indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
