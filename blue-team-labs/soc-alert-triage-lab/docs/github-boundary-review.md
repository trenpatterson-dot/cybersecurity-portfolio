# GitHub Boundary Review

## Project

- Project path: `blue-team-labs/soc-alert-triage-lab`
- Review type: report-only GitHub boundary cleanup review
- Review date: 2026-05-07
- Scope inspected: `README.md`, `docs/`, `queries/`, `evidence/screenshots/`, `outputs/`, and `SOC_Triage_HANDOFF.md`

## GitHub-Safe Files

These files are reasonable GitHub candidates after final content and privacy review:

- `README.md`
- `docs/findings.md`
- `docs/investigation.md`
- `queries/investigation-queries.txt`
- `evidence/screenshots/01-wazuh-alert-overview.png`
- `evidence/screenshots/02-failed-login-raw-event.png`
- `evidence/screenshots/03-repeated-failed-logins-filtered.png`
- `evidence/screenshots/04-alert-fields-source-user-host-time.png`
- `evidence/screenshots/04-related-events-timeline.png`
- `evidence/screenshots/05-pam-login-session-details.png`

Important qualifier: the screenshot files are structurally valid evidence, but they still need human privacy review before public GitHub use because visible fields include local host/user context, local Wazuh URLs, timestamps, private lab IP context, and command/session details.

## Local-Only Files

These files and folders should stay local-only unless Tren explicitly approves a separate publishing review:

- `SOC_Triage_HANDOFF.md`
- `outputs/`
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

The LinkedIn drafts inside `outputs/` are currently ignored:

- `outputs/20260421_225032/linkedin-post.md`
- `outputs/20260421_225032/linkedin.md`
- `outputs/20260421_232119/linkedin-post.md`
- `outputs/20260421_232119/linkedin.md`

Accidental commit risk: normal `git add` should not add these ignored files, but `git add -f` or manually changing `.gitignore` could still force them into Git. Keep them out of staging.

## Evidence Status

- Evidence folder exists: yes
- Screenshot folder exists: yes
- Screenshot files exist: yes
- Screenshot image headers are valid according to the evidence validator: yes
- README references all six local screenshot files: yes
- README image references are valid: yes
- Missing README image references: none
- Secret-like files found by validator: none
- Validator status: `NEEDS ORGANIZATION`

The validator status remains `NEEDS ORGANIZATION` because local-only artifacts are still present inside the project path: `outputs/`, LinkedIn drafts under `outputs/`, and `SOC_Triage_HANDOFF.md`.

## Screenshot Privacy Review Status

Needs human privacy review before GitHub publishing.

Observed review notes:

- `01-wazuh-alert-overview.png` shows Wazuh dashboard context, local browser URL, manager/agent name `tren`, and authentication metrics.
- `02-failed-login-raw-event.png` shows raw event details, local host/user context, rule IDs, timestamps, and private lab IP context.
- `03-repeated-failed-logins-filtered.png` shows Wazuh event rows, timestamps, agent name `tren`, failed login rule details, and rule IDs.
- `04-alert-fields-source-user-host-time.png` shows dashboard metrics and host/agent context.
- `04-related-events-timeline.png` shows detailed event fields, local user/host context, UID values, sudo/pkexec activity, command path details, and timestamps.
- `05-pam-login-session-details.png` shows PAM session details, root session context, local user/host context, rule and compliance fields, and timestamps.

No obvious secrets or credentials were identified by filename or validator output, but the screenshots include enough local lab identifiers to require a deliberate public-safety decision.

## README Status

- README is evidence-linked and references all six screenshots with relative paths.
- README excludes `outputs/`, `SOC_Triage_HANDOFF.md`, and LinkedIn drafts from the evidence narrative.
- README is more recruiter-readable than the earlier version.
- README should not be considered GitHub-ready until screenshot privacy review and source-doc consistency cleanup are complete.

Content consistency notes:

- `docs/findings.md` describes a systemd service failure and related PAM/sudo context.
- `SOC_Triage_HANDOFF.md` describes repeated failed SSH login attempts and should remain local-only because it conflicts with the current README/findings narrative.
- `docs/investigation.md` still contains blank alert-summary fields and a stale screenshot list that does not match the current screenshot filenames.
- `queries/investigation-queries.txt` exists but appears empty, so it should either be populated with real queries used or removed from public README references in a later cleanup pass.

## `.gitignore` Coverage

Confirmed by `git check-ignore -v`:

- `blue-team-labs/soc-alert-triage-lab/outputs` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_225032/linkedin-post.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_225032/linkedin.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_232119/linkedin-post.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_232119/linkedin.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/20260421_225032/github-update.md` is ignored by `.gitignore:42:outputs/`
- `blue-team-labs/soc-alert-triage-lab/SOC_Triage_HANDOFF.md` is ignored by `.gitignore:27:**/*HANDOFF*.md`

Tracked-file check:

- `git ls-files -- blue-team-labs/soc-alert-triage-lab` returned only `blue-team-labs/soc-alert-triage-lab/README.md`.
- No ignored local-only files are currently tracked.

## Files That Need Privacy Review

- `evidence/screenshots/01-wazuh-alert-overview.png`
- `evidence/screenshots/02-failed-login-raw-event.png`
- `evidence/screenshots/03-repeated-failed-logins-filtered.png`
- `evidence/screenshots/04-alert-fields-source-user-host-time.png`
- `evidence/screenshots/04-related-events-timeline.png`
- `evidence/screenshots/05-pam-login-session-details.png`

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

- Screenshot privacy review is still required before GitHub/public use.
- `docs/investigation.md` contains blank fields and stale screenshot names.
- `queries/investigation-queries.txt` appears empty.
- `SOC_Triage_HANDOFF.md` conflicts with the current README/findings narrative and must remain local-only.
- `outputs/` contains generated and LinkedIn draft artifacts that should stay ignored and out of README.
- Evidence validator still returns `NEEDS ORGANIZATION` due to local-only artifacts inside the project path.

## Recommended Next Action

Do not run GitHub readiness yet.

Recommended next safe cleanup pass:

1. Update `docs/investigation.md` so it matches the final README, real screenshot filenames, and documented findings.
2. Decide whether `queries/investigation-queries.txt` should be populated with real Wazuh queries used or removed from the README support links.
3. Complete human screenshot privacy review for all six screenshots.
4. Keep `outputs/` and `SOC_Triage_HANDOFF.md` local-only and ignored.
5. Rerun the evidence validator after the docs cleanup.
