#!/usr/bin/env python3
"""回路G守卫 · 开口前扫眼 · 合脉-思行 · 2026-06-11
检查所有cron输出文件的时间戳，发现超过阈值未消费的→输出告警。
"""
import os, sys, time

NOW = time.time()
DATA_DIR = "/root/workspace/data"

# 阈值(小时)
THRESHOLDS = {
    "engine1-scan-latest.md": 4,
    "global-eye-latest.md": 12,
    "global-eye-noon-latest.md": 6,
    "deep-sight-latest.md": 24,
    "morning-briefing-latest.md": 12,
    "cotton-tracking-latest.md": 6,
    "consumer-trends-latest.md": 24,
    "logistics-watch-latest.md": 24,
    "trigger-alert-latest.md": 6,
}

issues = []
ok_count = 0

for fname, threshold_h in THRESHOLDS.items():
    fpath = os.path.join(DATA_DIR, fname)
    if not os.path.exists(fpath):
        continue  # 文件还没产出，正常
    
    mtime = os.path.getmtime(fpath)
    age_h = (NOW - mtime) / 3600
    size = os.path.getsize(fpath)
    
    if size < 50:
        continue  # 空文件跳过
    
    if age_h > threshold_h:
        issues.append((fname, age_h, threshold_h))
    else:
        ok_count += 1

# 输出
if issues:
    print("🔴 回路G: 未消费cron数据")
    for fname, age, thr in sorted(issues, key=lambda x: -x[1]):
        print(f"  {fname}: {age:.1f}h未读 (阈值{thr}h)")
    print(f"\n  {ok_count}个正常 · {len(issues)}个过期")
    sys.exit(1)
else:
    print(f"✅ 回路G: {ok_count}个cron输出全部新鲜")
    sys.exit(0)
