"""
A2推荐任务 - 高多样性版本
目标覆盖率: 30%+
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
item_list = list(all_items)
print(f"商品池: {len(all_items)}")

# 统计热门商品
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)
popular_items = [item for item, _ in item_counts.most_common(500)]

# 构建商品共现矩阵
co_occur = defaultdict(Counter)
for _, row in train.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    target = row['target_iid']
    for item in history:
        co_occur[item][target] += 1

# 构建商品相似度矩阵
item_similarity = defaultdict(dict)
for item1 in popular_items[:300]:
    for item2 in popular_items[:300]:
        if item1 != item2:
            # 基于共现的相似度
            common_users = len(set(co_occur[item1].keys()) & set(co_occur[item2].keys()))
            if common_users > 0:
                item_similarity[item1][item2] = common_users

# 生成高多样性推荐
predictions = []
diversity_items = set()

for idx, row in test.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    history_set = set(history)
    
    scores = defaultdict(float)
    
    # 策略1: 基于历史的协同过滤 (权重25%)
    for item in history[:5]:
        if item in co_occur:
            for related, cnt in co_occur[item].most_common(50):
                if related not in history_set:
                    scores[related] += cnt * 0.25
    
    # 策略2: 热门商品 (权重20%)
    for idx_item, item in enumerate(popular_items[:300]):
        if item not in history_set:
            scores[item] += (300 - idx_item) * 0.01
    
    # 策略3: 训练数据中出现过的商品 (权重20%)
    for item in train_items[:2000]:
        if item not in history_set and item in all_items:
            scores[item] += 0.15
    
    # 策略4: 基于相似商品的推荐 (权重15%)
    for hist_item in history[:3]:
        if hist_item in item_similarity:
            for similar, sim_score in item_similarity[hist_item].items():
                if similar not in history_set:
                    scores[similar] += sim_score * 0.05
    
    # 策略5: 随机有效商品大幅增加多样性 (权重20%)
    np.random.shuffle(item_list)
    for item in item_list[:1500]:
        if item not in history_set:
            scores[item] += np.random.random() * 0.2
    
    # 排序并获取Top 10
    sorted_items = sorted(scores.items(), key=lambda x: -x[1])
    recs = [item for item, _ in sorted_items[:10]]
    
    # 确保高多样性
    if len(set(recs)) < 8:
        valid_items = [item for item in item_list if item not in history_set and item not in recs]
        np.random.shuffle(valid_items)
        for item in valid_items[:5]:
            if len(recs) < 10:
                recs.append(item)
    
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