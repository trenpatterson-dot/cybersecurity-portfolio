# Portfolio Agent

Local-first Python agent for summarizing cybersecurity portfolio projects.

## What it does

- Scans top-level project folders in your portfolio
- Reads useful source files in this order: `README.md`, `.md`, `.txt`, `.docx`, `.pdf`
- Skips junk folders such as `.git`, `node_modules`, `venv`, and `__pycache__`
- Generates one output folder per project inside `agent-output`
- Leaves original project files untouched

## Generated files per project

- `eli10.md`
- `technical-summary.md`
- `github-update.md`
- `linkedin-post.md`
- `onenote-notes.md`
- `sources.md`

## Setup

```powershell
cd C:\Users\trenp\cybersecurity-portfolio\portfolio-agent
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

## Manual run

```powershell
python agent.py
```

Full scan example:

```powershell
python agent.py
```

Single-project example:

```powershell
python agent.py --project phishing-analysis
```

Recent-only example:

```powershell
python agent.py --recent-days 7
```

Combined example:

```powershell
python agent.py --project phishing-analysis --recent-days 7
```

Optional:

```powershell
python agent.py --limit-projects 3
```

## Discovery Controls

You can control scanning later in `.env`:

```powershell
PROJECT_ALLOWLIST=brute-force-detection-lab,threat-hunting-wazuh
PROJECT_DENYLIST=portfolio,portfolio-agent,lab-doc-agent,log-analyst-agent,journal,agent-output,.git,.github,node_modules,venv,__pycache__,.vscode,screenshots
```

- `PROJECT_ALLOWLIST`: if set, only these top-level folders are eligible
- `PROJECT_DENYLIST`: always skip these folder names

## Notes

- This tool is template-based and fully local. It does not send your data to cloud services.
- If `python-docx` or `pypdf` are unavailable, the agent will skip `.docx` or `.pdf` parsing gracefully.

## Tests

Run the test suite from the `portfolio-agent` folder:

```powershell
pytest
```
