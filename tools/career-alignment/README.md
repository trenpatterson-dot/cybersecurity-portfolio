# Career Alignment Engine

The Career Alignment Engine is a read-only local reporting tool for estimating SOC and blue-team career readiness from the cybersecurity portfolio.

It inspects local documentation and evidence structure only. It does not stage, commit, push, move, delete, rename, publish, call external APIs, run live scans, or read secret-like file contents.

## What It Reviews

- README files
- `project-closeout-report.md`
- `github-readiness-report.md`
- recruiter-portfolio reports when available
- portfolio-index reports when available
- orchestrator reports when available
- `evidence/screenshots-public/`
- `docs/`
- `queries/`

## CMD Usage

Run markdown mode:

```cmd
python tools\career-alignment\career_alignment.py --repo-path .
```

Run JSON mode:

```cmd
python tools\career-alignment\career_alignment.py --repo-path . --json
```

Write markdown and JSON reports:

```cmd
python tools\career-alignment\career_alignment.py --repo-path . --output tools\career-alignment\reports
```

## Output Sections

- Career readiness summary
- SOC/blue-team skill map
- Proven skills
- Weak/missing skills
- Suggested next labs/projects
- Suggested GitHub pin order
- Suggested recruiter talking points
- Suggested resume bullet themes
- Suggested LinkedIn themes
- Risk areas / weak evidence areas

## Readiness Labels

- `EARLY STAGE`
- `DEVELOPING`
- `SOC READY`
- `STRONG JUNIOR CANDIDATE`
- `NEEDS MORE EVIDENCE`

## Safety Boundary

- Report-only by default.
- No external APIs.
- No live scans.
- No Git actions.
- Secret-like paths are skipped by path/name only.
- Secret contents are not read.
- LinkedIn themes are suggestions only; LinkedIn drafts remain local-only.
