**Key Findings:**

1. **Initial Access**: Phishing email attachment clicked by one user at 1:47 PM, evidenced by email gateway logs.
2. **Ransomware Attack**: Three accounting workstations and file server FS01 encrypted with ransom notes present.
3. **Lateral Movement**: Ransomware spread to FS01 via accessible SMB shares.
4. **Detection Lag**: Help desk received three calls within 10 minutes beginning at 2:14 PM, indicating detection lag of 27 minutes.
5. **Data Loss Window**: Last backup was Monday at 11 PM, creating a data loss window of up to 15 hours.

**Steps Performed:**

1. **Preparation Phase**: Identified strengths (daily backups, email gateway logging) and gaps (no EDR, no phishing filtering, poor segmentation, weak user training, untested IR plan).
2. **Detection Phase**: Correlated help desk calls with email gateway log evidence of phishing attachment click at 1:47 PM.
3. **Containment Phase**: Isolated affected workstations and FS01 from network, blocked phishing sender/indicators, preserved logs and evidence, flagged fourth VLAN workstation as potentially exposed pending validation.
4. **Eradication Phase**: Removed malware and all persistence mechanisms, reset compromised credentials, patched initial access vector.
5. **Recovery Phase**: Verified eradication before any restore, restored FS01 from Monday 11 PM backup, rebuilt or restored affected workstations, validated restored files and systems, monitored closely for reinfection, phased systems back into production.

**Gaps in Incident Response:**

1. No EDR deployed on endpoints.
2. No phishing prevention or strong email filtering in place.
3. Poor VLAN segmentation allowed FS01 to be reachable via standard user shares.
4. IR plan was not regularly tested.

Overall, the Incident Response Tabletop - NIST SP 800-61 Ransomware Scenario highlights the importance of implementing EDR solutions on endpoints, enforcing strong email filtering and phishing prevention measures, regularly testing incident response plans, and maintaining a robust backup and recovery process to minimize data loss windows.