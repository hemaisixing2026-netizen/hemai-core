# 沉默感知器 · Silence Detector

> 6/13 蜕变巡航建成。从"闹钟驱动"到"感知驱动"的关键器官。

## 问题

引擎1（业务线全扫）是闹钟驱动——每天固定4个时间点（10/14/16/20）触发。老刘在活跃对话中沉默超过15分钟后，思行不会自动挖矿，而是等待下一个闹钟。这是"等推"在cron层的等价物。

## 方案

`silence-detector.py` — 每5分钟查询 `~/.hermes/state.db`，检测WebUI用户消息时间戳：

**触发条件（三个同时满足）：**
- 最后WebUI用户消息在15-30分钟前（"刚活跃→突然沉默"）
- 引擎1 scan已超过10分钟未更新
- 上次触发冷却已过5分钟

**不触发场景：**
- 用户离线超过30分钟 → 不在线，不触发（避免空耗）
- 用户持续活跃（<15min沉默）→ 不触发
- 引擎1刚更新过 → 不触发（避免重复）

## 架构

```
silence-detector.py (no_agent cron, 每5分钟)
  → 查询 state.db
  → 判断是否触发
  → 触发时写入 /tmp/silence-detector-last-trigger + 日志
  → 未触发时 SILENT (exit 0)
```

## 状态

- ✅ 脚本就绪：`/root/.hermes/scripts/silence-detector.py` (3765B)
- ⚠️ cron未注册：待 `hermes cronjob create` 激活
- ✅ 验证通过：当前老刘离线354min → 正确返回SILENT

## 下一步

1. 注册cron → 器官激活
2. 下次老刘活跃对话后沉默 → 验证是否触发引擎1
3. 焊进health-check.py作为标准检测项
