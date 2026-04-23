# SOC Alert Investigation — Privilege Escalation via Sudo (Wazuh)

## 🚨 What This Project Shows
This project demonstrates real SOC analyst workflow:
- Investigating SIEM alerts (Wazuh)
- Analyzing Linux authentication + privilege escalation logs
- Interpreting command-level behavior (not just alert labels)
- Making a risk-based decision with supporting evidence

This is not just alert triage — this is **analysis and validation**.

---

## 🧠 Scenario
While reviewing Wazuh events, I identified repeated sudo activity tied to privilege escalation.

Instead of filtering for high-severity alerts only, I:
- Pivoted to raw event analysis
- Identified repeated behavior patterns
- Investigated command-level activity

---

## 🔍 What I Found

A user (`tren`) executed the following command multiple times:/usr/sbin/setcap cap_net_raw,cap_net_admin=eip /usr/bin/dumpcap

### Key observations:
- Privilege escalation: user → root
- Command modifies binary capabilities
- Repeated execution (`firedtimes: 6`)
- Executed from user home directory

---

## ⚠️ Why This Matters

This action enables packet capture **without requiring root privileges** later.

### This can be:
- ✅ Legitimate → configuring Wireshark / network analysis tools  
- ⚠️ Risky → enabling network sniffing or credential capture  

---

## 🧠 Analyst Decision

No direct malicious indicators were observed.

However:
- Privilege escalation occurred
- Binary capabilities were modified
- Behavior could support post-exploitation activity

### 👉 Conclusion:
**Low–Medium risk — requires validation and monitoring**

---

## 🛠️ What I Would Do Next

- Validate user intent (legitimate setup vs unauthorized change)
- Confirm presence of packet capture tools (Wireshark, etc.)
- Monitor for:
  - unusual network traffic capture
  - repeated sudo activity
  - credential harvesting behavior

---

## 🧩 MITRE ATT&CK Mapping

- Privilege Escalation  
- Defense Evasion  
- Credential Access (potential)  
- Network Sniffing (potential)  

---

## 📸 Evidence

Located in:evidence/screenshots/

- `01-alert-overview.png`
- `02-alert-details.png`

---

## ⚙️ Tools Used

- Wazuh (SIEM)
- Ubuntu Linux VM
- Wazuh Threat Hunting (Events view)

---

## 💡 What This Project Proves

- I don’t rely on alert severity — I investigate behavior
- I can break down Linux logs and commands
- I understand privilege escalation beyond surface-level alerts
- I can explain risk in a way that supports decision-making

---

## 🚀 Author

**Tren Patterson**  
Aspiring SOC Analyst | Blue Team | Threat Detection  

---