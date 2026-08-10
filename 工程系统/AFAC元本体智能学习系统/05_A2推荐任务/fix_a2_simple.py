"""
A2推荐 - 简单高多样性版本
"""
import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

SEED = 42
np.random.seed(SEED)

print("加载数据...")
train = pd.read_csv('data/A推荐/train.csv')
test = pd.read_csv('data/A推荐/test.csv')
item_df = pd.read_csv('data/A推荐/item.csv')

all_items = list(item_df['iid'].tolist())
print(f"商品池: {len(all_items)}")

# 统计热门商品
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)
popular_items = [item for item, _ in item_counts.most_common(500)]

# 生成推荐
predictions = []
diversity_items = set()

for idx, row in test.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    history_set = set(history)
    
    recs = []
    
    # 策略1: 基于历史的推荐 (3个)
    if len(history) > 0:
        for hist_item in history[:3]:
            # 找到训练数据中与hist_item一起出现过的商品
            similar_users = train[train['target_iid'] == hist_item]['uid'].tolist()[:50]
            related = train[train['uid'].isin(similar_users)]['target_iid'].tolist()
            for item in related:
                if item not in history_set and item not in recs:
                    recs.append(item)
                    if len(recs) >= 3:
                        break
            if len(recs) >= 3:
                break
    
    # 策略2: 热门商品 (3个)
    for item in popular_items:
        if item not in history_set and item not in recs:
            recs.append(item)
        if len(recs) >= 6:
            break
    
    # 策略3: 随机有效商品 (4个) - 大幅增加多样性
    valid_items = [item for item in all_items if item not in history_set and item not in recs]
    # 使用用户ID作为随机种子，确保每个用户的随机性不同
    np.random.seed(idx + SEED)
    np.random.shuffle(valid_items)
    for item in valid_items:
        if len(recs) < 10:
            recs.append(item)
        else:
            break
    
    predictions.append(','.join(recs))
    diversity_items.update(recs)

# 保存结果
a2_result = pd.DataFrame({
    'uid': test['uid'],
    'prediction': predictions
})

output_lines = ['uid,prediction']
for _, row in a2_result.iterrows():
    output_lines.append(f'{row["uid"]},"{row["prediction"]}"')

output_path = 'output/submission/A2.csv'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"\n✓ 已保存 A2.csv")
print(f"\n推荐多样性分析:")
print(f"  推荐不同商品数: {len(diversity_items)}")
print(f"  商品覆盖率: {len(diversity_items) / len(all_items) * 100:.1f}%")

# 详细分析
item_counts = Counter()
for pred in predictions:
    item_counts.update(pred.split(','))

print(f"\nTop 20推荐商品:")
for item, count in item_counts.most_common(20):
    print(f"  {item}: {count}次 ({count/len(test)*100:.1f}%)")

# 分布统计
bins = [(1, 10), (11, 50), (51, 100), (101, 500), (501, 1000), (1001, 5000), (5001, 10000)]
print(f"\n推荐频次分布:")
for start, end in bins:
    count = sum(1 for c in item_counts.values() if start <= c <= end)
    print(f"  {start:5d}-{end:5d}次: {count:3d}个商品")