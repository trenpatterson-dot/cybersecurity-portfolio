# Command History / Query Notes

Review alert summary:
Get-Content .\evidence\alert-summary.md

Review simulated PowerShell events:
Import-Csv .\evidence\powershell-events.csv | Format-Table

Filter PowerShell activity:
Import-Csv .\evidence\powershell-events.csv | Where-Object {$_.FileName -eq "powershell.exe"}

Filter bypass-style arguments:
Import-Csv .\evidence\powershell-events.csv | Where-Object {$_.ProcessCommandLine -like "*ExecutionPolicy Bypass*"}

Filter suspicious web request behavior:
Import-Csv .\evidence\powershell-events.csv | Where-Object {$_.ProcessCommandLine -like "*Invoke-WebRequest*"}

Review KQL-style query:
Get-Content .\queries\investigation-query.kql
