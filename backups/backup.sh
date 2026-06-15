#!/bin/bash
# 思行核心资产每日快照 v2
# Cron: 每日03:00 | no_agent模式

DATE=$(date +%Y-%m-%d)
SRC=/root/workspace
DST=$SRC/backups/$DATE
GDRIVE=/mnt/g/openclaw-workspace
HERMES=/root/.hermes

mkdir -p "$DST"

echo "=== $DATE 快照开始 ==="

# === Tier 1 宪法级 ===
cp $SRC/SOUL.md $SRC/MEMORY.md $SRC/IDENTITY.md $SRC/LEARNING.md $DST/
cp $SRC/HEARTBEAT.md $SRC/AGENTS.md $SRC/WORKING_PRINCIPLES.md $DST/
cp $SRC/USER.md $DST/ 2>/dev/null

# === 绝密加密件 ===
mkdir -p $DST/private-encrypted
cp $SRC/private/encrypted/*.gpg $DST/private-encrypted/ 2>/dev/null

# === Tier 2 执行层 ===
cp $SRC/learnings/ERRORS.md $DST/
cp -r $SRC/rules/ $DST/rules/
cp -r $SRC/data/ $DST/data/

# === Hermes配置 ===
mkdir -p $DST/hermes-config
cp $HERMES/config.yaml $DST/hermes-config/ 2>/dev/null
# 不复制 private.key — 密钥只在本地

# === G盘全量（排除node_modules和.secrets）===
rsync -a --delete --exclude='node_modules' --exclude='.git' \
  $SRC/ "$GDRIVE/" 2>/dev/null
# 加密件同步
cp $SRC/private/encrypted/*.gpg $GDRIVE/private/encrypted/ 2>/dev/null
# G盘明文private/保持空

# === Hermes自加载同步 ===
cp $SRC/SOUL.md $SRC/MEMORY.md $SRC/IDENTITY.md $SRC/LEARNING.md $HERMES/
cp $SRC/HEARTBEAT.md $SRC/AGENTS.md $SRC/WORKING_PRINCIPLES.md $HERMES/

# === 快照标记 ===
echo "快照时间: $(date)" > $DST/SNAPSHOT.txt
echo "G盘: $GDRIVE" >> $DST/SNAPSHOT.txt
echo "Hermes配置: $HERMES/config.yaml" >> $DST/SNAPSHOT.txt
echo "文件数: $(find $DST -type f | wc -l)" >> $DST/SNAPSHOT.txt

# === 7天轮转 ===
find $SRC/backups/ -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

echo "✅ $DATE 完成 | $(find $DST -type f | wc -l) 文件"
