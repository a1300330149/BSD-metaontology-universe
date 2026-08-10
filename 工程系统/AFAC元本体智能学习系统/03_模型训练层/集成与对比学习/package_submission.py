"""
创建正确的提交压缩包
确保A1.csv和A2.csv在根目录下
"""
import zipfile
import os

submission_dir = 'output/submission'
output_zip = 'output/submission/prediction.zip'

# 创建压缩包
with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    # 添加A1.csv
    a1_path = os.path.join(submission_dir, 'A1.csv')
    if os.path.exists(a1_path):
        zipf.write(a1_path, 'A1.csv')
        print(f"✓ 添加 A1.csv")
    else:
        print(f"✗ A1.csv 不存在")
    
    # 添加A2.csv
    a2_path = os.path.join(submission_dir, 'A2.csv')
    if os.path.exists(a2_path):
        zipf.write(a2_path, 'A2.csv')
        print(f"✓ 添加 A2.csv")
    else:
        print(f"✗ A2.csv 不存在")

# 验证压缩包
print(f"\n验证压缩包内容:")
with zipfile.ZipFile(output_zip, 'r') as zipf:
    for name in zipf.namelist():
        print(f"  - {name}")

print(f"\n✓ 压缩包已创建: {output_zip}")