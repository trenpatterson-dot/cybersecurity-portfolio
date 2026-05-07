# Portfolio Index Generator

Read-only local inventory generator for the cybersecurity portfolio repo.

The generator scans local folders and produces recruiter-friendly markdown and JSON summaries. It does not stage, commit, push, move, delete, rename, publish, call external APIs, run live scans, or read secret-like file contents.

## Usage

Markdown output:

```cmd
python tools\portfolio-index\portfolio_index.py --repo-path .
```

JSON output:

```cmd
python tools\portfolio-index\portfolio_index.py --repo-path . --json
```

Save reports:

```cmd
python tools\portfolio-index\portfolio_index.py --repo-path . --output tools\portfolio-index\reports
```

When `--output` points to a directory, the tool writes:

```text
portfolio-index.md
portfolio-index.json
```

## Classifications

- `WORKFLOW READY`
- `CLOSEOUT READY`
- `GITHUB READY`
- `NEEDS REVIEW`
- `LOCAL ONLY`
- `INCOMPLETE`

## Detected Signals

- README presence
- docs/
- evidence/
- evidence/screenshots-public/
- queries/
- tool folders
- orchestrator compatibility
- GitHub readiness artifacts
- project-closeout-report.md
- outputs/
- HANDOFF files
- LinkedIn/local-only draft paths

## Notes

The index is an inventory and triage aid, not a publishing decision. Human review is still required before any git action or public use.
