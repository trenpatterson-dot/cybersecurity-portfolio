# Phishing Investigation Workflow

## Overview

This project demonstrates a SOC-style phishing investigation workflow using a controlled phishing email sample.

The investigation focused on:
- phishing indicator identification
- suspicious domain analysis
- reply-to mismatch analysis
- IOC extraction
- phishing URL review
- MITRE ATT&CK mapping
- investigation documentation
- defensive analysis workflows

The goal was to simulate how a SOC analyst would review and document a suspicious phishing email in a production environment.

---

# Environment

## Investigation Environment
- Local analysis workstation
- VS Code documentation workflow

## Tools Used
- Markdown documentation
- IOC analysis workflow
- MITRE ATT&CK mapping
- Manual phishing analysis techniques

---

# Investigation Objectives

- Identify phishing indicators
- Extract suspicious indicators of compromise (IOCs)
- Analyze sender and reply-to inconsistencies
- Review suspicious phishing URLs
- Map findings to MITRE ATT&CK techniques
- Produce SOC-style investigation documentation

---

# Key Phishing Indicators Observed

## Typosquatting Domain
- micr0soft-verification.com

The domain used the number “0” instead of the letter “o” to imitate Microsoft branding.

---

## Reply-To Mismatch
Observed mismatch between:
- sender domain
- reply-to domain

This behavior is commonly associated with phishing and credential harvesting campaigns.

---

## Social Engineering Language
The phishing sample used:
- urgency
- password expiration warnings
- account suspension threats

to pressure users into interacting with the malicious verification link.

---

## Suspicious Verification URL
Observed phishing-themed URL:
hxxp://microsoft-login-verification-reset[.]example

The URL was safely defanged for documentation purposes.

---

# MITRE ATT&CK Mapping

## T1566.002 — Spearphishing Link
Initial Access

## T1036 — Masquerading
Defense Evasion

## T1583.001 — Acquire Infrastructure: Domains
Resource Development

---

# Investigation Findings

- Multiple phishing indicators were successfully identified
- The phishing sample demonstrated common credential harvesting behaviors
- MITRE ATT&CK mapping improved investigation context
- IOC extraction supported defensive analysis workflows
- Documentation quality significantly improved investigation clarity

---

# Evidence

## Screenshots
Located in:
```text
evidence/screenshots
```

## Documentation
Located in:
```text
docs
```

Included documentation:
- investigation notes
- findings
- IOC analysis
- email header analysis
- URL analysis
- MITRE ATT&CK mapping
- lessons learned

---

# Skills Demonstrated

- Phishing Investigation
- IOC Analysis
- Email Security Analysis
- Threat Investigation
- MITRE ATT&CK Mapping
- Social Engineering Analysis
- SOC Documentation Workflow
- Defensive Security Analysis

---

# Future Expansion

Future phases may include:
- VirusTotal enrichment
- URLScan analysis
- AlienVault OTX enrichment
- phishing header parsing
- automated IOC extraction
- SOAR phishing workflows
- email gateway detections