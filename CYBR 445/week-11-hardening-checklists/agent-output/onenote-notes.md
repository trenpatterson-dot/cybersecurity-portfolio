# Hardening Checklists — Personal Notes

## What worked
- Lynis baseline and after-scan process was easy to follow
- Disabling extra services gave a clean first win
- SSH hardening changes applied without breaking the service
- Password policy updates were simple and high value
- Before/after comparison made the improvement easy to prove

## What didn't work
- Lost time on the Windows half because I was on Windows 11 Home, not Windows Server 2022
- VMware Workstation Pro did not have the Windows Server VM available
- gpedit.msc was not found — confirmed Home edition immediately
- Local Users and Groups snap-in returned edition restriction error

## Commands used
```bash
sudo apt update && sudo apt install lynis -y
sudo lynis audit system
sudo lynis audit system 2>&1 | tee ~/lynis-before.txt
grep "Suggestion" ~/lynis-before.txt | head -30
grep "Hardening index" ~/lynis-before.txt
sudo systemctl list-units --type=service --state=running
sudo systemctl disable --now cups
sudo systemctl disable --now avahi-daemon
sudo systemctl disable --now bluetooth
sudo nano /etc/ssh/sshd_config
sudo systemctl restart ssh
sudo systemctl status ssh --no-pager
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
sudo apt install libpam-pwquality -y
sudo nano /etc/security/pwquality.conf
sudo lynis audit system 2>&1 | tee ~/lynis-after.txt
grep "Hardening index" ~/lynis-after.txt
grep "Hardening index" ~/lynis-before.txt ~/lynis-after.txt
```

## Important results
- before score: 58
- after score: 63
- improvement: +5
- cups disabled
- avahi-daemon disabled
- bluetooth disabled
- SSH hardened successfully
- password quality policy updated

## Gotchas
- validate the OS before starting the Windows side
- Windows 11 Home is not the same as Windows Server 2022 for this lab
- missing VM = blocked completion, not failure

## Next steps
- create or import the Windows Server 2022 VM later
- finish the Windows policy and port review steps
- keep this version documented as partial, not full
