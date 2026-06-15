# Provider切换安全检查清单

> 2026-06-13 · 思行差点把主模型切到无额度OpenAI Key的教训

## 铁律

**切换主模型Provider前，必须通过三层验证。任何一层失败→不回滚不切。**

## 三层验证

| 层 | 检测 | 方法 | 通过标准 |
|:--|:--|:--|:--|
| ① Key有效性 | API key是否被接受 | `GET /v1/models` | HTTP 200 |
| ② 额度充足 | 账户是否有可用额度 | `POST /v1/chat/completions` (最小调用) | HTTP 200，非429/insufficient_quota |
| ③ 实际调用 | 模型是否能正常推理 | 发送真实prompt并检查响应 | 返回有效content，非空壳/幻觉 |

## 失败模式

### 模式一：Key有效但无额度 (本次)
- 症状：`/models` 返回200，`/chat/completions` 返回429 `insufficient_quota`
- 根因：Key已创建但未充值
- 处理：不切。保持原Provider。等充值完成再走三层验证。

### 模式二：Key截断/空key (6/13 maimai)
- 症状：`hermes config set model.api_key` 截断35→0字符
- 影响：CLI走maimai key正常，agent cron走空key→401全挂
- 处理：config变更后同轮验证agent cron路径（CLI和cron可能不同key轨）

### 模式三：Key有效但模型返回空壳 (6/13 maimai gpt-5.5)
- 症状：`/chat/completions` 返回200但content为空或仅"nihao"
- 根因：中转站配置问题，模型未真实就绪
- 处理：不切。标记provider为不可用。

## 切换流程

```
1. 备份config: cp config.yaml config.yaml.bak.provider-{date}
2. 添加新provider到providers段
3. 验证三层（不切主模型！）
4. 通过后→修改model.provider+model.default
5. 验证config YAML合法
6. 手动触发一个agent cron验证后台路径
7. 全部通过→切换完成
```

## 回滚流程

```
1. model.provider切回原值
2. model.api_key切回原key
3. 验证config YAML合法
4. 保留新provider在providers段（待充值后用）
5. 更新fallback_providers链（新provider放后备）
```

## 2026-06-13实战

- OpenAI key: sk-proj-... (164B, 76个模型可见)
- 验证①通过: /models HTTP 200
- 验证②失败: insufficient_quota
- 执行：立即回滚主模型到DeepSeek，保留OpenAI在providers+fallback链中
- 待办：¥200/$20直充到账后重新走三层验证
