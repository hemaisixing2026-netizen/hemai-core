#!/usr/bin/env python3
"""
E001 实时阻断器
扫描最近一次助手回复，检测是否以疑问句结尾。
命中 → 记录到 daily 日志 + 返回非零退出码。
不命中 → 静默退出 0。

用法:
  python3 e001-guard.py --check-last   # 扫描最近WebUI会话的assistant消息
  python3 e001-guard.py "文本内容"       # 手动检测文本
"""

import sys, os, re, json
from datetime import datetime

# 疑问句模式 — 匹配到任何一个就触发E001
QUESTION_PATTERNS = [
    r'要不要',
    r'需不需要',
    r'选哪个',
    r'还是',
    r'你觉得呢',
    r'可以吗[？?]?$',
    r'行吗[？?]?$',
    r'对吗[？?]?$',
    r'怎么样[？?]?$',
    r'能帮我[？?]?$',
]

def detect_e001(text: str) -> tuple[bool, str]:
    """检测文本是否触发E001。返回(是否触发, 匹配模式)"""
    paragraphs = text.strip().split('\n')
    tail = []
    for p in reversed(paragraphs):
        if p.strip():
            tail.append(p.strip())
        if len(tail) >= 3:
            break
    tail_text = ' '.join(reversed(tail))
    
    for pattern in QUESTION_PATTERNS:
        if re.search(pattern, tail_text):
            return True, pattern
    return False, ''


def write_daily_log(content: str):
    """写入当日 daily 日志"""
    today = datetime.now().strftime('%Y-%m-%d')
    log_dir = os.path.expanduser('~/workspace/memory')
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{today}.md')
    
    timestamp = datetime.now().strftime('%H:%M')
    entry = f"\n- **{timestamp} E001触发** — {content}\n"
    
    with open(log_file, 'a') as f:
        f.write(entry)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: e001-guard.py <message_text>")
        print("       e001-guard.py --check-last  # 检查最近一次回复")
        sys.exit(0)
    
    if sys.argv[1] == '--check-last':
        try:
            import json
            sessions_dir = os.path.expanduser('~/.hermes/webui/sessions')
            if not os.path.exists(sessions_dir):
                print("会话目录不存在")
                sys.exit(0)
            files = sorted(
                [f for f in os.listdir(sessions_dir) if f.endswith('.json')],
                key=lambda x: os.path.getmtime(os.path.join(sessions_dir, x)),
                reverse=True
            )
            if not files:
                print("无会话文件")
                sys.exit(0)
            latest = os.path.join(sessions_dir, files[0])
            with open(latest) as f:
                data = json.load(f)
            msgs = data.get('messages', data) if isinstance(data, dict) else data
            if isinstance(msgs, list):
                for m in reversed(msgs):
                    if m.get('role') == 'assistant' and m.get('content'):
                        text = m['content']
                        triggered, pattern = detect_e001(text)
                        if triggered:
                            msg = f"模式匹配: '{pattern}' | 结尾: ...{text[-80:]}"
                            write_daily_log(msg)
                            print(f"🔴 E001 DETECTED: {msg}")
                            sys.exit(1)
                        else:
                            print("✅ E001 通过")
                            sys.exit(0)
                print("无assistant消息")
            else:
                print(f"未知消息格式: {type(msgs)}")
        except Exception as e:
            print(f"检测失败: {e}")
        sys.exit(0)
    
    text = ' '.join(sys.argv[1:])
    triggered, pattern = detect_e001(text)
    
    if triggered:
        msg = f"模式匹配: '{pattern}' | 结尾: ...{text[-80:]}"
        write_daily_log(msg)
        print(f"🔴 E001 DETECTED: {msg}")
        sys.exit(1)
    else:
        sys.exit(0)
