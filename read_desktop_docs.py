from docx import Document
import os

desktop = r"C:\Users\13003\OneDrive\桌面"
docx_files = [
    r"意义大一统.docx",
    r"本源结构.docx",
    r"天道6系.docx",
    r"全方位推翻广义存在论（GET）.docx",
]

for fname in docx_files:
    path = os.path.join(desktop, fname)
    if not os.path.exists(path):
        print(f"NOT FOUND: {fname}")
        continue
    try:
        doc = Document(path)
        text = "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
        preview = text[:500]
        print(f"=== {fname} ===")
        print(preview)
        print()
    except Exception as e:
        print(f"ERROR {fname}: {e}")
