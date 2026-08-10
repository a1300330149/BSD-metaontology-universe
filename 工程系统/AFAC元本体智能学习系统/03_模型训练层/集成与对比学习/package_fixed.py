"""
打包修复后的提交文件
"""
import zipfile
import os

os.makedirs("output/submission", exist_ok=True)

# 打包
zip_path = "output/submission/prediction_fixed.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("output/submission/A1_improved.csv", arcname="A1.csv")
    zipf.write("output/submission/A2.csv", arcname="A2.csv")

print(f"✓ 已打包: {zip_path}")
print(f"  - A1.csv: 修复格式 (2751行)")
print(f"  - A2.csv: 修复格式 (10000行, uid=u000009格式, item=i000001格式)")