# Central Orchestrator

Read-only local workflow runner for chaining the portfolio safety wrappers.

The orchestrator is report-only by default. It does not stage, commit, push, move, delete, rename, publish, call external APIs, run live scans, or read secret-like file contents.

## Workflow Order

1. evidence-validator
2. github-readiness
3. project-closeout

Missing wrappers are handled gracefully and produce `PARTIAL TOOLCHAIN`.

## Usage

Markdown output:

```cmd
python tools\orchestrator\orchestrator.py --project-path blue-team-labs\soc-alert-triage-lab
```

JSON output:

```cmd
python tools\orchestrator\orchestrator.py --project-path blue-team-labs\soc-alert-triage-lab --json
```

Save timestamped reports:

```cmd
python tools\orchestrator\orchestrator.py --project-path blue-team-labs\soc-alert-triage-lab --report-dir tools\orchestrator\reports
```

Reports are written under:

```text
<report-dir>\<timestamp>\
```

## Overall Statuses

- `WORKFLOW READY`
- `NEEDS REVIEW`
- `BLOCKED`
- `PARTIAL TOOLCHAIN`
- `LOCAL ONLY`

`WORKFLOW READY` still requires human approval before git actions, publishing, LinkedIn posting, Notion updates, file movement, or any external action.
