## Lab Recap
- **Lab Name:** Blue-Team Dashboard Analysis with Wazuh
- **Platform:** Wazuh
- **Lab Type:** Detection Engineering
- **Date Completed:** (use today's date if unknown) [Insert Today's Date]
- **Objective:** Analyze failed SSH authentication activity using Wazuh dashboard views.
- **Tools Used:** wazuh
- **What I Did:** I generated failed SSH login attempts, detected authentication failures in Wazuh, and used the dashboard view for analysis to review alert totals and authentication failures.
- **What I Found / Results:** 9 authentication failures were detected with no successful logins. The activity was concentrated in a short time window. [Insert Key Findings from handoff]
- **What Clicked / What I Learned:** Using visualization instead of raw logs for SOC-style triage can be efficient and effective.
- **Difficulty:** Medium
- **Screenshots:**
  1. [Dashboard Overview](screenshots/01-dashboard-overview.png)
  2. [Failed Logins Panel](screenshots/02-failed-logins-panel.png)
  3. [Auth Failure Panel](screenshots/03-auth-failure-panel.png)
- **Tags:** Wazuh, Detection Engineering, SSH Authentication, Brute Force, SOC Triage

## Study Notes
- Utilize Wazuh for detection engineering and analysis of failed authentication attempts.
- Familiarize yourself with Wazuh's dashboard views to quickly review alert totals and authentication failures.
- Understand the importance of triaging using visualization instead of raw logs in a SOC setting.
- Be aware that brute force attacks (MITRE T1110) can lead to multiple failed login attempts in a short time window.