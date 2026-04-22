# Threat Hunting with Wazuh

A self-built home lab deploying Wazuh SIEM across Ubuntu and Windows 11 endpoints to simulate attacker
activity and detect it in real time. Covers the full blue team workflow: environment provisioning,
multi-OS agent enrollment, attack execution from Kali Linux, alert triage in the Wazuh dashboard,
and SOC-style findings documented with MITRE ATT&CK mapping.

---

## Overview

| Component        | Role                        | OS / Platform          |
|------------------|-----------------------------|------------------------|
| Wazuh Server     | Manager · Indexer · Dashboard | Ubuntu (VMware)      |
| Target Endpoint  | Monitored agent             | Ubuntu 24.04 (VMware)  |
| Attacker         | Attack simulation           | Kali Linux (VMware)    |
| Target Endpoint  | Monitored agent             | Windows 11 (VMware)    |

All machines run on an internal NAT network in VMware Workstation.
The lab simulates two detection scenarios — **credential access** and **brute force authentication** —
and validates that Wazuh detects both within seconds of execution.

---

## Objectives

- Deploy Wazuh Manager, Indexer (OpenSearch), and Dashboard on a self-managed Ubuntu server
- Enroll Ubuntu and Windows 11 agents and verify active log forwarding
- Simulate credential access (`/etc/shadow` read) and brute force authentication from a Kali Linux attacker
- Triage generated alerts in the Wazuh dashboard: rule IDs, severity, timestamps, source context
- Map detected behaviors to the MITRE ATT&CK framework
- Document the full blue team workflow as a SOC-style lab report

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Wazuh Manager | Log collection, rule evaluation, alert generation |
| Wazuh Indexer (OpenSearch) | Alert storage and search backend |
| Wazuh Dashboard | Alert triage, threat hunting, agent monitoring UI |
| Wazuh Agent — Ubuntu | Endpoint log forwarding (Linux target) |
| Wazuh Agent — Windows MSI | Endpoint log forwarding (Windows 11 target) |
| VMware Workstation | Virtualization platform for all lab VMs |
| Kali Linux | Attacker machine for simulated offensive activity |
| Ubuntu 24.04 | Primary monitored Linux endpoint |
| Windows 11 | Secondary monitored Windows endpoint |

---

## Steps Performed

### Phase 1 — Environment Setup

1. Provisioned three VMs in VMware Workstation on an internal NAT network: Wazuh Server (Ubuntu),
   Target Endpoint (Ubuntu 24.04), and Attacker (Kali Linux). A Windows 11 VM was also enrolled as
   a secondary monitored endpoint.
2. Installed Wazuh Manager, Indexer (OpenSearch), and Dashboard on the server VM.
3. Resolved initial service startup failures:
   - Wazuh Manager service was not installed — installed and enabled manually.
   - API port 55000 was not listening — confirmed service state and restarted.
   - Password desynchronization between the Wazuh Dashboard and the API service caused the dashboard
     to show the API as offline — reset credentials using Wazuh password tools and updated the
     dashboard configuration file to match.
4. Opened TCP port **1515** on the server to unblock agent enrollment; without this, agents fail to
   register with no visible error surfaced in the dashboard.
5. Enrolled the Ubuntu agent by configuring `ossec.conf` with the manager's IP address and
   restarting the agent service. Verified active status in the Wazuh dashboard.
6. Enrolled the Windows 11 agent via the official MSI package, pointed it at the manager, and
   verified active status in the dashboard.
7. Confirmed both agents were actively forwarding logs via the Wazuh Overview Dashboard.

### Phase 2 — Detection 1: Credential Access via `/etc/shadow`

**MITRE ATT&CK: [T1003.008 — OS Credential Dumping: /etc/passwd and /etc/shadow](https://attack.mitre.org/techniques/T1003/008/)**

8. Executed the following commands on the monitored Ubuntu endpoint to simulate a credential access attempt:
   ```bash
   sudo su          # escalate to root
   whoami           # confirm privileged identity
   cat /etc/shadow  # read password hash file
   ```
9. Triaged the resulting Wazuh alert: reviewed rule ID, severity level, triggering process, and
   timestamp. Confirmed the alert correctly identified access to `/etc/shadow` under elevated privileges.
10. Mapped the event to MITRE T1003.008 and documented findings.

### Phase 3 — Detection 2: Brute Force Authentication Attempts

**MITRE ATT&CK: [T1110 — Brute Force](https://attack.mitre.org/techniques/T1110/)**

11. Executed a bash loop on the Ubuntu endpoint to generate 10 consecutive failed `su` authentication
    attempts, simulating brute force behavior:
    ```bash
    for i in {1..10}; do su root; done
    ```
12. Observed **Wazuh Rule 5763** (multiple authentication failures) fire in the dashboard within
    seconds of the loop starting.
13. Performed timestamp correlation between the attacker terminal output and the SIEM alert timestamp
    to measure detection latency.
14. Triaged the alert in Wazuh Discover: reviewed rule ID, description, severity, agent context,
    and timestamp. Mapped to MITRE T1110 and documented findings.

---

## Key Findings

### ✅ Wazuh Rule 5763 detected brute force activity in real time
Wazuh Rule 5763 (multiple authentication failures) triggered within seconds of the brute force loop
starting. Rule fires reliably on repeated `su` failures consistent with **MITRE T1110 (Brute Force)**.
Confirms the detection pipeline is functional and responsive for this attack pattern.

### ✅ `/etc/shadow` access detected under elevated privileges
`cat /etc/shadow` executed via `sudo su` on a monitored Ubuntu endpoint generated a Wazuh alert
correctly identifying access to the Linux shadow password file. `/etc/shadow` stores password hashes
for all system accounts — unauthorized access maps directly to **MITRE T1003.008 (OS Credential
Dumping: /etc/passwd and /etc/shadow)**.

### ✅ Sub-10-second detection latency confirmed
Timestamp correlation between the Kali Linux attacker terminal and the Wazuh SIEM alert confirmed
detection latency under 10 seconds. Validates that the log forwarding and alerting pipeline has
minimal lag — relevant for benchmarking against real-world SOC mean-time-to-detect (MTTD) targets.

### ✅ Multi-OS endpoint coverage established
Both Ubuntu 24.04 and Windows 11 agents successfully enrolled and confirmed active in the Wazuh
dashboard. Demonstrates cross-platform SIEM deployment and monitoring capability across heterogeneous
endpoints.

### ⚠️ Misconfigured agent produces a silent blind spot
A misconfigured `ossec.conf` on an agent caused it to silently fail to forward logs — no alerts
generated, and no error surfaced in the Wazuh dashboard. **A non-forwarding agent is indistinguishable
from a quiet endpoint without active health monitoring.** This is a critical SIEM deployment risk in
production environments.

### ⚠️ Port 1515 closure silently blocks agent enrollment
Agent enrollment was blocked because TCP port 1515 was not open on the Wazuh server. The agent
failed to register with no visible indication in the dashboard, leaving the endpoint entirely
unmonitored. Firewall rules must be explicitly validated as part of any agent deployment checklist.

### ⚠️ Credential desynchronization disables management plane visibility
Password mismatch between the Wazuh Dashboard and the API service caused the management plane to
appear offline. No agent data or alerts were accessible via the UI until credentials were reset using
Wazuh password tools and services were restarted. Component-level credential management must be
treated as a critical operational dependency.

---

## Screenshots

**Wazuh Overview Dashboard** — Agent summary and triggered alert counts across monitored endpoints.

![Wazuh Overview Dashboard](screenshots/wazuh-overview-dashboard.png)

---

**Active Agents** — Both Ubuntu and Windows 11 endpoints enrolled and reporting to the Wazuh manager.

![Agents Active](screenshots/agents-active.png)

---

**Attack Simulation Terminal** — Execution of attack simulation commands: brute force loop and
credential access sequence on the monitored Ubuntu endpoint.

![Attack Simulation Terminal](screenshots/attack-simulation-terminal.png)

---

**Brute Force Detection** — Wazuh Rule 5763 triggered in the dashboard following the brute force
authentication simulation. Alert fired within seconds of attack start.

![Brute Force Detection](screenshots/brute-force-detection.png)

---

## Lessons Learned

**Silent failures are the most dangerous failures.**
Both the misconfigured agent and the closed port 1515 produced zero visible errors in the dashboard.
An unmonitored endpoint looks identical to a quiet one. In a production SOC, agent health checks and
enrollment validation must be automated and continuously monitored — not assumed.

**SIEM deployment is an operational discipline, not a one-time install.**
Three distinct infrastructure issues (service startup, port access, credential synchronization) each
independently blocked the platform from functioning. Each required a different remediation path.
Understanding the full dependency chain of a SIEM — manager, indexer, API, dashboard, and agent —
is a prerequisite for reliable deployment and troubleshooting.

**Detection latency matters and can be measured.**
Timestamp correlation between the attacker terminal and the SIEM alert is a concrete, reproducible
way to benchmark detection pipeline performance. Sub-10-second latency in this lab provides a
baseline for comparing against production MTTD targets and identifying forwarding bottlenecks.

**MITRE ATT&CK mapping sharpens triage decisions.**
Assigning technique IDs (T1003.008, T1110) to detected events moves alert triage from reactive
("something fired") to contextual ("this matches a known attacker behavior pattern with documented
mitigations"). Building this habit in a lab environment directly transfers to structured threat hunting
and incident response workflows.
```

---

### What was done and why

| Decision | Rationale |
|---|---|
| **Findings section leads with severity indicators (✅ / ⚠️)** | Lets recruiters scan impact immediately; lets technical reviewers locate the operational findings fast |
| **⚠️ findings get equal weight to ✅ findings** | The three infrastructure failures are the most technically instructive part of this lab — burying them would underrepresent the actual work done and the real-world relevance |
| **MITRE technique IDs are hyperlinked inline** | Places ATT&CK context exactly where a technical reviewer needs it, without a separate appendix |
| **Commands in fenced code blocks with inline comments** | Makes the attack simulation reproducible and readable without requiring the reader to open a separate doc |
| **Screenshot captions precede images** | Caption-first layout works in rendered GitHub markdown where images may load slowly, and keeps context visible in raw markdown too |
| **Lessons Learned are analytical, not generic** | Each lesson is grounded in a specific event from *this* lab — no filler statements like "I learned the importance of security" |