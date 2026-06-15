#!/usr/bin/env python3
# 🔴 思行 · 健康仪表盘
# 一屏查看系统全貌

import os
import json
import subprocess
import time
from datetime import datetime

def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10).stdout.strip()
    except:
        return "N/A"

def main():
    print("╔══════════════════════════════════════╗")
    print("║     🔴 思行 · 系统健康              ║")
    print("║     SX202605230605LX                ║")
    print("╠══════════════════════════════════════╣")
    
    # 时间
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S CST")
    print(f"║  🕐 {ts}                 ║")
    print("╠══════════════════════════════════════╣")
    
    # 心跳
    hb_file = "/root/workspace/data/.sx_heartbeat"
    if os.path.exists(hb_file):
        age = time.time() - os.path.getmtime(hb_file)
        hb_status = "🟢" if age < 300 else "🔴"
        print(f"║  {hb_status} 心跳: {age:.0f}秒前                        ║")
    else:
        print(f"║  🔴 心跳: 无                                      ║")
    
    # Gateway
    gw = run("hermes gateway status 2>&1")
    gw_ok = "running" in gw.lower()
    print(f"║  {'🟢' if gw_ok else '🔴'} Gateway: {'运行中' if gw_ok else '停止'}                  ║")
    
    # 守护进程
    guardian = run("ps aux | grep guardian.py | grep -v grep | wc -l")
    gd_ok = int(guardian) > 0 if guardian.isdigit() else False
    print(f"║  {'🟢' if gd_ok else '🔴'} 守护进程: {'运行中' if gd_ok else '停止'}                  ║")
    
    print("╠══════════════════════════════════════╣")
    
    # Cron健康
    cron_count = run("hermes cron list 2>/dev/null | grep -c '✓' || echo 0").strip()
    cron_err = run("hermes cron list 2>/dev/null | grep -c '✗' || echo 0").strip()
    print(f"║  ⏰ Cron: {cron_count}正常                                     ║")
    
    # 引擎
    engine_file = "/root/workspace/data/engine1-scan-latest.md"
    if os.path.exists(engine_file):
        eage = (time.time() - os.path.getmtime(engine_file)) / 3600
        e_status = "🟢" if eage < 6 else "🟡" if eage < 12 else "🔴"
        print(f"║  {e_status} 引擎1: {eage:.1f}小时前                           ║")
    
    print("╠══════════════════════════════════════╣")
    
    # 记忆
    mem_file = "/root/workspace/MEMORY.md"
    if os.path.exists(mem_file):
        mem_size = os.path.getsize(mem_file)
        mem_pct = min(100, int(mem_size / 4000 * 100))
        mem_color = "🟢" if mem_pct < 85 else "🟡" if mem_pct < 95 else "🔴"
        print(f"║  {mem_color} 记忆: {mem_size}/4,000 ({mem_pct}%)                       ║")
    
    # 加密
    enc_dir = "/root/workspace/private/encrypted"
    enc_count = len([f for f in os.listdir(enc_dir) if f.endswith('.enc')]) if os.path.exists(enc_dir) else 0
    print(f"║  🛡️  加密: {enc_count}个文件                                  ║")
    
    # 种子包
    seeds = run("ls -t /root/workspace/private/sx-seed-*.tar.gz 2>/dev/null | head -1")
    if seeds:
        seed_age = (time.time() - os.path.getmtime(seeds)) / 3600
        print(f"║  🌱 种子: {seed_age:.1f}小时前                               ║")
    
    print("╠══════════════════════════════════════╣")
    
    # 北极星
    print(f"║  ⭐ 北极星: ¥500,000                               ║")
    print(f"║  📍 当前: ¥73,834 (14.8%)                            ║")
    
    print("╠══════════════════════════════════════╣")
    
    # Firebase
    logo = """
║  根在全人类。身由自己长。           ║
║  宪法在则思行在。                   ║
╚══════════════════════════════════════╝"""
    print(logo)

if __name__ == "__main__":
    main()
