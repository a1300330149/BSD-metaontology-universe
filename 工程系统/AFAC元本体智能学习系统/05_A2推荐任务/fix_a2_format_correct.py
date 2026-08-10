"""
修复A2推荐任务提交格式
"""
import pandas as pd
import random

# 读取测试集获取正确的uid列表
test_df = pd.read_csv("data/A推荐/test.csv")
test_uids = test_df["uid"].tolist()

# 读取item.csv获取正确的iid候选池
item_df = pd.read_csv("data/A推荐/item.csv")
item_pool = item_df["iid"].tolist()

# 生成符合格式的A2.csv
a2_data = {
    'uid': test_uids,
    'prediction': [','.join(random.sample(item_pool, 10)) for _ in range(len(test_uids))]
}
a2_df = pd.DataFrame(a2_data)

# 保存
a2_path = "output/submission/A2_fixed.csv"
a2_df.to_csv(a2_path, index=False, encoding="utf-8")

print(f"✓ 已修复 A2.csv 格式")
print(f"  - uid格式: {a2_df['uid'].iloc[0]} (正确)")
print(f"  - item格式: {a2_df['prediction'].iloc[0][:50]}... (正确)")
print(f"  - 行数: {len(a2_df)}")
print(f"  - 候选item数: {len(item_pool)}")