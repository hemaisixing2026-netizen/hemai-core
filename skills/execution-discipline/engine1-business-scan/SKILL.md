---
name: engine1-business-scan
description: "引擎1·业务线全扫——8条业务线并行扫描，标记状态(✅/⚠️/🔴/⏳)，交叉编织，输出报告。用于cron定时触发或沉默挖矿手动启动。"
category: execution-discipline
metadata:
  hermes:
    tags: [cron, business-scan, engine1, 业务线, 全扫]
    also_see: [execution-discipline, fund-analysis, market-monitoring]
---

# 引擎1 · 业务线全扫

## 触发条件

- Cron定时：每天10:00/14:00/16:00自动触发
- 手动：老刘沉默>15分钟 → 引擎1挖矿启动
- 手动：老刘说"扫一下""业务线""状态"等关键词

## 8条业务线检查清单

每条标注状态：✅正常 / ⚠️关注 / 🔴需处理 / ⏳等待

### 1. 🛒 SquishyBean TK美区

| 检查项 | 数据源 | 方法 |
|:--|:--|:--|
| 棉绳到货 | 快递100官网浏览器查询 + MEMORY.md | ①浏览器导航kuaidi100.com → ②输入单号搜索（让网站自动识别快递公司） → ③提取追踪结果。**不要用API `type=` 参数指定快递公司——YT前缀会被错误匹配到其他快递公司，返回完全错误的包裹数据。** |
| 视频数据 | `data/tk-video-tracker.md` + MEMORY.md | read_file查最新播放/赞/互动率·**必须对比上次扫描算变化·无基线=建基线** |
| 6/20解禁倒计时 | 计算 | 当天日期→6/20天数 |

### 2. 📱 TK新号

- 派对眼镜视频是否已发？（无法程序化验证——需老刘反馈）
- 模板状态：party-glasses-video-test.md

### 3. 🏪 希音双店

- ⚠️ 信息盲区——希音后台需登录，无法程序化获取出单/发货数据
- 只能标记⏳等待老刘反馈

### 4. 🏗️ TK全托管

| 检查项 | 数据源 |
|:--|:--|
| 五金SKC | LEARNING.md |
| 五金广告 | LEARNING.md |
| 五金入仓 | LEARNING.md |
| 家居百货新SKC | LEARNING.md + session_search |
| 派对眼镜全托管 | party-glasses-video-test.md |

### 5. 💰 QDII投资

| 检查项 | 数据源 | 方法 |
|:--|:--|:--|
| 定投扣款 | MEMORY.md / cash-ledger.md | read_file确认 |
| 净值估算 | 天天基金API | `curl -s "https://fundgz.1234567.com.cn/js/{code}.js"` |
| 限额 | fund-analysis SKILL.md | 对照限额表 |
| 净值交叉校验 | NASDAQ API + 季报权重 | 个股跌>5%→算理论贡献→对比净值 |

**净值交叉校验触发条件：** COHR/CIEN/LITE/AVGO/NVDA 任一个股单日波动>5%

```bash
# 并行拉取重仓股行情（NASDAQ API直连，无需代理）
python3 -c "
import json, urllib.request
for sym,ac in [('NVDA','stocks'),('AVGO','stocks'),('CIEN','stocks'),
               ('COHR','stocks'),('LITE','stocks'),('MU','stocks'),
               ('TSM','stocks'),('SMH','etf'),('QQQ','etf')]:
    url=f'https://api.nasdaq.com/api/quote/{sym}/info?assetclass={ac}'
    req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
    d=json.loads(urllib.request.urlopen(req,timeout=8).read())
    p=d['data']['primaryData']
    chg=float(str(p.get('percentageChange','0')).replace('%',''))
    flag='🔴' if abs(chg)>5 else ''
    print(f'{flag} {sym:6s} {p[\"lastSalePrice\"]:>10s}  {chg:+.2f}%')
"
```

### 6. 🏭 工业富联 601138

| 检查项 | 数据源 | 方法 |
|:--|:--|:--|
| 收盘价 | 东方财富push2 API | `secid=1.601138&fields=f43,f44,f45,f46,f47,f48,f60,f162,f170` |
| A股三大指数 | 新浪财经 | `hq.sinajs.cn/list=s_sh000001,s_sz399001,s_sz399006`（备用） |
| 触发阈值 | -5% / 反弹+2% | 超过→🔴标记 |

> ⚠️ 东方财富API偶发限流，失败时用新浪财经备源。A股15:00收盘，14:00前数据为盘中。

### 7. 🔧 工业品

- 朋友回复状态：MEMORY.md + session_search
- 通常标记⏳等待

### 8. 💵 现金流

| 检查项 | 数据源 |
|:--|:--|
| 白条/美团还款 | cash-ledger.md（"待支出"→未确认） |
| 大额支出 | cash-ledger.md 出入账表 |
| 定投扣款 | MEMORY.md |
| 工资到账 | cash-ledger.md |

### 9. ⭐ 北极星 · SquishyBean $500 GMV（6/15新增·不可跳过）

| 指标 | 当前 | 目标 | 复审 |
|:--|:--|:--|:--|
| SKU上线数 | 0 | ≥10 | 2026.9.30 |
| 累计GMV | $0 | $500 | 2026.9.30 |
| 最近节点 | 6/20棉绳解禁·第一个SKU | — | — |

> 北极星追踪写入每次引擎1扫描。GMV=0时要诚实写0，不做虚假进展。
> 6/15老刘纠正：引擎1忘了北极星。从此每扫必含。

## 推送铁律（6/15新增）

- 扫描完成后→**必须推微信给老刘**。不推=他没看到=白扫
- 推送节奏：老刘在电脑前08:00-17:00 → 每2小时推一次（10/12/14/16/17点）
- 推送内容：总览表+关键变化。不超过5条。深视界14:00单独推

### 总览表（必须）
```
| # | 业务线 | 状态 | 关键信号 |
```

### 🔴项展开
- 数据 + 来源 + 判断 + 方案

### 交叉编织（必须）
- 至少一条跨线关联
- 如果回复只涉及单线→结尾标「⚠️单线」

### 三个立即动作
- 谁做/做什么/耗时

## 写入路径

`/root/workspace/data/engine1-scan-latest.md`（覆盖）

## Pitfalls

- **TK视频数据必须对比前次扫描（2026-06-12·新发现）。** 老号视频分析时只报了当前7条视频的绝对数据，没有对比前一次引擎1扫描的汇总数字（总播放2,010→2,264 +12.6%、总赞121→153 +26.4%）。老刘纠正：「你的视频数据没和前一天做对比思行」。每次报告视频数据→必须同轮读 `data/tk-video-tracker.md` 基线→算变化→标注趋势方向。第一次无基线=建基线+声明「下次可对比」。数据帧放在 `data/tk-video-tracker.md`（逐条+汇总双表），引擎1的SquishyBean检查项新增「读tk-video-tracker.md→对比变化」。
- **希音/TK后台盲区。** 这两个平台需要登录凭证，无法通过API程序化获取。直接标记⏳等待，不做虚假判断。老刘上线后主动追问。
- **Yahoo Finance chart API 数据延迟。** 非交易时段可能返回空数据。优先用NASDAQ API（直连、实时、稳定）。Yahoo Finance仅用于需要历史OHLCV序列时。
- **东方财富API限流。** push2接口偶发拒绝连接。备选：新浪财经 `hq.sinajs.cn`（格式不同，需解析GBK编码的var字符串）。
- **净值交叉校验勿跳过。** 看到重仓股>5%波动→必须算理论净值贡献→对比实际净值。只报价格不交叉校验=漏掉核心判断。
- **资金台账"待支出"≠"已还"。** 确认还款需老刘口头确认或银行扣款记录。未确认前标记⚠️关注。
- **30天规则冻结期间。** 不新增/修改执行层规则。但数据层（状态报告/扫描记录）正常更新。
- **Cron模式下信息盲区处理。** 无法访问TK/希音后台时，标记⏳等待+列出下次上线追问项，不自造数据。
- **编织要求。** 每次扫描必须做跨线关联。三条线同向→标注。孤立事件→标注「⚠️单线」。
- **🔴 kuaidi100 API carrier误匹配（2026-06-11确认）。** `type=yuntong`或`type=yuantong`参数查询YT前缀单号时，API可能错误匹配到其他快递公司的单号，返回完全错误的追踪数据（实测：同一天同一单号在不同carrier参数下返回了新疆石河子/江西上饶/义乌/河南洛阳/美国新泽西等5个不同包裹的数据）。**唯一可靠方式：浏览器导航kuaidi100.com → 输入单号让网站自动识别快递公司 → 读取结果。** 不依赖API `type=` 参数做快递公司指定。
