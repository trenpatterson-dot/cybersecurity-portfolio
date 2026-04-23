# Suspicious Network Traffic Investigation Project Context

This file gives Codex and Cowork the local context needed to continue work in this project folder without re-explaining the setup.

---

## Project

**Project Name:** Suspicious Network Traffic Investigation
**Path:** `C:\Users\trenp\cybersecurity-portfolio\security-plus-projects\suspicious-network-traffic-investigation`
**Category:** Security+ project
**Focus:** Network traffic analysis, SIEM/log review, alert investigation, blue team documentation

---

## Objective

Document a suspicious network traffic investigation from the analyst point of view. The finished project should show:

- what traffic or alert triggered the investigation
- what evidence was reviewed
- what source, destination, protocol, port, or pattern stood out
- how the activity was classified
- what defensive value the investigation produced

---

## Required Structure

```text
suspicious-network-traffic-investigation/
|-- AGENTS.md
|-- HANDOFF.md
|-- README.md
|-- TODO.md
|-- docs/
|   |-- analysis.md
|   |-- findings.md
|   |-- timeline.md
|   `-- images/
`-- evidence/
    `-- commands/
        `-- commands-used.md
```

---

## Working Rules

- Keep all edits inside this project folder.
- Use direct, portfolio-ready writing.
- Frame the work like a SOC analyst investigation, not a classroom summary.
- Track assumptions clearly if evidence is still missing.
- Add screenshots to `docs/images/` when they become available.
- Record commands used during analysis in `evidence/commands/commands-used.md`.

---

## Expected Outputs

- `README.md`: final portfolio-facing project overview
- `HANDOFF.md`: current project status and next-step context
- `TODO.md`: active checklist for completion
- `docs/analysis.md`: investigation workflow and analyst reasoning
- `docs/findings.md`: confirmed findings and security impact
- `docs/timeline.md`: ordered sequence of events
- `evidence/commands/commands-used.md`: command log and purpose

---

## Next Session Start

When work resumes in this folder:

1. Review `HANDOFF.md` for current status.
2. Check `TODO.md` for the next open tasks.
3. Update the docs with real alert data, packet/log evidence, timestamps, screenshots, and commands.
4. Tighten the README after the evidence and findings are complete.
