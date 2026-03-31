# 🖥️ Windows Active Directory Lab

## 📌 Overview
This lab demonstrates the configuration and management of Active Directory components including users, computers, organizational units (OUs), security groups, permissions, and Group Policy Objects (GPOs).

---

## 🛠️ Tools Used
- Windows Server
- Active Directory Users and Computers
- Group Policy Management

---

## 👤 User Creation
Users were created and configured with appropriate logon names.

![Users](images/figure1-users-created.png)

---

## 💻 Computer Objects
Computer objects were created and added to Active Directory.

![Computers](images/figure2-computers-created.png)

---

## 🗂️ Organizational Units (OUs)
Organizational Units were created to logically group users and resources.

![OUs](images/figure3-organizational-units.png)

---

## ⚔️ OU Assignment

### Rebel Alliance OU
![Rebel Alliance](images/figure4-rebel-alliance-ou.png)

### Galactic Empire OU
![Galactic Empire](images/figure5-galactic-empire-ou.png)

---

## 🔐 Security Groups

### Rebel Alliance Groups
- JediKnights  
![Jedi](images/figure6-jedi-knights-group.png)

- Leadership  
![Leadership](images/figure7-leadership-group.png)

- RebelForces  
![Rebel Forces](images/figure8-rebel-forces-group.png)

---

### Galactic Empire Groups
- SithLords  
![Sith](images/figure9-sith-lords-group.png)

- Executives  
![Executives](images/figure10-executives-group.png)

- GalacticForces  
![Forces](images/figure11-galactic-forces-group.png)

---

## 🔑 Access Control
Permissions were assigned to users and groups, including granting Full Control access.

![Permissions](images/figure12-permissions-summary.png)

---

## ⚙️ Advanced Permissions
Granular permissions were configured based on requirements:
- Objects cannot be deleted  
- Access cannot be restricted by opposing groups  
- Permissions support continuous knowledge growth  

### SithLords Permissions
![Sith Permissions](images/figure13-sith-permissions.png)

### JediKnights Permissions
![Jedi Permissions](images/figure14-jedi-permissions.png)

---

## 🛡️ Group Policy Objects (GPO)

A logon message policy was created for the Rebel Alliance.

### Title Configuration
![GPO Title](images/figure15-gpo-title.png)

### Message Configuration
![GPO Message](images/figure16-gpo-message.png)

### Policy Applied
![GPO Console](images/figure17-group-policy-console.png)

---

## 🧠 Key Takeaways
- Active Directory is critical for managing enterprise environments  
- Organizational Units help structure and manage resources  
- Security groups simplify permission management  
- Group Policy enforces security settings across systems  
- Proper access control is essential for security and compliance  

---

## 📸 Screenshots
All screenshots document the configuration and validation of Active Directory components.