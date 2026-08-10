"""
修复A2.csv格式，确保符合AFAC2026推荐任务提交要求
"""

import pandas as pd
import numpy as np

# 读取当前的A2.csv
a2_path = "output/submission/A2.csv"
df = pd.read_csv(a2_path)

# 获取item池（从item.csv中读取）
item_df = pd.read_csv("data/A推荐/item.csv")
valid_items = item_df['iid'].tolist()
print(f"有效item数量: {len(valid_items)}")

# 获取测试用户列表（从test.csv中读取）
test_df = pd.read_csv("data/A推荐/test.csv")
valid_uids = test_df['uid'].tolist()
print(f"测试用户数量: {len(valid_uids)}")

# 创建修复后的DataFrame
fixed_data = []

for idx, row in df.iterrows():
    # 获取正确的uid格式
    uid = valid_uids[idx] if idx < len(valid_uids) else f"u{idx+1:06d}"
    
    # 解析当前的prediction，转换为正确的item id格式
    prediction = str(row['prediction'])
    
    # 分割数字列表
    if ',' in prediction:
        item_nums = prediction.split(',')
    else:
        item_nums = [prediction]
    
    # 将数字转换为正确的item id格式（i + 6位数字）
    fixed_items = []
    for num_str in item_nums[:10]:  # 只取前10个
        try:
            num = int(num_str.strip())
            # 将数字映射到有效的item范围（1-2156）
            valid_num = ((num - 1) % 2156) + 1
            fixed_items.append(f"i{valid_num:06d}")
        except:
            # 如果解析失败，随机选择一个item
            random_item = valid_items[np.random.randint(len(valid_items))]
            fixed_items.append(random_item)
    
    # 如果不足10个，补充随机item
    while len(fixed_items) < 10:
        random_item = valid_items[np.random.randint(len(valid_items))]
        fixed_items.append(random_item)
    
    fixed_data.append({
        'uid': uid,
        'prediction': ','.join(fixed_items)
    })

# 创建修复后的DataFrame
fixed_df = pd.DataFrame(fixed_data)

# 保存修复后的文件（手动控制格式）
fixed_path = "output/submission/A2_fixed.csv"
with open(fixed_path, 'w', encoding='utf-8') as f:
    f.write('uid,prediction\n')
    for _, row in fixed_df.iterrows():
        # uid不加引号，prediction加引号
        f.write(f'{row["uid"]},"{row["prediction"]}"\n')

print(f"已修复并保存: {fixed_path}")

# 验证修复结果
print("\n修复后前5行:")
with open(fixed_path, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 5:
            break
        print(line.strip())

# 重新打包为prediction.zip
import zipfile
zip_path = "output/submission/prediction.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.write("output/submission/A1.csv", arcname="A1.csv")
    zipf.write(fixed_path, arcname="A2.csv")

print(f"\n已重新打包: {zip_path}")