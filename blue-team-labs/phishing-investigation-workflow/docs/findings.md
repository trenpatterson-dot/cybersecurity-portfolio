# Findings

## Finding 1 — Suspicious Sender Domain

### Observation
The email claimed to originate from Microsoft Security Team, but the sender domain used:

micr0soft-verification.com

The domain used a zero in place of the letter “o,” indicating possible typosquatting behavior.

### Security Relevance
Typosquatting domains are commonly used in phishing campaigns to impersonate legitimate organizations and trick users into trusting malicious communications.

---

## Finding 2 — Reply-To Mismatch

### Observation
The Reply-To address differed from the sender domain:

support@account-verification-alerts.com

### Security Relevance
Reply-To mismatches are common phishing indicators and may redirect responses to attacker-controlled infrastructure.

---

## Finding 3 — Urgency and Social Engineering Language

### Observation
The email used urgency-based language, including:
- “Urgent”
- “Password Expiration Notice”
- “verify your account immediately”
- “account suspension”

### Security Relevance
Urgency and fear-based messaging are common social engineering techniques used to pressure users into bypassing normal security awareness practices.

---

## Finding 4 — Suspicious Verification URL

### Observation
The email included a suspicious verification link:

http://microsoft-login-verification-reset.example

### Security Relevance
The URL did not use an official Microsoft domain and attempted to mimic legitimate Microsoft authentication branding.

The use of a non-standard domain strongly suggests phishing intent.

---

## Initial Investigation Verdict

The email contains multiple phishing indicators, including:
- typosquatting
- sender/reply-to mismatch
- urgency-based social engineering
- suspicious verification URL
- impersonation of a trusted organization

The message should be classified as a phishing attempt and blocked/quarantined in a production environment.