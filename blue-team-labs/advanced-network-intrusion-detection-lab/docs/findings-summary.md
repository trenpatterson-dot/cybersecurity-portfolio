# Findings Summary

## Overview
This lab focused on detecting malicious network activity using Suricata, Zeek, and RITA. The goal was to identify suspicious traffic patterns, validate custom IDS rules, and analyze metadata for evidence of command-and-control behavior.

## Key Findings
- A custom Suricata rule successfully detected a suspicious User-Agent string and generated an alert in SELKS.
- Kibana and Evebox showed how IDS alerts can be reviewed and triaged in a SOC-style workflow.
- Wireshark was useful for viewing the packet capture, but the volume of packets made manual analysis difficult.
- Zeek logs provided structured metadata for connections, DNS, HTTP, TLS, file activity, anomalies, and certificates.
- RITA identified suspicious long-lived TLS connections, likely beaconing activity, suspicious DNS patterns, and an abnormal PowerShell-based user agent.

## Conclusion
This lab demonstrated how combining IDS signatures with metadata analysis and threat-hunting tools can make malicious network behavior easier to detect than relying on raw packet captures alone.