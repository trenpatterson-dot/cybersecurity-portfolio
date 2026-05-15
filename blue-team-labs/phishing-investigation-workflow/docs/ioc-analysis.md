# IOC Analysis

## Extracted Indicators

### Sender Domain
- micr0soft-verification.com

### Reply-To Domain
- account-verification-alerts.com

### Suspicious URL
- hxxp://microsoft-login-verification-reset[.]example

---

## IOC Notes

The phishing sample contained multiple suspicious indicators connected to impersonation and credential harvesting.

The sender domain used typosquatting by replacing the letter “o” in Microsoft with the number “0.”

The Reply-To domain did not match the sender domain, which is a common phishing indicator.

The suspicious URL attempted to imitate a Microsoft login or password reset workflow but did not use a legitimate Microsoft-owned domain.

---

## Defensive Value

These indicators could be used for:

- email filtering
- blocklists
- alert enrichment
- user awareness training
- phishing investigation documentation

---

## Analyst Assessment

The extracted IOCs support the conclusion that this message should be classified as phishing.