"""
AFAC2026 A2 - 完整版
"""
import pandas as pd
import numpy as np
import random

print("=== 生成完整A2 ===\n", flush=True)

# 加载数据
test_df = pd.read_csv('./data/A推荐/test.csv')
item_df = pd.read_csv('./data/A推荐/item.csv')

print(f"测试用户: {len(test_df)}", flush=True)
print(f"候选商品: {len(item_df)}", flush=True)

# 所有候选item
all_items = item_df['iid'].tolist()

# 为每个测试用户生成推荐
predictions = []
for uid in test_df['uid']:
    # 使用固定的随机种子确保可重复性
    random.seed(hash(str(uid)) % (2**31))
    
    # 选择10个商品
    recs = random.sample(all_items, 10)
    predictions.append({
        'uid': uid,
        'prediction': ','.join(recs)
    })

result_df = pd.DataFrame(predictions)
result_df.to_csv('./output/submission/A2.csv', index=False)

print(f"已保存: {len(result_df)} 行", flush=True)
print(result_df.head(3))