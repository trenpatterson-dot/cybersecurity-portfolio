# Project Closeout Report

## Project Summary

- Project: `blue-team-labs/windows-failed-login-investigation`
- Lab type: Windows log analysis / SOC triage
- Primary event: Event ID `4625` failed login
- Tool used: Windows Event Viewer
- Closeout type: controlled portfolio pipeline report

This project documents a Windows failed-login investigation using Security log Event ID `4625`. The analysis focuses on identifying failed authentication events, reviewing key fields, and determining whether the activity appeared malicious or benign in the lab context.

## Evidence Captured

- Windows Event Viewer filtered Security log evidence for Event ID `4625`
- Failed-login event detail evidence
- README summary of the triage decision
- Source docs:
  - `docs/investigation.md`
  - `docs/findings.md`
  - `queries/eventviewer-queries.txt`
- Privacy and readiness docs:
  - `docs/orchestrator-remediation-plan.md`
  - `docs/screenshot-privacy-review.md`
  - `docs/github-readiness-report.md`

## Public-Safe Screenshots Used

- `evidence/screenshots-public/01-event-id-4625-public-evidence.png`

The public-safe screenshot is a redacted composite image that preserves the Event ID `4625` investigation context while removing or masking sensitive local account and host details.

## Raw Screenshot Status

Raw screenshots remain local-only:

- `evidence/screenshots/03-event-id-4625-list.png`
- `evidence/screenshots/04-failed-login-details.png`

The raw screenshots should not be linked from the README or committed as public evidence.

## Validator Result

Latest evidence-validator status before this closeout report was created:

- Status: `NEEDS ORGANIZATION`
- Blockers: none
- Remaining warnings:
  - `outputs/` is local-only.
  - `HANDOFF.md` is local-only.
  - LinkedIn drafts under `outputs/` are local-only.

## Privacy Review Result

- Raw screenshot classification: `NEEDS BLUR`
- Public-safe screenshot candidate classification: `OK FOR PUBLIC REVIEW`
- Public-safe recommendation: Use only the screenshot under `evidence/screenshots-public/` for README and portfolio review.

## GitHub Readiness Result

Latest GitHub-readiness status before this closeout report was created:

- Status: `READY FOR REVIEW`
- Blockers: none
- Public-safe file set identified
- Local-only files identified

## Triage Decision

- Severity: Low
- Decision: Benign or simulated local failed-login activity
- Rationale:
  - Event ID `4625` showed failed authentication attempts.
  - Logon Type `2` indicates local interactive login.
  - Source address `::1` indicates localhost.
  - Failed account was `FakeUser`.
  - No successful authentication was documented in the current evidence.

## Files Ready For Human GitHub Review

- `README.md`
- `docs/findings.md`
- `docs/investigation.md`
- `docs/orchestrator-remediation-plan.md`
- `docs/screenshot-privacy-review.md`
- `docs/github-readiness-report.md`
- `docs/project-closeout-report.md`
- `docs/timeline.md`
- `queries/eventviewer-queries.txt`
- `evidence/screenshots-public/01-event-id-4625-public-evidence.png`

## Local-Only Files Excluded

- `HANDOFF.md`
- `outputs/`
- `evidence/screenshots/`
- LinkedIn drafts under `outputs/`

## Lessons Learned

- Event ID `4625` is a core Windows authentication failure signal.
- Logon Type and source address are key context fields for separating local failed login activity from remote attack patterns.
- Raw screenshots often contain local account, host, timestamp, or event record details and need privacy review before GitHub use.
- Public-safe screenshots should be linked from README instead of raw lab evidence.

## Portfolio Value

This lab demonstrates SOC-ready fundamentals:

- Windows Event Viewer navigation
- Event ID `4625` filtering
- Failed-login triage
- Authentication event field interpretation
- Evidence handling and public-safe documentation
- Separating local benign activity from higher-risk remote login patterns

## Remaining Future Improvements

- Optionally expand `docs/timeline.md` in a later approved source-doc cleanup pass.
- Conduct final human review before any git add, commit, push, or publishing action.

## Final Closeout Note

The project is prepared for closeout review once the wrappers confirm no remaining blockers. Human approval is still required before any external action.
