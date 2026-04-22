## Lab Recap

- **Lab Name:** Phishing Analysis — logi32-mrelay.pro
- **Platform:** Standalone (independent investigation)
- **Lab Type:** Phishing — Malicious URL Triage & IOC Extraction
- **Date Completed:** 2025-07-14
- **Objective:** Investigate the domain `logi32-mrelay.pro` as a phishing candidate, enumerate its infrastructure, identify evasion techniques in use, extract all IOCs, and render a defensible analyst verdict.
- **Tools Used:** URLScan.io, VirusTotal, Phishing.Database
- **What I Did:**
  1. Received `logi32-mrelay.pro` as a candidate from Phishing.Database
  2. Submitted to URLScan.io — identified IP `188.114.97.3`, ASN `AS13335` (Cloudflare), dynamic script path `/as.php`, and a redirect to `https://www.lemonde.fr/en/`
  3. Recognized the redirect as **conditional redirect evasion** — automated scanners get the benign Le Monde page; real victims get the phishing payload
  4. Submitted to VirusTotal — initial scan returned **0/90 detections**, confirming evasion was active at scan time
  5. Triggered VirusTotal reanalysis — **6/95 vendors** flagged the domain as Phishing/Malicious (BitDefender, Emsisoft, Fortinet, G-Data, Netcraft, Webroot), once the evasion window had closed
  6. Evaluated domain-level risk indicators: ~1 month domain age, dynamic PHP path, abused `.pro` TLD, Cloudflare proxying masking the true origin, and a random-character name with no brand affiliation
  7. Compiled the full IOC table
  8. Rendered analyst verdict and documented remediation recommendations
- **What I Found / Results:**

  | IOC Type | Value | Source |
  |---|---|---|
  | Domain | `logi32-mrelay.pro` | Phishing.Database |
  | IP Address | `188.114.97.3` | URLScan.io |
  | ASN | AS13335 (Cloudflare) | URLScan.io |
  | Full URL | `https://logi32-mrelay.pro/as.php` | Phishing.Database |
  | Redirect Target | `https://www.lemonde.fr/en/` | URLScan.io |

  | Domain Indicator | Finding | Risk |
  |---|---|---|
  | Domain age | ~1 month | HIGH |
  | Script path | `/as.php` | HIGH — dynamic PHP phishing kit |
  | TLD | `.pro` | MEDIUM — commonly abused |
  | Hosting | Cloudflare | MEDIUM — masks true origin |
  | Domain name | `logi32-mrelay.pro` | HIGH — random chars, no brand |

  **Verdict: MALICIOUS** — despite an initial 0/90 VirusTotal score, cumulative behavioral and structural indicators confirmed phishing kit deployment with active evasion.

- **What Clicked / What I Learned:**
  - A **0/90 VirusTotal score is not a clean bill of health** — it can simply mean evasion is working. A redirect-capable URL must be treated with skepticism until the redirect destination itself has been verified.
  - **Conditional redirect evasion** is a concrete, real-world technique, not a theoretical one. The mechanism is elegant: fingerprint the visitor (bot vs. human) and serve content accordingly. URLScan.io exposed it; VT initially missed it entirely.
  - **Reanalysis matters.** Triggering a fresh VT scan after the evasion window closes is a valid step in phishing triage — the 0→6 detection shift confirmed the malicious classification.
  - Multi-signal correlation (domain age + PHP kit path + TLD abuse + evasion behavior + Cloudflare masking) is the right model for borderline verdicts. No single indicator is sufficient alone; all of them together are decisive.
  - Cloudflare as a hosting intermediary complicates both attribution and takedown — abuse reporting to Cloudflare is a necessary recommended action, not just an optional one.

- **Difficulty:** Medium
- **Screenshots:**
  - `urlscan-summary.png` — URLScan.io summary for `logi32-mrelay.pro`: detected redirect to Le Monde, resolved IP, and domain behavior overview ✅
  - `urlscan-ip-detail.png` — URLScan.io IP detail for `188.114.97.3`: ASN AS13335 (Cloudflare) attribution and hosting infrastructure ✅
  - `virustotal-detections.png` — VirusTotal reanalysis results: 6/95 vendor flagging breakdown (BitDefender, Emsisoft, Fortinet, G-Data, Netcraft, Webroot) ✅
- **Tags:** `phishing` `url-triage` `IOC-extraction` `evasion` `conditional-redirect` `virustotal` `urlscan` `cloudflare` `php-kit` `standalone` `SOC` `manual-analysis`

---

## Study Notes

### Conditional Redirect Evasion
A phishing site **fingerprints visitors** (via IP, user-agent, request headers) and routes bots/scanners to a legitimate site (here: Le Monde) while real victims receive the phishing payload. Defeats URL sandboxes and first-pass reputation lookups. Detection requires manual triage or delayed reanalysis.

### VirusTotal Triage Rules
- **0 detections ≠ clean** — especially for redirect URLs. Always check *what VT actually scanned*.
- **Trigger reanalysis** if you suspect evasion was active during the first scan. Detection rate can shift significantly (0→6 here).
- VT is a force multiplier, not a verdict machine.

### Phishing Domain Red Flags (exam-ready checklist)
| Signal | Risk |
|---|---|
| Domain age < 30 days | HIGH |
| Random-character / no-brand name | HIGH |
| Dynamic PHP path (e.g. `/as.php`) | HIGH — phishing kit |
| `.pro` / `.xyz` / `.top` TLD | MEDIUM |
| Cloudflare or proxy hosting | MEDIUM — masks origin |

### SOC Workflow for Redirect URLs
`URLScan first → check redirect chain → VT (+ reanalysis if needed) → domain indicators → multi-signal verdict`

### Recommended Blocklist Actions
Block domain at DNS/firewall · Add IP to threat intel feed · File Cloudflare abuse report

> **Core takeaway:** *Automated tools can be evaded. Manual triage caught what 90 vendors missed.*