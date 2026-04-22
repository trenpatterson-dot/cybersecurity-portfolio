Wazuh Rule ID 5760 fired 10 alerts during a Hydra SSH brute force run — zero successful logins, full detection, no manual rule tuning required.

The setup: Kali Linux (192.168.64.133) ran Hydra v9.6 against an Ubuntu target (192.168.64.130) with OpenSSH intentionally exposed on port 22 and no compensating controls in place. Hydra cycled a custom wordlist against username "tren" while Wireshark captured the burst of high-frequency TCP SYN packets to port 22 in real time — a textbook network-layer signature for this attack type, visible without touching host-based telemetry at all.

Wazuh picked up every authentication failure automatically. All 10 alerts mapped to MITRE ATT&CK T1110.001 — Password Guessing, SSH sub-technique — without any custom rule configuration. The pipeline from Ubuntu log forwarding through alert generation worked end-to-end out of the box.

The more useful part was working through the defensive gaps afterward. The lab exposed a distinction worth noting: Wazuh Rule 5763 (the brute force threshold alert) never fired — only the per-failure Rule 5760 did. Without 5763 triggering active response, an attacker with a larger wordlist keeps going unimpeded. Detection without automated containment is half a solution. Remediation documented in the incident report covers fail2ban, key-based SSH auth, disabling root login via sshd_config, and Wazuh active response tied to Rule 5763 to close that gap.

Full write-up, screenshots, and incident report are in my portfolio.

#CyberSecurity #BlueTeam #SOC #Wazuh #MITREATTACK