## Lab Recap

- **Lab Name:** Threat Hunting with Wazuh
- **Platform:** Wazuh SIEM (Manager · Indexer/OpenSearch · Dashboard · Agents) — hosted in VMware Workstation
- **Lab Type:** Threat Hunting / SIEM — Attack Simulation, Alert Detection & SOC Triage Documentation
- **Date Completed:** 2025-07-14
- **Objective:** Deploy Wazuh across multi-OS endpoints (Ubuntu 24.04 + Windows 11), simulate real attacker techniques from Kali Linux (credential access and brute force), detect those techniques in the Wazuh dashboard in real time, triage the resulting alerts, and document findings with MITRE ATT&CK mapping using a full blue-team workflow.
- **Tools Used:**
  - Wazuh Manager, Indexer (OpenSearch), Dashboard
  - Wazuh Agent — Ubuntu (ossec.conf) and Windows 11 (MSI package)
  - VMware Workstation (Internal NAT network)
  - Kali Linux (attacker VM)
  - Ubuntu 24.04 (target endpoint VM)
  - Windows 11 (second monitored endpoint)
- **What I Did:**
  1. Provisioned three VMs in VMware Workstation on an Internal NAT network: Wazuh Server (Ubuntu), Target Endpoint (Ubuntu 24.04), Attacker (Kali Linux); also enrolled a Windows 11 VM.
  2. Installed and configured Wazuh Manager, Indexer, and Dashboard on the server VM.
  3. Troubleshot a series of setup failures: manager service not installed, API port 55000 not listening, API credential desync between Dashboard and API service, and TCP port 1515 blocked for agent enrollment.
  4. Reset API credentials via Wazuh password tools, updated `wazuh.yml` dashboard config, restarted all three Wazuh services, and confirmed API online.
  5. Enrolled the Ubuntu agent by editing `ossec.conf` with the manager IP; enrolled Windows 11 via MSI installer pointed at the manager. Verified both agents active in the Agents panel.
  6. **Detection 1 — Credential Access (MITRE T1003.008):** On the Ubuntu target ran `sudo su` → `whoami` → `cat /etc/shadow` to simulate reading the Linux shadow password file under elevated privileges. Triaged the resulting Wazuh alert.
  7. **Detection 2 — Brute Force (MITRE T1110):** Ran `for i in {1..10}; do su root; done` on the Ubuntu target to generate 10 rapid consecutive failed authentication events. Observed Wazuh Rule 5763 fire in the dashboard.
  8. Performed timestamp correlation between attacker terminal output and SIEM alert timestamp; measured detection latency.
  9. Triaged alerts in Wazuh Discover: reviewed rule IDs, severity, source context, and timestamps.
  10. Documented all findings with MITRE ATT&CK mapping and captured four screenshots for a SOC-style lab report.
- **What I Found / Results:**

  | Finding | Significance |
  |---|---|
  | **Wazuh Rule 5763** fired within seconds of brute force loop starting | Confirms real-time detection; reliable trigger on multiple auth failures → MITRE T1110 |
  | `cat /etc/shadow` executed under `sudo su` on monitored endpoint | Exposes password hashes; cleanly maps to MITRE T1003.008 (OS Credential Dumping: /etc/shadow) |
  | **Sub-10-second detection latency** confirmed via timestamp correlation | Validates log-forwarding pipeline; directly relevant to SOC MTTD benchmarking |
  | **Misconfigured `ossec.conf`** caused silent log-forwarding failure | No alerts, no visible errors in dashboard — critical blind-spot risk in real deployments |
  | **TCP 1515 not open** blocked agent enrollment entirely | Firewall misconfiguration can silently leave endpoints unmonitored |
  | **API credential desync** took dashboard management plane offline | Credential mismatch between SIEM components disables visibility; fixed by password reset + service restart |
  | **Both Ubuntu and Windows 11 agents** successfully enrolled and forwarding | Multi-OS SIEM coverage demonstrated end-to-end |

- **What Clicked / What I Learned:**
  - A misconfigured or unreachable agent produces *no errors in the Wazuh dashboard* — you only notice when alerts stop or enrollment never appears. Proactive agent health checks are essential.
  - Wazuh's built-in ruleset (Rule 5763) handles common attack patterns out of the box — you don't need custom rules to catch textbook brute force.
  - SIEM deployment is as much a *network/firewall problem* as a software problem: ports 1515 (enrollment) and 55000 (API) must be explicitly allowed or everything silently breaks.
  - Timestamp correlation between attacker terminal and SIEM is a powerful validation technique for assessing pipeline lag — and a skill directly transferable to real SOC MTTD work.
  - Reading `/etc/shadow` is a high-fidelity credential dumping simulation on Linux — Wazuh's file integrity and audit rules surface it clearly, giving a concrete T1003.008 artifact.

- **Difficulty:** Medium *(setup troubleshooting raised the difficulty; detection work itself was straightforward once the environment was stable)*
- **Screenshots:**

  | File | What It Shows |
  |---|---|
  | `screenshots/wazuh-overview-dashboard.png` ✅ | Wazuh manager overview dashboard — monitored agent summary and triggered alert counts |
  | `screenshots/agents-active.png` ✅ | Agents panel — Ubuntu and Windows 11 endpoints enrolled and reporting active |
  | `screenshots/attack-simulation-terminal.png` ✅ | Ubuntu/Kali terminal — brute force loop or credential access commands executing |
  | `screenshots/brute-force-detection.png` ✅ | Wazuh dashboard alert view — Rule 5763 triggered by the brute force simulation |

- **Tags:** `#wazuh` `#siem` `#threat-hunting` `#blue-team` `#brute-force` `#credential-access` `#mitre-attack` `#T1110` `#T1003.008` `#linux` `#windows` `#kali` `#soc-analyst` `#home-lab` `#vmware` `#opensearch` `#alert-triage` `#log-analysis`

---

## Study Notes

### Wazuh Architecture (3 tiers)
| Component | Role |
|---|---|
| **Manager** | Receives logs, applies rules, generates alerts |
| **Indexer** (OpenSearch) | Stores and indexes alert data |
| **Dashboard** | Visualization + triage UI (Discover, Alerts, Agents) |
| **Agent** | Installed on endpoint; forwards logs via TCP **1515** (enrollment) |

### Critical Ports
- `1515` — Agent enrollment *(must be open or agents can't register — silently)*
- `55000` — Wazuh REST API *(blocked = dashboard management plane goes offline)*

### Key Commands (Lab)
```bash
sudo su && whoami && cat /etc/shadow   # T1003.008 — credential access simulation
for i in {1..10}; do su root; done    # T1110 — brute force simulation
```

### Wazuh Rules to Know
| Rule ID | Trigger | MITRE TTP |
|---|---|---|
| **5763** | Multiple consecutive authentication failures | T1110 — Brute Force |

### MITRE Mappings
- **T1110** — Brute Force: repeated failed `su`/SSH attempts
- **T1003.008** — OS Credential Dumping: `/etc/passwd` and `/etc/shadow`

### SOC Mental Models
> **"No alert ≠ no problem."** A misconfigured agent silently stops forwarding — always verify agent health, not just alert volume.

> **Timestamp correlation = MTTD.** Cross-referencing attacker terminal time with SIEM alert time measures your detection pipeline's real-world lag.

> **SIEM deployment is a network problem first.** Lock down firewall rules for enrollment and API ports before troubleshooting software.