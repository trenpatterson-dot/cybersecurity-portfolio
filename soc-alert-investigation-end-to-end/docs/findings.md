# Findings — Privilege Escalation via Sudo

## Finding Title
Repeated privileged command execution involving modification of binary capabilities

## Summary
Wazuh detected repeated sudo activity where the user `tren` executed a command as `root` to assign packet capture-related capabilities to the `dumpcap` binary.

## Evidence
- Rule description: Successful sudo to ROOT executed
- Rule ID: 5402
- Rule level: 3
- User context:
  - source user: tren
  - destination user: root
- Command observed:
  - `/usr/sbin/setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap`
- Repeated activity:
  - `rule.firedtimes = 6`

## Why It Matters
This behavior may be legitimate if the system owner is configuring Wireshark or packet capture tooling. It can also be risky because assigning network capture capabilities to a binary can support unauthorized sniffing or credential capture if abused.

## Risk
Low to Medium

## Analyst Assessment
At the time of review, there was no direct evidence of malware, external attacker activity, or clear malicious intent. However, the behavior represents privilege use that should be validated because it changes what a local binary is allowed to do.

## Recommendation
- Validate whether this activity was expected administrative behavior
- Confirm whether Wireshark or another packet capture tool was being configured
- Continue monitoring for repeated privilege escalation or suspicious network capture activity
- Review related authentication and process execution logs for added context