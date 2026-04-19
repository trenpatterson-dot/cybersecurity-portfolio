# Incident Response Tabletop — NIST SP 800-61 Ransomware Scenario

Documentation-based IR tabletop applying the full NIST SP 800-61 lifecycle to a ransomware scenario.

## Tools / Framework

- NIST SP 800-61 Rev 2
- CISA Ransomware Guide
- MITRE ATT&CK (T1486, T1566)

## What This Lab Demonstrates

- Applying the 6-phase IR lifecycle in sequence under a realistic scenario
- Building an attack timeline from log evidence
- Distinguishing containment from eradication (common conflation that causes reinfection)
- Documenting chain of custody procedures for forensic integrity
- Classifying severity and estimating data loss from backup gap analysis
- Identifying preparation gaps and producing actionable recommendations

## Scenario Summary

Acme Corp ransomware incident. Three accounting workstations and file server FS01 encrypted via phishing attachment clicked at 1:47 PM. Help desk calls began at 2:14 PM. Fourth workstation in the same VLAN treated as potentially exposed until validated. Recovery source: Monday 11 PM backup. Estimated data loss: up to 15 hours.

## Key Findings

- Initial access: phishing email attachment (confirmed via email gateway logs)
- Lateral movement: SMB shares between workstations and FS01
- Severity: Critical
- Data loss window: up to 15 hours
- Preparation gaps: no EDR, weak segmentation, no phishing prevention, untested IR plan

## Skills Demonstrated

- IR lifecycle execution (Preparation → Detection → Containment → Eradication → Recovery → Lessons Learned)
- Evidence-based timeline construction
- Chain of custody documentation
- Business risk framing (backup gap = data loss decision, not just a technical metric)
