# SOC Alert Investigation: Privilege Escalation via Sudo

## Overview
End-to-end SOC alert investigation in Wazuh focused on Linux sudo activity, privilege escalation context, and risk-based analyst decision-making.

## What I Did
- Reviewed Wazuh events instead of relying only on alert severity.
- Pivoted from dashboard review into raw event details.
- Investigated repeated sudo activity tied to privilege escalation.
- Examined the exact command, user, target account, terminal, and working directory.
- Assessed whether the behavior looked legitimate, suspicious, or required validation.

## Key Findings
- A lab user executed sudo activity that assigned network capture capabilities to `dumpcap`.
- The command modified binary capabilities for packet capture use.
- The activity involved privilege escalation from user context to root-level action.
- No direct malicious indicator was documented in the available evidence.
- The behavior could be legitimate Wireshark setup, but it still deserves validation and monitoring.

## Security Impact
Granting packet capture capabilities can be legitimate for network analysis, but it can also support credential capture or unauthorized traffic inspection if abused. A SOC analyst should validate intent, monitor related activity, and document the risk clearly.

## Tools Used
- Wazuh
- Ubuntu Linux VM
- Linux authentication and sudo logs
- Wazuh Threat Hunting Events view

## Outcome
The project demonstrates end-to-end SOC reasoning: investigate the event, interpret Linux command behavior, avoid overstating the evidence, and produce a low-to-medium risk decision with clear follow-up actions.
