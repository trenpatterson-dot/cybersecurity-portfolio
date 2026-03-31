# TryHackMe - Intro to LAN

## Overview
This room introduced fundamental networking concepts including MAC addresses, ICMP (ping), and basic network communication.

## Skills Practiced
- Understanding MAC addresses
- MAC address spoofing concepts
- Using ICMP (ping) for network testing
- Identifying weaknesses in network-based access controls

## Key Concepts

### MAC Address
A MAC (Media Access Control) address is a unique identifier assigned to network interfaces for communication on a network.

### MAC Spoofing
MAC spoofing involves changing a device’s MAC address to impersonate another device.

### ICMP (Ping)
The ping command is used to test connectivity between devices on a network.

```bash
ping 10.10.10.10
ping 8.8.8.8
Findings
MAC Spoofing Lab
Successfully spoofed MAC address to impersonate an authorized device
Gained access to restricted resource
Retrieved flag:
THM{YOU_GOT_ON_TRYHACKME}
ICMP Lab
Verified connectivity using ping
Retrieved flag:
THM{I_PINGED_THE_SERVER}
Key Learning

MAC address filtering is not a secure form of access control because MAC addresses can be easily spoofed.

Takeaway

Network security should rely on strong authentication mechanisms rather than identifiers like MAC addresses, which can be manipulated.

Personal Reflection

This room helped reinforce foundational networking concepts and demonstrated how easily weak access controls can be bypassed. It also improved my understanding of how tools like ping are used in both troubleshooting and reconnaissance.
 