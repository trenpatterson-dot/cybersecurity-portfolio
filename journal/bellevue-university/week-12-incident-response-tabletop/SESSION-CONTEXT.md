# SESSION-CONTEXT — Week 12 Incident Response Tabletop

Paste this file at the start of the next session to resume instantly.

---

## Lab Identity

- **Lab name:** week-12-incident-response-tabletop
- **Display name:** Incident Response Tabletop — NIST SP 800-61 Ransomware Scenario
- **Type:** Bellevue University coursework
- **Folder:** `bellevue-university/week-12-incident-response-tabletop/`
- **Date completed:** 2026-04-19
- **Difficulty:** 2/5
- **Has screenshots:** No

---

## Scenario Summary

Acme Corp ransomware incident. Three accounting workstations and file server FS01 confirmed affected. Files renamed with `.locked` extension, ransom notes present. Fourth workstation in same VLAN treated as potentially exposed. No active VPN. Daily backups exist; last backup Monday 11 PM.

Framework: NIST SP 800-61 Rev 2

---

## Attack Timeline

- 1:47 PM — user clicks phishing attachment
- Shortly after — malware executes, local files begin encrypting
- Spread to FS01 via accessible shares
- 2:14 PM — help desk calls begin (3 calls in under 10 minutes)

---

## Key Numbers

- Affected: 3 accounting workstations + FS01
- Potentially exposed: 1 workstation (same VLAN, unvalidated)
- Severity: Critical
- Data loss window: up to 15 hours
- Recovery source: Monday 11 PM backup

---

## Files Written

- [x] agent-output/eli10.md
- [x] agent-output/technical-summary.md
- [x] agent-output/linkedin-post.md
- [x] agent-output/onenote-notes.md
- [x] agent-output/github-update.md
- [x] agent-output/sources.md
- [x] README.md
- [x] SESSION-CONTEXT.md

---

## Git Status

- Committed: pending push
- Branch: main

---

## Next Steps

- [ ] `git push` from VS Code or terminal
- [ ] Post linkedin-post.md to LinkedIn
- [ ] Read NIST 800-61 Rev 2 full document (not just framework summary)
- [ ] Find a real ransomware case study and map it to this lifecycle
