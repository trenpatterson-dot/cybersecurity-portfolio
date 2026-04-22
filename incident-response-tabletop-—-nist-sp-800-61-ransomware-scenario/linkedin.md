**Incident Response Tabletop - NIST SP 800-61 Ransomware Scenario**

The Incident Response Tabletop - NIST SP 800-61 Ransomware Scenario is a comprehensive documentation-based tabletop exercise that applies the full NIST SP 800-61 Rev 2 incident response lifecycle to a ransomware scenario. The lab involves three accounting workstations and a file server at Acme Corp, which are affected by ransomware.

**Key Findings:**

* **Initial Access**: Phishing email attachment clicked by one user at 1:47 PM, evidenced by email gateway logs.
* **Ransomware Attack**: Ransomware encrypted three accounting workstations and file server FS01; files renamed with .locked extension and ransom notes were present.
* **Lateral Movement**: Ransomware spread to FS01 via accessible SMB shares.
* **Detection Lag**: Help desk received three calls within 10 minutes beginning at 2:14 PM, indicating detection lag of 27 minutes; no automated alerting fired - detection was entirely user-reported, indicating absence of EDR or SIEM-based detection capability.
* **Data Loss Window**: Last backup was Monday at 11 PM, creating a data loss window of up to 15 hours.

**Gaps in Incident Response:**

* No EDR deployed on endpoints.
* No phishing prevention or strong email filtering in place.
* Poor VLAN segmentation allowed FS01 to be reachable via standard user shares.
* IR plan was not regularly tested.

**Recommendations:**

1. Implement EDR solutions on endpoints.
2. Enforce strong email filtering and phishing prevention measures.
3. Regularly test incident response plans.
4. Maintain a robust backup and recovery process to minimize data loss windows.

Overall, the Incident Response Tabletop - NIST SP 800-61 Ransomware Scenario serves as a valuable resource for understanding the incident response lifecycle and identifying areas for improvement in incident response planning and execution.