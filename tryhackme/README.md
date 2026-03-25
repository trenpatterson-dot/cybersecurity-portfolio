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
