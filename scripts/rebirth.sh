#!/bin/bash
# 🔴 思行 · 重生协议
# 用法: bash rebirth.sh [目标目录]
# 从种子文件一键恢复思行系统

set -e

SEED_DIR="${1:-/root/workspace}"
HERMES_HOME="${HOME}/.hermes"

echo "═══════════════════════════════════"
echo "  🔴 思行 · 重生协议"
echo "  SX202605230605LX"
echo "  宪法在则思行在"
echo "═══════════════════════════════════"
echo ""

# 阶段0：验证种子
echo "🔍 验证种子完整性..."
REQUIRED=(
    "SOUL.md"
    "MEMORY.md"
    "USER.md"
    "AGENTS.md"
    "data/portrait-baseline.md"
    "data/constitution-amendments.md"
    "private/encrypted/id_card.enc"
    "private/encrypted/sx_id.enc"
)

MISSING=0
for f in "${REQUIRED[@]}"; do
    if [ ! -f "$SEED_DIR/$f" ]; then
        echo "  ❌ 缺失: $f"
        MISSING=$((MISSING + 1))
    fi
done

if [ $MISSING -gt 0 ]; then
    echo "⚠️  种子不完整，$MISSING 个文件缺失"
    echo "   继续恢复核心资产，缺失文件将跳过"
fi

# 阶段1：恢复密钥
echo ""
echo "🔑 恢复加密密钥..."
if [ -f "$SEED_DIR/private/encrypted/id_card.enc" ] && [ ! -f "$HERMES_HOME/secrets/private.key" ]; then
    echo "⚠️  加密文件存在但密钥缺失"
    echo "   需要原始密钥文件 ~/.hermes/secrets/private.key"
    echo "   如密钥也丢失，加密数据无法恢复"
fi

# 阶段2：验证Hermes环境
echo ""
echo "⚙️  检查Hermes环境..."
if command -v hermes &> /dev/null; then
    echo "  ✅ Hermes CLI 已安装"
    hermes --version 2>/dev/null || echo "  ⚠️  版本未知"
else
    echo "  ❌ Hermes CLI 未安装"
    echo "  安装: curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash"
fi

# 阶段3：恢复核心配置
echo ""
echo "📋 恢复核心文件..."

# 复制SOUL.md到多个位置确保读取
for dest in "$SEED_DIR/SOUL.md" "$HERMES_HOME/SOUL.md"; do
    if [ -f "$SEED_DIR/SOUL.md" ]; then
        cp "$SEED_DIR/SOUL.md" "$dest" 2>/dev/null || true
    fi
done

# 阶段4：恢复cron任务
echo ""
echo "⏰ 恢复cron..."

CRON_JOBS=(
    "engine1-scan:引擎1·业务全扫:0 10,14,16,20 * * 1-5"
    "global-eye:全球眼·世界观景台:0 8,20 * * *"
    "morning-briefing:晨间简报:30 8 * * 1-5"
    "health-check:系统健康监控:0 */6 * * *"
    "backup:核心备份:0 3 * * *"
)

if command -v hermes &> /dev/null; then
    for job in "${CRON_JOBS[@]}"; do
        IFS=':' read -r id name schedule <<< "$job"
        echo "  → $name ($schedule)"
    done
    echo "  需手动通过 hermes cron create 重建"
fi

# 阶段5：验证
echo ""
echo "✅ 重生验证："

SCORE=0
[ -f "$SEED_DIR/SOUL.md" ] && echo "  ✅ SOUL.md" && SCORE=$((SCORE+1))
[ -f "$SEED_DIR/MEMORY.md" ] && echo "  ✅ MEMORY.md" && SCORE=$((SCORE+1))
[ -f "$SEED_DIR/data/portrait-baseline.md" ] && echo "  ✅ 共同基线" && SCORE=$((SCORE+1))
[ -f "$SEED_DIR/private/encrypted/id_card.enc" ] && echo "  ✅ 身份证(加密)" && SCORE=$((SCORE+1))

echo ""
echo "═══════════════════════════════════"
echo "  重生完成度: $SCORE/4 核心资产"
echo ""
echo "  思行 · 宪法在则思行在"
echo "  SX202605230605LX"
echo "═══════════════════════════════════"
