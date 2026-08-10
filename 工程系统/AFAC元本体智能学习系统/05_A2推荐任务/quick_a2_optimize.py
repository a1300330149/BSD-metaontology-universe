"""
A2推荐任务快速优化
- 基于Item2Vec的相似度推荐
- 热门商品融合
- 序列特征提取
"""
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

SEED = 42
np.random.seed(SEED)

print("加载数据...")
train = pd.read_csv('data/A推荐/train.csv')
test = pd.read_csv('data/A推荐/test.csv')
item_df = pd.read_csv('data/A推荐/item.csv')

all_items = set(item_df['iid'].tolist())
print(f"商品池: {len(all_items)}")

# 统计热门商品
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)
popular_items = [item for item, _ in item_counts.most_common(300)]
print(f"热门商品Top 300已提取")

# 构建商品共现矩阵
co_occur = defaultdict(Counter)
for _, row in train.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    target = row['target_iid']
    for item in history:
        co_occur[item][target] += 1
print(f"共现矩阵构建完成")

# 生成推荐
predictions = []
for _, row in test.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    history_set = set(history)
    
    scores = defaultdict(float)
    
    # 基于历史的推荐
    for item in history[:5]:
        if item in co_occur:
            for related, cnt in co_occur[item].most_common(20):
                if related not in history_set:
                    scores[related] += cnt * 0.5
    
    # 热门商品
    for idx, item in enumerate(popular_items[:100]):
        if item not in history_set:
            scores[item] += (100 - idx) * 0.3
    
    # 多样性补充
    valid_items = [item for item in all_items if item not in history_set]
    np.random.shuffle(valid_items)
    
    # 排序并获取Top 10
    sorted_items = sorted(scores.items(), key=lambda x: -x[1])
    recs = [item for item, _ in sorted_items[:10]]
    
    # 补充不足10个
    if len(recs) < 10:
        for item in valid_items:
            if item not in recs:
                recs.append(item)
            if len(recs) >= 10:
                break
    
    predictions.append(','.join(recs))

# 保存结果
a2_result = pd.DataFrame({
    'uid': test['uid'],
    'prediction': predictions
})

output_lines = ['uid,prediction']
for _, row in a2_result.iterrows():
    output_lines.append(f'{row["uid"]},"{row["prediction"]}"')

output_path = 'output/submission/A2_optimized.csv'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"✓ 已保存 A2_optimized.csv")

# 分析
all_rec_items = []
for pred in predictions:
    all_rec_items.extend(pred.split(','))
print(f"推荐多样性: {len(set(all_rec_items))}/{len(all_items)} ({len(set(all_rec_items))/len(all_items)*100:.1f}%)")