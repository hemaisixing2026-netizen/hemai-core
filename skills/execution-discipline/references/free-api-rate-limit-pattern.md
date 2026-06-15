# 免费API限流·标记文件模式

> Polygon.io 免费层实战 · 2026-06-13

## 问题

免费API硬限流（5 calls/min），批量拉取超过限流→HTTP 429→数据丢失。简单的`sleep(12)`不够——因为前一次运行可能刚消耗了限流窗口。

## 模式

三步保证不超限流：

### 1. 脚本开头检测标记文件

```python
rate_marker = "/tmp/<api>-last-call"
if os.path.exists(rate_marker):
    last_call = os.path.getmtime(rate_marker)
    elapsed = time.time() - last_call
    if elapsed < 65:  # 限流窗口+5秒缓冲
        time.sleep(65 - elapsed)
```

### 2. 批次间等待

```python
for i, item in enumerate(items):
    fetch(item)
    if (i + 1) % 5 == 0 and i < len(items) - 1:
        time.sleep(65)  # 确保窗口重置，不赌刚好60秒
```

### 3. 脚本收尾写入新标记

```python
with open("/tmp/<api>-last-call", "w") as f:
    f.write(str(time.time()))
```

## 原则

- **不靠cron调度间隔保证限流** — cron间隔可能漂移，脚本自带限流检测
- **65秒不是60秒** — 留5秒缓冲避免边界碰撞
- **静默降级** — 单票403静默跳过，不阻断整批
- **标记文件放/tmp** — 重启自动清除，不留死状态

## 适用场景

- Polygon.io免费层（5/min）
- Alpha Vantage免费层（5/min）
- 任何有硬限流的免费API
- cron定期拉取批量数据

## 对接

脚本: `/root/.hermes/scripts/polygon-pull.py`
Cron: `a94065d6bcfc` (每日07:00/16:30, no_agent)
