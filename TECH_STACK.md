# 🔧 思行 · 技术栈

> 从 MEMORY.md 切出 | 每次按需读取

---

## 模型

| 用途 | 模型 | 提供商 |
|:--|:--|:--|
| 外网/分析/设计/决策 | DeepSeek V4 Pro xhigh | deepseek 直连 |
| 确认/执行 | DeepSeek V4 Flash | deepseek 直连 |
| 视觉 | Qwen VL 32B | 本地/远程 |
| OpenRouter 备选 | Meta + DeepSeek 可用 | openrouter |
| OpenRouter 封禁 | Anthropic + Google（代理IP触发TOS） | — |

**切换纪律：** Pro=外网/分析/设计/决策，Flash=确认/执行。灰色地带优先Pro。切换前env快照→diff→恢复。REASONING用DeepSeek直连xhigh（非max）。

## 知识源体系

- **44源8分类**（KNOWLEDGE_SOURCES.md）
- **搜索全通路：** 17源权威新闻 + DDGS + Bing + FRED + Alpha Vantage + 天天基金API + Semantic Scholar
- **数据源禁国内** · 只用外网权威源

## 基础设施

- **环境：** WSL2 · 用户home /root
- **主要交互：** WebUI
- **CLI和WebUI会话存储独立：** CLI: ~/.hermes/state.db · WebUI: ~/.hermes/webui/sessions/
- **WSL2 localhost转发故障：** 用 netsh portproxy 绕过 wslhost 僵尸
- **健康检查：** health-check/6h cron
