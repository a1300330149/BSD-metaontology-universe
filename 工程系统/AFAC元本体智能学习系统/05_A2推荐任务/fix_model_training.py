import torch
import numpy as np
import pandas as pd
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from torch_geometric.data import Data
from torch_geometric.utils import degree
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from src.utils.afac2026_data_loader import load_afac2026_real_data, create_train_val_split
from src.utils.data_utils import normalize_graph_features

print("=== 重新训练高质量模型 ===")

# 1. 加载数据
print("\n1. 加载数据...")
data = load_afac2026_real_data('../data/A分类/A1.npz')
data = create_train_val_split(data, val_ratio=0.2, seed=42)

# 创建mask
data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.val_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
data.train_mask[data.train_idx] = True
data.val_mask[data.val_idx] = True

# 归一化特征
data = normalize_graph_features(data)

print(f"节点数: {data.num_nodes}")
print(f"特征维度: {data.x.shape[1]}")
print(f"训练节点数: {data.train_idx.shape[0]}")
print(f"验证节点数: {data.val_idx.shape[0]}")
print(f"测试节点数: {data.test_idx.shape[0]}")

# 2. 添加图结构特征
print("\n2. 添加图结构特征...")
deg = degree(data.edge_index[0], data.num_nodes)
deg_norm = deg / (deg.max() + 1e-8)
deg_log = torch.log(deg + 1).unsqueeze(1)
deg_norm = deg_norm.unsqueeze(1)
deg_sq = (deg ** 2).unsqueeze(1)

# 添加度特征
graph_features = torch.cat([deg_log, deg_norm, deg_sq], dim=1)
data.x = torch.cat([data.x, graph_features], dim=1)

print(f"增强后特征维度: {data.x.shape[1]}")

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

print(f"训练集大小: {X_train.shape}")
print(f"验证集大小: {X_val.shape}")
print(f"测试集大小: {X_test.shape}")

# 4. 处理类别不平衡
print("\n4. 处理类别不平衡...")
print("原始标签分布:")
unique, counts = np.unique(y_train, return_counts=True)
for label, count in zip(unique, counts):
    print(f"  标签{label}: {count}个 ({count/len(y_train)*100:.2f}%)")

print("使用class_weight='balanced'处理类别不平衡")

# 5. 训练多个模型
print("\n5. 训练多个模型...")

models = {
    "逻辑回归": LogisticRegression(max_iter=1000, n_jobs=-1, class_weight='balanced'),
    "随机森林": RandomForestClassifier(n_estimators=200, max_depth=20, n_jobs=-1, class_weight='balanced', random_state=42),
    "梯度提升": GradientBoostingClassifier(n_estimators=100, max_depth=10, random_state=42)
}

results = {}
for name, model in models.items():
    print(f"\n训练{name}...")
    model.fit(X_train, y_train)
    
    train_pred = model.predict(X_train)
    val_pred = model.predict(X_val)
    
    train_acc = accuracy_score(y_train, train_pred)
    val_acc = accuracy_score(y_val, val_pred)
    
    results[name] = {
        'model': model,
        'train_acc': train_acc,
        'val_acc': val_acc,
        'val_pred': val_pred
    }
    
    print(f"  训练准确率: {train_acc:.4f}")
    print(f"  验证准确率: {val_acc:.4f}")

# 6. 选择最佳模型
print("\n6. 选择最佳模型...")
best_model_name = max(results.keys(), key=lambda k: results[k]['val_acc'])
best_model = results[best_model_name]['model']
best_val_acc = results[best_model_name]['val_acc']

print(f"最佳模型: {best_model_name}")
print(f"最佳验证准确率: {best_val_acc:.4f}")

# 7. 生成测试集预测
print("\n7. 生成测试集预测...")
test_pred = best_model.predict(X_test)
test_proba = best_model.predict_proba(X_test)

print(f"预测标签分布:")
unique, counts = np.unique(test_pred, return_counts=True)
for label, count in zip(unique, counts):
    print(f"  标签{label}: {count}个 ({count/len(test_pred)*100:.2f}%)")

# 8. 保存结果
print("\n8. 保存结果...")
# 读取真实的test_idx
raw_data = np.load('../data/A分类/A1.npz')
real_test_idx = raw_data['test_idx']

# 创建提交文件
submission = pd.DataFrame({
    'test_idx': real_test_idx,
    'label': test_pred
})

# 保存A1.csv
output_path = 'output/submission/A1_improved.csv'
submission.to_csv(output_path, index=False)
print(f"已保存改进的A1.csv: {output_path}")

# 9. 验证格式
print("\n9. 验证格式...")
sample = pd.read_csv('../data/A分类/sample_submission.csv')
print(f"sample_submission.csv行数: {len(sample)}")
print(f"A1_improved.csv行数: {len(submission)}")
print(f"test_idx顺序一致: {(sample['test_idx'].values == real_test_idx).all()}")

# 10. 对比改进效果
print("\n10. 对比改进效果...")
old_a1 = pd.read_csv('output/submission/A1_fixed.csv')
print(f"旧模型预测分布:")
old_counts = old_a1['label'].value_counts().sort_index()
for label, count in old_counts.items():
    print(f"  标签{label}: {count}个 ({count/len(old_a1)*100:.2f}%)")

print(f"\n新模型预测分布:")
new_counts = submission['label'].value_counts().sort_index()
for label, count in new_counts.items():
    print(f"  标签{label}: {count}个 ({count/len(submission)*100:.2f}%)")

# 计算预测熵
from scipy.stats import entropy
old_dist = old_counts.values / len(old_a1)
new_dist = new_counts.values / len(submission)
old_entropy = entropy(old_dist)
new_entropy = entropy(new_dist)
max_entropy = entropy(np.ones(10) / 10)

print(f"\n旧模型预测熵: {old_entropy:.4f} (随机性: {old_entropy/max_entropy*100:.2f}%)")
print(f"新模型预测熵: {new_entropy:.4f} (随机性: {new_entropy/max_entropy*100:.2f}%)")
print(f"预期准确率提升: {(max_entropy - new_entropy) / (max_entropy - old_entropy) * 100:.2f}%")

print("\n=== 完成 ===")
print(f"预期评测准确率: {best_val_acc:.4f}")
print(f"改进后的A1.csv已保存到: {output_path}")