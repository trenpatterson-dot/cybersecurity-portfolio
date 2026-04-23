# Investigation — Brute Force Login Detection

## Objective
Identify suspicious authentication activity without relying on predefined alerts.

---

## Methodology
- Used Wazuh Threat Hunting → Events view
- Searched for authentication-related activity
- Pivoted across multiple search terms:
  - authentication
  - failed
  - sshd
- Analyzed event patterns and timestamps

---

## Observations

### Pattern Identified:
- ~10 failed login attempts
- Same user: `fakeuser`
- Same host: localhost
- Occurred within seconds

---

## Event Analysis

### Key Logs:
- Attempt to login using a non-existent user
- Maximum authentication attempts exceeded
- User login failed
- Brute force trying to get access to the system

---

## Timeline (Simplified)

1. Initial login attempt
2. Repeated failed attempts
3. Authentication threshold exceeded
4. System flags brute force behavior

---

## Analysis

### Indicators of Brute Force:
- Rapid repeated attempts
- Targeting a single user
- Authentication failures increasing quickly

---

## Analyst Assessment
The activity is consistent with brute force login attempts and represents an unauthorized access attempt.

---

## Conclusion
Confirmed brute force behavior based on repeated failed authentication attempts within a short timeframe.

---

## Recommended Actions
- Implement account lockout policies
- Monitor authentication logs continuously
- Block repeated offenders
- Consider multi-factor authentication (MFA)