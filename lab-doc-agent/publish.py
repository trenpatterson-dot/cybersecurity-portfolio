"""
publish.py — Push an existing lab output folder to Notion and GitHub.

Usage:
    python publish.py outputs/20260415_wireshark_packet_analysis
    python publish.py  # prompts you to pick from available folders
"""

import os
import sys
from pathlib import Path

# Pull shared functions from agent.py
sys.path.insert(0, str(Path(__file__).parent))
from agent import push_to_notion, commit_to_github, load_dotenv

from dotenv import load_dotenv
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
GITHUB_REPO_PATH = os.getenv("GITHUB_REPO_PATH")


def pick_folder() -> Path:
    outputs_dir = Path(__file__).parent / "outputs"
    folders = sorted([f for f in outputs_dir.iterdir() if f.is_dir()])
    if not folders:
        print("No output folders found in outputs/")
        sys.exit(1)

    print("\nAvailable output folders:")
    for i, f in enumerate(folders):
        print(f"  [{i + 1}] {f.name}")

    choice = input("\nPick a folder number: ").strip()
    try:
        return folders[int(choice) - 1]
    except (ValueError, IndexError):
        print("Invalid choice.")
        sys.exit(1)


def load_folder(out_dir: Path) -> tuple[dict, dict]:
    import json

    details_file = out_dir / "lab_details.json"
    if not details_file.exists():
        print(f"ERROR: lab_details.json not found in {out_dir}")
        print("This folder was generated outside the agent — create lab_details.json manually.")
        sys.exit(1)

    details = json.loads(details_file.read_text(encoding="utf-8"))

    outputs = {}
    file_map = {
        "eli10":         "eli10.md",
        "technical":     "technical_writeup.md",
        "linkedin":      "linkedin_post.md",
        "github_update": "github_update.md",
        "onenote":       "onenote_notes.md",
        "sources":       "sources.md",
    }
    for key, filename in file_map.items():
        f = out_dir / filename
        outputs[key] = f.read_text(encoding="utf-8") if f.exists() else ""

    return details, outputs


def main():
    missing = [k for k in ["NOTION_TOKEN", "NOTION_PAGE_ID"] if not os.getenv(k)]
    if missing:
        print(f"ERROR: Missing env vars: {', '.join(missing)}")
        sys.exit(1)

    # Resolve output folder
    if len(sys.argv) > 1:
        out_dir = Path(sys.argv[1])
        if not out_dir.is_absolute():
            out_dir = Path(__file__).parent / out_dir
    else:
        out_dir = pick_folder()

    if not out_dir.exists():
        print(f"ERROR: Folder not found: {out_dir}")
        sys.exit(1)

    print(f"\nPublishing: {out_dir.name}")
    details, outputs = load_folder(out_dir)

    print("\n" + "=" * 60)
    print("  NOTION")
    print("=" * 60)
    try:
        push_to_notion(details, outputs)
    except Exception as e:
        print(f"  Notion error: {e}")

    print("\n" + "=" * 60)
    print("  GITHUB")
    print("=" * 60)
    try:
        commit_to_github(out_dir, details)
    except Exception as e:
        print(f"  GitHub error: {e}")

    print("\n  Done.")


if __name__ == "__main__":
    main()
