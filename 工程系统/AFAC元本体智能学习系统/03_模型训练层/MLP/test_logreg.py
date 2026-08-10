import os
import sys
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

data_path = os.path.join(BASE, "data/afac2026_sparse_graph.npz")
npz = np.load(data_path)

features = npz["node_features"]
labels = npz["labels"]
train_mask = npz["train_mask"]
val_mask = npz["val_mask"]
test_mask = npz["test_mask"]

print("=== 逻辑回归 ===")
clf = LogisticRegression(max_iter=1000)
clf.fit(features[train_mask], labels[train_mask])

train_pred = clf.predict(features[train_mask])
val_pred = clf.predict(features[val_mask])
test_pred = clf.predict(features[test_mask])

print(f"训练准确率: {accuracy_score(labels[train_mask], train_pred):.4f}")
print(f"验证准确率: {accuracy_score(labels[val_mask], val_pred):.4f}")
print(f"测试准确率: {accuracy_score(labels[test_mask], test_pred):.4f}")

print("\n=== 特征重要性 ===")
importances = np.abs(clf.coef_).mean(axis=0)
top_features = np.argsort(importances)[-10:]
print(f"Top 10重要特征索引: {top_features}")
print(f"对应重要性值: {importances[top_features]}")

print("\n=== 使用重要特征训练 ===")
clf2 = LogisticRegression(max_iter=1000, multi_class='multinomial', solver='lbfgs')
clf2.fit(features[train_mask][:, top_features], labels[train_mask])
val_pred2 = clf2.predict(features[val_mask][:, top_features])
test_pred2 = clf2.predict(features[test_mask][:, top_features])
print(f"使用Top10特征验证准确率: {accuracy_score(labels[val_mask], val_pred2):.4f}")
print(f"使用Top10特征测试准确率: {accuracy_score(labels[test_mask], test_pred2):.4f}")