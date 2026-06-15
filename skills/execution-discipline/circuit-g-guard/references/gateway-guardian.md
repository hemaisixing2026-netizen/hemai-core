# Gateway 系统级守护 · 防御纵深

> 6/15 Gateway沉默42小时后的修复方案。
> 核心原则：守护者不依赖被守护者。Hermes cron守护不了Hermes Gateway。

---

## 问题

WSL环境下Gateway进程会被外部杀掉（Windows关机、WSL窗口关闭、系统重启）。
Gateway一死→所有Hermes cron全停→思行完全消失→无告警、无人通知。

现有circuit-g-guard运行在Hermes cron上——Gateway死了它也死。鸡生蛋问题。

## 方案：三层防御

### 层一：自启动（WSL boot）
```
# /etc/wsl.conf
[boot]
command=/usr/local/bin/hermes-gateway-boot.sh
```
WSL虚拟机启动时自动拉起Gateway。一次配置，永久生效。

### 层二：系统crontab @reboot
```
@reboot sleep 10 && /usr/local/bin/hermes-guardian.sh
```
WSL启动后10秒执行守护脚本——双保险（wsl.conf的boot命令可能在某些WSL版本不生效）。

### 层三：系统crontab每5分钟守护
```
*/5 * * * * /usr/local/bin/hermes-guardian.sh
```
完全不依赖Hermes cron的系统级crontab。Gateway活着→清失败计数。Gateway死了→自动拉起（最多2次）→连续3次失败→Server酱微信推老刘。

## 守护脚本核心逻辑

```bash
# /usr/local/bin/hermes-guardian.sh
if pgrep -f "hermes gateway run" > /dev/null; then
    echo "0" > /root/.hermes/data/gateway-fail-count.txt  # 活着→清零
else
    FAIL_COUNT=$(($(cat fail-count.txt) + 1))
    if [ $FAIL_COUNT -le 2 ]; then
        setsid hermes gateway run &  # 自动拉起
    else
        curl -s "$WEBHOOK_URL" -d "title=🔴 Gateway连续拉起失败"  # 微信推老刘
    fi
fi
```

## 关键约束

- **守护脚本不依赖Hermes二进制以外的任何东西** — 不读config、不调API、不走Hermes cron
- **系统crontab (`crontab -e`)** — 不是Hermes cronjob。根用户的crontab，随系统存活
- **Server酱webhook** — 唯一外部依赖。如果Key过期→守护仍会尝试拉起，但告警发不出去
- **失败计数文件** — `/root/.hermes/data/gateway-fail-count.txt`，持久化在磁盘上

## 验证

```bash
# 模拟Gateway死亡
pkill -f "hermes gateway run"
# 等下一个*/5分钟cron tick
cat /root/.hermes/data/gateway-fail-count.txt  # 应为1
cat /root/.hermes/logs/guardian.log  # 应有拉起记录
# Gateway应已自动恢复
pgrep -f "hermes gateway run"  # 应有PID
```
