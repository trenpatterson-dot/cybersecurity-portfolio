# Findings

## Summary

Multiple Windows failed-login events were identified in the Security event log using Event ID `4625`.

The evidence supports a low-risk triage decision because the failed login activity was local, used Logon Type `2`, targeted the simulated account `FakeUser`, and did not show successful authentication.

## Key Evidence

- Event ID: `4625`
- Event type: Audit Failure
- Target account: `FakeUser`
- Logon Type: `2` - Interactive
- Failure reason: `Unknown user name or bad password`
- Source network address: `::1` - localhost
- Process: `svchost.exe`
- Successful login observed: No, based on the current README and docs

## Finding 1: Failed Login Events Were Present

The Security log contained multiple Event ID `4625` audit-failure records. This confirms failed authentication activity was captured by Windows logging.

## Finding 2: Activity Was Local

The source address `::1` indicates localhost. Combined with Logon Type `2`, the evidence points to local interactive login attempts rather than remote network or RDP authentication.

## Finding 3: Target Account Was Simulated or Invalid

The failed account shown in the project evidence was `FakeUser`. The failure reason was `Unknown user name or bad password`, which is consistent with an invalid username or bad credential attempt.

## Finding 4: No Compromise Was Documented

The current project evidence does not document a successful login or external access attempt. The activity is therefore assessed as low risk in this lab context.

## Security Assessment

- Risk level: Low
- Triage decision: Benign or simulated local failed-login activity
- Escalation needed: No, based on current evidence

If similar events showed external source addresses, Logon Type `3`, Logon Type `10`, successful authentication, or a high-volume pattern against real accounts, the risk would increase and the event should be triaged as a possible brute-force or credential attack.

## Public Evidence Status

- Public-safe screenshot candidate exists under `evidence/screenshots-public/`.
- Raw screenshots under `evidence/screenshots/` should remain local-only.
- Outputs, HANDOFF files, and LinkedIn drafts should remain local-only.
