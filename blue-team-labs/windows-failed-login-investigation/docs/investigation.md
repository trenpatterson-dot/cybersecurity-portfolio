# Investigation

## Alert Type

Windows failed login activity in the Security event log.

## Event Source

- Tool: Windows Event Viewer
- Log: Security
- Event ID: `4625`
- Event meaning: An account failed to log on
- Event type: Audit Failure

## Objective

Review Windows Security log failures to determine whether the activity appeared to be remote malicious access, local testing, or benign failed authentication.

## Workflow

1. Opened Windows Event Viewer.
2. Navigated to Windows Logs > Security.
3. Filtered the Security log for Event ID `4625`.
4. Reviewed the repeated failed-login events.
5. Opened a failed-login event detail record.
6. Compared the logon type, target account, source address, failure reason, and process details.
7. Assessed whether the activity showed signs of successful compromise or remote access.

## Evidence Observed

- Multiple Event ID `4625` audit-failure records were present.
- The failed account shown in the README evidence was `FakeUser`.
- Logon Type was `2`, which indicates an interactive local login attempt.
- Failure reason was `Unknown user name or bad password`.
- Source network address was `::1`, which indicates localhost.
- Process shown in the event details was `svchost.exe`.
- No successful login was documented in the project evidence.

## Analysis

The activity matched repeated failed authentication attempts against a non-existent or invalid account. The source address and logon type point to local activity rather than a remote brute-force attempt.

Because the activity used Logon Type `2` and localhost as the source address, the evidence supports the README assessment that this was low-risk local or simulated failed-login behavior rather than confirmed external compromise.

## Triage Decision

- Severity: Low
- Decision: Benign or simulated local failed-login activity
- Rationale: No successful authentication was observed, the source was localhost, and the logon type was interactive local login rather than remote/network login.

## Evidence Handling Notes

- Raw screenshots under `evidence/screenshots/` remain local-only.
- The README uses the public-safe screenshot under `evidence/screenshots-public/`.
- Generated outputs, HANDOFF files, and LinkedIn drafts remain local-only.
