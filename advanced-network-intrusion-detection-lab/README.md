# Advanced Network Intrusion Detection & Threat Hunting Lab

## Overview

This project documents a hands-on blue team lab focused on intrusion detection, network metadata analysis, and beacon detection. The lab used Suricata in SELKS for IDS alerting, Zeek for network metadata generation, and RITA for identifying suspicious long connections, beaconing activity, DNS tunneling, and abnormal user agents.

## Skills Demonstrated

* Writing and validating custom Suricata detection rules
* Uploading and activating IDS signatures in SELKS
* Triggering and verifying IDS alerts with test traffic
* Reviewing Kibana dashboards and Evebox alerts
* Using Zeek logs to analyze network metadata
* Using `zeek-cut` to make Zeek output more readable
* Using RITA to identify:

  * Long-lived connections
  * Beaconing behavior
  * Suspicious DNS activity
  * Unusual user agents
* Documenting findings with screenshots and analyst notes

## Tools Used

* SELKS
* Suricata
* Kibana
* Evebox
* Zeek
* RITA
* Wireshark
* PowerShell
* SSH
* Remote Desktop

## Environment

* Course: CYBR 445 – Advanced Incident Detection and Response
* Lab: Module 5 – Advanced Network Intrusion Detection/Prevention
* Analyst: Tren Patterson (Analyst 3)

## Project Structure

```text
advanced-network-intrusion-detection-lab/
├── README.md
├── docs/
│   ├── Lab5_Completed.docx
│   └── findings-summary.md
├── screenshots/
│   ├── Lab5_SS01_SELKS_AppMenu_Kibana.png
│   ├── Lab5_SS02a_Kibana_SN_Alerts.png
│   ├── Lab5_SS02b_Kibana_SN_All.png
│   ├── Lab5_SS02c_Kibana_SN_Anomaly.png
│   ├── Lab5_SS02d_Kibana_SN_Overview.png
│   ├── Lab5_SS03_Evebox_Inbox_LastWeek.png
│   ├── Lab5_SS04_Suricata_Metrics.png
│   ├── Lab5_SS05_ETOpen_Rulesets.png
│   ├── Lab5_SS06_EmergingExploit_RuleList.png
│   ├── Lab5_SS07_RuleDetail_Page.png
│   ├── Lab5_SS08_RuleDefinition_InfoTab.png
│   ├── Lab5_SS09_Notepad_analyst3_rule.png
│   ├── Lab5_SS10_AddCustomSource_Form.png
│   ├── Lab5_SS11_CustomSource_Detail.png
│   ├── Lab5_SS12_SID_20220003_InfoTab.png
│   ├── Lab5_SS13a_RulesetActions_Before.png
│   ├── Lab5_SS13b_RulesetActions_After_Applied.png
│   ├── Lab5_SS14_PowerShell_SSH_Curl.png
│   ├── Lab5_SS15_Suricata_RulesActivity_Triggered.png
│   ├── Lab5_SS16_RDP_Connected.png
│   ├── Lab5_SS17_Terminal_Open.png
│   ├── Lab5_SS18_Wireshark_pcap_Loaded.png
│   ├── Lab5_SS19_Zeek_Logs_Directory.png
│   ├── Lab5_SS20a_Zeek_conn_log.png
│   ├── Lab5_SS20b_Zeek_dns_log.png
│   ├── Lab5_SS20c_Zeek_http_log.png
│   ├── Lab5_SS20d_Zeek_ssl_log.png
│   ├── Lab5_SS20e_Zeek_files_log.png
│   ├── Lab5_SS20f_Zeek_weird_log.png
│   ├── Lab5_SS20g_Zeek_x509_log.png
│   ├── Lab5_SS21_RITA_Import.png
│   ├── Lab5_SS22_RITA_Report_Generated.png
│   ├── Lab5_SS23_RITA_Homepage.png
│   ├── Lab5_SS24_RITA_Beacons.png
│   ├── Lab5_SS25_RITA_DNS.png
│   ├── Lab5_SS26_RITA_LongConnections.png
│   └── Lab5_SS27_RITA_UserAgents.png
└── queries/
    └── commands-used.md
```

## Lab Workflow Summary

### Part 1: Suricata in SELKS

The first phase of the lab focused on Suricata-based intrusion detection in SELKS. Kibana dashboards were reviewed to observe alerts, protocol activity, and anomalies. Evebox was used to examine IDS alerts from the previous week. The ETOpen ruleset was explored, and an existing exploit rule was reviewed to understand its protocol, flow direction, payload matching, and classification.

A custom Suricata rule was then created to detect a suspicious User-Agent string tied to Analyst 3. The rule was uploaded as a custom source, added to the default ruleset, applied in Suricata, and triggered using a curl command over SSH. The resulting alert appeared in the Rules Activity view, confirming that the rule worked as expected.

### Part 2: Zeek and RITA

The second phase focused on threat hunting with Zeek and RITA. Wireshark was used to open a packet capture, but the packet volume made manual inspection difficult. Zeek logs were then reviewed for connection metadata, DNS queries, HTTP requests, SSL/TLS sessions, file transfers, anomalies, and certificate data.

RITA was used to identify suspicious behavior at scale. The analysis highlighted long-duration TLS connections, high-confidence beaconing behavior, suspicious DNS activity related to potential tunneling, and an unusual PowerShell-based user agent. These findings demonstrated how metadata-based analysis can surface malicious activity that is difficult to detect through raw packet inspection alone.

## Key Findings

* Suricata generated detailed alert and event data that was searchable in Elasticsearch and visible in Kibana.
* A custom rule detecting `User-Agent: Analyst3` was successfully created, uploaded, activated, and triggered.
* Wireshark alone was not an efficient way to find suspicious behavior in a very large packet capture.
* Zeek logs provided structured, readable metadata that made analysis far easier.
* RITA identified long-lived HTTPS connections that may represent command-and-control activity.
* RITA highlighted suspicious beaconing behavior with a very high beacon score.
* DNS analysis suggested possible tunneling or exfiltration behavior.
* A PowerShell-based user agent stood out as an abnormal outlier.

## Example Detection Rules

### Custom Rule 1

```snort
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"ET USER_AGENTS Suspicious User Agent (Analyst3)"; flow:to_server,established; content:"User-Agent|3a| Analyst3"; nocase; http_header; reference:url,www.bbtrust.com/test.html; classtype:trojan-activity; sid:20220003; rev:6;)
```

### Custom Rule 2

```snort
alert tcp $HOME_NET any -> $EXTERNAL_NET any (msg:"Something really bad is happening"; flow:to_server,established; content:"|53 6F 6D 65 74 68 69 6E 67 20 42 61 64|"; reference:url,www.bbtrust.com/somethingbad.html; classtype:bad-unknown; sid:20221003; rev:6;)
```

## Notable Threat Hunting Observations

* Suspicious long-lived connections were observed over TCP/443.
* Beaconing activity showed highly regular communication patterns.
* DNS activity suggested possible tunneling behavior.
* An unusual PowerShell user agent indicated likely scripted or malicious web requests.

## What I Learned

This lab reinforced the value of layered network defense and threat hunting. Writing a Suricata rule showed how signatures can be tailored to detect specific traffic patterns. Zeek demonstrated how metadata can simplify analysis compared to raw packets, and RITA showed how automation and statistics can reveal beaconing, exfiltration, and outlier behavior that would be difficult to identify manually.

## Files to Include in GitHub

* Completed lab report
* All screenshots used in the report
* A short findings summary in Markdown
* A command reference file listing the major commands used

## Suggested Repo Description

Blue team lab using Suricata, SELKS, Zeek, Wireshark, and RITA to detect IDS alerts, beaconing, long-lived connections, suspicious DNS activity, and abnormal user agents.

## Suggested Tags

`suricata` `zeek` `rita` `wireshark` `threat-hunting` `ids` `network-security` `cybersecurity-lab`
