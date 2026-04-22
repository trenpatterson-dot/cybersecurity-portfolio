"""
Job Application Tailor
Reads a job posting + your profile, generates tailored resume bullets,
cover letter, gap analysis, talking points, and logs the application.
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
PROFILE_PATH = Path(__file__).parent / "profile.md"


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def ask(prompt: str, multiline: bool = False) -> str:
    print(f"\n{prompt}")
    if multiline:
        print("(Paste your content, then type END on a new line when done)")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        return "\n".join(lines).strip()
    return input("> ").strip()


def collect_inputs() -> dict:
    print("\n" + "=" * 60)
    print("  JOB APPLICATION TAILOR")
    print("=" * 60)
    print("Paste the job posting and answer a few questions.\n")

    data = {}
    data["company"] = ask("Company name?")
    data["role"] = ask("Job title / role?")
    data["jd"] = ask("Paste the full job description:", multiline=True)
    data["notes"] = ask(
        "Anything specific you want emphasized? (e.g. a lab, a skill, a talking point) "
        "Leave blank to skip.",
        multiline=False,
    )
    data["date"] = datetime.today().strftime("%Y-%m-%d")
    return data


# ---------------------------------------------------------------------------
# Claude generation
# ---------------------------------------------------------------------------

def generate_all(data: dict, profile: str) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    # System prompt with profile cached — profile is static, won't change between runs
    system_blocks = [
        {
            "type": "text",
            "text": (
                "You are a career strategist specializing in cybersecurity hiring. "
                "You know exactly how SOC and blue team hiring managers think. "
                "Your job is to help a candidate present their real experience in the "
                "language the employer is already using — no fabrication, no padding, "
                "just precise alignment between what the candidate has done and what "
                "the employer is looking for.\n\n"
                "Candidate profile:\n\n"
                + profile
            ),
            "cache_control": {"type": "ephemeral"},
        }
    ]

    jd_block = f"Company: {data['company']}\nRole: {data['role']}\n\nJob Description:\n{data['jd']}"
    if data["notes"]:
        jd_block += f"\n\nCandidate emphasis notes: {data['notes']}"

    prompts = {
        "bullets": f"""
Analyze the job description and rewrite the candidate's resume experience as tailored bullets.

Rules:
- Mirror the JD's exact language and keywords where the candidate's experience legitimately matches
- Lead each bullet with a strong action verb
- Be specific — include tools, outcomes, and context
- Do NOT invent experience. Only use what's in the profile.
- Group bullets by section: Current Role, Labs & Projects, Technical Skills
- Flag any JD requirement the candidate can't honestly claim with [GAP]

{jd_block}
""",
        "cover_letter": f"""
Write a cover letter for this application.

Voice rules — non-negotiable:
- Direct and confident. No wind-up, no "I am writing to express my interest..."
- Zero fluff. Cut anything that doesn't add meaning.
- Blue team framing: frame experience through the defender's lens
- Do NOT use: "passionate", "excited to", "thrilled", "leverage", "synergy", "game-changer"
- Real talk — write like a sharp professional, not a corporate template
- 3 short paragraphs max: who you are + what you bring / why this role / close
- No sign-off platitudes ("I look forward to hearing from you at your earliest convenience")
- Max 250 words

{jd_block}
""",
        "gap_analysis": f"""
Identify the gaps between the job description requirements and the candidate's profile.

Format:
## Requirements the candidate meets
- List each one with a brief note on which experience covers it

## Gaps (requirements the candidate doesn't clearly demonstrate)
- List each gap
- For each gap, suggest a concrete action: lab to build, cert to pursue, or talking point to develop

Be honest and specific. Don't soften gaps — the candidate needs an accurate picture.

{jd_block}
""",
        "talking_points": f"""
Generate interview talking points for this specific role.

Structure:
## Why this company / role
2-3 specific, honest reasons based on the JD (not generic answers)

## Strength stories (STAR-lite format)
For the top 3 requirements in the JD, write a tight talking point the candidate can
deliver in 60-90 seconds: situation → what they did → result. Draw only from the profile.

## Questions to ask the interviewer
5 sharp, specific questions that show the candidate understands SOC operations and
has done their homework on this role. Not generic "what does a day look like" questions.

## How to address gaps
For each gap identified, write a 1-2 sentence honest bridge: what the candidate does
have, and what they're actively doing to close it.

{jd_block}
""",
    }

    outputs = {}
    for key, prompt in prompts.items():
        print(f"  Generating {key}...", end=" ", flush=True)
        response = client.messages.create(
            model=MODEL,
            max_tokens=2048,
            system=system_blocks,
            messages=[{"role": "user", "content": prompt}],
        )
        outputs[key] = response.content[0].text.strip()
        print("done")

    return outputs


# ---------------------------------------------------------------------------
# File output
# ---------------------------------------------------------------------------

def save_outputs(data: dict, outputs: dict) -> Path:
    safe_company = re.sub(r"[^\w\-]", "_", data["company"].lower())
    safe_role = re.sub(r"[^\w\-]", "_", data["role"].lower())
    folder_name = f"{data['date']}_{safe_company}_{safe_role}"
    out_dir = Path(__file__).parent / "outputs" / folder_name
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "tailored_bullets.md").write_text(outputs["bullets"], encoding="utf-8")
    (out_dir / "cover_letter.md").write_text(outputs["cover_letter"], encoding="utf-8")
    (out_dir / "gap_analysis.md").write_text(outputs["gap_analysis"], encoding="utf-8")
    (out_dir / "talking_points.md").write_text(outputs["talking_points"], encoding="utf-8")

    # Log the application
    log_entry = {
        "date": data["date"],
        "company": data["company"],
        "role": data["role"],
        "output_dir": str(out_dir),
        "jd_snippet": data["jd"][:500],
    }
    (out_dir / "application.json").write_text(
        json.dumps(log_entry, indent=2), encoding="utf-8"
    )

    # Append to master application log
    log_path = Path(__file__).parent / "application_log.jsonl"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")

    print(f"\n  Files saved → {out_dir}")
    return out_dir


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set. Add it to your .env file.")
        raise SystemExit(1)

    if not PROFILE_PATH.exists():
        print(f"ERROR: profile.md not found at {PROFILE_PATH}")
        print("Fill out profile.md with your experience before running.")
        raise SystemExit(1)

    profile = PROFILE_PATH.read_text(encoding="utf-8")

    # Collect inputs
    data = collect_inputs()

    print("\n" + "=" * 60)
    print("  GENERATING OUTPUTS (Claude API)")
    print("=" * 60)

    outputs = generate_all(data, profile)

    print("\n" + "=" * 60)
    print("  SAVING FILES")
    print("=" * 60)
    out_dir = save_outputs(data, outputs)

    print("\n" + "=" * 60)
    print("  OUTPUTS")
    print("=" * 60)

    print("\n--- TAILORED RESUME BULLETS ---")
    print(outputs["bullets"])

    print("\n--- COVER LETTER ---")
    print(outputs["cover_letter"])

    print("\n--- GAP ANALYSIS ---")
    print(outputs["gap_analysis"])

    print("\n--- TALKING POINTS ---")
    print(outputs["talking_points"])

    print("\n" + "=" * 60)
    print(f"  ALL DONE — {data['company']} / {data['role']}")
    print("=" * 60)
    print(f"  Output folder: {out_dir}")
    print(f"  Application logged to: application_log.jsonl")


if __name__ == "__main__":
    main()
