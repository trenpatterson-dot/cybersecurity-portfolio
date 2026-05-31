# IAM-001 Failed Authentication Investigation

## Objective
Generate and investigate failed Active Directory authentication attempts.

## Event Observed
- Event ID: 4625
- Event Name: An account failed to log on
- Target Account: TRENLAB\test-user
- Domain: TRENLAB
- Logon Type: 2
- Failure Status: 0xC000006D
- Failure Substatus: 0xC000006A

## What Happened
The test-user account attempted to authenticate with an incorrect password. The failed attempts generated Windows Security Event ID 4625.

## Analyst Findings
The failed login attempts were caused by intentional lab testing. The substatus code 0xC000006A confirmed that the failure was due to an incorrect password.

## Assessment
Benign lab-generated activity.

## Evidence
- detection-failed-domain-login
- detection-failed-domain-login-details

# IAM-002 Account Lockout Investigation

## Objective
Configure an account lockout policy and investigate a locked Active Directory account.

## Event Observed
- Event ID: 4740
- Event Name: A user account was locked out
- Target Account: TRENLAB\test-user
- Caller Computer: WIN-UI0N9PGJUEU
- Lockout Threshold: 3 invalid logon attempts

## What Happened
The test-user account was locked after three failed authentication attempts. The lockout was enforced by the domain account lockout policy.

## Analyst Findings
The account lockout was expected and caused by intentional lab testing. Event ID 4740 confirmed that Active Directory locked the account.

## Assessment
Benign lab-generated activity.

## Evidence
- gpo-account-lockout-threshold
- test-user-account-locked
- detection-account-lockout


# IAM-003 Privileged Access Investigation

## Objective
Monitor and investigate Active Directory security group membership changes.

## Events Generated

### Event ID 4728
A member was added to a security-enabled global group.

Actor:
TRENLAB\Administrator

Affected User:
TRENLAB\soc-analyst

Group:
Security-Analysts

Result:
User successfully added to security group.

### Event ID 4729
A member was removed from a security-enabled global group.

Actor:
TRENLAB\Administrator

Affected User:
TRENLAB\soc-analyst

Group:
Security-Analysts

Result:
User successfully removed from security group.

# IAM-004 User Lifecycle Monitoring

## Objective
Monitor and investigate Active Directory user lifecycle events.

## Event 4720 - User Created
Administrator created contractor-user.

## Event 4724 - Password Reset
Administrator reset the password for contractor-user.

## Event 4738 - User Modified
Administrator modified account attributes for contractor-user.

## Event 4726 - User Deleted
Administrator deleted contractor-user.

## Findings
The complete user lifecycle was successfully generated and validated through Windows Security Event Logs. All actions were attributable to the Administrator account and were captured by Active Directory auditing.

# IAM-005 Privileged Access Monitoring

## Objective
Investigate privileged group membership changes in Active Directory.

## Events Observed
- Event ID: 4728 - A member was added to a security-enabled global group
- Event ID: 4729 - A member was removed from a security-enabled global group

## Group Monitored
- Tier1-Admins

## What Happened
The Tier1-Admins security group was created to simulate privileged access management. HelpDesk User and Test User were added to the group and then removed to generate membership change events.

## Analyst Findings
The Administrator account performed the group membership changes. HelpDesk User represented an expected privileged access assignment. Test User represented a suspicious privilege escalation scenario requiring validation.

## Assessment
Expected lab-generated activity, with Test User treated as a simulated suspicious access change.

## Evidence
- tier1-admins-group-created
- tier1-admins-helpdesk-added
- tier1-admins-member-added-event-4728
- tier1-admins-test-user-event-4728
- tier1-admins-helpdesk-removed-event-4729
- tier1-admins-test-user-removed-event-4729
