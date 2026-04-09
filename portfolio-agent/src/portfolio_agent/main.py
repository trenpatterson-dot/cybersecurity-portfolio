from __future__ import annotations

import argparse
from pathlib import Path

from .config import get_settings
from .scanner import ProjectDecision, collect_project_sources, discover_projects_with_filters
from .writer import write_project_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Local-first portfolio agent for cybersecurity project summaries."
    )
    parser.add_argument(
        "--project",
        help="Only process one top-level project folder by name.",
    )
    parser.add_argument(
        "--limit-projects",
        type=int,
        default=0,
        help="Only process the first N discovered projects.",
    )
    parser.add_argument(
        "--recent-days",
        type=int,
        default=0,
        help="Only process projects with supported source files modified in the last N days.",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Print quick-access paths for github-update.md, linkedin-post.md, and onenote-notes.md after the run.",
    )
    parser.add_argument(
        "--pick",
        action="store_true",
        help="Show a numbered list of eligible projects and let you choose one interactively.",
    )
    parser.add_argument(
        "--public",
        action="store_true",
        help="Write safer public-facing outputs with extra redaction and sanitized source listings.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be processed and which sources would be used without writing any files.",
    )
    return parser


def write_run_index(
    output_dir: Path,
    processable_projects: list[ProjectDecision],
    skipped_projects: list[ProjectDecision],
) -> Path:
    lines = [
        "# Portfolio Agent Index",
        "",
        "## Processed Projects",
    ]

    if processable_projects:
        for decision in processable_projects:
            project_output_dir = output_dir / _slugify(decision.path.name)
            lines.append(
                f"- `{decision.path.name}` | reason: {decision.reason} | output: `{project_output_dir}`"
            )
    else:
        lines.append("- None")

    lines.extend(["", "## Skipped Folders"])
    if skipped_projects:
        for decision in skipped_projects:
            lines.append(f"- `{decision.path.name}` | reason: {decision.reason}")
    else:
        lines.append("- None")

    index_path = output_dir / "index.md"
    index_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return index_path


def _slugify(name: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in name).strip("-").replace("--", "-")


def print_quick_access_paths(project_output_dirs: list[Path]) -> None:
    print("Quick-access files:")
    for output_dir in project_output_dirs:
        print(f"  - {output_dir.name}")
        print(f"    github-update.md : {output_dir / 'github-update.md'}")
        print(f"    linkedin-post.md : {output_dir / 'linkedin-post.md'}")
        print(f"    onenote-notes.md : {output_dir / 'onenote-notes.md'}")


def print_dry_run_preview(project_name: str, source_paths: list[str], output_dir: Path) -> None:
    print(f"[DRY-RUN] Would process {project_name}")
    print(f"    Output folder : {output_dir}")
    if source_paths:
        print("    Source files :")
        for source_path in source_paths:
            print(f"      - {source_path}")
    else:
        print("    Source files : none")


def pick_project(processable_projects: list[ProjectDecision]) -> ProjectDecision:
    print("Pick a project:")
    for index, decision in enumerate(processable_projects, start=1):
        print(f"  {index}. {decision.path.name} ({decision.reason})")

    while True:
        choice = input("Enter project number: ").strip()
        if not choice.isdigit():
            print("Invalid selection. Enter a number from the list.")
            continue
        selected_index = int(choice)
        if 1 <= selected_index <= len(processable_projects):
            return processable_projects[selected_index - 1]
        print("Invalid selection. Enter a number from the list.")


def main() -> int:
    base_dir = Path(__file__).resolve().parents[2]
    settings = get_settings(base_dir=base_dir)
    args = build_parser().parse_args()
    top_level_dirs = {
        child.name.lower(): child
        for child in settings.portfolio_root.iterdir()
        if child.is_dir()
    }

    print("=" * 72)
    print("Local Portfolio Agent")
    print("=" * 72)
    print(f"Portfolio root : {settings.portfolio_root}")
    print(f"Output folder  : {settings.output_dir}")
    print("Mode           : Manual run")
    print(f"Allowlist      : {', '.join(sorted(settings.allowlist)) if settings.allowlist else '(not set)'}")
    print(f"Denylist       : {', '.join(sorted(settings.denylist)) if settings.denylist else '(not set)'}")
    print(f"Recent filter  : last {args.recent_days} day(s)" if args.recent_days > 0 else "Recent filter  : (not set)")
    print(f"Public mode    : {'enabled' if args.public else 'disabled'}")
    print(f"Dry run        : {'enabled' if args.dry_run else 'disabled'}")
    print("-" * 72)

    if args.pick and args.project:
        print("ERROR: Use only one of --pick or --project.")
        return 1

    decisions = discover_projects_with_filters(
        settings.portfolio_root,
        settings,
        recent_days=args.recent_days,
    )
    if args.project:
        target_name = args.project.lower()
        if target_name not in top_level_dirs:
            print(f"ERROR: Project folder '{args.project}' does not exist in {settings.portfolio_root}")
            return 1
        decisions = [decision for decision in decisions if decision.path.name.lower() == target_name]

    if args.limit_projects > 0:
        processable = [decision for decision in decisions if decision.should_process]
        allowed_names = {decision.path.name for decision in processable[: args.limit_projects]}
        decisions = [
            decision
            for decision in decisions
            if not decision.should_process or decision.path.name in allowed_names
        ]

    processable_projects = [decision for decision in decisions if decision.should_process]
    skipped_projects = [decision for decision in decisions if not decision.should_process]

    if not decisions:
        print("No matching project folders were found.")
        return 1

    if not processable_projects:
        if args.project and skipped_projects:
            skip_reason = skipped_projects[0].reason
            print(f"ERROR: Project folder '{args.project}' was found but skipped: {skip_reason}")
            return 1
        if args.recent_days > 0:
            print(f"No eligible project folders were found with supported files modified in the last {args.recent_days} day(s).")
            return 1
        print("No eligible project folders were found after discovery rules were applied.")
        return 1

    if args.pick:
        selected_project = pick_project(processable_projects)
        processable_projects = [selected_project]
        skipped_projects = []

    processed_count = 0
    project_output_dirs: list[Path] = []
    for decision in processable_projects:
        project = decision.path
        scan = collect_project_sources(project, settings)
        output_dir = settings.output_dir / _slugify(project.name)
        if args.dry_run:
            print_dry_run_preview(
                project_name=project.name,
                source_paths=[source.relative_path for source in scan.sources],
                output_dir=output_dir,
            )
        else:
            settings.output_dir.mkdir(parents=True, exist_ok=True)
            print(f"[+] Scanning {project.name}")
            output_dir = write_project_outputs(scan, settings.output_dir, public_mode=args.public)
            print(f"    Sources used : {len(scan.sources)}")
            print(f"    Output saved : {output_dir}")
        processed_count += 1
        project_output_dirs.append(output_dir)

    index_path = None
    if not args.dry_run:
        index_path = write_run_index(settings.output_dir, processable_projects, skipped_projects)

    print("-" * 72)
    print("Processed folders:")
    for decision in processable_projects:
        print(f"  - {decision.path.name} ({decision.reason})")
    print("Skipped folders:")
    for decision in skipped_projects:
        print(f"  - {decision.path.name} ({decision.reason})")
    print("-" * 72)
    if args.open:
        if args.dry_run:
            print("Quick-access files: no output files were written because --dry-run was used.")
        else:
            print_quick_access_paths(project_output_dirs)
        print("-" * 72)
    if args.dry_run:
        print("Run index      : not written in dry-run mode")
    else:
        print(f"Run index      : {index_path}")
    print(f"Completed {processed_count} project(s).")
    return 0
