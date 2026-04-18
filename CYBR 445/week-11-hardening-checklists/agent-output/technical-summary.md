# Hardening Checklists

## Objective
This lab focused on system hardening and baseline improvement. The goal was to harden Ubuntu and Windows systems, reduce attack surface, and compare the system state before and after secure configuration changes. The Ubuntu half was completed successfully. The Windows half could not be completed because the required Windows Server 2022 VM was not available.

## Tools Used
- Lynis
- systemctl
- nano
- OpenSSH
- unattended-upgrades
- libpam-pwquality
- VMware Workstation Pro

## Steps Taken
1. Installed Lynis on Ubuntu and ran an initial baseline audit.
2. Saved the baseline scan output to `~/lynis-before.txt`.
3. Recorded the initial hardening index and suggestion count.
4. Listed active running services to identify unnecessary services.
5. Disabled `cups`, `avahi-daemon`, and `bluetooth` to reduce attack surface.
6. Edited `/etc/ssh/sshd_config` and applied the following hardening settings:
   - `PermitRootLogin no`
   - `MaxAuthTries 3`
   - `LoginGraceTime 30`
   - `AllowTcpForwarding no`
   - `X11Forwarding no`
7. Restarted SSH and confirmed the service remained active.
8. Installed and enabled unattended upgrades to support automatic security patching.
9. Installed `libpam-pwquality` and updated `/etc/security/pwquality.conf` to require stronger passwords.
10. Re-ran Lynis and saved the output to `~/lynis-after.txt`.
11. Compared the before and after hardening scores.
12. Attempted to complete the Windows half of the lab but confirmed the environment was Windows 11 Home, not Windows Server 2022.
13. Checked VMware Workstation Pro and confirmed the required Windows Server 2022 VM was not present.

## Findings
The Ubuntu portion of the lab produced measurable results. The initial Lynis hardening index was 58. After disabling unnecessary services, tightening SSH, enabling unattended upgrades, and enforcing stronger password quality requirements, the final hardening index increased to 63 — a clear improvement of 5 points.

The service reduction step mattered because it removed functions that were not needed for the system's use case. Disabling `cups`, `avahi-daemon`, and `bluetooth` reduced the number of exposed components that could potentially be abused.

SSH hardening was another high-value change. Blocking root login, limiting authentication attempts, shortening the login grace period, and disabling forwarding features reduced risk around one of the most common remote administration services in Linux environments.

The password policy update improved account security by enforcing a minimum length of 12 characters and requiring uppercase, lowercase, numeric, and special characters. That aligned with the goal of strengthening local authentication controls.

The Windows half of the lab was blocked by an environment issue, not a process failure. The system initially used for the Windows side was confirmed as Windows 11 Home — `gpedit.msc` was not present and the Local Users and Groups snap-in returned an edition restriction error. VMware Workstation Pro did not contain an available Windows Server 2022 VM to continue the required Group Policy and port review steps.

## Key Takeaways
- Hardening is a series of smaller, practical decisions that reduce risk — not one giant change
- Before-and-after scoring with Lynis proves the improvement instead of just claiming it
- Validating the environment before starting saves time — wrong OS means blocked steps
- Partial completion is documented honestly, not hidden
