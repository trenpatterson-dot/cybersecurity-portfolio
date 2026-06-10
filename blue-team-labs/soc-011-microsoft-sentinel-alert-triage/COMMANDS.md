# Command History / Query Notes

Review alert summary:

```powershell
Get-Content .\evidence\alert-summary.md
```

Review simulated sign-in events:

```powershell
Import-Csv .\evidence\signin-events.csv | Format-Table
```

Filter the reserved suspicious source IP:

```powershell
Import-Csv .\evidence\signin-events.csv | Where-Object {$_.IPAddress -eq "203.0.113.45"}
```

Filter failed sign-ins:

```powershell
Import-Csv .\evidence\signin-events.csv | Where-Object {$_.Result -eq "Failure"}
```

Check for successful authentication from the suspicious source:

```powershell
Import-Csv .\evidence\signin-events.csv | Where-Object {$_.IPAddress -eq "203.0.113.45" -and $_.Result -eq "Success"}
```

Review the KQL-style investigation query:

```powershell
Get-Content .\queries\investigation-query.kql
```
