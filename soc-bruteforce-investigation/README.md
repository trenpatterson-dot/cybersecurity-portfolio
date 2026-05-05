# SOC Brute Force Investigation

## Overview
SOC alert investigation of repeated SSH authentication failures in Wazuh, documented as a controlled brute force simulation with no successful login observed.

## What I Did
- Reviewed the Wazuh alert for repeated SSH authentication failures.
- Extracted the source IP, target user, service, and event message.
- Confirmed the activity matched brute force behavior.
- Checked whether any successful authentication occurred.
- Mapped the behavior to MITRE ATT&CK T1110: Brute Force.

## Key Findings
- Total failed attempts: 29.
- Authentication successes: 0.
- Source IP: 127.0.0.1.
- Target user: fakeuser.
- Service: SSH (sshd).
- Event message: maximum authentication attempts exceeded.
- Wazuh rule ID 5758 triggered at level 8.

## Security Impact
Repeated SSH failures can indicate credential access activity. In this case, the local source IP shows a controlled simulation, but the pattern is still useful for SOC practice because it mirrors the kind of authentication behavior analysts must triage quickly.

## Tools Used
- Wazuh
- Linux
- SSH authentication logs
- MITRE ATT&CK

## Outcome
The investigation confirmed brute force behavior in a controlled lab, found no successful login, and documented the alert data needed to explain the risk from a SOC analyst perspective.
