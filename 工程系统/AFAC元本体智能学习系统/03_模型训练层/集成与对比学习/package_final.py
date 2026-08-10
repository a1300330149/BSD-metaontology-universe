import zipfile
import os

zip_path = 'output/submission/prediction_final.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write('output/submission/A1_improved.csv', arcname='A1.csv')
    zipf.write('output/submission/A2_improved.csv', arcname='A2.csv')

print(f'已打包: {zip_path}')
print(f'文件大小: {os.path.getsize(zip_path)/1024:.2f} KB')

# 验证内容
print('\n验证zip包内容:')
with zipfile.ZipFile(zip_path, 'r') as zipf:
    for name in zipf.namelist():
        print(f'  {name}')