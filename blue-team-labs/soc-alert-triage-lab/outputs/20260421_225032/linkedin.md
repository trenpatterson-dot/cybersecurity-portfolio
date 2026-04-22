In the SOC Alert Triage Lab, I utilized Wazuh to simulate a real-world security incident response scenario. The environment consisted of an Ubuntu server running as a Wazuh manager and a Kali Linux machine acting as an attacker.

Upon setup, I encountered issues with the Wazuh API connectivity, which I resolved. Post-resolution, I verified the functionality of both the Wazuh manager and dashboard. Subsequently, SSH was configured on the Ubuntu target.

To emulate a potential attack, repeated failed SSH login attempts were generated from the Kali Linux machine to the Ubuntu Wazuh server. These attempts triggered alerts within the Wazuh SIEM, allowing me to perform SOC-style alert triage and investigate the source of these events.

The investigation revealed that the repeated failed logins originated from the attacker machine. I filtered these events for further analysis, focusing on user, host, and time fields. The findings were documented in the source material.

With the lab complete, the next steps involve generating final documentation outputs and preparing a GitHub repository structure for this project.

#Cybersecurity #SOC #SIEM #Wazuh #BlueTeam #LabExercise #CyberSecurityLearning