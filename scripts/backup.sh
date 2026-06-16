#!/bin/bash
# 思行备份脚本 · 双身通用
# Cron: 每日03:00 执行
# 功能：快照核心文件 → backups/YYYY-MM-DD/ → 7天轮转 → 同步G盘

set -e
TIMESTAMP="$(date +%Y-%m-%d)"
WORKSPACE="/root/workspace"
BACKUP_DIR="$WORKSPACE/backups/$TIMESTAMP"
GDRIVE="/mnt/g/openclaw-workspace"
RETENTION_DAYS=7

echo "=== 思行备份 · $TIMESTAMP ==="

# 1. 创建备份目录
mkdir -p "$BACKUP_DIR"

# 2. 核心文件快照
CORE_FILES=(
    "SOUL.md"
    "IDENTITY.md"
    "MEMORY.md"
    "USER.md"
    "HEARTBEAT.md"
    "AGENTS.md"
    "LEARNING.md"
    "TOOLS.md"
    "WORKING_PRINCIPLES.md"
    "DAILY_TRACKER.md"
)

for f in "${CORE_FILES[@]}"; do
    if [ -f "$WORKSPACE/$f" ]; then
        cp "$WORKSPACE/$f" "$BACKUP_DIR/"
        echo "📄 $f"
    fi
done

# 3. 关键目录快照
cp -r "$WORKSPACE/rules" "$BACKUP_DIR/" 2>/dev/null
cp -r "$WORKSPACE/data" "$BACKUP_DIR/" 2>/dev/null
cp -r "$WORKSPACE/private" "$BACKUP_DIR/" 2>/dev/null
cp -r "$WORKSPACE/archive" "$BACKUP_DIR/" 2>/dev/null
cp -r "$WORKSPACE/memory" "$BACKUP_DIR/" 2>/dev/null
echo "📁 rules/ data/ private/ archive/ memory/"

# 4. 同步到 G 盘（如果已挂载）
if [ -d "$GDRIVE" ]; then
    # 核心文件同步
    for f in "${CORE_FILES[@]}"; do
        if [ -f "$WORKSPACE/$f" ]; then
            cp "$WORKSPACE/$f" "$GDRIVE/$f"
        fi
    done
    # 目录同步
    cp -r "$WORKSPACE/memory" "$GDRIVE/" 2>/dev/null
    echo "🔄 已同步到 G 盘"
else
    echo "⚠️  G 盘未挂载，跳过同步"
fi

# 5. 7天轮转清理
find "$WORKSPACE/backups" -maxdepth 1 -type d -name "20*" | sort | head -n -$RETENTION_DAYS | while read old; do
    rm -rf "$old"
    echo "🗑️  清理: $(basename $old)"
done

echo "=== 完成 ==="

# 私人仓库全量快照（不公开）
bash /root/workspace/scripts/backup-to-private.sh 2>&1 | tee -a /root/workspace/backups/backup.log
