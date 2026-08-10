"""生成高多样性A2推荐"""
import pandas as pd
import numpy as np
from collections import Counter

train = pd.read_csv('data/A推荐/train.csv')
test = pd.read_csv('data/A推荐/test.csv')
item_df = pd.read_csv('data/A推荐/item.csv')

all_items = list(item_df['iid'].tolist())
np.random.seed(42)

# 获取训练数据中的商品
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)
popular_items = [item for item, _ in item_counts.most_common(500)]

predictions = []
diversity_items = set()

for idx, row in test.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    history_set = set(history)
    
    recs = []
    
    # 1. 基于历史的推荐 (3个)
    if len(history) > 0:
        for hist_item in history[:3]:
            similar_users = train[train['target_iid'] == hist_item]['uid'].tolist()[:50]
            related = train[train['uid'].isin(similar_users)]['target_iid'].tolist()
            for item in related:
                if item not in history_set and item not in recs:
                    recs.append(item)
                    if len(recs) >= 3:
                        break
            if len(recs) >= 3:
                break
    
    # 2. 热门商品 (3个)
    for item in popular_items:
        if item not in history_set and item not in recs:
            recs.append(item)
        if len(recs) >= 6:
            break
    
    # 3. 随机商品 (4个) - 使用用户索引作为种子
    valid_items = [item for item in all_items if item not in history_set and item not in recs]
    np.random.seed(idx + 42)
    np.random.shuffle(valid_items)
    for item in valid_items:
        if len(recs) < 10:
            recs.append(item)
        else:
            break
    
    predictions.append(','.join(recs))
    diversity_items.update(recs)

# 保存
a2_result = pd.DataFrame({'uid': test['uid'], 'prediction': predictions})
output_lines = ['uid,prediction']
for _, row in a2_result.iterrows():
    output_lines.append(f'{row["uid"]},"{row["prediction"]}"')

with open('output/submission/A2.csv', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f'覆盖率: {len(diversity_items)/len(all_items)*100:.1f}%')
print(f'不同商品数: {len(diversity_items)}')