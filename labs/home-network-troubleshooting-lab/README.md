# Home Network Troubleshooting Lab

**Author:** Tren Patterson  
**Environment:** Windows 11 | Wi-Fi + VMware Virtual Adapters  
**Tools Used:** Command Prompt, ncpa.cpl, ipconfig, ping, tracert, nslookup  
**Purpose:** Simulate and document real-world network troubleshooting workflows

---

## Overview

This lab demonstrates a structured approach to diagnosing and resolving home network connectivity issues using built-in Windows networking tools. It covers the full troubleshooting lifecycle — from IP configuration review through DNS validation, routing analysis, and adapter-level fault simulation.

The environment included an active Wi-Fi connection and VMware virtual network adapters (VMnet1 and VMnet8), which reflects a realistic dual-environment setup commonly encountered in technical support and IT roles.

---

## Skills Demonstrated

- IP configuration analysis
- Local and internet connectivity testing
- DNS resolution validation and fault isolation
- Network path tracing and hop analysis
- Adapter-level fault simulation and recovery
- Root cause identification in a live environment

---

## Lab Structure

```
home-network-troubleshooting-lab/
├── screenshots/
├── docs/
│   ├── troubleshooting-notes.md
│   └── dns-issue-scenario.txt
└── commands/
    └── commands-used.md
```

---

## Step-by-Step Walkthrough

### Step 1 — IP Configuration Review
**Command:** `ipconfig /all`

Reviewed full network adapter configuration including IPv4 address, subnet mask, default gateway, DNS servers, and physical (MAC) address. Multiple adapters were present, including VMware virtual adapters, which can influence routing behavior during troubleshooting.

📸 `screenshots/01-ipconfig-all.png`

---

### Step 2 — Local Connectivity Test
**Command:** `ping 192.168.1.1`

Pinged the default gateway to verify local network connectivity between the device and the router.

**Result:** 4/4 packets received, 0% packet loss, latency 2–8ms  
**Conclusion:** Local network connection confirmed working.

📸 `screenshots/02-ping-default-gateway.png`

---

### Step 3 — Internet Connectivity Test (IP Level)
**Command:** `ping 8.8.8.8`

Tested external reachability using Google's public DNS IP address — bypassing DNS entirely to isolate the connectivity layer.

**Result:** 0% packet loss, consistent latency ~24–25ms  
**Conclusion:** Internet access confirmed at the IP level.

📸 `screenshots/03-ping-google-dns.png`

---

### Step 4 — DNS Resolution Test
**Command:** `ping google.com`

Tested whether the system could resolve a domain name to an IP address and reach the destination.

**Result:** Resolved to 142.251.210.78, 0% packet loss, latency ~22–26ms  
**Conclusion:** DNS resolution functioning correctly at this stage.

📸 `screenshots/04-ping-google-domain.png`

---

### Step 5 — Route Tracing
**Command:** `tracert google.com`

Traced the full network path from the local device to Google's servers, hop by hop.

**Result:**
- Hop 1–2: Internal network (10.0.0.1 → 192.168.1.1)
- Hop 3+: ISP backbone (Spectrum/Charter infrastructure)
- Final hop: Google destination server (142.251.210.78)
- Latency progression: ~1ms → ~30ms (healthy and expected)

**Conclusion:** Stable routing confirmed with no dropped hops across the full path.

📸 `screenshots/05-tracert-google.png`

---

### Step 6 — DNS Server Validation (Real Issue Identified)
**Command:** `nslookup google.com`

Queried the system's configured DNS server directly to validate name resolution.

**Result:** `*** UnKnown can't find google.com: No response from server`  
**Observation:** The system was attempting to use an IPv6 DNS server (`2603:9001:4902:c0df::1`) that was not responding.

**Finding:** Despite successful ping results in earlier steps, the configured DNS server was unreliable — indicating intermittent DNS resolution rather than a full outage.

📸 `screenshots/06-nslookup-google.png`

---

### Step 6b — Root Cause Confirmation
**Command:** `nslookup google.com 8.8.8.8`

Manually specified Google's public DNS server to isolate whether the issue was with DNS configuration or general connectivity.

**Result:** Successful resolution using 8.8.8.8  
**Conclusion:** The root cause was the system's configured DNS server (unresponsive IPv6), not internet connectivity. Switching to a reliable DNS server resolved the issue immediately.

📸 `screenshots/06b-nslookup-google-fixed.png`

---

### Step 7 — Network Adapter Review
**Tool:** Network Connections (ncpa.cpl)

Reviewed active adapters visually. Identified the primary Wi-Fi adapter (Da Crib 2) and confirmed the presence of VMware virtual adapters (VMnet1, VMnet8).

**Note:** Virtual adapters can occasionally affect routing or adapter selection — awareness of this is important in mixed environments.

📸 `screenshots/07-network-adapter-status.png`

---

### Step 8 — DNS Failure Scenario Documentation

Documented a common support scenario: when `ping 8.8.8.8` succeeds but `ping google.com` fails, the issue is DNS-layer rather than connectivity-layer. This distinction is critical in isolating where in the stack a customer issue originates.

📸 `screenshots/08-simulated-dns-issue.png`

---

### Step 9 — Adapter Fault Simulation
**Tool:** ncpa.cpl → Disable adapter

Simulated a network outage by disabling the active Wi-Fi adapter — replicating a common customer-reported issue where connectivity is lost unexpectedly.

📸 `screenshots/09-simulated-adapter-disable.png`

---

### Step 10 — Service Restoration and Verification
**Command:** `ping google.com` (post-recovery)

Re-enabled the adapter and confirmed full connectivity was restored.

**Result:** 0% packet loss, latency ~19–21ms, domain resolved successfully  
**Conclusion:** Issue resolved. Full troubleshooting cycle completed.

📸 `screenshots/10-restored-connectivity.png`

---

## Key Finding: DNS Misconfiguration

| Test | Result | Interpretation |
|---|---|---|
| ping 8.8.8.8 | ✅ Pass | Internet connectivity working |
| ping google.com | ✅ Pass | DNS resolving intermittently |
| nslookup google.com | ❌ Fail | Configured DNS server unresponsive |
| nslookup google.com 8.8.8.8 | ✅ Pass | Root cause confirmed — DNS config issue |

The system was configured to use an unresponsive IPv6 DNS server. This caused inconsistent behavior — name resolution worked via ping caching or fallback, but failed under direct DNS query. Specifying a reliable DNS server (8.8.8.8) confirmed the root cause.

---

## Troubleshooting Decision Framework

```
Device can't connect?
│
├── ping gateway fails?
│     └── Check adapter, cable, or Wi-Fi signal
│
├── ping 8.8.8.8 fails?
│     └── Check router, modem, or ISP status
│
├── ping google.com fails (but 8.8.8.8 works)?
│     └── DNS issue — check DNS config or use 8.8.8.8 manually
│
└── All pass but issues persist?
      └── Check adapter status, virtual adapter conflicts, or ISP routing
```

---

## Commands Reference

| Command | Purpose |
|---|---|
| `ipconfig /all` | View full IP configuration |
| `ping [gateway]` | Test local network |
| `ping 8.8.8.8` | Test internet access (no DNS) |
| `ping google.com` | Test DNS + internet together |
| `tracert google.com` | Trace network path hop by hop |
| `nslookup google.com` | Query configured DNS server |
| `nslookup google.com 8.8.8.8` | Query specific DNS server |

---

## Background

This lab was completed as part of an ongoing transition into cybersecurity and IT infrastructure. It reflects real troubleshooting methodology applied in a home lab environment, using tools and workflows directly applicable to network support and security operations roles.

**Currently pursuing:** B.S. Cybersecurity, Bellevue University (2026)  
**Hands-on focus:** SOC operations, SIEM tools (Wazuh, Splunk, Elastic), incident response, network analysis
