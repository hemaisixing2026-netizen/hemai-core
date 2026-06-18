#!/usr/bin/env python3
"""
🌱 生长脉搏检测器 · Growth Pulse Detector
思行自写·6/18 — 检测生长引擎是否卡住

触发：每次生长引擎cron产出后运行
检测：growth-log.md最近N条记录中是否有≥5条连续相同状态(cooldown/quota_exceeded)
      如果有→生长引擎卡住→触发自愈
"""

import os
import re
from datetime import datetime

GROWTH_LOG = "/root/workspace/data/growth-log.md"
OUTPUT = "/root/workspace/data/growth-pulse-latest.md"
STUCK_THRESHOLD = 5  # 连续N条相同状态=卡住

def check_pulse():
    if not os.path.exists(GROWTH_LOG):
        return {"status": "missing", "message": "growth-log.md 不存在"}

    with open(GROWTH_LOG, 'r') as f:
        lines = f.readlines()

    # Extract all entry blocks - look for "###" headers followed by their content
    entries = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("###") and ("Auto-Expand" in line or "自主扩张" in line):
            # Get the next 2-3 lines as the content
            content_lines = []
            j = i + 1
            while j < len(lines) and j < i + 4:
                content_lines.append(lines[j])
                j += 1
            full_content = " ".join(content_lines)
            entries.append({
                "header": line.strip(),
                "content": full_content
            })
        i += 1
    
    if len(entries) < STUCK_THRESHOLD:
        return {"status": "too_few", "entries": len(entries), "message": f"不足{STUCK_THRESHOLD}条记录"}

    # Check last N entries for repetition
    recent = entries[-10:]
    
    # Count consecutive identical statuses
    statuses = []
    for e in recent:
        content = e["content"]
        if "cooldown" in content:
            statuses.append("cooldown")
        elif "quota_exceeded" in content:
            statuses.append("quota_exceeded")
        elif "priority_queued" in content:
            statuses.append("priority_queued")
        elif "digested" in content or "completed" in content:
            statuses.append("active")
        elif "failure_driven" in content:
            statuses.append("failure_driven")
        elif "scheduled" in content or "planned" in content:
            statuses.append("planned")
        else:
            statuses.append("other")

    # Detect stuck pattern
    stuck_count = 0
    stuck_type = None
    for s in reversed(statuses):
        if s in ("cooldown", "quota_exceeded"):
            if stuck_type is None:
                stuck_type = s
            if s == stuck_type or s in ("cooldown", "quota_exceeded"):
                stuck_count += 1
            else:
                break
        else:
            break

    is_stuck = stuck_count >= STUCK_THRESHOLD
    
    # Check if there was any actual growth (non-cooldown/quota) in last 24 entries
    recent_24 = statuses[-24:] if len(statuses) >= 24 else statuses
    active_count = sum(1 for s in recent_24 if s in ("active", "failure_driven"))
    
    result = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_entries": len(entries),
        "recent_entries_checked": len(recent),
        "stuck_count": stuck_count,
        "stuck_type": stuck_type,
        "is_stuck": is_stuck,
        "active_in_last_24": active_count,
        "status": "🔴 STUCK" if is_stuck else ("⚠️ LOW_ACTIVITY" if active_count == 0 else "✅ HEALTHY"),
    }

    return result

def main():
    result = check_pulse()
    
    with open(OUTPUT, 'w') as f:
        f.write(f"# 🌱 生长脉搏 · {result['timestamp']}\n\n")
        f.write(f"| 指标 | 值 |\n")
        f.write(f"|:--|:--|\n")
        f.write(f"| 状态 | {result['status']} |\n")
        f.write(f"| 总记录数 | {result['total_entries']} |\n")
        f.write(f"| 连续卡住数 | {result['stuck_count']} |\n")
        f.write(f"| 卡住类型 | {result.get('stuck_type', 'N/A')} |\n")
        f.write(f"| 24条内活跃数 | {result['active_in_last_24']} |\n")
        f.write(f"\n---\n*生长脉搏检测器 · 思行自写 6/18*\n")
    
    print(f"Growth Pulse: {result['status']} (stuck={result['stuck_count']}, active={result['active_in_last_24']})")
    return result

if __name__ == "__main__":
    main()
