# Detection 1: Credential Access via /etc/shadow

## Objective
Simulate suspicious credential access activity on a Linux endpoint and detect it using Wazuh.

## Attack Simulation
The following commands were executed on the Ubuntu system:

```bash
sudo su
whoami
cat /etc/shadow