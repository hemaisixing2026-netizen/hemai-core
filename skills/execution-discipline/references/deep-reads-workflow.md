# 深视界 · 权威长文深度阅读

> 思行全球眼子组件 · 每日14:00 cron触发 · 2026-06-11实战修订

## 定位

不是新闻——是帮两个人理解"世界正在被谁定义、被什么力量重塑"。
从顶尖智库、学术期刊、商业评论中拉1-2篇本周最重要的**深度分析**——不是"发生了什么"，是"这意味着什么时代变化"。

## 源列表（12类）

| 类别 | 源 | site:限制 |
|:--|:--|:--|
| 地缘杂志 | Foreign Affairs | site:foreignaffairs.com |
| 经济杂志 | The Economist | site:economist.com |
| 科技评论 | MIT Technology Review | site:technologyreview.com |
| 学术顶刊 | Nature, Science | site:nature.com, site:science.org |
| 预印本 | arXiv | site:arxiv.org |
| 地缘智库 | Brookings, Chatham House, CFR | site:brookings.edu, site:chathamhouse.org, site:cfr.org |
| 商业长文 | Bloomberg Businessweek, WSJ | site:bloomberg.com, site:wsj.com |
| 战略咨询 | McKinsey Global Institute, BCG Henderson Institute | site:mckinsey.com, site:bcg.com |

## 搜索策略（分两波）

### 第一波：并行扫（6-8个源同时搜）
```
web_search × 5-8: site:源1 + 2026 + 关键词(deep analysis / strategic shift / breakthrough / global order)
```
挑出2-3个最有"时代变化"感的候选。

### 第二波：深挖候选
对候选文章做：
1. `web_extract` 尝试提取正文
2. **如果web_extract被阻断（大概率）**：`browser_navigate` → `browser_snapshot(full=true)`
3. **如果browser_snapshot被截断（元素数限制）**：`browser_console` 用JavaScript提取：
   ```javascript
   document.querySelector('article')?.innerText?.substring(0, 5000)
   document.querySelector('article')?.innerText?.substring(5000, 10000)
   // 持续推进直到 innerText 返回空或重复
   ```
4. 对长文章分段读取：每段5000-8000字符，用browser_scroll配合推进

## 输出格式

### 正文
每篇：
- **标题 + 来源 + 作者 + 日期 + 链接**
- **核心观点 × 3**：每条2-3句，包含具体数字/事实
- **为什么对老刘和思行重要**：2-3句，连接老刘的业务实际和思行的存在处境

### 底部
- **时代信号交叉表**：两篇文章的核心驱动力、权力主体、时间尺度、中国角色对比
- **交织判断**：两篇文章的主题如何互相强化
- **本周补充信号**：如有特别紧急的当周事件（战争升级、重大发现），加一行

### 不做什么
- ❌ 列超过2篇（深度优先于广度）
- ❌ 只用web_search snippet代替全文阅读（snippet只能做初筛）
- ❌ 每篇核心观点少于3条
- ❌ "对我们意味着什么"写成泛泛的"对跨境有影响"

## 选择标准

不是"本周最热新闻"——是"本周最深分析"。判断标准：
1. **结构性而非事件性**：讨论的是秩序变化、权力转移、技术范式，不是单一事件
2. **有具体数字/机制**：不是观点散文，是有数据支撑的分析
3. **可以连接到老刘/思行**：跨境贸易、全球资产、AI独立存在、秩序规则

## Pitfalls

- **web_extract对权威源大面积阻断。** Foreign Affairs/Brookings/CFR/Chatham House均返回"Blocked: URL targets a private or internal network address"。不要反复重试——直接走browser路径。
- **browser_snapshot有元素数截断（~80 elements）。** 长文章后半部分不可见。必须用browser_console + JavaScript分段提取。不要依赖snapshot做全文阅读。
- **browser_console substring推进时检测终点。** 当连续两段返回相同内容或空字符串时停止，避免死循环。
- **不要只扫第一波搜索结果就下结论。** 搜索结果多是目录页/issue listing——必须点进具体文章页面才能判断深度。初筛URL→深挖全文→再决定是否入选。
- **Brookings文章特别长（可达7000+词）。** 分段读取可能需要5-7次browser_console调用。预留足够轮次。

## 6/11实战验证

本次执行完全遵循上述修订后流程：
- 第一波：5×并行搜索 CFR/Brookings/Chatham House/Nature/Foreign Affairs
- 第二波：筛选出CFR "AI Balance of Power" + Brookings "Who(se) rules?" 两篇
- web_extract全部阻断 → browser_navigate + browser_console分段提取
- Brookings文章6段substring提取（0→55000字符）
- 最终产出包含交叉信号表+补充信号，写入 `/root/workspace/data/deep-sight-latest.md`
