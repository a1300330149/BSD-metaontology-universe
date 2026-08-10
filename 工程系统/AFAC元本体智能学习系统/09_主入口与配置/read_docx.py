from docx import Document
import os

doc_path = r"C:\Users\13003\OneDrive\桌面\意义大一统.docx"
doc = Document(doc_path)

print(f"=== 意义大一统.docx 内容 ===\n")
print(f"文档段落数: {len(doc.paragraphs)}\n")

# 输出所有段落内容
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text:
        print(f"[段落{i}] {text[:200]}{'...' if len(text) > 200 else ''}")

# 输出表格内容
if doc.tables:
    print(f"\n表格数: {len(doc.tables)}")
    for t_idx, table in enumerate(doc.tables):
        print(f"\n表格{t_idx}:")
        for row in table.rows[:5]:  # 只显示前5行
            cells = [cell.text[:50] for cell in row.cells]
            print(f"  {cells}")