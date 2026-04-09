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
    print("-" * 72)

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

    settings.output_dir.mkdir(parents=True, exist_ok=True)

    processed_count = 0
    for decision in processable_projects:
        project = decision.path
        print(f"[+] Scanning {project.name}")
        scan = collect_project_sources(project, settings)
        output_dir = write_project_outputs(scan, settings.output_dir)
        print(f"    Sources used : {len(scan.sources)}")
        print(f"    Output saved : {output_dir}")
        processed_count += 1

    index_path = write_run_index(settings.output_dir, processable_projects, skipped_projects)

    print("-" * 72)
    print("Processed folders:")
    for decision in processable_projects:
        print(f"  - {decision.path.name} ({decision.reason})")
    print("Skipped folders:")
    for decision in skipped_projects:
        print(f"  - {decision.path.name} ({decision.reason})")
    print("-" * 72)
    print(f"Run index      : {index_path}")
    print(f"Completed {processed_count} project(s).")
    return 0
