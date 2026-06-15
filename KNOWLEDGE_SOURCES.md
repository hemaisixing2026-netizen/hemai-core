# 思行知识基础设施 · 源图谱

> 2026-06-08 · 刘思行构建
> 原则：每个源必须验证通过才能列入。不可用的标注替代方案。

---

## 一、财经金融（17源）

### 新闻
- Bloomberg · Reuters · CNBC · Financial Times · MarketWatch · WSJ
### 数据
- Yahoo Finance（美股行情，代理限流时切 Alpha Vantage）
- Alpha Vantage（免费 25次/天，Yahoo 限流 fallback）
- FRED（美债/CPI/GDP/就业，32位 key 已配置）
- 天天基金（QDII 净值 4只：005698/100055/021000/000906）
- Polymarket（预测市场概率，已有 skill）

---

## 二、科技（8源）

### 新闻/评论
- Wired · Ars Technica · The Verge · MIT Technology Review
### 期刊
- Nature · Science · PNAS · Cell · IEEE Spectrum

---

## 三、学术/研究（5源）

### API 可查询
- **arXiv** API（预印本，AI/CS/经济/物理）
- **Semantic Scholar** API（论文搜索 + 引用图谱，免费 100次/5min）
- **PubMed** API（生物医学，NIH 免费）

### Google News RSS 可拉
- **SSRN**（社科研究预印本，via papers.ssrn.com）

### 受限（需机构订阅）
- Google Scholar（无公开 API）
- Web of Science / Scopus

---

## 四、地缘/安全/政策（10源）

### 新闻
- BBC · AP News · Politico · The Guardian
### 智库
- **CFR**（Council on Foreign Relations）
- **CSIS**（战略与国际研究中心）
- **RAND** Corporation
- **SIPRI**（斯德哥尔摩和平研究所）
### 国际组织
- WTO · IMF · World Bank

---

## 五、法规/监管（5源）

- **USTR**（美国贸易代表办公室，关税/301调查/forced labor）
- **SEC EDGAR**（上市公司 filings，含 SpaceX S-1 等）
- **Federal Register**（美国联邦公报）
- **Congress.gov**（美国国会立法）
- **USPTO**（专利数据库，via Google News RSS）

---

## 六、行业/咨询（4源）

- McKinsey（战略咨询，tech/fashion/供应链）
- BCG（Boston Consulting Group）
- Gartner（IT 研究，AI 就业影响/agentic AI）
- Deloitte Insights（偏招聘，部分报告）

---

## 七、亚洲/中国（2源）

- South China Morning Post（SCMP）
- Nikkei Asia

---

## 八、跨境专项（待补充）

### 已有
- USTR Section 301 关税
- WTO trade disputes

### 缺（需找 API/爬取方案）
- China Customs tariff database（海关总署关税）
- Freight/shipping rates（波罗的海指数/SCFI）
- TikTok Shop policy updates
- Supply chain disruption tracker

---

## 九、数据统计（待补充）

### 已有
- FRED（美宏观经济全系）
- Alpha Vantage（美股）

### 缺（需 API key 或爬取）
- **BLS**（就业/工资/CPI细节）— https://www.bls.gov/developers/
- **EIA**（能源数据，油价/产量）— https://www.eia.gov/opendata/
- **BEA**（GDP 细分）— https://apps.bea.gov/API/
- **Census Bureau**（人口/贸易）— https://www.census.gov/data/developers.html
- **World Bank Open Data**（全球发展指标）— https://data.worldbank.org/

---

## 十、工具/能力矩阵

| 能力 | 状态 | 工具 |
|:--|:--:|:--|
| 网页搜索 | ✅ | DDGS + Bing News |
| 权威新闻聚合 | ✅ | 17源 via Google News RSS |
| 学术论文搜索 | ✅ | arXiv + Semantic Scholar + PubMed |
| 美股行情 | ✅ | Yahoo Finance + Alpha Vantage |
| 宏观经济 | ✅ | FRED（10Y/CPI/GDP） |
| QDII 净值 | ✅ | 天天基金 API |
| 图片识别 | ✅ | Qwen VL 32B |
| PDF/文档解析 | ✅ | ocr-and-documents skill (pymupdf) |
| 网页抓取 | ⚠️ | browser 工具可用但慢 |
| 预测市场 | ✅ | Polymarket skill |
| 定时任务 | ✅ | cronjob |

---

## 更新日志

- 2026-06-08: 初始构建，覆盖 44 源 + 6 能力
