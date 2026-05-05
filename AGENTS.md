# AGENTS.md

Read `docs\ai-context\CODEX-START-HERE.md` at the start of new Codex tasks.
Read `docs\ai-context\CODEX-CLOSEOUT-CHECKLIST.md` before closing out lab, project, or GitHub tasks.

Core repo defaults:
- Use CMD-style commands when giving Windows commands.
- Do not invent evidence, screenshots, findings, or lab results.
- Do not push to GitHub without explicit approval.
- Do not commit secrets, credentials, private lab docs, reports, screenshots, or generated outputs unless explicitly approved.
- When giving screenshot rename instructions, do not include `.png`; provide base filename only.

Workflow notes:
- Prefer proof-first, blue-team, and SOC framing across portfolio work.
- Use the existing repo skills in `.agents\skills\` before adding new process.
- Keep public documentation aligned to real evidence and approved artifacts.

Notion Portfolio Command Center:
- Completed lab and project closeouts must include a copy/paste-ready `Notion Update` section for Tren's Notion cybersecurity/SOC portfolio command center.
- The Notion update is manual output only. Do not connect to Notion, require the Notion API, or assume a Notion integration is available.
- Track portfolio work through this default status flow: `Idea -> In Progress -> Needs Evidence -> Needs README -> Needs Security Review -> GitHub Ready -> Published`.
- No project is fully complete until evidence/screenshots are validated, the README is complete, the security review is complete, the supervisor-agent handoff is complete, and GitHub publishing status is clear.
- Keep LinkedIn drafts local-only. Do not add LinkedIn draft files to GitHub publishing guidance.
- Use `docs\ai-context\NOTION-PORTFOLIO-COMMAND-CENTER.md` for the required closeout fields and copy/paste template.

Required startup behavior:
1. Read `docs\ai-context\CODEX-START-HERE.md`.
2. Check project-specific skills under `.agents\skills\`.
3. Confirm the task type and safety rules before making changes.
4. Use small safe edits and validate structure before suggesting git actions.

Required closeout behavior:
- Follow `docs\ai-context\CODEX-CLOSEOUT-CHECKLIST.md`.
