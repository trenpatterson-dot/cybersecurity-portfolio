# Orchestrator Remediation Plan

## Project

- Project: `blue-team-labs/windows-failed-login-investigation`
- Review type: report-only controlled portfolio pipeline preparation
- Current status: `READY FOR REVIEW`
- External actions: none
- Git actions: none

## Current Pipeline Status

- GitHub-readiness wrapper status: `READY FOR REVIEW`
- Evidence-validator status: `NEEDS ORGANIZATION`
- Project closeout report: present
- Public-safe screenshot: present
- README screenshot reference: valid
- Raw screenshots: local-only

The project is no longer blocked for human GitHub review. The remaining evidence-validator warning is organizational: local-only artifacts still exist inside the project path, and those files must stay out of staging.

## Current Public-Safe Files

These files are candidates for human GitHub review:

- `README.md`
- `docs/findings.md`
- `docs/investigation.md`
- `docs/github-readiness-report.md`
- `docs/orchestrator-remediation-plan.md`
- `docs/project-closeout-report.md`
- `docs/screenshot-privacy-review.md`
- `docs/timeline.md`
- `queries/eventviewer-queries.txt`
- `evidence/screenshots-public/01-event-id-4625-public-evidence.png`

## Local-Only Files

These files and folders should stay local-only unless a later human review explicitly approves otherwise:

- `HANDOFF.md`
- `outputs/`
- LinkedIn drafts under `outputs/`
- `evidence/screenshots/`
- `evidence/screenshots/03-event-id-4625-list.png`
- `evidence/screenshots/04-failed-login-details.png`

## Evidence Boundary

README should reference only:

- `evidence/screenshots-public/01-event-id-4625-public-evidence.png`

README should not reference:

- raw screenshots under `evidence/screenshots/`
- generated outputs
- HANDOFF files
- LinkedIn drafts

## Remaining Human Review

Before publishing or pinning:

1. Confirm the public-safe screenshot redactions are acceptable.
2. Confirm the README stays evidence-bound to Event ID `4625`, Logon Type `2`, `FakeUser`, `::1`, `svchost.exe`, and the low-risk local/simulated triage decision.
3. Use explicit file paths for any future staging; do not use `git add .`.
4. Keep `HANDOFF.md`, `outputs/`, raw screenshots, and LinkedIn drafts out of GitHub.

## Recommended Next Action

Proceed to human review for GitHub publication readiness. No further remediation is required before review unless Tren wants additional wording polish.
