# Soc Alert Investigation End To End

## Overview
A comprehensive investigation into a potential security incident within a Ubuntu Linux Virtual Machine (VM) using the Wazuh platform for threat hunting and event analysis.

## Objective
The objective of this exercise was to investigate an alert related to privileged activity on the target system, specifically a successful sudo execution to root level.

## Tools Used
- Wireshark
- Wazuh

## Environment / Lab Setup
The lab environment consisted of a Ubuntu Linux VM hosting a browser-based Wazuh dashboard, which was accessed from a laptop browser for threat hunting and event analysis.

## Investigation Steps
1. Accessed the Wazuh dashboard hosted on the Ubuntu VM from my laptop browser.
2. Opened Threat Hunting and moved from the dashboard view into the Events view.
3. Reviewed available event data and tested filtering for medium-level alerts.
4. Determined there were no medium alerts currently available and pivoted to low-level event review.
5. Identified repeated privileged activity tied to sudo execution.
6. Expanded the event details to review the exact command, user, target account, terminal, and working directory.
7. Assessed whether the activity looked legitimate or potentially suspicious.
8. Investigated the alert: Successful sudo to ROOT executed.
9. Main finding: User `tren` used sudo to assign network capture capabilities to `dumpcap`.

## Key Findings
- User `tren` used sudo to assign network capture capabilities to `dumpcap`, potentially indicating an attempt to investigate or further analyze the system.

## Security Impact
The security impact of this finding is moderate, as it indicates that a user has elevated privileges and may have access to sensitive information or system components. However, without additional context or evidence, it's difficult to determine the full extent of potential damage or compromise.

## MITRE ATT&CK Mapping
- Technique: Privilege Escalation (T1078) - Command and Scripting Interpreter: Abuse Execution with sudo
