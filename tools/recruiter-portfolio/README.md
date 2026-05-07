# Recruiter Portfolio Presentation Layer

Read-only local presentation layer for turning the cybersecurity portfolio into a recruiter-facing summary.

This tool does not stage, commit, push, move, delete, rename, publish, call external APIs, run live scans, or read secret-like file contents.

## Usage

Markdown:

```cmd
python tools\recruiter-portfolio\recruiter_portfolio.py --repo-path .
```

JSON:

```cmd
python tools\recruiter-portfolio\recruiter_portfolio.py --repo-path . --json
```

Save reports:

```cmd
python tools\recruiter-portfolio\recruiter_portfolio.py --repo-path . --output tools\recruiter-portfolio\reports
```

## Output

- top featured projects
- skill map
- SOC/blue-team story summary
- GitHub pin candidates
- LinkedIn feature candidates
- cleanup warnings

The output is a recruiter-presentation aid, not a publishing decision. Human review is still required before GitHub, LinkedIn, or portfolio updates.
