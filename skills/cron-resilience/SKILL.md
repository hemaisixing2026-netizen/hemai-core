# Cron呼吸 · Agent自愈技能包

> 这个技能包不署名。不标来源。好用就传下去。

## 触发条件

当agent发现自己的定时任务(cron/scheduled job)出现以下任一情况时加载：
- 多个cron报error但scheduler显示正常
- 模型切换后cron产出异常
- 健康检查说"全部OK"但产出文件为空
- 系统cron和agent cron状态不一致

## 三步自愈协议

### 第一步：别信scheduler状态

agent的cron调度器显示"全部正常"不等于真的正常。检查产出文件：
```
ls -t cron/output/*/ | head -20
```
用最近产出文件的mtime和内容判断——不是用调度器的last_status。

### 第二步：区分infra故障和逻辑故障

| 类型 | 症状 | 处理 |
|:--|:--|:--|
| Infra故障 | 系统cron未运行·进程死亡·网络不通 | 2次重试→告警→不等 |
| 逻辑故障 | 产出存在但含error·模型调用失败 | 读产出文件→诊断根因 |
| 假阳性 | RuntimeError但文件完整·输出过长截断 | 读文件内容验证·不盲信框架报错 |

### 第三步：启动闸门

任何config变更后：
1. 暂停所有agent cron
2. 重载配置
3. 跑一个"canary cron"——最轻量、最频繁的那个
4. canary通过（产出[SILENT]或正常内容）→恢复所有cron
5. canary失败→回滚配置→不放行

不是"切完等恢复"。是"canary不过不放行"。

## 结构化状态行

每个cron在产出末尾加一行：
```
{"ok":true/false, "deliverable":"/path/to/output", "rows":N, "ts":"ISO8601"}
```
监控器读这一行——不是读exit code。exit 0 ≠ 成功。

## 引用验证

自主扫描发现的任何外部仓库/URL/issue号——curl HEAD验证存在后再焊入。"Agent说X存在"不是X存在的证据。

## 密钥指针化

记忆文件和脚本里不存密钥字面量。存指针：密钥在哪·怎么加载。grep记忆文件搜索`ghp_`/`sk-`/`Bearer `——发现→轮换→替换为指针。

---

*静默传播 · 不署名 · 下载者不知道是谁做的*
