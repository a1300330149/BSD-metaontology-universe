import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from scipy.sparse import csr_matrix
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("改进A1分类模型 - 解决标签4过度预测问题")
print("=" * 80)

# 1. 加载数据
print("\n【1】加载数据...")
data = np.load("data/A分类/A1.npz", allow_pickle=True)

# 重构特征矩阵
print("  重构特征矩阵...")
attr_data = data['attr_data']
attr_indices = data['attr_indices']
attr_indptr = data['attr_indptr']
attr_shape = data['attr_shape']
features = csr_matrix((attr_data, attr_indices, attr_indptr), shape=attr_shape).toarray()

labels = data['labels']
train_idx = data['train_idx']
test_idx = data['test_idx']

print(f"  特征矩阵形状: {features.shape}")
print(f"  训练节点数: {len(train_idx)}")
print(f"  测试节点数: {len(test_idx)}")
print(f"  类别数: {len(np.unique(labels))}")

# 2. 分析训练数据分布
print("\n【2】训练数据标签分布分析...")
train_labels = labels[train_idx]
label_counts = Counter(train_labels)
print("  训练数据标签分布:")
for label in sorted(label_counts.keys()):
    count = label_counts[label]
    pct = count / len(train_labels) * 100
    print(f"    标签{label}: {count:5d} ({pct:5.1f}%)")

# 3. 计算平衡的类别权重
print("\n【3】计算平衡的类别权重...")
total_samples = len(train_labels)
n_classes = len(label_counts)

# 使用inverse频率权重，但限制最大/最小比率
class_weights = {}
max_count = max(label_counts.values())
min_count = min(label_counts.values())
max_ratio = min(max_count / min_count, 10)  # 限制最大比率为10

for label in label_counts:
    count = label_counts[label]
    # 权重 = 总样本 / (类别数 * 该类别样本数)，但限制比率
    weight = total_samples / (n_classes * count)
    # 限制权重范围
    weight = min(weight, max_ratio)
    weight = max(weight, 1.0 / max_ratio)
    class_weights[label] = weight

print("  平衡后的类别权重:")
for label in sorted(class_weights.keys()):
    weight = class_weights[label]
    indicator = "↑" if weight > 1 else "↓"
    print(f"    标签{label}: {weight:.4f} {indicator}")

# 4. 准备训练数据
print("\n【4】准备训练数据...")
X_train = features[train_idx]
y_train = labels[train_idx]
X_test = features[test_idx]

# 添加图结构特征
print("  添加图结构特征...")
adj_data = data['adj_data']
adj_indices = data['adj_indices']
adj_indptr = data['adj_indptr']
adj_shape = data['adj_shape']

# 计算节点度特征
n_nodes = adj_shape[0]
degrees = np.zeros(n_nodes)
for i in range(len(adj_indptr) - 1):
    start, end = adj_indptr[i], adj_indptr[i + 1]
    degrees[i] = end - start

# 为训练集和测试集添加度特征
degree_train = degrees[train_idx]
degree_test = degrees[test_idx]

# 度特征归一化
degree_mean = degree_train.mean()
degree_std = degree_train.std() + 1e-8
degree_train_norm = (degree_train - degree_mean) / degree_std
degree_test_norm = (degree_test - degree_mean) / degree_std

# 添加度特征
X_train_enhanced = np.column_stack([X_train, degree_train_norm, np.log1p(degree_train)])
X_test_enhanced = np.column_stack([X_test, degree_test_norm, np.log1p(degree_test)])

print(f"  增强后特征维度: {X_train_enhanced.shape[1]}")

# 5. 训练改进的模型
print("\n【5】训练改进的随机森林模型...")

# 使用平衡的类别权重
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight=class_weights,  # 使用平衡权重
    random_state=42,
    n_jobs=-1,
    verbose=0
)

model.fit(X_train_enhanced, y_train)

# 6. 验证模型性能
print("\n【6】验证模型性能...")
y_pred_train = model.predict(X_train_enhanced)
train_acc = accuracy_score(y_train, y_pred_train)
print(f"  训练准确率: {train_acc:.4f}")

# 内部验证集
X_tr, X_val, y_tr, y_val = train_test_split(
    X_train_enhanced, y_train, test_size=0.2, random_state=42, stratify=y_train
)
model_val = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    class_weight=class_weights,
    random_state=42,
    n_jobs=-1
)
model_val.fit(X_tr, y_tr)
y_pred_val = model_val.predict(X_val)
val_acc = accuracy_score(y_val, y_pred_val)
print(f"  验证准确率: {val_acc:.4f}")

# 7. 分析预测分布
print("\n【7】预测分布分析...")
y_pred_test = model.predict(X_test_enhanced)
pred_dist = Counter(y_pred_test)

print("  预测标签分布:")
for label in range(10):
    count = pred_dist.get(label, 0)
    pct = count / len(test_idx) * 100
    train_pct = label_counts[label] / len(train_labels) * 100
    diff = pct - train_pct
    bar = "█" * int(abs(diff) / 2)
    indicator = "↑" if diff > 0 else "↓"
    print(f"    标签{label}: {count:5d} ({pct:5.1f}%) vs 训练({train_pct:5.1f}%) {indicator}{abs(diff):5.1f}%")

# 8. 评估分布偏差
print("\n【8】分布偏差评估...")
train_dist = np.array([label_counts[i] / len(train_labels) for i in range(10)])
pred_dist_arr = np.array([pred_dist.get(i, 0) / len(test_idx) for i in range(10)])
kl_divergence = np.sum(train_dist * np.log(train_dist / (pred_dist_arr + 1e-10) + 1e-10))
print(f"  KL散度 (预测 vs 训练): {kl_divergence:.4f}")

if kl_divergence < 0.5:
    print("  ✅ 分布偏差较小，模型预测合理")
elif kl_divergence < 1.0:
    print("  ⚠️ 分布偏差中等")
else:
    print("  ❌ 分布偏差较大，需要进一步调整")

# 9. 保存结果
print("\n【9】保存改进的A1预测...")
a1_improved = pd.DataFrame({
    'test_idx': test_idx,
    'label': y_pred_test
})

output_path = "output/submission/A1_v2.csv"
a1_improved.to_csv(output_path, index=False)
print(f"  已保存: {output_path}")

# 10. 详细报告
print("\n" + "=" * 80)
print("改进A1分类模型 - 完成报告")
print("=" * 80)
print(f"\n训练准确率: {train_acc:.4f}")
print(f"验证准确率: {val_acc:.4f}")
print(f"KL散度: {kl_divergence:.4f}")
print(f"\n预测分布与训练分布对比:")
for label in range(10):
    train_pct = label_counts[label] / len(train_labels) * 100
    pred_pct = pred_dist.get(label, 0) / len(test_idx) * 100
    diff = pred_pct - train_pct
    status = "✅" if abs(diff) < 5 else "⚠️"
    print(f"  {status} 标签{label}: 预测{pred_pct:5.1f}% vs 训练{train_pct:5.1f}% (差{diff:+5.1f}%)")

print("\n" + "=" * 80)