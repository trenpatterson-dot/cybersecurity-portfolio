# Threat Hunting Wazuh Brute Force Detection

## Overview
Wazuh threat hunting workflow focused on identifying repeated SSH login failures and correlating them into a brute force pattern.

## What I Did
- Opened the Wazuh Events view for threat hunting.
- Searched authentication activity for repeated SSH failures.
- Reviewed repeated failed login behavior from the same user and source IP.
- Compared event timing to determine whether the behavior suggested automation.
- Documented the brute force pattern and mapped it to MITRE ATT&CK T1110.

## Key Findings
- Repeated failed SSH login attempts were observed.
- The same user and source IP were involved in the documented failed attempts.
- The timing between attempts supported a brute force pattern.
- The project shows pattern recognition across events, not just single-alert review.

## Security Impact
Brute force behavior can lead to unauthorized access if credentials are guessed successfully. Detecting repeated authentication failures early gives defenders a chance to block the source, protect accounts, and validate whether any login succeeded.

## Tools Used
- Wazuh
- Ubuntu Linux VM
- SSH authentication logs
- MITRE ATT&CK

## Outcome
The documented workflow identified a brute force pattern in Wazuh and produced a clear SOC-style explanation of the risk and investigation path.
