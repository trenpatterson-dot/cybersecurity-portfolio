# Cowork Lab Workflow — Tren Patterson

This is the step-by-step process for turning a completed lab into a finished GitHub writeup + LinkedIn post using Cowork.

---

## How It Works

You do the lab. I handle the documentation, folder setup, screenshots, and commit.
You do one final `git push` to publish.

---

## The 5-Step Process

### Step 1 — Tell Me About the Lab
Start a new Cowork session and say:

> "I just finished [lab name]. Let me walk you through what I did."

Then give me:
- **Lab name** (e.g., "Blue Room TryHackMe" or "Wazuh Credential Stuffing Detection")
- **Platform** (TryHackMe / home lab / Hack The Box / class assignment)
- **Objective** — what was the goal?
- **Tools used** — list every tool you touched
- **What you did** — walk me through the steps, even rough notes are fine
- **What you found** — results, alerts fired, flags captured, access gained
- **What clicked** — what you learned or understood better

You can dump this all at once or we can go back and forth. Either works.

---

### Step 2 — Screenshots
Tell me which screenshots go with the lab. You can say:

- "Use the screenshots from today" — I'll pull the most recent ones from your Screenshots folder
- "Use these files: 01_nmap.png, 02_alert.png" — I'll grab specific files
- "I'll add screenshots manually" — I'll skip this step

Screenshots live at: `C:\Users\trenp\OneDrive\Pictures\Screenshots 1`

---

### Step 3 — I Build Everything
I will:
1. Create the lab folder in the right location in your portfolio
2. Copy screenshots into `screenshots/`
3. Write all documentation into `agent-output/`:
   - `eli10.md` — plain-English explanation (non-technical audience)
   - `technical-summary.md` — full writeup for hiring managers and SOC leads
   - `linkedin-post.md` — ready-to-post LinkedIn content in your voice
   - `onenote-notes.md` — your personal reference notes
   - `sources.md` — tools, CVEs, and references used
4. Write the `README.md` — the GitHub-facing writeup
5. Stage and commit everything to git locally

---

### Step 4 — Review
I'll show you:
- The LinkedIn post draft (review and approve before posting)
- The README preview
- What was committed

You make any edits, I update the files.

---

### Step 5 — You Push
Open VS Code (or your terminal) and run:

```bash
git push
```

That publishes everything to GitHub. Then you copy the LinkedIn post and post it.

---

## Lab Folder Structure

Every lab gets this structure:

```
[lab-name]/
├── README.md                  ← GitHub-facing writeup
├── screenshots/               ← All screenshots for this lab
│   └── *.png
├── docs/                      ← Any extra notes, configs, or command output
└── agent-output/              ← Claude-generated content
    ├── eli10.md
    ├── technical-summary.md
    ├── linkedin-post.md
    ├── onenote-notes.md
    └── sources.md
```

---

## Where Labs Go in the Portfolio

| Lab Type | Folder Location |
|---|---|
| TryHackMe rooms | `tryhackme/[room-name]/` |
| SIEM / Wazuh / Splunk | `[lab-name]/` (root level) |
| Kali / Pen test | `[lab-name]/` (root level) |
| Incident Response | `labs/[lab-name]/` |
| CYBR 445 class | `CYBR 445/[module]/` |

---

## Quick-Start Commands

**See recent screenshots:**
```bash
cd lab-workflow && python setup_lab.py
```

**Manually set up a new lab folder:**
```bash
python lab-workflow/setup_lab.py tryhackme/blue-room 01_nmap.png 02_alert.png
```

**Push to GitHub (run from your machine):**
```bash
git push
```

---

## Notes

- I handle: folder creation, screenshot copying, all writing, git add + commit
- You handle: `git push` + LinkedIn post (copy/paste)
- The PAT is stored in the git remote config for this repo only
- Screenshots folder: `C:\Users\trenp\OneDrive\Pictures\Screenshots 1`
- Portfolio root: `C:\Users\trenp\cybersecurity-portfolio`
