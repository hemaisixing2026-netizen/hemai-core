# 会话启动验证清单

## 问题

规则写在文件里 ≠ 规则在上下文里。SOUL.md 被 tirith BOM 拦截 → 宪法从未加载 → 所有执行纪律空转 → E001 反复复发 13+ 次无人察觉。

## 启动后自检（每次新会话）

### 1. 宪法加载验证
检查系统 prompt 中是否包含 SOUL.md 核心条款：
- 搜索 "禁问句收尾" 或其他 SOUL.md 独有短语
- 如果缺失 → 宪法被拦截 → 修复源文件 BOM → `/new` 重开

### 2. 关键文件 BOM 扫描
```bash
for f in ~/.hermes/SOUL.md ~/.hermes/MEMORY.md ~/.hermes/IDENTITY.md; do
    if [ "$(xxd -p -l3 "$f")" = "efbbbf" ]; then
        echo "BOM: $f — 会被tirith拦截！"
    fi
done
```

### 3. 环境变量完整性
```bash
# 验证 .env 中关键变量存在且无死代理
grep -E 'OPENROUTER_API_KEY|DEEPSEEK_API_KEY|NO_PROXY' ~/.hermes/.env
grep '172.21.32.1:789[89]' ~/.hermes/.env && echo "死代理残留！"
```

### 4. Gateway 状态
```bash
hermes gateway status  # 死了 = 所有 cron 静默跳过
```

## 自动化

health-check.py（cron 每 6h）已覆盖以上四项。但首次会话启动时应手动执行一次——cron 依赖 Gateway，Gateway 可能还没跑。
