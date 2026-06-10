# Defender Alert Summary

Alert Name:
Suspicious PowerShell command line

Severity:
Medium

Status:
New

Affected Device:
WIN-WS-014

Affected User:
analyst3

Detection Summary:
Microsoft Defender for Endpoint-style telemetry identified PowerShell execution with an encoded command argument. The parent process was winword.exe, which may indicate suspicious script execution from an Office document.

Initial Assessment:
The activity is suspicious because Office applications should not normally launch encoded PowerShell commands during standard user activity.

Triage Decision:
Escalate for endpoint timeline review, command-line analysis, and containment consideration.
