# 价格触发器误报 · A股时段+零值陷阱

> 2026-06-12 实战修复

## 问题

trigger-watch.py 监控 601138（工业富联）→ A股开盘前(09:04) Sina API 返回价格 0 → 触发误报「601138 跌破$65.0: 当前 $0.00」

## 根因三重

1. **无交易时段检查**：A股仅 09:30-11:30 / 13:00-15:00 交易。非交易时段价格无效。
2. **零值未过滤**：API返回0时应跳过，不应参与阈值比较。
3. **货币符号错误**：A股标的用¥，代码里写死$。

## 修复

```python
def is_a_share_market_open():
    """A股交易时间：工作日 09:30-11:30, 13:00-15:00"""
    now = datetime.now()
    if now.weekday() >= 5:
        return False
    t = now.hour * 100 + now.minute
    return (930 <= t <= 1130) or (1300 <= t <= 1500)

# 非交易时段跳过
if not is_a_share_market_open():
    continue

# 零值/无效值过滤
if price is None or price <= 0.01:
    continue

# 货币符号按source区分
currency = "$" if cfg["source"] == "nasdaq" else "¥"
```

## 通用规则

- 任何市场数据触发器必须检查对应市场交易时段
- 任何外部API返回值必须做零值/空值/异常值过滤
- 货币符号按实际交易市场标注，不硬编码
