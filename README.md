# Tren Patterson Cybersecurity Portfolio

Entry-level SOC and security analyst portfolio focused on blue-team investigation, log analysis, detection engineering, and clear incident documentation.

## About This Portfolio

I am building this repository as a practical cybersecurity portfolio for SOC analyst and security analyst roles. The projects here document hands-on work with alerts, logs, packet captures, detection logic, and investigation notes.

The goal is to show how I approach security work:

- Start with observable evidence.
- Review logs, alerts, screenshots, and commands.
- Separate suspicious behavior from benign or simulated lab activity.
- Document findings in a way another analyst could review.
- Keep public GitHub material clean, safe, and evidence-based.

This repo is not meant to be a dump of every local note or generated file. The public-facing work should show a clear blue-team career story: triage alerts, analyze authentication activity, investigate suspicious traffic, map behavior to MITRE ATT&CK, and write practical findings.

## Featured Projects

### SOC Alert Triage Lab

[blue-team-labs/soc-alert-triage-lab](blue-team-labs/soc-alert-triage-lab/)

A Wazuh-based SOC triage project that reviews an alert, checks event details, correlates related authentication activity, and documents a final analyst decision.

Highlights:

- Wazuh alert review
- Authentication and PAM event analysis
- MITRE ATT&CK context
- Public-safe evidence screenshots
- Analyst-style triage decision: Monitor / Informational

### Windows Failed Login Investigation

[blue-team-labs/windows-failed-login-investigation](blue-team-labs/windows-failed-login-investigation/)

A Windows Event Log investigation focused on Event ID 4625 failed logons. The project reviews failed authentication details, identifies the source and target account context, and explains why the activity was assessed as low risk in the lab environment.

Highlights:

- Windows Security log analysis
- Event ID 4625 review
- Failed logon interpretation
- Local versus remote activity assessment
- SOC-style risk explanation

### Suspicious Network Traffic Investigation

[security-plus-projects/suspicious-network-traffic-investigation](security-plus-projects/suspicious-network-traffic-investigation/)

A packet-analysis and reconnaissance detection project using Wireshark and Nmap in a controlled lab. The investigation identifies scanning behavior, validates service responses, and documents the traffic patterns that support the finding.

Highlights:

- Wireshark packet review
- Nmap scan behavior analysis
- TCP SYN, SYN/ACK, and RST/ACK interpretation
- Service identification
- MITRE ATT&CK T1046 mapping

## Review-Ready / In Progress

These projects are useful parts of the portfolio story, but still need final screenshot review, README polish, or GitHub readiness checks before being treated as fully polished public work.

- [Advanced Network Intrusion Detection Lab](blue-team-labs/advanced-network-intrusion-detection-lab/) - Suricata, SELKS, Zeek, RITA, Kibana, Evebox, and threat hunting workflow.
- [Phishing Investigation Workflow](blue-team-labs/phishing-investigation-workflow/) - phishing indicator review, IOC extraction, URL analysis, email-header reasoning, and MITRE ATT&CK mapping.
- [Detection Engineering with Wazuh](blue-team-labs/detection-engineering-wazuh/) - Wazuh authentication telemetry, false-positive analysis, and detection engineering lessons.
- [Malware Detection with YARA and Sigma](blue-team-labs/malware-detection-yara-sigma/) - YARA/Sigma practice that needs additional README and public-screenshot cleanup before featuring.

## Tools and Skills

This portfolio is organized around practical SOC and blue-team skills:

- SIEM and alert review: Wazuh, Kibana
- Windows logging: Windows Event Logs, Event ID 4625
- Network analysis: Wireshark, Nmap, TCP/IP traffic interpretation
- Network detection and hunting: Suricata, Zeek, RITA
- Detection logic: Sigma, YARA
- Framework mapping: MITRE ATT&CK
- Investigation workflow: alert triage, evidence review, timeline notes, findings, and incident documentation

## Repository Layout

- `blue-team-labs/` - main hands-on SOC, detection, and blue-team lab projects.
- `security-plus-projects/` - Security+ aligned investigations and structured practice projects.
- `labs/` - additional lab writeups and public-safe summaries.
- `tools/` - local helper tools for evidence validation, GitHub readiness review, project closeout, and portfolio indexing.
- `docs/ai-context/` - local Codex workflow guidance for safe portfolio work.

Some folders are still in progress or local-only. A project should not be treated as GitHub-ready just because a folder exists.

## Public GitHub Safety Boundary

This portfolio intentionally excludes local-only and private working material from public GitHub guidance.

Do not include:

- `.env` files, API keys, tokens, credentials, or secret-like files
- generated `outputs/` folders
- HANDOFF files and private workflow notes
- LinkedIn drafts or publishing queues
- OneNote notebooks and local journal files
- coursework submissions such as `.docx`, `.xlsx`, `.zip`, or final class packages
- job-tailor local profile data or application logs
- raw screenshots that have not passed privacy review

Public README files should only describe evidence that exists in the repo and has been reviewed for safe sharing. If evidence is missing, private, or not yet validated, the README should say that clearly instead of overstating the result.

## Portfolio Direction

The strongest direction for this repo is a focused entry-level SOC analyst portfolio:

1. Show a small number of polished investigations first.
2. Keep evidence and screenshots public-safe.
3. Use clear analyst language instead of hype.
4. Explain objectives, tools, investigation steps, findings, and lessons learned.
5. Keep unfinished labs marked as in progress until they pass README, evidence, screenshot, and safety review.
