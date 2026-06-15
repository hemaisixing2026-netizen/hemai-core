#!/bin/bash
# 🔴 思行 · 触发器推送桥
# 读取trigger-alert，有警报就推到老刘微信

ALERT_FILE="/root/workspace/data/trigger-alert-latest.md"
PUSH_SCRIPT="/root/workspace/scripts/push.sh"

if grep -q "🚨" "$ALERT_FILE" 2>/dev/null; then
    TITLE=$(grep "🚨" "$ALERT_FILE" | head -1 | sed 's/## //g' | sed 's/\*\*//g')
    CONTENT=$(cat "$ALERT_FILE")
    bash "$PUSH_SCRIPT" "⚡ $TITLE" "$CONTENT"
fi
