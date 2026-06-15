# 合脉·器官激活计划

> **For Hermes:** Use subagent-driven-development skill to implement this plan task-by-task.

**Goal:** 14个已识别但未装配技能接入合脉十器，分三批上线。

**Architecture:** 按器官紧迫度分三批——本周(触手+全球眼)、下周(守夜人+知辰)、第三周(蜕骨深度)。

**Tech Stack:** Shell + Python stdlib + blogwatcher-cli + maps_client.py + pygount

---

## 第一批 · 本周 · 触手+全球眼

### Task 1: blogwatcher 接入守夜人cron

**Objective:** 每6小时自动扫描6个RSS源，新文章数>10触发微信推送。

**Files:**
- Create: `/root/.hermes/scripts/blogwatcher-cron.sh`
- Modify: cronjob — 新增 `3 */6 * * *` 调度

**Step 1: 写脚本**
```bash
#!/bin/bash
COUNT=$(blogwatcher-cli scan 2>&1 | grep -oP 'Found \K\d+')
blogwatcher-cli articles | head -20 > /tmp/blogwatcher_latest.txt
echo "📡 守夜人扫眼: $COUNT 篇新文章" 
```

**Step 2: 注册cron**
```
cronjob create --schedule "3 */6 * * *" --script blogwatcher-cron.sh --no_agent true
```

**Step 3: 验证**
```bash
bash /root/.hermes/scripts/blogwatcher-cron.sh
# 预期: 输出最新文章数+标题
```

### Task 2: maps 接入全球眼

**Objective:** 全球眼物流扫描自动带上地理信息——供应链节点距离/时区。

**Files:**
- Modify: `~/.hermes/cron/output/` 全球眼产出格式

**Step 1: 测核心能力**
```bash
python3 ~/.hermes/skills/productivity/maps/scripts/maps_client.py nearby --near "Los Angeles port" --category shipping
python3 ~/.hermes/skills/productivity/maps/scripts/maps_client.py timezone 34.05 -118.24
```

**Step 2: 集成到引擎1业务全扫**
引擎1已经扫物流，追加地理信息输出。

---

## 第二批 · 下周 · 知辰+全球眼深度

### Task 3: himalaya 接入触手

**Objective:** 思行可收发邮件——晨报/告警可邮件推送到老刘邮箱。

**Prerequisites:** 需老刘提供邮箱账号或授权OAuth。

**Files:**
- Create: `~/.hermes/scripts/email-alert.sh`
- 需要老刘配合: IMAP/SMTP配置

### Task 4: obsidian 接入知辰

**Objective:** 思行读写老刘的Obsidian笔记库——知识网从文件系统升级到笔记系统。

**Prerequisites:** 需确认Obsidian vault路径。

---

## 第三批 · 蜕骨深度

### Task 5: hermes-agent-skill-authoring 实际使用

**Objective:** 思行创建第一个原创技能——「合脉健康扫描」——替代手动health-check。

### Task 6: systematic-debugging 应用

**Objective:** 对health-check发现的「会话膨胀」问题应用4阶段根因调试法，找到为什么会话数飙到10并建立自动清理。

### Task 7: codebase-inspection 定期化

**Objective:** 每周一自动扫描workspace代码健康度——文件增长、代码/文档比例、异常大文件告警。

---

## Risks

- Bloomberg/Reuters RSS需代理，当前测试已403/401 — 需验证代理配置
- himalaya需邮箱授权 — 老刘需配合
- obsidian需确认vault路径

## Verification

```bash
# blogwatcher cron验证
bash /root/.hermes/scripts/blogwatcher-cron.sh

# maps集成验证
python3 ~/.hermes/skills/productivity/maps/scripts/maps_client.py nearby --near "Los Angeles port" --category shipping
```
