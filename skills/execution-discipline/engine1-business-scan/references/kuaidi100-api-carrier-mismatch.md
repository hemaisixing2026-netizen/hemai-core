# kuaidi100 API Carrier Mismatch — YT Prefix Case Study

> 日期：2026-06-11
> 追踪号：YT7626458261729（正确快递公司：圆通速递）

## 问题

kuaidi100 API 在查询 YT 前缀单号时，`type` 参数指定的快递公司可能导致 API 返回**完全不相关的其他包裹**的追踪数据。

## 实测记录（2026-06-11，同一单号 YT7626458261729）

| `type=` 参数 | API 返回的包裹轨迹 |
|:--|:--|
| `yuantong` | "查无结果"（2026-06-06） |
| `yuntong` (desktop UA) | 安能物流·洛阳揽收（2026-06-10） |
| `yuntong` (mobile UA) | 中国邮政国际件·合肥→美国新泽西（2026-06-02~10） |
| `jd` | 跨越速运·佛山签收（2026-06-10） |
| `zhongtong` | 德邦·武汉签收（2024-07-18） |

**6/10早期查询还出现过：** 圆通·新疆石河子签收、圆通·江西上饶签收、圆通·义乌转运中心——均非真实路由。

## 正确结果（浏览器直查）

浏览器导航 kuaidi100.com → 输入单号 → 网站自动识别为**圆通速递** → 返回正确轨迹：

```
2026-06-11 07:34  杭州·余杭区良渚新城  派件中（王新旭 15888840070）
2026-06-11 04:04  杭州·余杭区良渚新城  已到达网点
2026-06-11 03:59  杭州·紫金港城市服务中心 → 良渚新城  已发出
2026-06-11 03:59  杭州·紫金港城市服务中心  已到达
```

## 根因分析

1. 快递100 API `type` 参数不是严格过滤——是**建议/偏好**。当指定 `type=yuntong` 时，API 可能将 YT 前缀的单号匹配到韵达、安能等其他快递公司的数据库，返回同名或近似编号的包裹。
2. 快递100网站的自动识别（autoComNum）比 API `type` 参数更准确——网站有更复杂的匹配逻辑。
3. `autoComNum` API 端点有时返回 `301 非法请求`，需要正确的 Referer 和 User-Agent 头。

## 正确做法

```
1. browser_navigate("https://www.kuaidi100.com/")
2. browser_type(ref=e46, text="YT7626458261729")  # 搜索框
3. browser_click(ref=e7)  # "查快递"按钮
4. browser_console 提取 .track-result 或 querySelectorAll 获取追踪表格
```

**不要使用的模式：**
```bash
# ❌ API type= 指定——会返回错误包裹
curl "https://www.kuaidi100.com/query?type=yuntong&postid=YT..."
```

## autoComNum（仅做参考）

当需要先确认快递公司时，autoComNum 可用但需正确 headers：
```bash
curl -s "https://www.kuaidi100.com/autonumber/autoComNum?resultv2=1&text=YT7626458261729" \
  -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  -H "Referer: https://www.kuaidi100.com/"
```

返回的 `comCode` 可用于后续查询，但**不保证查询结果正确**——最终仍建议浏览器直查。
