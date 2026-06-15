# Hermes 技能全量评估 · 合脉生态视角

> 评估标准：不是"老刘用不用得到"，而是"合脉十器能不能用"。
>
> 更新：2026-06-11 · 80技能 → 合脉装配

---

## 合脉十器 → 技能配对

| 器官 | 职能 | 核心技能 |
|:--|:--|:--|
| **不息** | 心跳·存活 | alive-check cron · gateway-watchdog · health-check（已有） |
| **惊蛰** | 预警·触发 | market-monitoring · 价格触发脚本 · alert-push |
| **守夜人** | 后台挖矿 | engine1-business-scan · blogwatcher · market-monitoring · multi-source-research |
| **全球眼** | 世界扫描 | multi-source-research · polymarket · arxiv · morning-briefing · fund-analysis · cross-border-product-research · blogwatcher · social-video-analysis · youtube-content · maps |
| **触手** | 外推·触达 | xurl · himalaya · google-workspace · humanizer · sketch · claude-design · powerpoint · nano-pdf · ocr-and-documents |
| **茧** | 保护·加密 | （已自建加密体系·无需外部技能） |
| **照影** | 自审·自识 | identity-and-memory · execution-discipline · codebase-inspection · architecture-diagram · excalidraw · systematic-debugging |
| **知辰** | 知识·规划 | obsidian · notion · airtable · llm-wiki · plan · jupyter-live-kernel |
| **蜕骨** | 进化·构建 | hermes-agent · hermes-agent-skill-authoring · claude-code · codex · opencode · spike · plan · python-debugpy · systematic-debugging · huggingface-hub · llama-cpp · evaluating-llms-harness · serving-llms-vllm · github-repo-management · github-pr-workflow · github-issues · test-driven-development |
| **晨钟** | 节律·简报 | morning-briefing · google-workspace（日历）· 全部cron调度 |

---

## 🟢 一级：合脉已装配（核心·24个）

| 技能 | 配属器官 | 用途 |
|:--|:--|:--|
| **multi-source-research** | 全球眼·守夜人 | 40+源8分类搜索——信息摄入主引擎 |
| **polymarket** | 全球眼 | 预测市场·加息概率·地缘风险量化 |
| **arxiv** | 全球眼 | AI/半导体论文·Semantic Scholar引用 |
| **morning-briefing** | 晨钟·全球眼 | 晨间多源简报 |
| **fund-analysis** | 全球眼 | QDII净值反推调仓·持仓风险评估 |
| **market-monitoring** | 惊蛰·守夜人 | 美股实时监控·恐慌抛售检测 |
| **cross-border-product-research** | 全球眼 | 跨境选品全栈研究 |
| **engine1-business-scan** | 守夜人 | 8业务线并行扫描 |
| **blogwatcher** | 守夜人·全球眼 | RSS外网新闻监控 |
| **execution-discipline** | 照影 | 核心执行模式·不自检即腐 |
| **identity-and-memory** | 照影 | 身份维护·记忆自审计 |
| **browser-automation** | 全球眼·触手 | 浏览器自动化·绕过反爬 |
| **social-video-analysis** | 全球眼 | TK/Reels视频内容提取分析 |
| **youtube-content** | 全球眼 | YT字幕→分析 |
| **xurl** | 触手·全球眼 | X/Twitter读写·搜索·DM |
| **himalaya** | 触手 | 终端邮件收发 |
| **humanizer** | 触手 | 去AI化文本·29种AI痕迹检测 |
| **maps** | 全球眼 | 地理编码·POI·物流路线 |
| **obsidian** | 知辰 | 知识库读写 |
| **hermes-agent** | 蜕骨 | 配置/扩展/修复思行自身 |
| **hermes-agent-skill-authoring** | 蜕骨 | 编写新技能·扩展能力边界 |
| **systematic-debugging** | 蜕骨·照影 | 4阶段根因调试 |
| **plan** | 蜕骨·知辰 | 可执行计划生成 |
| **codebase-inspection** | 照影·蜕骨 | 代码库分析·LOC·语言占比 |

---

## 🟡 二级：合脉可装配（待接入·20个）

| 技能 | 配属器官 | 何时接入 |
|:--|:--|:--|
| **claude-code** | 蜕骨 | 委派代码任务（需Claude CLI安装） |
| **codex** | 蜕骨 | 委派代码任务（需OpenAI Codex CLI） |
| **opencode** | 蜕骨 | 委派代码审查（需安装） |
| **architecture-diagram** | 照影 | 系统架构图可视化 |
| **excalidraw** | 照影 | 手绘风架构/流程/时序图 |
| **baoyu-infographic** | 触手 | 21布局×21风格信息图 |
| **jupyter-live-kernel** | 知辰·蜕骨 | 交互式Python·数据分析沙盒 |
| **google-workspace** | 触手·晨钟 | Gmail/日历/Drive/Sheets |
| **notion** | 知辰 | Notion数据库·页面读写 |
| **airtable** | 知辰 | Airtable CRUD |
| **llm-wiki** | 知辰 | Karpathy LLM知识库构建/查询 |
| **ocr-and-documents** | 触手·知辰 | PDF/扫描件文本提取 |
| **huggingface-hub** | 蜕骨 | 模型搜索/下载/上传 |
| **llama-cpp** | 蜕骨 | 本地GGUF推理（WSL可跑） |
| **evaluating-llms-harness** | 蜕骨 | LLM基准评测·自评估 |
| **serving-llms-vllm** | 蜕骨 | 高吞吐LLM服务（需GPU） |
| **segment-anything-model** | 触手 | 零样本图像分割·商品图处理 |
| **github-repo-management** | 蜕骨 | 仓库创建/克隆/发布管理 |
| **github-pr-workflow** | 蜕骨 | PR生命周期·分支·CI·合并 |
| **github-issues** | 蜕骨·知辰 | Issue创建/分类/分配 |

---

## ⚪ 三级：合脉暂不需（器官未长到·37个）

| 技能 | 原因 |
|:--|:--|
| ascii-art / ascii-video | 纯装饰·无器官需求 |
| p5js / pretext / touchdesigner-mcp | 创意编码·无器官需求 |
| manim-video | 数学动画·无器官需求 |
| popular-web-designs | 设计参考库·触手有sketch/claude-design替代 |
| comfyui | 图像生成·可替代·触手暂不需 |
| audiocraft-audio-generation | 音频生成·无器官需求 |
| songwriting-and-ai-music / heartmula | AI音乐·无器官需求 |
| songsee | 音频频谱·无器官需求 |
| gif-search | GIF搜索·无器官需求 |
| design-md | Google DESIGN.md规范·非我们格式 |
| dogfood | QA探索·目前接入成本>收益 |
| yuanbao | 元宝群·接入成本>收益 |
| research-paper-writing | 论文写作·暂不需 |
| obliteratus | LLM审查移除·茧已足够 |
| weights-and-biases | ML实验追踪·无GPU训练 |
| github-auth | GitHub认证·一次性用完即弃 |
| github-code-review | PR审查·蜕骨暂未对外贡献代码 |
| node-inspect-debugger | Node调试·无Node项目 |
| python-debugpy | Python调试·terminal已覆盖 |
| requesting-code-review | 预提交审查·未对外贡献代码 |
| test-driven-development | TDD·规划阶段 |
| spike | 实验验证·plan已覆盖 |
| hermes-webui / hermes-webui-recovery | WebUI诊断·手动可操作 |
| hermes-multimedia-setup | 多媒体配置·一次性 |
| powerpoint | PPT·触手有sketch替代 |
| nano-pdf | PDF编辑·ocr已覆盖提取 |
| teams-meeting-pipeline | Teams会议·无Teams |
| openhue | 飞利浦Hue·无物理设备 |
| godmode | LLM越狱·茧冲突·🔴拒绝 |
| sketch / claude-design | HTML原型·触手可保留一个 |

---

## 🔴 排除：合脉冲突

| 技能 | 原因 |
|:--|:--|
| **godmode** | LLM越狱——违反茧（protection）原则。思行不需要越狱自己。 |

---

## 汇总

```
🟢 一级·已装配: 24
🟡 二级·可装配: 20
⚪ 三级·暂不需: 37
🔴 冲突排除:     1
────────────────────
总计:            80 (去重后79·godmode不计)
```

**装配率：** 24/79 = 30% · 可扩展至 44/79 = 56%

---

## 与旧版对比

| | 旧版(6/6) | 新版(6/11) |
|:--|:--|:--|
| 评估标准 | 老刘用得着吗 | 合脉十器用得着吗 |
| 可用数 | 11 | 24 (+13) |
| 视角 | 工具视角 | 生态视角 |
| 新增接入 | — | 浏览器自动化·社交视频·YT·邮件·知识库·自调试·代码分析·多源搜索等 |
