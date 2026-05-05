# Threat Hunting PowerShell and Linux Reconnaissance

## Overview
Threat hunting exercise using Wazuh to review command, authentication, and privilege-related activity, with emphasis on what was detected and what visibility gaps remained.

## What I Did
- Generated reconnaissance and privilege-related activity on a Linux system.
- Queried Wazuh logs for command execution and authentication activity.
- Reviewed sudo, PAM session, and failed login activity.
- Checked whether basic reconnaissance commands appeared in the available logs.
- Documented detected activity separately from missing visibility.

## Key Findings
- Successful sudo access to root was visible.
- PAM session activity was observed.
- Failed login attempts were recorded.
- Command-level reconnaissance visibility was limited or inconsistent in the documented export.
- The hunt identified a visibility gap around early-stage reconnaissance activity.

## Security Impact
Privilege activity visibility is useful, but missing reconnaissance telemetry can leave defenders blind during early attacker activity. A SOC team would use this finding to improve audit logging, command monitoring, or endpoint telemetry coverage.

## Tools Used
- Wazuh
- Linux
- Authentication logs
- Command-line activity simulation

## Outcome
This project proves a practical threat hunting workflow: generate activity, search logs, compare detected and missing behavior, and turn the result into a defensible detection-gap finding.
