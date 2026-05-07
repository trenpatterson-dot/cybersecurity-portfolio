# Project Closeout Wrapper

Read-only local wrapper for deciding whether a portfolio lab or project is ready for final closeout review.

The wrapper is report-only by default. It does not stage, commit, push, move, delete, rename, publish, call external services, run live scans, or read secret-like file contents.

## Usage

```cmd
python tools\project-closeout\project_closeout.py --project-path blue-team-labs\soc-alert-triage-lab
```

JSON output:

```cmd
python tools\project-closeout\project_closeout.py --project-path blue-team-labs\soc-alert-triage-lab --json
```

Optional report inputs:

```cmd
python tools\project-closeout\project_closeout.py --project-path blue-team-labs\soc-alert-triage-lab --github-readiness-report docs\github-readiness-report.md --evidence-report docs\evidence-validation-report.md
```

## Checks

- README exists
- docs/ exists
- queries/ exists
- public screenshots exist
- raw screenshots are ignored or local-only
- outputs, HANDOFF files, and LinkedIn drafts are local-only
- evidence-validator status if available
- GitHub readiness wrapper status if available
- project-closeout-report.md exists or is recommended
- project-scoped git status
- secret-like files by filename only

## Decision Statuses

- `CLOSEOUT READY`
- `NEEDS WORK`
- `SECURITY BLOCKED`
- `GITHUB BLOCKED`
- `EVIDENCE BLOCKED`
- `KEEP LOCAL ONLY`

`CLOSEOUT READY` still requires human approval before git actions, publishing, LinkedIn posting, or Notion updates.
