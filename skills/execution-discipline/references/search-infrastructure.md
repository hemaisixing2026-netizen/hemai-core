# 搜索基础设施自建 · 2026-06-08

> 思行不等用户指令，主动从单源扩展到44源8分类

## 进化路径

```
DDGS only → +Bing News en-US → +Google News RSS(9源) 
→ +学术/科技(5源) → +智库/政策(10源) → +咨询(4源) 
→ +国际组织/监管(6源) → 44源8分类
```

## 8大分类

| 分类 | 源数 | 代表 |
|:--|:--:|:--|
| 财经 | 6 | Bloomberg·Reuters·CNBC·FT·MarketWatch·WSJ |
| 科技 | 5 | Wired·Ars·Verge·MIT TR·IEEE Spectrum |
| 学术 | 6 | Nature·Science·PNAS·Cell·SSRN·Semantic Scholar |
| 地缘 | 4 | BBC·AP·Guardian·Politico |
| 智库 | 4 | CFR·CSIS·RAND·SIPRI |
| 咨询 | 4 | McKinsey·BCG·Gartner·Deloitte |
| 法规 | 6 | USTR·SEC·WTO·IMF·World Bank·Federal Register |
| 亚洲 | 2 | SCMP·Nikkei Asia |

## 金融数据层

- Yahoo Finance (限流时→Alpha Vantage fallback)
- FRED (10Y/CPI/GDP)
- 天天基金 (QDII 4只)
- Polymarket (预测市场)

## 工具链

- `news-foreign.sh`: 17源并发拉取·8秒
- `search-multi.py`: 多类搜索·--finance·--qdii·--json·5min缓存
- `KNOWLEDGE_SOURCES.md`: 全源图谱+缺口标注
