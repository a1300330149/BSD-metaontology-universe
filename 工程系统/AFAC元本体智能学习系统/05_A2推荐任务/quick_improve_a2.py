import pandas as pd
from collections import Counter

print("=== 快速生成改进的A2推荐 ===")

# 读取数据
train = pd.read_csv('../data/A推荐/train.csv')
test = pd.read_csv('../data/A推荐/test.csv')

# 分析训练数据中的热门商品
print("分析训练数据热门商品...")
train_items = train['target_iid'].tolist()
train_item_counts = Counter(train_items)
popular_items = [item for item, count in train_item_counts.most_common(50)]

print(f"训练数据总商品数: {len(train_item_counts)}")
print(f"前50个热门商品覆盖率: {sum(count for item, count in train_item_counts.most_common(50)) / len(train) * 100:.1f}%")

# 生成基于流行度的推荐
print("生成改进推荐...")
improved_predictions = []

for _, row in test.iterrows():
    uid = row['uid']
    history_str = row['item_seq_dedup'] if pd.notna(row['item_seq_dedup']) else ''
    history = history_str.split(',') if history_str else []

    # 基于流行度推荐，排除历史商品
    recommended = []
    for item in popular_items:
        if item not in history:
            recommended.append(item)
        if len(recommended) >= 10:
            break

    # 如果不够10个，补充其他热门商品
    if len(recommended) < 10:
        for item in list(train_item_counts.keys()):
            if item not in history and item not in recommended:
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
print(f"已保存: {output_path}")

# 分析改进后的推荐
all_items_improved = []
improved_a2['prediction'].apply(lambda x: all_items_improved.extend(x.split(',')))
unique_items_improved = len(set(all_items_improved))

print(f"\n改进后推荐分析:")
print(f"推荐的不同商品数: {unique_items_improved}")
print(f"推荐商品中出现在训练数据中的比例: {len(set(all_items_improved) & set(train_items)) / len(set(all_items_improved)) * 100:.1f}%")

item_counts_improved = Counter(all_items_improved)
print(f"\n改进后热门推荐商品:")
for item, count in item_counts_improved.most_common(5):
    print(f"   {item}: {count}次 ({count/len(improved_a2)*100:.1f}%)")