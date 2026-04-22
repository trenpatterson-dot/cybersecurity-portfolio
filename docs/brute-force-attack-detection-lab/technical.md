All source files are fully read and internally consistent. Writing the technical summary now, honoring the QA flag about the three OpenSSH bash commands being illustrative rather than verbatim-evidenced.

---

## Overview

This home lab simulates a complete SSH brute force attack cycle — from initial reconnaissance through SIEM-based detection — and exercises the end-to-end SOC workflow: attack execution, real-time network capture, automated alerting, and incident documentation. A Kali Linux VM acts as the attacker and an Ubuntu VM acts as the intentionally exposed target, both hosted in VMware Workstation Pro. Hydra v9.6 launches a dictionary-based credential attack against the Ubuntu SSH service while Wireshark captures the attack traffic and Wazuh SIEM independently detects and classifies the activity with no manual rule tuning.

---

## Tools & Environment

| Tool | Role |
|---|---|
| VMware Workstation Pro | Virtualization platform (standalone, host-only network) |
| Kali Linux (`192.168.64.133`) | Attacker VM |
| Ubuntu (`192.168.64.130`) | Target VM |
| OpenSSH Server | SSH attack surface on the Ubuntu target |
| Hydra v9.6 | SSH brute force / dictionary attack execution |
| Wireshark | Real-time network packet capture on the attacker |
| Wazuh SIEM | Log ingestion, automated alert generation, ATT&CK mapping |

---

## Steps Performed

1. **Environment provisioning** — Two VMs were configured in VMware Workstation Pro on a shared local network segment.
2. **Connectivity verification** — Ping from Kali to Ubuntu confirmed bi-directional reachability: 29 packets transmitted, 0% packet loss.
3. **Target exposure** — OpenSSH Server was installed and enabled on Ubuntu, intentionally exposing port 22 with no compensating access controls.
4. **Traffic capture setup** — Wireshark was launched on Kali with display filter `tcp.port == 22` applied before the attack began to isolate SSH traffic.
5. **Brute force execution** — Hydra was run against the target:
   ```bash
   hydra -l tren -P ~/passwords.txt ssh://192.168.64.130
   ```
   The attack targeted username `tren` using a custom local wordlist (`~/passwords.txt`).
6. **Packet capture** — Wireshark recorded high-frequency TCP SYN bursts to port 22 from `192.168.64.133` in real time during Hydra execution.
7. **SIEM detection** — Wazuh automatically generated 10 alerts under Rule ID 5760 (*sshd: authentication failed*) at Alert Level 5, with automatic MITRE ATT&CK mapping applied.
8. **Alert review** — The Wazuh dashboard and events view were reviewed to confirm alert count, rule metadata, and technique classification.
9. **Incident documentation** — Findings were compiled in `Incident_Report_SSH_BruteForce.docx`, covering attack timeline, indicators, and remediation recommendations.

---

## Findings

| Field | Value |
|---|---|
| Rule Triggered | 5760 — `sshd: authentication failed` |
| Alert Level | 5 |
| Total Alerts Fired | 10 |
| Successful Logins | 0 |
| MITRE ATT&CK Mapping | T1110 — Brute Force / T1110.001 — Password Guessing (SSH) |
| Attacker IP | `192.168.64.133` |
| Target IP | `192.168.64.130` |
| Username Targeted | `tren` |
| Wordlist Used | `~/passwords.txt` |

All 10 alerts were generated automatically without manual rule tuning. Wireshark independently corroborated the attack at the network layer via a visible burst of SYN packets to port 22 from a single source. No credentials were compromised across all attempts. Wazuh Rule ID 5763 (brute force threshold, higher severity) was not triggered during this lab, which is noted as a meaningful detection gap — per-failure alerting alone does not produce an automated block response.

---

## Security Significance

This lab confirms that **out-of-box Wazuh rule coverage detects SSH brute force campaigns** with zero custom configuration — Ubuntu log forwarding through alert generation worked end-to-end automatically. The dual-layer visibility (host-based SIEM + network packet capture) reflects how SOC and network teams would independently observe the same event through separate telemetry sources.

The intentional absence of compensating controls — no firewall restrictions, no fail2ban, no key-based authentication — mirrors a common real-world misconfiguration and allowed the full Hydra attack chain to proceed unimpeded. Remediation recommendations documented in the lab directly address each gap: deploying **fail2ban** for rate-limiting, enforcing **key-based SSH authentication**, disabling root SSH login via `/etc/ssh/sshd_config` (`PermitRootLogin no`), and enabling **Wazuh active response** to auto-block brute force source IPs on Rule ID 5763. The distinction between Rule 5760 (per-failure) and Rule 5763 (aggregate threshold) is highlighted as architecturally significant: detection without automated response leaves an attacker with a larger wordlist free to continue unimpeded.