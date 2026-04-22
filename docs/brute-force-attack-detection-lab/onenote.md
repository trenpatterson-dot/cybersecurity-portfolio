All source files are fully read and consistent. I have everything I need — including the QA revision notes to address. Generating the final structured output now.

---

## Lab Recap

- **Lab Name:** Brute Force Attack Detection Lab
- **Platform:** Standalone Home Lab — VMware Workstation Pro (Kali Linux attacker + Ubuntu target + Wazuh SIEM)
- **Lab Type:** Brute Force Simulation / SIEM Detection / Incident Response
- **Date Completed:** April 16, 2026
- **Objective:** Simulate a real-world SSH brute force attack in a controlled environment using Hydra, capture the attack traffic live with Wireshark, detect and alert on it automatically with Wazuh SIEM, map all findings to MITRE ATT&CK, and produce a professional incident report covering the full attack → detection → remediation workflow.
- **Tools Used:**
  - `Hydra v9.6` — dictionary-based brute force engine (attacker)
  - `Wazuh SIEM` — log ingestion, rule-based alerting, MITRE ATT&CK mapping
  - `Wireshark` — live network packet capture (Kali)
  - `Kali Linux` (`192.168.64.133`) — attacker VM
  - `Ubuntu` (`192.168.64.130`) — target VM running OpenSSH Server
  - `OpenSSH Server` — intentionally exposed attack surface on target
  - `VMware Workstation Pro` — lab virtualization / network isolation
- **What I Did:**
  1. Provisioned two VMs in VMware Workstation Pro — Kali Linux as the attacker (`192.168.64.133`) and Ubuntu as the target (`192.168.64.130`) on a shared local network segment.
  2. Verified bi-directional network reachability with a ping test — 29 packets transmitted, **0% packet loss**.
  3. Installed and enabled OpenSSH Server on Ubuntu, deliberately exposing SSH on port 22 with no compensating controls (intentional misconfiguration scenario — no firewall rules, no fail2ban, no key-based auth).
  4. Launched Wireshark on Kali and applied display filter `tcp.port == 22` to isolate all SSH traffic, armed **before** the attack began.
  5. Executed a Hydra dictionary attack against the Ubuntu SSH service targeting username `tren` with a custom local wordlist:
     ```bash
     hydra -l tren -P ~/passwords.txt ssh://192.168.64.130
     ```
  6. Watched Wireshark capture a high-frequency burst of TCP connections to port 22 from Kali in real time during Hydra execution.
  7. Reviewed the Wazuh dashboard and events view — confirmed 10 automatically generated alerts, rule metadata, and MITRE ATT&CK technique tagging with zero manual tuning required.
  8. Documented all findings and produced a formal incident report (`Incident_Report_SSH_BruteForce.docx`) covering attack timeline, IOCs, alert data, and layered remediation recommendations.

- **What I Found / Results:**

  | Field | Value |
  |---|---|
  | SIEM Rule Triggered | Rule ID 5760 — `sshd: authentication failed` |
  | Alert Level | 5 |
  | Total Alerts Generated | **10** |
  | Successful Logins | **0** |
  | MITRE ATT&CK Mapping | T1110 — Brute Force: Password Guessing / SSH (T1110.001) |
  | Attacker IP | `192.168.64.133` (Kali) |
  | Target IP | `192.168.64.130` (Ubuntu) |
  | Targeted Username | `tren` |
  | Wordlist | `~/passwords.txt` (custom local list) |
  | Network Evidence | Wireshark: rapid TCP SYN bursts to port 22 from single source IP |

  - Wazuh detected all 10 authentication failures automatically — no custom rules or manual tuning required, validating out-of-box coverage.
  - The attack was entirely unsuccessful — zero credentials were compromised — keeping the lab safely contained.
  - Wazuh automatically enriched every alert with MITRE ATT&CK technique tags (T1110 — Password Guessing, SSH), surfaced directly in the dashboard.
  - Wireshark provided a second, independent **network-layer** corroboration alongside the **log-layer** SIEM detection.
  - Rule ID 5763 (Wazuh's brute force *threshold* aggregate alert) was **not triggered** during this lab — a meaningful architectural gap noted for remediation.

- **What Clicked / What I Learned:**
  - **Rule 5760 vs. Rule 5763 — individual vs. aggregate detection:** Rule 5760 fires on each individual auth failure (noisy, low-confidence); Rule 5763 fires when the brute force *threshold* is crossed (aggregate pattern, high-confidence escalation signal). Understanding this layering is essential for SOC triage — and the fact that 5763 never fired means an attacker with a larger wordlist could have continued unimpeded past detection without a response action.
  - **Two detection planes beat one:** Wazuh caught the attack at the *log layer* (auth failures in syslog/auditd); Wireshark caught it at the *network layer* (SYN bursts to port 22). Correlating both in a real SOC eliminates false-positive doubt and dramatically increases alert confidence.
  - **Username enumeration comes first:** Hydra's `-l tren` flag means the attacker needed a valid username *before* the password guessing phase was useful. This makes username exposure (verbose SSH error messages, OSINT, etc.) its own upstream risk worth hardening separately.
  - **Detection without response is incomplete:** Wazuh fired alerts, but nothing blocked the attacker. Configuring Wazuh active response to auto-block the source IP on Rule 5763 would close the loop — turning a passive SIEM into an active control, which is the lightweight SOAR pattern.
  - **Intentional misconfiguration is the real threat model:** No firewall, no fail2ban, default SSH on port 22 — this mirrors how exposed servers routinely sit on the internet. The lab made that abstract threat concrete.

- **Difficulty:** Medium
- **Screenshots:**

  | # | File | What It Shows |
  |---|---|---|
  | 01 | `screenshots/01_ping_test.png` | Ping output from Kali → Ubuntu: 29 packets transmitted, 0% packet loss |
  | 02 | `screenshots/02_ssh_install.png` | Ubuntu terminal: OpenSSH Server installation and/or service enable/start output |
  | 03 | `screenshots/03_wireshark_filter_ready.png` | Wireshark on Kali with `tcp.port == 22` display filter applied, capture armed before attack launch |
  | 04 | `screenshots/04_wireshark_attack_capture.png` | Wireshark live capture: high-frequency TCP connections to port 22 during Hydra execution |
  | 05 | `screenshots/05_hydra_attack.png` | Hydra terminal on Kali: command execution and per-attempt results against `ssh://192.168.64.130` targeting `tren` |
  | 06 | `screenshots/06_wazuh_dashboard.png` | Wazuh dashboard: Rule ID 5760 alerts, Alert Level 5, MITRE ATT&CK T1110 technique tags |
  | 07 | `screenshots/07_wazuh_events.png` | Wazuh events view: 10 individual `sshd: authentication failed` alert entries |

- **Tags:** `#brute-force` `#SSH` `#Wazuh` `#SIEM` `#Hydra` `#Wireshark` `#MITRE-ATT&CK` `#T1110` `#T1110.001` `#detection-engineering` `#home-lab` `#SOC` `#incident-response` `#linux` `#VMware`

---

## Study Notes

### Wazuh SSH Brute Force Rules — Know Both
| Rule ID | Trigger | Alert Level | SOC Action |
|---|---|---|---|
| **5760** | Single `sshd: authentication failed` event | 5 | Log / low-priority |
| **5763** | Brute force *threshold* crossed (aggregate) | Higher | Escalate / block |

> Rule 5760 alone = noise. Rule 5763 = confirmed brute force — escalate and respond.

### Hydra Quick Reference
```bash
hydra -l <user>   -P <wordlist>  ssh://<target-ip>   # single username, password list
hydra -L <users>  -P <wordlist>  ssh://<target-ip>   # username list + password list
```

### Wireshark — SSH Triage Filter
```
tcp.port == 22
```
**Brute force network signature:** high-frequency TCP SYN packets from a single source IP to port 22, with no sustained session establishment.

### MITRE ATT&CK Mapping
- **T1110** — Brute Force
  - **T1110.001** — Password Guessing (known username + wordlist via SSH)

### Layered Remediation Stack
1. **fail2ban** — auto-block source IP after N failures (rate-limiting)
2. **Key-based SSH auth** — eliminates the password attack surface entirely
3. **`PermitRootLogin no`** in `/etc/ssh/sshd_config` — reduce privilege exposure
4. **Wazuh active response** — SIEM-driven automated IP block on Rule 5763 (detection → response loop)
5. **Monitor Rule 5763** — your threshold-level brute force confirmation signal

### Core Mental Model
> **Log-layer (SIEM) + Network-layer (Wireshark/IDS) = high-confidence, low-false-positive brute force triage.**
> In a real SOC, corroborating both data planes before escalating is standard practice. Neither alone is sufficient.

---

> ⚠️ **QA Note (from `qa_report_attempt1.json`):** The three explicit OpenSSH bash commands (`sudo apt install openssh-server`, `sudo systemctl enable ssh`, `sudo systemctl start ssh`) that appeared in a prior generated output were flagged as **plausible but not verbatim-evidenced** in the source README or `commands_seen` in `evidence.json`. They are technically correct standard commands and shown in `02_ssh_install.png`, but should be treated as **illustrative** rather than confirmed verbatim commands from the lab session. All other content in these notes is fully source-verified.