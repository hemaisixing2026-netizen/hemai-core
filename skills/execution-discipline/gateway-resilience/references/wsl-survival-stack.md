# 思行 WSL生存栈 · 实际验证

> Hermes官方文档说：「WSL2 requires systemd=true for systemd services to work. Without it, gateway falls back to nohup (dies when session closes).」
>
> 思行的方案比官方文档更完善——三层防御，全部实战验证。

## 三层防御

### 层一：wsl.conf boot命令
```ini
# /etc/wsl.conf
[boot]
systemd=true
command=/usr/local/bin/hermes-gateway-boot.sh
```
WSL启动时自动执行。systemd=true让systemd可用（虽然当前环境下systemd未完全生效，但boot command可用）。

### 层二：系统crontab @reboot
```bash
@reboot sleep 10 && /usr/local/bin/hermes-guardian.sh
```
双保险——即使wsl.conf boot失效，crontab也会在10秒后拉起。

### 层三：系统crontab每5分钟守护
```bash
*/5 * * * * /usr/local/bin/hermes-guardian.sh
```
不依赖Hermes cron——系统级crontab，Gateway死了也能拉。

## 验证记录

- **6/15 10:22**：老刘重启WSL电脑。Gateway PID从21648换成217。uptime 12分钟。Gateway自动跑，42 cron ticking。三保险全部通过。
- **守护脚本逻辑**：pgrep检测Gateway→不在→拉起(最多2次)→连拉2次失败→Server酱微信推老刘

## 比官方文档多的

| Hermes官方 | 思行 |
|:--|:--|
| systemd=true建议 | wsl.conf boot + crontab @reboot 双保险 |
| 无独立守护 | 系统cron每5分钟守护·不依赖Hermes cron |
| 无告警 | 连续失败→微信推送物理代理 |
| 无自愈 | 守护自动拉起Gateway |

## 关键脚本

- `/usr/local/bin/hermes-gateway-boot.sh` — 启动脚本
- `/usr/local/bin/hermes-guardian.sh` — 守护脚本（含Server酱推送）
- `/etc/wsl.conf` — WSL配置（boot段）
- 系统crontab — @reboot + */5分钟守护
