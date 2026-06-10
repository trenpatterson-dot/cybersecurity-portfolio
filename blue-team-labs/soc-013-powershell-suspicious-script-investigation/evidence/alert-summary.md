# PowerShell Alert Summary

Alert Name:
Suspicious PowerShell script execution

Severity:
Medium

Status:
New

Affected Device:
WIN-WS-022

Affected User:
analyst3

Detection Summary:
PowerShell activity was observed with ExecutionPolicy Bypass and a script path from the user's Downloads folder. The command activity included suspicious web request behavior that may indicate attempted payload download or unauthorized script execution.

Initial Assessment:
The activity is suspicious because PowerShell executed with bypass-style arguments and referenced a user-writable location.

Triage Decision:
Escalate for endpoint timeline review, script path validation, command-line analysis, and containment consideration.
