## Overview

This lab is a self-built home SIEM deployment using Wazuh to simulate attacker behavior across mixed-OS endpoints and validate real-time detection. The project covers the full blue team cycle: infrastructure provisioning, agent enrollment, controlled attack execution, alert triage in the Wazuh Dashboard, and SOC-style documentation with MITRE ATT&CK mapping. Two detection scenarios were executed — credential access via `/etc/shadow` and brute force authentication — both triggered and triaged in the live Wazuh environment.

---

## Tools & Environment

| Component | Detail |
|---|---|
| Hypervisor | VMware Workstation |
| SIEM Platform | Wazuh (Manager, Indexer/OpenSearch, Dashboard) |
| Attacker Machine | Kali Linux |
| Target Endpoint | Ubuntu 24.04 (Wazuh Agent) |
| Additional Endpoint | Windows 11 (Wazuh Agent via MSI) |
| Network | Internal NAT |
| Key Ports | TCP 1515 (agent enrollment), TCP 55000 (Wazuh API) |

---

## Steps Performed

1. **Lab provisioning** — Deployed three VMs in VMware Workstation: Wazuh Server (Ubuntu), monitored target (Ubuntu 24.04), and attacker (Kali Linux); a Windows 11 endpoint was also enrolled.
2. **Wazuh stack installation** — Installed Wazuh Manager, Indexer (OpenSearch), and Dashboard on the Ubuntu server VM.
3. **Troubleshooting** — Resolved startup failures including: Wazuh Manager not initially installed, API port 55000 not listening, and password desynchronization between the Dashboard and the API service (resolved via Wazuh password tools and service restarts).
4. **Agent enrollment** — Opened TCP port 1515 and configured `ossec.conf` on the Ubuntu agent with the manager IP; enrolled the Windows 11 agent via MSI package. Both verified active in the Dashboard.
5. **Detection 1 – Credential Access:** Executed `sudo su`, `whoami`, and `cat /etc/shadow` on the monitored Ubuntu endpoint; triaged the resulting Wazuh alert and mapped to MITRE ATT&CK T1003.008.
6. **Detection 2 – Brute Force:** Executed `for i in {1..10}; do su root; done` on the Ubuntu target; observed Wazuh Rule 5763 fire in the Dashboard and correlated timestamps with attacker terminal output.
7. **Alert triage** — Reviewed alerts in Wazuh Discover, examining rule IDs, severity, source context, and timestamps. Documented all findings with screenshots.

---

## Findings

| Finding | Detail |
|---|---|
| **Rule 5763 triggered** | Fired within seconds of brute force loop start; consistent with MITRE T1110 (Brute Force) |
| **`/etc/shadow` accessed** | Read under elevated privileges (`sudo su`); exposes password hashes — maps to MITRE T1003.008 |
| **Sub-10-second detection latency** | Timestamp correlation between attacker terminal and SIEM alert confirmed minimal log forwarding lag |
| **Silent agent misconfiguration** | A misconfigured `ossec.conf` caused log forwarding to fail with no visible error in the Dashboard |
| **Port 1515 blockage** | Closed firewall port prevented agent registration entirely, leaving the endpoint silently unmonitored |
| **API credential desync** | Password mismatch between Dashboard and API service disabled management-plane visibility; resolved by credential reset and service restart |
| **Multi-OS agent coverage** | Both Ubuntu and Windows 11 agents successfully enrolled and actively forwarding logs |

---

## Security Significance

This lab demonstrates two high-value blue team competencies. First, it validates Wazuh's real-time detection pipeline — Rule 5763 and the `/etc/shadow` alert both fired with sub-10-second latency, a meaningful benchmark for SOC mean-time-to-detect evaluation. Second, the deployment challenges uncovered three classes of critical SIEM blind spots: misconfigured `ossec.conf` produces silent log-forwarding failure, a closed enrollment port leaves endpoints completely unregistered, and API credential drift silently disables dashboard management — none of which surface visible errors by default. Identifying and resolving these issues demonstrates operational SIEM hardening knowledge beyond basic deployment, and the MITRE ATT&CK mappings (T1003.008, T1110) tie each detection directly to real-world adversary techniques.