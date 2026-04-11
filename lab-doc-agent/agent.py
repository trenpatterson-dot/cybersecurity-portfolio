"""
Lab Documentation Agent
Prompts for lab details, generates docs, posts to Notion, commits to GitHub.
"""

import os
import sys
import re
import json
import textwrap
from datetime import datetime
from pathlib import Path

import anthropic
from notion_client import Client as NotionClient
from git import Repo, InvalidGitRepositoryError
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_PAGE_ID = os.getenv("NOTION_PAGE_ID")
GITHUB_REPO_PATH = os.getenv("GITHUB_REPO_PATH")

MODEL = "claude-sonnet-4-6"


# ---------------------------------------------------------------------------
# Prompt helpers
# ---------------------------------------------------------------------------

def ask(prompt: str, multiline: bool = False) -> str:
    """Prompt the user for input. Use multiline=True for paragraph-length answers."""
    print(f"\n{prompt}")
    if multiline:
        print("(Enter your response, then type END on a new line when done)")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        return "\n".join(lines).strip()
    return input("> ").strip()


def collect_lab_details() -> dict:
    print("\n" + "=" * 60)
    print("  LAB DOCUMENTATION AGENT")
    print("=" * 60)
    print("Answer the questions below. Your answers fuel every output.\n")

    details = {}
    details["lab_name"] = ask("Lab name / title?")
    details["platform"] = ask("Platform (e.g. TryHackMe, HackTheBox, home lab)?")
    details["date"] = ask(f"Date completed? [default: {datetime.today().strftime('%Y-%m-%d')}]") or datetime.today().strftime('%Y-%m-%d')
    details["objective"] = ask("What was the objective of the lab?", multiline=True)
    details["tools"] = ask("What tools did you use? (comma-separated, e.g. Nmap, Metasploit, Wireshark)")
    details["steps"] = ask("Walk me through what you did step by step:", multiline=True)
    details["findings"] = ask("What did you find / what was the outcome?", multiline=True)
    details["learned"] = ask("What did you learn or what clicked for you?", multiline=True)
    details["difficulty"] = ask("Difficulty rating? (1–5)")
    details["tags"] = ask("Tags / categories? (e.g. enumeration, privilege-escalation, OSINT)")

    return details


# ---------------------------------------------------------------------------
# Claude generation
# ---------------------------------------------------------------------------

def generate_all(details: dict) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    context = json.dumps(details, indent=2)

    prompts = {
        "eli10": f"""
You are writing for a curious 10-year-old who loves video games and technology.
Explain this cybersecurity lab in a fun, simple, exciting way. Use analogies to
games, adventures, or everyday life. No jargon. Max 200 words. Be enthusiastic.

Lab details:
{context}
""",
        "technical": f"""
You are a senior SOC analyst writing a professional technical writeup for a
cybersecurity portfolio. Include:
- Lab overview and objective
- Tools used (with brief purpose of each)
- Methodology / steps taken
- Key findings and results
- Defensive takeaways or mitigations
- Skills demonstrated

Be precise and structured. Use markdown headers. Target audience: hiring managers
and security professionals.

Lab details:
{context}
""",
        "linkedin": f"""
Write a LinkedIn post about completing this cybersecurity lab.

Style rules — follow every one:
- Punchy, confident, zero fluff
- Start with a hook (not "I just completed...")
- Short paragraphs, max 3 lines each
- Include 1-2 concrete things learned
- End with a question OR a call to action
- 3-5 relevant hashtags at the end
- Max 250 words total
- No corporate buzzwords, no humble-bragging

Lab details:
{context}
""",
    }

    outputs = {}
    for key, prompt in prompts.items():
        print(f"  Generating {key}...", end=" ", flush=True)
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        outputs[key] = response.content[0].text.strip()
        print("done")

    return outputs


# ---------------------------------------------------------------------------
# File output
# ---------------------------------------------------------------------------

def save_outputs(details: dict, outputs: dict) -> Path:
    safe_name = re.sub(r"[^\w\-]", "_", details["lab_name"].lower())
    date_str = details["date"].replace("-", "")
    folder_name = f"{date_str}_{safe_name}"
    out_dir = Path(__file__).parent / "outputs" / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "eli10.md").write_text(outputs["eli10"], encoding="utf-8")
    (out_dir / "technical_writeup.md").write_text(outputs["technical"], encoding="utf-8")
    (out_dir / "linkedin_post.md").write_text(outputs["linkedin"], encoding="utf-8")
    (out_dir / "lab_details.json").write_text(json.dumps(details, indent=2), encoding="utf-8")

    print(f"\n  Files saved → {out_dir}")
    return out_dir


# ---------------------------------------------------------------------------
# Notion
# ---------------------------------------------------------------------------

def _rich_text(text: str) -> list:
    return [{"type": "text", "text": {"content": text[:2000]}}]


def _heading(text: str, level: int = 2) -> dict:
    return {
        "object": "block",
        "type": f"heading_{level}",
        f"heading_{level}": {"rich_text": _rich_text(text)},
    }


def _paragraph(text: str) -> list:
    """Split long text into multiple paragraph blocks (Notion 2000-char limit)."""
    blocks = []
    for chunk in textwrap.wrap(text, 1900, break_long_words=False, replace_whitespace=False):
        blocks.append({
            "object": "block",
            "type": "paragraph",
            "paragraph": {"rich_text": _rich_text(chunk)},
        })
    return blocks


def _bullet(text: str) -> dict:
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {"rich_text": _rich_text(text[:2000])},
    }


def _divider() -> dict:
    return {"object": "block", "type": "divider", "divider": {}}


def _normalize_page_id(page_id: str) -> str:
    """Accept a Notion page ID with or without dashes, or a full URL."""
    # Strip URL down to the ID portion (last path segment, before any ?)
    if page_id.startswith("http"):
        page_id = page_id.rstrip("/").split("/")[-1].split("?")[0]
        # Last 32 hex chars (may be appended after a dash in the slug)
        page_id = page_id.split("-")[-1] if "-" in page_id else page_id

    # Remove dashes then reformat as UUID: 8-4-4-4-12
    raw = page_id.replace("-", "")
    if len(raw) == 32:
        return f"{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}"
    return page_id  # return as-is if it doesn't look like a UUID


def push_to_notion(details: dict, outputs: dict) -> str:
    notion = NotionClient(auth=NOTION_TOKEN)

    page_id = _normalize_page_id(NOTION_PAGE_ID)

    tools_list = [t.strip() for t in details["tools"].split(",")]
    tags_list = [t.strip() for t in details["tags"].split(",")]

    # Build child blocks
    blocks = [
        _heading("Lab Overview", 2),
        *_paragraph(f"Platform: {details['platform']}"),
        *_paragraph(f"Date: {details['date']}"),
        *_paragraph(f"Difficulty: {details['difficulty']}/5"),
        *_paragraph(f"Tags: {details['tags']}"),
        _divider(),

        _heading("Objective", 2),
        *_paragraph(details["objective"]),
        _divider(),

        _heading("Tools Used", 2),
        *[_bullet(tool) for tool in tools_list],
        _divider(),

        _heading("ELI10 — Explain Like I'm 10", 2),
        *_paragraph(outputs["eli10"]),
        _divider(),

        _heading("Technical Writeup", 2),
        *_paragraph(outputs["technical"]),
        _divider(),

        _heading("What I Learned", 2),
        *_paragraph(details["learned"]),
        _divider(),

        _heading("LinkedIn Post", 2),
        *_paragraph(outputs["linkedin"]),
    ]

    page = notion.pages.create(
        parent={"page_id": page_id},
        properties={
            "title": {
                "title": _rich_text(f"{details['date']} — {details['lab_name']}")
            }
        },
        children=blocks,
    )

    url = page.get("url", "")
    print(f"  Notion page created → {url}")
    return url


# ---------------------------------------------------------------------------
# GitHub commit
# ---------------------------------------------------------------------------

def commit_to_github(out_dir: Path, details: dict) -> bool:
    if not GITHUB_REPO_PATH:
        print("  GITHUB_REPO_PATH not set — skipping GitHub commit.")
        return False

    try:
        repo = Repo(GITHUB_REPO_PATH)
    except InvalidGitRepositoryError:
        print(f"  {GITHUB_REPO_PATH} is not a git repo — skipping.")
        return False

    # Copy output folder into the repo under lab-docs/
    import shutil
    dest = Path(GITHUB_REPO_PATH) / "lab-doc-agent" / "outputs" / out_dir.name
    dest.mkdir(parents=True, exist_ok=True)
    for f in out_dir.iterdir():
        shutil.copy2(f, dest / f.name)

    repo.index.add([str(dest.relative_to(GITHUB_REPO_PATH)).replace("\\", "/")])

    safe_name = re.sub(r"[^\w\-]", "-", details["lab_name"].lower()).strip("-")
    commit_msg = f"Add lab writeup: {safe_name} ({details['date']})"
    repo.index.commit(commit_msg)

    print(f"  Committed to repo → \"{commit_msg}\"")
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    # Validate env
    missing = [k for k in ["ANTHROPIC_API_KEY", "NOTION_TOKEN", "NOTION_PAGE_ID"] if not os.getenv(k)]
    if missing:
        print(f"ERROR: Missing env vars: {', '.join(missing)}")
        print("Copy .env.example → .env and fill in your keys.")
        sys.exit(1)

    # 1. Collect details
    details = collect_lab_details()

    print("\n" + "=" * 60)
    print("  GENERATING OUTPUTS (Claude API)")
    print("=" * 60)

    # 2. Generate with Claude
    outputs = generate_all(details)

    # 3. Save files locally
    print("\n" + "=" * 60)
    print("  SAVING FILES")
    print("=" * 60)
    out_dir = save_outputs(details, outputs)

    # 4. Push to Notion
    print("\n" + "=" * 60)
    print("  NOTION")
    print("=" * 60)
    try:
        push_to_notion(details, outputs)
    except Exception as e:
        print(f"  Notion error: {e}")

    # 5. GitHub commit
    print("\n" + "=" * 60)
    print("  GITHUB")
    print("=" * 60)
    try:
        commit_to_github(out_dir, details)
    except Exception as e:
        print(f"  GitHub error: {e}")

    # 6. Print outputs to terminal
    print("\n" + "=" * 60)
    print("  OUTPUTS")
    print("=" * 60)

    print("\n--- ELI10 ---")
    print(outputs["eli10"])

    print("\n--- LINKEDIN POST ---")
    print(outputs["linkedin"])

    print("\n--- TECHNICAL WRITEUP ---")
    print(outputs["technical"])

    print("\n" + "=" * 60)
    print("  ALL DONE")
    print("=" * 60)


if __name__ == "__main__":
    main()
