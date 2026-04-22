**Overview**

The document describes a standalone phishing triage investigation of the domain `logi32-mrelay.pro`, sourced from Phishing.Database. The domain employed conditional redirect evasion, serving automated scanners a benign redirect to `https://www.lemonde.fr/en/` while delivering phishing content to real victims.

**Tools & Environment**

* URLScan.io: used for infrastructure enumeration and redirect behavior identification
* VirusTotal: used for multi-vendor reputation scan and reanalysis
* Phishing.Database: provided the candidate domain and phishing URL

No command-line tools or scripts were used in this investigation.

**Steps Performed**

1. Received `logi32-mrelay.pro` as a phishing candidate from Phishing.Database.
2. Submitted the domain to URLScan.io, identifying IP `188.114.97.3`, ASN AS13335 (Cloudflare), dynamic script path `/as.php`, and the redirect target `https://www.lemonde.fr/en/`.
3. Identified conditional redirect evasion: automated scanners were served the Le Monde redirect; real victims were served the phishing payload.
4. Submitted the domain to VirusTotal - initial scan returned 0/90 detections, confirming evasion was active at scan time.
5. Triggered VirusTotal reanalysis - 6/95 vendors flagged the domain as Phishing/Malicious: BitDefender, Emsisoft, Fortinet, G-Data, Netcraft, and Webroot.
6. Evaluated structural domain indicators: ~1-month domain age, dynamic PHP path `/as.php`, `.pro` TLD, Cloudflare hosting masking the true origin server, and a random-character domain name with no brand affiliation.
7. Compiled the IOC table and rendered analyst verdict.
8. Documented recommended containment actions.

**Findings**

* Domain: `logi32-mrelay.pro` - HIGH risk due to random characters and lack of brand affiliation
* IP Address: `188.114.97.3`
* ASN: AS13335 (Cloudflare) - MEDIUM risk due to masking the true origin server
* Phishing URL: `https://logi32-mrelay.pro/as.php` - HIGH risk due to dynamic PHP phishing kit
* Redirect Target: `https://www.lemonde.fr/en/` - EVASION LORE
* Domain Age: ~1 month - HIGH risk due to throwaway infrastructure
* TLD: `.pro` - MEDIUM risk due to common abuse

**Analyst Verdict: MALICIOUS**

**Security Significance**

This investigation highlights three compounding risks present in modern phishing infrastructure:

1. Conditional redirect evasion defeats automated tooling.
2. PHP-based routing (`/as.php`) indicates a phishing kit deployment.
3. Cloudflare proxying complicates attribution and takedown.

The lab emphasizes the importance of manual behavioral triage and multi-signal correlation for identifying threats that fully evade automated detection pipelines. Recommended actions include DNS/firewall blocking of `logi32-mrelay.pro`, adding `188.114.97.3` to threat intelligence blocklists, and submitting an abuse report to Cloudflare.