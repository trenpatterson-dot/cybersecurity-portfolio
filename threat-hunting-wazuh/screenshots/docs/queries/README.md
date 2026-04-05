# Threat Hunting with Wazuh: Detecting Credential Access and Brute Force Activity

## Overview
This project documents the deployment and use of the Wazuh SIEM platform in a lab environment to detect suspicious activity on monitored endpoints. The lab included a Windows 11 endpoint and an Ubuntu Linux endpoint connected to a Wazuh server.

The project focused on two detection scenarios:
1. Credential access activity through access to `/etc/shadow`
2. Brute force behavior through repeated failed authentication attempts using `su`

## Objectives
- Deploy and configure Wazuh in a virtual lab
- Connect endpoints to the SIEM
- Generate suspicious activity in a controlled environment
- Use Wazuh Discover to hunt for related alerts and logs
- Map detected behavior to the MITRE ATT&CK framework

## Environment
- Wazuh server deployed on Ubuntu VM
- Ubuntu Linux endpoint
- Windows 11 endpoint
- VMware Workstation
- Wazuh Dashboard, Indexer, Manager, and Agents

## Detection Scenario 1: Credential Access
A privileged command was executed on the Ubuntu endpoint to access `/etc/shadow`, which stores password hashes.

### Commands used
```bash
sudo su
whoami
cat /etc/shadow