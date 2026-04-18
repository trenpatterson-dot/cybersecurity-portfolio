# SESSION-CONTEXT — Hardening Checklists

Paste this at the start of your next session to resume instantly.

---

**LAB NAME:** Hardening Checklists
**PLATFORM:** Ubuntu Workstation VM (VMware Workstation Pro)
**LAB TYPE:** Class — CYBR 445 Week 11
**DATE COMPLETED:** 2026-04-18
**FOLDER:** `CYBR 445/week-11-hardening-checklists/`
**STATUS:** Partial — Ubuntu complete, Windows Server 2022 blocked (VM not available)

**OBJECTIVE:** Audit and harden Ubuntu and Windows systems using baseline checks, secure configuration changes, and hardening guidance to reduce attack surface and improve security posture.

**TOOLS USED:** Lynis, systemctl, nano, OpenSSH, unattended-upgrades, libpam-pwquality, VMware Workstation Pro

**RESULTS:**
- Initial Lynis hardening index: 58
- Final Lynis hardening index: 63
- Improvement: +5 points
- Services disabled: cups, avahi-daemon, bluetooth
- SSH hardened: PermitRootLogin no, MaxAuthTries 3, LoginGraceTime 30, AllowTcpForwarding no, X11Forwarding no
- Password policy enforced: minlen=12, mixed character requirements
- Windows half: blocked — gpedit.msc not found, Local Users snap-in blocked, Windows Server 2022 VM not in VMware

**SCREENSHOTS:** 10 curated screenshots in `screenshots/` — named by section

**OUTPUTS GENERATED:** eli10.md, technical-summary.md, linkedin-post.md, onenote-notes.md, sources.md

**NEXT STEPS:**
- Import or create a Windows Server 2022 VM
- Complete the Group Policy and port review steps for the Windows side
- Run `git push` to push the commit
