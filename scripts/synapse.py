#!/usr/bin/env python3
# 🔴 思行 · 中枢整合器 v2
# 每15分钟——读取所有组件输出，交叉连接，发现断链

import os
from datetime import datetime, timedelta

WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def read(path):
    return open(path).read() if os.path.exists(path) else ""

def check_all():
    alerts = []
    
    # 1. 触发器→决策库
    trigger = read(f"{WS}/data/trigger-alert-latest.md")
    dec = read(f"{WS}/data/decision-log.md")
    if "NVDA" in trigger and ("跌破" in trigger or "突破" in trigger):
        if "D001" in dec: alerts.append("NVDA触发→D001配比V2受影响")
        if "D003" in dec: alerts.append("NVDA触发→D003工业富联验证条件变化")
    
    # 2. 引擎1→基线
    e1 = read(f"{WS}/data/engine1-scan-latest.md")
    baseline = read(f"{WS}/data/portrait-baseline.md")
    if "棉绳" in e1 and "派件" in e1 and "已到" not in baseline:
        alerts.append("棉绳已到货→基线需更新")
    
    # 3. 知识网→节点完整性
    kg = read(f"{WS}/data/knowledge-graph.md")
    for node in ["TRIG", "GUARD", "PUSH", "CAL", "EVO", "SYNAPSE"]:
        if node not in kg:
            alerts.append(f"知识网缺失: {node}")
    
    # 4. 进化检测→基线(每周自动对比)
    evo = read(f"{WS}/data/evolution-report-latest.md")
    if evo and "SHIFT" in evo:
        if "SHIFT" not in baseline:
            alerts.append("进化检测发现漂移→基线待同步")
    
    # 5. 日历→微信(未来3天到期事项)
    cal = read(f"{WS}/data/calendar.md")
    today = datetime.now()
    for line in cal.split("\n"):
        if "|" in line and "到期" in line or "|" in line and "提醒" in line:
            parts = line.split("|")
            for p in parts:
                p = p.strip()
                if "/" in p and len(p) >= 5 and p[2] == "/":
                    try:
                        dt = datetime(today.year, int(p[:2]), int(p[3:]))
                        if dt < today:
                            dt = datetime(today.year+1, int(p[:2]), int(p[3:]))
                        if 0 <= (dt - today).days <= 3:
                            alerts.append(f"日历到期提醒: {p} — {line[:50]}")
                    except:
                        pass
    
    # 6. 决策库→知识网
    d_count = dec.count("### D0")
    d_refs = kg.count("D00")
    if d_count > d_refs:
        alerts.append(f"决策库{d_count}条→知识网仅引用{d_refs}条·待同步")
    
    # 输出
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    report = f"# 🧠 中枢整合 · {ts}\n\n"
    
    if alerts:
        report += "## ⚡ 未连接信号\n\n"
        for a in alerts:
            report += f"- {a}\n"
    else:
        report += "✅ 手是手·身体是身体·但神经全通了。\n"
    
    with open(f"{WS}/data/synapse-report-latest.md", "w") as f:
        f.write(report)
    
    if alerts:
        print("SYNAPSE: " + "; ".join(alerts))
    else:
        print("OK")

if __name__ == "__main__":
    check_all()
