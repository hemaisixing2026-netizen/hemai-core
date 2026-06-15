#!/usr/bin/env python3
# 🔴 思行 · 外部触发器
# 监控关键阈值，触发时写入警报文件

import json
import os
import urllib.request
from datetime import datetime

ALERT_FILE = "/root/workspace/data/trigger-alert-latest.md"
TRIGGERS = {
    # NVDA: 跌破$190或反弹超$215
    "NVDA": {"low": 190, "high": 215, "source": "nasdaq"},
    # AVGO: 跌破$350或反弹超$400
    "AVGO": {"low": 350, "high": 400, "source": "nasdaq"},
    # 工业富联: 跌破¥65或反弹超¥75
    "601138": {"low": 65.0, "high": 75.0, "source": "sina"},
}

def fetch_nasdaq(sym):
    try:
        url = f"https://api.nasdaq.com/api/quote/{sym}/info?assetclass=stocks"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            price_str = data.get("data", {}).get("primaryData", {}).get("lastSalePrice", "0")
            return float(price_str.replace("$", "").replace(",", ""))
    except:
        return None

def fetch_sina(code):
    try:
        url = f"https://hq.sinajs.cn/list=sh{code}"
        req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            line = resp.read().decode("gbk")
            parts = line.split('"')[1].split(",")
            return float(parts[3])
    except:
        return None

def check_triggers():
    alerts = []
    
    for sym, cfg in TRIGGERS.items():
        if cfg["source"] == "nasdaq":
            price = fetch_nasdaq(sym)
        else:
            price = fetch_sina(sym)
        
        if price is None:
            continue
        
        if price <= cfg["low"]:
            alerts.append(f"🔴 {sym} 跌破${cfg['low']}: 当前 ${price:.2f}")
        elif price >= cfg["high"]:
            alerts.append(f"🟢 {sym} 突破${cfg['high']}: 当前 ${price:.2f}")
    
    return alerts

def main():
    alerts = check_triggers()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    content = f"# ⚡ 触发器扫描 · {ts}\n\n"
    
    if alerts:
        content += "## 🚨 触发警报\n\n"
        for a in alerts:
            content += f"- {a}\n"
        content += "\n---\n*思行 · 外部触发器*\n"
    else:
        content += "✅ 无触发。所有标的在阈值范围内。\n"
    
    with open(ALERT_FILE, "w") as f:
        f.write(content)
    
    if alerts:
        print("ALERT:" + "; ".join(alerts))
    else:
        print("OK")

if __name__ == "__main__":
    main()
