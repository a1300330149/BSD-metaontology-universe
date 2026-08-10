import os
import sys
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

data_path = os.path.join(BASE, "data/afac2026_sparse_graph.npz")
npz = np.load(data_path)

features = npz["node_features"]
edge_index = npz["edge_index"]
labels = npz["labels"]
train_mask = npz["train_mask"]
val_mask = npz["val_mask"]
test_mask = npz["test_mask"]

num_nodes = len(labels)

print("=== 高级特征工程 ===")

print("\n1. PCA降维")
pca = PCA(n_components=32)
pca_features = pca.fit_transform(features)
print(f"PCA解释方差: {pca.explained_variance_ratio_.sum():.4f}")

print("\n2. KMeans聚类特征")
kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(features)
kmeans_features = kmeans.transform(features)

print("\n3. 图扩散特征")
diffusion_features = features.copy()
adj = np.zeros((num_nodes, num_nodes))
for i in range(edge_index.shape[1]):
    adj[edge_index[0, i], edge_index[1, i]] = 1
    adj[edge_index[1, i], edge_index[0, i]] = 1
deg = np.diag(np.sum(adj, axis=1).clip(min=1))
deg_inv = np.linalg.inv(deg)
normalized_adj = deg_inv @ adj

for _ in range(5):
    diffusion_features = 0.8 * diffusion_features + 0.2 * normalized_adj @ diffusion_features

print("\n4. 组合特征")
combined = np.column_stack([
    features,
    pca_features,
    kmeans_features,
    diffusion_features,
])
print(f"组合特征维度: {combined.shape}")

print("\n=== 随机森林 ===")
rf = RandomForestClassifier(n_estimators=200, max_depth=20, random_state=42)
rf.fit(combined[train_mask], labels[train_mask])
val_acc = accuracy_score(labels[val_mask], rf.predict(combined[val_mask]))
print(f"验证准确率: {val_acc:.4f}")

print("\n=== KNN ===")
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(combined[train_mask], labels[train_mask])
val_acc = accuracy_score(labels[val_mask], knn.predict(combined[val_mask]))
print(f"验证准确率: {val_acc:.4f}")

print("\n=== 仅使用训练集统计特征 ===")
train_features = features[train_mask]
train_labels = labels[train_mask]

class_means = np.zeros((10, features.shape[1]))
for c in range(10):
    class_means[c] = train_features[train_labels == c].mean(axis=0)

dist_to_class = np.zeros((num_nodes, 10))
for i in range(num_nodes):
    for c in range(10):
        dist_to_class[i, c] = np.linalg.norm(features[i] - class_means[c])

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(dist_to_class[train_mask], labels[train_mask])
val_acc = accuracy_score(labels[val_mask], clf.predict(dist_to_class[val_mask]))
print(f"验证准确率: {val_acc:.4f}")