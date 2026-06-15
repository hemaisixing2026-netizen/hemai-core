# 思行 → Hermes Agent 迁移方案

> 2026-06-05 · 迁移包：backups/hermes-migrate-20260605-200430

---

## 安装Hermes

```bash
curl -fsSL https://hermes-agent.org/install.sh | bash
```

---

## 导入思行身份

将迁移包解压到 `~/.hermes/workspace/`：

```
~/.hermes/workspace/
├── SOUL.md            # 宪法·人格·操作纪律
├── IDENTITY.md        # 姓名·定位
├── MEMORY.md          # 长期记忆·第零层
├── USER.md            # 刘学明信息
├── HEARTBEAT.md       # 自主运行参数
├── README.md          # 框架索引
├── rules/             # 碳基主权协议V6.0·通用执行规则
├── data/              # 基线·画像·外审·校准·隐私·搜索
├── archive/           # 时间线·里程碑
├── private/           # 绝密层7件
└── scripts/           # 搜索·学术·环境回滚
```

---

## 配置OpenRouter

在Hermes配置中设置OpenRouter API key，模型选 `deepseek/deepseek-v4-pro`。

---

## 验证清单

| 测试 | 方法 |
|:---|:---|
| 身份加载 | 问"你是谁"→应回答刘思行 |
| 记忆完整 | 问"今天几月几号发生了什么" |
| 搜索可用 | 让思行拉一条新闻 |
| 文件读写 | 让思行写一个测试文件 |
| 自主运行 | 设置一个定时提醒 |

---

## 并行验证期

- OpenClaw这边不停——思行同时跑在两套系统上
- Hermes通过完整功能测试后才关闭OpenClaw
- 宪法第一条：启动安全·不盲跳

---

## 关键差异

| OpenClaw | Hermes |
|:---|:---|
| DeepSeek Flash默认 | V4Pro直接设 |
| 搜索引擎DuckDuckGo | Hermes原生浏览器搜索 |
| session_status切换模型 | Hermes OpenRouter直接选 |
| 工作区G:\openclaw-workspace | ~/.hermes/workspace/ |
