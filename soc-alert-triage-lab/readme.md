# SOC Alert Triage Lab

## Overview
This is a cybersecurity lab exercise documenting a Simulated Security Operations Center (SOC) Alert Triage using the Wazuh platform. The goal was to perform SOC-style alert triage and respond to a series of simulated repeated failed SSH login attempts from an attacker machine (Kali Linux) to a Ubuntu Wazuh server.

## Objectives
The main objective of this lab was to demonstrate the ability to utilize Wazuh as a Security Information and Event Management (SIEM) system for alert triage, incident response, and threat hunting.

## Tools Used
- Wazuh

## Steps Performed
1. Fixed Wazuh API connectivity issue
2. Verified Wazuh manager and dashboard functionality
3. Configured SSH on Ubuntu target
4. Fixed VM networking (host-only configuration)

## Key Findings
- 9 failed SSH login attempts detected
- Source IP: 192.168.32.128
- Target Host: tren (Ubuntu)
- Username attempted: fakeuser
- No successful login observed
- Rule ID: 2502 tri...

## Lessons Learned
This lab provided valuable insights into the capabilities of Wazuh as a SIEM system for alert triage and incident response. It also highlighted the importance of proper configuration and network setup to ensure effective monitoring and threat detection.
