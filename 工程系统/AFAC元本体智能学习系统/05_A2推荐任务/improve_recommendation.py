import pandas as pd
import numpy as np
from collections import Counter

print("=== 分析A2.csv推荐质量 ===")

# 读取数据
a2 = pd.read_csv('output/submission/A2_fixed.csv')
train = pd.read_csv('../data/A推荐/train.csv')
test = pd.read_csv('../data/A推荐/test.csv')
item_df = pd.read_csv('../data/A推荐/item.csv')

print(f"\n1. 基本统计:")
print(f"   总用户数: {len(a2)}")
print(f"   推荐数量: {a2['prediction'].apply(lambda x: len(x.split(','))).mean():.1f}")

# 分析推荐多样性
print(f"\n2. 推荐多样性分析:")
all_items = []
a2['prediction'].apply(lambda x: all_items.extend(x.split(',')))
unique_items = len(set(all_items))
print(f"   推荐的不同商品数: {unique_items}")
print(f"   商品池总数: {len(item_df)}")
print(f"   覆盖率: {unique_items/len(item_df)*100:.1f}%")

# 分析热门商品
print(f"\n3. 热门推荐商品:")
item_counts = Counter(all_items)
top_items = item_counts.most_common(10)
for item, count in top_items:
    print(f"   {item}: {count}次 ({count/len(a2)*100:.1f}%)")

# 分析训练数据中的热门商品
print(f"\n4. 训练数据热门商品:")
train_items = []
train['target_iid'].apply(lambda x: train_items.append(x))
train_item_counts = Counter(train_items)
train_top_items = train_item_counts.most_common(10)
for item, count in train_top_items:
    print(f"   {item}: {count}次 ({count/len(train)*100:.1f}%)")

# 分析推荐与训练数据的匹配度
print(f"\n5. 推荐质量分析:")
recommended_items = set(all_items)
train_item_set = set(train_items)
overlap = recommended_items & train_item_set
print(f"   推荐商品中出现在训练数据中的比例: {len(overlap)/len(recommended_items)*100:.1f}%")

# 分析用户历史交互
print(f"\n6. 用户历史交互分析:")
test['history_length'] = test['item_seq_dedup'].apply(lambda x: len(x.split(',')) if pd.notna(x) and x else 0)
print(f"   平均历史交互长度: {test['history_length'].mean():.1f}")
print(f"   最长历史交互: {test['history_length'].max()}")
print(f"   最短历史交互: {test['history_length'].min()}")

# 简单的基于流行度的推荐策略
print(f"\n7. 生成改进的推荐...")
# 基于训练数据的流行度推荐
popular_items = [item for item, count in train_item_counts.most_common(100)]

# 为每个用户生成推荐
improved_predictions = []
for _, row in test.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = history_str.split(',') if history_str else []

    # 基于历史推荐相似商品
    history_items = [item for item in history if item in train_item_set]

    # 结合流行度和历史
    recommended = []
    # 添加历史相关商品（简单策略：推荐训练数据中与历史商品一起出现的商品）
    for hist_item in history_items[:3]:  # 只考虑前3个历史商品
        # 找到训练数据中与hist_item一起出现的其他商品
        related_users = train[train['target_iid'] == hist_item]['uid'].tolist()
        related_items = train[train['uid'].isin(related_users)]['target_iid'].tolist()
        related_items = [item for item in related_items if item not in history and item not in recommended]
        recommended.extend(related_items[:2])

    # 添加流行商品
    for item in popular_items:
        if item not in history and item not in recommended:
            recommended.append(item)
        if len(recommended) >= 10:
            break

    # 确保有10个推荐
    if len(recommended) < 10:
        for item in popular_items:
            if item not in recommended:
                recommended.append(item)
            if len(recommended) >= 10:
                break

    improved_predictions.append(','.join(recommended[:10]))

# 保存改进的A2.csv
improved_a2 = pd.DataFrame({
    'uid': test['uid'],
    'prediction': improved_predictions
})

output_path = 'output/submission/A2_improved.csv'
improved_a2.to_csv(output_path, index=False)
print(f"   已保存改进的A2.csv: {output_path}")

# 分析改进后的推荐
print(f"\n8. 改进后的推荐分析:")
all_items_improved = []
improved_a2['prediction'].apply(lambda x: all_items_improved.extend(x.split(',')))
unique_items_improved = len(set(all_items_improved))
print(f"   推荐的不同商品数: {unique_items_improved}")
print(f"   覆盖率: {unique_items_improved/len(item_df)*100:.1f}%")

item_counts_improved = Counter(all_items_improved)
top_items_improved = item_counts_improved.most_common(10)
print(f"\n   改进后热门推荐商品:")
for item, count in top_items_improved:
    print(f"      {item}: {count}次 ({count/len(improved_a2)*100:.1f}%)")