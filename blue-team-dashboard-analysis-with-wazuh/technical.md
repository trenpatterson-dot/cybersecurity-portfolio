## Overview
The Blue-Team Dashboard Analysis with Wazuh is a detection engineering exercise that utilizes the Wazuh platform to analyze and visualize cybersecurity events. The lab focuses on detecting and analyzing failed SSH login attempts after a brute-force simulation, demonstrating SOC (Security Operations Center) style triage using visualization instead of raw logs first.

## Tools & Environment
The primary tool used in this lab is Wazuh, an open-source, lightweight Security Information and Event Management (SIEM) system. The environment consists of Ubuntu running Wazuh and Kali Linux acting as the attacker.

## Steps Performed
1. Generated failed SSH login attempts using a brute-force simulation on the target host (tren).
2. Detected authentication failures in Wazuh.
3. Utilized the Wazuh dashboard for analysis.
4. Reviewed alert totals and authentication failures.
5. Validated no successful login events.
6. Analyzed MITRE ATT&CK mapping (Brute Force).

## Findings
- 9 authentication failures detected.
- 0 successful logins.
- MITRE mapping: T1110 (Brute Force).
- Source activity concentrated in a short time window.
- Target host: tren.

## Security Significance
The findings from this lab demonstrate the effectiveness of using visualization tools like Wazuh for triaging and analyzing cybersecurity events, specifically failed SSH login attempts after a brute-force simulation. This exercise highlights the importance of monitoring and responding to such activities in a timely manner to prevent unauthorized access to systems.