# GitHub Boundary Review

## Project

- Project path: `blue-team-labs/soc-alert-triage-lab`
- Review type: report-only GitHub boundary review
- Review date: 2026-05-17
- Current status: GitHub pin candidate after final human screenshot redaction review
- Scope inspected: `README.md`, `docs/`, `queries/`, `evidence/screenshots-public/`, local-only raw screenshot boundary, generated outputs boundary, and `SOC_Triage_HANDOFF.md` ignore boundary

## GitHub-Safe Files

These files are reasonable GitHub candidates after final human review:

- `README.md`
- `docs/findings.md`
- `docs/investigation.md`
- `docs/github-boundary-review.md`
- `docs/github-readiness-report.md`
- `docs/screenshot-privacy-review.md`
- `queries/investigation-queries.txt`
- `evidence/screenshots-public/01-wazuh-alert-overview-public.png`
- `evidence/screenshots-public/02-failed-login-raw-event-public.png`
- `evidence/screenshots-public/03-repeated-failed-logins-filtered-public.png`
- `evidence/screenshots-public/04-alert-fields-source-user-host-time-public.png`
- `evidence/screenshots-public/04-related-events-timeline-public.png`
- `evidence/screenshots-public/05-pam-login-session-details-public.png`

Important qualifier: the public screenshot copies are the only screenshot candidates for GitHub. They still need final human privacy review before hard-pinning because some local lab identifiers and event details may remain visible.

## Local-Only Files

These files and folders should stay local-only unless Tren explicitly approves a separate publishing review:

- `SOC_Triage_HANDOFF.md`
- `outputs/`
- `evidence/screenshots/`
- `evidence/screenshots/01-wazuh-alert-overview.png`
- `evidence/screenshots/02-failed-login-raw-event.png`
- `evidence/screenshots/03-repeated-failed-logins-filtered.png`
- `evidence/screenshots/04-alert-fields-source-user-host-time.png`
- `evidence/screenshots/04-related-events-timeline.png`
- `evidence/screenshots/05-pam-login-session-details.png`
- `outputs/20260421_140818/evidence.json`
- `outputs/20260421_140818/intake.json`
- `outputs/20260421_225032/eli10.md`
- `outputs/20260421_225032/evidence.json`
- `outputs/20260421_225032/github-update.md`
- `outputs/20260421_225032/intake.json`
- `outputs/20260421_225032/linkedin-post.md`
- `outputs/20260421_225032/linkedin.md`
- `outputs/20260421_225032/onenote-notes.md`
- `outputs/20260421_225032/onenote.md`
- `outputs/20260421_225032/qa_report_attempt1.json`
- `outputs/20260421_225032/qa_report_attempt2.json`
- `outputs/20260421_225032/qa_report_attempt3.json`
- `outputs/20260421_225032/readme.md`
- `outputs/20260421_225032/run_metadata.json`
- `outputs/20260421_225032/technical-summary.md`
- `outputs/20260421_225032/technical.md`
- `outputs/20260421_232119/eli10.md`
- `outputs/20260421_232119/evidence.json`
- `outputs/20260421_232119/github-update.md`
- `outputs/20260421_232119/intake.json`
- `outputs/20260421_232119/linkedin-post.md`
- `outputs/20260421_232119/linkedin.md`
- `outputs/20260421_232119/onenote-notes.md`
- `outputs/20260421_232119/onenote.md`
- `outputs/20260421_232119/qa_report_attempt1.json`
- `outputs/20260421_232119/readme.md`
- `outputs/20260421_232119/run_metadata.json`
- `outputs/20260421_232119/technical-summary.md`
- `outputs/20260421_232119/technical.md`

## Files That Should Be Excluded By `.gitignore`

Current `.gitignore` coverage should exclude:

- `outputs/` by `.gitignore` rule `outputs/`
- All nested files under `outputs/`, including generated markdown, JSON, QA reports, and LinkedIn drafts
- `SOC_Triage_HANDOFF.md` by `.gitignore` rule `**/*HANDOFF*.md`
- Raw screenshots under `evidence/screenshots/` by the project-specific raw screenshot ignore rule

The LinkedIn drafts inside `outputs/` are currently ignored:

- `outputs/20260421_225032/linkedin-post.md`
- `outputs/20260421_225032/linkedin.md`
- `outputs/20260421_232119/linkedin-post.md`
- `outputs/20260421_232119/linkedin.md`

Accidental commit risk: normal `git add` should not add these ignored files, but `git add -f` or manually changing `.gitignore` could still force them into Git. Keep them out of staging.

## Evidence Status

- Evidence folder exists: yes
- Public screenshot folder exists: yes
- Public screenshot files exist: yes
- Raw screenshot folder exists and remains local-only: yes
- Screenshot image headers are valid according to the evidence validator: yes
- README references all six public screenshot files: yes
- README image references are valid: yes
- Missing README image references: none
- Secret-like files found by validator: none
- Validator status: `NEEDS ORGANIZATION`

The validator status remains `NEEDS ORGANIZATION` because local-only artifacts are still present inside the project path: `outputs/`, LinkedIn drafts under `outputs/`, and `SOC_Triage_HANDOFF.md`.

## Screenshot Privacy Review Status

Final human privacy review is still required before GitHub publishing or hard-pinning.

Observed review notes:

- Raw screenshots under `evidence/screenshots/` expose local lab context and should stay local-only.
- Public screenshot copies under `evidence/screenshots-public/` are improved GitHub candidates, but they still need final human review for local identifiers, timestamps, event IDs, private lab IP context, and detailed event fields.

No obvious secrets or credentials were identified by filename or validator output, but the screenshots include enough local lab identifiers to require a deliberate public-safety decision.

## README Status

- README is evidence-linked and references all six screenshots with relative paths.
- README excludes `outputs/`, `SOC_Triage_HANDOFF.md`, and LinkedIn drafts from the evidence narrative.
- README is more recruiter-readable than the earlier version.
- README should be considered ready for human GitHub review, with final screenshot redaction review still required before hard-pinning.

Content consistency notes:

- `docs/findings.md` describes a systemd service failure and related PAM/sudo context.
- `SOC_Triage_HANDOFF.md` describes repeated failed SSH login attempts and should remain local-only because it conflicts with the current README/findings narrative.
- `docs/investigation.md` now aligns with the current service-failure and authentication-context narrative.
- `queries/investigation-queries.txt` contains Wazuh investigation terms used for this lab and should remain evidence-bound.

## `.gitignore` Coverage

Confirmed by `git check-ignore -v`:

- `blue-team-labs/soc-alert-triage-lab/outputs` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_225032/linkedin-post.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_225032/linkedin.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_232119/linkedin-post.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_232119/linkedin.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_225032/github-update.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/SOC_Triage_HANDOFF.md` is ignored by `.gitignore:27:**/*HANDOFF*.md`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots/` is ignored by the project-specific raw screenshot ignore rule

Tracked-file check:

- Safe project docs, public screenshots, and query notes are tracked or safe candidates.
- Ignored local-only raw screenshots, generated outputs, and HANDOFF files should remain out of staging.

## Screenshot Files That Need Final Human Review

- `evidence/screenshots-public/01-wazuh-alert-overview-public.png`
- `evidence/screenshots-public/02-failed-login-raw-event-public.png`
- `evidence/screenshots-public/03-repeated-failed-logins-filtered-public.png`
- `evidence/screenshots-public/04-alert-fields-source-user-host-time-public.png`
- `evidence/screenshots-public/04-related-events-timeline-public.png`
- `evidence/screenshots-public/05-pam-login-session-details-public.png`

Raw screenshots under `evidence/screenshots/` should remain local-only and are not GitHub candidates.

## Files That Should Stay Out Of README

- `SOC_Triage_HANDOFF.md`
- `outputs/`
- `outputs/**`
- `outputs/**/linkedin-post.md`
- `outputs/**/linkedin.md`
- `outputs/**/onenote*.md`
- `outputs/**/qa_report*.json`
- `outputs/**/run_metadata.json`
- `outputs/**/intake.json`
- `outputs/**/evidence.json`
- Generated `outputs/**/readme.md`, `technical*.md`, `github-update.md`, and `eli10.md` files unless a separate cleanup pass promotes specific wording into the real README after review.

## Remaining Blockers

- No blocker prevents human GitHub review.
- Final human screenshot redaction review is still required before hard-pinning this project.
- `SOC_Triage_HANDOFF.md` remains local-only and should not be used as public source material.
- `outputs/` contains generated and LinkedIn draft artifacts that should stay ignored and out of README.
- Evidence validator may still return `NEEDS ORGANIZATION` because local-only artifacts exist inside the project path.

## Recommended Next Action

Proceed to final human review for GitHub pinning.

Recommended next safe steps:

1. Complete final human privacy review of `evidence/screenshots-public/`.
2. If needed, replace only the public screenshot copies, not the raw screenshots.
3. Keep `outputs/`, `SOC_Triage_HANDOFF.md`, and `evidence/screenshots/` local-only and ignored.
4. Use explicit file-path staging only after approval; do not use `git add .`.
