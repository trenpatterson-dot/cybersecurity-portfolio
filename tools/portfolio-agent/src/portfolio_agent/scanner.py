from __future__ import annotations

import os
import stat
from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .parsers import is_binary_text_file, read_supported_file


BASE_SKIP_DIRS = {
    ".git",
    ".github",
    ".venv",
    ".tmp.driveupload",
    ".vscode",
    "__pycache__",
    "agent-output",
    "lab-doc-agent",
    "node_modules",
    "portfolio-agent",
    "screenshots",
    "venv",
}

SUPPORTED_EXTENSIONS = {".md", ".txt", ".docx", ".pdf"}
README_NAMES = {"readme", "readme.md", "readme.txt"}
SUPPORTING_DIR_NAMES = {"docs", "doc", "notes", "note", "assets", "images", "img", "screenshots"}
SECRET_FILE_NAMES = {"api.txt"}
SECRET_FILE_EXTENSIONS = {".env", ".key", ".pem", ".p12", ".pfx", ".kdbx"}
SECRET_NAME_TOKENS = {
    "secret",
    "token",
    "credential",
    "apikey",
    "api-key",
    "private-key",
    "private_key",
}


@dataclass
class SourceFile:
    path: Path
    relative_path: str
    source_type: str
    content: str


@dataclass
class ProjectScan:
    project_name: str
    project_path: Path
    sources: list[SourceFile]


@dataclass
class ProjectDecision:
    path: Path
    should_process: bool
    reason: str


def _is_hidden_dir(path: Path) -> bool:
    return any(part.startswith(".") for part in path.parts)


def _is_skippable_dir_name(name: str, settings: Settings) -> bool:
    lowered = name.lower()
    if lowered in BASE_SKIP_DIRS or lowered in settings.denylist:
        return True
    if lowered.startswith("."):
        return True
    if "screenshot" in lowered:
        return True
    return False


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _resolve_existing_path(path: Path) -> Path | None:
    try:
        return path.resolve(strict=True)
    except OSError:
        return None


def _safe_iterdir(path: Path) -> list[Path]:
    try:
        return list(path.iterdir())
    except OSError:
        return []


def _is_link_or_reparse_point(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        stat_result = os.lstat(path)
    except OSError:
        return True

    file_attributes = getattr(stat_result, "st_file_attributes", 0)
    file_attribute_reparse_point = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
    return bool(file_attributes & file_attribute_reparse_point)


def _is_safe_directory(path: Path, settings: Settings) -> bool:
    if _is_link_or_reparse_point(path):
        return False
    resolved_path = _resolve_existing_path(path)
    if resolved_path is None:
        return False
    return _is_relative_to(resolved_path, settings.portfolio_root)


def _is_secret_like_file(path: Path) -> bool:
    name = path.name.lower()
    stem = path.stem.lower()
    suffix = path.suffix.lower()

    if name == ".env" or name.startswith(".env."):
        return True
    if name in SECRET_FILE_NAMES:
        return True
    if suffix in SECRET_FILE_EXTENSIONS:
        return True
    if any(token in stem for token in SECRET_NAME_TOKENS):
        return True
    return False


def _is_supported_source_file(path: Path) -> bool:
    return path.suffix.lower() in SUPPORTED_EXTENSIONS and not _is_secret_like_file(path)


def _is_safe_source_path(path: Path, settings: Settings) -> bool:
    if not path.is_file():
        return False
    if not _is_supported_source_file(path):
        return False
    if _is_link_or_reparse_point(path):
        return False
    resolved_path = _resolve_existing_path(path)
    if resolved_path is None:
        return False
    if not _is_relative_to(resolved_path, settings.portfolio_root):
        return False
    try:
        if path.stat().st_size > settings.max_file_size_bytes:
            return False
    except OSError:
        return False
    if path.suffix.lower() in {".md", ".txt"} and is_binary_text_file(path):
        return False
    return True


def discover_projects(portfolio_root: Path, settings: Settings) -> list[ProjectDecision]:
    return discover_projects_with_filters(portfolio_root, settings, recent_days=0)


def discover_projects_with_filters(
    portfolio_root: Path,
    settings: Settings,
    recent_days: int = 0,
) -> list[ProjectDecision]:
    decisions: list[ProjectDecision] = []
    portfolio_root_resolved = _resolve_existing_path(portfolio_root)
    if portfolio_root_resolved is None:
        return decisions
    settings = Settings(
        portfolio_root=portfolio_root_resolved,
        output_dir=settings.output_dir,
        max_files_per_project=settings.max_files_per_project,
        max_chars_per_file=settings.max_chars_per_file,
        max_pdf_pages=settings.max_pdf_pages,
        max_file_size_bytes=settings.max_file_size_bytes,
        allowlist=settings.allowlist,
        denylist=settings.denylist,
    )
    cutoff = None
    if recent_days > 0:
        cutoff = datetime.now() - timedelta(days=recent_days)
    for child in sorted(_safe_iterdir(portfolio_root), key=lambda item: item.name.lower()):
        child_name = child.name.lower()
        if not child.is_dir():
            continue
        if _is_hidden_dir(child):
            decisions.append(ProjectDecision(path=child, should_process=False, reason="hidden folder"))
            continue
        if settings.allowlist and child_name not in settings.allowlist:
            decisions.append(ProjectDecision(path=child, should_process=False, reason="not in allowlist"))
            continue
        if _is_skippable_dir_name(child.name, settings):
            decisions.append(ProjectDecision(path=child, should_process=False, reason="denylisted or meta folder"))
            continue
        if not _is_safe_directory(child, settings):
            decisions.append(ProjectDecision(path=child, should_process=False, reason="linked or out-of-root folder"))
            continue
        root_content_count = count_root_supported_files(child, settings)
        if root_content_count == 0:
            decisions.append(ProjectDecision(path=child, should_process=False, reason="no supported project files in project root"))
            continue
        child_project_count = count_child_project_dirs(child)
        if child_project_count >= 2:
            decisions.append(ProjectDecision(path=child, should_process=False, reason="collection folder with multiple child projects"))
            continue
        content_count = count_supported_files(child, settings)
        if content_count == 0:
            decisions.append(ProjectDecision(path=child, should_process=False, reason="no supported project files found after folder filtering"))
            continue
        if cutoff is not None:
            recent_file = find_recent_supported_file(child, settings, cutoff)
            if recent_file is None:
                decisions.append(
                    ProjectDecision(
                        path=child,
                        should_process=False,
                        reason=f"no supported files modified in the last {recent_days} day(s)",
                    )
                )
                continue
            relative_recent = str(recent_file.relative_to(child)).replace("\\", "/")
            decisions.append(
                ProjectDecision(
                    path=child,
                    should_process=True,
                    reason=f"included by recent file: {relative_recent}",
                )
            )
            continue
        decisions.append(ProjectDecision(path=child, should_process=True, reason=f"{content_count} supported file(s) found"))
    return decisions


def _file_priority(path: Path) -> tuple[int, int, int, int, str]:
    name = path.name.lower()
    suffix = path.suffix.lower()

    readme_rank = 0 if name in README_NAMES else 1
    extension_rank = {
        ".md": 0,
        ".txt": 1,
        ".docx": 2,
        ".pdf": 3,
    }.get(suffix, 9)
    depth_rank = len(path.parts)
    length_rank = len(name)
    return (readme_rank, extension_rank, depth_rank, length_rank, name)


def collect_project_sources(project_path: Path, settings: Settings) -> ProjectScan:
    candidates: list[Path] = []

    for current_root, dirnames, filenames in os.walk(project_path, topdown=True, onerror=lambda _: None):
        current_root = Path(current_root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skippable_dir_name(dirname, settings) and _is_safe_directory(current_root / dirname, settings)
        ]
        for filename in filenames:
            path = current_root / filename
            if _is_safe_source_path(path, settings):
                candidates.append(path)

    candidates = sorted(candidates, key=_file_priority)
    selected = candidates[: settings.max_files_per_project]

    sources: list[SourceFile] = []
    for path in selected:
        content = read_supported_file(
            path=path,
            max_chars=settings.max_chars_per_file,
            max_pdf_pages=settings.max_pdf_pages,
        )
        if not content.strip():
            continue
        sources.append(
            SourceFile(
                path=path,
                relative_path=str(path.relative_to(project_path)).replace("\\", "/"),
                source_type=path.suffix.lower().lstrip("."),
                content=content.strip(),
            )
        )

    return ProjectScan(
        project_name=project_path.name,
        project_path=project_path,
        sources=sources,
    )


def count_supported_files(project_path: Path, settings: Settings) -> int:
    count = 0
    for current_root, dirnames, filenames in os.walk(project_path, topdown=True, onerror=lambda _: None):
        current_root = Path(current_root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skippable_dir_name(dirname, settings) and _is_safe_directory(current_root / dirname, settings)
        ]
        for filename in filenames:
            if _is_safe_source_path(current_root / filename, settings):
                count += 1
                if count >= 1:
                    return count
    return count


def count_root_supported_files(project_path: Path, settings: Settings) -> int:
    count = 0
    for child in _safe_iterdir(project_path):
        if child.is_file() and _is_safe_source_path(child, settings):
            count += 1
    return count


def find_recent_supported_file(
    project_path: Path,
    settings: Settings,
    cutoff: datetime,
) -> Path | None:
    candidates: list[Path] = []
    for current_root, dirnames, filenames in os.walk(project_path, topdown=True, onerror=lambda _: None):
        current_root = Path(current_root)
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skippable_dir_name(dirname, settings) and _is_safe_directory(current_root / dirname, settings)
        ]
        for filename in filenames:
            path = current_root / filename
            if not _is_safe_source_path(path, settings):
                continue
            modified_at = datetime.fromtimestamp(path.stat().st_mtime)
            if modified_at >= cutoff:
                candidates.append(path)

    if not candidates:
        return None
    candidates.sort(key=lambda item: item.stat().st_mtime, reverse=True)
    return candidates[0]


def count_child_project_dirs(project_path: Path) -> int:
    count = 0
    for child in _safe_iterdir(project_path):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name.lower() in SUPPORTING_DIR_NAMES:
            continue
        if has_root_readme(child):
            count += 1
    return count


def has_root_readme(project_path: Path) -> bool:
    for child in _safe_iterdir(project_path):
        if child.is_file() and child.name.lower() in README_NAMES:
            return True
    return False
