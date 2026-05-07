#!/usr/bin/env python3
"""Read-only portfolio index generator.

Scans local portfolio files and produces a recruiter-friendly inventory. It
does not stage, commit, push, move, delete, rename, publish, call external APIs,
run live scans, or read secret-like file contents.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


CLASSIFICATIONS = (
    "WORKFLOW READY",
    "CLOSEOUT READY",
    "GITHUB READY",
    "NEEDS REVIEW",
    "LOCAL ONLY",
    "INCOMPLETE",
)
SKIP_DIR_NAMES = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}
LOCAL_ONLY_DIR_NAMES = {"outputs", "output", "agent-output", "linkedin-drafts", "drafts", "reports"}
SECRET_EXTENSIONS = {".pem", ".p12", ".pfx", ".key"}
SECRET_NAME_PATTERNS = (
    re.compile(r"(^|[._-])\.?env($|[._-])", re.IGNORECASE),
    re.compile(r"(secret|credential|token|apikey|api_key|access_key)", re.IGNORECASE),
    re.compile(r"(password|passwd|pwd|cookie)", re.IGNORECASE),
    re.compile(r"(^|[._-])id_rsa($|[._-])", re.IGNORECASE),
    re.compile(r"(^|[._-])private[_-]?key($|[._-])", re.IGNORECASE),
)
HANDOFF_RE = re.compile(r"handoff", re.IGNORECASE)
LINKEDIN_RE = re.compile(r"(linkedin|social[-_]post|post[-_]draft)", re.IGNORECASE)
PROJECT_MARKERS = {
    "README.md",
    "docs",
    "evidence",
    "queries",
    "src",
    "app",
    "tests",
    "pyproject.toml",
    "package.json",
}
TOOL_DIRS = {"tools", "supervisor-agent", "vuln-agent", "job-search-agent", "job-tailor"}
SKILL_RULES = (
    ("Wazuh", ("wazuh",)),
    ("SIEM", ("siem", "security information and event management", "wazuh", "splunk")),
    ("Windows Event Logs", ("windows event", "event id", "eventviewer", "event viewer", "4625")),
    ("Threat Hunting", ("threat hunting", "hunt", "powershell")),
    ("Detection Engineering", ("detection", "sigma", "yara", "rule")),
    ("Incident Response", ("incident response", "triage", "alert", "investigation")),
    ("Malware Analysis", ("malware", "yara")),
    ("YARA", ("yara",)),
    ("Sigma", ("sigma",)),
    ("Python Automation", ("python", ".py", "automation", "orchestrator", "validator")),
    ("GitHub Workflow", ("github", "readiness", "closeout", "gitignore")),
    ("Blue Team", ("blue team", "blue-team", "soc", "defensive")),
    ("SOC Operations", ("soc", "alert", "triage", "event id", "failed login")),
)


@dataclass
class ProjectInfo:
    name: str
    path: str
    classification: str
    skill_tags: list[str] = field(default_factory=list)
    has_readme: bool = False
    has_docs: bool = False
    has_evidence: bool = False
    has_screenshots_public: bool = False
    has_queries: bool = False
    is_tool: bool = False
    orchestrator_compatible: bool = False
    has_github_readiness: bool = False
    has_closeout_report: bool = False
    has_outputs: bool = False
    has_handoff: bool = False
    has_linkedin: bool = False
    safe_candidate: bool = False
    cleanup_reasons: list[str] = field(default_factory=list)
    local_only_reasons: list[str] = field(default_factory=list)


@dataclass
class PortfolioIndex:
    repo_path: str
    reviewed_at: str
    projects: list[ProjectInfo]
    warnings: list[str] = field(default_factory=list)


def is_secret_like(path: Path) -> bool:
    name = path.name
    if path.suffix.lower() in SECRET_EXTENSIONS:
        return True
    return any(pattern.search(name) for pattern in SECRET_NAME_PATTERNS)


def safe_walk(root: Path, max_depth: int = 4) -> Iterable[Path]:
    root = root.resolve()
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        try:
            depth = len(current_path.resolve().relative_to(root).parts)
        except ValueError:
            depth = 0
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_DIR_NAMES
            and not is_secret_like(current_path / name)
            and depth < max_depth
        ]
        for filename in files:
            path = current_path / filename
            if not is_secret_like(path):
                yield path


def read_text_if_safe(path: Path, max_chars: int = 12000) -> str:
    if is_secret_like(path):
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def child_names(path: Path) -> set[str]:
    try:
        return {child.name for child in path.iterdir()}
    except OSError:
        return set()


def has_any_file(path: Path, pattern: str) -> bool:
    try:
        return any(path.glob(pattern))
    except OSError:
        return False


def is_project_candidate(path: Path, repo_root: Path) -> bool:
    if path == repo_root:
        return False
    names = child_names(path)
    marker_count = len(PROJECT_MARKERS.intersection(names))
    if marker_count >= 2:
        return True
    if "README.md" in names and path.parent == repo_root:
        return True
    if path.parent.name in {"blue-team-labs", "labs", "security-plus-projects", "tools"} and marker_count >= 1:
        return True
    return False


def discover_project_dirs(repo_root: Path) -> list[Path]:
    candidates: set[Path] = set()
    for current, dirs, _ in os.walk(repo_root):
        current_path = Path(current)
        try:
            depth = len(current_path.resolve().relative_to(repo_root.resolve()).parts)
        except ValueError:
            depth = 0
        dirs[:] = [
            name
            for name in dirs
            if name not in SKIP_DIR_NAMES
            and not is_secret_like(current_path / name)
            and depth < 3
        ]
        if is_project_candidate(current_path, repo_root):
            candidates.add(current_path)
            dirs[:] = []
    return sorted(candidates)


def infer_skill_tags(project_path: Path, repo_root: Path) -> list[str]:
    text_parts = [project_path.name, rel(project_path, repo_root)]
    for relative in ("README.md", "docs/findings.md", "docs/investigation.md", "queries/eventviewer-queries.txt"):
        candidate = project_path / relative
        if candidate.exists() and candidate.is_file():
            text_parts.append(read_text_if_safe(candidate))
    combined = "\n".join(text_parts).lower()
    tags = [tag for tag, needles in SKILL_RULES if any(needle in combined for needle in needles)]
    return sorted(set(tags))


def classify_project(
    has_readme: bool,
    has_docs: bool,
    has_evidence: bool,
    has_screenshots_public: bool,
    has_queries: bool,
    has_github_readiness: bool,
    has_closeout_report: bool,
    has_outputs: bool,
    has_handoff: bool,
    is_tool: bool,
) -> str:
    if has_github_readiness and has_closeout_report and has_screenshots_public:
        return "WORKFLOW READY"
    if has_closeout_report:
        return "CLOSEOUT READY"
    if has_github_readiness or (has_readme and has_screenshots_public and (has_docs or has_evidence)):
        return "GITHUB READY"
    if has_outputs and not has_readme:
        return "LOCAL ONLY"
    if has_handoff and not has_readme:
        return "LOCAL ONLY"
    if has_readme and (has_docs or has_evidence or has_queries or is_tool):
        return "NEEDS REVIEW"
    return "INCOMPLETE"


def inspect_project(project_path: Path, repo_root: Path) -> ProjectInfo:
    names = child_names(project_path)
    has_readme = (project_path / "README.md").is_file()
    has_docs = (project_path / "docs").is_dir()
    has_evidence = (project_path / "evidence").is_dir()
    has_screenshots_public = (project_path / "evidence" / "screenshots-public").is_dir()
    has_queries = (project_path / "queries").is_dir()
    is_tool = project_path.parent.name == "tools" or project_path.name in TOOL_DIRS
    has_github_readiness = has_any_file(project_path / "docs", "*github-readiness*.md")
    has_closeout_report = (project_path / "docs" / "project-closeout-report.md").is_file()
    has_outputs = any(name in LOCAL_ONLY_DIR_NAMES for name in names)
    has_handoff = any(HANDOFF_RE.search(name) for name in names)
    has_linkedin = any(LINKEDIN_RE.search(str(path)) for path in safe_walk(project_path, max_depth=3))
    orchestrator_compatible = has_readme and (has_docs or has_evidence or has_queries)

    classification = classify_project(
        has_readme,
        has_docs,
        has_evidence,
        has_screenshots_public,
        has_queries,
        has_github_readiness,
        has_closeout_report,
        has_outputs,
        has_handoff,
        is_tool,
    )
    cleanup_reasons: list[str] = []
    if not has_readme:
        cleanup_reasons.append("missing README")
    if has_evidence and not has_screenshots_public:
        cleanup_reasons.append("evidence exists without screenshots-public")
    if has_readme and has_evidence and not has_github_readiness:
        cleanup_reasons.append("missing GitHub readiness artifact")
    if has_github_readiness and not has_closeout_report:
        cleanup_reasons.append("missing project closeout report")

    local_only_reasons: list[str] = []
    if has_outputs:
        local_only_reasons.append("outputs present")
    if has_handoff:
        local_only_reasons.append("HANDOFF present")
    if has_linkedin:
        local_only_reasons.append("LinkedIn/local-only draft detected")

    return ProjectInfo(
        name=project_path.name,
        path=rel(project_path, repo_root),
        classification=classification,
        skill_tags=infer_skill_tags(project_path, repo_root),
        has_readme=has_readme,
        has_docs=has_docs,
        has_evidence=has_evidence,
        has_screenshots_public=has_screenshots_public,
        has_queries=has_queries,
        is_tool=is_tool,
        orchestrator_compatible=orchestrator_compatible,
        has_github_readiness=has_github_readiness,
        has_closeout_report=has_closeout_report,
        has_outputs=has_outputs,
        has_handoff=has_handoff,
        has_linkedin=has_linkedin,
        safe_candidate=classification in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY"},
        cleanup_reasons=cleanup_reasons,
        local_only_reasons=local_only_reasons,
    )


def generate_index(repo_path: Path) -> PortfolioIndex:
    repo_root = repo_path.resolve()
    projects = [inspect_project(path, repo_root) for path in discover_project_dirs(repo_root)]
    return PortfolioIndex(
        repo_path=str(repo_root),
        reviewed_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        projects=projects,
    )


def project_to_dict(project: ProjectInfo) -> dict:
    return {
        "name": project.name,
        "path": project.path,
        "classification": project.classification,
        "skill_tags": project.skill_tags,
        "has_readme": project.has_readme,
        "has_docs": project.has_docs,
        "has_evidence": project.has_evidence,
        "has_screenshots_public": project.has_screenshots_public,
        "has_queries": project.has_queries,
        "is_tool": project.is_tool,
        "orchestrator_compatible": project.orchestrator_compatible,
        "has_github_readiness": project.has_github_readiness,
        "has_closeout_report": project.has_closeout_report,
        "has_outputs": project.has_outputs,
        "has_handoff": project.has_handoff,
        "has_linkedin": project.has_linkedin,
        "safe_candidate": project.safe_candidate,
        "cleanup_reasons": project.cleanup_reasons,
        "local_only_reasons": project.local_only_reasons,
    }


def as_dict(index: PortfolioIndex) -> dict:
    counts = {status: 0 for status in CLASSIFICATIONS}
    for project in index.projects:
        counts[project.classification] = counts.get(project.classification, 0) + 1
    return {
        "repo_path": index.repo_path,
        "reviewed_at": index.reviewed_at,
        "summary": {
            "total_projects": len(index.projects),
            "classification_counts": counts,
        },
        "suggested_recruiter_projects": [project_to_dict(p) for p in suggested_recruiter_projects(index.projects)],
        "suggested_cleanup_targets": [project_to_dict(p) for p in suggested_cleanup_targets(index.projects)],
        "suggested_archive_local_only_targets": [project_to_dict(p) for p in suggested_archive_targets(index.projects)],
        "projects": [project_to_dict(project) for project in index.projects],
        "warnings": index.warnings,
    }


def suggested_recruiter_projects(projects: list[ProjectInfo]) -> list[ProjectInfo]:
    status_rank = {"WORKFLOW READY": 0, "CLOSEOUT READY": 1, "GITHUB READY": 2, "NEEDS REVIEW": 3}
    candidates = [p for p in projects if p.classification in status_rank and p.skill_tags]
    return sorted(candidates, key=lambda p: (status_rank[p.classification], -len(p.skill_tags), p.path))[:10]


def suggested_cleanup_targets(projects: list[ProjectInfo]) -> list[ProjectInfo]:
    targets = [p for p in projects if p.cleanup_reasons or p.classification in {"NEEDS REVIEW", "INCOMPLETE"}]
    return sorted(targets, key=lambda p: (p.classification, p.path))[:15]


def suggested_archive_targets(projects: list[ProjectInfo]) -> list[ProjectInfo]:
    targets = [p for p in projects if p.classification == "LOCAL ONLY" or p.local_only_reasons]
    return sorted(targets, key=lambda p: (p.classification != "LOCAL ONLY", p.path))[:15]


def bool_mark(value: bool) -> str:
    return "yes" if value else "no"


def render_table(projects: list[ProjectInfo]) -> str:
    rows = [
        "| Project | Status | README | Docs | Evidence | Public Screens | Queries | Tags |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for project in projects:
        tags = ", ".join(project.skill_tags[:5])
        rows.append(
            f"| `{project.path}` | {project.classification} | {bool_mark(project.has_readme)} | "
            f"{bool_mark(project.has_docs)} | {bool_mark(project.has_evidence)} | "
            f"{bool_mark(project.has_screenshots_public)} | {bool_mark(project.has_queries)} | {tags} |"
        )
    return "\n".join(rows)


def render_markdown(index: PortfolioIndex) -> str:
    data = as_dict(index)
    counts = data["summary"]["classification_counts"]
    recruiter = suggested_recruiter_projects(index.projects)
    cleanup = suggested_cleanup_targets(index.projects)
    archive = suggested_archive_targets(index.projects)
    all_tags = sorted({tag for project in index.projects for tag in project.skill_tags})
    return f"""# Portfolio Index

## Summary

- Repo path: `{index.repo_path}`
- Reviewed at: `{index.reviewed_at}`
- Projects/tools detected: {len(index.projects)}
- WORKFLOW READY: {counts.get("WORKFLOW READY", 0)}
- CLOSEOUT READY: {counts.get("CLOSEOUT READY", 0)}
- GITHUB READY: {counts.get("GITHUB READY", 0)}
- NEEDS REVIEW: {counts.get("NEEDS REVIEW", 0)}
- LOCAL ONLY: {counts.get("LOCAL ONLY", 0)}
- INCOMPLETE: {counts.get("INCOMPLETE", 0)}

## Project Inventory

{render_table(index.projects)}

## Detected Skill Tags

{list_or_none(all_tags)}

## Suggested Recruiter-Facing Projects

{project_list(recruiter)}

## Suggested Cleanup Targets

{project_list(cleanup, include_reasons=True)}

## Suggested Archive / Local-Only Targets

{project_list(archive, include_local=True)}

## Safety Boundary

- Report-only: yes
- Git actions run: no
- External APIs run: no
- Live scans run: no
- Secret-like file contents read: no
"""


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def project_list(projects: list[ProjectInfo], include_reasons: bool = False, include_local: bool = False) -> str:
    if not projects:
        return "- None found"
    rows: list[str] = []
    for project in projects:
        extra = ""
        if include_reasons and project.cleanup_reasons:
            extra = f" - {', '.join(project.cleanup_reasons)}"
        if include_local and project.local_only_reasons:
            extra = f" - {', '.join(project.local_only_reasons)}"
        rows.append(f"- `{project.path}` - {project.classification}{extra}")
    return "\n".join(rows)


def write_outputs(index: PortfolioIndex, output: Path) -> list[str]:
    if output.suffix.lower() in {".md", ".json"}:
        output.parent.mkdir(parents=True, exist_ok=True)
        markdown_path = output if output.suffix.lower() == ".md" else output.with_suffix(".md")
        json_path = output if output.suffix.lower() == ".json" else output.with_suffix(".json")
    else:
        output.mkdir(parents=True, exist_ok=True)
        markdown_path = output / "portfolio-index.md"
        json_path = output / "portfolio-index.json"
    markdown_path.write_text(render_markdown(index), encoding="utf-8")
    json_path.write_text(json.dumps(as_dict(index), indent=2), encoding="utf-8")
    return [str(markdown_path), str(json_path)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only portfolio index generator.")
    parser.add_argument("--repo-path", required=True, help="Repository path to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    parser.add_argument("--output", help="Optional output file or directory for markdown and JSON reports.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    index = generate_index(Path(args.repo_path))
    report_paths: list[str] = []
    if args.output:
        report_paths = write_outputs(index, Path(args.output))
    if args.json:
        payload = as_dict(index)
        payload["generated_report_paths"] = report_paths
        print(json.dumps(payload, indent=2))
    else:
        text = render_markdown(index)
        if report_paths:
            text += "\n## Generated Report Paths\n\n" + list_or_none(report_paths) + "\n"
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
