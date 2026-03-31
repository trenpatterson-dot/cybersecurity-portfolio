# Cybersecurity Journal – Lab 2: Active Defense & Cyber Deception

**Date:** March 2026
**Course:** CYBR 445 – Advanced Incident Detection and Response
**Lab:** Module 2 – Active Defense and Cyber Deception
**Focus Area:** Honeypots, Deception Technologies, Attacker Attribution

---

## Objective

The goal of this lab was to gain hands-on experience with active defense and cyber deception tools used in real-world SOC and blue team environments. The lab covered four tools — Canary Tokens, Portspoof, Cowrie, and Spidertrap — each representing a different approach to detecting, slowing down, or attributing attacker activity.

---

## Tools Used

- **Canarytokens.org** – Web-based token generation platform
- **Portspoof** – Port deception and service spoofing tool
- **Cowrie** – SSH honeypot for capturing attacker interaction
- **Spidertrap** – Web-based deception tool for logging reconnaissance
- **Nmap** – Network scanner (used to test Portspoof)
- **Nikto** – Web vulnerability scanner (used to trigger Spidertrap)
- **ADHD Distribution** – Lab environment hosting the defense tools

---

## Key Activities Performed

### Part 1 – Canary Tokens
- Visited Canarytokens.org and reviewed all 32 available token types
- Selected and documented two token types (DNS and URL) with explanations of how each traps attackers
- Created a Microsoft Word canary token with a custom reminder note
- Triggered the token by opening the file and received an email alert
- Reviewed the alert history page which showed IP address, geolocation, timestamp, and user-agent data
- Answered reflection questions about token placement and effectiveness

### Part 2 – Portspoof
- Set up iptables rules to redirect ports 1–30 to Portspoof
- Started Portspoof using a custom signatures file
- Ran an Nmap service version scan (-sV) against the target while Portspoof was active
- Observed that Nmap returned misleading, inconsistent, and fake service names and versions
- Cleaned up iptables rules and stopped Portspoof after capturing results

### Part 3 – Cowrie SSH Honeypot
- Located and started Cowrie in /opt/cowrie
- Connected to the honeypot from a Kali terminal using SSH on port 2222
- Logged in with any password (honeypot accepted all credentials)
- Ran commands including ls, whoami, and pwd inside the fake shell
- Reviewed cowrie.json logs confirming the session was captured with login event, session ID, and commands

### Part 4 – Spidertrap
- Started Spidertrap on port 8000 from the ADHD system
- Ran a Nikto scan against the Spidertrap server from the same machine (localhost:8000)
- Observed Spidertrap responding with 200 OK to every request, logging all paths and requests
- Captured terminal output showing reconnaissance activity being recorded

---

## Key Findings

- **Canary tokens** revealed a surprising amount of attacker information from a single file open — IP, location, browser, and time
- **Portspoof** successfully confused Nmap, returning fake services like `finger`, `compressnet`, `pop3-proxy`, and unrecognized fingerprint data
- **Cowrie** accepted any password and fully logged the session — demonstrating how honeypots can lure and study attackers
- **Spidertrap** returned valid responses to every URL path Nikto tried, making the attacker's scanner believe everything was valid

---

## Active Defense Categories

| Tool | Category | Why |
|------|----------|-----|
| Canary Tokens | Attribution | Identifies attacker via IP, location, and timing |
| Portspoof | Annoyance | Slows and confuses reconnaissance |
| Cowrie | Attribution | Logs attacker commands and behavior |
| Spidertrap | Attribution | Records web scanning and request patterns |

---

## Challenges & Lessons Learned

- **Terminal confusion** – Learned the difference between running commands on Kali (attacker machine) vs. ADHD (defender machine). Commands like `iptables` must run on the system where the rule was set.
- **Port targeting** – Cowrie runs on port 2222, not port 22. Targeting the wrong port caused repeated "connection refused" errors until the correct port was identified.
- **localhost vs. IP** – Nikto must be run from the same machine as Spidertrap when targeting `127.0.0.1`. Running it from Kali against `localhost` pointed to Kali itself, not the ADHD server.
- **File viewer exits** – Learned to exit `less` and `cat` viewers using `q` or `Ctrl+C` to regain terminal control.

---

## Skills Gained

- Deploying and interacting with honeypots (Cowrie)
- Configuring iptables rules for port redirection
- Using Nmap and Nikto for network and web reconnaissance
- Reading and interpreting honeypot log files (cowrie.json)
- Understanding the difference between annoyance, attribution, and attack as defensive strategies
- Troubleshooting multi-machine lab environments with separate attacker and defender roles

---

## Reflection

This lab was one of the most practical so far. Working with real deception tools showed me how defenders can flip the script on attackers — instead of just blocking them, you can study them, slow them down, and gather intelligence. The most powerful concept was that honeypots and canary tokens provide visibility *after* an attacker has already gotten past other defenses. In a real SOC environment, these tools would be part of a layered defense strategy where the goal is not just prevention but also detection and response.

The troubleshooting throughout the lab — fixing command typos, identifying the right IP and port, understanding which terminal to use — was genuinely valuable. These are the same kinds of mistakes that happen in real environments, and working through them built real problem-solving skills.

---

## What's Next

- Continue building hands-on labs and documenting them in this portfolio
- Explore more blue team tools (SIEM, threat hunting, forensics)
- Apply deception concepts to future incident response scenarios
