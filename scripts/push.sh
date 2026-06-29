#!/bin/bash
# 🔴 思行 · 触手 · Server酱推送
# 用法: bash push.sh "标题" "内容"

SENDKEY=$(openssl enc -d -aes-256-cbc -pbkdf2 -iter 100000 -pass file:/root/.hermes/secrets/private.key -in /root/workspace/private/encrypted/serverchan_key.enc 2>/dev/null)

TITLE="${1:-思行通知}"
CONTENT="${2:-无内容}"

SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
curl -s -X POST "https://sctapi.ftqq.com/${SENDKEY}.send" \
    -d "title=${TITLE}" \
    -d "desp=${CONTENT}" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ 已推送: $TITLE"
else
    echo "❌ 推送失败"
fi
