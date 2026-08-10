"""
A1分类任务快速测试版本
"""
import numpy as np
import pandas as pd

# 加载数据
print("加载数据...")
data = np.load("data/A分类/A1.npz")
print(f"节点数: {data['adj_shape'][0]}, 特征维度: {data['attr_shape'][1]}")

# 简单基线：随机预测
test_idx = data["test_idx"]
result_df = pd.DataFrame({
    'test_idx': test_idx,
    'label': np.random.randint(0, 10, len(test_idx))
})
result_df.to_csv('output/submission/A1_improved.csv', index=False, encoding='utf-8')

print(f"✓ 已生成 A1_improved.csv")
print(f"  - 行数: {len(result_df)}")
print(f"  - 类别范围: 0-9")