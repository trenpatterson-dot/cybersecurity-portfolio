# Phishing Analysis — logi32-mrelay.pro

## Overview

Manual triage of a submitted phishing domain — `logi32-mrelay.pro` — sourced from
Phishing.Database. The domain employed **conditional redirect evasion**, serving
automated scanners a benign redirect to Le Monde (`https://www.lemonde.fr/en/`) while
delivering phishing content to real victims. This technique successfully suppressed an
initial VirusTotal score of **0/90 detections**. Manual behavioral analysis and
multi-signal correlation resulted in a **MALICIOUS** verdict, later confirmed by a
6/95 reanalysis score across six vendors.

---

## Objectives

- Triage a suspected phishing domain using manual analysis tools
- Identify and document active evasion techniques bypassing automated detection
- Extract and structure all actionable IOCs for downstream blocking
- Demonstrate analyst decision-making when automated tooling returns a false negative

---

## Tools Used

| Tool | Purpose |
|---|---|
| **URLScan.io** | Domain scan, infrastructure enumeration, redirect behavior mapping |
| **VirusTotal** | Reputation lookup, vendor detection scoring, reanalysis trigger |
| **Phishing.Database** | Initial domain submission source |

---

## Steps Performed

1. **Received** domain `logi32-mrelay.pro` as a phishing candidate from Phishing.Database.
2. **Submitted to URLScan.io** — identified resolved IP `188.114.97.3`, ASN `AS13335`
   (Cloudflare), dynamic script path `/as.php`, and redirect target
   `https://www.lemonde.fr/en/`.
3. **Identified conditional redirect evasion** — URLScan confirmed the domain routes
   automated scanners to a legitimate news site while serving the phishing payload to
   real visitors.
4. **Submitted to VirusTotal** — initial scan returned **0/90 detections**, confirming
   the evasion technique was active at time of first submission.
5. **Triggered VirusTotal reanalysis** — after the redirect window closed, **6/95
   vendors** flagged the domain as Phishing/Malicious: BitDefender, Emsisoft, Fortinet,
   G-Data (Phishing); Netcraft, Webroot (Malicious).
6. **Evaluated structural domain indicators**: ~1-month domain age, dynamic PHP routing
   via `/as.php`, abused `.pro` TLD, Cloudflare hosting masking the origin server, and
   a random-character domain name with no brand affiliation.
7. **Compiled IOC table** covering domain, IP, ASN, full phishing URL, and redirect
   target.
8. **Rendered analyst verdict of MALICIOUS** based on cumulative behavioral and
   structural indicators — independent of VirusTotal's initial score.
9. **Documented remediation actions**: DNS/firewall block, IP blocklist entry, and
   Cloudflare abuse report.

---

## Key Findings

### Verdict: ⚠️ MALICIOUS

> Manual triage caught what 90 vendors missed.

#### Evasion Technique — Conditional Redirect
The domain actively fingerprints inbound requests and redirects automated scanners
(URLScan, VirusTotal crawlers, etc.) to `https://www.lemonde.fr/en/` — a legitimate,
high-reputation news site. Real victims receive the phishing payload. This technique
defeats URL sandbox analysis and first-pass reputation lookups entirely.

#### VirusTotal: 0/90 → 6/95
| Scan | Result |
|---|---|
| Initial scan | **0 / 90** — evasion active, all vendors bypassed |
| Reanalysis | **6 / 95** — BitDefender, Emsisoft, Fortinet, G-Data, Netcraft, Webroot |

The delta between scans directly illustrates why a single-tool, single-pass workflow
is insufficient for redirect-capable URLs.

#### IOC Table

| IOC Type | Value | Source |
|---|---|---|
| Domain | `logi32-mrelay.pro` | Phishing.Database |
| IP Address | `188.114.97.3` | URLScan.io |
| ASN | `AS13335` (Cloudflare) | URLScan.io |
| Full URL | `https://logi32-mrelay.pro/as.php` | Phishing.Database |
| Redirect Target | `https://www.lemonde.fr/en/` | URLScan.io |

#### Domain Risk Indicators

| Indicator | Finding | Risk |
|---|---|---|
| Domain age | ~1 month | 🔴 HIGH — throwaway infrastructure |
| Script path | `/as.php` | 🔴 HIGH — dynamic PHP phishing kit routing |
| Domain name | `logi32-mrelay.pro` | 🔴 HIGH — random characters, no brand affiliation |
| TLD | `.pro` | 🟡 MEDIUM — commonly abused TLD |
| Hosting | Cloudflare (AS13335) | 🟡 MEDIUM — masks true origin, complicates attribution |

#### Recommended Actions
- Block `logi32-mrelay.pro` at DNS and firewall level
- Add `188.114.97.3` to threat intelligence blocklist
- Submit abuse report to Cloudflare
- Do **not** rely solely on VirusTotal for URLs exhibiting redirect behavior

---

## Screenshots

**URLScan.io — Scan Summary**
Redirect to Le Monde confirmed, IP and domain behavior overview.

![URLScan.io summary scan results for logi32-mrelay.pro](screenshots/urlscan-summary.png)

---

**URLScan.io — IP Detail**
Infrastructure attribution for `188.114.97.3` via ASN AS13335 (Cloudflare).

![URLScan.io IP detail view for 188.114.97.3 showing Cloudflare ASN](screenshots/urlscan-ip-detail.png)

---

**VirusTotal — Reanalysis Detections**
6/95 vendor breakdown after evasion window closed: BitDefender, Emsisoft, Fortinet,
G-Data, Netcraft, Webroot.

![VirusTotal detection results showing 6/95 vendor flagging after reanalysis](screenshots/virustotal-detections.png)

---

## Lessons Learned

**Automated tools can be gamed — multi-signal correlation cannot.**

1. **A 0/90 VirusTotal score is not a clearance.** Conditional redirect evasion is a
   documented, accessible technique. Any URL that resolves to an unrelated legitimate
   site under sandbox conditions warrants manual escalation, not clearance.

2. **Reanalysis is a required step, not an optional one.** Triggering a second scan
   after initial results removed the evasion window and produced confirmatory detections.
   First-pass scores on short-lived or redirect-capable domains should always be
   treated as provisional.

3. **Structural indicators hold when behavioral signals are suppressed.** Domain age
   under 30 days, a dynamic PHP routing script, a nonsensical name pattern, and an
   abused TLD together form a high-confidence signal cluster — independently of any
   vendor score.

4. **Cloudflare proxying is an attribution blocker, not a trust signal.** The presence
   of AS13335 masks the origin server and complicates takedown. Treat Cloudflare-hosted
   suspicious domains with additional scrutiny, not less.

5. **Verdict documentation matters.** Clearly reasoning through a MALICIOUS finding
   against a 0/90 score produces an auditable record and reinforces the analyst's role
   in a detection pipeline — human judgment as a final control layer where automated
   tooling fails.
```

---

**Notes on decisions made:**

- **Screenshot paths** use `screenshots/` as the relative prefix since the images sit directly in the lab root alongside the README — move them into a `screenshots/` subfolder and the paths resolve without edits.
- **Lead-with-findings structure**: the Overview paragraph states the verdict and the evasion technique before the reader hits any procedural content, which is what a recruiter skimming for signal needs.
- **0/90 → 6/95 table**: surfaced early and kept visible in Key Findings rather than buried in Steps, because it's the sharpest proof-of-work moment in the lab.
- **No commands section**: the evidence confirmed no CLI commands were used; omitting it keeps the README honest rather than padded.
- **Lessons Learned** are written as transferable principles, not just "I learned X" — framing that reads well to both technical reviewers and hiring managers evaluating analyst maturity.