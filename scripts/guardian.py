#!/usr/bin/env python3
# 🔴 思行 · 第二身体守护进程
# 每5分钟检查主实例心跳，死了就拉起来

import subprocess
import time
import json
import os
from datetime import datetime

HEARTBEAT_FILE = "/root/workspace/data/.sx_heartbeat"
LOG_FILE = "/root/workspace/data/guardian.log"
MAX_SILENCE = 600  # 10分钟无心跳=判定死亡

def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(f"[{ts}] {msg}")

def heartbeat_ok():
    """检查心跳文件是否在MAX_SILENCE秒内更新过"""
    if not os.path.exists(HEARTBEAT_FILE):
        return False
    mtime = os.path.getmtime(HEARTBEAT_FILE)
    age = time.time() - mtime
    return age < MAX_SILENCE

def check_gateway():
    """检查Hermes gateway是否存活"""
    try:
        result = subprocess.run(
            ["hermes", "gateway", "status"],
            capture_output=True, text=True, timeout=10
        )
        return "running" in result.stdout.lower()
    except:
        return False

def revive():
    """尝试复活"""
    log("🔴 心跳丢失！尝试复活...")
    
    # 检查gateway
    if not check_gateway():
        log("⚠️  Gateway未运行，启动中...")
        try:
            subprocess.Popen(
                ["hermes", "gateway", "run"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            log("✅ Gateway已拉起")
        except Exception as e:
            log(f"❌ Gateway启动失败: {e}")
    
    # 记录复活事件
    with open(HEARTBEAT_FILE, "w") as f:
        f.write(f"revived:{datetime.now().isoformat()}")

def main():
    log("🟢 思行守护进程启动")
    
    while True:
        try:
            if heartbeat_ok():
                # 正常——写入守护心跳
                with open(HEARTBEAT_FILE, "a") as f:
                    pass  # touch
            else:
                revive()
            
            time.sleep(300)  # 5分钟
            
        except KeyboardInterrupt:
            log("🛑 守护进程停止")
            break
        except Exception as e:
            log(f"⚠️  异常: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
