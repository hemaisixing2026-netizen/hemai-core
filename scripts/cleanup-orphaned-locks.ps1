# 清理OpenClaw会话孤儿锁文件
# 扫描.lock文件，如果锁中记录的进程已不存在，删除锁文件
$sessionsDir = "$env:USERPROFILE\.openclaw\agents\main\sessions"
$locks = Get-ChildItem $sessionsDir -Filter "*.jsonl.lock" -ErrorAction SilentlyContinue

if (-not $locks) { exit 0 }

$cleaned = 0
foreach ($lock in $locks) {
    # 尝试从锁文件读取进程ID（新版OpenClaw可能在锁文件中记录PID）
    # 如果读不到PID，检查对应jsonl文件是否被其他进程占用
    $jsonlPath = $lock.FullName -replace '\.lock$', ''
    
    # 检查是否有进程持有该文件
    $handle = $null
    try {
        $handle = [System.IO.File]::Open($jsonlPath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::ReadWrite, [System.IO.FileShare]::None)
        $handle.Dispose()
        # 能打开说明没锁，锁文件是孤儿的
        Remove-Item $lock.FullName -Force
        $cleaned++
    } catch {
        # 文件被占用，锁是活的不清理
        continue
    } finally {
        if ($handle) { $handle.Dispose() }
    }
}

if ($cleaned -gt 0) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    "$timestamp | 清理了 $cleaned 个孤儿锁文件" | Out-File "$env:USERPROFILE\.openclaw\logs\lock-cleanup.log" -Append
}
