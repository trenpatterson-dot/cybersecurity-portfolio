# Command History / Query Notes

Review alert summary:
Get-Content .\evidence\alert-summary.md

Review simulated endpoint process events:
Import-Csv .\evidence\process-events.csv | Format-Table

Filter PowerShell activity:
Import-Csv .\evidence\process-events.csv | Where-Object {$_.FileName -eq "powershell.exe"}

Filter Office-to-PowerShell process chain:
Import-Csv .\evidence\process-events.csv | Where-Object {$_.InitiatingProcessFileName -eq "winword.exe"}

Filter encoded command activity:
Import-Csv .\evidence\process-events.csv | Where-Object {$_.ProcessCommandLine -like "*EncodedCommand*"}

Review KQL-style query:
Get-Content .\queries\investigation-query.kql
