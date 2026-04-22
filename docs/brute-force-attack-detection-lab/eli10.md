I have everything I need. The previous ELI10 passed QA cleanly — the QA issues were against the `readme` and `linkedin` outputs, not `eli10`. The prior ELI10 is solid, but I'll write a fresh, clean version grounded strictly in confirmed evidence.

# Brute Force Attack Detection Lab

## What Is a Brute Force Attack?

Imagine a thief trying every single key on a giant keyring to unlock your front door. They don't know which key works — they just keep trying until one fits. That's a **brute force attack**, but on a computer instead of a door.

## What Was This Lab?

Two pretend computers were set up inside a safe, private network. One was the **attacker** (running Kali Linux). The other was the **target** (running Ubuntu). They couldn't hurt anything real — it was all contained, like a fire drill.

## What Did They Do?

First, they made sure the two computers could talk to each other. Then the target had its **SSH service** switched on. SSH is basically a remote door — it lets someone log into a computer over a network.

Then a tool called **Hydra** was used on the attacker machine. Hydra automatically tried password after password for the username *tren*, like a robot trying every key on that giant keyring. A tool called **Wireshark** watched and recorded all that frantic knocking happening on the network in real time.

## What Was Found?

A security alarm system called **Wazuh** was watching the whole time. It caught the attack automatically — no human had to intervene. It fired **10 alerts** and correctly identified the problem as repeated failed SSH logins. The best part? **Zero passwords worked.** The attack completely failed. Wazuh also automatically matched the attack to a real hacker playbook called **MITRE ATT&CK**, tagging it as a known password-guessing technique.

## Why Does This Matter?

This lab proves a properly set-up alarm system can catch an attack the moment it starts — even without anyone watching. It also showed exactly what's missing without the right defenses: things like auto-blocking repeat login attempts, using keys instead of passwords, and having Wazuh automatically ban the attacker's IP. You can't defend against attacks you can't see. 🔐