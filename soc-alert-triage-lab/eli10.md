# What's a Cybersecurity Lab? Let's Explore the SOC Alert Triage Lab! 🕵️‍♂️💻

A cybersecurity lab is like a playground for super-smart people who protect computers and networks from bad guys. In this case, we're talking about the **SOC Alert Triage Lab**.

This lab was set up with a special tool called Wazuh. Imagine it as a big, helpful robot that keeps an eye on everything happening in our computer world! 🤖

In this lab, the goal was to pretend there were some bad guys trying to break into our system (Ubuntu server) from another computer (Kali Linux). The bad guys tried to log in 9 times but couldn't! This is called a brute force attack. 🔪

Our job was to use Wazuh like a detective, finding out who, what, when, and where the attacks happened. We fixed some problems with Wazuh first, then looked at the alerts it generated. 🚨

We found that the bad guys kept trying to log in as 'fakeuser' on our server 'tren'. No successful login was observed, but a rule called '2502' (which is very important) was triggered. This rule tells us the attackers were using brute force to guess passwords! 🔓

This lab helps us practice being cyber detectives and learn how to use tools like Wazuh to protect our computers better! 💪