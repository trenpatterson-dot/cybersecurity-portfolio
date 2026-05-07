# Project Closeout Report

## Project

- Project name: SOC Alert Triage Lab
- Project path: `blue-team-labs/soc-alert-triage-lab`
- Closeout date: 2026-05-07
- GitHub status: pushed successfully before this closeout report
- Confirming evidence: local Git history shows commit `218c29c` as `HEAD -> main, origin/main`
- Commit message: `Add public-safe SOC alert triage lab`

Note: This closeout report was created after the successful push and is not included in commit `218c29c`.

## Project Summary

This lab documents a blue-team SOC alert triage workflow using Wazuh. The investigation reviewed alert details, raw event context, related authentication activity, PAM session context, sudo/pkexec-related activity, and supporting Wazuh timeline evidence.

The documented triage decision was **Monitor / Informational**. The final README presents the lab as a recruiter-readable portfolio project while keeping generated outputs, handoff notes, LinkedIn drafts, and raw screenshots local-only.

## Evidence Captured

Evidence captured and documented for the public lab package:

- README narrative describing objective, workflow, key findings, triage decision, and skills demonstrated
- Investigation notes in `docs/investigation.md`
- Findings summary in `docs/findings.md`
- Wazuh investigation terms in `queries/investigation-queries.txt`
- Boundary review in `docs/github-boundary-review.md`
- Screenshot privacy review in `docs/screenshot-privacy-review.md`
- GitHub readiness review in `docs/github-readiness-report.md`
- Public-safe screenshot copies under `evidence/screenshots-public/`

The original raw screenshots remain in `evidence/screenshots/` and are treated as local-only.

## Public-Safe Screenshots Used

The README links to these public-safe screenshot files:

- `evidence/screenshots-public/01-wazuh-alert-overview-public.png`
- `evidence/screenshots-public/02-failed-login-raw-event-public.png`
- `evidence/screenshots-public/03-repeated-failed-logins-filtered-public.png`
- `evidence/screenshots-public/04-alert-fields-source-user-host-time-public.png`
- `evidence/screenshots-public/04-related-events-timeline-public.png`
- `evidence/screenshots-public/05-pam-login-session-details-public.png`

These public-safe copies are the GitHub candidate images. The original screenshots under `evidence/screenshots/` are ignored and local-only.

## Validator Result

Latest evidence-validator result:

- Final status: `NEEDS ORGANIZATION`
- Blockers: none
- Secret-like files found: none
- Missing README image references: none
- Valid README image references: all six public-safe screenshot links

The status remains `NEEDS ORGANIZATION` because local-only artifacts are still present inside the project path:

- LinkedIn drafts under `outputs/`
- Generated output folders under `outputs/`
- `SOC_Triage_HANDOFF.md`

Those artifacts are intentionally ignored/local-only and do not block human GitHub review.

## Privacy Review Result

Privacy review result:

- Original raw screenshots: local-only
- Public-safe screenshot copies: GitHub candidate images
- README now links to `evidence/screenshots-public/`
- No visible tokens, API keys, passwords, emails, or customer data were identified in the documented review
- Raw screenshots exposed local Wazuh URLs, usernames/hostnames, private lab IP context, timestamps, and detailed event fields, so they were excluded from normal Git staging

Boundary cleanup completed:

- `.gitignore` now ignores `blue-team-labs/soc-alert-triage-lab/evidence/screenshots/`
- `evidence/screenshots-public/` is not ignored

## GitHub Readiness Result

Final readiness result:

- Status: `READY FOR REVIEW`
- Human approval required before future `git add`, commit, or push
- No current blockers for report-only GitHub review
- No credentialed Git remote was observed; `origin` uses `https://github.com/trenpatterson-dot/cybersecurity-portfolio.git`

The readiness report confirms:

- README links to public-safe screenshots
- Public screenshot files exist and are not ignored
- Raw screenshots are ignored
- `outputs/` is ignored
- `SOC_Triage_HANDOFF.md` is ignored
- LinkedIn drafts are ignored/local-only
- Docs and queries are public-safe candidates
- No `.env` or `.env.*` files were found under the lab path
- Evidence validator has no blockers

## Files Committed

Commit `218c29c` included the public-safe lab package:

- `.gitignore`
- `blue-team-labs/soc-alert-triage-lab/README.md`
- `blue-team-labs/soc-alert-triage-lab/docs/findings.md`
- `blue-team-labs/soc-alert-triage-lab/docs/github-boundary-review.md`
- `blue-team-labs/soc-alert-triage-lab/docs/github-readiness-report.md`
- `blue-team-labs/soc-alert-triage-lab/docs/investigation.md`
- `blue-team-labs/soc-alert-triage-lab/docs/screenshot-privacy-review.md`
- `blue-team-labs/soc-alert-triage-lab/queries/investigation-queries.txt`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots-public/01-wazuh-alert-overview-public.png`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots-public/02-failed-login-raw-event-public.png`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots-public/03-repeated-failed-logins-filtered-public.png`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots-public/04-alert-fields-source-user-host-time-public.png`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots-public/04-related-events-timeline-public.png`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots-public/05-pam-login-session-details-public.png`

This closeout report is a follow-up artifact and was not part of that commit.

## Local-Only Files Excluded

These files and folders were intentionally kept local-only:

- `blue-team-labs/soc-alert-triage-lab/SOC_Triage_HANDOFF.md`
- `blue-team-labs/soc-alert-triage-lab/outputs/`
- `blue-team-labs/soc-alert-triage-lab/outputs/**`
- `blue-team-labs/soc-alert-triage-lab/outputs/**/linkedin-post.md`
- `blue-team-labs/soc-alert-triage-lab/outputs/**/linkedin.md`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots/`
- `blue-team-labs/soc-alert-triage-lab/evidence/screenshots/*.png`

Reason for exclusion:

- `outputs/` contains generated drafts, QA outputs, JSON run data, and LinkedIn/OneNote-oriented content.
- `SOC_Triage_HANDOFF.md` is an operator handoff artifact and does not match the final public README narrative.
- Raw screenshots contain local lab identifiers and detailed event context that should not be published as-is.

## Lessons Learned

- Screenshot filenames can contain cybersecurity terms such as login, session, PAM, SSH, sudo, user, host, auth, and IP without being secret files.
- Evidence validation should separate path-based checks from visual privacy review.
- Public portfolio evidence needs a clean split between raw artifacts and public-safe copies.
- `git add .` is too risky for this workflow because public evidence and local-only artifacts can live near each other.
- README quality improves when it is anchored to verified docs, screenshots, and validator output instead of generated drafts.
- Generated outputs and LinkedIn drafts should remain local-only even when they are useful for review.

## Portfolio Value

This lab adds a strong SOC/blue-team portfolio example because it demonstrates:

- Wazuh alert triage
- Authentication event review
- PAM and sudo/pkexec context analysis
- Timeline correlation
- MITRE ATT&CK awareness
- Evidence organization
- Privacy review and public-safe documentation discipline
- GitHub boundary control for cybersecurity artifacts

It shows not only the technical investigation but also the professional workflow needed to prepare security evidence for public portfolio use.

## Remaining Future Improvements

Future improvements that do not block the current GitHub review:

- Add a short visual evidence index that maps each screenshot to the investigation step it supports.
- Add a brief architecture/environment note explaining the Wazuh lab setup at a high level without exposing private details.
- Add sanitized query examples in a more structured format if this lab becomes a reusable playbook.
- Add a final human-review checklist before any future public refresh.
- Consider moving local-only artifacts out of the public lab tree in a separate approved cleanup pass.

## Closeout Status

- Controlled pipeline completed: yes
- Evidence validation completed: yes
- Screenshot privacy review completed: yes
- Public-safe screenshot relink completed: yes
- GitHub boundary cleanup completed: yes
- GitHub readiness review completed: yes
- Commit completed: yes
- Push completed: yes, based on local Git refs showing `218c29c` at both `HEAD -> main` and `origin/main`
- Further publish actions needed: no
- Future changes require human approval: yes
