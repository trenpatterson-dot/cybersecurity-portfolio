**Key Findings:**

| Finding | Description |
| --- | --- |
| Initial Access | Phishing email attachment clicked by one user at 1:47 PM, evidenced by email gateway logs. |
| Ransomware Impact | Three accounting workstations and file server FS01 encrypted with ransom notes present. |
| Lateral Movement | Ransomware spread to FS01 via accessible SMB shares. |
| Detection Lag | Help desk received three calls within 10 minutes after initial click, indicating detection lag of 27 minutes. |
| Data Loss Window | Last backup was Monday at 11 PM, creating a data loss window of up to 15 hours. |

**Steps Performed:**

| Step | Description |
| --- | --- |
| Preparation Phase | Identified strengths (daily backups, email gateway logging) and gaps (no EDR, no phishing filtering, poor segmentation, weak user training, untested IR plan). |
| Detection Phase | Correlated help desk calls with email gateway log evidence of phishing attachment click at 1:47 PM. |
| Containment Phase | Isolated affected workstations and FS01 from network, blocked phishing sender/indicators, preserved logs and evidence, flagged fourth VLAN workstation as potentially exposed pending validation. |
| Eradication Phase | Removed malware and all persistence mechanisms, reset compromised credentials, patched initial access vector. |
| Recovery Phase | Verified eradication before any restore, restored FS01 from Monday 11 PM backup, rebuilt or restored affected workstations, validated restored files and systems, monitored closely for reinfection, phased systems back into production. |

Please note that this summary is based on the provided JSON data and might not be an exhaustive list of all key findings and steps performed during the Incident Response Tabletop - NIST SP 800-61 Ransomware Scenario.