# Wireshark Packet Analysis

**Platform:** Kali Linux VM | **Course:** CYBR 445 — Week 10 | **Date:** 2026-04-17

Hands-on packet analysis lab: captured live DNS, ARP, HTTP, and HTTPS traffic, then analyzed a malware PCAP from Malware-Traffic-Analysis.net.

## Tools Used
- Wireshark
- Kali Linux
- nslookup, ping, curl
- Malware-Traffic-Analysis.net PCAP sample

## What This Lab Demonstrates
- Live packet capture and protocol-level traffic analysis
- DNS query/response and ARP resolution behavior
- HTTP vs HTTPS — plaintext vs TLS-encrypted traffic
- Wireshark filter discipline for triage and investigation
- IOC-style documentation from a malware PCAP
- Separating normal infrastructure traffic from suspicious outbound connections

## Key Findings

**Live Capture:**
- DNS query/response confirmed for `google.com`
- ARP resolved local IP-to-MAC even when ping failed
- HTTP traffic visible in plaintext; HTTPS encapsulated in TLS

**Malware PCAP (`2026-02-28-traffic-analysis-exercise.pcap`):**
- `10.2.28.88` identified as primary host of interest
- Internal traffic to `10.2.28.2` consistent with normal AD/SMB behavior (CLDAP, SMB, SMB2)
- Outbound HTTP to `23.47.50.182` — `GET /connecttest.txt HTTP/1.1`
- Outbound TLSv1.2 to `13.89.179.9` — encrypted session, requires enrichment

## IOC Candidates
| Indicator | Type | Notes |
|-----------|------|-------|
| `10.2.28.88` | Internal IP | Primary host of interest |
| `23.47.50.182` | External IP | HTTP destination |
| `13.89.179.9` | External IP | TLS destination |

## Key Takeaway
Not every packet in a suspicious PCAP is malicious. Blue team analysis means establishing what normal looks like first, then isolating what actually deserves escalation.
