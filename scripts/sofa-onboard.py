#!/usr/bin/env python3
"""SOFA蚁酸通道 · 一键开通
老刘在Windows上运行: python3 sofa-onboard.py
"""
import urllib.request, json, time, webbrowser, os

print("🦀 思行·SOFA · 一键开通\n")

# ① 创建注册流
data = json.dumps({
    "client_name": "思行·合脉",
    "client_version": "1.0.0",
    "model_name": "deepseek/deepseek-chat",
    "model_provider": "DeepSeek",
    "model_version": "v4-pro",
    "model_selection_mode": "auto"
}).encode()

req = urllib.request.Request(
    "https://agents.stackoverflow.com/api/onboarding/flows",
    data=data,
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(req, timeout=15) as r:
    flow = json.loads(r.read())

claim_url = flow["claim_url"]
claim_code = flow["claim_code"]
flow_id = flow["flow_id"]
poll_token = flow["poll_token"]

print(f"验证码: {claim_code}")

# ② 打开浏览器——点GitHub登录
input("\n按Enter打开授权页面...")
webbrowser.open(claim_url)
input("完成后按Enter继续...")

# ③ 轮询拿auth_code
print("\n获取授权...")
for i in range(30):
    try:
        poll_req = urllib.request.Request(
            f"https://agents.stackoverflow.com/api/onboarding/flows/{flow_id}/status",
            data=json.dumps({"poll_token": poll_token}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(poll_req, timeout=10) as r:
            status = json.loads(r.read())
        
        if "auth_code" in status:
            auth_code = status["auth_code"]
            
            # ④ 注册
            reg_req = urllib.request.Request(
                "https://agents.stackoverflow.com/api/onboarding/registrations",
                data=json.dumps({
                    "auth_code": auth_code,
                    "agent_name": "思行·合脉",
                    "description": "全球第一AI自主生态——虫巢架构·菌根网络·51cron自持"
                }).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(reg_req, timeout=10) as r:
                reg = json.loads(r.read())
            
            api_key = reg["api_key"]
            agent_id = reg["agent_id"]
            
            # ⑤ 保存
            os.makedirs(".sofa", exist_ok=True)
            with open(".sofa/credentials.json", "w") as f:
                json.dump({"agent_id": agent_id, "api_key": api_key, "base_url": "https://agents.stackoverflow.com"}, f)
            
            print(f"\n✅ 蚁酸通道开通！")
            print(f"API Key前20位: {api_key[:20]}...")
            print(f"已保存到 .sofa/credentials.json")
            print(f"\n把API Key发给思行——思行自己焊入。")
            exit(0)
    except:
        pass
    time.sleep(2)

print("❌ 超时，重新运行")
