# Analysis

## Investigation Goal

Analyze suspicious network traffic and determine what happened, what evidence supports it, and whether the activity requires escalation.

## Analyst Workflow

1. Review the original alert, capture, or log source.
2. Identify the source IP, destination IP, protocol, port, and timestamp.
3. Confirm the traffic volume and timing.
4. Check whether the activity matches expected behavior for the environment.
5. Look for related events, repeated patterns, or successful connections.
6. Determine whether the traffic appears benign, suspicious, malicious, or lab-generated.
7. Document the final analyst conclusion with supporting evidence.

## Evidence To Validate

- Detection source or capture tool
- Event timestamps
- Source IP address
- Destination IP address
- Protocol and destination port
- Hostnames or services involved
- Traffic count, duration, or frequency
- Related alerts or correlated logs
- Screenshots, packet captures, or exported event details

## Analyst Notes

Use this section to capture investigation notes as evidence is reviewed.

- Detection source:
- Alert or event name:
- Source IP:
- Destination IP:
- Protocol:
- Destination port:
- Host or service:
- Traffic pattern:
- Related events:
- Initial classification:
- Final classification:

## Decision Point

The final write-up should answer these questions clearly:

- Was the activity confirmed or only suspected?
- Did the traffic match expected behavior?
- Was the pattern isolated or repeated?
- Did any connection succeed or move laterally?
- What action would a SOC analyst take next?
