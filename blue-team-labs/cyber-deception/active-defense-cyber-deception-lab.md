# Active Defense & Cyber Deception Lab

> **Course:** CYBR445 — Advanced Incident Detection and Response
> **Author:** Tren Patterson | Bellevue University
> **Tools Used:** Canary Tokens, Portspoof, Cowrie SSH Honeypot, Spidertrap

---

## Overview

This lab explores free active defense and cyber deception tools that help defenders transition from a passive to an active security mindset. The tools covered — provided by [Thinkst Canary](https://canarytokens.org) and [Active Countermeasures / Black Hills Information Security](https://www.activecountermeasures.com/) — are used to detect, attribute, and frustrate attackers. These countermeasures can significantly slow or dissuade red teams, penetration testers, and real-world attackers.

**Three core categories of active defense techniques:**
| Technique | Description |
|-----------|-------------|
| **Annoyance** | Slows down attackers by returning false or confusing information |
| **Attribution** | Identifies and gathers intelligence on attackers |
| **Attack** | Actively disrupts attacker operations |

---

## Part 1 — Canary Tokens

### What Are Canary Tokens?

Canary tokens are a type of honeypot that alerts defenders when an attacker interacts with a seemingly benign resource (e.g., opening a Word document). They act as invisible tripwires — authorized users won't trigger them in normal activity, but attackers performing reconnaissance or data theft will.

### Lab Exercise

A **Microsoft Word canary token** was created via [canarytokens.org](https://canarytokens.org/generate) and opened to simulate an attacker accessing a sensitive document.

**Alert triggered — information captured:**
- Source IP address
- Geolocation of the request
- Timestamp
- User agent string

> There are **32 different types** of canary tokens available, covering file types, URLs, DNS, AWS keys, and more.

### Analysis

**Q: Are you surprised by the amount of information available?**
Yes — the amount of detail captured is significant. A single document open event reveals the attacker's IP address, approximate location, timestamp, and browser/OS details. This demonstrates how effectively cyber deception tools can expose unauthorized access even when an attacker has bypassed other defenses.

**Q: Where could Word canary tokens be deployed?**
- Shared network drives
- Email attachments sent to suspicious parties
- Cloud storage (OneDrive, Google Drive)
- Sensitive document repositories (HR, finance, credentials folders)

**Q: How do you make a canary token more enticing?**
Rename the file to appear high-value: `Confidential Financial Report.docx`, `Employee Salary Data Q4.xlsx`, or `Network Admin Credentials.docx`. An attacker who breaks into a network and sees these files is highly likely to open them — triggering the alert.

**Classification: Attribution** — provides IP, geolocation, and timestamp intelligence on the attacker.

---

## Part 2 — Portspoof

### What Is Portspoof?

Portspoof is an active defense tool from the [ADHD (Active Defense Harbinger Distribution)](https://adhdproject.github.io) project. It intercepts port scans and returns fake, confusing service banners — wasting the attacker's time and making it impossible to accurately map open services.

### Lab Exercise

1. Ran a baseline `nmap -p 1-30` scan against the ADHD system — returned accurate, minimal results
2. Enabled Portspoof via iptables redirect rule:
   ```bash
   sudo iptables -t nat -A PREROUTING -p tcp -m tcp --dport 1:30 -j REDIRECT --to-ports 4444
   sudo portspoof -s /usr/local/etc/portspoof_signatures
   ```
3. Re-ran `nmap -p 1-30 -sV` — results returned dozens of fake, nonsensical services with conflicting version data

**Result:** The version scan returned completely false service information, making reconnaissance unreliable and time-consuming for the attacker.

### Analysis

**Classification: Annoyance** — intentionally provides misleading reconnaissance data to slow down port scanning and network mapping. Forces attackers to spend significant time validating results that are entirely fabricated.

---

## Part 3 — Cowrie SSH Honeypot

### What Is Cowrie?

[Cowrie](https://github.com/cowrie/cowrie) is a medium-to-high interaction SSH honeypot that simulates a real SSH service. It accepts connections, logs all commands entered by attackers, and records credential attempts — all while operating in a sandboxed environment where no real system access is granted.

### Lab Exercise

1. Started Cowrie on the ADHD system:
   ```bash
   cd /opt/cowrie
   sudo ./bin/cowrie start
   ```
2. Connected to the honeypot as an attacker would:
   ```bash
   ssh -o HostKeyAlgorithms=+ssh-rsa root@localhost -p 2222
   # Entered any password — Cowrie accepted it
   ```
3. Ran commands inside the honeypot: `ls`, `pwd`, `whoami`
4. Reviewed the Cowrie log to see the captured session:
   ```bash
   more /opt/cowrie/var/log/cowrie/cowrie.log
   ```

**Captured in logs:**
- Login attempt with credentials
- All commands typed by the simulated attacker
- Session duration and timing

### Analysis

**Classification: Attribution** — records attacker behavior in detail including login credentials attempted, commands executed, and session timing. This intelligence can be used for threat hunting and understanding attacker TTPs.

---

## Part 4 — Spidertrap

### What Is Spidertrap?

Spidertrap is an HTTP tarpit designed to confuse web spiders and vulnerability scanners. It responds to every request with a valid `200 OK` and a link to another fake page — trapping automated scanners in an infinite loop of fake content.

### Lab Exercise

1. Started Spidertrap:
   ```bash
   cd /opt/spidertrap
   python3 spidertrap.py
   ```
2. Ran a Nikto web scan against it from a second terminal:
   ```bash
   nikto -host http://127.0.0.1:8000
   ```
3. Observed the Spidertrap log — every requested path returned `200 OK`, generating thousands of fake valid URLs for the scanner to chase

**Result:** The Nikto scan was flooded with false positives, unable to distinguish real content from generated noise.

### Analysis

**Classification: Attribution** — logs all web-based reconnaissance activity including requested URLs and scanning patterns. Helps defenders identify active scanning behavior and gather intelligence on attacker tooling.

---

## Summary: Tool Classification

| Tool | Primary Technique | Key Capability |
|------|------------------|----------------|
| **Canary Tokens** | Attribution | Detects access, reveals attacker IP and location |
| **Portspoof** | Annoyance | Returns false port/service data to waste attacker time |
| **Cowrie** | Attribution | Logs full SSH session including credentials and commands |
| **Spidertrap** | Attribution | Traps web scanners in infinite fake content loops |

---

## Key Takeaways

Active defense and cyber deception tools provide a significant advantage to defenders by:

1. **Detecting threats that bypass perimeter defenses** — canary tokens and honeypots catch attackers who have already gotten in
2. **Generating attacker intelligence** — logs from Cowrie and Spidertrap reveal TTP patterns
3. **Wasting attacker resources** — Portspoof and Spidertrap force attackers to spend time on false data
4. **Requiring zero ongoing maintenance** — once deployed, these tools operate passively until triggered

These tools complement traditional security controls (firewalls, IDS/IPS, SIEM) and shift the cost asymmetry of cyber defense — making it significantly more expensive for attackers to operate undetected.

---

## References

- Thinkst Applied Research. *Canarytokens*. https://canarytokens.org
- Active Countermeasures. *ADHD Project*. https://adhdproject.github.io
- Cowrie Project. *Cowrie SSH/Telnet Honeypot*. https://github.com/cowrie/cowrie
