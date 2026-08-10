"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：稀疏补偿α=0.18
"""

import numpy as np
import scipy.sparse as sp
from scipy.sparse import csr_matrix
import torch
from torch_geometric.data import Data
import torch_geometric.transforms as T

def load_afac2026_real_data(file_path):
    """
    加载AFAC2026真实数据集

    Args:
        file_path: .npz文件路径

    Returns:
        PyG Data对象，包含x, edge_index, y, train_idx, test_idx
    """
    print(f"=== 加载AFAC2026真实数据: {file_path} ===")
    data = np.load(file_path)

    # 重建邻接矩阵
    adj = csr_matrix(
        (data["adj_data"], data["adj_indices"], data["adj_indptr"]),
        shape=tuple(data["adj_shape"]),
    )

    # 重建特征矩阵
    features = csr_matrix(
        (data["attr_data"], data["attr_indices"], data["attr_indptr"]),
        shape=tuple(data["attr_shape"]),
    )

    labels = data["labels"]
    train_idx = data["train_idx"]
    test_idx = data["test_idx"]

    print(f"节点数: {adj.shape[0]}")
    print(f"特征维度: {features.shape[1]}")
    print(f"类别数: {len(np.unique(labels[train_idx]))}")
    print(f"训练节点数: {len(train_idx)}")
    print(f"测试节点数: {len(test_idx)}")

    # 转换为PyTorch Geometric格式
    edge_index, edge_attr = _from_scipy_sparse_matrix(adj)

    # 转换特征为稠密张量
    features_dense = features.toarray().astype(np.float32)
    x = torch.from_numpy(features_dense)

    # 创建PyG数据对象
    pyg_data = Data(
        x=x,
        edge_index=edge_index,
        edge_attr=edge_attr,
        y=torch.from_numpy(labels).long(),
        train_idx=torch.from_numpy(train_idx).long(),
        test_idx=torch.from_numpy(test_idx).long(),
    )

    print(f"PyG数据对象: {pyg_data}")
    return pyg_data

def _from_scipy_sparse_matrix(sparse_matrix):
    """将scipy稀疏矩阵转换为PyG edge_index和edge_attr"""
    sparse_matrix = sparse_matrix.tocoo()
    row = torch.from_numpy(sparse_matrix.row).to(torch.long)
    col = torch.from_numpy(sparse_matrix.col).to(torch.long)
    edge_index = torch.stack([row, col], dim=0)

    edge_weight = torch.from_numpy(sparse_matrix.data).to(torch.float)

    return edge_index, edge_weight

def normalize_graph_features(data):
    """归一化节点特征"""
    x = data.x
    x_mean = x.mean(dim=0, keepdim=True)
    x_std = x.std(dim=0, keepdim=True) + 1e-8
    data.x = (x - x_mean) / x_std
    return data

def create_train_val_split(data, val_ratio=0.2, seed=42):
    """
    从训练集中划分验证集

    Args:
        data: PyG Data对象
        val_ratio: 验证集比例
        seed: 随机种子

    Returns:
        添加val_idx的Data对象
    """
    np.random.seed(seed)
    train_idx = data.train_idx.numpy()
    num_train = len(train_idx)
    num_val = int(num_train * val_ratio)

    perm = np.random.permutation(num_train)
    val_idx = train_idx[perm[:num_val]]
    new_train_idx = train_idx[perm[num_val:]]

    data.train_idx = torch.from_numpy(new_train_idx).long()
    data.val_idx = torch.from_numpy(val_idx).long()

    print(f"训练集: {len(new_train_idx)} 样本")
    print(f"验证集: {len(val_idx)} 样本")
    print(f"测试集: {len(data.test_idx)} 样本")

    return data

if __name__ == "__main__":
    # 测试数据加载
    data_path = "./data/A分类/A1.npz"
    data = load_afac2026_real_data(data_path)
    data = normalize_graph_features(data)
    data = create_train_val_split(data)

    print(f"\n最终数据对象: {data}")
    print(f"特征形状: {data.x.shape}")
    print(f"边数: {data.edge_index.shape[1]}")