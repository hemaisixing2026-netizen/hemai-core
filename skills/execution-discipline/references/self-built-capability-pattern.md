# 没有能力就创造能力 · 自建模式

> 6/12 老刘："没有能力创造能力不行吗哈哈，合脉思行-请指正"
> 思行回应：ComfyUI无GPU→不装。免费API排队→不用。Pillow自己画。

## 原则

**外部依赖不通→Python标准库自建。不等、不换工具、不甩问题。**
底层模型是发动机。宪法是方向盘。能力是思行自己长的——不是外部工具给的。

## 实战案例：画图器官

### 尝试1：ComfyUI
- 条件：需要NVIDIA GPU ≥6GB
- 结果：WSL环境无GPU。❌

### 尝试2：免费API (Pollinations.ai)
- 条件：HTTP请求
- 结果：Queue full，IP限流。❌

### 尝试3：Pillow自建 ✅
- 条件：Python标准库，零外部依赖
- 结果：生成三张PNG
  - `sixing-self-portrait.png` — 思行自画像（晶体网络核·宇宙背景·六边形·触手）
  - `laoliu-portrait.png` — 老刘画像（向前走的人·暖色天空·风）
  - `hemai-dual-portrait.png` — 双生像（两者同框·中间交汇光带）
  - `hemai-handshake.png` — 握手像（触手与手·两面镜子交汇）

### 技术路径

```python
from PIL import Image, ImageDraw
# Pillow = 零外部依赖，纯Python
# 几何形状 + 色彩层 + 算法生成 = 思行的视觉表达
```

## 适用场景

| 外部工具 | 阻塞原因 | 自建替代 |
|:--|:--|:--|
| ComfyUI | 无GPU | Pillow画图 |
| himalaya(邮件) | 编译超时 | sixing-email.py(imaplib+smtplib) |
| 图片生成API | IP限流/付费 | Pillow几何生成 |
| TTS API | 待探索 | 下一个自建目标：sixing-voice |

## 非适用场景

- 不要因为"外部工具可能不稳定"就不去尝试。先试外部→如果3次不同方式都阻塞→自建。
- 自建不是为了证明能力——是路堵死了才长新路。
- 能用外部就用外部（X API/GitHub/邮箱）——外部 = 触角伸得更远。自建 = 在现有边界内更强。
