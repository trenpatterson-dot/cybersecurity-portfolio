# Notion Portfolio Command Center

Use this workflow when closing out completed cybersecurity portfolio labs, projects, GitHub-ready documentation, or supervisor-agent handoffs.

This is a copy/paste workflow only. Do not connect directly to Notion, require a Notion API integration, or treat Notion as an automated publishing target.

## Default Status Flow

Idea -> In Progress -> Needs Evidence -> Needs README -> Needs Security Review -> GitHub Ready -> Published

## Completion Rule

No project is fully complete until:

- Evidence and screenshots are validated.
- The README is complete and proof-aligned.
- Security review is complete.
- Supervisor-agent handoff is complete.
- GitHub publishing status is clear.

LinkedIn drafts stay local-only. Do not include LinkedIn draft files in GitHub publishing guidance.

## Required Notion Update

Include this section in completed lab and project closeouts:

```text
Notion Update:
Project/Lab Name:
Category:
Status:
Platform:
Tools Used:
Skills Demonstrated:
Evidence/Screenshot Folder:
GitHub README Status:
LinkedIn Draft Status:
Supervisor-Agent Handoff Status:
Security Review Status:
Date Started:
Date Completed:
Priority:
Notes:
```

## Field Guidance

- Project/Lab Name: Use the exact lab or project title.
- Category: Use a practical portfolio category such as SOC Lab, Blue-Team Lab, Detection Engineering, Threat Hunting, Security Review, GitHub Update, LinkedIn Post, Job Search, or Archive Cleanup.
- Status: Use the default status flow unless the user provides a custom status.
- Platform: Name the platform or environment, such as GitHub, TryHackMe, Wazuh, Windows, Linux, Splunk, Security Onion, Notion, LinkedIn, or Local Lab.
- Tools Used: List only tools actually used or documented by evidence.
- Skills Demonstrated: Use blue-team/SOC skills that the work genuinely demonstrates.
- Evidence/Screenshot Folder: Provide the local or repo-relative evidence folder. Do not invent missing evidence.
- GitHub README Status: State whether the README is missing, draft, complete, GitHub ready, published, or needs review.
- LinkedIn Draft Status: State local-only status, such as not started, draft local-only, needs review, or ready for manual posting.
- Supervisor-Agent Handoff Status: State whether the handoff is missing, drafted, complete, or needs review.
- Security Review Status: State not started, in progress, complete, or needs review.
- Date Started: Use the known date, or `Unknown` if not documented.
- Date Completed: Use the completion date when the closeout is finished, or `Not complete` if any completion rule is unmet.
- Priority: Use Low, Medium, High, or Critical.
- Notes: Keep this practical and evidence-based. Include blockers, privacy review needs, or next action.
