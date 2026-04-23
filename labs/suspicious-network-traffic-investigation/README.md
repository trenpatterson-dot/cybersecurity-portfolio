# Suspicious Network Traffic Investigation

## Overview
This project is a reconnaissance exercise focused on investigating suspicious network traffic, using tools such as nmap and Wireshark. The objective is to identify potential threats and understand the behavior of the observed traffic.

## Objective
The goal of this investigation was to analyze network traffic between IP addresses 192.168.32.128 (source) and a target system, with a focus on understanding the protocols in use, open ports, and services running on the target system.

## Tools Used
- nmap
- Wireshark

## Environment / Lab Setup
This investigation was conducted in a standalone environment, with the specific details of the network setup not provided in the evidence.

## Investigation Steps
1. Reviewed the original alert or log source to initiate the investigation.
2. Identified the source IP (192.168.32.128), destination IP, protocols, open ports, and timestamps from the evidence.
3. Confirmed the traffic volume and timing through Wireshark packet captures.
4. Checked whether the activity matched expected behavior for the environment.

## Key Findings
- Nmap scan output identified SSH and HTTPS services on the target system.
- Wireshark packet captures revealed a SYN scan, RST responses, ICMP connectivity validation, TCP SYN scan from 192.168.32.128, and active HTTPS service via TLSv1.3 handshake.
- The target system responded with both open and closed port behavior.

## Security Impact
The findings suggest that the observed traffic may be a reconnaissance attempt, as the attacker is probing for open ports and services on the target system.

## Screenshots
- [01-nmap-command.png](docs/images/01-nmap-command.png)
- [02-wireshark-overview.png](docs/images/02-wireshark-overview.png)
- [03-syn-scan-evidence.png](docs/images/03-syn-scan-evidence.png)
- [04-port-response-evidence.png](docs/images/04-port-response-evidence.png)
- [05-target-ip-traffic.png](docs/images/05-target-ip-traffic.png)
- [06-service-detection-evidence.png](docs/images/06-service-detection-evidence.png)

