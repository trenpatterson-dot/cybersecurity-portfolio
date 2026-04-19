# Incident Response Tabletop — Personal Notes

## What worked
- NIST 800-61 is a solid mental scaffold — phases are clearly sequenced for a reason
- Working through each phase in order forces you to think about what each step depends on
- Building the attack timeline from evidence first made the containment decisions cleaner
- Chain of custody section was straightforward once the forensic imaging rationale clicked

## What didn't / gotchas
- Easy to blur containment and eradication — they have different goals, different actions
- The 4th workstation (unaffected, same VLAN) is a trap — assume exposure until validated
- Recovery timing is a real business decision: restore fast vs. restore safely are not the same thing
- Data loss window (up to 15 hours) is not a technical problem — it is a backup policy problem

## Key concepts to remember

**Containment:** Stop the spread. Preserve evidence. Buy time. Do not remove anything yet.

**Eradication:** Remove malware and all persistence. Reset credentials. Patch the entry point. Verify no other systems are encrypting.

**Recovery:** Verify eradication first — always. Restore from known-good backup. Validate before reconnecting. Monitor post-restore for reinfection. Phase production return.

**Chain of custody:** Image the drive before doing anything. Analyze the forensic image, not the original. Never run AV on the original drive. Documentation tracks who touched what and when.

## Attack timeline
- 1:47 PM — user clicks phishing attachment
- Shortly after — malware executes, local files begin encrypting
- Spread to FS01 via accessible shares
- 2:14 PM — help desk begins receiving calls
- 3 calls within 10 minutes

## Numbers that matter
- Affected: 3 accounting workstations + FS01
- Potentially exposed: 1 additional workstation (same VLAN, unvalidated)
- Severity: Critical
- Data loss window: up to 15 hours
- Recovery source: Monday 11 PM backup

## Preparation gaps identified
- No strong phishing prevention
- No endpoint detection / EDR
- Poor segmentation (FS01 reachable via user shares)
- Weak user awareness training
- IR plan not regularly tested

## Recommendations documented
- Stronger email filtering
- Deploy EDR across endpoints
- Improve VLAN segmentation
- Regular phishing awareness training
- Scheduled IR tabletop testing

## Next steps
- Read NIST 800-61 Rev 2 full document (not just the framework summary)
- Find a real ransomware case study and map it to this lifecycle
- Practice chain of custody documentation — useful for DFIR work
