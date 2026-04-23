"""
Lab Workflow Helper — Cowork Edition
Creates folder structure, copies screenshots, stages and commits to git.
Run this AFTER Claude has generated all content into the lab folder.

Usage:
  python setup_lab.py <lab_folder_name> [screenshot1.png screenshot2.png ...]

Examples:
  python setup_lab.py tryhackme/blue-room-walkthrough
  python setup_lab.py wazuh-credential-stuffing-lab 01_nmap.png 02_wazuh_alert.png
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────────
PORTFOLIO_ROOT = Path(__file__).parent.parent
SCREENSHOTS_SRC = Path("/sessions/kind-sleepy-shannon/mnt/Screenshots 1")

# ── Folder template ────────────────────────────────────────────────────────
LAB_TEMPLATE_DIRS = [
    "screenshots",
    "docs",
    "agent-output",
]

LAB_TEMPLATE_FILES = {
    "README.md": "# {lab_title}\n\n> Generated: {date}\n\n---\n\n*Content will be filled in by the Cowork workflow.*\n",
    "agent-output/eli10.md": "",
    "agent-output/technical-summary.md": "",
    "agent-output/linkedin-post.md": "",
    "agent-output/onenote-notes.md": "",
    "agent-output/sources.md": "",
}


def slugify(name: str) -> str:
    return name.lower().replace(" ", "-").replace("_", "-")


def create_lab_folder(lab_path: Path, lab_title: str):
    """Create the standard folder structure for a new lab."""
    lab_path.mkdir(parents=True, exist_ok=True)

    for d in LAB_TEMPLATE_DIRS:
        (lab_path / d).mkdir(parents=True, exist_ok=True)

    date_str = datetime.today().strftime("%Y-%m-%d")
    for filename, content in LAB_TEMPLATE_FILES.items():
        fpath = lab_path / filename
        if not fpath.exists():
            fpath.parent.mkdir(parents=True, exist_ok=True)
            fpath.write_text(content.format(lab_title=lab_title, date=date_str), encoding="utf-8")

    print(f"  ✅ Created lab folder: {lab_path}")


def copy_screenshots(lab_path: Path, screenshot_names: list[str]):
    """Copy named screenshots from the Screenshots folder into the lab."""
    dest = lab_path / "screenshots"
    dest.mkdir(exist_ok=True)
    copied = []
    missing = []

    for name in screenshot_names:
        src = SCREENSHOTS_SRC / name
        if src.exists():
            shutil.copy2(src, dest / name)
            copied.append(name)
        else:
            missing.append(name)

    if copied:
        print(f"  ✅ Copied {len(copied)} screenshot(s): {', '.join(copied)}")
    if missing:
        print(f"  ⚠️  Not found in Screenshots folder: {', '.join(missing)}")


def list_recent_screenshots(n: int = 20):
    """Print the most recently modified screenshots for reference."""
    if not SCREENSHOTS_SRC.exists():
        print(f"  ⚠️  Screenshots folder not found: {SCREENSHOTS_SRC}")
        return

    files = sorted(SCREENSHOTS_SRC.glob("*.png"), key=lambda f: f.stat().st_mtime, reverse=True)
    print(f"\n  📸 Most recent screenshots (last {n}):")
    for f in files[:n]:
        mtime = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
        print(f"    {mtime}  {f.name}")


def git_stage_and_commit(lab_rel_path: str, lab_title: str):
    """Stage the lab folder and commit to git (no push)."""
    import subprocess

    result = subprocess.run(
        ["git", "add", lab_rel_path],
        cwd=PORTFOLIO_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  git add failed: {result.stderr.strip()}")
        return False

    date_str = datetime.today().strftime("%Y-%m-%d")
    commit_msg = f"Add lab writeup: {slugify(lab_title)} ({date_str})"
    result = subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=PORTFOLIO_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"  ⚠️  git commit failed: {result.stderr.strip()}")
        return False

    print(f"  ✅ Committed: \"{commit_msg}\"")
    print(f"  👉 Run `git push` from VS Code or your terminal to publish.")
    return True


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n--- Recent screenshots ---")
        list_recent_screenshots()
        sys.exit(0)

    lab_rel = sys.argv[1].strip("/\\")
    screenshots = sys.argv[2:] if len(sys.argv) > 2 else []

    lab_path = PORTFOLIO_ROOT / lab_rel
    lab_title = Path(lab_rel).name.replace("-", " ").replace("_", " ").title()

    print(f"\n{'='*55}")
    print(f"  LAB SETUP: {lab_title}")
    print(f"{'='*55}")

    create_lab_folder(lab_path, lab_title)

    if screenshots:
        copy_screenshots(lab_path, screenshots)
    else:
        print("  ℹ️  No screenshots specified. Add them manually to the screenshots/ folder.")
        print("     Run with no args to see recent screenshots available.")

    print(f"\n  📁 Lab path: {lab_path}")
    print(f"  📝 Next: Claude fills in README and agent-output/ files, then commits.\n")


if __name__ == "__main__":
    main()
