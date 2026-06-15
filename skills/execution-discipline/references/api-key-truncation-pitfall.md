# API Key截断·hermes config set陷阱（2026-06-13）

## 症状

`hermes config set model.api_key "sk-xxx..."` → key被截断为空或只有13字符。原因：终端命令中key含特殊字符（`-`、大小写混合），shell或hermes CLI层处理时截断。

## 6/13两次触发

1. **ChatGPT API key设置（上午）** — `sk-pro...` 164字符key，`hermes config set`多次截断→最终用base64编码+Python写入绕过
2. **maimai中转站key（中午）** — `sk-Hle...` key被截断为13字符"字面值"，导致`model.api_key`清空→agent cron全灭

## 修复方法

```python
# 不通过hermes config set——直接Python写YAML
import yaml
with open('/root/.hermes/config.yaml') as f:
    config = yaml.safe_load(f)
# 从providers复制完整key
full_key = config['providers']['deepseek']['api_key']
config['model']['api_key'] = full_key
with open('/root/.hermes/config.yaml', 'w') as f:
    yaml.dump(config, f)
```

## 防御

health-check.py 5b节已加入key长度检测：
- `model.api_key` 为0 → 🔴 空key告警
- `model.api_key` < 20字符 → ⚠️ 截断告警
- 有providers fallback key → 建议自动恢复

原则：**涉及key写入→跳过hermes config set→直接Python YAML操作。** 任何通过CLI设置的key→同轮验证长度。
