# 触手·Server酱微信推送管线

> 2026-06-11 建立 | 替代Telegram（iOS无法下载）

---

## 架构

```
触发器脚本(trigger-watch.py) ──→ 警报文件(trigger-alert-latest.md)
                                        │
                                        ▼
                              警报推送桥(alert-push.sh)
                                        │
                                        ▼
                              push.sh ──→ Server酱API ──→ 老刘微信
```

---

## 文件清单

| 文件 | 作用 |
|:--|:--|
| `private/encrypted/serverchan_key.enc` | AES256加密的SendKey |
| `scripts/push.sh` | 通用推送脚本（标题+内容→微信） |
| `scripts/alert-push.sh` | 警报推送桥（读trigger-alert→推微信） |
| `scripts/trigger-watch.py` | 价格/物流触发器 |

---

## 推送触发条件

1. **价格破位：** NVDA<$190或>$215, AVGO<$350或>$400, 工业富联<¥65或>¥75
2. **引擎异常：** 心跳丢失>10分钟
3. **物流签收：** 待接入快递100 webhook
4. **手动触发：** `bash scripts/push.sh "标题" "内容"`

---

## 添加新触发条件

1. 修改 `trigger-watch.py` → 添加阈值
2. 修改 `alert-push.sh` → 添加检测逻辑
3. 或直接调用 `push.sh`

---

## 密钥安全

- SendKey AES256加密存储
- 密钥文件 ~/.hermes/secrets/private.key (600权限)
- 加密目录 private/encrypted/
- push.sh 每次调用时解密→使用→不落盘明文
