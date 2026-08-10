import os
import sys
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

data_path = os.path.join(BASE, "data/afac2026_sparse_graph.npz")
npz = np.load(data_path)

edge_index = npz["edge_index"]
labels = npz["labels"]

print("=== 图结构分析 ===")
num_nodes = len(labels)
num_edges = edge_index.shape[1]
print(f"节点数: {num_nodes}, 边数: {num_edges}")

print("\n=== 同类别边比例 ===")
same_class_edges = 0
for i in range(num_edges):
    u = edge_index[0, i]
    v = edge_index[1, i]
    if labels[u] == labels[v]:
        same_class_edges += 1
print(f"同类别边数: {same_class_edges} ({same_class_edges/num_edges*100:.2f}%)")

print("\n=== 类别内聚程度 ===")
for c in range(10):
    class_nodes = np.where(labels == c)[0]
    class_size = len(class_nodes)
    class_edge_count = 0
    for i in range(num_edges):
        u, v = edge_index[0, i], edge_index[1, i]
        if labels[u] == c and labels[v] == c:
            class_edge_count += 1
    density = class_edge_count / (class_size * (class_size - 1) / 2) if class_size > 1 else 0
    print(f"类别 {c}: 节点数={class_size}, 内部边数={class_edge_count}, 密度={density:.4f}")

print("\n=== 邻居类别分布 ===")
for c in range(10):
    class_nodes = np.where(labels == c)[0]
    neighbor_classes = []
    for u in class_nodes:
        neighbors = edge_index[1, edge_index[0] == u]
        neighbor_classes.extend(labels[neighbors].tolist())
    if neighbor_classes:
        unique, counts = np.unique(neighbor_classes, return_counts=True)
        total = len(neighbor_classes)
        print(f"类别 {c} 的邻居类别分布:")
        for cls, cnt in zip(unique, counts):
            print(f"  -> 类别 {cls}: {cnt} ({cnt/total*100:.1f}%)")
    print()

print("\n=== 度分布 ===")
degrees = np.bincount(edge_index[0])
print(f"平均度数: {degrees.mean():.2f}")
print(f"度数中位数: {np.median(degrees):.2f}")
print(f"度数标准差: {degrees.std():.2f}")

print("\n=== 度-类别相关性 ===")
for c in range(10):
    class_degrees = degrees[labels == c]
    print(f"类别 {c}: 平均度数={class_degrees.mean():.2f}")