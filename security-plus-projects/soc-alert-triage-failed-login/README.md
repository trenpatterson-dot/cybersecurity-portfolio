# SSH Brute Force Detection and SIEM Investigation with Wazuh
Simulated and investigated an SSH brute force attack using Wazuh SIEM, correlating authentication failures, source IP activity, and MITRE ATT&CK techniques to produce a SOC-ready incident analysis.
## Project Overview

This Security+ aligned project presents a SOC analyst workflow for detecting and investigating SSH brute force activity in Wazuh. It focuses on repeated failed SSH login alerts, SIEM triage, source and target identification, successful-login validation, MITRE ATT&CK mapping, and practical remediation.

The evidence comes from completed portfolio work across the SOC Alert Triage Lab, Wazuh threat-hunting labs, Wazuh dashboard analysis, and the SSH brute force incident report. The goal is to show the full blue-team path from alert review to documented analyst outcome.

This project is based on Linux SSH authentication evidence. No completed repository match was found for Windows Event ID 4625, so this write-up does not claim Windows authentication event coverage.

## Objective

- Triage a failed-login alert from initial detection through analyst disposition.
- Identify the source, target, username, detection platform, and alert metadata.
- Confirm whether any successful authentication followed the failed attempts.
- Map supported activity to MITRE ATT&CK brute force / password guessing behavior.
- Document the investigation in a Security+ friendly portfolio format.
- Capture remediation options that reduce future SSH brute force risk.

## Tools Used

| Tool | Role |
|---|---|
| Wazuh SIEM | Alert detection, rule evaluation, and authentication failure review |
| Wazuh Dashboard | Alert triage, visualization, MITRE mapping, and failed-login panels |
| Ubuntu | Wazuh / target host environment documented in the completed labs |
| Kali Linux | Attacker machine used to generate failed SSH login activity |
| Hydra v9.6 | SSH brute force tool documented in the incident report |
| Wireshark | Packet capture validation for SSH traffic on port 22 |
| VMware / host-only lab networking | Virtual lab environment used for the completed work |

## Investigation Summary

The primary SOC Alert Triage Lab documented repeated failed SSH login attempts from a Kali Linux attacker machine against an Ubuntu Wazuh environment. Wazuh detected 9 failed SSH login attempts from source IP `192.168.32.128` against target host `tren` using the attempted username `fakeuser`. The source write-up states that no successful login was observed.

Related Wazuh dashboard analysis supports the same investigation pattern: failed SSH authentication activity was reviewed in Wazuh dashboard views, 9 authentication failures were detected, 0 successful logins were validated, the target host was `tren`, and the activity was mapped to MITRE ATT&CK T1110 (Brute Force).

The supporting SSH brute force incident report documents a second confirmed SSH brute force scenario: Hydra was launched from Kali at `192.168.64.133` against Ubuntu target `192.168.64.130`, Wazuh logged 10 failed SSH attempts under Rule ID `5760` (`sshd: authentication failed`), Wireshark confirmed SSH traffic on port 22, and no successful logins occurred.

## Key Findings

| Finding | Evidence |
|---|---|
| Repeated failed SSH login attempts occurred | Primary SOC triage source documents 9 failed SSH login attempts; incident report documents 10 failed SSH attempts |
| Primary source IP identified | `192.168.32.128` |
| Primary target host identified | `tren` (Ubuntu) |
| Primary targeted username identified | `fakeuser` |
| Supporting brute force source and target identified | Attacker `192.168.64.133` to target `192.168.64.130` |
| No successful login observed | Supported by both the SOC alert triage source and the incident report |
| Wazuh Rule ID `2502` supported | SOC alert triage technical summary lists Rule ID `2502`, Severity 10, mapped to MITRE ATT&CK T1110 |
| Wazuh Rule ID `5760` supported | Incident report lists Rule ID `5760`, `sshd: authentication failed`, Alert Level 5 |
| Wazuh Rule ID `5763` supported | Threat-hunting source documents Rule `5763` for multiple authentication failures; incident report recommends monitoring for Rule `5763` as the brute force threshold alert |
| MITRE brute force / password guessing mapping supported | Sources map activity to MITRE ATT&CK T1110 and password guessing / SSH |

## Skills Demonstrated

- SOC alert triage
- SSH failed-login investigation
- Wazuh SIEM alert review
- Source, target, and account identification
- Successful-login correlation
- Rule ID and severity interpretation
- MITRE ATT&CK mapping
- Packet-capture corroboration using Wireshark
- Security+ aligned remediation planning
- Portfolio-ready incident documentation
- SIEM log analysis (Wazuh)
- Alert triage and investigation workflow
- Brute force attack detection
- MITRE ATT&CK mapping (T1110)
- Incident documentation and reporting
- Basic network traffic validation (Wireshark)

## Evidence Location

- `docs/analysis.md` - investigation workflow and analyst reasoning
- `docs/findings.md` - confirmed evidence and final classification
- `docs/timeline.md` - event and investigation sequence
- `evidence/commands/commands-used.md` - documented commands, filters, and supported analysis actions

Supporting source evidence:

- `soc-alert-triage-lab/readme.md`
- `soc-alert-triage-lab/technical.md`
- `blue-team-labs/soc-alert-triage-lab/README.md`
- `threat-hunting-with-wazuh/readme.md`
- `blue-team-dashboard-analysis-with-wazuh/readme.md`
- `blue-team-dashboard-analysis-with-wazuh/technical.md`
- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/README.md`
- `blue-team-labs/brute-force-detection-lab/Incident_Report_SSH_BruteForce.docx`

Source screenshots are referenced but not duplicated into this folder yet:

- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/01-dashboard-overview.png`
- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/02-failed-logins-panel.png`
- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/03-auth-failure-panel.png`
- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/04-mitre-brute-force-panel.png`
- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/05-alert-evolution-panel.png`
- `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/06-top-agent-panel.png`
- `blue-team-labs/threat-hunting-wazuh/screenshots/brute-force-detection.png`
- `blue-team-labs/threat-hunting-wazuh/screenshots/attack-simulation-terminal.png`
- `blue-team-labs/threat-hunting-wazuh/screenshots/wazuh-overview-dashboard.png`

## Outcome

The activity was confirmed as repeated failed SSH authentication detected by Wazuh. The primary scenario is classified as lab-generated brute force behavior against host `tren` with no successful login observed. The supporting incident report reinforces the same detection pattern with Wazuh Rule ID `5760`, Wireshark validation, and an unsuccessful Hydra SSH brute force attempt.

Recommended defensive actions are to deploy `fail2ban`, disable password-based SSH authentication, enforce key-based SSH access, disable direct root SSH login, configure Wazuh active response for brute force sources, and monitor Wazuh Rule ID `5763` for brute force threshold alerts.
