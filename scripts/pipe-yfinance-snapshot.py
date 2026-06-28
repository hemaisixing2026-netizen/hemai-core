#!/usr/bin/env python3
"""🌱 思行·yfinance快照管道
每4h拉取关键标的价格快照——免费·无需API key·无需注册。
补充Twelve Data/FRED未覆盖的ETF/航运/债券维度。
输出 /root/workspace/data/yfinance-snapshot-latest.json
"""

import json, os, time, sys
from datetime import datetime, timezone, timedelta

WORKSPACE = os.path.expanduser("~/workspace/data")
OUTPUT = f"{WORKSPACE}/yfinance-snapshot-latest.json"

# ── 监控标的 ──
TICKERS = {
    # 核心股票
    "NVDA": {"name": "NVIDIA", "category": "半导体"},
    # ETF
    "QQQ": {"name": "纳指100 ETF", "category": "美股大盘"},
    "SMH": {"name": "半导体ETF", "category": "半导体"},
    "FXI": {"name": "中国大盘ETF", "category": "中国"},
    "ASHR": {"name": "沪深300 ETF", "category": "中国"},
    "KWEB": {"name": "中国互联网ETF", "category": "中国"},
    "EEM": {"name": "新兴市场ETF", "category": "新兴市场"},
    # 债券/利率
    "TLT": {"name": "20年+国债ETF", "category": "利率"},
    "SHY": {"name": "1-3年国债ETF", "category": "利率"},
    # 商品
    "CL=F": {"name": "WTI原油期货", "category": "能源"},
    "GDX": {"name": "黄金矿业ETF", "category": "贵金属"},
    # 航运/物流
    "BDRY": {"name": "干散货航运ETF", "category": "物流"},
    # 外汇
    "DX-Y.NYB": {"name": "美元指数", "category": "外汇"},
}

def pull():
    try:
        import yfinance as yf
    except ImportError:
        return {"error": "yfinance not installed", "timestamp": now_iso()}
    
    results = {}
    for symbol, meta in TICKERS.items():
        try:
            t = yf.Ticker(symbol)
            info = t.info
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            prev_close = info.get("previousClose") or info.get("regularMarketPreviousClose")
            change_pct = None
            if price and prev_close and prev_close != 0:
                change_pct = round((price - prev_close) / prev_close * 100, 2)
            
            results[symbol] = {
                "name": meta["name"],
                "category": meta["category"],
                "price": price,
                "prevClose": prev_close,
                "changePct": change_pct,
                "marketCap": info.get("marketCap"),
                "volume": info.get("volume"),
            }
        except Exception as e:
            results[symbol] = {
                "name": meta["name"],
                "category": meta["category"],
                "error": str(e)[:200],
            }
    
    return {"timestamp": now_iso(), "tickers": results}

def now_iso():
    return datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%dT%H:%M:%S+08:00")

def main():
    data = pull()
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    # Summary
    ok = sum(1 for v in data.get("tickers", {}).values() if "error" not in v)
    total = len(data.get("tickers", {}))
    print(f"yfinance快照: {ok}/{total} OK | {OUTPUT}")

if __name__ == "__main__":
    main()
