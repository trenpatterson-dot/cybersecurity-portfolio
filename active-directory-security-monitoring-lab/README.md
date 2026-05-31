# Active Directory Security Monitoring Lab

## Overview

This project demonstrates the deployment of a Windows Server 2022 Active Directory environment and the investigation of key Active Directory security events used by Security Operations Center (SOC) and Identity and Access Management (IAM) teams.

The lab was built to simulate real-world identity monitoring, user lifecycle management, account lockout investigations, and privileged access monitoring.

---

## Environment

### Infrastructure

* Windows Server 2022 Domain Controller
* Active Directory Domain Services (AD DS)
* DNS Server
* Organizational Unit (IAM-Lab)

### Domain

* Domain Name: trenlab.local
* NetBIOS Name: TRENLAB

### Test Accounts

* HelpDesk User
* SOC Analyst
* Test User
* Contractor User

---

## Objectives

* Deploy and configure Active Directory
* Create and manage users and groups
* Generate Windows Security Events
* Investigate identity-related activity
* Document findings and evidence
* Build practical IAM and SOC investigation experience

---

## Investigations Completed

### IAM-001 – Failed Authentication Monitoring

Event ID:

* 4625 – Failed Logon

Activities:

* Generated failed login attempts
* Investigated authentication failures
* Analyzed failure status codes

---

### IAM-002 – Account Lockout Monitoring

Event ID:

* 4740 – Account Locked Out

Activities:

* Configured account lockout policy
* Triggered lockout conditions
* Investigated lockout events

---

### IAM-003 – Group Membership Monitoring

Event IDs:

* 4728 – Member Added To Group
* 4729 – Member Removed From Group

Activities:

* Created security groups
* Added and removed users
* Investigated group membership changes

---

### IAM-004 – User Lifecycle Monitoring

Event IDs:

* 4720 – User Created
* 4724 – Password Reset
* 4738 – User Modified
* 4726 – User Deleted

Activities:

* Created user accounts
* Reset passwords
* Modified account attributes
* Deleted user accounts
* Investigated lifecycle events

---

### IAM-005 – Privileged Access Monitoring

Event IDs:

* 4728 – Privileged Group Assignment
* 4729 – Privileged Group Removal

Activities:

* Created Tier1-Admins group
* Assigned privileged access
* Simulated privilege escalation scenarios
* Investigated access revocation events

---

## Key Security Events Investigated

| Event ID | Description              |
| -------- | ------------------------ |
| 4625     | Failed Logon             |
| 4740     | Account Lockout          |
| 4720     | User Created             |
| 4724     | Password Reset           |
| 4738     | User Modified            |
| 4726     | User Deleted             |
| 4728     | Group Membership Added   |
| 4729     | Group Membership Removed |

---

## Skills Demonstrated

* Active Directory Administration
* Windows Server 2022
* Identity and Access Management (IAM)
* Security Event Analysis
* Log Investigation
* Incident Documentation
* Security Monitoring
* User Lifecycle Management
* Privileged Access Monitoring

---

## Repository Structure

```text
active-directory-security-monitoring-lab/
├── detections/
├── docs/
├── notes/
├── queries/
├── screenshots/
│   ├── detections/
│   └── domain-controller/
```

---

## Future Enhancements

* Integrate Active Directory with Wazuh
* Forward Windows Security Events to SIEM
* Create Active Directory detection rules
* Build identity-focused threat hunting scenarios
* Develop automated alerting and dashboards

---

## Author

Tren Patterson

Cybersecurity Student | SOC Analyst Candidate | Blue Team Enthusiast

Bellevue University – Cybersecurity
