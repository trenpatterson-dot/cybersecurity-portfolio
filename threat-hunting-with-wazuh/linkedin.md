Wazuh Rule 5763 fired in under 10 seconds. That was the confirmation I needed.

Built a full Wazuh SIEM lab from scratch in VMware — Wazuh Manager, Indexer, and Dashboard on Ubuntu, with agents enrolled on both an Ubuntu 24.04 endpoint and a Windows 11 machine. Then attacked my own environment from Kali Linux to see what the platform would catch.

Two detections ran. First, I escalated to root and read /etc/shadow on the monitored Ubuntu endpoint. Wazuh flagged the file access — maps to MITRE T1003.008 (OS Credential Dumping). Second, I generated 10 consecutive failed su authentication attempts with a bash loop. Rule 5763 triggered within seconds. Timestamp correlation between the attacker terminal and the SIEM alert confirmed sub-10-second detection latency.

The deployment wasn't clean. Agent enrollment was silently blocked because port 1515 wasn't open — no dashboard error, no indication the endpoint wasn't being monitored. A misconfigured ossec.conf had the same effect: agents appeared enrolled but forwarded nothing. API connectivity failed entirely due to credential desync between the Dashboard and the Wazuh API service, fixed by resetting credentials through Wazuh's password tooling.

Those failure modes matter more than the detections. A SIEM with blind spots looks healthy until it isn't. Knowing how they happen is half of defending against them.

Full writeup and screenshots in my portfolio.

#Wazuh #ThreatHunting #SIEM #BlueTeam #MITREATTACK