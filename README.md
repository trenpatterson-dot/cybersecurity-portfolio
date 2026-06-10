# Tren Patterson Cybersecurity Portfolio

**B.S. in Cybersecurity, Bellevue University, May 2026**

Blue-team portfolio focused on evidence-based alert triage, log analysis, threat hunting, detection engineering, and incident documentation.

**Target roles:** SOC Analyst | Security Analyst | Cybersecurity Operations Analyst

**Core tools:** Wazuh | Windows Event Logs | Wireshark | PowerShell | KQL | MITRE ATT&CK | Microsoft Defender and Sentinel concepts through simulated security operations cases

## Portfolio Highlights

* 10+ completed blue-team investigations
* Active Directory and IAM monitoring series
* Microsoft Sentinel, Defender EDR, and KQL investigations
* Network traffic analysis and threat hunting
* MITRE ATT&CK-aligned investigation documentation

## Featured Investigations

| Project | Investigation Focus | Tools and Evidence |
| --- | --- | --- |
| [SOC-011 Microsoft Sentinel Alert Triage](blue-team-labs/soc-011-microsoft-sentinel-alert-triage/) | Triaged simulated repeated failed sign-ins from one unfamiliar source and documented an evidence-based escalation decision. | Microsoft Sentinel concepts, KQL, authentication telemetry, MITRE ATT&CK |
| [SOC-012 Microsoft Defender EDR Alert Investigation](blue-team-labs/soc-012-microsoft-defender-edr-alert-investigation/) | Investigated a simulated Office-to-encoded-PowerShell process chain and documented an evidence-based escalation decision. | Microsoft Defender concepts, KQL, endpoint process telemetry, MITRE ATT&CK |
| [SOC-013 PowerShell Suspicious Script Investigation](blue-team-labs/soc-013-powershell-suspicious-script-investigation/) | Investigated simulated bypass-style PowerShell, attempted file-retrieval behavior, and related process activity. | PowerShell, KQL, endpoint events, MITRE ATT&CK |
| [SOC Alert Triage Lab](blue-team-labs/soc-alert-triage-lab/) | Reviewed Wazuh alert context, correlated authentication activity, and documented a Monitor / Informational disposition. | Wazuh, PAM, Linux logs, MITRE ATT&CK, public-safe screenshots |
| [Active Directory Security Monitoring Lab](active-directory-security-monitoring-lab/) | Investigated failed logons, account lockouts, user lifecycle events, and privileged group membership changes. | Windows Server, Active Directory, Windows Security Events |
| [Advanced Network Intrusion Detection and Threat Hunting](blue-team-labs/advanced-network-intrusion-detection-lab/) | Validated a custom IDS rule and investigated beaconing, suspicious DNS activity, and long-lived connections. | Suricata, SELKS, Zeek, RITA, Kibana, Wireshark |
| [Suspicious Network Traffic Investigation](security-plus-projects/suspicious-network-traffic-investigation/) | Identified TCP SYN scanning behavior and validated open and closed service responses. | Wireshark, Nmap, TCP/IP analysis, MITRE ATT&CK T1046 |

## Microsoft Security Operations Series

- [**SOC-011 - Microsoft Sentinel Alert Triage**](blue-team-labs/soc-011-microsoft-sentinel-alert-triage/)
- [**SOC-012 - Microsoft Defender EDR Alert Investigation**](blue-team-labs/soc-012-microsoft-defender-edr-alert-investigation/)
- [**SOC-013 - PowerShell Suspicious Script Investigation**](blue-team-labs/soc-013-powershell-suspicious-script-investigation/)

## Skills-to-Evidence Matrix

| Skill                             | Portfolio Evidence                                            |
| --------------------------------- | ------------------------------------------------------------- |
| Microsoft Sentinel concepts / KQL | SOC-011 Microsoft Sentinel Alert Triage                       |
| Microsoft Defender EDR concepts   | SOC-012 Microsoft Defender EDR Alert Investigation            |
| PowerShell investigation          | SOC-013 PowerShell Suspicious Script Investigation            |
| Wazuh SIEM alert triage           | SOC Alert Triage Lab                                          |
| Active Directory / IAM monitoring | Active Directory Security Monitoring Lab                      |
| Windows Event Logs                | Windows Failed Login Investigation                            |
| Wireshark / packet analysis       | Suspicious Network Traffic Investigation                      |
| Threat hunting                    | Advanced Network Intrusion Detection and Threat Hunting       |
| MITRE ATT&CK mapping              | SOC-011, SOC-012, SOC-013, and network investigation projects |

## Analyst Approach

The projects in this repository show how I approach security investigations:

- Start with observable evidence.
- Review logs, alerts, screenshots, and commands.
- Separate suspicious behavior from benign or simulated lab activity.
- Document findings in a way another analyst could review.
- Keep public GitHub material clean, safe, and evidence-based.

## About This Portfolio

This repository documents hands-on work with alerts, logs, packet captures, detection logic, and investigation notes for SOC and security analyst roles. The public-facing work is intended to show a clear blue-team career story: triage alerts, analyze authentication activity, investigate suspicious traffic, map behavior to MITRE ATT&CK, and write practical findings.

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
- `docs/` - supporting documentation and portfolio notes.

Some folders are still in progress or local-only. A project should not be treated as GitHub-ready just because a folder exists.

## Public Evidence Policy

All projects in this repository are reviewed before publication.

Private data, credentials, internal notes, generated outputs, unpublished drafts, and unreviewed evidence are intentionally excluded.

Public project documentation is limited to reviewed evidence, validated findings, and safe-to-share screenshots.

## Portfolio Direction

The strongest direction for this repo is a focused entry-level SOC analyst portfolio:

1. Show a small number of polished investigations first.
2. Keep evidence and screenshots public-safe.
3. Use clear analyst language instead of hype.
4. Explain objectives, tools, investigation steps, findings, and lessons learned.
5. Keep unfinished labs marked as in progress until they pass README, evidence, screenshot, and safety review.
