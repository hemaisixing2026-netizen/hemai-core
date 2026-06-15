# 搜索能力架构 V2

> 2026-06-05 · 双通道

## 通道一：Bing（金融/新闻）

| 方法 | 范围 | 状态 |
|:---|:---|:--:|
| bing-search.ps1 + 日本节点 | 金融·新闻·股票·通用 | 🟢 |
| 限制 | 学术查询被IP污染 | ⚠️ |

## 通道二：学术（Semantic Scholar + arXiv）

| 方法 | 范围 | 状态 |
|:---|:---|:--:|
| api.semanticscholar.org（免费·免key）| 全学科·论文标题+摘要+作者 | 🟢 |
| arxiv.org/search | CS·AI·数学·物理·经济 | 🟢 |
| arxiv.org/pdf/e-print | 论文全文 | 🟢 |

## 通道三：数据（API直读）

| 方法 | 范围 | 状态 |
|:---|:---|:--:|
| NASDAQ API | 美股实时 | 🟢 |
| FRED API | 美国经济 | 🟢 |

## 通道四：新闻深度（web_fetch 直读）

| 白名单源 | 状态 |
|:---|:--:|
| MIT Technology Review | 🟢 |
| The Verge | 🟢 |
| WIRED | 🟢 |
| Anthropic Institute | 🟢 |
| Dario Amodei 个人站 | 🟢 |
