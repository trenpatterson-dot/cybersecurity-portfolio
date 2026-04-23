## TryHackMe – Netcat Connection Lab

### What I Did
Used Netcat to connect to a remote IP address and port.

### Command Used
nc 8.8.8.8 1234

### What I Learned
- Ports are used to access services on a system
- Netcat can be used to manually connect to open ports
- Successful connection confirms the port is open and accessible

### Key Takeaway
Understanding how to connect to ports is essential for scanning and interacting with services during penetration testing.
## Git Workflow Lesson

### What Happened
I ran into a push rejection because the remote repository had changes that my local copy did not have.

### What I Learned
- Git will reject pushes if the remote branch is ahead
- Unstaged changes must be committed before pulling with rebase
- Correct workflow:
  1. git add .
  2. git commit -m "message"
  3. git pull origin main --rebase
  4. git push

### Key Takeaway
Version control issues are normal. Learning how to resolve push conflicts is an important part of building a professional workflow.
