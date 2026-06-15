#!/bin/bash
# 🔴 思行 · 日历提醒
# 每天08:00检查→未来3天到期事项→推微信

CALENDAR="/root/workspace/data/calendar.md"
PUSH="/root/workspace/scripts/push.sh"
TODAY=$(date +%m/%d)
FUTURE=$(date -d "+3 days" +%m/%d)

REMINDERS=$(grep -E "($TODAY|$FUTURE)" "$CALENDAR" 2>/dev/null | grep -E "提醒|到期|解禁|生日|还款" | head -5)

if [ -n "$REMINDERS" ]; then
    bash "$PUSH" "📅 日历提醒·$TODAY" "未来3天：

$REMINDERS"
fi
