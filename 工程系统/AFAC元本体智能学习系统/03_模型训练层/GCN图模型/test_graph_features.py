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
edge_index = npz["edge_index"]
labels = npz["labels"]
train_mask = npz["train_mask"]
val_mask = npz["val_mask"]
test_mask = npz["test_mask"]

num_nodes = len(labels)

print("=== 构建图结构特征 ===")
degrees = np.bincount(edge_index[0], minlength=num_nodes).astype(np.float64)

two_hop_counts = np.zeros(num_nodes, dtype=np.float64)
for u in range(num_nodes):
    neighbors = set(edge_index[1, edge_index[0] == u])
    two_hop = set()
    for v in neighbors:
        two_hop.update(edge_index[1, edge_index[0] == v])
    two_hop_counts[u] = len(two_hop)

clustering_coeff = np.zeros(num_nodes, dtype=np.float64)
for u in range(num_nodes):
    neighbors = list(set(edge_index[1, edge_index[0] == u]))
    k = len(neighbors)
    if k >= 2:
        edges_between = 0
        for i in range(k):
            for j in range(i+1, k):
                if np.any((edge_index[0] == neighbors[i]) & (edge_index[1] == neighbors[j])):
                    edges_between += 1
        clustering_coeff[u] = 2 * edges_between / (k * (k - 1))

eigenvector_centrality = np.zeros(num_nodes, dtype=np.float64)
adj = np.zeros((num_nodes, num_nodes))
for i in range(edge_index.shape[1]):
    adj[edge_index[0, i], edge_index[1, i]] = 1
    adj[edge_index[1, i], edge_index[0, i]] = 1
eigvals, eigvecs = np.linalg.eig(adj)
max_eig_idx = np.argmax(eigvals)
eigenvector_centrality = np.abs(eigvecs[:, max_eig_idx].real)

graph_features = np.column_stack([
    degrees,
    two_hop_counts,
    clustering_coeff,
    eigenvector_centrality,
])

print(f"图结构特征维度: {graph_features.shape}")

print("\n=== 使用图结构特征训练 ===")
clf = LogisticRegression(max_iter=1000)
clf.fit(graph_features[train_mask], labels[train_mask])

train_acc = accuracy_score(labels[train_mask], clf.predict(graph_features[train_mask]))
val_acc = accuracy_score(labels[val_mask], clf.predict(graph_features[val_mask]))
test_acc = accuracy_score(labels[test_mask], clf.predict(graph_features[test_mask]))
print(f"训练准确率: {train_acc:.4f}")
print(f"验证准确率: {val_acc:.4f}")
print(f"测试准确率: {test_acc:.4f}")

print("\n=== 使用组合特征训练 ===")
combined_features = np.column_stack([features, graph_features])
clf2 = LogisticRegression(max_iter=1000)
clf2.fit(combined_features[train_mask], labels[train_mask])

train_acc2 = accuracy_score(labels[train_mask], clf2.predict(combined_features[train_mask]))
val_acc2 = accuracy_score(labels[val_mask], clf2.predict(combined_features[val_mask]))
test_acc2 = accuracy_score(labels[test_mask], clf2.predict(combined_features[test_mask]))
print(f"训练准确率: {train_acc2:.4f}")
print(f"验证准确率: {val_acc2:.4f}")
print(f"测试准确率: {test_acc2:.4f}")