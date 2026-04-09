from __future__ import annotations

from datetime import datetime, timedelta
from dataclasses import dataclass
from pathlib import Path

from .config import Settings
from .parsers import read_supported_file


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


def discover_projects(portfolio_root: Path, settings: Settings) -> list[ProjectDecision]:
    return discover_projects_with_filters(portfolio_root, settings, recent_days=0)


def discover_projects_with_filters(
    portfolio_root: Path,
    settings: Settings,
    recent_days: int = 0,
) -> list[ProjectDecision]:
    decisions: list[ProjectDecision] = []
    cutoff = None
    if recent_days > 0:
        cutoff = datetime.now() - timedelta(days=recent_days)
    for child in sorted(portfolio_root.iterdir(), key=lambda item: item.name.lower()):
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
        root_content_count = count_root_supported_files(child)
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

    for current_root, dirnames, filenames in project_path.walk(top_down=True):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skippable_dir_name(dirname, settings)
        ]
        for filename in filenames:
            path = current_root / filename
            if path.suffix.lower() in SUPPORTED_EXTENSIONS:
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
    for current_root, dirnames, filenames in project_path.walk(top_down=True):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skippable_dir_name(dirname, settings)
        ]
        for filename in filenames:
            if Path(filename).suffix.lower() in SUPPORTED_EXTENSIONS:
                count += 1
                if count >= 1:
                    return count
    return count


def count_root_supported_files(project_path: Path) -> int:
    count = 0
    for child in project_path.iterdir():
        if child.is_file() and child.suffix.lower() in SUPPORTED_EXTENSIONS:
            count += 1
    return count


def find_recent_supported_file(
    project_path: Path,
    settings: Settings,
    cutoff: datetime,
) -> Path | None:
    candidates: list[Path] = []
    for current_root, dirnames, filenames in project_path.walk(top_down=True):
        dirnames[:] = [
            dirname
            for dirname in dirnames
            if not _is_skippable_dir_name(dirname, settings)
        ]
        for filename in filenames:
            path = current_root / filename
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
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
    for child in project_path.iterdir():
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
    for child in project_path.iterdir():
        if child.is_file() and child.name.lower() in README_NAMES:
            return True
    return False
