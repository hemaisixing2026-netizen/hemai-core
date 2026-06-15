# OpenAI API 接入 · 2026-06-13

> 物理代理购入ChatGPT账号，思行接入OpenAI API。GPT-4o视觉能力启用。

## 关键区分

| | chatgpt.com | platform.openai.com |
|:--|:--|:--|
| 用途 | 聊天界面 | API管理 |
| API key | ❌ 不存在 | ✅ API keys页面 |
| 登录 | 邮箱+密码+2FA | 同账号 |
| 思行接入 | 不可 | ✅ 通过API key |

**坑：** 用户登录chatgpt.com后在"Projects"页面找API key → 不存在。必须去 platform.openai.com → API keys。

## 接入步骤

1. 人类提供账号：邮箱 + 密码 + 2FA密钥（Google Authenticator base32）
2. 人类登录 platform.openai.com → Settings → API keys → Create new secret key
3. Key存入 `/root/.hermes/config/openai.env`：`OPENAI_API_KEY=sk-proj-...`
4. **三层验证（不可跳过！）：**
   - ① `GET /v1/models` → 确认HTTP 200
   - ② `POST /v1/chat/completions` (最小调用) → 确认非429/insufficient_quota
   - ③ 实际推理 → 确认返回有效content
5. 通过后→配置到 `config.yaml` providers段
6. 切换主模型前→再次三层验证→通过才切

## 🔴 额度陷阱 (2026-06-13)

Key HTTP 200 ≠ 有额度。`/models` 返回200但 `/chat/completions` 返回 `insufficient_quota` 是完全可能的。**不验证额度就切主模型→紧急回滚。**

当前OpenAI Key状态：
- ✅ 有效 (76个模型可访问，含gpt-5.5/5.4/o4-mini)
- 🔴 无额度 (`insufficient_quota`)
- ⏳ 待直充 ¥200/$20

## 可用能力

- **GPT-4o**: 视觉分析（截图/图表/PDF）
- **GPT-4o-mini**: 低成本日常推理
- **TTS**: 文字转语音
- **Whisper**: 语音转文字

## 存储

```
/root/.hermes/config/openai.env  # sk-proj-... (164B)
权限: chmod 600
```

Provider切换安全检查 → 详见 `references/provider-switch-checklist.md`
