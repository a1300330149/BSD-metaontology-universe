import torch
import numpy as np
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from torch_geometric.utils import degree
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from src.utils.afac2026_data_loader import load_afac2026_real_data, create_train_val_split
from src.utils.data_utils import normalize_graph_features
from scipy.stats import entropy

print("=== 快速训练高质量模型 ===")

# 1. 加载数据
print("\n1. 加载数据...")
data = load_afac2026_real_data('../data/A分类/A1.npz')
data = create_train_val_split(data, val_ratio=0.2, seed=42)

data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.val_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.train_mask[data.train_idx] = True
data.val_mask[data.val_idx] = True

data = normalize_graph_features(data)

# 2. 添加图结构特征
print("\n2. 添加图结构特征...")
deg = degree(data.edge_index[0], data.num_nodes)
deg_log = torch.log(deg + 1).unsqueeze(1)
deg_norm = (deg / (deg.max() + 1e-8)).unsqueeze(1)
deg_sq = (deg ** 2).unsqueeze(1)
graph_features = torch.cat([deg_log, deg_norm, deg_sq], dim=1)
data.x = torch.cat([data.x, graph_features], dim=1)

# 3. 准备训练数据
print("\n3. 准备训练数据...")
train_idx = data.train_idx.numpy()
val_idx = data.val_idx.numpy()
test_idx = data.test_idx.numpy()

X_train = data.x[train_idx].numpy()
y_train = data.y[train_idx].numpy()
X_val = data.x[val_idx].numpy()
y_val = data.y[val_idx].numpy()
X_test = data.x[test_idx].numpy()

# 4. 训练随机森林
print("\n4. 训练随机森林...")
rf = RandomForestClassifier(
    n_estimators=300,
    max_depth=30,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight='balanced',
    n_jobs=-1,
    random_state=42
)
rf.fit(X_train, y_train)

train_pred = rf.predict(X_train)
val_pred = rf.predict(X_val)
train_acc = accuracy_score(y_train, train_pred)
val_acc = accuracy_score(y_val, val_pred)

print(f"训练准确率: {train_acc:.4f}")
print(f"验证准确率: {val_acc:.4f}")

# 5. 生成测试集预测
print("\n5. 生成测试集预测...")
test_pred = rf.predict(X_test)

print("预测标签分布:")
unique, counts = np.unique(test_pred, return_counts=True)
for label, count in zip(unique, counts):
    print(f"  标签{label}: {count}个 ({count/len(test_pred)*100:.2f}%)")

# 6. 保存结果
print("\n6. 保存结果...")
raw_data = np.load('../data/A分类/A1.npz')
real_test_idx = raw_data['test_idx']

submission = pd.DataFrame({
    'test_idx': real_test_idx,
    'label': test_pred
})

output_path = 'output/submission/A1_improved.csv'
submission.to_csv(output_path, index=False)
print(f"已保存: {output_path}")

# 7. 对比效果
print("\n7. 对比改进效果...")
old_a1 = pd.read_csv('output/submission/A1_fixed.csv')
old_counts = old_a1['label'].value_counts().sort_index()
new_counts = submission['label'].value_counts().sort_index()

print("旧模型预测分布:")
for label in range(10):
    count = old_counts.get(label, 0)
    print(f"  标签{label}: {count}个 ({count/len(old_a1)*100:.2f}%)")

print("\n新模型预测分布:")
for label in range(10):
    count = new_counts.get(label, 0)
    print(f"  标签{label}: {count}个 ({count/len(submission)*100:.2f}%)")

old_dist = old_counts.values / len(old_a1)
new_dist = new_counts.values / len(submission)
old_entropy = entropy(old_dist)
new_entropy = entropy(new_dist)
max_entropy = entropy(np.ones(10) / 10)

print(f"\n旧模型预测熵: {old_entropy:.4f} (随机性: {old_entropy/max_entropy*100:.2f}%)")
print(f"新模型预测熵: {new_entropy:.4f} (随机性: {new_entropy/max_entropy*100:.2f}%)")
print(f"\n预期评测准确率: {val_acc:.4f}")