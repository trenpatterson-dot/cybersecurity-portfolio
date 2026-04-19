# Incident Response Tabletop — ELI10

Ransomware hit a company. Files got locked. I had to figure out what happened, stop it from spreading, clean it up, get things back online, and make sure it does not happen again.

I followed the incident response lifecycle — a 6-step framework that tells defenders exactly what to do and in what order.

**Preparation.** The company had daily backups and email logs. Good. But they were missing strong phishing filters and proper endpoint detection. Bad.

**Detection.** IT help desk got three calls in 10 minutes. Email logs showed one user clicked a suspicious attachment at 1:47 PM. That is when it started.

**Containment.** Pull the affected computers off the network. Lock down the file server. Block the sender. Do not let it spread further.

**Eradication.** Remove the malware. Reset passwords. Patch whatever let it in.

**Recovery.** Restore from the Monday backup — but check everything before reconnecting anything.

**Lessons Learned.** Fix what failed. Train users. Improve detection. Test the plan before the next incident.

No VMs needed for this lab. It was a tabletop exercise — working through a real scenario on paper. Defenders who have thought through a ransomware response once will move faster and smarter when it actually happens.

Thinking through the problem counts as training. This lab proved it.
