# SOC Alert Triage Investigation

## Objective

Investigate a Wazuh alert and determine whether the event required escalation, additional monitoring, or no immediate response. The investigation focused on alert details, related timeline activity, authentication context, and whether the available evidence showed signs of compromise.

## Alert Summary

- Alert source: Wazuh alert data from local Linux system logs / journald context
- Alert name/rule: Systemd service failure event with related authentication context
- Severity: Wazuh level 5 event documented in findings
- Host context: Wazuh manager host shown in the available screenshots
- User context: Local `tren` user context and related root session activity shown in the available screenshots
- Source context: Local lab event context shown in Wazuh fields and timeline screenshots
- Destination context: Local Wazuh-monitored host context shown in Wazuh fields
- Timestamp context: Event timestamps are visible in the Wazuh screenshots

## Investigation Steps

1. Reviewed the Wazuh alert overview.
2. Opened the raw event details.
3. Checked affected host, user, source context, and alert fields.
4. Reviewed related events and timeline activity.
5. Correlated surrounding authentication and PAM events.
6. Investigated successful local login session activity tied to `pkexec` and sudo-related events.
7. Determined whether the systemd failure appeared isolated or related to broader suspicious activity.
8. Documented the triage decision and supporting evidence.

## Findings

- Wazuh detected a level 5 event tied to a local systemd service failure.
- The event originated from local journald logs on the Wazuh manager host.
- The affected service was `xdg-permission-store.service`.
- The service exited with `status=1/FAILURE`.
- Related PAM login session events showed successful local authentication activity for the root account initiated by the `tren` user account.
- MITRE ATT&CK mappings included Valid Accounts (T1078) and privilege escalation-related tactics.
- No evidence of authentication abuse, malicious persistence, or remote compromise was identified from the documented event alone.
- The observed activity appeared consistent with expected administrative behavior during local system usage.

## Triage Decision

- Decision: Monitor / Informational
- Reason: The documented event indicates a local service failure rather than clear malicious activity. Related authentication and sudo activity was reviewed, but the available notes did not identify direct evidence of compromise. Continued monitoring is appropriate in case similar service failures, authentication events, or privilege-related activity repeat.

## Screenshots Captured

- `01-wazuh-alert-overview.png`
- `02-failed-login-raw-event.png`
- `03-repeated-failed-logins-filtered.png`
- `04-alert-fields-source-user-host-time.png`
- `04-related-events-timeline.png`
- `05-pam-login-session-details.png`
