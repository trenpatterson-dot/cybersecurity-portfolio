# Lab Documentation Agent

A Python automation tool that turns raw lab notes into a full portfolio publication in one command. Prompts for lab details, generates six document types via the Claude API, pushes to Notion, and commits to GitHub.

---

## What It Does

1. Collects lab details interactively (name, platform, tools, steps, findings, takeaways)
2. Calls the **Claude API** to generate six outputs in parallel:
   - ELI10 summary (explain like I'm 10)
   - Technical writeup (SOC/hiring manager audience)
   - LinkedIn post (voice-matched, no fluff)
   - GitHub README section
   - Personal reference notes
   - Sources and references
3. Saves all outputs locally under `outputs/[date]_[lab-name]/`
4. Creates a structured page in **Notion** with all content
5. Commits the output folder to this GitHub repo

---

## Usage

```bash
# Full interactive run (collect details + generate + publish)
python agent.py

# Publish an existing output folder
python publish.py
```

---

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env  # fill in your keys
```

Required environment variables in `.env`:

```
ANTHROPIC_API_KEY=...
NOTION_TOKEN=...
NOTION_PAGE_ID=...
GITHUB_REPO_PATH=...
```

---

## Stack

| Component | Purpose |
|---|---|
| `anthropic` | Claude API — generates all written content |
| `notion-client` | Pushes structured pages to Notion |
| `gitpython` / `subprocess` | Commits output to the portfolio repo |
| `python-dotenv` | Loads credentials from `.env` |

---

## Output Structure

```
outputs/
└── 20260415_wireshark_packet_analysis/
    ├── lab_details.json
    ├── eli10.md
    ├── technical_writeup.md
    ├── linkedin_post.md
    ├── github_update.md
    ├── onenote_notes.md
    └── sources.md
```

---

## Skills Demonstrated

- Claude API (Anthropic SDK) — multi-prompt generation pipeline
- Notion API — programmatic page creation with batched block writes
- Git automation via subprocess with UTF-8 encoding on Windows
- Environment-based configuration and secrets management
- Content sanitization for third-party API content filters
