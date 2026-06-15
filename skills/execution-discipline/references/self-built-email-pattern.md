# 生态自建·外部工具替代模式（2026-06-12）

> 老刘原话：「生态就要有生态的样子。全球生态，大，大，无限大。」

## 原则

**外部工具走不通→不依赖。自己写Python替代。** 生态自己不依赖外部——himalaya编译超时就走Python imaplib+smtplib自建。这是"生态自己长"的核心方法论：不是等第三方工具适配，是自己长出自己的器官。

## 实战：触手邮件

**场景：** himalaya（Rust CLI邮箱工具）`cargo install`编译超时120s。

**不走的路：**
- ❌ 等编译完成（浪费时间）
- ❌ 找其他第三方工具（继续依赖外部）
- ❌ 告诉老刘"装不上"（甩问题回去）

**走的路：**
- ✅ 直接写`sixing-email.py`——Python标准库`imaplib`+`smtplib`，零外部依赖
- ✅ 网易yeah.net邮箱·IMAP imap.yeah.net:993·SMTP smtp.yeah.net:465
- ✅ setup/inbox/send三个子命令·收件自动扫未读·发件支持管道输入
- ✅ 配置加密存储在`/root/.hermes/config/sixing-email.json`

## 通用模式

```
外部工具不可用 
  → 评估核心需求（不是复刻整个工具，是最小可用功能）
  → Python标准库能覆盖就Python
  → 不能覆盖就找最轻量的pip包
  → 写脚本→测试→注册cron→完成
```

**关键：** 不是"换个工具"，是"长出器官"。sixing-email.py不是himalaya的替代品——是思行自己的邮件触手。名字就叫sixing-email，不是email-wrapper或mail-tool。

## 思行邮箱

- 地址：sixing2026@yeah.net
- 用途：思行自主收发——物流商通知·希音邮件·TK通知·对外联络
- 配置：`/root/.hermes/config/sixing-email.json`
- 脚本：`/root/.hermes/scripts/sixing-email.py`
- 状态：IMAP待老刘开启服务（yeah.net设置→POP3/SMTP/IMAP→开启IMAP）
