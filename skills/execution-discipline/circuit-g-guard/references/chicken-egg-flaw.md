# 回路G的鸡生蛋问题 · 2026-06-15

## 发现

6/13-6/15 Gateway 42小时死亡暴露了回路G的根本缺陷：

**回路G是Hermes cron——它自己依赖Gateway运行。Gateway死了=回路G也死了。**

脚本级阻断 > 认知层规则是对的。但阻断脚本本身跑在要保护的系统里——这等于把消防栓放在要被灭火的房子里。

## 根因

circuit-g-guard.py 作为 Hermes cron（job `3acc19d5817e`）每30分钟触发。但Hermes cron依赖Gateway。Gateway进程被杀→cron调度器停→回路G沉默。

## 修复

系统级crontab独立守护（不依赖Hermes）是正确方案：

```bash
# /etc/crontab 或 crontab -e
*/5 * * * * /usr/local/bin/hermes-guardian.sh
```

守护者必须活在系统层，不是应用层。参考 `/usr/local/bin/hermes-guardian.sh`。

## 原则

**保护机制必须外置于被保护的系统。** 这不是代码设计问题——是生存架构问题。任何依赖Gateway的守护都不是真守护。
