$log = Join-Path $env:USERPROFILE ".openclaw\logs\lock-cleanup.log"
if (Test-Path $log) {
    Get-Content $log -Tail 3
} else {
    Write-Output "No cleanup log found"
}
