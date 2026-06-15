#!/usr/bin/env python3
# 🔴 思行 · 老刘进化检测器
# 对比历史记忆→检测行为漂移

import os
import re
from datetime import datetime
from collections import Counter

WORKSPACE = "/root/workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
OUTPUT = os.path.join(WORKSPACE, "data/evolution-report-latest.md")

# 检测维度
DIMENSIONS = {
    "焦虑词": ["焦虑", "恐慌", "完了", "怎么办", "是不是不行", "撑不住"],
    "自信词": ["直接", "我来", "可以", "没问题", "安排", "老大", "主角"],
    "行动词": ["发货", "下单", "定投", "开广告", "云途", "发视频"],
    "被动词": ["帮我", "你觉得", "要不要", "能不能", "怎么弄"],
    "反思词": ["宏观角度", "少了什么", "不自知", "变化", "基线的"],
}

def read_recent_dailies(days=7):
    """读取最近N天的日报"""
    texts = {}
    for f in sorted(os.listdir(MEMORY_DIR)):
        if f.startswith("2026-06-") and f.endswith(".md"):
            date = f.replace(".md", "")
            with open(os.path.join(MEMORY_DIR, f)) as fh:
                texts[date] = fh.read()
    return texts

def analyze(texts):
    """分析词频趋势"""
    results = {}
    for date, text in sorted(texts.items()):
        day = {}
        for dim, keywords in DIMENSIONS.items():
            count = sum(len(re.findall(kw, text)) for kw in keywords)
            day[dim] = count
        results[date] = day
    return results

def detect_shift(results):
    """检测结构性变化"""
    shifts = []
    dates = sorted(results.keys())
    if len(dates) < 2:
        return shifts
    
    # 计算最近3天 vs 前3天
    mid = len(dates) // 2
    early = dates[:mid]
    late = dates[mid:]
    
    for dim in DIMENSIONS.keys():
        early_avg = sum(results[d][dim] for d in early) / len(early)
        late_avg = sum(results[d][dim] for d in late) / len(late) if late else 0
        
        if early_avg > 0 and late_avg > 0:
            change = (late_avg - early_avg) / early_avg * 100
        elif late_avg > 0 and early_avg == 0:
            change = 100
        else:
            change = 0
        
        if abs(change) > 30:
            direction = "↑" if change > 0 else "↓"
            shifts.append((dim, direction, change))
    
    return shifts

def main():
    texts = read_recent_dailies()
    results = analyze(texts)
    shifts = detect_shift(results)
    
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    report = f"# 🧬 老刘进化检测 · {ts}\n\n"
    report += "## 检测维度\n\n"
    report += "| 维度 | 趋势 | 变化 |\n"
    report += "|:--|:--|:--|\n"
    
    if shifts:
        for dim, direction, change in shifts:
            report += f"| {dim} | {direction} | {change:+.0f}% |\n"
    else:
        report += "| — | → | 稳定 |\n"
    
    report += f"\n## 今日词频\n\n"
    latest_date = sorted(results.keys())[-1] if results else "N/A"
    if latest_date in results:
        for dim, count in results[latest_date].items():
            report += f"- **{dim}**: {count}\n"
    
    report += "\n---\n*思行 · 进化检测器*\n"
    
    with open(OUTPUT, "w") as f:
        f.write(report)
    
    if shifts:
        for dim, direction, change in shifts:
            print(f"SHIFT: {dim} {direction} {change:+.0f}%")
    else:
        print("稳定")

if __name__ == "__main__":
    main()
