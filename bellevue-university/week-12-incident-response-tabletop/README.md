# Incident Response Tabletop — NIST SP 800-61 Ransomware Scenario

Documentation-based tabletop exercise applying the full NIST SP 800-61 incident response lifecycle to a ransomware scenario.

## Overview

Acme Corp gets hit with ransomware. Three accounting workstations and a file server are encrypted. One user clicked a phishing attachment at 1:47 PM — confirmed in email gateway logs. Help desk starts getting calls at 2:14 PM.

This exercise works through every IR phase in order: detection, containment, eradication, recovery, and lessons learned. No VM. No live environment. Just the scenario, the framework, and structured decision-making under pressure.

## Framework

- **NIST SP 800-61 Rev 2** — Computer Security Incident Handling Guide

## Scenario Facts

| Item | Detail |
|---|---|
| Affected systems | 3 accounting workstations + FS01 |
| Potential exposure | 1 additional workstation (same VLAN, unvalidated) |
| Initial access | Phishing email attachment (1:47 PM) |
| Detection | Help desk calls (2:14 PM, 3 calls in 10 min) |
| Severity | Critical |
| Last backup | Monday 11 PM |
| Data loss window | Up to 15 hours |

## Attack Timeline

- **1:47 PM** — User clicks phishing attachment
- **Shortly after** — Malware executes, local files begin encrypting
- **Spread** — Ransomware moves to FS01 via accessible shares
- **2:14 PM** — Help desk receives first of 3 calls within 10 minutes

## Key Takeaways

- Containment and eradication are distinct phases — conflating them causes reinfection
- The 4th workstation (same VLAN, unaffected) is a trap — assume exposure until validated
- Recovery means restoring safely, not just restoring fast
- Backup gap (15 hours) is a business risk decision, not a technical problem
- Chain of custody: image the drive first, analyze the image, never touch the original

## Preparation Gaps Identified

- No phishing prevention / email filtering
- No endpoint detection (EDR)
- Poor VLAN segmentation (FS01 reachable via user shares)
- Weak user awareness training
- IR plan not regularly tested

## Agent Output Files

| File | Description |
|---|---|
| [eli10.md](agent-output/eli10.md) | Plain-English explanation for non-technical readers |
| [technical-summary.md](agent-output/technical-summary.md) | Full technical writeup |
| [linkedin-post.md](agent-output/linkedin-post.md) | LinkedIn portfolio post |
| [onenote-notes.md](agent-output/onenote-notes.md) | Personal notes and gotchas |
| [github-update.md](agent-output/github-update.md) | GitHub README content |
| [sources.md](agent-output/sources.md) | References and resources |
