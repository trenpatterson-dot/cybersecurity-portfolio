Locked down the Ubuntu side of a hardening lab and proved the improvement with before-and-after scoring.

Used Lynis to baseline the system, then reduced attack surface by disabling unnecessary services, tightening SSH settings, enabling unattended security updates, and enforcing a stronger password policy.

Result:
- hardening index moved from 58 to 63
- SSH stayed stable after config changes
- service footprint was reduced
- password controls were tightened

The Windows half did not get finished because the required Windows Server 2022 VM was not available in VMware Workstation Pro. I'm documenting that exactly how it happened instead of pretending the environment matched the lab.

That still matters. Blue-team work is not just making changes. It is validating the environment, proving the results, and being honest about the gaps.

#CyberSecurity #BlueTeam #LinuxHardening #SecurityOperations #Lynis #SecurityPlus
