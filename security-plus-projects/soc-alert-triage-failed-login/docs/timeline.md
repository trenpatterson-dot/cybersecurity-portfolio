# Timeline

## Primary SOC Alert Triage Timeline

The completed primary SOC alert triage source files do not include exact timestamps for the `fakeuser` failed-login activity. This timeline uses the documented investigation sequence without inventing times.

| Time | Event | Notes |
|---|---|---|
| Not documented | Wazuh lab environment prepared | Source lab documents fixing Wazuh API connectivity, verifying manager/dashboard functionality, configuring SSH on the Ubuntu target, and fixing host-only VM networking |
| Not documented | Failed SSH login activity generated | Kali Linux attacker machine generated repeated failed SSH login attempts against the Ubuntu/Wazuh environment |
| Not documented | Wazuh captured authentication failure alerts | Source lab documents Wazuh alerts for authentication failures |
| Not documented | Analyst reviewed alert details | Source IP `192.168.32.128`, target host `tren`, and attempted username `fakeuser` were identified |
| Not documented | Failed attempts confirmed | 9 failed SSH login attempts were detected |
| Not documented | Successful-login check completed | Source lab states no successful login was observed |
| Not documented | Alert mapped to brute force behavior | Rule ID `2502`, Severity 10, mapped to MITRE ATT&CK T1110 in the technical source |
| Not documented | Final classification completed | Lab-generated SSH brute force / failed-login activity with no successful access observed |

## Supporting SSH Brute Force Incident Report Timeline

The incident report provides exact times for a separate but related SSH brute force scenario.

| Time | Event | Notes |
|---|---|---|
| 21:30:30 | Hydra launched from Kali | Attacker IP `192.168.64.133` |
| 21:30:34 | Wazuh began logging authentication failures | Wazuh SIEM detected failed SSH activity |
| 21:30:34 | 10 failed SSH attempts recorded | Rule ID `5760`, `sshd: authentication failed` |
| 21:30:34 | Wireshark captured SSH traffic | Filter documented as `tcp.port == 22` |
| 21:30:34 | Attack completed with 0 successful logins | Incident report states the attack was unsuccessful |

## Dashboard Review Sequence

The Wazuh dashboard analysis source supports the analyst review flow:

| Step | Review Area | Purpose |
|---|---|---|
| 1 | Dashboard overview | Confirm Wazuh visibility and alert summary |
| 2 | Failed logins panel | Review failed SSH authentication count |
| 3 | Authentication failure panel | Validate auth failure activity |
| 4 | MITRE brute-force panel | Confirm brute force / T1110 mapping |
| 5 | Alert evolution panel | Review activity concentration in a short time window |
| 6 | Top agent panel | Confirm affected host context |

## Timeline Notes

- Exact timestamps for the primary `fakeuser` scenario are still a remaining evidence gap.
- Exact timestamps from the incident report are included only for the supporting Hydra scenario.
- No Windows Event ID 4625 timeline was added because no completed source evidence was found.
