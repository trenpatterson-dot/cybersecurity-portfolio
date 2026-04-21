**Incident Summary**

A ransomware attack occurred at Acme Corp, affecting three accounting workstations and a file server. The incident was classified as Critical due to the potential for significant data loss and disruption to business operations.

**Attack Timeline**

* 1:47 PM: Phishing email attachment clicked by an employee, resulting in initial access.
* 1:47 PM - 2:14 PM: Malware executes and encrypts local files on three workstations.
* 2:14 PM: Help desk receives three calls within 10 minutes, indicating detection of the incident.

**Containment Actions**

* Isolate affected workstations and file server from the network.
* Block phishing sender/indicators to prevent further attacks.
* Preserve logs and evidence for analysis.

**Eradication Actions**

* Perform full log review across endpoint, email, server, and network layers.
* Remove malware and all persistence mechanisms.
* Reset compromised credentials.
* Patch initial access vector.

**Recovery Actions**

* Verify eradication before any restore.
* Restore file server from Monday 11 PM backup.
* Rebuild or restore affected workstations.
* Validate restored files and systems.
* Monitor closely for reinfection.
* Phase systems back into production.

**Lessons Learned**

* Initial access confirmed via phishing email attachment clicked by an employee.
* Ransomware encrypted three accounting workstations and file server FS01.
* Lateral movement from workstations to FS01 occurred via accessible SMB shares.
* Help desk received three calls within 10 minutes, indicating detection lag of 27 minutes.
* Last backup was Monday at 11 PM, creating a data loss window of up to 15 hours.
* No EDR deployed on endpoints.
* No phishing prevention or strong email filtering in place.
* Poor VLAN segmentation allowed FS01 to be reachable via standard user shares.
* IR plan was not regularly tested.

**Recommendations**

* Implement EDR on all endpoints.
* Deploy phishing prevention and strong email filtering solutions.
* Regularly test the IR plan.
* Improve VLAN segmentation to prevent lateral movement.
* Consider implementing a backup rotation policy to minimize data loss windows.