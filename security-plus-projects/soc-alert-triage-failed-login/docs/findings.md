# Findings

## Confirmed Primary Findings

| Finding | Value | Source Support |
|---|---|---|
| Detection source | Wazuh SIEM | SOC Alert Triage Lab |
| Activity type | Repeated failed SSH login attempts | SOC Alert Triage Lab |
| Failed attempts | 9 | SOC Alert Triage Lab |
| Source IP | `192.168.32.128` | SOC Alert Triage Lab |
| Target host | `tren` (Ubuntu) | SOC Alert Triage Lab |
| Target username | `fakeuser` | SOC Alert Triage Lab |
| Successful login observed | No | SOC Alert Triage Lab |
| Rule metadata | Rule ID `2502`, Severity 10 | `soc-alert-triage-lab/technical.md` |
| MITRE ATT&CK mapping | T1110 - Brute Force | `soc-alert-triage-lab/technical.md` |
| Classification | Lab-generated SSH brute force / failed-login activity | Supported by failed attempts, Wazuh alerting, no successful login, and MITRE T1110 mapping |

## Supporting Incident Report Findings

| Finding | Value | Source Support |
|---|---|---|
| Attack type | SSH brute force | `Incident_Report_SSH_BruteForce.docx` |
| Tool used | Hydra v9.6 | `Incident_Report_SSH_BruteForce.docx` |
| Attacker IP | `192.168.64.133` | `Incident_Report_SSH_BruteForce.docx` |
| Target IP | `192.168.64.130` | `Incident_Report_SSH_BruteForce.docx` |
| Target service | SSH, port 22 | `Incident_Report_SSH_BruteForce.docx` |
| Failed attempts | 10 | `Incident_Report_SSH_BruteForce.docx` |
| Successful logins | 0 | `Incident_Report_SSH_BruteForce.docx` |
| Wazuh Rule ID | `5760` | `Incident_Report_SSH_BruteForce.docx` |
| Rule description | `sshd: authentication failed` | `Incident_Report_SSH_BruteForce.docx` |
| Alert level | 5 | `Incident_Report_SSH_BruteForce.docx` |
| MITRE mapping | Password Guessing, SSH | `Incident_Report_SSH_BruteForce.docx` |
| Network corroboration | Wireshark confirmed rapid TCP connections on port 22 | `Incident_Report_SSH_BruteForce.docx` |

## Wazuh Rule Context

- Rule ID `2502` is supported by the primary SOC alert triage technical summary and is tied to the 9 failed SSH attempts against `tren`.
- Rule ID `5760` is supported by the SSH brute force incident report as `sshd: authentication failed`.
- Rule ID `5763` is supported by the Wazuh threat-hunting source as multiple authentication failures, and the incident report recommends monitoring it as the brute force threshold alert.

## Analyst Conclusion

The evidence supports a failed SSH login triage scenario detected by Wazuh. The primary case shows 9 failed SSH attempts from `192.168.32.128` against host `tren` using username `fakeuser`, with no successful login observed. The supporting incident report confirms the same pattern in a separate Hydra scenario: Wazuh Rule ID `5760`, 10 failed SSH attempts, 0 successful logins, and Wireshark validation of SSH traffic.

The final disposition is unsuccessful SSH brute force / password guessing activity in a controlled lab environment. In a real SOC, the recommended next step would be to validate whether the source is authorized, block or rate-limit the source if unauthorized, review the targeted account, and confirm no successful authentication occurred after the failure burst.

## Recommended Remediation

The following remediation actions are supported by the SSH brute force incident report:

- Install `fail2ban` to automatically block IPs after repeated failed login attempts.
- Disable password-based SSH authentication and require key-based authentication.
- Disable direct root SSH login in `sshd_config`.
- Configure Wazuh active response to auto-block brute force source IPs.
- Monitor for Wazuh Rule ID `5763`, the brute force threshold alert.

## Security Value

- Demonstrates authentication alert triage from detection to disposition.
- Shows how to distinguish failed authentication from confirmed compromise.
- Reinforces source, target, account, and rule validation.
- Connects Wazuh alert metadata to MITRE ATT&CK brute force / password guessing behavior.
- Converts lab evidence into a Security+ aligned SOC analyst workflow.
