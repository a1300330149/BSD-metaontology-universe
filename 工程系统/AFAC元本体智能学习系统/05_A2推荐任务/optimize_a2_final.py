"""
A2推荐任务最终优化版
- 高多样性策略
- 多层级推荐融合
- 目标: 超越0.76845
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

# 分析训练数据中的商品分布
print(f"训练目标商品数: {len(item_counts)}")
print(f"热门商品覆盖率: {len(set(popular_items[:100]) & set(train_items))/len(train_items)*100:.1f}%")

# 生成推荐
predictions = []
diversity_items = set()

for _, row in test.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = [item for item in history_str.split(',') if item in all_items]
    history_set = set(history)
    
    scores = defaultdict(float)
    
    # 策略1: 基于历史的协同过滤 (权重40%)
    for item in history[:5]:
        if item in co_occur:
            for related, cnt in co_occur[item].most_common(30):
                if related not in history_set:
                    scores[related] += cnt * 0.4
    
    # 策略2: 热门商品 (权重30%)
    for idx, item in enumerate(popular_items[:200]):
        if item not in history_set:
            scores[item] += (200 - idx) * 0.015
    
    # 策略3: 训练数据中出现过的商品 (权重20%)
    for item in train_items[:1000]:
        if item not in history_set and item in all_items:
            scores[item] += 0.2
    
    # 策略4: 随机有效商品增加多样性 (权重10%)
    np.random.shuffle(item_list)
    for item in item_list[:500]:
        if item not in history_set:
            scores[item] += np.random.random() * 0.1
    
    # 排序并获取Top 10
    sorted_items = sorted(scores.items(), key=lambda x: -x[1])
    recs = [item for item, _ in sorted_items[:10]]
    
    # 确保有足够多样性
    if len(set(recs)) < 8:
        valid_items = [item for item in item_list if item not in history_set and item not in recs]
        np.random.shuffle(valid_items)
        for item in valid_items[:3]:
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

output_path = 'output/submission/A2_final.csv'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output_lines) + '\n')

print(f"\n✓ 已保存 A2_final.csv")
print(f"推荐多样性分析:")
print(f"  推荐不同商品数: {len(diversity_items)}")
print(f"  商品覆盖率: {len(diversity_items) / len(all_items) * 100:.1f}%")

# 验证格式
print(f"\n格式验证:")
with open(output_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    print(f"  行数: {len(lines)}")
    print(f"  首行: {lines[0].strip()}")
    print(f"  示例行: {lines[1].strip()}")