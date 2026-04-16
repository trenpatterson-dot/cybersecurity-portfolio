# Wireshark Packet Analysis

**Platform:** Kali Linux VM
**Date:** 2026-04-15
**Difficulty:** 3/5
**Type:** Class Lab — Network Protocol Analysis / Malware PCAP Investigation

---

## Objective

Analyze live network traffic and a malware PCAP using Wireshark. Goals: understand protocol behavior at the packet level, compare plaintext HTTP vs TLS-encrypted HTTPS traffic, and produce IOC-style findings from a real-world malware capture.

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Wireshark | Packet capture and analysis |
| Kali Linux | Analysis platform |
| nslookup | Generate controlled DNS query/response traffic |
| ping | Trigger ARP requests for local MAC resolution |
| curl | Generate HTTP and HTTPS traffic for side-by-side comparison |
| Malware-Traffic-Analysis.net PCAP | Real-world malware traffic sample |

---

## Methodology

### Phase 1 — Live Traffic Capture

1. Opened Wireshark on Kali and captured on the active network interface.
2. Used `nslookup` to generate DNS traffic; filtered on `dns` to observe query and response packet structure.
3. Pinged a local IP to trigger ARP; filtered on `arp` to confirm IP-to-MAC resolution behavior.
4. Used `curl http://example.com` — confirmed full HTTP request/response content visible in plaintext.
5. Used `curl https://example.com` — filtered on `tls`, confirmed traffic was encrypted and application data unreadable.

### Phase 2 — Malware PCAP Analysis

6. Downloaded a password-protected malware exercise PCAP from Malware-Traffic-Analysis.net.
7. Extracted the archive from the terminal and opened the PCAP in Wireshark.
8. Reviewed **Protocol Hierarchy** to identify protocols present across the full capture.
9. Reviewed **Conversations** to identify the most active hosts by traffic volume.
10. Applied targeted display filters — `dns`, `http.request`, `tls`, `smb`, `smb2` — to investigate activity systematically.
11. Pivoted on host `10.2.28.88` as the primary system of interest based on traffic volume and external connections.

---

## Findings

### Protocol Behavior (Live Capture)

- DNS query/response cycle confirmed and captured — structure clearly visible in packet detail pane.
- ARP confirmed: request fires before local IP communication even when the ICMP ping itself fails. The stack resolves MAC before it can send anything.
- HTTP traffic confirmed readable in plaintext — headers, method, URI, and response body all visible.
- HTTPS/TLS traffic confirmed encrypted — TLS handshake visible, application data is ciphertext.

### Malware PCAP — Host 10.2.28.88

- **Internal traffic:** DNS, CLDAP, SMB, SMB2 between `10.2.28.88` and `10.2.28.2` — consistent with Active Directory and Windows domain environment baseline activity.
- **Outbound HTTP:** `GET /connecttest.txt` to `23.47.50.182` — identified as Windows NCSI (Network Connectivity Status Indicator) behavior. Flagged, assessed as likely benign Microsoft connectivity check.
- **Outbound TLS:** Encrypted sessions to `13.89.179.9` — confirmed **AS8075 Microsoft Corporation** (Des Moines, Iowa) via ipinfo.io. Ruled out as malicious; consistent with normal Windows/Azure service communication.

**Key analytical decision:** Several initially suspicious connections were ruled out as normal Windows background traffic. Separating AD/domain baseline behavior from actual anomalies was the core challenge of this exercise.

---

## Skills Demonstrated

- Live packet capture and protocol-level traffic analysis in Wireshark
- Display filter workflow across multiple protocols: `dns`, `arp`, `http.request`, `tls`, `smb`, `smb2`
- Malware PCAP triage: Protocol Hierarchy → Conversations → host pivot → targeted filtering
- IOC documentation and traffic contextualization
- Distinguishing normal Windows/Active Directory traffic from anomalous external connections
