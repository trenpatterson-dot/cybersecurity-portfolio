# Recruiter README Checklist

Use this checklist before making any public GitHub repo recruiter-facing.

## Required README Elements

Every public repo should have:

- Clear project title.
- Short role-focused description.
- Tools and skills list.
- What problem the project solves.
- What evidence is included.
- What the recruiter should review first.
- Public-safe boundary statement.
- No secrets, credentials, private data, internal work information, or unreviewed evidence.
- No exaggerated claims about production SOC access, live incident authority, tenant ownership, legal authority, or compliance authority.

## Recruiter Review Standard

A recruiter should understand the repo in 30 seconds:

1. What the project is.
2. Which SOC, security analyst, IAM, or GRC role skills it supports.
3. Which files or sections to open first.
4. Whether the evidence is lab-based, simulated, sanitized, or production-approved.
5. Why the work matters for blue-team analysis.

## Public-Safe Wording Standard

Use direct language:

- Good: `Lab-based Microsoft Sentinel alert triage case study.`
- Good: `Simulated identity-risk investigation with public-safe notes.`
- Avoid: `Production SOC investigation` unless that is explicitly approved and safe to disclose.
- Avoid: `Real incident response` unless the evidence is public-approved and legally safe.

## Pre-Publish Check

Before pushing README changes, check for:

- Secrets, tokens, API keys, private keys, credentials, or passwords.
- Private screenshots, customer data, internal work information, or restricted logs.
- Claims that imply live SOC employment, tenant ownership, legal/compliance authority, or production action authority.
- Broken links to featured projects.
- Empty folders presented as completed work.