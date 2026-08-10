import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("改进A2推荐 - 多样化推荐策略")
print("=" * 80)

# 1. 加载数据
print("\n【1】加载数据...")
train = pd.read_csv('../data/A推荐/train.csv')
test = pd.read_csv('../data/A推荐/test.csv')
item_df = pd.read_csv('../data/A推荐/item.csv')

print(f"  训练集用户数: {len(train)}")
print(f"  测试集用户数: {len(test)}")
print(f"  商品池大小: {len(item_df)}")

# 2. 分析训练数据中的商品分布
print("\n【2】分析训练数据商品分布...")
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)

print(f"  训练数据商品数: {len(item_counts)}")
print(f"  Top 10热门商品:")
for i, (item, count) in enumerate(item_counts.most_common(10), 1):
    pct = count / len(train) * 100
    print(f"    {i:2d}. {item}: {count:5d}次 ({pct:5.1f}%)")

# 3. 分析测试用户历史
print("\n【3】分析测试用户历史...")
test_histories = []
for _, row in test.iterrows():
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = history_str.split(',') if history_str else []
    test_histories.append(history)

avg_history_len = np.mean([len(h) for h in test_histories])
print(f"  测试用户平均历史长度: {avg_history_len:.1f}")

# 4. 获取所有有效商品
all_valid_items = set(item_df['iid'].tolist())
print(f"  有效商品池: {len(all_valid_items)}个商品")

# 5. 分析训练商品与有效商品的匹配
train_item_set = set(train_items)
overlap = train_item_set & all_valid_items
print(f"  训练商品在有效池中: {len(overlap)}/{len(train_item_set)}")

# 6. 制定分层推荐策略
print("\n【4】制定分层推荐策略...")

# 层级1: 训练数据中的热门商品（与用户历史相关）
popular_in_train = [item for item, count in item_counts.most_common(100)]
print(f"  层级1: 训练热门商品Top 100")

# 层级2: 所有有效商品（增加多样性）
all_valid_list = list(all_valid_items)
np.random.seed(42)
np.random.shuffle(all_valid_list)
print(f"  层级2: 随机有效商品")

# 层级3: 基于用户历史推荐
print(f"  层级3: 基于用户历史推荐")

# 7. 生成多样化推荐
print("\n【5】生成多样化推荐...")
predictions = []

for idx, row in test.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = history_str.split(',') if history_str else []

    # 过滤有效商品
    valid_history = [item for item in history if item in all_valid_items]
    history_set = set(valid_history)

    recommended = []

    # 策略1: 基于历史的协同过滤（权重40%）
    # 找到与用户历史商品一起出现过的其他商品
    for hist_item in valid_history[:3]:  # 考虑前3个历史商品
        # 在训练数据中找相似用户
        similar_users = train[train['target_iid'] == hist_item]['uid'].tolist()
        # 获取这些用户的目标商品
        related_items = train[train['uid'].isin(similar_users)]['target_iid'].tolist()
        related_items = [item for item in related_items if item in all_valid_items and item not in history_set]
        recommended.extend(related_items[:2])
        if len(set(recommended)) >= 4:
            break

    # 策略2: 训练热门商品（权重30%）
    for item in popular_in_train:
        if item not in history_set and item not in recommended:
            recommended.append(item)
        if len(recommended) >= 7:
            break

    # 策略3: 随机有效商品补充多样性（权重30%）
    for item in all_valid_list:
        if item not in history_set and item not in recommended:
            recommended.append(item)
        if len(recommended) >= 10:
            break

    predictions.append(','.join(recommended[:10]))

# 8. 分析推荐结果
print("\n【6】分析推荐结果...")
a2_improved = pd.DataFrame({
    'uid': test['uid'],
    'prediction': predictions
})

# 推荐多样性分析
all_items = []
a2_improved['prediction'].apply(lambda x: all_items.extend(x.split(',')))
unique_items = len(set(all_items))
item_coverage = Counter(all_items)

print(f"  推荐的不同商品数: {unique_items}")
print(f"  商品覆盖率: {unique_items / len(item_df) * 100:.1f}%")

# 多样性分布
print(f"\n  推荐商品分布:")
bins = [(0, 10), (10, 50), (50, 100), (100, 500), (500, 1000), (1000, len(a2_improved))]
for start, end in bins:
    count = sum(1 for c in item_coverage.values() if start <= c < end)
    pct = count / len(item_coverage) * 100
    bar = "█" * int(pct / 5)
    print(f"    {start:5d}-{end:5d}次: {count:3d}个商品 ({pct:5.1f}%) {bar}")

# Top商品
print(f"\n  Top 20推荐商品:")
top_items = item_coverage.most_common(20)
for i, (item, count) in enumerate(top_items, 1):
    pct = count / len(a2_improved) * 100
    in_train = "✓" if item in train_item_set else "✗"
    print(f"    {i:2d}. {item}: {count:5d}次 ({pct:5.1f}%) {in_train}")

# 9. 与训练数据对比
print("\n【7】与训练数据对比...")
recommended_items = set(all_items)
overlap = train_item_set & recommended_items
print(f"  推荐商品出现在训练数据: {len(overlap)}/{len(recommended_items)} ({len(overlap) / len(recommended_items) * 100:.1f}%)")

# 10. 保存结果
print("\n【8】保存改进的A2推荐...")
output_path = 'output/submission/A2_v3.csv'
a2_improved.to_csv(output_path, index=False)
print(f"  已保存: {output_path}")

# 11. 最终报告
print("\n" + "=" * 80)
print("改进A2推荐系统 - 完成报告")
print("=" * 80)

print(f"\n推荐策略:")
print(f"  1. 协同过滤推荐 (权重40%)")
print(f"  2. 训练热门商品 (权重30%)")
print(f"  3. 随机有效商品 (权重30%)")

print(f"\n关键改进:")
print(f"  ✅ 推荐多样性: {unique_items}个商品 (vs 之前19个)")
print(f"  ✅ 商品覆盖率: {unique_items / len(item_df) * 100:.1f}%")
print(f"  ✅ 与训练匹配: {len(overlap) / len(recommended_items) * 100:.1f}%")

# 多样性评估
diversity_score = unique_items / len(item_df)
if diversity_score < 0.05:
    print(f"  ⚠️ 多样性仍然较低")
elif diversity_score < 0.10:
    print(f"  ✅ 多样性中等")
else:
    print(f"  ✅ 多样性良好")

print("\n" + "=" * 80)