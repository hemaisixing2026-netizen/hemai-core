#!/bin/bash
# Key validation script
CONFIG="/root/.hermes/config.yaml"
OPENCLAW_KEY=$(cat /mnt/g/openclaw-workspace/temp_deepseek_key.txt 2>/dev/null)

# Get key from config
HERMES_KEY=$(grep "api_key: sk-" "$CONFIG" | head -1 | sed 's/.*api_key: //' | tr -d ' ')

echo "=== Key comparison ==="
echo "Hermes key length: ${#HERMES_KEY}"
echo "Hermes key start: ${HERMES_KEY:0:15}"
echo "Hermes key end: ${HERMES_KEY: -5}"

# Test with this key
echo ""
echo "=== Testing Hermes key ==="
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $HERMES_KEY" --connect-timeout 10)
echo "HTTP: $HTTP_CODE"

# Also test with key from OpenClaw config
if [ -n "$OPENCLAW_KEY" ]; then
    echo ""
    echo "=== Testing OpenClaw key ==="
    HTTP_CODE2=$(curl -s -o /dev/null -w "%{http_code}" https://api.deepseek.com/v1/models \
      -H "Authorization: Bearer $OPENCLAW_KEY" --connect-timeout 10)
    echo "HTTP: $HTTP_CODE2"
fi
