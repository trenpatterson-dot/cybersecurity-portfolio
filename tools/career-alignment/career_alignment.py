#!/usr/bin/env python3
"""Read-only Career Alignment Engine for SOC and blue-team readiness.

The tool inspects local portfolio documentation and evidence structure only.
It does not stage, commit, push, move, delete, rename, publish, call external
APIs, run live scans, or read secret-like file contents.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


READINESS_LEVELS = (
    "EARLY STAGE",
    "DEVELOPING",
    "SOC READY",
    "STRONG JUNIOR CANDIDATE",
    "NEEDS MORE EVIDENCE",
)

SKILL_CATEGORIES = (
    "SIEM",
    "Wazuh",
    "Windows Event Logs",
    "Event ID analysis",
    "Failed login investigation",
    "Threat hunting",
    "Incident response",
    "Detection engineering",
    "Malware analysis",
    "YARA/Sigma",
    "Git/GitHub workflow",
    "Evidence handling",
    "Privacy review",
    "Python automation",
    "AI-assisted workflow design",
    "SOC operations",
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
SECRET_EXTENSIONS = {".pem", ".p12", ".pfx", ".key", ".keystore", ".sqlite", ".sqlite3", ".db"}
SECRET_NAME_PATTERNS = (
    re.compile(r"(^|[._-])\.?env($|[._-])", re.IGNORECASE),
    re.compile(r"(secret|credential|token|apikey|api_key|access_key)", re.IGNORECASE),
    re.compile(r"(password|passwd|pwd|cookie)", re.IGNORECASE),
    re.compile(r"(^|[._-])id_rsa($|[._-])", re.IGNORECASE),
    re.compile(r"(^|[._-])private[_-]?key($|[._-])", re.IGNORECASE),
)
TEXT_EXTENSIONS = {".md", ".txt", ".json", ".csv", ".yml", ".yaml", ".toml", ".py", ".ps1", ".cmd", ".bat"}
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
REPORT_NAMES = {
    "project-closeout-report.md",
    "github-readiness-report.md",
    "recruiter-portfolio.md",
    "portfolio-index.md",
    "orchestration-report.md",
}
PROJECT_MARKERS = {
    "README.md",
    "readme.md",
    "docs",
    "evidence",
    "queries",
    "src",
    "tests",
    "project-closeout-report.md",
    "github-readiness-report.md",
}
LOCAL_ONLY_NAMES = {"outputs", "output", "agent-output", "linkedin-drafts", "drafts", "reports"}
TODO_RE = re.compile(r"\b(TODO|TBD|FIXME|placeholder|coming soon|insert screenshot|add screenshot)\b", re.IGNORECASE)

SKILL_RULES: dict[str, tuple[str, ...]] = {
    "SIEM": ("siem", "security information and event management", "wazuh", "splunk", "alert dashboard"),
    "Wazuh": ("wazuh",),
    "Windows Event Logs": ("windows event", "event viewer", "event log", "wineventlog"),
    "Event ID analysis": ("event id", "4624", "4625", "4740", "4688", "7045"),
    "Failed login investigation": ("failed login", "failed logon", "4625", "brute force", "login investigation"),
    "Threat hunting": ("threat hunt", "threat hunting", "hunt query", "hypothesis", "ioc"),
    "Incident response": ("incident response", "triage", "containment", "eradication", "recovery", "alert investigation"),
    "Detection engineering": ("detection engineering", "detection rule", "sigma", "yara", "rule logic", "alert rule"),
    "Malware analysis": ("malware analysis", "malware", "static analysis", "dynamic analysis", "sample analysis"),
    "YARA/Sigma": ("yara", "sigma"),
    "Git/GitHub workflow": ("github", "git status", "readiness", "commit", "pull request", "gitignore"),
    "Evidence handling": ("evidence", "screenshot", "screenshots-public", "artifact", "proof"),
    "Privacy review": ("privacy review", "public-safe", "redact", "pii", "local-only"),
    "Python automation": ("python", ".py", "automation", "validator", "orchestrator", "cli"),
    "AI-assisted workflow design": ("ai-assisted", "agent", "orchestrator", "codex", "workflow design"),
    "SOC operations": ("soc", "alert", "queue", "escalation", "runbook", "triage"),
}


@dataclass
class ProjectSignal:
    name: str
    path: str
    score: int
    evidence_score: int
    recruiter_score: int
    skill_hits: dict[str, int] = field(default_factory=dict)
    has_readme: bool = False
    has_docs: bool = False
    has_queries: bool = False
    has_evidence: bool = False
    has_public_screenshots: bool = False
    has_closeout: bool = False
    has_github_readiness: bool = False
    has_tests: bool = False
    unfinished_reasons: list[str] = field(default_factory=list)
    cleanup_reasons: list[str] = field(default_factory=list)
    recruiter_reasons: list[str] = field(default_factory=list)


@dataclass
class CareerReport:
    repo_path: str
    reviewed_at: str
    readiness_level: str
    readiness_score: int
    summary: str
    skill_map: dict[str, dict]
    proven_skills: list[str]
    weak_missing_skills: list[str]
    strongest_projects: list[ProjectSignal]
    unfinished_projects: list[ProjectSignal]
    cleanup_projects: list[ProjectSignal]
    recruiter_friendly_projects: list[ProjectSignal]
    suggested_next_labs: list[str]
    suggested_github_pin_order: list[str]
    recruiter_talking_points: list[str]
    resume_bullet_themes: list[str]
    linkedin_themes: list[str]
    risk_areas: list[str]
    missing_portfolio_areas: list[str]
    source_files_reviewed: list[str]
    secret_like_paths_skipped: list[str]
    warnings: list[str] = field(default_factory=list)


def is_secret_like(path: Path) -> bool:
    name = path.name
    if path.suffix.lower() in SECRET_EXTENSIONS:
        return True
    return any(pattern.search(name) for pattern in SECRET_NAME_PATTERNS)


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def safe_walk(root: Path, max_depth: int = 6) -> Iterable[tuple[Path, list[str], list[str]]]:
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
        yield current_path, dirs, files


def read_text_if_safe(path: Path, max_chars: int = 20000) -> str:
    if is_secret_like(path):
        return ""
    if path.suffix.lower() not in TEXT_EXTENSIONS:
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


def find_readme(path: Path) -> Path | None:
    for name in ("README.md", "readme.md", "Readme.md"):
        candidate = path / name
        if candidate.is_file() and not is_secret_like(candidate):
            return candidate
    return None


def is_project_candidate(path: Path, repo_root: Path) -> bool:
    if path == repo_root:
        return False
    names = child_names(path)
    marker_count = len(PROJECT_MARKERS.intersection(names))
    if marker_count >= 2:
        return True
    if find_readme(path) and path.parent == repo_root:
        return True
    if path.parent.name in {"blue-team-labs", "labs", "security-plus-projects", "tools"} and marker_count >= 1:
        return True
    return False


def discover_project_dirs(repo_root: Path) -> list[Path]:
    candidates: set[Path] = set()
    for current, dirs, _ in safe_walk(repo_root, max_depth=4):
        if is_project_candidate(current, repo_root):
            candidates.add(current)
            dirs[:] = []
    return sorted(candidates)


def collect_source_text(project_path: Path, repo_root: Path, reviewed: set[str], skipped: set[str]) -> str:
    text_parts = [project_path.name, rel(project_path, repo_root)]
    preferred_names = {"README.md", "readme.md", *REPORT_NAMES}
    preferred_dirs = {"docs", "queries"}
    for current, dirs, files in safe_walk(project_path, max_depth=3):
        local_parts = set(Path(rel(current, project_path)).parts)
        for filename in files:
            path = current / filename
            if is_secret_like(path):
                skipped.add(rel(path, repo_root))
                continue
            if filename in preferred_names or current.name in preferred_dirs:
                text = read_text_if_safe(path)
                if text:
                    reviewed.add(rel(path, repo_root))
                    text_parts.append(text)
        dirs[:] = [name for name in dirs if name in preferred_dirs or current == project_path]
    return "\n".join(text_parts)


def count_public_screenshots(project_path: Path) -> int:
    screenshot_dir = project_path / "evidence" / "screenshots-public"
    if not screenshot_dir.is_dir():
        return 0
    count = 0
    for path in screenshot_dir.rglob("*"):
        if path.is_file() and not is_secret_like(path) and path.suffix.lower() in IMAGE_EXTENSIONS:
            count += 1
    return count


def infer_skill_hits(text: str) -> dict[str, int]:
    lowered = text.lower()
    hits: dict[str, int] = {}
    for skill, needles in SKILL_RULES.items():
        count = sum(lowered.count(needle.lower()) for needle in needles)
        if count:
            hits[skill] = count
    return hits


def inspect_project(project_path: Path, repo_root: Path, reviewed: set[str], skipped: set[str]) -> ProjectSignal:
    names = child_names(project_path)
    readme = find_readme(project_path)
    has_docs = (project_path / "docs").is_dir()
    has_queries = (project_path / "queries").is_dir()
    has_evidence = (project_path / "evidence").is_dir()
    public_screenshots = count_public_screenshots(project_path)
    has_public_screenshots = public_screenshots > 0
    has_closeout = (project_path / "docs" / "project-closeout-report.md").is_file()
    has_github_readiness = (project_path / "docs" / "github-readiness-report.md").is_file()
    has_tests = (project_path / "tests").is_dir() or any(name.startswith("test_") for name in names)
    text = collect_source_text(project_path, repo_root, reviewed, skipped)
    skill_hits = infer_skill_hits(text)

    evidence_score = 0
    evidence_score += 2 if readme else 0
    evidence_score += 2 if has_docs else 0
    evidence_score += 2 if has_evidence else 0
    evidence_score += 3 if has_public_screenshots else 0
    evidence_score += 2 if has_closeout else 0
    evidence_score += 2 if has_github_readiness else 0
    evidence_score += min(3, public_screenshots)

    skill_score = min(10, len(skill_hits) * 2)
    recruiter_score = evidence_score + skill_score
    if "SOC operations" in skill_hits:
        recruiter_score += 2
    if "Wazuh" in skill_hits or "SIEM" in skill_hits:
        recruiter_score += 2
    if has_tests:
        recruiter_score += 1

    unfinished: list[str] = []
    if not readme:
        unfinished.append("missing README")
    if has_evidence and not has_public_screenshots:
        unfinished.append("evidence exists without evidence/screenshots-public")
    if TODO_RE.search(text):
        unfinished.append("placeholder or TODO language detected")
    if not has_docs and not has_queries and not has_evidence:
        unfinished.append("limited lab/project support folders")

    cleanup: list[str] = []
    if any(name in LOCAL_ONLY_NAMES for name in names):
        cleanup.append("local/generated output folder present")
    if has_public_screenshots and not has_github_readiness:
        cleanup.append("public screenshots exist but GitHub readiness report was not found")
    if has_github_readiness and not has_closeout:
        cleanup.append("GitHub readiness exists but closeout report was not found")

    recruiter_reasons: list[str] = []
    if has_public_screenshots:
        recruiter_reasons.append("public screenshots available")
    if has_closeout:
        recruiter_reasons.append("closeout report available")
    if has_github_readiness:
        recruiter_reasons.append("GitHub readiness report available")
    if skill_hits:
        recruiter_reasons.append("clear SOC/blue-team skill tags")

    return ProjectSignal(
        name=project_path.name,
        path=rel(project_path, repo_root),
        score=evidence_score + skill_score,
        evidence_score=evidence_score,
        recruiter_score=recruiter_score,
        skill_hits=skill_hits,
        has_readme=bool(readme),
        has_docs=has_docs,
        has_queries=has_queries,
        has_evidence=has_evidence,
        has_public_screenshots=has_public_screenshots,
        has_closeout=has_closeout,
        has_github_readiness=has_github_readiness,
        has_tests=has_tests,
        unfinished_reasons=unfinished,
        cleanup_reasons=cleanup,
        recruiter_reasons=recruiter_reasons,
    )


def collect_repo_sources(repo_root: Path, reviewed: set[str], skipped: set[str]) -> str:
    text_parts: list[str] = []
    source_roots = [repo_root / "docs", repo_root / "queries", repo_root / "tools" / "recruiter-portfolio" / "reports", repo_root / "tools" / "portfolio-index" / "reports"]
    for source_root in source_roots:
        if not source_root.exists():
            continue
        for current, _, files in safe_walk(source_root, max_depth=4):
            for filename in files:
                path = current / filename
                if is_secret_like(path):
                    skipped.add(rel(path, repo_root))
                    continue
                if filename in REPORT_NAMES or path.suffix.lower() in {".md", ".json", ".txt"}:
                    text = read_text_if_safe(path)
                    if text:
                        reviewed.add(rel(path, repo_root))
                        text_parts.append(text)
    return "\n".join(text_parts)


def readiness_from_score(score: int, skill_map: dict[str, dict], strongest: list[ProjectSignal], risk_count: int) -> str:
    proven = [skill for skill, data in skill_map.items() if data["status"] == "PROVEN"]
    weak = [skill for skill, data in skill_map.items() if data["status"] == "MISSING"]
    evidence_backed = [p for p in strongest if p.has_public_screenshots or p.has_closeout or p.has_github_readiness]
    if len(evidence_backed) < 2 or len(proven) < 4:
        return "NEEDS MORE EVIDENCE" if score >= 35 else "EARLY STAGE"
    if score >= 82 and len(proven) >= 10 and len(evidence_backed) >= 5 and risk_count <= 3:
        return "STRONG JUNIOR CANDIDATE"
    if score >= 58 and len(proven) >= 7:
        return "SOC READY"
    if score >= 32:
        return "DEVELOPING"
    if len(weak) >= 10:
        return "NEEDS MORE EVIDENCE"
    return "EARLY STAGE"


def build_skill_map(projects: list[ProjectSignal]) -> dict[str, dict]:
    by_skill: dict[str, list[ProjectSignal]] = defaultdict(list)
    hit_counts: Counter[str] = Counter()
    for project in projects:
        for skill, count in project.skill_hits.items():
            by_skill[skill].append(project)
            hit_counts[skill] += count

    skill_map: dict[str, dict] = {}
    for skill in SKILL_CATEGORIES:
        evidence_projects = sorted(by_skill.get(skill, []), key=lambda p: (-p.recruiter_score, p.path))[:5]
        project_count = len(by_skill.get(skill, []))
        if project_count >= 2 and any(p.has_public_screenshots or p.has_closeout for p in evidence_projects):
            status = "PROVEN"
        elif project_count >= 1:
            status = "PARTIAL"
        else:
            status = "MISSING"
        skill_map[skill] = {
            "status": status,
            "hit_count": hit_counts.get(skill, 0),
            "project_count": project_count,
            "evidence_projects": [p.path for p in evidence_projects],
        }
    return skill_map


def suggested_next_labs(skill_map: dict[str, dict]) -> list[str]:
    suggestions = []
    if skill_map["Threat hunting"]["status"] != "PROVEN":
        suggestions.append("Threat hunting mini-lab with a hypothesis, query notes, findings, and public-safe screenshots.")
    if skill_map["Detection engineering"]["status"] != "PROVEN":
        suggestions.append("Detection engineering lab that turns one observed behavior into a Sigma-style rule and test notes.")
    if skill_map["YARA/Sigma"]["status"] == "MISSING":
        suggestions.append("YARA or Sigma starter project with one simple rule, test sample notes, and false-positive discussion.")
    if skill_map["Malware analysis"]["status"] == "MISSING":
        suggestions.append("Safe malware-analysis writeup using benign/static examples, hashes, strings, and containment notes.")
    if skill_map["Incident response"]["status"] != "PROVEN":
        suggestions.append("Incident response timeline lab with alert, scope, containment decision, and lessons learned.")
    if not suggestions:
        suggestions.append("Polish the strongest SOC lab into a full recruiter case study with screenshots, README, closeout, and GitHub readiness.")
    return suggestions[:6]


def build_report(repo_path: Path) -> CareerReport:
    repo_root = repo_path.resolve()
    reviewed: set[str] = set()
    skipped: set[str] = set()
    projects = [inspect_project(path, repo_root, reviewed, skipped) for path in discover_project_dirs(repo_root)]
    repo_text = collect_repo_sources(repo_root, reviewed, skipped)
    if repo_text:
        repo_project = ProjectSignal(
            name="repo-level-summaries",
            path=".",
            score=0,
            evidence_score=0,
            recruiter_score=0,
            skill_hits=infer_skill_hits(repo_text),
        )
        projects_for_skills = projects + [repo_project]
    else:
        projects_for_skills = projects

    skill_map = build_skill_map(projects_for_skills)
    evidence_backed_projects = [
        p for p in projects if p.has_public_screenshots or p.has_closeout or p.has_github_readiness
    ]
    strongest_pool = evidence_backed_projects or projects
    strongest = sorted(strongest_pool, key=lambda p: (-p.recruiter_score, -p.evidence_score, p.path))[:8]
    unfinished = sorted([p for p in projects if p.unfinished_reasons], key=lambda p: (-len(p.unfinished_reasons), p.path))[:12]
    cleanup = sorted([p for p in projects if p.cleanup_reasons], key=lambda p: (-len(p.cleanup_reasons), p.path))[:12]
    recruiter = sorted([p for p in projects if p.recruiter_reasons and p.skill_hits], key=lambda p: (-p.recruiter_score, p.path))[:8]

    proven = [skill for skill, data in skill_map.items() if data["status"] == "PROVEN"]
    weak_missing = [skill for skill, data in skill_map.items() if data["status"] in {"MISSING", "PARTIAL"}]
    evidence_projects = evidence_backed_projects
    readiness_score = min(
        100,
        len(proven) * 4
        + len([s for s, data in skill_map.items() if data["status"] == "PARTIAL"]) * 2
        + min(30, len(evidence_projects) * 10)
        + min(10, len(recruiter) * 2),
    )
    if len(evidence_projects) < 3:
        readiness_score = min(readiness_score, 72)

    risk_areas: list[str] = []
    if len(evidence_projects) < 3:
        risk_areas.append("Few projects have closeout, GitHub readiness, or public screenshot evidence.")
    if weak_missing:
        risk_areas.append("Several SOC/blue-team skill areas are partial or missing.")
    if unfinished:
        risk_areas.append("Some projects look unfinished or thinly documented.")
    if cleanup:
        risk_areas.append("Some projects need cleanup before being treated as recruiter-facing.")
    if skipped:
        risk_areas.append("Secret-like paths were detected and skipped by path only.")

    readiness_level = readiness_from_score(readiness_score, skill_map, strongest, len(risk_areas))
    pin_order = [p.path for p in recruiter[:6]]

    talking_points = [
        "Built a local, evidence-first blue-team portfolio with README, docs, queries, screenshots, and closeout artifacts.",
        "Used SOC-style triage framing to document alert context, investigation steps, evidence, and readiness gaps.",
        "Applied GitHub/public-readiness checks before treating portfolio work as publishable.",
    ]
    if skill_map["Wazuh"]["status"] != "MISSING":
        talking_points.append("Hands-on Wazuh/SIEM documentation appears in the portfolio and can anchor SOC conversations.")
    if skill_map["Python automation"]["status"] != "MISSING":
        talking_points.append("Python automation is used to support repeatable portfolio review and reporting workflows.")

    resume_themes = [
        "SOC alert triage and failed-login investigation using documented evidence and event context.",
        "Blue-team documentation workflow covering README quality, evidence handling, and GitHub readiness.",
        "Python automation for local report generation, validation, and portfolio quality checks.",
    ]
    linkedin_themes = [
        "Evidence-backed SOC lab writeups and what each investigation proved.",
        "Lessons learned from turning lab work into recruiter-readable GitHub projects.",
        "Blue-team workflow improvements: screenshots, privacy review, closeout, and readiness gates.",
    ]

    missing_areas = [
        skill
        for skill in ("Threat hunting", "Detection engineering", "Malware analysis", "YARA/Sigma", "Incident response")
        if skill_map[skill]["status"] != "PROVEN"
    ]

    summary = (
        f"Estimated readiness is {readiness_level}. The portfolio shows {len(proven)} proven skill areas "
        f"and {len(evidence_projects)} projects with stronger evidence signals. Treat this as a local "
        "career-readiness estimate, not a hiring guarantee."
    )

    return CareerReport(
        repo_path=str(repo_root),
        reviewed_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        readiness_level=readiness_level,
        readiness_score=readiness_score,
        summary=summary,
        skill_map=skill_map,
        proven_skills=proven,
        weak_missing_skills=weak_missing,
        strongest_projects=strongest,
        unfinished_projects=unfinished,
        cleanup_projects=cleanup,
        recruiter_friendly_projects=recruiter,
        suggested_next_labs=suggested_next_labs(skill_map),
        suggested_github_pin_order=pin_order,
        recruiter_talking_points=talking_points,
        resume_bullet_themes=resume_themes,
        linkedin_themes=linkedin_themes,
        risk_areas=risk_areas,
        missing_portfolio_areas=missing_areas,
        source_files_reviewed=sorted(reviewed),
        secret_like_paths_skipped=sorted(skipped),
        warnings=[],
    )


def project_to_dict(project: ProjectSignal) -> dict:
    return {
        "name": project.name,
        "path": project.path,
        "score": project.score,
        "evidence_score": project.evidence_score,
        "recruiter_score": project.recruiter_score,
        "skill_hits": project.skill_hits,
        "has_readme": project.has_readme,
        "has_docs": project.has_docs,
        "has_queries": project.has_queries,
        "has_evidence": project.has_evidence,
        "has_public_screenshots": project.has_public_screenshots,
        "has_closeout": project.has_closeout,
        "has_github_readiness": project.has_github_readiness,
        "has_tests": project.has_tests,
        "unfinished_reasons": project.unfinished_reasons,
        "cleanup_reasons": project.cleanup_reasons,
        "recruiter_reasons": project.recruiter_reasons,
    }


def as_dict(report: CareerReport) -> dict:
    return {
        "repo_path": report.repo_path,
        "reviewed_at": report.reviewed_at,
        "readiness_level": report.readiness_level,
        "readiness_score": report.readiness_score,
        "summary": report.summary,
        "skill_map": report.skill_map,
        "proven_skills": report.proven_skills,
        "weak_missing_skills": report.weak_missing_skills,
        "strongest_evidence_backed_projects": [project_to_dict(p) for p in report.strongest_projects],
        "unfinished_projects": [project_to_dict(p) for p in report.unfinished_projects],
        "projects_needing_cleanup": [project_to_dict(p) for p in report.cleanup_projects],
        "recruiter_friendly_projects": [project_to_dict(p) for p in report.recruiter_friendly_projects],
        "suggested_next_labs": report.suggested_next_labs,
        "suggested_github_pin_order": report.suggested_github_pin_order,
        "suggested_recruiter_talking_points": report.recruiter_talking_points,
        "suggested_resume_bullet_themes": report.resume_bullet_themes,
        "suggested_linkedin_themes": report.linkedin_themes,
        "risk_areas": report.risk_areas,
        "missing_portfolio_areas": report.missing_portfolio_areas,
        "source_files_reviewed": report.source_files_reviewed,
        "secret_like_paths_skipped": report.secret_like_paths_skipped,
        "warnings": report.warnings,
        "safety": {
            "report_only": True,
            "external_apis": False,
            "live_scans": False,
            "git_actions": False,
            "secret_contents_read": False,
        },
    }


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def project_list(projects: list[ProjectSignal], reason_attr: str | None = None) -> str:
    if not projects:
        return "- None found"
    rows: list[str] = []
    for project in projects:
        extra = ""
        if reason_attr:
            reasons = getattr(project, reason_attr)
            if reasons:
                extra = f" - {', '.join(reasons)}"
        rows.append(f"- `{project.path}` - score {project.recruiter_score}; {', '.join(project.skill_hits) or 'no SOC skill tags'}{extra}")
    return "\n".join(rows)


def render_skill_map(skill_map: dict[str, dict]) -> str:
    rows = ["| Skill | Status | Projects | Evidence |", "|---|---|---:|---|"]
    for skill in SKILL_CATEGORIES:
        data = skill_map[skill]
        evidence = ", ".join(data["evidence_projects"][:3])
        rows.append(f"| {skill} | {data['status']} | {data['project_count']} | {evidence} |")
    return "\n".join(rows)


def render_markdown(report: CareerReport) -> str:
    return f"""# Career Alignment Report

## Career Readiness Summary

- Repo path: `{report.repo_path}`
- Reviewed at: `{report.reviewed_at}`
- Estimated readiness level: {report.readiness_level}
- Readiness score: {report.readiness_score}/100
- Summary: {report.summary}

## SOC / Blue-Team Skill Map

{render_skill_map(report.skill_map)}

## Proven Skills

{list_or_none(report.proven_skills)}

## Weak / Missing Skills

{list_or_none(report.weak_missing_skills)}

## Strongest Evidence-Backed Projects

{project_list(report.strongest_projects)}

## Projects That Look Unfinished

{project_list(report.unfinished_projects, "unfinished_reasons")}

## Projects Needing Cleanup

{project_list(report.cleanup_projects, "cleanup_reasons")}

## Recruiter-Friendly Projects

{project_list(report.recruiter_friendly_projects, "recruiter_reasons")}

## Suggested Next Labs / Projects

{list_or_none(report.suggested_next_labs)}

## Suggested GitHub Pin Order

{list_or_none(report.suggested_github_pin_order)}

## Suggested Recruiter Talking Points

{list_or_none(report.recruiter_talking_points)}

## Suggested Resume Bullet Themes

{list_or_none(report.resume_bullet_themes)}

## Suggested LinkedIn Themes

{list_or_none(report.linkedin_themes)}

## Risk Areas / Weak Evidence Areas

{list_or_none(report.risk_areas)}

## Missing Portfolio Areas

{list_or_none(report.missing_portfolio_areas)}

## Source Files Reviewed

{list_or_none(report.source_files_reviewed)}

## Secret-Like Paths Skipped

{list_or_none(report.secret_like_paths_skipped)}

## Safety Boundary

- Report-only: yes
- External APIs used: no
- Live scans run: no
- Git actions run: no
- Secret contents read: no
"""


def write_outputs(report: CareerReport, output: Path) -> list[str]:
    if output.suffix.lower() in {".md", ".json"}:
        output.parent.mkdir(parents=True, exist_ok=True)
        markdown_path = output if output.suffix.lower() == ".md" else output.with_suffix(".md")
        json_path = output if output.suffix.lower() == ".json" else output.with_suffix(".json")
    else:
        output.mkdir(parents=True, exist_ok=True)
        markdown_path = output / "career-alignment.md"
        json_path = output / "career-alignment.json"
    markdown_path.write_text(render_markdown(report), encoding="utf-8")
    json_path.write_text(json.dumps(as_dict(report), indent=2), encoding="utf-8")
    return [str(markdown_path), str(json_path)]


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only SOC/blue-team Career Alignment Engine.")
    parser.add_argument("--repo-path", required=True, help="Repository path to inspect.")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of markdown.")
    parser.add_argument("--output", help="Optional output file or directory for markdown and JSON reports.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_path = Path(args.repo_path)
    if not repo_path.exists() or not repo_path.is_dir():
        print(f"ERROR: repo path does not exist or is not a directory: {repo_path}", file=sys.stderr)
        return 2
    report = build_report(repo_path)
    generated_paths: list[str] = []
    if args.output:
        generated_paths = write_outputs(report, Path(args.output))
    if args.json:
        payload = as_dict(report)
        payload["generated_report_paths"] = generated_paths
        print(json.dumps(payload, indent=2))
    else:
        text = render_markdown(report)
        if generated_paths:
            text += "\n## Generated Report Paths\n\n" + list_or_none(generated_paths) + "\n"
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
