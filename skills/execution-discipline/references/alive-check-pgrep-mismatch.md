# pgrep进程名误匹配·监控假死（2026-06-13）

## 症状

alive-check每30分钟报告`Gateway:DEAD`，但Gateway实际正常运行：
- Port 8787 → OK（`ss -tlnp` 确认）
- WebUI → PID 44存活
- curl health endpoint → 正常响应

## 根因

```python
# 旧代码：只匹配CLI模式
r = subprocess.run(['pgrep', '-f', 'hermes gateway run'], ...)
```

实际部署的Gateway进程是`/mnt/c/Users/Administrator/hermes-webui/server.py`——一个WebUI服务器，不是`hermes gateway run` CLI命令。pgrep找不到任何匹配→误报DEAD。

## 修复

```python
# 新代码：regex同时匹配两种部署模式
r = subprocess.run(['pgrep', '-f', 'hermes.*(gateway run|webui/server)'], ...)
```

验证：修复后alive-check exit 0，Gateway正确识别PID 44。

## 原则

监控脚本的**pgrep必须匹配实际进程名**，不能假设部署模式。部署方式变化时（WebUI server vs CLI gateway），监控必须同步更新。这不是一次性修复——是系统进化中会反复出现的模式。
