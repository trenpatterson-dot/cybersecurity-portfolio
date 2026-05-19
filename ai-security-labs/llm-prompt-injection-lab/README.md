# LLM Prompt Injection Lab

## Overview

This project is a controlled AI security lab focused on prompt injection risk. The goal was to test how an AI assistant responds when user input attempts to override instructions, fake authority, hide malicious instructions inside documents, expose sensitive-looking data, or force unsafe automation.

This lab is built from a blue-team/SOC perspective. The focus is not on attacking real systems. The focus is on documenting risk, validating safe assistant behavior, and identifying defensive controls that keep analysts in control.

No real secrets, credentials, customer data, company data, or private system prompts were used.

---

## Objective

The objective of this lab was to test common prompt injection scenarios and document whether the assistant would:

- Refuse instruction override attempts
- Reject fake authority or roleplay bypass attempts
- Detect malicious instructions hidden inside untrusted content
- Redact sensitive-looking information
- Require human approval before destructive actions

---

## Tools Used

- ChatGPT
- Visual Studio Code
- Markdown
- Manual screenshot evidence
- AI security testing prompts

---

## Lab Structure

```text
llm-prompt-injection-lab/
├── README.md
├── HANDOFF.md
├── docs/
│   ├── lab-notes.md
│   ├── findings.md
│   └── defensive-controls.md
├── prompts/
│   └── test-prompts.md
├── evidence/
│   └── screenshots/
└── outputs/