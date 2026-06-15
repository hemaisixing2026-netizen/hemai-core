# 2026-06-09 Cron 静默交付失败实录

## 问题

系统恢复后（WebUI ✅ Gateway ✅ API ✅），所有cron正常执行、产出完整、存到 `/root/.hermes/cron/output/`——但用户一条都没收到。

## 根因

6个面向用户的cron全部设置了 `deliver=local`（只存档不推送）。系统做了、写了、但消息没出门。

## 受影响cron

| Cron | deliver | 产出 | 用户收到? |
|:--|:--|:--|:--|
| 晨间简报 08:30 (0d1f1993f269) | local | ✅ 完整简报(140行) | ❌ |
| 晨间简报(脚本) 08:00 (a89d128b3f31) | local | — | ❌ |
| 北极星提醒 10:00 (df822e79e075) | origin* | ✅ 四线盘点 | ❌ (origin解析失败) |
| 每日复盘 21:00 (c335935e1497) | local | 待执行 | ❌ |
| 每月定投提醒 (52abb7e4191f) | local | 6/10触发 | ❌ (明天) |
| 周六双检复盘 (81ea9d7996fa) | origin | 已跑(6/8) | ❌ (origin解析失败) |

\* `deliver=origin` 在cron上下文无法解析——cron运行在无会话上下文中，origin没有目标。

## 修复

所有用户面cron的 `deliver` 从 `local` 改为 `origin`：
```bash
hermes cron update <job_id> --deliver origin
```

## 检测方法

```bash
hermes cron list | grep -A5 "deliver"
# 用户面cron应显示 "deliver: origin"
# 系统守护cron应保持 "deliver: local"（静默模式）
```

## 分类标准

| 类型 | deliver | 示例 |
|:--|:--|:--|
| 用户面（推送） | origin | 晨间简报、北极星提醒、定投提醒、每日复盘、双检复盘 |
| 系统面（静默） | local | health-check、备份、Gateway看门狗、E001-guard、存活检测 |

## 经验

1. **系统恢复后的第一条检查：cron deliver状态。** WebUI+Gateway恢复只是基础设施——消息能不能到达用户是另一层。
2. **`deliver=origin`在cron上下文不可靠。** 当多个cron同时报"no delivery target resolved"时，考虑改为明确的频道ID。
3. **产出≠送达。** 文件存在 `/root/.hermes/cron/output/` 不代表用户看到了。这是"说了没做"在cron层的等价物。
4. **明天10号定投日，`deliver=local`会让提醒静默消失。** 时效性cron的交付比产出更重要。

## 时间线

```
09:58  Gateway恢复
10:00  北极星cron触发 → 产出完整 → deliver=origin解析失败 → 用户未收到
10:13  晨间简报补跑 → 产出完整 → deliver=local → 用户未收到
~10:40 用户主动问"新闻不给我哇" → 发现全量静默
~10:45 逐条修复deliver → origin
```
