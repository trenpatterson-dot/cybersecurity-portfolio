
---

# 📄 `docs/detection-2-brute-force.md`

```markdown
# Detection 2: Brute Force Authentication Attempts

## Objective
Simulate a brute force attack by generating repeated failed login attempts and detect the behavior using Wazuh.

## Attack Simulation
The following command was executed:

```bash
for i in {1..10}; do su root; done