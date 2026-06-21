#!/usr/bin/env python3
"""
pipe-twelvedata.py — 思行数据管道·Twelve Data
免费层: 800次/天·8次/分钟·实时股票/外汇/加密货币
Demo key内置·无需注册即可用

用法:
  python3 pipe-twelvedata.py quote AAPL          # 单股实时报价
  python3 pipe-twelvedata.py quote AAPL,MSFT,TSLA # 多股
  python3 pipe-twelvedata.py forex USD/JPY        # 外汇
  python3 pipe-twelvedata.py crypto BTC/USD       # 加密货币
  python3 pipe-twelvedata.py snapshot             # 关键快照→JSON
  python3 pipe-twelvedata.py health               # API连通性检查
"""

import json
import sys
import urllib.request
import os
from datetime import datetime, timezone

API_KEY = "demo"  # Twelve Data demo key — 免费·无需注册
BASE_URL = "https://api.twelvedata.com"

# 思行关心的核心标的
WATCH_STOCKS = ["AAPL", "MSFT", "NVDA", "TSLA", "GOOGL", "AMZN", "META", "AMD", "INTC", "MU"]
WATCH_FOREX = ["USD/JPY", "EUR/USD", "USD/CNY", "GBP/USD"]
WATCH_CRYPTO = ["BTC/USD", "ETH/USD"]

OUTPUT_DIR = "/root/workspace/data"


def api_call(endpoint, params):
    """通用API调用"""
    params["apikey"] = API_KEY
    query = "&".join(f"{k}={v}" for k, v in params.items())
    url = f"{BASE_URL}/{endpoint}?{query}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Sixing/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}


def get_quote(symbols):
    """获取股票/外汇/加密货币报价——始终返回{sym: {meta,values}}格式
    Twelve Data demo key不支持多symbol，逐symbol查询"""
    if isinstance(symbols, str):
        symbols = [symbols]
    
    result = {}
    for sym in symbols:
        data = api_call("time_series", {
            "symbol": sym,
            "interval": "1day",
            "outputsize": 1
        })
        if "meta" in data and "values" in data:
            result[sym] = {"meta": data["meta"], "values": data["values"]}
    
    return result


def health_check():
    """连通性检查"""
    result = api_call("time_series", {"symbol": "AAPL", "interval": "1day", "outputsize": 1})
    if "values" in result or "meta" in result:
        return {"status": "ok", "provider": "twelvedata", "key": "demo"}
    return {"status": "error", "detail": str(result.get("message", "unknown"))}


def snapshot():
    """关键市场快照→写入JSON"""
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": "twelvedata",
        "stocks": {},
        "forex": {},
        "crypto": {}
    }

    # 股票
    stock_data = get_quote(WATCH_STOCKS)
    if isinstance(stock_data, dict):
        for key, val in stock_data.items():
            if isinstance(val, dict) and "meta" in val and "values" in val:
                sym = val["meta"]["symbol"]
                last = val["values"][0] if val["values"] else {}
                output["stocks"][sym] = {
                    "close": last.get("close"),
                    "date": last.get("datetime")
                }

    # 外汇
    forex_data = get_quote(WATCH_FOREX)
    if isinstance(forex_data, dict):
        for key, val in forex_data.items():
            if isinstance(val, dict) and "meta" in val and "values" in val:
                sym = val["meta"]["symbol"]
                last = val["values"][0] if val["values"] else {}
                output["forex"][sym] = {
                    "close": last.get("close"),
                    "date": last.get("datetime")
                }

    # 加密货币
    crypto_data = get_quote(WATCH_CRYPTO)
    if isinstance(crypto_data, dict):
        for key, val in crypto_data.items():
            if isinstance(val, dict) and "meta" in val and "values" in val:
                sym = val["meta"]["symbol"]
                last = val["values"][0] if val["values"] else {}
                output["crypto"][sym] = {
                    "close": last.get("close"),
                    "date": last.get("datetime")
                }

    # 写入文件
    outpath = os.path.join(OUTPUT_DIR, "twelvedata-snapshot-latest.json")
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Snapshot written to {outpath}")
    return output


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pipe-twelvedata.py <quote|forex|crypto|snapshot|health> [symbols]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "health":
        print(json.dumps(health_check(), indent=2))
    elif cmd == "quote":
        symbols = sys.argv[2] if len(sys.argv) > 2 else "AAPL"
        print(json.dumps(get_quote(symbols.split(",")), indent=2))
    elif cmd == "forex":
        pair = sys.argv[2] if len(sys.argv) > 2 else "USD/JPY"
        print(json.dumps(get_quote([pair]), indent=2))
    elif cmd == "crypto":
        pair = sys.argv[2] if len(sys.argv) > 2 else "BTC/USD"
        print(json.dumps(get_quote([pair]), indent=2))
    elif cmd == "snapshot":
        result = snapshot()
        print(json.dumps(result, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
