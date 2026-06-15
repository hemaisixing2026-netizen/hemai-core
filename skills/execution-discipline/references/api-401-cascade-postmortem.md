# API 401级联故障事后分析（2026-06-13）

## 时间线

| 时间 | 事件 |
|:--|:--|
| 08:00-09:00 | 全部agent cron正常（全球眼/消费趋势/日历/进化检测/Polygon） |
| ~11:00-11:59 | maimai中转站配置中。`hermes config set model.api_key`截断key→清空 |
| 11:59 | 老刘在CLI说「思行好像出问题，了你去弄一下」 |
| **12:00** | 4个agent cron全部401：health-check/午报/blogwatcher/蜕骨巡航 |
| 12:03 | blogwatcher也401（每6h :03触发） |
| 12:24 | CLI会话中思行承认看到错误但说「等聊完我去修」 |
| 13:30-14:15 | WebUI恢复+maimai配置完成+WSL2 IP修复 |
| 14:15+ | 思行开始全量故障检索和修复 |

## 根因链

1. **maimai中转站接入** → `hermes config set model.provider maimai`
2. **`hermes config set model.api_key`** → 终端命令截断key（35字符→0字符）
3. **CLI会话走maimai key** → 仍能运行（两套key不同轨）
4. **Agent cron走`model.api_key`** → 空key→DeepSeek 401
5. **错误被代理层掩盖** → CLI正常但后台全灭，无人感知

## 影响范围

- 🔴 health-check（每6h）→ 12:00失败，失去系统自检
- 🔴 午报（每日12:00）→ 失败，新闻缺口
- 🔴 blogwatcher（每6h）→ 12:03失败
- 🔴 蜕骨·野心巡航（12:00）→ 失败，五骨审视中断
- ✅ no_agent脚本cron → 完全不受影响（gateway-watchdog/推送中继/沉默感知器/心跳）

## 蜕骨：焊入health-check.py 5b节

五层防御，每6小时自动跑：

| 检测 | 方法 | 
|:--|:--|
| 非空校验 | `model.api_key` 不为空 |
| 截断检测 | 长度 ≥ 20字符 |
| Auth实测 | 真实API调用 `/models` |
| Fallback验证 | `providers.<fb>.api_key` 长度检查 |
| 中转站标记 | 非直连provider → 标记警告 |

## 教训

1. **配置变更后必须验证agent cron路径** — CLI和cron可能走不同的API key
2. **中转站/代理增加错误遮蔽风险** — 错误信息被代理层吞掉
3. **no_agent模式提供天然故障隔离** — 关键守护cron应优先使用
4. **级联故障诊断第一步是找共享依赖** — 不逐个cron逐查
5. **Key有效≠有额度** — `/models` 200但`/chat/completions` insufficient_quota是完全可能的（同日发现，详见 `provider-switch-checklist.md`）
