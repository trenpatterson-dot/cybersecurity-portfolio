## Lab Recap
- **Lab Name:** SOC Alert Triage Lab
- **Platform:** Wazuh
- **Lab Type:** Cybersecurity lab
- **Date Completed:** 2022-03-15 (Today's date)
- **Objective:** Perform SOC-style alert triage using Wazuh SIEM to investigate simulated repeated failed SSH login attempts from an attacker machine to a Ubuntu Wazuh server.
- **Tools Used:** wazuh
- **What I Did:** Fixed Wazuh API connectivity issue, verified Wazuh manager and dashboard functionality, configured SSH on the Ubuntu target, and fixed VM networking (host-only configuration).
- **What I Found / Results:** 9 failed SSH login attempts detected from IP 192.168.32.128 to the target host 'tren' (Ubuntu), with username 'fakeuser'. No successful login was observed.
- **What Clicked / What I Learned:** Gained hands-on experience with Wazuh SIEM for alert triage and investigation. Understood the importance of network configuration and API connectivity in a SOC environment.
- **Difficulty:** Medium (Some initial setup challenges were encountered but were resolved)
- **Screenshots:** N/A (No screenshots provided in the task)
- **Tags:** Wazuh, SIEM, Alert Triage, Cybersecurity Lab, SOC

## Study Notes
- Understand the role of a SIEM (Security Information and Event Management) system in a Security Operations Center (SOC).
- Familiarize with Wazuh as a SIEM solution for alert triage and investigation.
- Learn how to configure SSH on Linux systems and investigate failed login attempts.
- Recall common network configurations like host-only networks, and their importance in SOC environments.
- Key findings: Simulated repeated failed SSH login attempts, Wazuh manager and dashboard functionality, environment setup (Wazuh manager and attacker machine).