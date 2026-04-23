# Commands Used

This file includes only commands, filters, or analysis actions that are documented or clearly supported by the completed source material. The exact command used to generate the primary 9 failed SSH attempts against username `fakeuser` was not found in the inspected source files.

## Documented Commands And Filters

| Command / Filter / Action | Source | Purpose | Result Summary |
|---|---|---|---|
| `for i in {1..10}; do su root; done` | `threat-hunting-with-wazuh/readme.md` | Generate repeated failed authentication attempts in a Wazuh-monitored lab | Wazuh Rule ID `5763` fired for multiple authentication failures and mapped to MITRE T1110 |
| `tcp.port == 22` | `Incident_Report_SSH_BruteForce.docx` | Wireshark filter used to isolate SSH traffic during brute force validation | Wireshark confirmed rapid TCP connections on port 22 consistent with brute force behavior |
| Hydra launched from Kali | `Incident_Report_SSH_BruteForce.docx` | Simulate SSH brute force activity against Ubuntu | Wazuh logged 10 failed SSH attempts under Rule ID `5760`; exact Hydra command was not documented in the report |

## Supported Wazuh Review Actions

| Action | Source | Purpose | Result Summary |
|---|---|---|---|
| Review Wazuh failed-login / authentication failure alerts | `soc-alert-triage-lab/technical.md` | Confirm failed SSH login activity | 9 failed attempts from `192.168.32.128` against host `tren`, username `fakeuser` |
| Check for successful login events | `soc-alert-triage-lab/technical.md`; `blue-team-dashboard-analysis-with-wazuh/technical.md` | Determine whether the failed attempts led to access | No successful login observed in the primary SOC triage scenario; 0 successful logins validated in dashboard analysis |
| Review Wazuh dashboard failed-login panels | `blue-team-dashboard-analysis-with-wazuh/readme.md` | Triage failed SSH authentication activity visually | 9 authentication failures detected, source activity concentrated in a short time window, target host `tren` |
| Review MITRE brute-force mapping | `blue-team-dashboard-analysis-with-wazuh/readme.md`; `threat-hunting-with-wazuh/readme.md` | Connect alert activity to known attacker behavior | Activity mapped to MITRE ATT&CK T1110 / password guessing |

## Notes

- No Windows Event ID 4625 commands or Windows authentication queries were added because the completed source projects did not support that content.
- No fake screenshot capture commands were added.
- If the exact primary attack command is found later, add it here with the source path and result summary.
