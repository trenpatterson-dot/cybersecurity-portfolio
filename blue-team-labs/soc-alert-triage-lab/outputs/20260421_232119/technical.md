## Overview
The SOC Alert Triage Lab is a cybersecurity lab exercise designed to simulate and triage security incidents using the Wazuh Security Information and Event Management (SIEM) system. The lab includes an Ubuntu server running as a Wazuh manager and a Kali Linux machine acting as an attacker.

## Tools & Environment
The primary tool used in this lab is Wazuh, a open-source, lightweight SIEM solution for threat detection and response. The environment consists of two virtual machines: one running Ubuntu as the Wazuh manager and another running Kali Linux as the attacker machine.

## Steps Performed
1. Fixed Wazuh API connectivity issue
2. Verified Wazuh manager and dashboard functionality
3. Configured SSH on Ubuntu target
4. Fixed VM networking (host-only configuration)
5. Generated failed SSH login attempts from Kali Linux
6. Captured Wazuh alerts for authentication failures

## Findings
- 9 failed SSH login attempts were detected with the source IP `192.168.32.128` targeting the host `tren` (Ubuntu) and username `fakeuser`. No successful login was observed.
- Rule ID `2502` triggered (Severity 10), indicating a brute force attack according to MITRE ATT&CK T1110.

## Security Significance
The lab successfully demonstrated the ability to perform SOC-style alert triage using Wazuh SIEM in a simulated environment. The findings highlight the importance of monitoring and responding to repeated failed login attempts, as they can potentially indicate brute force attacks aimed at gaining unauthorized access to systems.