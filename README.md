# Tren Patterson — Cybersecurity Portfolio (SOC / Blue Team)

Hands-on cybersecurity portfolio focused on **SOC analysis, threat detection, and incident investigation**.

This repository contains real lab work, detection exercises, and investigations using tools like **Wazuh, Wireshark, Nmap, and SIEM-style workflows**, supported by structured documentation and evidence.

---

## 🔍 What I Do

- Investigate suspicious network activity
- Analyze logs and alerts for potential threats
- Detect brute force and reconnaissance behavior
- Correlate network traffic with host-based evidence
- Document findings in a structured, analyst-ready format

---

## 🧰 Tools & Technologies

- **SIEM / Detection:** Wazuh, Splunk (labs)
- **Network Analysis:** Wireshark, tcpdump
- **Scanning & Recon:** Nmap
- **Systems:** Linux, Windows
- **Other:** Git, GitHub, Python (automation), Virtualization (VMware)

---

## 🚨 Featured Projects

### 🔹 SOC Alert Triage — Failed Login Investigation
- Investigated repeated failed SSH login attempts
- Identified brute force behavior using Wazuh alerts
- Correlated log data with attacker activity patterns  
📁 `security-plus-projects/soc-alert-triage-failed-login`

---

### 🔹 Suspicious Network Traffic Investigation
- Captured and analyzed network traffic using Wireshark
- Identified SYN scan behavior from attacker host
- Confirmed open ports and reconnaissance activity  
📁 `security-plus-projects/suspicious-network-traffic-investigation`

---

### 🔹 Wazuh Threat Hunting Lab
- Performed threat hunting using Wazuh dashboards and queries
- Detected brute force activity mapped to MITRE ATT&CK
- Built queries and validated detection logic  
📁 `threat-hunting/wazuh-threat-hunting`

---

## 📂 Repository Structure

```text
security-plus-projects/   → SOC-focused investigation projects
blue-team-labs/           → detection labs and analysis exercises
threat-hunting/           → Wazuh and threat-hunting workflows
tryhackme/                → platform-based skill labs
tools/                    → automation agents and dashboards
journal/                  → coursework and learning progression
