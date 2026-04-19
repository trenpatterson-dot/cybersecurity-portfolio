Worked through a ransomware IR tabletop this week. No VM. Just the scenario, the lifecycle, and structured decision-making under pressure.

Acme Corp. Three accounting workstations encrypted. File server hit through accessible shares. Ransom notes, .locked extensions, one user who clicked an attachment at 1:47 PM — confirmed in email gateway logs.

Applied the full NIST SP 800-61 lifecycle: detection, containment, eradication, recovery, lessons learned. Built the attack timeline from log evidence. Documented chain of custody procedures. Flagged a fourth workstation in the same VLAN as potentially exposed until validated.

The thing that clicked hardest: containment and eradication are not the same step. Isolating systems buys time. Eradication is where you actually remove the threat. Conflating the two is how reinfection happens.

Backups helped the recovery plan — but the gap between the last backup (Monday 11 PM) and the incident meant up to 15 hours of potential data loss. That gap is a business risk, not just a technical detail.

Tabletop work builds real defender thinking. No alerts fired. No logs ran. But I came out of it with a sharper mental model of how structured IR actually works when the pressure is real.

#IncidentResponse #BlueTeam #Ransomware #NIST80061 #SecurityPlus
