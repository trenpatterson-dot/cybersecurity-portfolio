# Cyber Deception & Active Defense

> Part of my cybersecurity portfolio — Bellevue University CYBR445 & CYBR440

This section documents my study and hands-on practice of **cyber deception** as a defensive strategy. The work here covers the full arc from understanding who we're defending against, to deploying the tools used to catch them, to proposing a formal platform built around those techniques.

---

## Contents

### 1. [APT29 Threat Intelligence Report](./apt29-threat-intelligence-report.md)
A deep-dive into **APT29 (Cozy Bear / Nobelium)** — a Russian state-sponsored threat actor responsible for the SolarWinds supply chain attack and numerous government espionage campaigns. Covers their TTPs mapped to MITRE ATT&CK, targeted industries, malware arsenal, and recommended defensive countermeasures.

**Key topics:** Nation-state TTPs · MITRE ATT&CK · Supply chain compromise · C2 infrastructure · Threat-informed defense

---

### 2. [Active Defense & Cyber Deception Lab](./active-defense-cyber-deception-lab.md)
Hands-on lab using four open-source deception tools from the **Active Defense Harbinger Distribution (ADHD)** project. Each tool was deployed, tested, and analyzed in a lab environment simulating real attacker behavior.

| Tool | Technique | What It Does |
|------|-----------|--------------|
| Canary Tokens | Attribution | Alerts on document access with IP/geo data |
| Portspoof | Annoyance | Returns fake service banners to confuse port scans |
| Cowrie | Attribution | SSH honeypot that logs attacker commands |
| Spidertrap | Attribution | HTTP tarpit that traps web scanners in fake content |

**Key topics:** Honeypots · Active defense · Threat attribution · Canary tokens · Network deception

---

### 3. [CyberTrap Platform Proposal](./cybertrap-deception-platform-proposal.md)
A formal proposal recommending **CyberTrap** as an organizational cyber deception platform. Addresses the limitations of traditional reactive defenses and outlines a phased implementation plan with SIEM integration.

**Key topics:** Security architecture · Deception platforms · SIEM integration · SOC workflows · Proactive defense

---

## The Narrative

These three pieces tell a connected story:

```
Understand the threat (APT29)
        ↓
Build hands-on skills with the tools designed to catch them
        ↓
Propose a platform that formalizes those techniques at scale
```

Cyber deception flips the asymmetry of defense — instead of chasing every alert, defenders place tripwires that only fire when something is genuinely wrong. The result is fewer false positives, richer attacker intelligence, and faster incident response.

---

## Tools & Technologies

- [Canarytokens.org](https://canarytokens.org) — free canary token generation
- [ADHD Project](https://adhdproject.github.io) — Active Defense Harbinger Distribution
- [Cowrie](https://github.com/cowrie/cowrie) — SSH/Telnet honeypot
- [MITRE ATT&CK](https://attack.mitre.org/groups/G0138/) — threat intelligence framework
- Wazuh · Splunk · Nmap · Nikto

---

*For more of my work, see the [portfolio root](../../README.md).*
