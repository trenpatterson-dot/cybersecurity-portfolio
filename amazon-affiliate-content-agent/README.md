# Amazon Affiliate Content Agent

## Overview
Archived portfolio snapshot of a compliance-aware content workflow that loads products, drafts affiliate content, checks compliance, and routes output through a human review queue.

## What I Did
- Built a local-first affiliate content pipeline with product loading, draft generation, compliance checks, and review queue handling.
- Kept publishing gated behind human review instead of automatic posting.
- Added safe default behavior through a mock product provider for local development.
- Added configurable Creators API scaffolding for future signed request testing.
- Preserved this copy as an archived portfolio snapshot while active development moved to the standalone `affiliate-content-agent` project.

## Key Findings
- The workflow separates drafting, compliance review, approval, and publishing.
- The project defaults to local mock product data for safer development.
- If Creators API settings are incomplete, the app falls back to mock behavior.
- The archived copy should be treated as a portfolio snapshot, not the active source of truth.

## Security Impact
Even outside classic SOC work, this project shows safe automation habits: local defaults, explicit configuration, review gates, and no silent live publishing. Those controls are relevant to blue-team thinking because they reduce operational risk.

## Tools Used
- Python
- SQLite
- pytest
- python-dotenv
- Amazon Creators API scaffold

## Outcome
This project demonstrates controlled automation with compliance checks and human approval gates. It remains useful as a portfolio example of safe workflow design, while active development belongs in the standalone source project.
