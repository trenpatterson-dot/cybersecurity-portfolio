# Screenshot Privacy Review

## Project

- Project: `blue-team-labs/windows-failed-login-investigation`
- Review type: report-only screenshot privacy review
- Screenshot folder reviewed: `evidence/screenshots/`
- README reviewed: `README.md`
- Supporting docs reviewed:
  - `docs/investigation.md`
  - `docs/findings.md`
  - `queries/eventviewer-queries.txt`
- External actions: none
- Screenshot edits: none
- Git actions: none

## Summary

The project has two raw Windows Event Viewer screenshots. Both are useful evidence for the failed login investigation, but neither should be used publicly as-is. The screenshots expose exact timestamps and local system/account context.

A public-safe composite screenshot now exists under `evidence/screenshots-public/` and is the GitHub candidate image for README use:

- `evidence/screenshots-public/01-event-id-4625-public-evidence.png`

## Screenshot Review

### `03-event-id-4625-list.png`

- Classification: `NEEDS BLUR`
- Evidence value: Shows filtered Windows Security log entries for Event ID `4625` and repeated audit failures.
- Visible concerns:
  - Exact event timestamps are visible in the `Date and Time` column.
  - Event volume and event sequencing are visible.
  - The Event Viewer interface and Security log context are visible.
- Not observed:
  - No visible usernames.
  - No visible hostnames.
  - No visible emails.
  - No visible API keys, tokens, or secrets.
  - No visible customer/private business data.
- Required before GitHub:
  - Blur or crop exact timestamps in the `Date and Time` column.
  - Keep the Event ID and audit-failure context visible if possible.

### `04-failed-login-details.png`

- Classification: `NEEDS BLUR`
- Evidence value: Shows detailed Event ID `4625` fields supporting the README and findings narrative.
- Visible concerns:
  - Local account/security identifier context is visible: `TREN\trenp`.
  - Local account name is visible: `trenp`.
  - Local account domain is visible: `TREN`.
  - Failed account domain is visible: `TREN`.
  - Workstation name is visible: `TREN`.
  - Computer name is visible: `Tren`.
  - Exact logged timestamp is visible.
  - Logon ID and caller process ID are visible.
  - Source network address `::1` is visible; this is localhost and low risk, but it is still part of the event record.
- Not observed:
  - No visible emails.
  - No visible real full names beyond local machine/account naming.
  - No visible tokens, API keys, passwords, or secrets.
  - No visible customer/private business data.
  - No sensitive URL visible.
- Required before GitHub:
  - Blur local username/account identity fields.
  - Blur local domain/workstation/computer names.
  - Blur exact timestamp.
  - Consider blurring Logon ID and caller process ID.
  - Keep public-safe evidence fields visible where possible:
    - Event ID `4625`
    - Logon Type `2`
    - Failure reason
    - Failed account name `FakeUser`, if intentionally simulated and approved
    - Source address `::1`, if approved as localhost evidence
    - Process name `svchost.exe`

## Public-Safe Recommendation

- Do not link the raw screenshots from `README.md`.
- Do not commit the raw screenshots as GitHub evidence.
- Keep originals under `evidence/screenshots/` local-only.
- Use the public-safe screenshot candidate under `evidence/screenshots-public/` for README and portfolio content.
- Only link `README.md` to public-safe files under `evidence/screenshots-public/`.

Current public-safe candidate:

- `01-event-id-4625-public-evidence.png`

## Remaining Blockers

- Raw screenshots are not currently public-safe.
- Raw screenshots should remain ignored/local-only by project-specific `.gitignore` rule.
- `README.md` should reference only public-safe screenshots.
- The project still needs a later GitHub boundary review using the current public-safe screenshot candidate.

## Final Recommendation

Classification for raw screenshot GitHub use: `NEEDS BLUR`

Classification for the public-safe screenshot candidate: `OK FOR PUBLIC REVIEW`

The raw screenshots are usable evidence after privacy cleanup, but they should not be published in their current raw form. The public-safe composite screenshot is the current candidate for GitHub review.
