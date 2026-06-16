# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 已验证的可靠数据源

### 外网新闻获取流程（2026.6.1 更新 — 节点结构已变）
- **铁律**：**跑外网前先切节点**，不默认DIRECT出发
- **⚠️ 节点结构变更**：原NCloud组已不存在！当前代理结构已改为GLOBAL+自动选择+手动选择三层

**当前代理结构：**
| 组 | 类型 | 说明 |
|:--|:--|:--|
| **GLOBAL** | Selector | 全局开关，切到"自动选择"或"手动选择" |
| **自动选择** | URLTest | 自动测速选最优节点（当前：日本东京09）| **推荐** |
| **手动选择** | Selector | 手动选节点（当前：日本东京02） |
| **美国节点** | Vless/Hysteria2 | 可开CNBC/AP/BBC等 |

**标准操作流程：**
1. 切GLOBAL到"自动选择"（日本节点）×保证日本节点接通
2. 跑外网数据
3. 如需美国站点（CNBC/AP），切换手动选择到"美-国德克萨斯XX"节点

**切换命令：**
```powershell
# 切GLOBAL到自动选择（日本节点）
$body = @{name = "自动选择"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:9097/proxies/GLOBAL" -Method PUT -Body $body -ContentType "application/json; charset=utf-8"

# 切手动选择到美国节点
$body = @{name = "美-国德克萨斯01|BGP|CMCU"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://127.0.0.1:9097/proxies/%E6%89%8B%E5%8A%A8%E9%80%89%E6%8B%A9" -Method PUT -Body $body -ContentType "application/json; charset=utf-8"
```

**节点现状（6/1）**：日本节点（东京01-09）多数可用，美国节点（德克萨斯01-06+美国A-E）部分可用。新加坡/英国节点也有可用。

**请求超时说明**：搜索超时是**搜索API自身不稳定**，非代理问题。直链API（NASDAQ/FRED/MIT Tech Review）全部稳定。超时后降级路径：切日本节点 + 缩短关键词 → 改用web_fetch直扒URL → 已知知识库标注

### 美股行情 🟢 可用
| 数据源 | 方法 | 示例 |
|--------|------|------|
| **NASDAQ官方API** | web_fetch JSON | `https://api.nasdaq.com/api/quote/AAPL/info?assetclass=stocks` → 实时价+涨跌幅+成交量
| **NASDAQ API摘要** | web_fetch JSON | `https://api.nasdaq.com/api/quote/AAPL/summary?assetclass=stocks` → PE、市值、52周范围、分红
| **Finviz** | web_fetch HTML | `https://finviz.com/quote.ashx?t=AAPL` → 综合财务/估值数据

### 基金持仓 🟢 可用
| 数据源 | 方法 | 示例 |
|--------|------|------|
| **天天基金API（股票持仓）** | web_fetch raw-html | `https://fundf10.eastmoney.com/FundArchivesDatas.aspx?type=jjcc&code=005698&topline=10&year=&month=&rt=0.12345`

### 代理控制 🟢 可自动切换
- **API**：Clash Meta at 127.0.0.1:9097（无需密码）
- **代理组**：NCloud（手动选择组）
- **最佳节点**：`[Vless] 日本 [直连]`（4/5站点可达，速度最快）
- **切换命令**：`Invoke-RestMethod -Uri "http://127.0.0.1:9097/proxies/NCloud" -Method PUT -Body '{"name":"[Vless] \u65e5\u672c [\u76f4\u8fde]"}' -ContentType "application/json"`
- **美国节点**（美国 A-E）：只能打开CNBC/BBC/AP，打不开NYT/Reuters/Bloomberg
- **Reuters/Bloomberg**：所有节点都打不开（bot检测拦截，非IP问题）

### 外网新闻 🟢 白名单源（2026.5.24 更新，已实测验证）
**铁律**：所有结论必须有白名单源的原文可查。不从搜索摘要里摘数据做结论。每一篇新闻/数据必须标注出处。

#### ✅ 白名单（已实测通过日本节点可用）
| 源 | 访问方式 | 实测状态 |
|----|---------|:-------:|
| **NASDAQ API** | api.nasdaq.com/api/quote/XXX/info → 实时价/涨跌幅/52周 | 🟢 稳定JSON |
| **FRED API（美联储）** | api.stlouisfed.org/fred/series/observations → GDP/利率/通胀/失业 | 🟢 稳定JSON |
| **US Treasury** | home.treasury.gov → 国债收益率曲线 | 🟢 页面可读 |
| **MIT Technology Review** | technologyreview.com → 文章全文 | 🟢 直抓可读 |
| **AP News** | apnews.com → 图片报道+部分文字 | 🟡 JS渲染限图片caption |
| **NASA** | nasa.gov | 🟢 可读 |

#### ❌ 前端渲染/反爬（日本节点无法获取原文）
| 源 | 原因 | 替代方案 |
|----|:----|:--------|
| CNBC | 纯前端渲染，只返回CSS | 找具体文章URL（非首页） |
| NYT | paywall + 超时 | 搜索摘要+对比多源 |
| BBC | 超时 | 搜索摘要+对比多源 |
| WIRED | 前端渲染 | 搜索摘要+对比多源 |
| Goldman Sachs | 需邮箱登录 | 用搜索摘要（多源交叉验证可用） |
| Reuters/Bloomberg | bot检测拦截所有节点 | 不可直接获取 |

#### ⚠️ 搜索API（Kimi）超时说明
- 已配搜索提供者为Kimi（kimi-k2.6），搜索请求超时率较高（35秒+）
- **不是代理问题**（FRED/MIT API都能通）
- 超时后替代方案：（1）缩短查询关键词 （2）用web_fetch直扒URL （3）依赖已知知识库（标注清楚）

### FRED API（美国经济数据）🟢 已接入
- **API key**：FRED_KEY_REDACTED
- **可用数据**：CPI、GDP、非农就业、联邦基金利率、M2、10Y国债收益率、失业率……全部官方原始JSON
- **调用示例**：`https://api.stlouisfed.org/fred/series/observations?series_id=GDP&api_key=KEY&file_type=json`

### ❌ 不可靠（搜索幻觉高发，禁止用于数据结论）
- 搜索提供基金持仓数字（如"Direxion 3x 11.02%"为虚构）
- 所有依赖搜索摘要的数字型投资数据

**铁律**：基金持仓、股价、行情数据 → 直接扒API或页面。搜索只做线索查找，不做数据结论。

### 📏 长文本截断自动拆分
- 任何单次输出如果因长度限制被截断，**自动拆分为连续的多部分发送**（如PART 1 / PART 2）
- 每部分末尾标注「本篇到齐，下篇接着出」

---

## Related

- [Agent workspace](/concepts/agent-workspace)
