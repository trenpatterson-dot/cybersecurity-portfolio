# Screenshot Privacy Review

## Project

- Project path: `blue-team-labs/soc-alert-triage-lab`
- Review type: screenshot privacy review for GitHub/public boundary
- Review date: 2026-05-07
- Scope inspected: `README.md`, `docs/investigation.md`, `docs/findings.md`, `evidence/screenshots/`, and `evidence/screenshots-public/`

## Review Standard

Each screenshot was reviewed for visible or referenced public-safety concerns:

- Private IPs
- Usernames
- Hostnames
- Emails
- Real names
- Tokens or secrets
- API keys
- Customer or private data
- Sensitive URLs
- Fields that should be blurred before GitHub publication

If a screenshot was unclear or contained local identifiers, it was classified conservatively.

## Summary Recommendation

Public-safe recommendation: **GitHub candidates should use `evidence/screenshots-public/`, not the original raw screenshots**.

No visible tokens, API keys, passwords, emails, or customer data were identified during the raw screenshot review. However, the original screenshots under `evidence/screenshots/` expose some combination of local Wazuh URLs, local usernames, host/agent names, private lab IP context, timestamps, or detailed event fields. Those original screenshots should remain local-only.

README now links to public-safe screenshot copies under `evidence/screenshots-public/`. Those public screenshot copies are the GitHub candidate images.

## Screenshot Findings

### `01-wazuh-alert-overview.png`

- README context: Wazuh alert overview
- Classification: **NEEDS BLUR**
- Visible/reference concerns:
  - Local URL: `localhost/app/threat-hunting...`
  - Local manager/agent filter showing `tren`
  - Agent/host label `tren`
  - Browser/session UI visible
  - Lab timestamps and dashboard context
- No visible concerns found:
  - No tokens observed
  - No API keys observed
  - No emails observed
  - No customer/private business data observed
- Public-use note: Blur local URL and `tren` identifiers before GitHub, or get explicit approval to leave local lab identifiers visible.

### `02-failed-login-raw-event.png`

- README context: failed login raw event
- Classification: **NEEDS BLUR**
- Visible/reference concerns:
  - Local URL: `localhost/app/threat-hunting...`
  - Local host/agent/manager fields showing `tren`
  - Private lab IP visible in raw log context: `192.168.32.128`
  - Raw event details include authentication failure context, rule IDs, index names, timestamps, and event IDs
  - Wazuh index name and dashboard field values are visible
- No visible concerns found:
  - No tokens observed
  - No API keys observed
  - No emails observed
  - No customer/private business data observed
- Public-use note: Blur local URL, `tren` identifiers, private IP, event IDs, and any field values that should not be public.

### `03-repeated-failed-logins-filtered.png`

- README context: repeated failed logins filtered
- Classification: **NEEDS BLUR**
- Visible/reference concerns:
  - Local URL: `localhost/app/threat-hunting...`
  - Local manager filter showing `tren`
  - Event table includes agent name `tren`
  - Timestamps, rule descriptions, rule levels, and rule IDs are visible
  - Browser/session UI visible
- No visible concerns found:
  - No tokens observed
  - No API keys observed
  - No emails observed
  - No customer/private business data observed
- Public-use note: Blur local URL, `tren` identifiers, and any timestamps or event details that should not be public.

### `04-alert-fields-source-user-host-time.png`

- README context: alert fields, source, user, host, and time
- Classification: **NEEDS BLUR**
- Visible/reference concerns:
  - Wazuh dashboard context is visible
  - Agent/host label `tren` is visible
  - Timeline and dashboard fields include lab event timing context
  - MITRE and authentication summary context is visible
- No visible concerns found:
  - No tokens observed
  - No API keys observed
  - No emails observed
  - No customer/private business data observed
- Public-use note: Blur `tren` identifiers and any local timing/context fields that should not be published.

### `04-related-events-timeline.png`

- README context: related events timeline
- Classification: **NEEDS BLUR**
- Visible/reference concerns:
  - Local user/host/manager identifiers including `tren`
  - Root account/session context
  - UID values and local Linux authentication fields
  - Command/path details including sudo/pkexec activity and `/home/tren`
  - Wazuh index names, event IDs, timestamps, rule fields, and compliance mappings
  - Detailed full log fields are visible
- No visible concerns found:
  - No tokens observed
  - No API keys observed
  - No emails observed
  - No customer/private business data observed
- Public-use note: This screenshot has the highest amount of sensitive local context. Blur user/hostnames, local paths, event IDs, timestamps, and command details before GitHub unless explicitly approved.

### `05-pam-login-session-details.png`

- README context: PAM login session details
- Classification: **NEEDS BLUR**
- Visible/reference concerns:
  - Agent/manager/host fields showing `tren`
  - Root account/session context
  - UID and data source fields
  - PAM and pkexec session details
  - Wazuh index name, event ID, timestamps, rule fields, and compliance mappings
  - Full log text showing local session details
- No visible concerns found:
  - No tokens observed
  - No API keys observed
  - No emails observed
  - No customer/private business data observed
- Public-use note: Blur local user/host identifiers, event IDs, timestamps, UID fields, and full log session details before GitHub unless explicitly approved.

## Classification Summary

| Screenshot | Classification | Primary Reason |
|---|---|---|
| `01-wazuh-alert-overview.png` | NEEDS BLUR | Local URL and `tren` host/agent identifiers |
| `02-failed-login-raw-event.png` | NEEDS BLUR | Private IP, local URL, `tren` identifiers, raw event details |
| `03-repeated-failed-logins-filtered.png` | NEEDS BLUR | Local URL, `tren` identifiers, event timestamps and rule details |
| `04-alert-fields-source-user-host-time.png` | NEEDS BLUR | `tren` host/agent context and event timing context |
| `04-related-events-timeline.png` | NEEDS BLUR | Local user/host identifiers, root session context, command/path details, event metadata |
| `05-pam-login-session-details.png` | NEEDS BLUR | Local user/host identifiers, root session context, UID/event metadata, full log details |

## Public-Safe Recommendation

Do not publish the original screenshots from `evidence/screenshots/` to GitHub as-is.

README now links to public-safe copies under `evidence/screenshots-public/`. Those public copies are the GitHub candidate images.

Recommended safe path:

1. Keep original screenshots under `evidence/screenshots/` local-only.
2. Use the public-safe copies under `evidence/screenshots-public/` as the GitHub candidate images.
3. Re-run evidence validation after any approved screenshot replacement or README link update.

## Remaining Blockers

- Original screenshots under `evidence/screenshots/` should stay local-only unless Tren explicitly approves publishing local lab identifiers.
- README now links to `evidence/screenshots-public/`; those public screenshot copies are the GitHub candidate images.
