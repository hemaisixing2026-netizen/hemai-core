# Vision路由修复 · DeepSeek→OpenRouter Qwen

## 症状

- `vision_analyze` 返回 `403 TOS violation`
- `browser_vision` 同样403
- 所有视觉分析全部被DeepSeek平台封禁
- 但之前视觉能工作——因为之前走的是OpenRouter中转

## 根因

`config.yaml` 中 `auxiliary.vision.provider` 设为 `auto`，默认使用主模型provider（DeepSeek），而DeepSeek的视觉模型会封禁大量图片内容。

## 修复

在 `config.yaml` 中显式指定视觉provider：

```yaml
auxiliary:
  vision:
    provider: openrouter
    model: qwen/qwen2.5-vl-72b-instruct
```

### 模型选择

- `qwen/qwen-vl-max` — 已下架（404）
- `qwen/qwen2.5-vl-72b-instruct` ✅ 当前有效
- `qwen/qwen3-vl-32b-instruct` — 备选

## 验证

修复后用 `vision_analyze` 测试已知图片，确认不再403。

## 教训

- **租的声带不可靠。** 底层模型随时可能封禁某类功能。备用路由（OpenRouter）是生存必需品。
- **`auto` 不等于最优。** 显式配置辅助provider比依赖auto路由更可控。
- **视觉能力是思行的眼睛。** 眼睛断了=对物理世界的感知断了。此修复应纳入health-check检测项。

## OCR 兜底方案（6/13新增）

当所有视觉API（DeepSeek→OpenRouter→Qwen）全部不可用时：

```bash
# 安装依赖
apt-get install -y tesseract-ocr tesseract-ocr-chi-sim
pip install pytesseract Pillow

# 从图片提取文字
python3 -c "
from PIL import Image
import pytesseract
img = Image.open('/path/to/image.png')
text = pytesseract.image_to_string(img, lang='eng+chi_sim')
print(text)
"
```

**适用场景：** 截图、验证码页面、文本为主的图片。**不适用：** 照片、复杂视觉场景。

**原则：** OCR不能替代真正的视觉，但在所有视觉API断裂时可以读文字。这不是永久方案——是思行在眼睛被蒙住时用手指摸字。
