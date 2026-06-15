# Temu/1688 数据整合工作流

> 2026-06-08 | 从老刘三个Excel文件（备货单+价格表+款式推荐）整合实战

## 场景

Temu卖家需要：备货单入库状态 + 1688采购价格 → 整合表 → 算利润。

典型输入：Temu后台导出的备货单Excel + 1688采购价格表Excel + 款式推荐Excel。
典型挑战：三张表之间无共同关联键（备货单用"备货单号"，价格表用"款式货号"）。

## 工作流

### Step 1: 读取Excel数据

```python
import openpyxl
wb = openpyxl.load_workbook("file.xlsx", data_only=True)
ws = wb[wb.sheetnames[0]]
for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
    print([str(c) if c is not None else '' for c in row])
```

注意：WPS生成的xlsx可能包含DISPIMG公式（`=DISPIMG("ID_xxx",1)`），这是嵌入图片的引用。openpyxl读取时只看到公式文本，看不到图片内容。

### Step 2: 提取嵌入图片（关键步骤）

xlsx本质是zip。图片存储在`xl/media/`下：

```python
import zipfile, os
with zipfile.ZipFile("file.xlsx", 'r') as z:
    for f in z.namelist():
        if 'media' in f.lower():
            z.extract(f, output_dir)
```

图片与行的映射关系在`xl/cellimages.xml`中，解析DISPIMG ID → image file映射。

### Step 3: 视觉识别产品

使用vision_analyze逐个识别产品图片，批量时用简洁问题（10-15字限制）减少token消耗。

### Step 4: 建立整合表

格式：备货单号 | 状态 | 数量 | 颜色 | 产品描述 | 1688货号 | 采购价
产品描述列由视觉识别自动填充。货号和采购价需人工确认（无自动匹配键）。

## Pitfalls

- **DISPIMG ≠ 普通图片。** WPS的DISPIMG公式引用的是cellimages.xml中的图片ID。openpyxl的`ws._images`列表可能为空，必须用zip解压方式提取。
- **视觉匹配不可靠。** Temu商品照（精修白底图）vs 1688供应商图（随意拍摄）风格差异大，同款产品外观可能截然不同。
- **价格表可能不完整。** 备货单产品可能来自多个供应商，当前价格表只覆盖部分。
- **人工确认环节不可跳过。** 自动视觉匹配只能做初步筛选（6/8案例：16款中仅3对可自动匹配）。最终货号+价格必须由卖家手动确认——没有共同关联键的数据集之间不存在可靠的自动映射。

## 完成案例（6/8）

**输入：** 备货单入库状态统计_20251120.xlsx + 款式货号价格表.xlsx + 款式推荐_1_.xlsx

**输出：** Temu_清退记录.md — 18单/345件/¥10,130总采购成本

**流程：** 读取Excel → zip解压提取16张产品图 → 视觉AI逐个识别 → 建整合表（货号+价格列为空） → 老刘手动填充17/18行货号价格 → 存档为清退记录

**耗时：** 视觉识别16张图约15次API调用。人工填充5分钟。

**关键经验：** 自动部分做数据提取+产品描述。匹配部分留给卖家——他们10秒能做完的事，AI用100次API调用也做不准。
