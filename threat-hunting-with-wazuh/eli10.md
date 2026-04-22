# Threat Hunting with Wazuh

## What's a SIEM, and Why Does This Matter?

Imagine your computer is a house. A **SIEM** (Security Information and Event Management system) is like a super-smart security camera system. It watches *everything* happening inside, records it, and screams an alarm the second something sketchy occurs.

In this lab, the SIEM used was **Wazuh** — a free, powerful tool that real security teams use at actual companies.

---

## What Was Built

A mini fake "internet" was set up using virtual computers (like pretend PCs living inside one real PC). Three machines were created:

- 🖥️ **Wazuh Server** — the brain; watches everything
- 🎯 **Target Computer** — the victim being monitored (Ubuntu Linux + Windows 11)
- 💀 **Kali Linux** — the attacker machine used to launch fake attacks

---

## What Was Done

Two attacks were simulated — on purpose, in a safe lab:

**Attack 1 – Stealing Password Info**
Commands were run to open a secret Linux file called `/etc/shadow`. This file stores scrambled versions of user passwords. A real hacker would love to grab this. Wazuh caught it immediately and flagged it under a known attack technique called **T1003.008**.

**Attack 2 – Brute Force Login**
A script hammered the login system 10 times in a row with bad passwords — like a burglar trying every key on a keyring. Wazuh fired **Rule 5763** within *seconds*, flagging it as a brute force attack (**T1110**).

---

## What Was Found

- Wazuh detected both attacks in **under 10 seconds** ⚡
- A misconfigured agent silently stopped sending logs — *no warning, no alerts*. That's a dangerous blind spot.
- Firewall ports being closed could secretly block computers from being monitored at all.

---

## Why It Matters

Real attackers move fast. This lab proves that a properly set up SIEM can catch them just as fast — and shows exactly what can go wrong when it's *not* set up correctly.