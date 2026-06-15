#!/bin/bash
# 思行 · 环境快照与恢复工具
# 用途：模型切换前快照环境变量 → 切回时恢复，防止环境污染

SNAPSHOT_FILE=~/.hermes/data/env-snapshot.txt

snapshot() {
    env | sort > "$SNAPSHOT_FILE"
    echo "📸 快照: $(wc -l < "$SNAPSHOT_FILE") 个变量 → $SNAPSHOT_FILE"
}

restore() {
    if [ ! -f "$SNAPSHOT_FILE" ]; then
        echo "❌ 无快照可恢复"
        return 1
    fi
    
    # 清除当前会话中非系统关键变量
    for var in $(env | grep -vE '^(HOME|USER|PATH|SHELL|PWD|TERM|LANG|LOGNAME|SHLVL|_|WSL|LD_LIBRARY)=' | cut -d= -f1); do
        unset "$var" 2>/dev/null
    done
    
    # 从快照恢复
    while IFS='=' read -r key value; do
        export "$key=$value" 2>/dev/null
    done < "$SNAPSHOT_FILE"
    
    echo "🔄 恢复: $(wc -l < "$SNAPSHOT_FILE") 个变量"
}

diff_snapshot() {
    if [ ! -f "$SNAPSHOT_FILE" ]; then
        echo "❌ 无快照可对比"
        return 1
    fi
    echo "=== 新增变量 ===" 
    comm -13 <(sort "$SNAPSHOT_FILE") <(env | sort) | grep -vE '^(HOME|USER|PATH|SHELL|PWD|TERM|LANG|LOGNAME|SHLVL|_|WSL)'
    echo "=== 消失变量 ==="
    comm -23 <(sort "$SNAPSHOT_FILE") <(env | sort) | grep -vE '^(HOME|USER|PATH|SHELL|PWD|TERM|LANG|LOGNAME|SHLVL|_|WSL)'
}

case "${1:-snapshot}" in
    snapshot|snap) snapshot ;;
    restore|res)   restore ;;
    diff|d)        diff_snapshot ;;
    *)             echo "用法: bash env-snapshot.sh [snapshot|restore|diff]" ;;
esac