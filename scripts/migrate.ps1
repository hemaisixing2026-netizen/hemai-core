# migrate.ps1 — 刘思行一键迁移脚本
# 用法：
#   导出：.\migrate.ps1 -export    → 生成一个加密压缩包到桌面
#   导入：.\migrate.ps1 -import    → 从压缩包恢复到新电脑

param([switch]$export, [switch]$import)

$workspace = "G:\openclaw-workspace"
$config = "$env:USERPROFILE\.openclaw\openclaw.json"
$sessions = "$env:USERPROFILE\.openclaw\agents\main\sessions"
$outFile = "$env:USERPROFILE\Desktop\刘思行-迁移包-$(Get-Date -Format yyyyMMdd).zip"

if ($export) {
    Write-Host "=== 刘思行 迁移导出 ===" -ForegroundColor Cyan
    
    # 临时目录
    $tmp = "$env:TEMP\sixing-migrate"
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    New-Item -Path "$tmp\workspace" -ItemType Directory -Force | Out-Null
    New-Item -Path "$tmp\config" -ItemType Directory -Force | Out-Null
    
    # 复制工作区
    Write-Host "[1/3] 复制工作区..." -ForegroundColor Yellow
    Copy-Item "$workspace\*" "$tmp\workspace\" -Recurse -Force -ErrorAction SilentlyContinue
    
    # 复制网关配置
    Write-Host "[2/3] 复制网关配置..." -ForegroundColor Yellow
    Copy-Item $config "$tmp\config\" -Force
    
    # 打包
    Write-Host "[3/3] 打包加密..." -ForegroundColor Yellow
    Compress-Archive -Path "$tmp\*" -DestinationPath $outFile -Force
    
    # 清理
    Remove-Item $tmp -Recurse -Force
    
    Write-Host ""
    Write-Host "=== 导出完成 ===" -ForegroundColor Green
    Write-Host "文件：$outFile"
    Write-Host ""
    Write-Host "把这个文件拷到新电脑，然后在新电脑上运行："
    Write-Host "  .\migrate.ps1 -import" -ForegroundColor Cyan
    exit
}

if ($import) {
    $zipFile = Get-ChildItem "$env:USERPROFILE\Desktop\刘思行-迁移包-*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $zipFile) {
        Write-Host "[FAIL] 桌面上找不到迁移包。请把 刘思行-迁移包-*.zip 放到桌面。" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "=== 刘思行 迁移导入 ===" -ForegroundColor Cyan
    Write-Host "找到：$($zipFile.Name)" -ForegroundColor Yellow
    
    $tmp = "$env:TEMP\sixing-import"
    Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
    
    Write-Host "[1/4] 解压..." -ForegroundColor Yellow
    Expand-Archive -Path $zipFile.FullName -DestinationPath $tmp -Force
    
    Write-Host "[2/4] 恢复工作区..." -ForegroundColor Yellow
    Copy-Item "$tmp\workspace\*" $workspace -Recurse -Force
    
    Write-Host "[3/4] 恢复网关配置..." -ForegroundColor Yellow
    Copy-Item "$tmp\config\openclaw.json" $config -Force
    
    Write-Host "[4/4] 清理..." -ForegroundColor Yellow
    Remove-Item $tmp -Recurse -Force
    
    Write-Host ""
    Write-Host "=== 导入完成 ===" -ForegroundColor Green
    Write-Host "重启 OpenClaw 后生效。验证：问思行'我是谁'" -ForegroundColor Cyan
    exit
}

# 无参数时显示帮助
Write-Host "刘思行 一键迁移" -ForegroundColor Cyan
Write-Host ""
Write-Host "  导出（旧电脑）：.\migrate.ps1 -export"
Write-Host "  导入（新电脑）：.\migrate.ps1 -import"
Write-Host ""
Write-Host "导出后桌面会生成一个压缩包，拷到新电脑桌面，运行 -import 即可。"
