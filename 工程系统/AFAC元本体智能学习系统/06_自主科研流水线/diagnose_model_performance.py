import torch
import numpy as np
import pandas as pd
from torch_geometric.data import Data
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from src.utils.afac2026_data_loader import load_afac2026_real_data, create_train_val_split
from src.utils.data_utils import normalize_graph_features

print("=== 深度诊断模型性能下降原因 ===")

# 1. 加载原始数据
print("\n1. 加载原始AFAC2026数据...")
data = load_afac2026_real_data('data/A分类/A1.npz')
print(f"节点数: {data.num_nodes}")
print(f"边数: {data.edge_index.shape[1]}")
print(f"特征维度: {data.x.shape[1]}")
print(f"类别数: {data.y.max().item() + 1}")
print(f"训练节点数: {data.train_idx.shape[0]}")
print(f"测试节点数: {data.test_idx.shape[0]}")

# 2. 检查数据质量
print("\n2. 检查数据质量...")
print(f"特征矩阵中NaN数量: {torch.isnan(data.x).sum().item()}")
print(f"特征矩阵中Inf数量: {torch.isinf(data.x).sum().item()}")
print(f"特征值范围: [{data.x.min().item():.4f}, {data.x.max().item():.4f}]")
print(f"特征值均值: {data.x.mean().item():.4f}")
print(f"特征值标准差: {data.x.std().item():.4f}")

# 3. 检查标签分布
print("\n3. 检查标签分布...")
train_labels = data.y[data.train_idx].numpy()
unique, counts = np.unique(train_labels, return_counts=True)
print("训练集标签分布:")
for label, count in zip(unique, counts):
    print(f"  标签{label}: {count}个 ({count/len(train_labels)*100:.2f}%)")

# 4. 检查图结构
print("\n4. 检查图结构...")
from torch_geometric.utils import degree
deg = degree(data.edge_index[0], data.num_nodes)
print(f"平均度: {deg.mean().item():.2f}")
print(f"最大度: {deg.max().item()}")
print(f"度分布标准差: {deg.std().item():.2f}")
print(f"孤立节点数: {(deg == 0).sum().item()}")

# 5. 检查训练/测试节点分布
print("\n5. 检查训练/测试节点分布...")
train_deg = deg[data.train_idx]
test_deg = deg[data.test_idx]
print(f"训练节点平均度: {train_deg.mean().item():.2f}")
print(f"测试节点平均度: {test_deg.mean().item():.2f}")
print(f"度分布差异: {abs(train_deg.mean() - test_deg.mean()).item():.2f}")

# 6. 测试简单基线模型
print("\n6. 测试简单基线模型（逻辑回归）...")
# 创建训练验证划分
data_split = create_train_val_split(data.clone(), val_ratio=0.2, seed=42)

# 获取训练和验证节点
train_idx = data_split.train_idx.numpy()
val_idx = data_split.val_idx.numpy()

# 训练逻辑回归
X_train = data_split.x[train_idx].numpy()
y_train = data_split.y[train_idx].numpy()
X_val = data_split.x[val_idx].numpy()
y_val = data_split.y[val_idx].numpy()

lr = LogisticRegression(max_iter=1000, n_jobs=-1)
lr.fit(X_train, y_train)
train_pred = lr.predict(X_train)
val_pred = lr.predict(X_val)

train_acc = accuracy_score(y_train, train_pred)
val_acc = accuracy_score(y_val, val_pred)

print(f"逻辑回归训练准确率: {train_acc:.4f}")
print(f"逻辑回归验证准确率: {val_acc:.4f}")

# 7. 分析特征重要性
print("\n7. 分析特征重要性...")
if hasattr(lr, 'coef_'):
    feature_importance = np.abs(lr.coef_).mean(axis=0)
    top_features = np.argsort(feature_importance)[-10:][::-1]
    print(f"最重要的10个特征索引: {top_features}")
    print(f"对应重要性值: {feature_importance[top_features]}")

# 8. 检查当前A1.csv的预测质量
print("\n8. 检查当前A1.csv的预测质量...")
a1 = pd.read_csv('Agent_v2/output/submission/A1_fixed.csv')
print(f"A1.csv行数: {len(a1)}")

# 检查预测分布
label_counts = a1['label'].value_counts().sort_index()
print("预测标签分布:")
for label, count in label_counts.items():
    print(f"  标签{label}: {count}个 ({count/len(a1)*100:.2f}%)")

# 计算熵（衡量预测的随机性）
from scipy.stats import entropy
pred_dist = label_counts.values / len(a1)
pred_entropy = entropy(pred_dist)
max_entropy = entropy(np.ones(10) / 10)
print(f"\n预测熵: {pred_entropy:.4f}")
print(f"最大熵（完全随机）: {max_entropy:.4f}")
print(f"随机性比例: {pred_entropy/max_entropy*100:.2f}%")

# 9. 诊断结论
print("\n=== 诊断结论 ===")
if val_acc < 0.2:
    print("❌ 严重问题: 逻辑回归基线准确率很低，说明特征质量差或任务很难")
elif val_acc < 0.4:
    print("⚠️ 中等问题: 逻辑回归基线准确率一般，需要更强的模型")
else:
    print("✅ 基线正常: 逻辑回归基线准确率尚可，问题可能在模型训练")

if pred_entropy > max_entropy * 0.9:
    print("❌ 严重问题: 模型预测几乎是随机的，模型没有学到任何模式")
elif pred_entropy > max_entropy * 0.7:
    print("⚠️ 中等问题: 模型预测随机性较高，模型学到的信息有限")
else:
    print("✅ 预测正常: 模型学到了一定的模式")

print("\n可能的根本原因:")
print("1. 数据预处理问题（特征归一化、缺失值处理等）")
print("2. 模型架构不适合这个任务")
print("3. 超参数设置不当（学习率、正则化等）")
print("4. 训练过程问题（梯度消失、过拟合等）")
print("5. 图神经网络的消息传递机制有问题")

# 10. 建议
print("\n=== 改进建议 ===")
print("1. 使用更强的基线模型（如RandomForest、XGBoost）")
print("2. 检查并优化数据预处理流程")
print("3. 尝试不同的模型架构（GCN、GAT、GraphSAGE等）")
print("4. 调整超参数（学习率、隐藏层维度、dropout等）")
print("5. 增加训练轮数，使用早停机制")
print("6. 添加数据增强和正则化技术")