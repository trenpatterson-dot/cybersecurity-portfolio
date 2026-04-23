# Suspicious Network Traffic Investigation (Wireshark + Nmap)

## Overview
Built a controlled lab environment to simulate and analyze network reconnaissance activity using Kali Linux and an Ubuntu target system.

Captured and analyzed live packet data using Wireshark to identify scanning behavior, validate open/closed ports, and confirm active services.

## Lab Setup
- Attacker: Kali Linux (192.168.32.128)
- Target: Ubuntu (192.168.32.129)
- Network: Host-only (isolated lab)
- Tools:
  - Nmap
  - Wireshark

## Objective
Detect and analyze suspicious network activity and determine whether reconnaissance or scanning behavior is present.

## What I Did
- Verified connectivity between attacker and target (ICMP)
- Performed Nmap SYN scan with service detection:
- Captured live traffic using Wireshark on the target system
- Applied filters to isolate scanning activity:
- tcp.flags.syn == 1
- tcp.flags.reset == 1
- ip.addr == 192.168.32.129

## Key Findings
- High volume of SYN packets across multiple ports → confirms scanning behavior
- SYN/ACK responses on ports 22 and 443 → confirms open services
- RST/ACK responses → confirms closed ports
- TLSv1.3 handshake observed on port 443 → active HTTPS service
- SSH service identified on port 22

## Conclusion
Traffic analysis confirmed reconnaissance activity consistent with a TCP SYN scan. The attacker successfully identified open services and validated host responsiveness.

## Skills Demonstrated
- Packet analysis (Wireshark)
- Network reconnaissance detection
- TCP/IP analysis (SYN, ACK, RST behavior)
- Service identification
- Threat analysis mindset

## MITRE ATT&CK
- T1046 – Network Service Scanning

## Screenshots
See `/docs/images` for full evidence.