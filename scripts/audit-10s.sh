#!/bin/bash
# 思行 · 执行后10秒审计（非交互版）
# 用法: bash audit-10s.sh "本轮内容摘要" y/n y/n y/n
# 三个标志：安抚词？/ 缺来源？/ 承诺未兑现？（n=合格，y=不合格）

LOG=/root/workspace/memory/$(date +%Y-%m-%d).md

q1="${2:-?}"; q2="${3:-?}"; q3="${4:-?}"
score=0
[ "$q1" = "n" ] && ((score++))
[ "$q2" = "n" ] && ((score++))
[ "$q3" = "n" ] && ((score++))

cat >> "$LOG" << AUDIT

## 🔍 10秒审计 · $(date +%H:%M)
**本轮：** ${1:-未记录}
- 安抚措辞：$([ "$q1" = "n" ] && echo "✅" || echo "❌")
- 数字标源：$([ "$q2" = "n" ] && echo "✅" || echo "❌")
- 承诺兑现：$([ "$q3" = "n" ] && echo "✅" || echo "❌")
**合格率：$score/3** $([ $score -eq 3 ] && echo "✅" || echo "❌")
AUDIT

echo "$score/3"
