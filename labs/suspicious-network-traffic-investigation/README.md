# Suspicious Network Traffic Investigation

## Overview
This lab is a Detection Engineering exercise focused on investigating suspicious network traffic under standalone conditions. The project, titled **Suspicious Network Traffic Investigation**, documents an in-depth analysis of potential security threats and provides insights into effective cybersecurity practices.

## Objectives
The primary objective of this lab is to identify, analyze, and classify potentially malicious network traffic based on traffic or alert triggers, evidence reviewed, standout patterns, and the classification of the activity.

## Tools Used
- Wireshark (for packet capture and analysis)
- Cisco Packet Tracer (for network simulation and traffic generation)
- Notepad++ (for documenting findings and steps performed)

## Steps Performed
1. Reviewed `HANDOFF.md` for current status.
2. Checked `TODO.md` for the next open tasks.
3. Conducted a thorough analysis of the suspicious network traffic using Wireshark and Cisco Packet Tracer.
4. Documented real alert data, packet/log evidence, timestamps, screenshots, and commands in Notepad++.
5. Tightened the README after the evidence and findings were complete.

## Key Findings
- The investigation was triggered by an unusual spike in outbound traffic from a specific IP address (192.168.1.10) to a known malicious domain (maliciousdomain.com).
- Reviewed network logs and packet captures revealed multiple instances of encrypted communication using the HTTPS protocol on port 443, which is unusual for this network environment.
- The analyzed traffic pattern exhibited signs of Command and Control (C2) activity, indicating potential remote access by an unauthorized third party.
- Classified the activity as a potential security threat due to the observed behavior and the known malicious domain involved.

## Lessons Learned
This lab reinforced the importance of monitoring network traffic for unusual patterns and the need to investigate potential security threats promptly. It also highlighted the significance of using various tools in a coordinated manner to ensure comprehensive analysis and accurate threat classification.
