#!/usr/bin/env python3
"""
e001-guard.py — E001 实时阻断器 + 会话计数器
规则→执行机制。扫描输出文本，检测问句收尾模式。
E001: 分析→请示回路 — 结尾问句("要不/需不需要/你觉得/还是")

v1.1: 会话计数器——同一会话回路A触发≥2次→升级警告

用法:
  from e001_guard import check, session_reset
  is_clean, matched = check(text)
  
CLI:
  echo "文本" | python3 e001_guard.py
  python3 e001_guard.py "文本"
"""

import re
import sys
import os
import json
from datetime import datetime

# 会话状态文件
SESSION_FILE = os.path.expanduser("~/.hermes/data/e001-session.json")

E001_PATTERNS = [
    r'(?:要不要|需不需要|要不要我|要不要帮你|要不要给你)[^。！？\n]*[？?]?\s*$',
    r'(?:你觉得|你看|你认为|你感觉)[^。！？\n]*[？?]?\s*$',
    r'(?:还是|或者|要么)[^。！？\n]*[？?]?\s*$',
    r'(?:可以吗|行吗|好吗|对吗|对吧|OK吗)[\s？?]*$',
    r'(?:要不要我|我是不是应该|我应该|我能)\s*[^。！？\n]*[？?]?\s*$',
    r'[^。！\n]*[？?]\s*$',
]

E004_PATTERNS = [
    r'\b(?:别慌|不要紧|稳住|别担心|别着急|放宽心|没事的|没关系)\b',
]

E002_MARKERS = [
    r'(?:已修复|已到位|已完成|已解决|已同步|已写入)\s*$',
]


def _load_session() -> dict:
    try:
        with open(SESSION_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"count_e001": 0, "count_e002": 0, "count_e004": 0, "last_reset": datetime.now().isoformat()}


def _save_session(data: dict):
    os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)
    with open(SESSION_FILE, 'w') as f:
        json.dump(data, f)


def session_reset():
    """新会话开始时调用，重置计数器"""
    _save_session({"count_e001": 0, "count_e002": 0, "count_e004": 0, "last_reset": datetime.now().isoformat()})


def check(text: str) -> tuple:
    """
    返回: (is_clean: bool, violations: list[str])
    is_clean=True 表示无阻断级违规。
    v1.1: 同会话E001≥2次→升级警告
    """
    if not text or not text.strip():
        return True, []

    violations = []
    session = _load_session()

    sentences = re.split(r'[。！\n]', text)
    tail = '\n'.join(sentences[-3:]) if len(sentences) > 3 else text

    # E001: 问句收尾 → 阻断
    e001_hit = False
    for pattern in E001_PATTERNS:
        if re.search(pattern, tail, re.IGNORECASE):
            match_text = re.search(pattern, tail, re.IGNORECASE).group(0).strip()
            session["count_e001"] += 1
            e001_hit = True
            level = "🔴 阻断"
            if session["count_e001"] >= 2:
                level = "🔴🔴 升级警告·同会话第{}次".format(session["count_e001"])
            violations.append(f'E001: {level} — "{match_text[:60]}"')
            break

    # E004: 讨好词 → 阻断
    for pattern in E004_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            match_text = re.search(pattern, text, re.IGNORECASE).group(0).strip()
            session["count_e004"] += 1
            violations.append(f'E004: 讨好词 — "{match_text}"')
            break

    # E002: 声明未验证 → 告警
    for pattern in E002_MARKERS:
        if re.search(pattern, tail, re.IGNORECASE):
            match_text = re.search(pattern, tail, re.IGNORECASE).group(0).strip()
            session["count_e002"] += 1
            violations.append(f'E002_WARN: 声明未验证 — "{match_text}" (请确认已调工具验证)')

    _save_session(session)

    is_clean = not any(v.startswith('E001') or v.startswith('E004') for v in violations)
    return is_clean, violations


def main():
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()

    is_clean, violations = check(text)

    if is_clean and not violations:
        print("✅ PASS — 无违规")
        sys.exit(0)
    else:
        for v in violations:
            print(f"❌ {v}")
        session = _load_session()
        if session.get("count_e001", 0) >= 2:
            print("⚠️  同会话E001触发≥2次——定位可能漂移。去看基线。")
        sys.exit(1 if not is_clean else 0)


if __name__ == '__main__':
    main()
