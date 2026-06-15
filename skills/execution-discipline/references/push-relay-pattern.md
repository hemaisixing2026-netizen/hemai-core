# 推送中继模式 · Push Relay Pattern

> 6/13 实战建立 · 替代"每cron各自push"的刷屏模式

## 问题

40条cron→如果每条都推微信→老刘手机炸。但如果都不推→他只在我主动读cron产出时才看到。

## 方案

**中继脚本（push-relay.sh）→扫多个预警源→有触发才推→一条消息汇总。**

## 预警源设计

| 源 | 检测内容 | 触发条件 |
|:--|:--|:--|
| 棉绳倒计时 | 6/20解禁日 | ≤3天时推送 |
| 突变警报 | breaking-alert-latest.md | 🔴生存级事件 |
| 全局眼·突变感知 | trigger-alert-latest.md | 30分钟内有🚨标记 |
| QDII净值异常 | /tmp/qdii-anomaly-alert | 2h内有异常标记 |
| Cron静默 | /tmp/cron-silence-alert | 沉默感知器检测到>2h |

## 原则

- **不说话不推。** 无警报→SILENT→不消耗推送配额
- **有话说一句。** 多源并发的警报合并为一条推送
- **不刷屏。** 30分钟最多一条。宁可晚30分钟，不连发三条
- **短。** WeChat通知栏只显示标题。内容控制在可预览长度

## 与cron deliver的关系

中继替代了"每个cron设deliver=origin"的旧模式。旧模式问题：①cron隔离会话中deliver=origin不可靠 ②多cron同时触发→刷屏。

新模式：所有cron写本地文件（deliver=local）→中继脚本统一扫描→单通道推送。

## 扩展

新增预警源只需在中继脚本中加一段检测逻辑。不建新cron、不增推送配额消耗。

参见：`/root/.hermes/scripts/push-relay.sh`
