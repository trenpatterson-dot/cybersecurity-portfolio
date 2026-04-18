# TryHackMe - File Inclusion

## Overview
This room focused on Local File Inclusion (LFI) vulnerabilities and how attackers can exploit improperly validated user input to access sensitive files on a server.

## Skills Practiced
- Identifying Local File Inclusion (LFI) vulnerabilities
- Exploiting file inclusion via URL parameters
- Using directory traversal techniques
- Understanding insecure PHP include() usage

## Key Concepts

### Local File Inclusion (LFI)
LFI occurs when a web application includes files based on user input without proper validation, allowing attackers to access sensitive files.

### Directory Traversal
Attackers can use sequences like:

```bash
../../../
Exploitation Process
Lab 1: Basic File Inclusion
Identified vulnerable parameter:
lang
Exploited by accessing:
/lab1.php?lang=../../../etc/passwd
Successfully retrieved system file:
/etc/passwd
Lab 2: Directory Restriction Bypass
Application restricted file inclusion to a specific directory:
include("languages/" . $_GET["lang"]);
Bypassed restriction using directory traversal techniques
Findings
## Impact

- Exposure of sensitive system files (e.g., /etc/passwd)
- Potential for credential harvesting
- Increased risk of further exploitation (e.g., remote code execution)
Sensitive files such as /etc/passwd can be accessed
Improper input validation leads to unauthorized file access
Directory restrictions can be bypassed if not properly enforced
Key Learning

Input validation is critical. Applications should never trust user input when including files.
## Mitigation

- Validate and sanitize all user input
- Use allowlists for file inclusion
- Avoid direct use of user input in include() functions
- Implement proper access controls
Takeaway

LFI vulnerabilities can expose critical system files and should be mitigated using strict input validation and secure coding practices.

Personal Reflection
This type of vulnerability is commonly found in poorly secured web applications and is often exploited during real-world penetration tests.
This room helped me understand how attackers exploit file inclusion vulnerabilities in real-world scenarios. It reinforced the importance of secure coding and proper input validation when handling user input in web applications.
