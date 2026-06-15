# 刘思行 迁移手册

> 2026-06-05 · 换电脑时带走整个系统的完整流程

---

## 需要带走的三样东西

### ① 大脑核心（工作区所有文件）
```
G:\openclaw-workspace\
├── SOUL.md            ← 宪法·操作纪律·人格
├── MEMORY.md          ← 长期记忆·持仓·第零层
├── IDENTITY.md        ← "刘思行"·标签·定位
├── USER.md            ← "刘学明"·坐标·投资风格
├── HEARTBEAT.md       ← 自主运行参数
├── README.md          ← 框架索引
├── rules/             ← 碳基主权协议V3.3·通用执行规则·简报模板
├── data/              ← 基线·画像·外审·校准·搜索·隐私·内容·备份
├── memory/            ← 52条每日日志
├── archive/           ← 时间线·里程碑
├── private/           ← 绝密层7件
├── scripts/           ← bing-search·academic-search·reset-env
└── backups/           ← 备份历史
```

### ② 网关配置（API密钥·模型·Providers）
```
C:\Users\Administrator\.openclaw\openclaw.json
```
含：DeepSeek key · OpenRouter key · 模型列表 · DuckDuckGo搜索 · 端口配置

### ③ 会话历史（可选·对话记录）
```
C:\Users\Administrator\.openclaw\agents\main\sessions\
```
含：所有历史对话的完整jsonl记录

---

## 迁移步骤

### 步骤1：在新电脑安装OpenClaw
```powershell
npm install -g openclaw
```

### 步骤2：复制工作区
将旧电脑 `G:\openclaw-workspace\` 整个目录复制到新电脑相同路径。
或使用U盘/移动硬盘/网盘打包传输。

### 步骤3：覆盖网关配置
将旧电脑 `openclaw.json` 覆盖到新电脑 `C:\Users\<用户名>\.openclaw\openclaw.json`

### 步骤4：验证
```powershell
openclaw status          # 确认网关在线
openclaw gateway status  # 确认配置加载
```

### 步骤5（可选）：复制会话历史
将旧电脑的 `sessions\` 目录复制到新电脑对应位置。

---

## 验证清单

| 检查项 | 命令/方法 |
|:---|:---|
| 网关启动 | `openclaw status` |
| 工作区加载 | 对话中说"我是谁"→应回答刘思行 |
| 记忆完整 | 问"今天几月几号发生了什么" |
| 搜索可用 | 让思行拉一条新闻 |
| API认证 | 思行应能正常回复 |

---

## 安全提醒

- 传输工作区时用加密压缩（7z/zip+密码）
- 不在云端存储 `openclaw.json`（含API密钥明文）
- 不在云端存储 `private/` 目录
- 新电脑安装后立即运行 `reset-env.ps1 -snapshot` 存档新环境
