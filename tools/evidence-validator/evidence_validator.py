#!/usr/bin/env python3
"""Report-only evidence and screenshot validator.

This script inspects local project structure and README references without
modifying files or reading secret-like files.
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
from urllib.parse import unquote, urlparse


STATUSES = (
    "EVIDENCE READY",
    "NEEDS ORGANIZATION",
    "NEEDS MORE EVIDENCE",
    "PRIVACY REVIEW NEEDED",
    "BLOCKED",
)

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp"}
EVIDENCE_DIR_NAMES = {"evidence", "docs", "findings", "reports"}
SCREENSHOT_DIR_NAMES = {"screenshots", "images", "imgs"}
GENERATED_DIR_NAMES = {
    "outputs",
    "output",
    "agent-output",
    "agent_outputs",
    "generated",
    "dist",
    "build",
}
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
SECRET_NAME_PATTERNS = (
    re.compile(r"(^|[._-])\.?env($|[._-])", re.IGNORECASE),
    re.compile(r"(secret|credential|apikey|api_key|access_key)", re.IGNORECASE),
    re.compile(r"(password|passwd|pwd|cookie)", re.IGNORECASE),
    re.compile(r"(^|[._-])id_rsa($|[._-])", re.IGNORECASE),
    re.compile(r"(^|[._-])private[_-]?key($|[._-])", re.IGNORECASE),
)
TOKEN_NAME_RE = re.compile(r"token", re.IGNORECASE)
TOKEN_EVENT_SCREENSHOT_RE = re.compile(r"(^|[._-])token[._-]event($|[._-])", re.IGNORECASE)
SECRET_EXTENSIONS = {".pem", ".p12", ".pfx", ".key", ".keystore", ".sqlite", ".sqlite3", ".db"}
HANDOFF_NAME_RE = re.compile(r"(^handoff$|handoff)", re.IGNORECASE)
README_IMAGE_RE = re.compile(r"!\[[^\]]*]\(([^)]+)\)")
HTML_IMAGE_RE = re.compile(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", re.IGNORECASE)
TODO_RE = re.compile(
    r"\b(TODO|TBD|FIXME|placeholder|coming soon|insert screenshot|add screenshot|lorem ipsum)\b",
    re.IGNORECASE,
)
UNCLEAN_BASENAME_RE = re.compile(r"(^image\d*$|^screenshot\d*$|^untitled\d*$|^\d{8,}$)", re.IGNORECASE)
PRIVACY_HINT_RE = re.compile(r"(private|pii|sensitive|account|email|personal|grade|coursework)", re.IGNORECASE)


@dataclass
class ImageFinding:
    path: str
    exists: bool
    real_image: bool
    non_empty: bool
    clean_name: bool
    placeholder_name: bool
    referenced_by_readme: bool
    privacy_review: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class ValidationResult:
    project_name: str
    project_path: str
    reviewed_at: str
    readme_path: str | None
    status: str
    evidence_dirs: list[str]
    screenshot_dirs: list[str]
    images: list[ImageFinding]
    readme_exists: bool
    readme_image_refs: list[str]
    valid_readme_refs: list[str]
    missing_readme_refs: list[str]
    todo_lines: list[str]
    linkedin_drafts: list[str]
    generated_outputs: list[str]
    handoff_files: list[str]
    secret_like_files: list[str]
    warnings: list[str]
    blockers: list[str]


def is_secret_like(path: Path) -> bool:
    name = path.name
    lower = name.lower()
    if lower in {".env", ".env.local", ".env.production", ".env.development"}:
        return True
    if path.suffix.lower() in SECRET_EXTENSIONS:
        return True
    if any(pattern.search(name) for pattern in SECRET_NAME_PATTERNS):
        return True
    if TOKEN_NAME_RE.search(name):
        return not (
            path.suffix.lower() in IMAGE_EXTENSIONS
            and "evidence" in {part.lower() for part in path.parts}
            and "screenshots" in {part.lower() for part in path.parts}
            and TOKEN_EVENT_SCREENSHOT_RE.search(name)
        )
    return False


def is_handoff_file(path: Path) -> bool:
    return path.suffix.lower() == ".md" and bool(HANDOFF_NAME_RE.search(path.stem))


def is_linkedin_draft(path: Path) -> bool:
    normalized = "/".join(part.lower() for part in path.parts)
    name = path.name.lower()
    return (
        "linkedin" in normalized
        or "social-post" in name
        or "social_post" in name
        or "post-draft" in name
    )


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def safe_walk(root: Path) -> Iterable[tuple[Path, list[str], list[str]]]:
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        dirs[:] = [d for d in dirs if d not in SKIP_DIR_NAMES and not is_secret_like(current_path / d)]
        yield current_path, dirs, files


def read_text_if_safe(path: Path) -> str:
    if is_secret_like(path):
        return ""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def resolve_readme(project_path: Path, readme_arg: str | None) -> Path:
    if readme_arg:
        candidate = Path(readme_arg)
        if not candidate.is_absolute():
            candidate = project_path / candidate
        return candidate.resolve()
    return (project_path / "README.md").resolve()


def parse_readme_image_refs(readme_text: str) -> list[str]:
    refs = []
    refs.extend(README_IMAGE_RE.findall(readme_text))
    refs.extend(HTML_IMAGE_RE.findall(readme_text))
    cleaned = []
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


def has_image_signature(path: Path) -> bool:
    if path.suffix.lower() not in IMAGE_EXTENSIONS:
        return False
    try:
        header = path.read_bytes()[:16]
    except OSError:
        return False
    signatures = (
        b"\x89PNG\r\n\x1a\n",
        b"\xff\xd8\xff",
        b"GIF87a",
        b"GIF89a",
        b"RIFF",
        b"BM",
    )
    return any(header.startswith(sig) for sig in signatures)


def clean_base_name(path: Path) -> bool:
    stem = path.stem
    if not stem:
        return False
    if UNCLEAN_BASENAME_RE.search(stem):
        return False
    if re.search(r"\s", stem):
        return False
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", stem):
        return False
    return len(stem) >= 5


def collect_project(project_path: Path, readme_path: Path) -> ValidationResult:
    evidence_dirs: list[str] = []
    screenshot_dirs: list[str] = []
    image_paths: list[Path] = []
    linkedin_drafts: list[str] = []
    generated_outputs: list[str] = []
    handoff_files: list[str] = []
    secret_like_files: list[str] = []

    for current, dirs, files in safe_walk(project_path):
        for dirname in dirs:
            directory = current / dirname
            lower = dirname.lower()
            if lower in EVIDENCE_DIR_NAMES:
                evidence_dirs.append(rel(directory, project_path))
            if lower in SCREENSHOT_DIR_NAMES:
                screenshot_dirs.append(rel(directory, project_path))
            if lower in GENERATED_DIR_NAMES:
                generated_outputs.append(rel(directory, project_path))
            if "linkedin" in lower:
                linkedin_drafts.append(rel(directory, project_path))

        for filename in files:
            path = current / filename
            relative = rel(path, project_path)
            if is_secret_like(path):
                secret_like_files.append(relative)
                continue
            lower_name = filename.lower()
            if is_handoff_file(path):
                handoff_files.append(relative)
            if is_linkedin_draft(path):
                linkedin_drafts.append(relative)
            if path.suffix.lower() in IMAGE_EXTENSIONS:
                image_paths.append(path)

    readme_exists = readme_path.exists() and readme_path.is_file() and not is_secret_like(readme_path)
    readme_text = read_text_if_safe(readme_path) if readme_exists else ""
    readme_refs = parse_readme_image_refs(readme_text)
    readme_dir = readme_path.parent
    valid_refs: list[str] = []
    missing_refs: list[str] = []
    referenced_paths: set[Path] = set()

    for ref in readme_refs:
        if not is_local_ref(ref):
            continue
        resolved = ref_to_path(ref, readme_dir)
        if resolved.exists() and resolved.is_file():
            valid_refs.append(ref)
            referenced_paths.add(resolved)
        else:
            missing_refs.append(ref)

    todo_lines: list[str] = []
    for line_number, line in enumerate(readme_text.splitlines(), start=1):
        if TODO_RE.search(line):
            todo_lines.append(f"line {line_number}: {line.strip()[:140]}")

    images: list[ImageFinding] = []
    for image_path in sorted(image_paths):
        try:
            size = image_path.stat().st_size
        except OSError:
            size = 0
        notes: list[str] = []
        real_image = has_image_signature(image_path)
        non_empty = size > 0
        clean_name = clean_base_name(image_path)
        placeholder_name = bool(re.search(r"(placeholder|sample|example|dummy)", image_path.name, re.IGNORECASE))
        privacy_review = bool(PRIVACY_HINT_RE.search(image_path.as_posix()))
        if not real_image:
            notes.append("image header was not recognized")
        if not clean_name:
            notes.append("filename should be more descriptive and base-name friendly")
        if placeholder_name:
            notes.append("placeholder-like filename")
        if privacy_review:
            notes.append("privacy-review filename/path hint")
        images.append(
            ImageFinding(
                path=rel(image_path, project_path),
                exists=True,
                real_image=real_image,
                non_empty=non_empty,
                clean_name=clean_name,
                placeholder_name=placeholder_name,
                referenced_by_readme=image_path.resolve() in referenced_paths,
                privacy_review=privacy_review,
                notes=notes,
            )
        )

    warnings: list[str] = []
    blockers: list[str] = []

    if secret_like_files:
        blockers.append("Secret-like filenames were found. Paths are listed only; contents were not read.")
    if not readme_exists:
        warnings.append("README was not found or could not be read safely.")
    if not evidence_dirs:
        warnings.append("No evidence folder was found.")
    if not screenshot_dirs:
        warnings.append("No screenshot/images folder was found.")
    if missing_refs:
        blockers.append("README image references do not match actual local files.")
    if not images:
        warnings.append("No local image files were found.")
    if any(not image.real_image or not image.non_empty for image in images):
        warnings.append("One or more image files are empty or not recognized as real images.")
    if any(not image.clean_name or image.placeholder_name for image in images):
        warnings.append("One or more screenshot filenames need organization.")
    if any(image.privacy_review for image in images):
        warnings.append("One or more screenshot paths suggest privacy review is needed.")
    if images and readme_exists and not valid_refs and not missing_refs:
        warnings.append("Image files exist, but README does not reference local screenshots.")
    if todo_lines:
        warnings.append("README contains obvious placeholder/TODO language.")
    if linkedin_drafts:
        warnings.append("LinkedIn draft files or folders are inside the project path; treat as local-only.")
    if generated_outputs:
        warnings.append("Generated output folders are inside the project path; treat as local-only unless approved.")
    if handoff_files:
        warnings.append("HANDOFF files are inside the project path; treat as local-only unless approved.")

    status = decide_status(
        secret_like_files=secret_like_files,
        missing_refs=missing_refs,
        images=images,
        readme_exists=readme_exists,
        evidence_dirs=evidence_dirs,
        screenshot_dirs=screenshot_dirs,
        todo_lines=todo_lines,
        linkedin_drafts=linkedin_drafts,
        generated_outputs=generated_outputs,
    )

    return ValidationResult(
        project_name=project_path.name,
        project_path=str(project_path),
        reviewed_at=datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        readme_path=str(readme_path) if readme_path else None,
        status=status,
        evidence_dirs=sorted(set(evidence_dirs)),
        screenshot_dirs=sorted(set(screenshot_dirs)),
        images=images,
        readme_exists=readme_exists,
        readme_image_refs=readme_refs,
        valid_readme_refs=valid_refs,
        missing_readme_refs=missing_refs,
        todo_lines=todo_lines,
        linkedin_drafts=sorted(set(linkedin_drafts)),
        generated_outputs=sorted(set(generated_outputs)),
        handoff_files=sorted(set(handoff_files)),
        secret_like_files=sorted(set(secret_like_files)),
        warnings=warnings,
        blockers=blockers,
    )


def decide_status(
    *,
    secret_like_files: list[str],
    missing_refs: list[str],
    images: list[ImageFinding],
    readme_exists: bool,
    evidence_dirs: list[str],
    screenshot_dirs: list[str],
    todo_lines: list[str],
    linkedin_drafts: list[str],
    generated_outputs: list[str],
) -> str:
    if secret_like_files:
        return "BLOCKED"
    if missing_refs:
        return "NEEDS MORE EVIDENCE"
    if any(image.privacy_review for image in images):
        return "PRIVACY REVIEW NEEDED"
    if not readme_exists or not evidence_dirs or not screenshot_dirs or not images:
        return "NEEDS MORE EVIDENCE"
    if any(not image.real_image or not image.non_empty for image in images):
        return "NEEDS MORE EVIDENCE"
    if any(not image.clean_name or image.placeholder_name for image in images):
        return "NEEDS ORGANIZATION"
    if images and not any(image.referenced_by_readme for image in images):
        return "NEEDS ORGANIZATION"
    if todo_lines or linkedin_drafts or generated_outputs:
        return "NEEDS ORGANIZATION"
    return "EVIDENCE READY"


def as_dict(result: ValidationResult) -> dict:
    return {
        "project_name": result.project_name,
        "project_path": result.project_path,
        "reviewed_at": result.reviewed_at,
        "readme_path": result.readme_path,
        "status": result.status,
        "evidence_dirs": result.evidence_dirs,
        "screenshot_dirs": result.screenshot_dirs,
        "images": [image.__dict__ for image in result.images],
        "readme_exists": result.readme_exists,
        "readme_image_refs": result.readme_image_refs,
        "valid_readme_refs": result.valid_readme_refs,
        "missing_readme_refs": result.missing_readme_refs,
        "todo_lines": result.todo_lines,
        "linkedin_drafts": result.linkedin_drafts,
        "generated_outputs": result.generated_outputs,
        "handoff_files": result.handoff_files,
        "secret_like_files": result.secret_like_files,
        "warnings": result.warnings,
        "blockers": result.blockers,
    }


def list_or_none(items: list[str]) -> str:
    if not items:
        return "- None found"
    return "\n".join(f"- {item}" for item in items)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def render_markdown(result: ValidationResult) -> str:
    image_rows = []
    for image in result.images:
        notes = "; ".join(image.notes) if image.notes else ""
        image_rows.append(
            "| {path} | {exists} | {real} | {clean} | {ref} | {privacy} | {notes} |".format(
                path=image.path,
                exists=yes_no(image.exists),
                real=yes_no(image.real_image and image.non_empty),
                clean=yes_no(image.clean_name and not image.placeholder_name),
                ref=yes_no(image.referenced_by_readme),
                privacy=yes_no(image.privacy_review),
                notes=notes,
            )
        )
    if not image_rows:
        image_rows.append("| None found | no | no | no | no | no | No local image files found |")

    return f"""# Evidence Validation Report

## Project

- Project name: {result.project_name}
- Project path: {result.project_path}
- Review date: {result.reviewed_at}
- README path: {result.readme_path}
- Final status: {result.status}

## Evidence Summary

- README exists: {yes_no(result.readme_exists)}
- Evidence folders found:
{list_or_none(result.evidence_dirs)}
- Screenshot folders found:
{list_or_none(result.screenshot_dirs)}
- HANDOFF files found:
{list_or_none(result.handoff_files)}
- Generated output folders:
{list_or_none(result.generated_outputs)}
- LinkedIn local-only candidates:
{list_or_none(result.linkedin_drafts)}
- Secret-like files found:
{list_or_none(result.secret_like_files)}

## Screenshot Inventory

| Screenshot | Exists | Real Image | Clean Name | Referenced By README | Privacy Review | Notes |
|---|---|---|---|---|---|---|
{chr(10).join(image_rows)}

## README Reference Check

- README image references:
{list_or_none(result.readme_image_refs)}
- Valid local references:
{list_or_none(result.valid_readme_refs)}
- Missing local references:
{list_or_none(result.missing_readme_refs)}

## Placeholder / TODO Check

{list_or_none(result.todo_lines)}

## Local-Only Warnings

{list_or_none(result.warnings)}

## Blockers

{list_or_none(result.blockers)}

## Final Status

- Evidence validation status: {result.status}
- Can README be polished: {yes_no(result.status not in {"BLOCKED"})}
- Can GitHub readiness continue: {yes_no(result.status in {"EVIDENCE READY", "NEEDS ORGANIZATION", "PRIVACY REVIEW NEEDED"})}
- Can supervisor-agent closeout continue: {yes_no(result.status in {"EVIDENCE READY", "NEEDS ORGANIZATION", "PRIVACY REVIEW NEEDED"})}
- Can LinkedIn draft be written: {yes_no(result.status == "EVIDENCE READY")}
- Human approval required before public use: yes
"""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report-only evidence and screenshot validator.")
    parser.add_argument("--project-path", required=True, help="Project folder to inspect.")
    parser.add_argument("--readme", help="README path, relative to project path or absolute. Defaults to README.md.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    project_path = Path(args.project_path).resolve()
    if not project_path.exists() or not project_path.is_dir():
        print(f"ERROR: project path does not exist or is not a directory: {project_path}", file=sys.stderr)
        return 2

    readme_path = resolve_readme(project_path, args.readme)
    result = collect_project(project_path, readme_path)

    if args.json:
        print(json.dumps(as_dict(result), indent=2))
    else:
        print(render_markdown(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
