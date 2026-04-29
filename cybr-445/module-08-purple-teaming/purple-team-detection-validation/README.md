# Purple Team Detection Validation with Atomic Red Team, Caldera, Kibana, and VECTR

## Overview

This project summarizes a controlled purple-team validation exercise focused on detection visibility across discovery and credential-access behavior. The work used hands-on testing, adversary-emulation style automation, SIEM review, and structured documentation to confirm that defensive tooling surfaced recognizable attacker activity.

## Objective

Validate whether a monitored lab environment could detect selected ATT&CK-aligned behaviors, review the resulting alert coverage, and document outcomes in a way that supports blue-team analysis and defensive improvement.

## Tools Used

- Atomic Red Team
- Caldera
- Elastic/Kibana
- VECTR
- PowerShell
- Windows command line
- MITRE ATT&CK

## Techniques Tested

- Software discovery activity
- System owner and user discovery
- Network share enumeration
- Administrator account enumeration
- LSASS memory access behavior associated with credential dumping

## Detection Validation Summary

The exercise validated that multiple discovery and credential-access behaviors generated recognizable detections in the monitoring stack. From a SOC perspective, the value was not just that alerts fired, but that the alerts aligned to specific attacker behaviors that defenders should be able to investigate and triage quickly.

## VECTR Documentation Summary

VECTR was used to record the purple-team exercise in a structured way, including technique coverage, observed outcomes, severity, and defensive mapping. That documentation step turned testing activity into a repeatable detection-validation record instead of a one-off lab run.

## SOC Analyst Skills Demonstrated

- Mapping attacker behavior to ATT&CK techniques
- Validating SIEM and EDR detections against controlled test activity
- Reviewing detection output for investigation relevance
- Translating technical test activity into defensive findings
- Documenting detection outcomes and severity in a structured workflow

## Key Takeaways

- Detection validation is stronger when manual testing and automation are combined.
- Discovery activity should be treated seriously because it often appears early in attack chains.
- Credential-access detections carry higher defensive value because they can indicate direct risk to accounts and privileged access.
- Structured documentation improves repeatability and makes detection coverage easier to communicate.

## Privacy Note

Screenshots, raw reports, and assignment documents are retained locally due to lab environment privacy. This public version summarizes the workflow and results without exposing private lab infrastructure.
