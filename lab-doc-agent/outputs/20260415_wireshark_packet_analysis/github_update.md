# Wireshark Packet Analysis

Network traffic analysis lab — live capture plus malware PCAP triage using Wireshark on Kali Linux.

## Tools

- Wireshark
- Kali Linux
- nslookup / ping / curl (traffic generation)
- Malware-Traffic-Analysis.net PCAP sample

## What This Lab Demonstrates

- Protocol-level analysis: DNS, ARP, HTTP, HTTPS/TLS, SMB, SMB2, CLDAP
- Wireshark display filter workflow (`dns`, `arp`, `http.request`, `tls`, `smb`, `smb2`)
- Malware PCAP triage methodology: Protocol Hierarchy → Conversations → host pivot → targeted filtering
- Differentiating normal Windows/Active Directory background traffic from suspicious activity
- IOC identification and documentation from raw packet data

## Key Findings

**Live Capture**
- DNS query/response structure captured and confirmed
- ARP fires before local IP communication even when ICMP ping fails — stack needs MAC resolution first
- HTTP traffic confirmed readable in plaintext at packet level
- HTTPS/TLS confirmed encrypted — application data not visible without session keys

**Malware PCAP (host 10.2.28.88)**
- Internal DNS, CLDAP, SMB, SMB2 traffic to `10.2.28.2` — consistent with AD domain environment baseline
- Outbound HTTP: `GET /connecttest.txt` to `23.47.50.182` — assessed as Windows NCSI behavior (likely benign)
- Outbound TLS: Encrypted session to `13.89.179.9` — external destination, flagged for further investigation

## Setup Notes

To replicate the malware PCAP analysis:
1. Download a PCAP exercise from [Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/)
2. Extract the password-protected archive (standard password: `infected`)
3. Open in Wireshark — start with Protocol Hierarchy, then Conversations, then filter by host
