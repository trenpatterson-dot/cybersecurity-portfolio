# Investigation — Privilege Escalation via Sudo

## Alert Details
- Rule: Successful sudo to ROOT executed
- Rule ID: 5402
- Severity: 3 (Low)
- Agent: tren
- Timestamp: Apr 23, 2026

---

## Event Summary
The system detected repeated execution of privileged commands using sudo. The user escalated privileges to root and executed a command modifying capabilities of a system binary.

---

## Command Observed
`/usr/sbin/setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap`

---

## Breakdown of Activity

### User Activity
- Source user: tren
- Target user: root
- Terminal: pts/0
- Working directory: /home/tren

---

### Command Analysis
The `setcap` command was used to assign capabilities to the `dumpcap` binary.

Capabilities granted:
- `cap_net_raw` → allows raw packet capture
- `cap_net_admin` → allows network administration functions

This allows the binary to capture packets without requiring root privileges during execution.

---

### Behavioral Pattern
- Command executed multiple times (`firedtimes: 6`)
- Occurred within a short timeframe
- Associated with login session activity visible in surrounding PAM events

---

## Timeline (Simplified)
1. User logs in
2. User executes sudo command
3. Capabilities are modified on the binary
4. Session closes
5. Pattern repeats

---

## Analysis

### Legitimate Explanation
- Configuration of Wireshark or packet capture tools
- Preparing the system for network monitoring or analysis

### Suspicious Explanation
- Enabling persistent packet capture capability
- Potential for credential harvesting or traffic sniffing
- Privilege escalation misuse

---

## Analyst Assessment
The activity is consistent with system configuration behavior, but it introduces elevated risk because it modifies what a binary can do at the capability level.

No direct indicators of malware, outbound attacker infrastructure, or confirmed compromise were observed in this event alone. Still, the behavior aligns with techniques that can appear in post-exploitation scenarios.

---

## Conclusion
The event is not inherently malicious, but it should be validated as expected administrative behavior. Additional monitoring is appropriate to ensure the capability is not abused later.

---

## Recommended Next Steps
- Confirm user intent
- Check for installed network analysis tools such as Wireshark
- Monitor for unusual network capture activity
- Review related authentication and process execution logs for additional context