# 数据备份与恢复协议
> 建立：2026-06-04 · Claude审计补丁

## 备份规则

### 自动备份
- **频率**：每次心跳或对话结束时自动执行增量备份
- **位置**：`G:\openclaw-workspace\backups\workspace-YYYYMMDD-HHmmss\`
- **保留**：最近7天备份，超期自动清理

### 备份内容
- SOUL.md / MEMORY.md / IDENTITY.md / LEARNING.md
- rules/、memory/（daily日志）、data/
- 不备份：node_modules、.git、临时文件

### 验证
- 备份后自动检查文件数量≥核心文件数
- 每次恢复前先比对备份时间戳

## 恢复流程
1. 确认最新备份目录
2. 比对当前文件和备份文件的差异
3. 确认后覆盖恢复

## 加密
- **私有层数据**（baseline.md事件详情、神经劫持日志）：不在备份中明文存储
- 加密方案：GPG对称加密（待实施）
- 当前临时方案：私有层数据单独存储至加密分区
