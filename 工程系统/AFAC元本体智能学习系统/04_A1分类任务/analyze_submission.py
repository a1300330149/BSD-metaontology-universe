"""分析提交文件"""
import pandas as pd
from collections import Counter

# A1分析
a1 = pd.read_csv('output/submission/A1.csv')
print('=== A1分类分析 ===')
print(f'总行数: {len(a1)}')
print(f'标签分布:')
print(a1['label'].value_counts().sort_index())

# A2分析
a2 = pd.read_csv('output/submission/A2.csv')
all_items = []
a2['prediction'].apply(lambda x: all_items.extend(x.split(',')))

print('\n=== A2推荐分析 ===')
print(f'总用户数: {len(a2)}')
print(f'推荐商品总数: {len(all_items)}')
print(f'不同商品数: {len(set(all_items))}')
print(f'商品覆盖率: {len(set(all_items))/2156*100:.1f}%')

item_counts = Counter(all_items)
print(f'\nTop 10推荐商品:')
for item, count in item_counts.most_common(10):
    print(f'  {item}: {count}次 ({count/len(a2)*100:.1f}%)')

# 检查训练数据中的热门商品
train = pd.read_csv('data/A推荐/train.csv')
train_items = train['target_iid'].tolist()
train_counts = Counter(train_items)

print(f'\n=== 训练数据热门商品 ===')
print(f'训练目标商品数: {len(train_counts)}')
for item, count in train_counts.most_common(10):
    print(f'  {item}: {count}次 ({count/len(train)*100:.1f}%)')

# 检查推荐商品与训练商品的匹配
overlap = set(all_items) & set(train_items)
print(f'\n推荐商品在训练数据中: {len(overlap)}/{len(set(all_items))} ({len(overlap)/len(set(all_items))*100:.1f}%)')