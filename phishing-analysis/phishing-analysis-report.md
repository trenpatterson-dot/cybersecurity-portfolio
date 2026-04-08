The domain redirected scanners to a legitimate news site (Le Monde) 
to avoid detection. This is a known technique called **conditional redirect evasion**.

### 4b. VirusTotal Results
- **Initial scan:** 0 / 90 vendors flagged (evasion successful)
- **Reanalysis:** 6 / 95 vendors flagged as Phishing/Malicious
- **Flagged by:** BitDefender, Emsisoft, Fortinet, G-Data (Phishing) 
  Netcraft, Webroot (Malicious)
- **Conclusion:** Conditional redirect evaded most tools on first scan. 
  Reanalysis confirmed malicious classification.
### 4c. Domain Indicators
| Indicator | Finding | Risk |
|-----------|---------|------|
| Domain age | ~1 month | HIGH |
| Script path | /as.php | HIGH — dynamic PHP phishing kit |
| TLD | .pro | MEDIUM — commonly abused |
| Hosting | Cloudflare | MEDIUM — masks true origin |
| Domain name | logi32-mrelay.pro | HIGH — random chars, no brand |

---

## 5. IOC Table

| IOC Type | Value | Source |
|----------|-------|--------|
| Domain | logi32-mrelay.pro | Phishing.Database |
| IP Address | 188.114.97.3 | URLScan.io |
| ASN | AS13335 (Cloudflare) | URLScan.io |
| URL | https://logi32-mrelay.pro/as.php | Phishing.Database |
| Redirect target | https://www.lemonde.fr/en/ | URLScan.io |

---

## 6. Analyst Verdict

Despite 0/90 detections on VirusTotal, this domain exhibits multiple 
phishing indicators: creation date under 30 days, dynamic PHP routing, 
Cloudflare masking, and confirmed conditional redirect behavior designed 
to evade automated scanners. Manual analysis reveals active evasion 
techniques consistent with a phishing kit deployment.

**Verdict: MALICIOUS**

---

## 7. Recommended Actions

- Block domain `logi32-mrelay.pro` at DNS/firewall level
- Add IP `188.114.97.3` to threat intelligence blocklist
- Flag for abuse report to Cloudflare
- Do not rely solely on automated tools for URLs exhibiting redirect behavior

---

## 8. Key Takeaway

> Automated tools can be evaded. Manual triage caught what 90 vendors missed.