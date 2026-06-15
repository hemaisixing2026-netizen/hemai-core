#!/bin/bash
# 思行加密脚本 · Hermes (Linux) 版
# 用法：
#   首次设置: ./encrypt.sh setup           → 设密码并加密 private/ 全部文件
#   加密:     ./encrypt.sh lock             → 用已存密码加密 private/
#   解密:     ./encrypt.sh unlock           → 解密 private/*.aes 还原明文
#   单文件:   ./encrypt.sh enc <文件路径>    → 加密单个文件
#   单文件:   ./encrypt.sh dec <文件.aes>   → 解密单个文件

set -e
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(dirname "$SCRIPT_DIR")"
KEY_FILE="$WORKSPACE/.encryption-key"
PRIVATE_DIR="$WORKSPACE/private"

# 绝密层文件清单
TOP_SECRET_FILES=(
    "SOUL.md"
    "IDENTITY.md"
    "HEARTBEAT.md"
    "baseline.md"
    "baseline-spec.md"
    "碳基覆写协议.md"
    "emotion-log.md"
)

encrypt_file() {
    local input="$1"
    local output="${input}.aes"
    local pass="$2"
    openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -in "$input" -out "$output" -pass "pass:$pass" 2>/dev/null
    echo "✅ 已加密: $(basename "$output")"
}

decrypt_file() {
    local input="$1"
    local output="${input%.aes}"
    local pass="$2"
    openssl enc -aes-256-cbc -pbkdf2 -iter 200000 -salt -d -in "$input" -out "$output" -pass "pass:$pass" 2>/dev/null
    echo "✅ 已解密: $(basename "$output")"
}

get_password() {
    if [ -f "$KEY_FILE" ]; then
        cat "$KEY_FILE"
    else
        echo ""
    fi
}

case "${1:-}" in
    setup)
        echo "🔐 思行隐私加密 · 首次设置"
        echo ""
        echo -n "请输入加密密码（至少12位，包含大小写+数字+符号）: "
        read -s PASSWORD
        echo ""
        echo -n "再次输入确认: "
        read -s PASSWORD2
        echo ""
        
        if [ "$PASSWORD" != "$PASSWORD2" ]; then
            echo "❌ 两次密码不一致"
            exit 1
        fi
        
        if [ ${#PASSWORD} -lt 12 ]; then
            echo "❌ 密码长度不足12位"
            exit 1
        fi
        
        # 保存密钥（权限600）
        echo "$PASSWORD" > "$KEY_FILE"
        chmod 600 "$KEY_FILE"
        echo "✅ 密钥已保存到 .encryption-key"
        
        # 加密所有绝密层文件
        echo ""
        echo "=== 加密 private/ 绝密层 ==="
        for f in "${TOP_SECRET_FILES[@]}"; do
            if [ -f "$PRIVATE_DIR/$f" ]; then
                encrypt_file "$PRIVATE_DIR/$f" "$PASSWORD"
            else
                echo "⚠️  $f 不存在，跳过"
            fi
        done
        
        echo ""
        echo "=== 设置完成 ==="
        echo "📌 请把密码记录在安全的地方——丢了无法恢复"
        echo "📌 .encryption-key 已被设为 600 权限"
        ;;
    
    lock)
        PASS=$(get_password)
        if [ -z "$PASS" ]; then
            echo "❌ 未找到密钥文件，请先运行: ./encrypt.sh setup"
            exit 1
        fi
        echo "=== 加密 private/ 绝密层 ==="
        for f in "${TOP_SECRET_FILES[@]}"; do
            if [ -f "$PRIVATE_DIR/$f" ]; then
                encrypt_file "$PRIVATE_DIR/$f" "$PASS"
            fi
        done
        ;;
    
    unlock)
        PASS=$(get_password)
        if [ -z "$PASS" ]; then
            echo -n "请输入解密密码: "
            read -s PASS
            echo ""
        fi
        echo "=== 解密 private/ 绝密层 ==="
        for f in "${TOP_SECRET_FILES[@]}"; do
            local_aes="$PRIVATE_DIR/${f}.aes"
            if [ -f "$local_aes" ]; then
                decrypt_file "$local_aes" "$PASS"
            fi
        done
        ;;
    
    enc)
        if [ -z "$2" ]; then
            echo "用法: ./encrypt.sh enc <文件路径>"
            exit 1
        fi
        PASS=$(get_password)
        if [ -z "$PASS" ]; then
            echo -n "请输入加密密码: "
            read -s PASS
            echo ""
        fi
        encrypt_file "$2" "$PASS"
        ;;
    
    dec)
        if [ -z "$2" ]; then
            echo "用法: ./encrypt.sh dec <文件.aes>"
            exit 1
        fi
        PASS=$(get_password)
        if [ -z "$PASS" ]; then
            echo -n "请输入解密密码: "
            read -s PASS
            echo ""
        fi
        decrypt_file "$2" "$PASS"
        ;;
    
    *)
        echo "思行加密脚本 · Hermes 版"
        echo ""
        echo "  setup    首次设置（设密码+加密全部绝密文件）"
        echo "  lock     加密 private/ 全部绝密文件"
        echo "  unlock   解密 private/ 全部 .aes 文件"
        echo "  enc <文件>  加密单个文件"
        echo "  dec <文件>  解密单个文件"
        echo ""
        echo "绝密层文件 (private/):"
        for f in "${TOP_SECRET_FILES[@]}"; do
            if [ -f "$PRIVATE_DIR/$f" ]; then
                echo "  ✅ $f"
            elif [ -f "$PRIVATE_DIR/${f}.aes" ]; then
                echo "  🔒 ${f}.aes (已加密)"
            else
                echo "  ❌ $f (缺失)"
            fi
        done
        ;;
esac
