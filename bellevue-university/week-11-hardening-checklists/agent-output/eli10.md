# Hardening Checklists — ELI10

This lab was about making a computer harder to attack.

I used a tool called Lynis on Ubuntu. Lynis checks the system and points out weak spots. First, I ran a baseline scan to see where the system stood before making changes. Then I started locking things down.

I turned off services I did not need, like printing, device discovery, and Bluetooth. That matters because every extra service is one more thing that could be abused. I also hardened SSH, which is a way to remotely connect to Linux systems. I changed settings to block root login, limit login attempts, shorten login time, and disable features I did not need.

Then I improved the password policy so passwords had to be longer and more complex. After that, I ran Lynis again. My hardening score improved from 58 to 63.

I could not finish the Windows half because the required Windows Server 2022 virtual machine was not available. The machine I checked turned out to be Windows 11 Home instead. Still, the Ubuntu side gave me real proof of hardening work and showed how small security changes add up.
