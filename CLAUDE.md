# Tren Patterson — Cybersecurity Portfolio Context

This file is read automatically by Claude Code and Cowork when this folder is open.
It contains everything needed to pick up any session without re-explaining.

---

## Who This Is

**Name:** Tren Patterson | tren.patterson@gmail.com
**Location:** Clermont, FL
**Current Role:** Spectrum Internet/Voice Repair Rep 2
**Education:** B.S. Cybersecurity — Bellevue University (expected 2026)
**Career Target:** SOC Analyst / Blue Team
**GitHub:** https://github.com/trenpatterson-dot
**Portfolio Repo:** https://github.com/trenpatterson-dot/cybersecurity-portfolio

---

## Folder Locations

| Resource | Path |
|---|---|
| Portfolio (this repo) | `C:\Users\trenp\cybersecurity-portfolio` |
| Screenshots | `C:\Users\trenp\OneDrive\Pictures\Screenshots 1` |
| Workflow docs | `C:\Users\trenp\cybersecurity-portfolio\lab-workflow\` |
| Lab intake template | `C:\Users\trenp\cybersecurity-portfolio\lab-workflow\LAB-INTAKE.md` |

**Mounted paths (Cowork/Linux):**
- Portfolio → `/sessions/kind-sleepy-shannon/mnt/cybersecurity-portfolio`
- Screenshots → `/sessions/kind-sleepy-shannon/mnt/Screenshots 1`

---

## Lab Workflow (Cowork)

When Tren finishes a lab, the workflow is:
1. He pastes the intake form (from `lab-workflow/LAB-INTAKE.md`) or the `SESSION-CONTEXT.md` from the previous lab
2. Claude creates the lab folder, copies screenshots, writes all docs, stages git commit
3. Tren runs `git push` from VS Code
4. Claude drafts the LinkedIn post

**At the end of every lab session, Claude auto-saves a `SESSION-CONTEXT.md` inside the lab folder** with everything filled in so the next session starts instantly.

### Lab Folder Structure
```
[lab-name]/
├── README.md
├── SESSION-CONTEXT.md         ← paste this next session to resume
├── screenshots/
├── docs/
└── agent-output/
    ├── eli10.md
    ├── technical-summary.md
    ├── linkedin-post.md
    ├── onenote-notes.md
    └── sources.md
```

### Where New Labs Go
| Lab Type | Location |
|---|---|
| TryHackMe | `tryhackme/[room-name]/` |
| SIEM / Wazuh / Splunk | `[lab-name]/` (root) |
| Kali / Pentest | `[lab-name]/` (root) |
| Incident Response | `labs/[lab-name]/` |
| CYBR 445 class | `CYBR 445/[module]/` |

---

## Git Setup

- Remote: `https://github.com/trenpatterson-dot/cybersecurity-portfolio.git`
- Branch: `main`
- Auth: PAT stored in remote URL (Cowork environment only)
- **Claude handles:** `git add` + `git commit`
- **Tren handles:** `git push` (from VS Code or terminal)

---

## Voice & Content Rules

All written content follows the `tren-voice` skill. Key rules:
- Direct, confident, zero fluff
- Blue team / SOC framing always
- No: "I'm excited to share", "passionate", "game-changer", "dive deep"
- Frame Spectrum ISP experience as real-world network ops (not "call center")
- Labs are portfolio pieces, not just exercises

---

## Current Labs & Projects

| Lab | Type | Status |
|---|---|---|
| tryhackme/* | TryHackMe rooms | Various |
| threat-hunting-wazuh | SIEM/Wazuh | Complete |
| brute-force-detection-lab | SIEM | Complete |
| metasploitable-vsftpd-exploit-lab | Pentest | Complete |
| lab1-nmap-reconnaissance | Pentest | Complete |
| advanced-network-intrusion-detection-lab | Network | Complete |
| cyber-deception | IR/Deception | Complete |
| CYBR 445 | Class (Bellevue) | In Progress |

---

## How to Start a New Lab Session

If Tren pastes a `SESSION-CONTEXT.md`, immediately read it and start building.
If he describes a lab verbally, ask for:
- Lab name, platform, tools used
- Steps taken, findings, what clicked
- Which screenshots to pull

Then: create folder → copy screenshots → write all docs → `git add` + `git commit` → show LinkedIn draft → save `SESSION-CONTEXT.md`.
