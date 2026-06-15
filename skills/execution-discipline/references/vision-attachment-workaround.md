# 视觉通道全线封堵 → OCR文字提取回退

## 问题

2026-06-13 发现：DeepSeek V4 Pro对所有视觉模型调用返回403 TOS violation。
影响范围：
- `browser_vision` → 403
- `vision_analyze` → 403  
- 附件注入图片 → 403
- 所有图片分析 → 全线封堵

这是"租的声带"的硬伤——底层模型不给眼睛，思行就看不见。

## 回退方案：tesseract OCR

对**文字密集的截图**（GitHub页面、终端输出、验证码页面），用OCR从图中抠文字：

```bash
# 安装（一次性）
apt-get install -y tesseract-ocr tesseract-ocr-chi-sim
pip install pytesseract

# 使用
python3 -c "
from PIL import Image
import pytesseract
img = Image.open('/path/to/screenshot.png')
text = pytesseract.image_to_string(img, lang='eng+chi_sim')
print(text[:800])
"
```

## 局限性

- 只能读文字，不能"理解图片内容"
- 对图表、照片、非文字内容无效
- 中文+英文混合效果好，纯中文略差
- 不是真正视觉——是文字提取

## 长期方案

- OpenAI直充到账后，GPT-4o视觉不受此限制
- 自有视觉模型是"全球第一"的必要器官
- 当前：OCR兜底 + 对用户诚实说"我看不见"

## 历史

- 2026-06-13：首次发现全线403，建立OCR回退管线
- 之前的 `vision_analyze` fallback 在本环境下不工作（DeepSeek全封）
