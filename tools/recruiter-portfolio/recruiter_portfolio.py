#!/usr/bin/env python3
"""Read-only recruiter portfolio presentation layer.

Generates a recruiter-facing markdown and JSON summary from local portfolio
files. It does not stage, commit, push, move, delete, rename, publish, call
external APIs, run live scans, or read secret-like file contents.
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
PROJECT_MARKERS = {"README.md", "docs", "evidence", "queries", "src", "app", "tests", "pyproject.toml"}
READY_STATUSES = ("WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY", "NEEDS REVIEW", "LOCAL ONLY", "INCOMPLETE")
SKILL_RULES = (
    ("Wazuh", ("wazuh",)),
    ("SIEM", ("siem", "wazuh", "splunk", "security log")),
    ("Windows Event Logs", ("windows event", "event id", "event viewer", "eventviewer", "4625")),
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
class ProjectCard:
    name: str
    path: str
    status: str
    headline: str
    skill_tags: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    cleanup_warnings: list[str] = field(default_factory=list)
    local_only_warnings: list[str] = field(default_factory=list)
    github_pin_candidate: bool = False
    linkedin_feature_candidate: bool = False
    score: int = 0


@dataclass
class RecruiterPortfolio:
    repo_path: str
    reviewed_at: str
    story_summary: str
    featured_projects: list[ProjectCard]
    github_pin_candidates: list[ProjectCard]
    linkedin_feature_candidates: list[ProjectCard]
    cleanup_warnings: list[str]
    skill_map: dict[str, list[str]]
    all_projects: list[ProjectCard]


def is_secret_like(path: Path) -> bool:
    if path.suffix.lower() in SECRET_EXTENSIONS:
        return True
    return any(pattern.search(path.name) for pattern in SECRET_NAME_PATTERNS)


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_walk(root: Path, max_depth: int = 3) -> Iterable[Path]:
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


def read_text_if_safe(path: Path, max_chars: int = 16000) -> str:
    if is_secret_like(path):
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:max_chars]
    except OSError:
        return ""


def child_names(path: Path) -> set[str]:
    try:
        return {child.name for child in path.iterdir()}
    except OSError:
        return set()


def is_project_candidate(path: Path, repo_root: Path) -> bool:
    if path == repo_root:
        return False
    names = child_names(path)
    markers = len(PROJECT_MARKERS.intersection(names))
    if markers >= 2:
        return True
    if "README.md" in names and path.parent == repo_root:
        return True
    if path.parent.name in {"blue-team-labs", "labs", "security-plus-projects", "tools"} and markers >= 1:
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
    for relative in ("README.md", "docs/findings.md", "docs/investigation.md", "docs/project-closeout-report.md"):
        candidate = project_path / relative
        if candidate.exists() and candidate.is_file():
            text_parts.append(read_text_if_safe(candidate))
    combined = "\n".join(text_parts).lower()
    tags = [tag for tag, needles in SKILL_RULES if any(needle in combined for needle in needles)]
    return sorted(set(tags))


def status_for(path: Path) -> str:
    has_readme = (path / "README.md").is_file()
    has_docs = (path / "docs").is_dir()
    has_evidence = (path / "evidence").is_dir()
    has_public_screens = (path / "evidence" / "screenshots-public").is_dir()
    has_github_report = bool(list((path / "docs").glob("*github-readiness*.md"))) if has_docs else False
    has_closeout = (path / "docs" / "project-closeout-report.md").is_file()
    has_outputs = (path / "outputs").exists() or (path / "agent-output").exists()
    has_handoff = any(HANDOFF_RE.search(name) for name in child_names(path))
    if has_github_report and has_closeout and has_public_screens:
        return "WORKFLOW READY"
    if has_closeout:
        return "CLOSEOUT READY"
    if has_github_report or (has_readme and has_evidence and has_public_screens):
        return "GITHUB READY"
    if (has_outputs or has_handoff) and not has_readme:
        return "LOCAL ONLY"
    if has_readme and (has_docs or has_evidence or path.parent.name == "tools"):
        return "NEEDS REVIEW"
    return "INCOMPLETE"


def headline_for(path: Path, tags: list[str]) -> str:
    readme = read_text_if_safe(path / "README.md")
    for line in readme.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped.lstrip("# ").strip()
    if tags:
        return f"{path.name.replace('-', ' ').title()} - {', '.join(tags[:2])}"
    return path.name.replace("-", " ").title()


def inspect_project(path: Path, repo_root: Path) -> ProjectCard:
    names = child_names(path)
    status = status_for(path)
    tags = infer_skill_tags(path, repo_root)
    has_readme = (path / "README.md").is_file()
    has_docs = (path / "docs").is_dir()
    has_evidence = (path / "evidence").is_dir()
    has_public_screens = (path / "evidence" / "screenshots-public").is_dir()
    has_queries = (path / "queries").is_dir()
    has_outputs = any(name in LOCAL_ONLY_DIR_NAMES for name in names)
    has_handoff = any(HANDOFF_RE.search(name) for name in names)
    has_linkedin = any(LINKEDIN_RE.search(str(item)) for item in safe_walk(path, max_depth=3))

    reasons: list[str] = []
    if status in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY"}:
        reasons.append("public-safe review artifacts present")
    if has_public_screens:
        reasons.append("public-safe screenshots present")
    if has_queries:
        reasons.append("investigation queries documented")
    if tags:
        reasons.append(f"skills: {', '.join(tags[:4])}")

    cleanup: list[str] = []
    if not has_readme:
        cleanup.append("missing README")
    if has_evidence and not has_public_screens:
        cleanup.append("evidence exists without screenshots-public")
    if has_readme and has_evidence and status == "NEEDS REVIEW":
        cleanup.append("needs readiness/closeout review")
    if status == "INCOMPLETE":
        cleanup.append("incomplete public portfolio structure")

    local_only: list[str] = []
    if has_outputs:
        local_only.append("outputs present")
    if has_handoff:
        local_only.append("HANDOFF present")
    if has_linkedin:
        local_only.append("LinkedIn/local-only draft detected")

    score = score_project(status, tags, has_readme, has_docs, has_evidence, has_public_screens, has_queries)
    return ProjectCard(
        name=path.name,
        path=rel(path, repo_root),
        status=status,
        headline=headline_for(path, tags),
        skill_tags=tags,
        reasons=reasons,
        cleanup_warnings=cleanup,
        local_only_warnings=local_only,
        github_pin_candidate=status in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY"},
        linkedin_feature_candidate=status in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY"} and bool(tags),
        score=score,
    )


def score_project(status: str, tags: list[str], has_readme: bool, has_docs: bool, has_evidence: bool, has_public_screens: bool, has_queries: bool) -> int:
    score = {"WORKFLOW READY": 100, "CLOSEOUT READY": 90, "GITHUB READY": 82, "NEEDS REVIEW": 55, "LOCAL ONLY": 25, "INCOMPLETE": 10}[status]
    score += min(len(tags) * 2, 12)
    score += 4 if has_readme else 0
    score += 3 if has_docs else 0
    score += 3 if has_evidence else 0
    score += 5 if has_public_screens else 0
    score += 3 if has_queries else 0
    return min(score, 120)


def build_portfolio(repo_path: Path) -> RecruiterPortfolio:
    repo_root = repo_path.resolve()
    projects = [inspect_project(path, repo_root) for path in discover_project_dirs(repo_root)]
    featured = sorted(
        [project for project in projects if project.status in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY", "NEEDS REVIEW"} and project.skill_tags],
        key=lambda item: (-item.score, item.path),
    )[:8]
    github_pins = [project for project in featured if project.github_pin_candidate][:6]
    linkedin = [project for project in featured if project.linkedin_feature_candidate][:8]
    cleanup = cleanup_warning_lines(projects)
    return RecruiterPortfolio(
        repo_path=str(repo_root),
        reviewed_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        story_summary=story_summary(featured),
        featured_projects=featured,
        github_pin_candidates=github_pins,
        linkedin_feature_candidates=linkedin,
        cleanup_warnings=cleanup,
        skill_map=build_skill_map(projects),
        all_projects=projects,
    )


def story_summary(featured: list[ProjectCard]) -> str:
    if not featured:
        return "The portfolio is still being organized into recruiter-facing SOC and blue-team projects."
    return (
        "This portfolio presents a SOC and blue-team workflow: investigate real security logs, "
        "validate evidence, prepare public-safe screenshots, document findings, and use local "
        "readiness wrappers before GitHub or recruiter review."
    )


def build_skill_map(projects: list[ProjectCard]) -> dict[str, list[str]]:
    skill_map: dict[str, list[str]] = {}
    for project in projects:
        if project.status not in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY", "NEEDS REVIEW"}:
            continue
        for tag in project.skill_tags:
            skill_map.setdefault(tag, [])
            if len(skill_map[tag]) < 6:
                skill_map[tag].append(project.path)
    return dict(sorted(skill_map.items()))


def cleanup_warning_lines(projects: list[ProjectCard]) -> list[str]:
    lines: list[str] = []
    for project in projects:
        if project.cleanup_warnings:
            lines.append(f"{project.path}: {', '.join(project.cleanup_warnings)}")
        if project.local_only_warnings and project.status not in {"WORKFLOW READY", "CLOSEOUT READY", "GITHUB READY"}:
            lines.append(f"{project.path}: local-only artifacts present ({', '.join(project.local_only_warnings)})")
        if len(lines) >= 20:
            break
    return lines


def project_to_dict(project: ProjectCard) -> dict:
    return {
        "name": project.name,
        "path": project.path,
        "status": project.status,
        "headline": project.headline,
        "skill_tags": project.skill_tags,
        "reasons": project.reasons,
        "cleanup_warnings": project.cleanup_warnings,
        "local_only_warnings": project.local_only_warnings,
        "github_pin_candidate": project.github_pin_candidate,
        "linkedin_feature_candidate": project.linkedin_feature_candidate,
        "score": project.score,
    }


def as_dict(portfolio: RecruiterPortfolio) -> dict:
    return {
        "repo_path": portfolio.repo_path,
        "reviewed_at": portfolio.reviewed_at,
        "story_summary": portfolio.story_summary,
        "top_featured_projects": [project_to_dict(project) for project in portfolio.featured_projects],
        "skill_map": portfolio.skill_map,
        "github_pin_candidates": [project_to_dict(project) for project in portfolio.github_pin_candidates],
        "linkedin_feature_candidates": [project_to_dict(project) for project in portfolio.linkedin_feature_candidates],
        "cleanup_warnings": portfolio.cleanup_warnings,
        "all_projects": [project_to_dict(project) for project in portfolio.all_projects],
    }


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def project_list(projects: list[ProjectCard]) -> str:
    if not projects:
        return "- None found"
    rows = []
    for project in projects:
        tags = ", ".join(project.skill_tags[:5])
        rows.append(f"- `{project.path}` - {project.status} - {project.headline} ({tags})")
    return "\n".join(rows)


def skill_map_markdown(skill_map: dict[str, list[str]]) -> str:
    if not skill_map:
        return "- None found"
    rows = []
    for skill, paths in skill_map.items():
        rows.append(f"- {skill}: {', '.join(f'`{path}`' for path in paths[:4])}")
    return "\n".join(rows)


def render_markdown(portfolio: RecruiterPortfolio) -> str:
    return f"""# Recruiter Portfolio Summary

## SOC / Blue-Team Story

{portfolio.story_summary}

## Top Featured Projects

{project_list(portfolio.featured_projects)}

## Skill Map

{skill_map_markdown(portfolio.skill_map)}

## GitHub Pin Candidates

{project_list(portfolio.github_pin_candidates)}

## LinkedIn Feature Candidates

{project_list(portfolio.linkedin_feature_candidates)}

## Cleanup Warnings

{list_or_none(portfolio.cleanup_warnings)}

## Safety Boundary

- Report-only: yes
- Git actions run: no
- External APIs run: no
- Live scans run: no
- Secret-like file contents read: no
"""


def write_outputs(portfolio: RecruiterPortfolio, output: Path) -> list[str]:
    if output.suffix.lower() in {".md", ".json"}:
        output.parent.mkdir(parents=True, exist_ok=True)
        markdown_path = output if output.suffix.lower() == ".md" else output.with_suffix(".md")
        json_path = output if output.suffix.lower() == ".json" else output.with_suffix(".json")
    else:
        output.mkdir(parents=True, exist_ok=True)
        markdown_path = output / "recruiter-portfolio.md"
        json_path = output / "recruiter-portfolio.json"
    markdown_path.write_text(render_markdown(portfolio), encoding="utf-8")
    json_path.write_text(json.dumps(as_dict(portfolio), indent=2), encoding="utf-8")
    return [str(markdown_path), str(json_path)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only recruiter portfolio presentation generator.")
    parser.add_argument("--repo-path", default=".", help="Repository path to scan.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    parser.add_argument("--output", help="Optional output file or directory for markdown and JSON reports.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    portfolio = build_portfolio(Path(args.repo_path))
    report_paths: list[str] = []
    if args.output:
        report_paths = write_outputs(portfolio, Path(args.output))
    if args.json:
        payload = as_dict(portfolio)
        payload["generated_report_paths"] = report_paths
        print(json.dumps(payload, indent=2))
    else:
        text = render_markdown(portfolio)
        if report_paths:
            text += "\n## Generated Report Paths\n\n" + list_or_none(report_paths) + "\n"
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
