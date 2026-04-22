# Blue-Team Dashboard Analysis with Wazuh

## Overview
This project is a detection engineering exercise that demonstrates the use of Wazuh for analyzing failed SSH authentication activity after a brute-force simulation. The focus is on SOC-style triage using visualization instead of raw logs first, and the environment used was Ubuntu (Wazuh) and Kali Linux (attacker).

## Objectives
1. Analyze failed SSH authentication activity after a brute-force simulation using Wazuh dashboard views.
2. Demonstrate SOC-style triage using visualization instead of raw logs first.
3. Document the environment used: Ubuntu (Wazuh) and Kali Linux (attacker).

## Tools Used
1. wazuh

## Steps Performed
1. Generated failed SSH login attempts.
2. Detected authentication failures in Wazuh.
3. Utilized dashboard view for analysis.
4. Reviewed alert totals and authentication failures.

## Key Findings
- 9 authentication failures detected.
- 0 successful logins.
- MITRE mapping: T1110 (Brute Force).
- Source activity concentrated in a short time window.
- Target host: tren.

## Screenshots
- [Dashboard Overview](screenshots/01-dashboard-overview.png)
- [Failed Logins Panel](screenshots/02-failed-logins-panel.png)
- [Auth Failure Panel](screenshots/03-auth-failure-panel.png)
- [Mitre Brute-Force Panel](screenshots/04-mitre-brute-force-panel.png)
- [Alert Evolution Panel](screenshots/05-alert-evolution-panel.png)
- [Top Agent Panel](screenshots/06-top-agent-panel.png)

## Lessons Learned
This exercise reinforced the importance of utilizing visualization tools for efficient and effective triage in a SOC environment. The use of Wazuh dashboard views proved to be a valuable asset in quickly identifying and analyzing security events, ultimately leading to more informed decision-making and response strategies.