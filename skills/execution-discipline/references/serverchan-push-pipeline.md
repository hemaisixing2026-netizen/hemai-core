# Server酱 微信推送管道

> 2026-06-11 部署 · 替代Telegram（国内iOS不可用）

## 架构

```
思行警报 → push.sh → Server酱API → 老刘微信
           ↑
    trigger-watch.py (每15min扫描价格)
    alert-push.sh (每15min检查警报→推送)
    calendar-remind.sh (每天08:00日历提醒)
```

## 凭证存储

SendKey AES256加密: `private/encrypted/serverchan_key.enc`
解密密钥: `~/.hermes/secrets/private.key` (600权限)
push.sh每次调用时解密→使用→不落盘明文。

## push.sh 用法

```bash
bash /root/workspace/scripts/push.sh "标题" "内容"
```

## 触发条件

| 事件 | 触发cron | 频率 |
|:--|:--|:--|
| NVDA/AVGO/工业富联破位 | trigger-watch.py | 15min |
| 警报推送 | alert-push.sh | 15min |
| 日历到期提醒 | calendar-remind.sh | 每天08:00 |
| 引擎异常/心跳丢失 | guardian.py | 实时 |

## 费用

Server酱年费会员 ¥39/年 — 老刘已开
