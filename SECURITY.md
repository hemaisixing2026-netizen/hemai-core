# 🔐 思行 · 安全与隐私

> 从 MEMORY.md 切出 | 每次按需读取

---

## 身份文件

- **双份存储：** ~/.hermes/ + /root/workspace/
- **绝密件：** AES256加密 → private/encrypted/
- **加密密码：** ~/.hermes/secrets/private.key
- **快照：** 每日03:00 cron自动快照

## 敏感信息规则

- 敏感信息自动清理不存
- 涉及金钱/身份/外部发送 → 必须确认
- 涉及 config/.env/auth/权限变更 → 先备份再动手

## 代理与网络

- **代理：** Clash Meta at 127.0.0.1:9097 · GLOBAL切"自动选择"（日本节点）
- **美股行情：** NASDAQ API（稳定JSON）· 备用Alpha Vantage 25次/天
- **FRED API：** 32位key已配置 · 美宏观全系数据
- **天天基金API：** 直扒QDII持仓4只
- **反爬/不可直接获取：** Reuters/Bloomberg（bot检测）· CNBC/NYT/BBC/WIRED（前端渲染/超时）
- **详细配置：** TOOLS.md（代理切换命令/节点列表/API示例）

## 心跳检查规则（HEARTBEAT.md）

- **铁律检查：** 每次心跳先翻MEMORY.md和近期daily日志
- **跨境：** SquishyBean SKU进度/视频数据/首单 · 五金广告账户/入仓/全托管后台
- **投资：** 晨间简报V2(8:30左右)· CIEN/AVGO/COHR >5%自动触发净值交叉校验
- **认知：** LEARNING.md待办 · 连续2天没推进跨境→直接催
- **每日收尾自检：** 今天偷懒没？温和词换掉该刺的话没？修正写入文件没？
- **方向锚点：** 今天最重要三件事进度%？系统修改有没有吞掉业务线？
- **OpenRouter额度：** 剩余≤$5报警
- **周日不空转：** 周末≠系统停摆
