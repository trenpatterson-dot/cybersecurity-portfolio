Ran Wireshark against live traffic and a real malware PCAP. Here's what the analysis looked like.

Live capture first: DNS queries, ARP resolution, HTTP vs HTTPS side by side. Seeing plaintext HTTP next to TLS-encrypted traffic in the same tool makes the encryption conversation concrete fast. Every request header and response body visible in HTTP. Nothing but ciphertext in TLS.

Then the malware PCAP. Pulled a sample from Malware-Traffic-Analysis.net, opened it in Wireshark, and pivoted on host 10.2.28.88 as the main system of interest. Found outbound HTTP to 23.47.50.182 (GET /connecttest.txt), outbound TLS to 13.89.179.9, and internal SMB/SMB2/CLDAP traffic between the host and 10.2.28.2.

Not all of it was malicious. Some was Windows NCSI checks and normal AD behavior. Knowing what to rule out is half the job.

The real skill in packet analysis isn't spotting everything flagged — it's establishing the baseline first so the actual anomalies stand out.

Tools: Wireshark · Kali Linux · nslookup · curl · Malware-Traffic-Analysis.net

#Wireshark #PacketAnalysis #NetworkForensics #BlueTeam #SOC
