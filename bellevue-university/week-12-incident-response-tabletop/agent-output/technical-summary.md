# Incident Response Tabletop

## Objective
Apply the NIST SP 800-61 incident response lifecycle to a ransomware scenario. Document scope and severity, construct an attack timeline, define containment and recovery actions, produce lessons learned, and create a chain of custody template.

## Framework Used
- NIST SP 800-61 Rev 2 — Computer Security Incident Handling Guide
- Documentation-based exercise — no VM required

## Scenario
Acme Corp ransomware incident. Three accounting workstations and file server FS01 confirmed affected. Files renamed with `.locked` extension, ransom notes present. A fourth workstation in the same VLAN appears unaffected but is treated as potentially exposed until validated. No active VPN connections. Daily backups exist; last backup Monday at 11 PM.

## Steps Performed

1. Mapped all six IR lifecycle phases and documented each with clear, practical explanations.
2. Identified preparation strengths: daily backups and email gateway logging.
3. Identified weak or missing controls: phishing prevention, endpoint detection, network segmentation, user awareness training, IR plan maturity.
4. Analyzed detection: help desk received three calls within 10 minutes starting at 2:14 PM. Email logs confirmed a user clicked an attachment at 1:47 PM — strongest single piece of evidence.
5. Classified incident severity as Critical.
6. Built attack timeline:
   - 1:47 PM — user clicks attachment
   - Shortly after — malware executes, local files begin encrypting
   - Spread to FS01 via accessible shares
   - 2:14 PM — help desk calls begin (3 calls in under 10 minutes)
7. Documented containment actions: isolate affected workstations and FS01, block phishing indicators, preserve logs and evidence, validate fourth workstation before trusting it.
8. Documented eradication actions: full log review across endpoint, email, server, and network; remove malware and persistence; reset compromised credentials; patch initial access vector.
9. Documented recovery actions: verify eradication before any restore, restore FS01 from Monday backup, rebuild or restore affected workstations, validate files and systems, monitor closely for reinfection, phase systems back into production. Estimated data loss: up to 15 hours.
10. Documented lessons learned: phishing attachment as likely root cause, backups aided recovery planning, recommendations for stronger email filtering, EDR deployment, improved segmentation, regular user awareness training, and updated IR testing cadence.
11. Completed chain of custody section: built a template form, explained legal and investigative significance, documented forensic handling rules — image the drive first, analyze the image, never run antivirus on the original.

## Key Findings
- Initial access vector: phishing email attachment (1:47 PM click confirmed in email gateway logs)
- Confirmed affected systems: 3 accounting workstations, FS01
- Potential additional exposure: 4th workstation in same VLAN
- Severity: Critical
- Estimated data loss: up to 15 hours (backup gap from Monday 11 PM)
- Recovery path: restore from Monday backup after confirmed eradication

## Key Takeaways
- Containment and eradication are distinct phases — conflating them causes reinfection
- Recovery means restoring safely, not just restoring fast
- Chain of custody integrity affects both legal value and investigative trust
- Backups only help if the timing gap is understood and accepted as a business risk
- Tabletop exercises build real defender decision-making even without a live environment
