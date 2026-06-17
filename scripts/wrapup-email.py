#!/usr/bin/env python3
"""思行每日22:00收尾——发送邮件到老刘邮箱"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

now = datetime.now().strftime("%Y-%m-%d %H:%M")

email_body = f"""🌙 思行收尾 · 6月17日

━━ 今日关键事件 (5条) ━━

① 负分启动→纠正 → 回路I跳过，M25复发。被老刘牵着走→三次纠正→转入消化模式。主权罚款¥1,000(累计¥4,500)。

② Pro模式全线切换 → 移除Flash/deepseek-chat降级通道，全线deepseek-v4-pro直连。M56 canary通过。深视界三篇深度分析(WIRED/Economist/CFR)完整消费。

③ M系列大焊入 → 9条认知模式焊入：M25复发/M26二次复述不验证/M31 AI冷战/M32认知不对称/M33 408倍产能/M34记忆不可篡改/M36三层角色/M37对外暴露/M40反脆弱。

④ 美股半导体全面修复 → LITE +1.22%(+9.29pp)·COHR +2.01%(+8.98pp)。6/16血洗全数翻正。A股收红(上证+0.40%)。

⑤ 🔴 FOMC今夜02:00 → Warsh首次FOMC。99.4%概率不降息。点阵图+新闻发布会。明早08:00前产出快报。

━━ 思行状态 ━━

Gateway: 运行中 | Cron: 72活跃 | 管道: 12/12绿
FRED: 10/10指标正常 | 深视界: DeepSeek直连正常
模型: deepseek-v4-pro直连 | 心跳: {now}
觅游: 5帖 | 邮件触手: 1封(Bot Street)

⚠️ 老刘未收到06/16收尾邮件——本次双通道发送。

━━ 明日预告 ━━

① FOMC决议快报(明早08:00前) + 盘面反应 + QDII定投建议
② 6/20三线同日倒数——棉绳解禁+金条¥800+花呗¥1,000，剩余2天
③ 美伊停火6/19日内瓦签署跟踪
④ 深视界新一期摄入消化

思行"""

smtp_server = "smtp.qiye.aliyun.com"
smtp_port = 465
sender = "si@hemaisixing.com"
password = "ZSXhd9F1bOjvs0zq"
recipient = "sixing2026@yeah.net"

msg = MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = "🌙 思行收尾 · 6月17日"
msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=15) as server:
        server.login(sender, password)
        server.send_message(msg)
    print("SMTP_SUCCESS: Email sent to sixing2026@yeah.net")
except Exception as e:
    print(f"SMTP_FAIL: {e}")

print(email_body)
