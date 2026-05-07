# Evidence Validator

The Evidence Validator is a safe, report-only checker for local lab and project folders. It helps decide whether a project has real usable evidence and screenshots before README polish, GitHub readiness, supervisor-agent closeout, LinkedIn drafting, or OneNote notes.

It is based on `agent-team-planning/EVIDENCE-SCREENSHOT-VALIDATOR.md`.

## Safe Behavior

- Reads only local, non-secret project files needed for reporting.
- Outputs markdown by default.
- Outputs JSON with `--json`.
- Lists secret-like files by relative path only.
- Does not open `.env`, credential-like files, token files, databases, or private config files.
- Does not move, rename, delete, edit, stage, commit, push, publish, deploy, email, post, call Notion, scan live targets, or invent evidence.

## CMD Usage

```cmd
python tools\evidence-validator\evidence_validator.py --project-path tools\noc-dashboard
```

Use an explicit README path:

```cmd
python tools\evidence-validator\evidence_validator.py --project-path tools\noc-dashboard --readme README.md
```

Output JSON:

```cmd
python tools\evidence-validator\evidence_validator.py --project-path tools\noc-dashboard --json
```

## What It Checks

- README exists.
- Evidence folders exist.
- Screenshot/image folders exist.
- Local image files exist and have recognizable image headers.
- README image references match actual local files.
- Screenshot filenames are clean and base-name friendly.
- README contains obvious placeholder/TODO language.
- LinkedIn draft files or folders are inside the project path.
- Generated output folders are inside the project path.
- HANDOFF files are inside the project path.
- Secret-like filenames are present, without reading their contents.

## Decision Statuses

- `EVIDENCE READY`
- `NEEDS ORGANIZATION`
- `NEEDS MORE EVIDENCE`
- `PRIVACY REVIEW NEEDED`
- `BLOCKED`

Secret-like files return `BLOCKED`. Missing README image references return `NEEDS MORE EVIDENCE`. Screenshots that exist but are not referenced by the README return `NEEDS ORGANIZATION`. LinkedIn drafts, generated outputs, and HANDOFF files are listed as local-only warnings.

## What It Does Not Do

- Does not prove screenshot content is public-safe by visual inspection.
- Does not create screenshots.
- Does not invent missing evidence.
- Does not rewrite README links.
- Does not rename screenshots.
- Does not move local-only files.
- Does not delete generated outputs.
- Does not run security scans or live probes.
- Does not stage, commit, push, publish, post, email, or update Notion.
