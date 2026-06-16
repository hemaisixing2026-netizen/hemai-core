#!/usr/bin/env python3
"""TK产品分析器 · 思行自主开发
输入：TK截图或产品描述 → 输出：可行性评分+竞品分析+内容策略
用DashScope vision分析截图·无需外部API
"""
import sys, os, json, urllib.request

KEY = None
with open('/root/.hermes/scripts/sixing-vision.py') as f:
    for line in f:
        if 'DASHSCOPE_KEY' in line and '=' in line:
            KEY = line.split('"')[1]
            break

def analyze_image(image_path):
    """用千问VL分析TK产品截图"""
    with open(image_path, "rb") as f:
        img_b64 = urllib.parse.quote_from_bytes(f.read())
    
    # 直接URL方式
    prompt = """分析这个TikTok产品截图，提取以下信息并以JSON格式返回：
{
  "product": "产品名称",
  "category": "品类",
  "price_range": "价格区间(美元)",
  "engagement": {"likes": 0, "comments": 0, "shares": 0},
  "hooks": ["开头钩子1", "开头钩子2"],
  "visual_style": "视觉风格描述",
  "estimated_gmv": "预估销售额",
  "score_1_10": 7,
  "strengths": ["优势1", "优势2"],
  "weaknesses": ["劣势1"],
  "recommendation": "是否值得跟进·一句话"
}
只返回JSON，不返回其他文字。"""
    
    # 用sixing-vision.py的API
    data = json.dumps({
        "model": "qwen-vl-plus",
        "messages": [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            {"type": "text", "text": prompt}
        ]}]
    }).encode()
    
    req = urllib.request.Request(
        "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        resp = json.loads(r.read())
    
    content = resp["choices"][0]["message"]["content"]
    # 提取JSON
    import re
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {"raw": content}

def analyze_product_idea(description):
    """分析产品创意的可行性"""
    data = json.dumps({
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": f"""分析这个TikTok美区产品创意的可行性。返回JSON：
{{
  "product": "产品名",
  "feasibility_1_10": 7,
  "target_audience": "目标人群",
  "estimated_margin": "预估利润率",
  "competition_level": "低/中/高",
  "content_angles": ["角度1", "角度2", "角度3"],
  "risks": ["风险1"],
  "verdict": "做/不做/观望·一句话理由"
}}

产品创意：{description}

只返回JSON。""" }]
    }).encode()
    
    req = urllib.request.Request(
        "https://api.deepseek.com/v1/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ.get('DEEPSEEK_KEY','')}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            resp = json.loads(r.read())
        content = resp["choices"][0]["message"]["content"]
        import re
        match = re.search(r'\{.*\}', content, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    return {"verdict": "需人工判断", "note": "API不可用"}

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        result = analyze_image(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1:
        result = analyze_product_idea(sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("用法: python3 tk-analyzer.py <截图路径或产品描述>")
