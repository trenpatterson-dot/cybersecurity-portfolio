logi32-mrelay.pro returned 0/90 detections on VirusTotal. That does not mean it's clean — it means the evasion worked.

This domain uses conditional redirect evasion: when an automated scanner hits it, it redirects to Le Monde. When a real victim lands on it, they get the phishing payload. The technique is straightforward but effective — most URL sandbox tools and reputation engines see the benign redirect and move on. First-pass result was 0 flags across 90 vendors.

Manual triage told a different story. URLScan.io revealed the redirect behavior, the dynamic PHP script at /as.php (a common phishing kit indicator), and hosting through Cloudflare's AS13335, which masks the true origin server. The domain itself was approximately one month old — a high-risk indicator consistent with throwaway phishing infrastructure. Forcing a VirusTotal reanalysis after the evasion window closed confirmed it: 6/95 vendors flagged the domain as Phishing/Malicious, including BitDefender, Fortinet, Netcraft, and Webroot.

Verdict: MALICIOUS. Recommended actions include DNS/firewall block on the domain, blocklisting 188.114.97.3, and filing a Cloudflare abuse report.

The broader lesson here is operational: a 0/90 VirusTotal score on a redirect-capable URL is a starting point, not a verdict. Multi-signal manual triage is what catches what automated tooling misses.

#CyberSecurity #PhishingAnalysis #ThreatIntelligence #BlueTeam #SOC