# TryHackMe - Subdomain and Virtual Host Enumeration

## Overview
This lab focused on discovering hidden subdomains and virtual hosts using OSINT and active enumeration techniques.

## Skills Practiced
- DNS brute forcing
- Virtual host enumeration
- Host header fuzzing
- Response analysis
- Troubleshooting enumeration issues

## Tools Used
- dnsrecon
- ffuf
- SecLists
- Linux AttackBox

## Commands Used

### DNS Enumeration
```bash
dnsrecon -t brt -d acmeitsupport.thm
ffuf -w /usr/share/wordlists/SecLists/Discovery/DNS/namelist.txt -u http://acmeitsupport.thm/ -H "Host: FUZZ.acmeitsupport.thm"
Findings
DNS Subdomains Found
api
www
Virtual Hosts Found
delta
yellow
Challenges Encountered

At first, many responses looked identical, which made it difficult to identify valid virtual hosts. Most results returned the same HTTP status code and response size. This required focusing on subtle response differences and making sure the lab environment was configured correctly.

Lessons Learned
DNS enumeration and virtual host enumeration are not the same thing
The Host header is critical for virtual host fuzzing
Valid findings do not always return unique status codes
Proper /etc/hosts configuration is sometimes required
Output filtering is helpful, but filtering too early can hide valid results
Key Takeaway

This lab reinforced the importance of using the right tool for the right layer and paying attention to response patterns rather than relying only on status codes.
