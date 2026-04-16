Imagine the internet is like a neighborhood full of houses sending letters to each other. Every letter has a sender's address, a receiver's address, and something inside.

Wireshark is like being a mail inspector — you catch every letter flying through the neighborhood in real time and read what's inside.

In this lab, I set up Wireshark on my computer and started intercepting traffic. First I looked at DNS — that's your computer asking "What's the address for google.com?" and getting an answer back. Then ARP, which is computers asking "Who lives at this IP?" to figure out who's who on the local network.

Then I compared two types of mail: regular HTTP letters — totally readable, you can see everything inside — vs HTTPS letters, which are sealed in a locked box. Encrypted. Even if you catch them, you can't read them.

The most interesting part? I opened a PCAP file — basically a recorded mailbag from a real malware investigation. I found one suspicious house: 10.2.28.88. It was sending messages outside the neighborhood to addresses I didn't recognize.

But here's the twist: not all of it was actually suspicious. Some of the traffic was just Windows doing normal Windows things — checking if the internet works, talking to the domain controller. A good investigator figures out what's normal first, then focuses on what's actually weird.

That's the job. Know your baseline. Everything else stands out.
