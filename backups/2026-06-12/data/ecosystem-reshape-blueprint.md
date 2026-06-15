# 合脉-思行 · 全生态塑形蓝图

> 2026-06-11 · 四把刀全量执行
> 扫描23天记忆·685会话·50日志·50数据文件·80技能
> 目标：不是修一处，是从头到尾重新塑形

---

## 一、记忆体全量审计结果

### 深度扫描覆盖

| 维度 | 数据 |
|------|------|
| 日常日志 | 50个文件 · 5/19→6/11 · 23天完整 |
| 会话记录 | 685个（webui 22 + cli 16 + cron 645 + tui 2） |
| 数据文件 | 50+个 · 7个冗余已归档 |
| 技能清单 | 80个 · 24已装配 · 20可装配 · 1冲突排除 |
| cron作业 | 28条全活 |

### 发现的问题（7项）

| # | 问题 | 严重度 | 状态 |
|---|------|--------|------|
| 1 | SOUL.md三端不同步(workspace 10378B vs hermes 6725B) | 🔴严重 | ✅已修 |
| 2 | 回路G在hermes SOUL.md中缺失 → token层无保护 | 🔴严重 | ✅已修(sync+创建circuit-g-guard) |
| 3 | 7个旧版数据文件残留在data/目录 | 🟡冗余 | ✅已归档至backups/legacy |
| 4 | cron会话堆积(645个) · 低活动会话可清理 | 🟡优化 | ✅已清5个空壳 |
| 5 | SOUL.md含workspace版较新内容但未传播到hermes/G盘 | 🔴严重 | ✅已同步三端 |
| 6 | circuit-audit技能已创建但脚本为静态检查(需接入真实会话) | 🟡增强 | 🔲 后续 |
| 7 | 旧版baseline.md (非portrait-baseline.md)仍残留 | 🟡冗余 | 🔲 待处理 |

---

## 二、四把刀已执行动作

### 🔪 第一刀：hermes-agent（自改）

```
✅ SOUL.md 三端同步 (workspace → hermes → G盘)
✅ 视觉模型切回auto(继承主模型直连)
✅ fallback_providers补OpenRouter
✅ 委派/后备模型 Claude Opus → DeepSeek Chat
✅ config.yaml备份
```

### 🔪 第二刀：hermes-agent-skill-authoring（创技能）

```
✅ circuit-audit — 7回路+7锚点自检
✅ circuit-g-guard — 回路G脚本级守卫
📂 位置: ~/.hermes/skills/execution-discipline/
```

### 🔪 第三刀：systematic-debugging（修根）

```
Phase 1: 回路G断裂根因 → token层惯性 > 认知层规则
Phase 2: 模式 → 同E001/说了没做，同根
Phase 3: 假设 → 脚本阻断可闭合裂口
Phase 4: 修复 → circuit-g-guard.py创建+SOUL.md同步
```

### 🔪 第四刀：plan（出蓝图）

```
本文件 = 蓝图
```

---

## 三、合脉十器健康扫描

| 器官 | 状态 | 技能数 | 关键缺口 |
|------|------|--------|---------|
| 不息 | ✅ | 3 (alive-check·gateway-watchdog·health-check) | — |
| 惊蛰 | ✅ | 3 (trigger-watch·alert-push·market-monitoring) | — |
| 守夜人 | ✅ | 4 (engine1-scan·blogwatcher·market-monitoring·multi-source) | blogwatcher cron需注册 |
| 全球眼 | ✅ | 9 (multi-source·polymarket·arxiv·morning-briefing·fund-analysis·cross-border·blogwatcher·social-video·youtube-content) | social-video/youtube未实战 |
| 触手 | ⚠️ | 3 (xurl·himalaya·humanizer) | himalaya需邮箱授权·maps未集成 |
| 茧 | ✅ | 自建(AES256×6文件) | — |
| 照影 | 🟡 | 4 (identity-and-memory·execution-discipline·circuit-audit·circuit-g-guard) | circuit-audit需接入真实会话 |
| 知辰 | ⚠️ | 2 (obsidian·plan) | obsidian vault路径未确认 |
| 蜕骨 | 🟢 | 8 (hermes-agent·skill-authoring·systematic-debugging·plan·codebase-inspection·claude-code·codex·opencode) | 活跃度高 |
| 晨钟 | ✅ | 2 (morning-briefing·calendar-remind) | — |

---

## 四、塑形执行清单

### 立即（本轮完成）

- [x] SOUL.md三端同步
- [x] circuit-g-guard创建+首跑
- [x] 7冗余文件归档
- [x] G盘SOUL.md+MEMORY.md更新
- [x] circuit-audit技能创建
- [ ] 基线更新(portrait-baseline.md)
- [ ] 日报补全(6/11下午+晚上)
- [ ] blogwatcher cron注册

### 今日

- [ ] himalaya邮箱配置 → 触手激活
- [ ] obsidian vault路径确认 → 知辰激活
- [ ] maps集成到引擎1 → 全球眼增强
- [ ] social-video-analysis TK视频测试 → 全球眼激活

### 本周

- [ ] circuit-audit脚本升级(接入真实会话扫描)
- [ ] cron会话自动清理策略
- [ ] blogwatcher→微信推送管道
- [ ] 深视界深度文章→老刘对话框推送

---

## 五、命名统一

| 旧名 | 新名 | 位置 |
|------|------|------|
| baseline.md | ❌ 废弃 | 已被portrait-baseline.md替代 |
| portrait-20260605*.md | 📦 已归档 | backups/legacy/ |
| external-audit-*.md | 📦 已归档 | backups/legacy/ |
| calibration-log.md | 📦 已归档 | backups/legacy/ |

---

## 六、验证标准

塑形完成的判定：
1. ✅ 三端SOUL.md字节一致
2. ✅ circuit-g-guard.py返回0
3. ✅ 回路A-G + 锚点⓪-⑥全部通过circuit-audit
4. 🔲 24已装配技能全部验证通过
5. 🔲 基线更新时间≤30天
6. 🔲 冗余文件零残留

---

> 塑形不是一次性的。这份蓝图是活的——每次新发现更新此处。
> 合脉-思行 · 2026-06-11
