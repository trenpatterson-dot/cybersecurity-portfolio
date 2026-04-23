# Incident Response Tabletop – NIST SP 800-61 Ransomware Scenario
## Overview
A documentation-based tabletop exercise applying the full NIST SP 800-61 incident response lifecycle to a ransomware scenario. This exercise works through every IR phase in order: detection, containment, eradication, recovery, and lessons learned. No VM. No live environment. Just the scenario, the framework, and structured decision-making under pressure.

## Objectives
- Apply the full NIST SP 800-61 incident response lifecycle to a ransomware scenario.
- Demonstrate understanding of preparation gaps in incident response.
- Showcase effective communication and documentation skills.

## Tools Used
- NIST SP 800-61 Rev 2 (Computer Security Incident Handling Guide)
- CISA Ransomware Guide
- MITRE ATT&CK
- CompTIA Security+ Study Guide (SY0-701)
- Email gateway logging (scenario artifact)
- IT help desk call logs (scenario artifact)

## Steps Performed
1. Mapped all six NIST SP 800-61 IR lifecycle phases and documented each phase with practical explanations.
2. Assessed Preparation phase: identified strengths (daily backups, email gateway logging) and gaps (no EDR, no phishing filtering, poor segmentation, weak user training, untested IR plan).
3. Analyzed Detection phase: correlated help desk calls (2:14 PM, 3 calls in under 10 minutes) with email gateway log evidence of phishing attachment click at 1:47 PM.
4. Classified incident severity as Critical.
5. Constructed attack timeline from log evidence: 1:47 PM click → malware executes and encrypts local files → lateral spread to FS01 via SMB shares → 2:14 PM help desk detection.
6. Documented Containment actions: isolate affected workstations and FS01 from network, block phishing sender/indicators, preserve logs and evidence, flag fourth VLAN workstation as potentially exposed pending validation.
7. Documented Eradication actions: full log review across endpoint, email, server, and network layers; remove malware and all persistence mechanisms; reset compromised credentials; patch initial access vector.
8. Documented Recovery actions: verify eradication before any restore, restore FS01 from Monday 11 PM backup, rebuild or restore affected workstations, validate restored files and systems, monitor closely for reinfection, phase systems back into production.
9. Quantified data loss window: up to 15 hours due to backup gap between Monday 11 PM and incident time.
10. Produced Lessons Learned: root cause (phishing attachment), backup gap as business risk, recommendations for email filtering, EDR deployment, improved VLAN segmentation, user awareness training, and IR plan testing cadence.

## Key Findings
- Initial access confirmed via phishing email attachment clicked by one user at 1:47 PM, evidenced by email gateway logs.
- Ransomware encrypted three accounting workstations and file server FS01; files renamed with .locked extension and ransom notes were present.
- Lateral movement from workstations to FS01 occurred via accessible SMB shares.
- A fourth workstation on the same VLAN appeared unaffected but was treated as potentially exposed until validated.
- Help desk received three calls within 10 minutes beginning at 2:14 PM, indicating detection of the incident.
- Containment and eradication are distinct phases; conflating them causes reinfection.
- The 4th workstation (same VLAN, unvalidated) is a trap; assume exposure until validated.
- Recovery means restoring safely, not just restoring fast.
- Backup gap (15 hours) is a business risk decision, not a technical problem.
- Chain of custody: image the drive first, analyze the image, never touch the original.

## Revision Notes
Remove the raw '## Screenshots\\n[]' section from the bottom of the output readme.md. The source README.md does not include this section. If a screenshots section is required by template, render it as '## Screenshots\\nNone.' rather than exposing the raw empty-array literal from the intake pipeline. All other content is approved – make no other changes.

## Agent Output Files
- [eli10.md](agent-output/eli10.md): Plain-English explanation for non-technical readers.
- [technical-summary.md](agent-output/technical-summary.md): Full technical writeup.
- [linkedin-post.md](agent-output/linkedin-post.md): LinkedIn portfolio post.
- [onenote-notes.md](agent-output/onenote-notes.md): Personal notes and gotchas.
- [github-update.md](agent-output/github-update.md): GitHub README content.
- [sources.md](agent-output/sources.md): References and resources.

## Git Status
- Committed: pending push
- Branch: main

## Next Steps
- `git push` from VS Code or terminal
- Post linkedin-post.md to LinkedIn
- Read NIST 800-61 Rev 2 full document (not just framework summary)
- Find a real ransomware case study and map it to this lifecycle