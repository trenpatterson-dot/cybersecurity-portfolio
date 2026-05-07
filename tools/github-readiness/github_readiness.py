#!/usr/bin/env python3
"""Read-only GitHub readiness wrapper.

This tool inspects local project files and local Git metadata only. It does not
stage, commit, push, move, delete, rename, publish, scan live targets, or read
secret-like file contents.
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


DECISIONS = ("READY FOR REVIEW", "NEEDS FIXES", "BLOCKED", "DO NOT PUBLISH")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
README_IMAGE_RE = re.compile(r"!\[[^\]]*]\(([^)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
TODO_RE = re.compile(
    r"\b(TODO|TBD|FIXME|placeholder|coming soon|insert screenshot|add screenshot|lorem ipsum)\b",
    re.IGNORECASE,
)
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
class CheckResult:
    status: str
    warnings: list[str] = field(default_factory=list)
    blockers: list[str] = field(default_factory=list)
    safe_files: list[str] = field(default_factory=list)
    local_only_files: list[str] = field(default_factory=list)
    blocked_files: list[str] = field(default_factory=list)
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
            d
            for d in dirs
            if d not in SKIP_DIR_NAMES and not is_secret_like(current_path / d)
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
    raw_screenshots = [
        path
        for path in image_files
        if "evidence" in {part.lower() for part in path.parts}
        and "screenshots" in {part.lower() for part in path.parts}
        and "screenshots-public" not in {part.lower() for part in path.parts}
    ]
    public_screenshots = [
        path for path in image_files if "screenshots-public" in {part.lower() for part in path.parts}
    ]
    generated_outputs = [
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
        "image_files": image_files,
        "raw_screenshots": raw_screenshots,
        "public_screenshots": public_screenshots,
        "generated_outputs": generated_outputs,
        "handoffs": handoffs,
        "linkedin": linkedin,
        "secrets": secrets,
        "ignored": ignored,
    }


def run_evidence_validator(project_path: Path, repo_root: Path) -> dict:
    validator = repo_root / "tools" / "evidence-validator" / "evidence_validator.py"
    if not validator.exists():
        return {"available": False, "status": None, "warnings": ["evidence-validator was not found"]}
    code, stdout, stderr = run_command(
        [sys.executable, str(validator), "--project-path", str(project_path), "--json"],
        repo_root,
    )
    if code != 0:
        return {
            "available": True,
            "status": None,
            "warnings": [f"evidence-validator failed with exit code {code}"],
            "stderr": stderr,
        }
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return {
            "available": True,
            "status": None,
            "warnings": ["evidence-validator output was not valid JSON"],
        }
    return {
        "available": True,
        "status": data.get("status"),
        "warnings": data.get("warnings", []),
        "blockers": data.get("blockers", []),
        "missing_readme_refs": data.get("missing_readme_refs", []),
        "valid_readme_refs": data.get("valid_readme_refs", []),
        "secret_like_files": data.get("secret_like_files", []),
    }


def inspect_security_report(path: Path | None, project_path: Path) -> dict:
    if not path:
        return {"provided": False, "status": "not provided", "blockers": [], "warnings": []}
    candidate = path if path.is_absolute() else project_path / path
    if not candidate.exists() or not candidate.is_file():
        return {
            "provided": True,
            "status": "missing",
            "blockers": [],
            "warnings": [f"security report was not found: {candidate}"],
        }
    if is_secret_like(candidate):
        return {
            "provided": True,
            "status": "unsafe path",
            "blockers": [f"security report path is secret-like and was not read: {candidate.name}"],
            "warnings": [],
        }
    text = read_text_if_safe(candidate)
    lowered = text.lower()
    blockers: list[str] = []
    if "critical" in lowered and re.search(r"critical[^0-9]*(?:[1-9]|\btrue\b)", lowered):
        blockers.append("security report appears to include Critical findings")
    if "high" in lowered and re.search(r"high[^0-9]*(?:[1-9]|\btrue\b)", lowered):
        blockers.append("security report appears to include High findings")
    if "not ready" in lowered or "do not publish" in lowered:
        blockers.append("security report indicates the project is not ready for public use")
    status = "reviewed"
    return {"provided": True, "status": status, "blockers": blockers, "warnings": []}


def determine_decision(blockers: list[str], warnings: list[str], project_path: Path, readme_exists: bool) -> str:
    if any("credentialed git remote" in item.lower() for item in blockers):
        return "BLOCKED"
    if any("secret" in item.lower() or ".env" in item.lower() for item in blockers):
        return "BLOCKED"
    if blockers:
        return "NEEDS FIXES"
    if not readme_exists:
        return "NEEDS FIXES"
    # Documentation-only projects may remain READY with local-only warnings if
    # those artifacts are ignored or excluded from the public candidate set.
    return "READY FOR REVIEW"


def review_project(project_path: Path, security_report: Path | None = None) -> CheckResult:
    project_path = project_path.resolve()
    repo_root = find_repo_root(project_path)
    warnings: list[str] = []
    blockers: list[str] = []
    blocked_files: list[str] = []
    local_only_files: list[str] = []
    safe_files: list[str] = []

    if not project_path.exists() or not project_path.is_dir():
        return CheckResult(
            status="BLOCKED",
            blockers=[f"project path does not exist or is not a directory: {project_path}"],
        )

    readme_path = project_path / "README.md"
    readme_exists = readme_path.exists() and readme_path.is_file() and not is_secret_like(readme_path)
    readme_text = read_text_if_safe(readme_path) if readme_exists else ""
    if not readme_exists:
        blockers.append("README.md is missing or unsafe to read")
    elif not re.search(r"^#\s+\S+", readme_text, re.MULTILINE):
        warnings.append("README.md does not appear to have a clear H1 title")
    if TODO_RE.search(readme_text):
        warnings.append("README.md contains placeholder/TODO-style language")

    refs = parse_readme_image_refs(readme_text)
    valid_refs: list[str] = []
    missing_refs: list[str] = []
    public_refs: list[str] = []
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
        if "screenshots-public" in rel_ref:
            public_refs.append(ref)
        if "/screenshots/" in rel_ref or "\\screenshots\\" in rel_ref:
            raw_refs.append(ref)
    if missing_refs:
        blockers.append("README image references do not match local files")
    if raw_refs:
        blockers.append("README links to raw screenshots instead of public screenshots")
    if refs and not public_refs:
        warnings.append("README has image refs, but none point to screenshots-public")

    files = collect_files(project_path, repo_root)
    ignored = files["ignored"]

    public_screenshots = files["public_screenshots"]
    raw_screenshots = files["raw_screenshots"]
    if refs and not public_screenshots:
        blockers.append("README references screenshots, but screenshots-public files were not found")
    for path in public_screenshots:
        if ignored.get(path, False):
            blockers.append("public screenshot is ignored by git")
            blocked_files.append(rel(path, repo_root))
        else:
            safe_files.append(rel(path, repo_root))
    for path in raw_screenshots:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            blockers.append("raw screenshot is not ignored/local-only")
            blocked_files.append(rel(path, repo_root))

    for path in files["generated_outputs"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            blockers.append("generated output file is not ignored/local-only")
            blocked_files.append(rel(path, repo_root))
    for path in files["handoffs"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            blockers.append("HANDOFF file is not ignored/local-only")
            blocked_files.append(rel(path, repo_root))
    for path in files["linkedin"]:
        if ignored.get(path, False):
            local_only_files.append(rel(path, repo_root))
        else:
            blockers.append("LinkedIn draft is not ignored/local-only")
            blocked_files.append(rel(path, repo_root))

    for path in files["secrets"]:
        blockers.append("secret-like filename found; contents were not read")
        blocked_files.append(rel(path, repo_root))

    docs_dir = project_path / "docs"
    queries_dir = project_path / "queries"
    if docs_dir.exists() and docs_dir.is_dir():
        safe_files.extend(rel(path, repo_root) for path in sorted(docs_dir.glob("*.md")) if not is_secret_like(path))
    else:
        warnings.append("docs/ folder was not found")
    if queries_dir.exists() and queries_dir.is_dir():
        safe_files.extend(rel(path, repo_root) for path in sorted(queries_dir.glob("*")) if path.is_file() and not is_secret_like(path))
    else:
        warnings.append("queries/ folder was not found")
    if readme_exists:
        safe_files.append(rel(readme_path, repo_root))

    remote_code, remote_stdout, _ = run_command(["git", "remote", "-v"], repo_root)
    credentialed_remotes: list[str] = []
    if remote_code == 0:
        for line in remote_stdout.splitlines():
            if CREDENTIALED_REMOTE_RE.search(line):
                credentialed_remotes.append(re.sub(CREDENTIALED_REMOTE_RE, "://<redacted>@", line))
    if credentialed_remotes:
        blockers.append("credentialed git remote detected")

    project_pathspec = rel(project_path, repo_root)
    status_code, status_stdout, _ = run_command(["git", "status", "--short", "--", project_pathspec], repo_root)
    git_status = status_stdout.splitlines() if status_code == 0 and status_stdout else []

    evidence = run_evidence_validator(project_path, repo_root)
    if evidence.get("blockers"):
        blockers.extend(f"evidence-validator: {item}" for item in evidence["blockers"])
    if evidence.get("secret_like_files"):
        blockers.append("evidence-validator found secret-like files")
    if evidence.get("missing_readme_refs"):
        blockers.append("evidence-validator found missing README image references")
    if evidence.get("warnings"):
        warnings.extend(f"evidence-validator: {item}" for item in evidence["warnings"])

    security = inspect_security_report(security_report, project_path)
    blockers.extend(security.get("blockers", []))
    warnings.extend(security.get("warnings", []))

    status = determine_decision(blockers, warnings, project_path, readme_exists)
    return CheckResult(
        status=status,
        warnings=sorted(set(warnings)),
        blockers=sorted(set(blockers)),
        safe_files=sorted(set(safe_files)),
        local_only_files=sorted(set(local_only_files)),
        blocked_files=sorted(set(blocked_files)),
        details={
            "project_name": project_path.name,
            "project_path": str(project_path),
            "repo_root": str(repo_root),
            "reviewed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "readme_exists": readme_exists,
            "readme_image_refs": refs,
            "valid_readme_refs": valid_refs,
            "missing_readme_refs": missing_refs,
            "public_screenshots": [rel(path, repo_root) for path in public_screenshots],
            "raw_screenshots": [rel(path, repo_root) for path in raw_screenshots],
            "credentialed_remotes": credentialed_remotes,
            "git_status": git_status,
            "git_remote_checked": remote_code == 0,
            "evidence_validator": evidence,
            "security_report": security,
        },
    )


def as_dict(result: CheckResult) -> dict:
    return {
        "status": result.status,
        "warnings": result.warnings,
        "blockers": result.blockers,
        "safe_files": result.safe_files,
        "local_only_files": result.local_only_files,
        "blocked_files": result.blocked_files,
        **result.details,
    }


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def render_markdown(result: CheckResult) -> str:
    details = result.details
    evidence = details.get("evidence_validator", {})
    security = details.get("security_report", {})
    return f"""# GitHub Readiness Report

## Project

- Project name: {details.get("project_name")}
- Path: {details.get("project_path")}
- Review date: {details.get("reviewed_at")}
- Reviewer workflow: read-only GitHub readiness wrapper
- Readiness status: {result.status}

## Summary

This report inspected local files, README image references, public screenshot placement, local-only artifact boundaries, secret-like filenames, local Git remotes, project-scoped Git status, and evidence-validator output. No files were staged, committed, pushed, moved, deleted, renamed, published, or scanned externally.

## Safe Files

{list_or_none(result.safe_files)}

## Blocked Files

{list_or_none(result.blocked_files)}

## Local-Only Files

{list_or_none(result.local_only_files)}

## Evidence Status

- Evidence validator available: {yes_no(bool(evidence.get("available")))}
- Evidence validator status: {evidence.get("status") or "not available"}
- Evidence validator blockers:
{list_or_none(evidence.get("blockers", []))}
- Evidence validator warnings:
{list_or_none(evidence.get("warnings", []))}

## Screenshot Status

- Public screenshots:
{list_or_none(details.get("public_screenshots", []))}
- Raw screenshots:
{list_or_none(details.get("raw_screenshots", []))}
- Broken README references:
{list_or_none(details.get("missing_readme_refs", []))}

## README Status

- README exists: {yes_no(bool(details.get("readme_exists")))}
- README image references:
{list_or_none(details.get("readme_image_refs", []))}
- Valid README image references:
{list_or_none(details.get("valid_readme_refs", []))}

## Duplicate / Source-of-Truth Status

- Duplicate scan: not implemented in this first read-only wrapper.
- Recommended source of truth: {details.get("project_path")}
- Action required before GitHub: review manually if duplicate folders are suspected.

## Security Review Status

- Security report provided: {yes_no(bool(security.get("provided")))}
- Security report status: {security.get("status")}
- Must-fix blockers:
{list_or_none(security.get("blockers", []))}
- Review gaps:
{list_or_none(security.get("warnings", []))}

## Git Status

{list_or_none(details.get("git_status", []))}

## Git Remote Check

- Git remote checked: {yes_no(bool(details.get("git_remote_checked")))}
- Credentialed remotes:
{list_or_none(details.get("credentialed_remotes", []))}

## Remaining Blockers

{list_or_none(result.blockers)}

## Warnings

{list_or_none(result.warnings)}

## Final Human Approval Required

- Git add approved: no
- Commit approved: no
- Push approved: no
- Public screenshots approved: no
- Local-only exclusions reviewed: no
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only GitHub readiness wrapper.")
    parser.add_argument("--project-path", required=True, help="Project folder to inspect.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown.")
    parser.add_argument("--security-report", help="Optional security report path, relative to project path or absolute.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    result = review_project(Path(args.project_path), Path(args.security_report) if args.security_report else None)
    if args.json:
        print(json.dumps(as_dict(result), indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
