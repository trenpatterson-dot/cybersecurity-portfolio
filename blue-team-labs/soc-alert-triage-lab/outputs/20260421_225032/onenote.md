## Lab Recap

- **Lab Name:** SOC Alert Triage Lab
- **Platform:** Wazuh
- **Lab Type:** Cybersecurity lab
- **Date Completed:** 2023-05-15 (Today's date)
- **Objective:** Perform SOC-style alert triage using Wazuh SIEM to investigate simulated repeated failed SSH login attempts.
- **Tools Used:** wazuh
- **What I Did:** Fixed Wazuh API connectivity issue, verified Wazuh manager and dashboard functionality, configured SSH on Ubuntu target, fixed VM networking (host-only configuration).
- **What I Found / Results:** 9 failed SSH login attempts detected from IP 192.168.32.128 to the Ubuntu server with username 'fakeuser'. No successful login observed.
- **What Clicked / What I Learned:** Understanding the importance of alert triage in a SOC environment and the role of tools like Wazuh in detecting and investigating security incidents.
- **Difficulty:** Medium (Some configuration issues required troubleshooting)
- **Screenshots:** [No screenshots provided]
- **Tags:** SOC, Alert Triage, Wazuh, SIEM, Cybersecurity Lab

## Study Notes

*SOC Alert Triage:* Process of investigating security alerts in a Security Operations Center (SOC).

*Wazuh:* Open-source, lightweight SIEM solution for threat detection and alerting.

*Alert Triaging Steps:* 1. Verify the alert source, 2. Determine the significance of the alert, 3. Investigate the alert, 4. Classify and respond to the alert.

*Wazuh Tools:* Wazuh manager (central server), Wazuh agent (on target systems), Wazuh dashboard (web interface for monitoring alerts).

*Common Alert Types:* Failed login attempts, network traffic anomalies, system changes, etc.

*Importance of SOC Alert Triage:* Early detection and response to security incidents can minimize damage and prevent future attacks.