# Wireshark Packet Analysis — Personal Notes
**Date:** 2026-04-15

## What Worked

- Starting with live traffic before the malware PCAP — gave me a real baseline for normal protocol behavior
- Host pivot strategy: lock onto one IP (10.2.28.88) instead of trying to analyze the whole capture at once
- Protocol Hierarchy + Conversations as first steps before any filtering — use this every time
- Filter sequence that worked well: `dns` → `http.request` → `tls` → `smb` → `smb2`

## What Didn't / Gotchas

- CLDAP tripped me up — it's Connectionless LDAP, completely normal in AD environments for DC queries. Don't chase it.
- `GET /connecttest.txt` looked suspicious at first. It's Windows NCSI — checking if the internet is reachable. Know your Microsoft telemetry/connectivity patterns.
- Don't treat every flagged packet as malicious. Establish normal first.
- ARP behavior: if you only look at ping success/fail, you'll miss that ARP still fires even when ICMP doesn't get a response. Check the `arp` filter explicitly.

## Key Filters Used

```wireshark
dns
arp
http.request
tls
smb
smb2

# Filter by specific host
ip.addr == 10.2.28.88

# Combine host + protocol
ip.addr == 10.2.28.88 && http.request
ip.addr == 10.2.28.88 && tls
```

## Traffic Generation Commands

```bash
# DNS traffic
nslookup google.com

# ARP trigger
ping 10.x.x.x

# HTTP (plaintext)
curl http://example.com

# HTTPS (TLS encrypted)
curl https://example.com

# Extract password-protected PCAP
unzip -P infected malware-sample.zip
# or
7z x malware-sample.zip -pinfected
```

## Tools and Why

| Tool | Why I Used It |
|------|--------------|
| Wireshark | Core analysis — capture, filter, Protocol Hierarchy, Conversations |
| nslookup | Generate DNS traffic to observe query/response structure |
| ping | Trigger ARP requests, observe MAC resolution |
| curl | Generate both HTTP and HTTPS traffic for direct comparison |
| Malware-Traffic-Analysis.net | Real-world PCAP samples for practice |

## What Clicked

- **ARP before everything:** The network stack resolves MAC address via ARP before it can send any IP packets to a local host. Even if ping fails, ARP already happened.
- **HTTP vs HTTPS is obvious in Wireshark:** HTTP shows you the full request line, headers, body — everything. HTTPS shows a TLS handshake and then encrypted blobs. The contrast makes encryption tangible, not abstract.
- **Baseline first, anomalies second:** If you don't know what normal Windows domain traffic looks like, every SMB packet looks like lateral movement. CLDAP looks like C2. NCSI checks look like beaconing. Know your environment.

## Next Steps

- `13.89.179.9` — confirmed AS8075 Microsoft Corporation (Des Moines, IA) via `curl https://ipinfo.io/13.89.179.9`. Ruled out. Both outbound TLS destinations in this PCAP were Microsoft infrastructure.
- Deep dive into Windows NCSI behavior — exactly what triggers `GET /connecttest.txt` and to which IPs
- More malware PCAPs from Malware-Traffic-Analysis.net — focus on identifying full infection chains, not just individual IOCs
- Look into **NetworkMiner** as a complement to Wireshark — better for file extraction from PCAPs
- Explore **following TCP streams** in Wireshark to reconstruct HTTP conversations end-to-end
- Practice with `tshark` (CLI Wireshark) for faster headless analysis
