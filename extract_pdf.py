import PyPDF2
import json
import os

pdf_path = r"C:\Users\13003\Downloads\BSD System and Its Metaphilosophical Implications.pdf"
output_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\pdf_extracted.json"

reader = PyPDF2.PdfReader(pdf_path)
pages = []
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    pages.append({
        "page_num": i + 1,
        "text": text
    })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(pages, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(pages)} pages to {output_path}")
