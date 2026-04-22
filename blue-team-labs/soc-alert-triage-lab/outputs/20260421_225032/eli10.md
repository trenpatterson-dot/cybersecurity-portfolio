# What's a Cybersecurity Lab? Let's Explore the SOC Alert Triage Lab! 🕵️‍♂️💻

A cybersecurity lab is like a playground for super-smart people who keep computers safe. In this case, we're talking about the **SOC (Security Operations Center) Alert Triage Lab**. It's an exercise that was done using a tool called Wazuh.

In this lab, imagine there were two machines: one like a fortress (Ubuntu) and another like a sneaky hacker's toolkit (Kali Linux). The goal was to pretend that the hacker tried to break into the fortress by making lots of failed attempts to log in using SSH (Secure Shell). This is called **alert triage** - it's when cybersecurity experts investigate these alerts to figure out if they're real threats.

Here's what happened:
1. The team fixed some problems with the Wazuh tool so it could connect to the internet and work properly.
2. They checked that everything in the Wazuh manager (Ubuntu) and dashboard was working fine.
3. They set up SSH on the Ubuntu fortress machine.
4. They fixed the network settings for the virtual machines.
5. Using Kali Linux, they simulated 9 failed attempts to log into the Ubuntu fortress.

The cool part is that Wazuh detected these attempts and triggered an alert! The team investigated this alert and found out it was a fake user trying to break in. This is important because it helps us understand how to protect our computers better.

Now, they're preparing to write about what they did and share it with others. They also need to organize their findings in a special place called GitHub. 📚🚀