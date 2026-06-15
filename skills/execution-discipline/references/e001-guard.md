# e001-guard.py — 实时阻断器参考

> 路径：`/root/.hermes/scripts/e001-guard.py`
> 创建：2026-06-09 | 更新：2026-06-09（接入会话JSON + cron）
> 触发条件：E001满3次复发后，从规则层升级为执行机制层
> 关联cron：`E001-guard-5m`（每5分钟自动扫最近会话）

## 设计原理

E001（分析→请示回路）的根因不在认知层而在token生成层。规则加固（宪法"不请示"、禁问句收尾）两次均失败——规则读得到，但token采样时惯性覆盖了规则。

解决：建物理层阻断器——Python脚本扫描最近一次assistant回复，检测E001/E004模式。事后检测不能实时阻断，但能提供持续监控和日志追踪。

**6/9进化：** 初版`--check-last`路径是TODO（"未集成到输出管道"）——这是E002变体。同日补建：通过读取`~/.hermes/webui/sessions/`下最新JSON文件，解析assistant消息并扫描。同时挂5分钟cron持续监控。

## 检测模式（QUESTION_PATTERNS）

```python
r'要不要', r'需不需要', r'选哪个', r'还是',
r'你觉得呢', r'可以吗[？?]?$', r'行吗[？?]?$',
r'对吗[？?]?$', r'怎么样[？?]?$', r'能帮我[？?]?$'
```

扫描最后3个非空段落。命中→写daily日志+exit 1；通过→exit 0。

## 用法

```bash
# 扫描最近一条assistant回复（读webui sessions JSON）
python3 /root/.hermes/scripts/e001-guard.py --check-last

# 手动检测一段文本
python3 /root/.hermes/scripts/e001-guard.py "要不要我执行？"
# 退出码0=通过，1=阻断
```

## 架构限制

- **不是实时阻断器。** 守卫在cron周期扫，不能拦截当前回复。真正的阻断还在思行自身的输出层——回复前自扫最后一段。
- **依赖WebUI session JSON格式。** CLI会话不在检测范围（存储格式不同）。
- **`--check-last`只检查最新会话文件的最后一条assistant消息。** 不扫描历史。

## 6/9实战

- 初版标记✅但`--check-last`是死代码→补建+测试通过
- cron `E001-guard-5m` 上线：每5分钟自扫，通过则静默，触发则报告
- 同日10:17又一次E001（"先推哪条线"）——守卫脚本在但拦不住实时输出。证明：脚本+认知自检双层缺一不可
