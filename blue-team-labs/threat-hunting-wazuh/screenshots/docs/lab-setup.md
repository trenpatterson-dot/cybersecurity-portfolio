# Lab Setup

## Overview
This lab environment was built to deploy and test the Wazuh SIEM platform in a virtualized setting. The goal was to monitor endpoint activity and perform threat hunting on both Linux and Windows systems.

## Environment
- Virtualization: VMware Workstation
- SIEM Platform: Wazuh (Manager, Indexer, Dashboard)
- Linux Endpoint: Ubuntu 24.04
- Windows Endpoint: Windows 11
- Network: Internal NAT network

## Components Installed
- Wazuh Manager
- Wazuh Indexer (OpenSearch)
- Wazuh Dashboard
- Wazuh Agent (Ubuntu + Windows)

## Agent Configuration
- Ubuntu agent connected to Wazuh manager using IP address
- Windows agent installed via MSI package and connected to manager
- Both agents verified as active in the dashboard

## Challenges Encountered
- API connection errors (authentication failures)
- Wazuh manager service not initially installed
- Password synchronization issues between dashboard and API
- Agent enrollment issues (port 1515 not open)
- Dashboard showing API as offline

## Resolution Steps
- Installed and enabled Wazuh manager service
- Verified API port (55000) was listening
- Reset API credentials using Wazuh password tools
- Updated credentials in Wazuh dashboard configuration
- Restarted services (manager, indexer, dashboard)
- Verified successful API connection and agent status

## Outcome
The Wazuh platform was successfully deployed and configured. Both endpoints were actively sending logs, allowing for real-time monitoring and threat detection.