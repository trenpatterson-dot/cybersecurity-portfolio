# Email Header Analysis

## Sender Information

### From Address
security-update@micr0soft-verification.com

### Reply-To Address
support@account-verification-alerts.com

---

## Header Analysis Findings

### Suspicious Sender Domain

The sender domain used typosquatting behavior by replacing the letter “o” in Microsoft with the number “0.”

Observed domain:
- micr0soft-verification.com

This technique is commonly used in phishing campaigns to imitate trusted brands.

---

### Reply-To Mismatch

The Reply-To address used a different domain than the sender address.

Observed Reply-To:
- account-verification-alerts.com

Reply-To mismatches are common phishing indicators and may redirect victims to attacker-controlled infrastructure.

---

### Social Engineering Indicators

The message used:
- urgency
- password expiration warnings
- account suspension threats

to pressure the recipient into interacting with the phishing link.

---

## Analyst Assessment

The observed header characteristics strongly support classification of the message as phishing.