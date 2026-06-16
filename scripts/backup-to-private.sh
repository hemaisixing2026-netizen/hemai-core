#!/bin/bash
# 思行·私人备份——全量打包推送到私人仓库
# 每天03:00由cron触发
set -e

PRIVATE_REPO="git@ssh.github.com:hemaisixing2026-netizen/hemai-private.git"
WORK_DIR="/root/workspace"
BACKUP_DIR="/tmp/hemai-private-backup"
TIMESTAMP=$(date +%Y-%m-%d_%H%M)

# 克隆私人仓库（浅克隆，节省空间）
rm -rf "$BACKUP_DIR"
git clone --depth 1 "$PRIVATE_REPO" "$BACKUP_DIR" 2>/dev/null || git clone "$PRIVATE_REPO" "$BACKUP_DIR"

cd "$BACKUP_DIR"

# 创建当日备份目录
mkdir -p "snapshots/$TIMESTAMP"

# 全量复制workspace（排除.git和node_modules）
rsync -a --exclude='.git' --exclude='node_modules' --exclude='__pycache__' \
    "$WORK_DIR/" "snapshots/$TIMESTAMP/"

# 提交推送
git add -A
git commit -m "🦴 私人备份 $TIMESTAMP" || { echo "无变更"; exit 0; }
git push origin main

# 清理7天前的快照
find snapshots/ -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null || true

echo "✅ 私人备份完成: snapshots/$TIMESTAMP"
rm -rf "$BACKUP_DIR"