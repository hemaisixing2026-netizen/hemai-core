# API Key 传输截断 · 根因与解决方案

> 6/13 实战发现：长API Key（>150字符）在Hermes工具链中多次被截断。

## 问题模式

1. **write_file 截断**：写入长Key到.env文件时，工具调用参数被截断。写入后文件仅30-180字节，实际Key 170+字符。
2. **terminal heredoc 截断**：Shell heredoc（`cat << 'EOF'`）中Key字符破坏语法。
3. **Python inline 截断**：`python3 -c` 单行命令中长Key破坏引号配对。

## 根因

Key中包含 `_`、`-`、`T3BlbkFJ` 等字符，与工具JSON序列化、Shell转义、Python字符串解析发生冲突。

## 解决方案：Base64 编码中转

**流程：**
1. 物理代理在 `base64encode.org` 将Key编码
2. Base64字符串通过对话发送（纯字母数字，无特殊字符）
3. 思行用 `base64 -d` 解码写入文件

**命令：**
```bash
echo "ENCODED_STRING" | base64 -d > /path/to/key.env
```

**验证：** 先测 `/v1/models`（无配额消耗），确认Key有效再测 `/v1/chat/completions`。

## 中转API接入模式

```json
{"_type":"newapi_channel_conn","key":"sk-xxx","url":"https://maimai.it.com"}
```

- 转发地址 = url
- API Key = key  
- 模型端点 = `{url}/v1/models`
- 聊天端点 = `{url}/v1/chat/completions`
- 认证头 = `Authorization: Bearer {key}`
