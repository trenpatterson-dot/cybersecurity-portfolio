# GitHub Readiness Wrapper

Read-only local wrapper for deciding whether a project appears ready for human GitHub review.

The wrapper is report-only by default. It does not stage, commit, push, move, delete, rename, publish, run live scans, call external services, or read `.env` / secret-like file contents.

## Usage

Markdown output:

```cmd
python tools\github-readiness\github_readiness.py --project-path blue-team-labs\soc-alert-triage-lab
```

JSON output:

```cmd
python tools\github-readiness\github_readiness.py --project-path blue-team-labs\soc-alert-triage-lab --json
```

Optional security report:

```cmd
python tools\github-readiness\github_readiness.py --project-path blue-team-labs\soc-alert-triage-lab --security-report docs\security-review.md
```

## Checks

- README exists and has image references that resolve locally.
- README screenshots point to public-safe screenshot files when screenshots are used.
- Public screenshots exist and are not ignored.
- Raw screenshots are ignored or local-only.
- `outputs/`, HANDOFF files, and LinkedIn drafts are ignored or local-only.
- `docs/` and `queries/` exist.
- Secret-like filenames are reported by path only; contents are not read.
- Git remote URLs are checked for embedded credentials.
- Project-scoped `git status --short` is captured.
- Existing `tools\evidence-validator\evidence_validator.py` is run in JSON mode when available.

## Decision Statuses

- `READY FOR REVIEW`
- `NEEDS FIXES`
- `BLOCKED`
- `DO NOT PUBLISH`

Human approval is still required before any Git staging, commit, push, or publishing action.
