import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("改进A2推荐系统 - 增加推荐多样性")
print("=" * 80)

# 1. 加载数据
print("\n【1】加载数据...")
train = pd.read_csv('../data/A推荐/train.csv')
test = pd.read_csv('../data/A推荐/test.csv')
item_df = pd.read_csv('../data/A推荐/item.csv')

print(f"  训练集用户数: {len(train)}")
print(f"  测试集用户数: {len(test)}")
print(f"  商品池大小: {len(item_df)}")

# 2. 分析训练数据
print("\n【2】分析训练数据...")
train_items = train['target_iid'].tolist()
item_counts = Counter(train_items)
print(f"  训练数据中出现过的商品数: {len(item_counts)}")

# 3. 构建用户-商品交互图
print("\n【3】构建用户-商品交互图...")
user_interactions = defaultdict(list)
for _, row in train.iterrows():
    uid = row['uid']
    target_item = row['target_iid']
    user_interactions[uid].append(target_item)

# 4. 构建商品共现矩阵（协同过滤基础）
print("\n【4】构建商品共现矩阵...")
co_occurrence = defaultdict(Counter)
for uid, items in user_interactions.items():
    unique_items = list(set(items))
    for i in range(len(unique_items)):
        for j in range(i + 1, len(unique_items)):
            item1, item2 = unique_items[i], unique_items[j]
            co_occurrence[item1][item2] += 1
            co_occurrence[item2][item1] += 1

print(f"  构建了{len(co_occurrence)}个商品的共现关系")

# 5. 生成改进的推荐
print("\n【5】生成改进的推荐...")
predictions = []

# 获取所有有效商品
all_valid_items = set(item_df['iid'].tolist())
valid_item_list = list(all_valid_items)

# 按流行度排序
popular_items = [item for item, count in item_counts.most_common()]
print(f"  热门商品Top 10: {popular_items[:10]}")

for idx, row in test.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = history_str.split(',') if history_str else []

    # 过滤历史中的有效商品
    valid_history = [item for item in history if item in all_valid_items]
    history_set = set(valid_history)

    recommended = []

    # 策略1: 基于协同过滤推荐相似商品（权重60%）
    related_items = Counter()
    for hist_item in valid_history[:5]:  # 考虑前5个历史商品
        if hist_item in co_occurrence:
            for related_item, count in co_occurrence[hist_item].most_common(10):
                if related_item not in history_set:
                    related_items[related_item] += count

    # 添加最相关的商品
    for item, score in related_items.most_common(6):
        if item not in history_set and item not in recommended:
            recommended.append(item)

    # 策略2: 添加用户历史中热门但未交互的商品（权重20%）
    history_popular = [item for item in valid_history if item in popular_items[:50]]
    for item in history_popular[:2]:
        if item not in history_set and item not in recommended:
            recommended.append(item)

    # 策略3: 添加全局热门但未被推荐的商品（权重20%）
    for item in popular_items:
        if item not in history_set and item not in recommended:
            recommended.append(item)
        if len(recommended) >= 10:
            break

    # 确保有10个推荐
    while len(recommended) < 10:
        for item in valid_item_list:
            if item not in recommended:
                recommended.append(item)
            if len(recommended) >= 10:
                break

    predictions.append(','.join(recommended[:10]))

# 6. 分析推荐结果
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

# Top商品分布
print(f"\n  推荐热门度分布:")
top_items = item_coverage.most_common(10)
max_count = top_items[0][1]
for item, count in top_items:
    pct = count / len(a2_improved) * 100
    bar_len = int(pct / 2)
    bar = "█" * bar_len
    print(f"    {item}: {count:5d}次 ({pct:5.1f}%) {bar}")

# 多样性评估
print(f"\n  多样性评估:")
if unique_items < 50:
    print(f"    ⚠️ 多样性仍然较低 ({unique_items}个商品)")
elif unique_items < 100:
    print(f"    ✅ 多样性中等 ({unique_items}个商品)")
else:
    print(f"    ✅ 多样性良好 ({unique_items}个商品)")

# 7. 与训练数据对比
print("\n【7】与训练数据对比...")
trained_items = set(train_items)
recommended_items = set(all_items)
overlap = trained_items & recommended_items
print(f"  推荐商品出现在训练数据的比例: {len(overlap) / len(recommended_items) * 100:.1f}%")

# 8. 保存结果
print("\n【8】保存改进的A2推荐...")
output_path = 'output/submission/A2_v2.csv'
a2_improved.to_csv(output_path, index=False)
print(f"  已保存: {output_path}")

# 9. 最终报告
print("\n" + "=" * 80)
print("改进A2推荐系统 - 完成报告")
print("=" * 80)
print(f"\n推荐策略:")
print(f"  1. 协同过滤推荐相似商品 (权重60%)")
print(f"  2. 用户历史热门商品 (权重20%)")
print(f"  3. 全局热门商品补充 (权重20%)")

print(f"\n关键指标:")
print(f"  推荐多样性: {unique_items}个商品")
print(f"  商品覆盖率: {unique_items / len(item_df) * 100:.1f}%")
print(f"  与训练数据匹配: {len(overlap) / len(recommended_items) * 100:.1f}%")

print(f"\nTop 10推荐商品:")
for i, (item, count) in enumerate(top_items[:10], 1):
    pct = count / len(a2_improved) * 100
    print(f"  {i:2d}. {item}: {pct:5.1f}%")

print("\n" + "=" * 80)