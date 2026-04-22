## Overview

This lab documents a standalone phishing triage investigation of the domain **logi32-mrelay.pro**, sourced from Phishing.Database. The domain employed **conditional redirect evasion** — serving automated scanners a benign redirect to `https://www.lemonde.fr/en/` while delivering phishing content to real victims. Despite an initial 0/90 VirusTotal detection rate, manual multi-signal analysis produced a confirmed **MALICIOUS** verdict.

---

## Tools & Environment

| Tool | Purpose |
|---|---|
| **URLScan.io** | Infrastructure enumeration, redirect behavior identification |
| **VirusTotal** | Multi-vendor reputation scan and reanalysis |
| **Phishing.Database** | Source feed supplying the candidate domain and phishing URL |

No command-line tools or scripts were used; all analysis was performed through web-based platforms.

---

## Steps Performed

1. Received `logi32-mrelay.pro` as a phishing candidate from Phishing.Database.
2. Submitted the domain to **URLScan.io**, identifying IP `188.114.97.3`, ASN AS13335 (Cloudflare), dynamic script path `/as.php`, and the redirect target `https://www.lemonde.fr/en/`.
3. Identified **conditional redirect evasion**: automated scanners were served the Le Monde redirect; real victims were served the phishing payload.
4. Submitted the domain to **VirusTotal** — initial scan returned **0/90 detections**, confirming evasion was active at scan time.
5. Triggered **VirusTotal reanalysis** — **6/95 vendors** flagged the domain as Phishing/Malicious: BitDefender, Emsisoft, Fortinet, G-Data, Netcraft, and Webroot.
6. Evaluated structural domain indicators: ~1-month domain age, dynamic PHP path `/as.php`, `.pro` TLD, Cloudflare hosting masking the true origin server, and a random-character domain name with no brand affiliation.
7. Compiled the IOC table and rendered analyst verdict.
8. Documented recommended containment actions.

---

## Findings

| Indicator | Value | Risk |
|---|---|---|
| Domain | `logi32-mrelay.pro` | HIGH — random chars, no brand affiliation |
| IP Address | `188.114.97.3` | — |
| ASN | AS13335 (Cloudflare) | MEDIUM — masks true origin |
| Phishing URL | `https://logi32-mrelay.pro/as.php` | HIGH — dynamic PHP phishing kit |
| Redirect Target | `https://www.lemonde.fr/en/` | Evasion lure |
| Domain Age | ~1 month | HIGH — throwaway infrastructure |
| TLD | `.pro` | MEDIUM — commonly abused |

**Analyst Verdict: MALICIOUS**

---

## Security Significance

This investigation demonstrates three compounding risks present in modern phishing infrastructure:

1. **Conditional redirect evasion defeats automated tooling.** An initial 0/90 VirusTotal score illustrates that multi-AV aggregators are unreliable for URLs capable of fingerprinting and redirecting scanners. Reanalysis after the evasion window closed confirmed the domain's true nature (6/95 detections).

2. **PHP-based routing (`/as.php`) indicates a phishing kit deployment.** Dynamic server-side scripts are routinely used to conditionally serve payloads, collect credentials, or redirect based on visitor fingerprinting — a hallmark of packaged phishing kits.

3. **Cloudflare proxying complicates attribution and takedown.** Hosting behind AS13335 conceals the true origin server, requiring an abuse report to Cloudflare as a containment path rather than a direct registrar or host action.

The lab reinforces that manual behavioral triage and multi-signal correlation are essential for identifying threats that fully evade automated detection pipelines. Recommended actions include DNS/firewall blocking of `logi32-mrelay.pro`, adding `188.114.97.3` to threat intelligence blocklists, and submitting an abuse report to Cloudflare.