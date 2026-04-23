# Findings — Brute Force Login Attempt

## Finding Title
Repeated failed authentication attempts indicating brute force attack

---

## Summary
Wazuh logs revealed repeated failed login attempts targeting a non-existent user account. The activity occurred within a short timeframe and triggered multiple authentication-related alerts.

---

## Evidence
- ~10 authentication failures
- Same user: fakeuser
- Same host: localhost
- Rule descriptions:
  - Attempt to login using a non-existent user
  - Maximum authentication attempts exceeded
  - Brute force trying to get access to the system

---

## Impact
Unauthorized access attempts could lead to:
- account compromise
- credential discovery
- system access if successful

---

## Risk Level
Medium

---

## Analyst Assessment
The activity is consistent with brute force login attempts and is not typical user behavior.

---

## Recommendation
- Monitor and block suspicious authentication activity
- Implement account lockout controls
- Enforce strong password policies
- Deploy MFA where possible