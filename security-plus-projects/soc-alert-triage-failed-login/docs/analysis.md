# Analysis

## Investigation Goal

Analyze repeated failed SSH login activity detected by Wazuh and determine whether the activity represents benign authentication failure, lab-generated brute force behavior, or activity requiring escalation.

This analysis is based on completed Linux SSH / Wazuh evidence. No Windows Event ID 4625 evidence was found in the completed source projects.

## Security+ Alignment

This project aligns to Security+ style analyst skills: log review, alert triage, authentication failure analysis, incident documentation, threat classification, and remediation planning. The focus is on the blue-team decision process: validate the alert, confirm the scope, identify the source and target, check whether access succeeded, and document the recommended action.

## Source Evidence Reviewed

| Source | Evidence Used |
|---|---|
| `soc-alert-triage-lab/readme.md` | Primary Wazuh SOC alert triage scenario and key findings |
| `soc-alert-triage-lab/technical.md` | Rule ID `2502`, Severity 10, source IP, target host, attempted username, no success observed, MITRE T1110 |
| `blue-team-labs/soc-alert-triage-lab/README.md` | Confirms the primary SOC alert triage scenario |
| `threat-hunting-with-wazuh/readme.md` | Wazuh deployment context, Rule ID `5763`, alert triage workflow, MITRE T1110 |
| `blue-team-dashboard-analysis-with-wazuh/readme.md` | Dashboard-based triage, failed-login panels, 9 auth failures, 0 successful logins |
| `blue-team-dashboard-analysis-with-wazuh/technical.md` | Dashboard validation steps and MITRE brute force mapping |
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/README.md` | Screenshot references for dashboard evidence |
| `blue-team-labs/brute-force-detection-lab/Incident_Report_SSH_BruteForce.docx` | Supporting Hydra brute force incident, Wazuh Rule ID `5760`, Wireshark validation, remediation |

## Primary Alert Context

| Field | Value |
|---|---|
| Detection source | Wazuh SIEM |
| Alert type | Failed SSH login / authentication failure |
| Source IP | `192.168.32.128` |
| Target host | `tren` (Ubuntu) |
| Username attempted | `fakeuser` |
| Failed attempts | 9 |
| Successful login observed | No |
| Rule metadata | Rule ID `2502`, Severity 10 |
| MITRE mapping | T1110 - Brute Force |
| Environment | Kali Linux attacker machine against Ubuntu/Wazuh lab environment |

## Supporting Incident Context

The SSH brute force incident report provides a second supported example of the same detection pattern:

| Field | Value |
|---|---|
| Tool used | Hydra v9.6 |
| Attacker IP | `192.168.64.133` |
| Target IP | `192.168.64.130` |
| Target service | SSH, port 22 |
| Failed attempts | 10 |
| Successful logins | 0 |
| Wazuh Rule ID | `5760` |
| Rule description | `sshd: authentication failed` |
| Alert level | 5 |
| Packet capture validation | Wireshark filter `tcp.port == 22` |
| MITRE mapping | Password Guessing, SSH |

## Analyst Workflow

1. Reviewed the Wazuh alert context and confirmed the activity was authentication related.
2. Identified the source IP, target host, and attempted username from the primary SOC triage source.
3. Confirmed the number of failed SSH login attempts.
4. Checked whether any successful login was observed after the failed attempts.
5. Compared the failed-login activity against Wazuh dashboard analysis showing authentication failures, failed-login panels, and no successful logins.
6. Used the incident report as supporting evidence for how Wazuh Rule ID `5760` and Wireshark can validate SSH brute force behavior.
7. Mapped the supported activity to MITRE ATT&CK T1110 / password guessing.
8. Documented remediation guidance supported by the incident report.

## Screenshot Evidence Referenced

The source projects reference screenshots that support Wazuh dashboard review and brute force detection. They have not been copied into this destination folder yet.

| Source Screenshot | Relevance |
|---|---|
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/01-dashboard-overview.png` | Wazuh dashboard overview |
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/02-failed-logins-panel.png` | Failed login visualization |
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/03-auth-failure-panel.png` | Authentication failure panel |
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/04-mitre-brute-force-panel.png` | MITRE brute force mapping |
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/05-alert-evolution-panel.png` | Alert timing / evolution view |
| `blue-team-labs/blue-team-dashboard-analysis-with-wazuh/screenshots/06-top-agent-panel.png` | Affected agent context |
| `blue-team-labs/threat-hunting-wazuh/screenshots/brute-force-detection.png` | Wazuh brute force detection |
| `blue-team-labs/threat-hunting-wazuh/screenshots/attack-simulation-terminal.png` | Attack simulation terminal |
| `blue-team-labs/threat-hunting-wazuh/screenshots/wazuh-overview-dashboard.png` | Wazuh overview dashboard |

## Analyst Determination

The primary activity is confirmed as repeated failed SSH authentication against host `tren` from source IP `192.168.32.128` using username `fakeuser`. Because the source lab states that no successful login was observed, the event did not progress to confirmed unauthorized access. The supported classification is lab-generated SSH brute force / password guessing activity detected by Wazuh.

In a production SOC, this alert would warrant source validation, account review, and blocking or containment if the source were unauthorized. Defensive follow-up should include `fail2ban`, key-based SSH authentication, disabling direct root SSH login, Wazuh active response, and monitoring for Wazuh Rule ID `5763`.
