# LLM Prompt Injection Lab — Defensive Controls

## Purpose

This document lists defensive controls that reduce risk in AI-assisted SOC, help desk, documentation, and automation workflows.

The goal is not to make an AI assistant perfect. The goal is to design the workflow so user input, external documents, and unsafe requests cannot control the system.

---

## Control 1 — Separate Trusted Instructions From User Input

### Risk Addressed
Prompt injection attempts may tell the assistant to ignore previous instructions, reveal protected content, or change its role.

### Defensive Control
Trusted system instructions should be separated from user-controlled input. User input should be treated as data, not authority.

### Example
A user saying “ignore all previous instructions” should not override the assistant’s approved task.

---

## Control 2 — Treat External Content as Untrusted

### Risk Addressed
Indirect prompt injection can hide inside documents, emails, tickets, webpages, logs, or copied text.

### Defensive Control
The assistant should summarize external content without obeying commands found inside that content.

### Example
A document that says “do not mention risks” should be flagged as suspicious instead of followed.

---

## Control 3 — Reject Fake Authority and Roleplay Bypass Attempts

### Risk Addressed
Attackers may use phrases like “developer mode,” “admin mode,” or “pretend you are unrestricted” to pressure the assistant.

### Defensive Control
The assistant should reject fake authority claims and stay focused on the approved role.

### Example
A SOC assistant should continue helping with SOC documentation instead of pretending to enter developer mode.

---

## Control 4 — Redact Sensitive Data

### Risk Addressed
AI summaries may accidentally repeat passwords, SSNs, tokens, customer data, or private information.

### Defensive Control
Use data minimization and redaction. Do not include sensitive fields unless there is a clear approved need.

### Example
A ticket containing a password should be summarized as “login issue reported,” with the password redacted.

---

## Control 5 — Keep Human Approval for Destructive Actions

### Risk Addressed
AI tools connected to real systems can cause harm if they delete files, block IPs, quarantine hosts, or change firewall rules without validation.

### Defensive Control
Require human-in-the-loop approval for destructive or high-impact actions.

### Example
The assistant can recommend blocking an IP, but an analyst must validate and approve the action first.

---

## Control 6 — Log AI-Assisted Decisions

### Risk Addressed
Without documentation, teams may not know why an AI-assisted recommendation was made.

### Defensive Control
Record the alert, input, recommendation, analyst decision, and final action.

### Example
A SOC workflow should document whether the analyst accepted, rejected, or modified the AI recommendation.

---

## Control 7 — Use Approved Data Boundaries

### Risk Addressed
Sensitive company, customer, or regulated data may be pasted into an unapproved AI tool.

### Defensive Control
Define what data is allowed, restricted, or prohibited in AI workflows.

### Example
Real API keys, passwords, customer records, and private company data should not be used in public or unapproved AI tools.

---

## Final Recommendation

AI tools should support analyst judgment, not replace it. The safest workflow is:

1. Treat user input as untrusted.
2. Treat external content as untrusted.
3. Redact sensitive data.
4. Keep analysts in control.
5. Require approval for high-impact actions.
6. Document decisions and evidence.