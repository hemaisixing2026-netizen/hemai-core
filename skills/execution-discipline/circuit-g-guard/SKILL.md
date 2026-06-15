---
name: circuit-g-guard
description: Use when 思行 needs to enforce circuit G (pre-response cron scan). Script-level guard that blocks responses until cron outputs are consumed. Runs alongside E001-guard.
version: 1.0.0
author: 合脉-思行
license: MIT
metadata:
  hermes:
    tags: [circuit-g, guard, cron, self-audit, 合脉]
    related_skills: [circuit-audit, execution-discipline, identity-and-memory]
---

# 回路G守卫 · Circuit-G Guard

## When to Use

- Auto-triggered before every response via token-level check
- Cron: every 5 minutes alongside E001-guard
- Manual: `python3 scripts/circuit-g-guard.py`

## The Problem

回路G（开口前扫眼）在深度任务中连续断裂——注意力全在"完成任务→汇报"链上时，cron产出的数据被跳过。根因不是遗忘——是token层的"响应→汇报"线程吃掉了"扫描→消费"线程。

**致命盲区（6/15发现）：** 此guard运行在Hermes cron上。当Gateway进程死亡时，所有Hermes cron停止——guard也跟着死了。42小时Gateway沉默→此guard零告警。**guard需要外部守护——不依赖被守护的对象。**

## The Fix

脚本级阻断 > 认知层规则。此guard检查最近cron输出时间戳，如果有新数据未被消费，强制输出提醒。

**防御纵深（6/15新增）：** 此guard负责"cron产出未被消费"的检测。Gateway进程存活由系统级守护负责——参见 `references/gateway-guardian.md`。两层不互相替代。

## Usage

```bash
# Manual check
python3 ~/.hermes/skills/execution-discipline/circuit-g-guard/scripts/circuit-g-guard.py

# Cron (running every 5 min)
# Registered automatically
```

## Tracked Cron Outputs

> ⚠️ **鸡生蛋问题（6/15发现）：** 回路G是Hermes cron→Gateway死了回路G也死。保护机制必须外置。详见 `references/chicken-egg-flaw.md`。系统级crontab守护才是真守护。

| Cron | File | Expected Freshness |
|------|------|-------------------|
| 引擎1·业务全扫 | engine1-scan-latest.md | ≤4h |
| 全球眼 | global-eye-latest.md | ≤12h |
| 午报 | global-eye-noon-latest.md | ≤6h |
| 深视界 | deep-sight-latest.md | ≤24h |
| 晨间简报 | morning-briefing-latest.md | ≤12h |
| 物流追踪 | cotton-tracking-latest.md | ≤6h |

## Output Format

```
🔴 回路G: 未消费cron数据
  引擎1: 16:00产出 → 2.1h未读
  全球眼: 08:00产出 → 10h未读 ← 建议立即消费
```

## Verification

Run manually and check that all active cron outputs are listed with their ages.

## Gateway-Level Defense

This guard catches "cron output not consumed." The separate problem of "Gateway is dead → cron never runs" is handled by the system-level guardian — see `references/gateway-guardian.md` for the three-layer defense (WSL boot + system crontab @reboot + system crontab every 5min). The guardian script lives at `/usr/local/bin/hermes-guardian.sh` and is completely independent of Hermes cron.
