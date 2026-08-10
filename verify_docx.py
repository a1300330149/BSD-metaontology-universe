from docx import Document
import os

output_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\期刊理论\BSD_System_and_Metaphilosophical_Implications_Table1_Citation_Fixed.docx"

doc = Document(output_path)

print("=== DOCX Verification Report ===\n")

# 1. 检查2.4节引用标记
citation_found = False
section_24_context = []
for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text:
        section_24_context.append((i, para.style.name if para.style else "None", text[:200]))
    if "five truth values (see Table 1)" in text:
        citation_found = True
        print(f"[PASS] Citation found at paragraph {i}:")
        print(f"  Style: {para.style.name if para.style else 'None'}")
        print(f"  Text: {text}\n")
        break

if not citation_found:
    print("[FAIL] Citation 'five truth values (see Table 1)' NOT found.\n")
    print("Searching for similar text...")
    for i, para in enumerate(doc.paragraphs):
        if "five truth values" in para.text:
            print(f"  Paragraph {i}: {para.text[:300]}")

# 2. 检查Table 1
table1_found = False
table1_content = []
for i, table in enumerate(doc.tables):
    rows_text = []
    for row in table.rows:
        row_text = [cell.text.strip() for cell in row.cells]
        rows_text.append(row_text)
    # 检查是否是Table 1
    flat = " ".join(["|".join(r) for r in rows_text])
    if "Proposition Attribute" in flat and "Unfalsifiable" in flat and "Falsifiable" in flat:
        table1_found = True
        print(f"[PASS] Table 1 found at table index {i}:")
        for r in rows_text:
            print(f"  {' | '.join(r)}")
        print()
        break

if not table1_found:
    print("[FAIL] Table 1 NOT found.\n")

# 3. 检查文档基本统计
print(f"[INFO] Total paragraphs: {len(doc.paragraphs)}")
print(f"[INFO] Total tables: {len(doc.tables)}")
print(f"[INFO] File size: {os.path.getsize(output_path)} bytes")

# 4. 列出所有Heading样式段落
print("\n[INFO] Document Headings:")
for i, para in enumerate(doc.paragraphs):
    if para.style and para.style.name.startswith("Heading"):
        print(f"  {para.style.name}: {para.text[:100]}")

print("\n=== Verification Complete ===")
