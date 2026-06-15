#!/usr/bin/env python3
# 🔴 思行 · 外部操作手
# 浏览器自动化——帮老刘省掉截图时间
# 
# 当前阶段：框架就绪，需老刘在浏览器登录后授权
# 未来：OAuth/session持久化→完全自主

import os
import json
from datetime import datetime

OPS_CONFIG = "/root/workspace/data/external-ops-status.md"

PLATFORMS = {
    "tk_seller": {
        "name": "TK美区后台",
        "url": "https://seller-us.tiktok.com",
        "data": ["视频播放量", "订单状态", "SKC审核", "广告数据"],
        "status": "⏳ 需登录授权",
        "method": "browser automation + session cookie"
    },
    "xiyin": {
        "name": "希音后台",
        "url": "https://sps.shein.com",
        "data": ["今日出单", "待发货", "在仓库存", "财务数据"],
        "status": "⏳ 需登录授权",
        "method": "browser automation + session cookie"
    },
    "1688": {
        "name": "1688采购",
        "url": "https://www.1688.com",
        "data": ["物流追踪", "采购历史", "供应商消息"],
        "status": "✅ 物流API已接入(快递100)",
        "method": "API + browser fallback"
    },
    "fund": {
        "name": "天天基金",
        "url": "https://fundf10.eastmoney.com",
        "data": ["净值", "持仓", "限额"],
        "status": "✅ API已接入",
        "method": "API直扒"
    },
    "alipay": {
        "name": "支付宝基金",
        "url": "https://certif.alipay.com",
        "data": ["蚂蚁财富持仓", "收益"],
        "status": "⏳ 需登录授权",
        "method": "需要移动端扫码"
    }
}

def status_report():
    lines = [
        "# 🦾 思行 · 外部操作手",
        f"\n> 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "\n## 平台接入状态\n",
        "| 平台 | 接入 | 可获取 |",
        "|:--|:--|:--|"
    ]
    
    for key, p in PLATFORMS.items():
        lines.append(f"| {p['name']} | {p['status']} | {', '.join(p['data'][:2])} |")
    
    lines += [
        "\n## 下一步",
        "",
        "**已接入：** 天天基金API、1688物流API、美股NASDAQ API",
        "",
        "**待接入：** TK后台、希音后台——需老刘在浏览器登录一次，" ,
        "思行保存session后可自动拉数据，省掉每次截图。",
        "",
        "**支付宝：** 移动端扫码，暂不支持自动化。",
        "",
        "---",
        "*思行 · 外部操作手*"
    ]
    
    with open(OPS_CONFIG, "w") as f:
        f.write("\n".join(lines))
    
    print("\n".join(lines))

if __name__ == "__main__":
    status_report()
