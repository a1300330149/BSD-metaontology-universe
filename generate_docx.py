import json
from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import re
import os

# 路径配置
json_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\pdf_extracted.json"
output_dir = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\期刊理论"
output_path = os.path.join(output_dir, "BSD_System_and_Metaphilosophical_Implications_Table1_Citation_Fixed.docx")

# 读取提取的文本
with open(json_path, "r", encoding="utf-8") as f:
    pages = json.load(f)

# 合并所有页面文本
full_text = "\n".join(page["text"] for page in pages)

# 清理特殊字符
full_text = full_text.replace("\u0001", " ")

# 分割成段落（保留空行以辅助结构识别）
raw_lines = full_text.splitlines()
lines = [line.strip() for line in raw_lines]

# 预处理：合并以连字符结尾的断行（如 "Four-\nQuadrant Truth Model"）
merged_lines = []
j = 0
while j < len(lines):
    line = lines[j]
    if line.endswith('-') and j + 1 < len(lines):
        # 合并断行，去掉连字符
        line = line[:-1] + lines[j + 1]
        merged_lines.append(line.strip())
        j += 2
    else:
        merged_lines.append(line)
        j += 1
lines = merged_lines

# 创建文档
doc = Document()

# 设置默认字体
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')

# 标题样式辅助函数
def add_heading(doc, text, level):
    p = doc.add_heading(level=level)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.bold = True
    run.font.size = Pt([16, 14, 12][min(level-1, 2)])
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    return p

def add_paragraph(doc, text, style='Normal', bold=False, italic=False):
    p = doc.add_paragraph(style=style)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.font.bold = bold
    run.font.italic = italic
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    return p

# 状态机处理段落
i = 0
in_table1 = False
table1_data = []
in_table2 = False
table2_data = []
in_references = False
in_translation_notes = False

# 预处理：识别连续行，合并被拆分的句子
processed_lines = []
current_para = ""
for line in lines:
    if not line:
        if current_para:
            processed_lines.append(current_para.strip())
            current_para = ""
        continue
    # 如果是表格行或标题，先保存当前段落
    if line.startswith("Table ") or re.match(r'^[IVX]+\.\s', line) or re.match(r'^\d+\.\d+', line) or re.match(r'^A\d\s', line) or line in ["Abstract", "Introduction", "Keywords:", "References", "Translation Notes"]:
        if current_para:
            processed_lines.append(current_para.strip())
            current_para = ""
        processed_lines.append(line)
        continue
    # 如果是参考文献或列表项
    if re.match(r'^\[\d+\]', line) or line.startswith('◦'):
        if current_para:
            processed_lines.append(current_para.strip())
            current_para = ""
        processed_lines.append(line)
        continue
    # 普通文本行
    if current_para and not current_para.endswith('-'):
        current_para += " " + line
    else:
        current_para += line

if current_para:
    processed_lines.append(current_para.strip())

# 重新遍历处理后的段落
i = 0
while i < len(processed_lines):
    line = processed_lines[i]
    if not line:
        i += 1
        continue

    # 检测主标题 (H1)
    if line in ["Abstract", "Introduction", "Keywords:", "References", "Translation Notes"] or \
       re.match(r'^(I{1,3}|IV|V|VI{0,3}|IX|VII|VIII)\.', line):
        add_heading(doc, line, 1)
        if line == "References":
            in_references = True
        else:
            in_references = False
        if line == "Translation Notes":
            in_translation_notes = True
        else:
            in_translation_notes = False
        i += 1
        continue

    # 检测子标题 (H2) - 如 2.1, 2.2, 3.1 等
    if re.match(r'^\d+\.\d+', line):
        add_heading(doc, line, 2)
        i += 1
        continue

    # 检测附录子标题 A1, A2... (H2)
    if re.match(r'^A\d\s', line):
        add_heading(doc, line, 2)
        i += 1
        continue

    # 检测附录条目标题 (H3) - 如 "1.Passage:"
    if re.match(r'^\d+\.Passage:', line):
        add_heading(doc, line, 3)
        i += 1
        continue
    if re.match(r'^\d+\.Core', line):
        add_heading(doc, line, 3)
        i += 1
        continue

    # 检测 Table 1
    if line.startswith("Table 1"):
        # 添加表格标题段落
        add_paragraph(doc, line, bold=True)
        # 跳过提取文本中可能已被合并的表格数据行
        i += 1
        while i < len(processed_lines):
            next_line = processed_lines[i]
            # 如果下一行仍然包含Table 1的数据内容，则跳过
            if "Proposition Attribute" in next_line or "Unfalsifiable" in next_line or \
               "Provable" in next_line or "Unprovable" in next_line or \
               "True Statement" in next_line or "Suspended Statement" in next_line or \
               "Positive/Inverse" in next_line or "Fallacious Statement" in next_line:
                i += 1
            else:
                break
        # 直接重建 Table 1（内容已知）
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = "Proposition Attribute"
        hdr_cells[1].text = "Unfalsifiable"
        hdr_cells[2].text = "Falsifiable"
        # 数据行 1
        row_cells = table.add_row().cells
        row_cells[0].text = "Provable"
        row_cells[1].text = "True Statement"
        row_cells[2].text = "Positive/Inverse Statement"
        # 数据行 2
        row_cells = table.add_row().cells
        row_cells[0].text = "Unprovable"
        row_cells[1].text = "Suspended Statement"
        row_cells[2].text = "Fallacious Statement"
        continue

    # 检测 Table 2 (Page 16-17 的对比表格)
    if line.startswith("Table 2") or line.startswith("Comparative Table"):
        add_paragraph(doc, line, bold=True)
        i += 1
        continue

    # 处理参考文献
    if in_references and re.match(r'^\[\d+\]', line):
        add_paragraph(doc, line, style='Normal')
        i += 1
        continue

    # 处理列表项 (◦)
    if line.startswith('◦'):
        add_paragraph(doc, line, style='List Bullet')
        i += 1
        continue

    # 处理翻译注释中的列表项
    if in_translation_notes and (line.startswith('◦') or re.match(r'^\d+\.', line)):
        add_paragraph(doc, line, style='List Bullet')
        i += 1
        continue

    # 核心修改：在2.4节开头段落添加 Table 1 引用
    # 检测是否包含目标文本
    if "five truth values," in line and "four-quadrant" in line and "provability and falsifiability" in line:
        line = line.replace("five truth values,", "five truth values (see Table 1),", 1)
        add_paragraph(doc, line, style='Normal')
        i += 1
        continue

    # 普通正文
    add_paragraph(doc, line, style='Normal')
    i += 1

# 保存文档
os.makedirs(output_dir, exist_ok=True)
doc.save(output_path)
print(f"DOCX saved to: {output_path}")
