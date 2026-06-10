# Tren Patterson Cybersecurity Portfolio

**B.S. in Cybersecurity, Bellevue University, May 2026**

Blue-team portfolio focused on evidence-based alert triage, log analysis, threat hunting, detection engineering, and incident documentation.

**Target roles:** SOC Analyst | Security Analyst | Cybersecurity Operations Analyst

**Core tools:** Wazuh | Windows Event Logs | Wireshark | PowerShell | KQL | MITRE ATT&CK | Microsoft Defender and Sentinel concepts through simulated security operations cases

## Featured Investigations

| Project | Investigation Focus | Tools and Evidence |
| --- | --- | --- |
| [SOC-012 Microsoft Defender EDR Alert Investigation](blue-team-labs/soc-012-microsoft-defender-edr-alert-investigation/) | Investigated a simulated Office-to-encoded-PowerShell process chain and documented an evidence-based escalation decision. | Microsoft Defender concepts, KQL, endpoint process telemetry, MITRE ATT&CK |
| [SOC-013 PowerShell Suspicious Script Investigation](blue-team-labs/soc-013-powershell-suspicious-script-investigation/) | Investigated simulated bypass-style PowerShell, attempted file-retrieval behavior, and related process activity. | PowerShell, KQL, endpoint events, MITRE ATT&CK |
| [SOC Alert Triage Lab](blue-team-labs/soc-alert-triage-lab/) | Reviewed Wazuh alert context, correlated authentication activity, and documented a Monitor / Informational disposition. | Wazuh, PAM, Linux logs, MITRE ATT&CK, public-safe screenshots |
| [Active Directory Security Monitoring Lab](active-directory-security-monitoring-lab/) | Investigated failed logons, account lockouts, user lifecycle events, and privileged group membership changes. | Windows Server, Active Directory, Windows Security Events |
| [Windows Failed Login Investigation](blue-team-labs/windows-failed-login-investigation/) | Analyzed Event ID 4625 details and assessed local versus remote authentication risk. | Windows Event Viewer, Event ID 4625, public-safe evidence |
| [Advanced Network Intrusion Detection and Threat Hunting](blue-team-labs/advanced-network-intrusion-detection-lab/) | Validated a custom IDS rule and investigated beaconing, suspicious DNS activity, and long-lived connections. | Suricata, SELKS, Zeek, RITA, Kibana, Wireshark |
| [Suspicious Network Traffic Investigation](security-plus-projects/suspicious-network-traffic-investigation/) | Identified TCP SYN scanning behavior and validated open and closed service responses. | Wireshark, Nmap, TCP/IP analysis, MITRE ATT&CK T1046 |
| [Threat Hunting: PowerShell and Linux Reconnaissance](threat-hunting-powershell/) | Reviewed authentication and privilege activity and documented a command-visibility gap. | Wazuh, Linux logs, PowerShell, threat hunting |

## Microsoft Security Operations Series

- **SOC-011 - Microsoft Sentinel Alert Triage:** Public-safe portfolio export pending.
- [**SOC-012 - Microsoft Defender EDR Alert Investigation**](blue-team-labs/soc-012-microsoft-defender-edr-alert-investigation/)
- [**SOC-013 - PowerShell Suspicious Script Investigation**](blue-team-labs/soc-013-powershell-suspicious-script-investigation/)

## Analyst Approach

The projects in this repository show how I approach security investigations:

- Start with observable evidence.
- Review logs, alerts, screenshots, and commands.
- Separate suspicious behavior from benign or simulated lab activity.
- Document findings in a way another analyst could review.
- Keep public GitHub material clean, safe, and evidence-based.

## About This Portfolio

This repository documents hands-on work with alerts, logs, packet captures, detection logic, and investigation notes for SOC and security analyst roles. The public-facing work is intended to show a clear blue-team career story: triage alerts, analyze authentication activity, investigate suspicious traffic, map behavior to MITRE ATT&CK, and write practical findings.

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
