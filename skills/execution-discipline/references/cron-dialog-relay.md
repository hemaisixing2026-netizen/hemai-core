# Cron→对话 中继模式

> 2026-06-10 | WebUI环境·已验证

---

## 问题

WebUI下cron无法直接推送到对话。已验证的失败尝试：
- `deliver=null`（auto-detect）→ "no delivery target resolved"
- `deliver=origin` → 同样失败
- 原因：cron在隔离会话运行，无origin可解析

## 唯一可行方案

```
cron deliver=local → 写文件到 /root/.hermes/cron/output/<job_id>/
    ↓
思行在对话中主动读取 → 转述核心内容到对话框
```

## 思行职责

1. **每个cron触发时间点后1-5分钟内**，主动读最新输出文件
2. **提取核心数据**发到对话框（不要全量粘贴cron输出）
3. **标注**：这是哪个cron、什么时间的输出
4. **用户不在线时**：cron照常跑，思行下次对话启动时补发

## 自动化辅助

业务线全扫和盘前速查cron已设置将输出同时写入workspace：
- `data/engine1-scan-latest.md`
- `data/premarket-check-latest.md`

思行可快速读取这些文件而不需要遍历cron output目录。

## 陷阱

- cron输出目录为空≠cron没跑——可能是刚创建还没到触发时间
- deliver=local的cron静默运行，`last_status=ok`不代表用户看到了
- 创建cron后必须手动补跑当前窗口（如果创建时间已过触发点）
