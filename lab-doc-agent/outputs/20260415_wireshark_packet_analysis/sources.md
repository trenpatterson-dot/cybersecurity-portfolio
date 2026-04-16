# Sources & References — Wireshark Packet Analysis

- [Wireshark](https://www.wireshark.org/) — Packet capture and analysis tool; primary tool throughout the lab
- [Wireshark Display Filter Reference](https://www.wireshark.org/docs/dfref/) — Reference for display filter syntax used: dns, arp, http.request, tls, smb, smb2
- [Malware-Traffic-Analysis.net](https://www.malware-traffic-analysis.net/) — Source for the malware exercise PCAP used in Phase 2 analysis
- [Kali Linux](https://www.kali.org/) — Analysis platform used for live capture and PCAP investigation
- nslookup — Built-in DNS query tool; used to generate controlled DNS traffic for observation
- ping — ICMP tool; used to trigger ARP requests and observe local MAC resolution
- curl — CLI HTTP client; used to generate HTTP and HTTPS traffic for plaintext vs encrypted comparison
- [Windows NCSI Documentation](https://learn.microsoft.com/en-us/troubleshoot/windows-client/networking/internet-explorer-edge-open-connect-corporate-public-network) — Explains the `GET /connecttest.txt` behavior observed from 10.2.28.88 to 23.47.50.182
- [RFC 826 — ARP](https://datatracker.ietf.org/doc/html/rfc826) — Address Resolution Protocol specification; relevant to ARP request/reply behavior observed
- [RFC 5246 — TLS 1.2](https://datatracker.ietf.org/doc/html/rfc5246) — Transport Layer Security specification; relevant to TLS handshake and encrypted traffic analysis
- [MS-CLDAP — Connectionless LDAP](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-adts/7f9bfef5-d6f8-4cb2-aa57-f11b73e0cf2b) — Microsoft documentation on CLDAP; explains internal CLDAP traffic observed between 10.2.28.88 and 10.2.28.2
