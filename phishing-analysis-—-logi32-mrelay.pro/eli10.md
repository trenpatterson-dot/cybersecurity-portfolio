# Phishing Analysis — logi32-mrelay.pro

## What Was This Lab?

Imagine someone sends you a suspicious-looking address. This lab was like being a detective handed one of those addresses — a sketchy website called **logi32-mrelay.pro** — and figuring out if it was dangerous.

## What Did the Analyst Do?

The analyst used special investigator tools called **URLScan.io** and **VirusTotal**. Think of them like X-ray machines for websites. They scanned the address to see what was hiding inside.

First, VirusTotal checked it against **90 antivirus engines** — and got zero flags. Total clean bill of health. But the analyst wasn't fooled.

## The Sneaky Trick

Here's the clever part. This website was playing a trick called **conditional redirect evasion**. When a robot scanner visited the site, it got sent straight to a real, harmless news website (Le Monde, a French newspaper). "Nothing to see here!"

But real victims? They'd get the actual phishing trap.

It's like a criminal putting a fake bookshelf door in front of their hideout. Inspectors see a bookshelf. Victims walk right through it.

## What Was Found?

When the analyst ran the scan a **second time**, the disguise had slipped — and now **6 out of 95** security vendors flagged it as **phishing/malicious**. On top of that, the site had several red flags:

- The domain was only **~1 month old** — classic throwaway setup
- It used a sneaky **PHP script** (`/as.php`) to decide who gets the trap
- The name `logi32-mrelay.pro` is random gibberish — a dead giveaway
- It hid behind **Cloudflare**, making it hard to trace the real criminal

**Verdict: MALICIOUS** ✅

## Why Does This Matter?

This lab proves that **robots can be fooled, but humans can't be — if they know what to look for.** Trusting only automated tools would have missed this threat entirely. Manual detective work caught what 90 scanners missed.