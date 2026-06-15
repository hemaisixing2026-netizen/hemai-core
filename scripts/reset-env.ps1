# reset-env.ps1 — OpenClaw env rollback
# Created: 2025-06-05 | Source: model switch env pollution incident

param(
    [switch]$snapshot,
    [switch]$reset,
    [switch]$list
)

$watchVars = @(
    'OPENROUTER_API_KEY', 'OPENAI_API_KEY', 'ANTHROPIC_API_KEY',
    'DEEPSEEK_API_KEY', 'BAIDU_API_KEY', 'BAIDU_BCE_BEARER_TOKEN',
    'BAIDU_VISION_API_KEY', 'HTTPS_PROXY', 'HTTP_PROXY', 'NO_PROXY', 'NODE_ENV'
)
$snapshotFile = "G:\openclaw-workspace\data\env-snapshot.json"

function Get-EnvVal($v) {
    $val = [Environment]::GetEnvironmentVariable($v, 'Process')
    if ($null -eq $val) { $val = [Environment]::GetEnvironmentVariable($v, 'User') }
    if ($null -eq $val) { $val = [Environment]::GetEnvironmentVariable($v, 'Machine') }
    return $val
}

if ($list) {
    Write-Host "=== Monitored Env Vars ===" -ForegroundColor Cyan
    foreach ($v in $watchVars) {
        $val = Get-EnvVal $v
        Write-Host "  $v = " -NoNewline
        if ($null -eq $val) { Write-Host "(null)" -ForegroundColor DarkGray } 
        elseif ($val -match '^sk-|^sk-or-') { Write-Host "$($val.Substring(0,12))... (masked)" -ForegroundColor Yellow }
        else { Write-Host $val }
    }
    exit
}

if ($snapshot) {
    $data = @{}
    foreach ($v in $watchVars) {
        $data[$v] = Get-EnvVal $v
    }
    $data['_timestamp'] = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
    $data | ConvertTo-Json -Depth 1 | Set-Content $snapshotFile -Encoding UTF8
    Write-Host "[OK] Snapshot saved to $snapshotFile" -ForegroundColor Green
    exit
}

if ($reset) {
    if (-not (Test-Path $snapshotFile)) {
        Write-Host "[FAIL] No snapshot file. Run -snapshot first." -ForegroundColor Red
        exit 1
    }
    $knownGood = Get-Content $snapshotFile -Encoding UTF8 | ConvertFrom-Json
    Write-Host "=== Rolling back env vars ===" -ForegroundColor Yellow
    foreach ($v in $watchVars) {
        $current = Get-EnvVal $v
        $target = $knownGood.$v
        if ($current -ne $target) {
            if ($null -eq $target) {
                [Environment]::SetEnvironmentVariable($v, $null, 'Process')
                Write-Host "  [CLEAR] $v" -ForegroundColor Magenta
            } else {
                [Environment]::SetEnvironmentVariable($v, $target, 'Process')
                Write-Host "  [SET] $v" -ForegroundColor Green
            }
        }
    }
    Write-Host "[OK] Env vars restored to snapshot: $($knownGood._timestamp)" -ForegroundColor Green
    exit
}

Write-Host "OpenClaw Env Rollback Tool"
Write-Host "  -snapshot   Save current monitored env vars"
Write-Host "  -reset      Restore to last snapshot"
Write-Host "  -list       List all monitored vars"
