# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然/肉身能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：γ=0.92, 边缘丢弃率0.02, 特征丢弃率0.05
"""

import torch
import numpy as np
from torch_geometric.data import Data
from torch_geometric.utils import degree, to_scipy_sparse_matrix, k_hop_subgraph
from torch_geometric.transforms import GDC
from src.utils.data_utils import load_afac_sparse_graph, normalize_graph_features
from src.utils.afac2026_data_loader import load_afac2026_real_data, create_train_val_split
import scipy.sparse as sp

class DataPreprocessAgent:
    """
    功能：图数据预处理与特征增强
    理论映射：2重自然秩序基底·实体数据处理规则
    能级关联：肉身能级e_body更新
    约束来源：科研动力学公理
    """
    def __init__(self):
        self.enable_debias = False
        self.debias_strength = 0.3
        self.edge_dropout = 0.02
        self.feature_dropout = 0.05
        self.label_smoothing = 0.1
        self.enable_feature_enhance = True
        self.data_type = "synthetic"  # "synthetic" or "real"

    def load_and_preprocess(self, data_path):
        # 根据数据路径判断数据类型
        if "A分类" in data_path or "A1.npz" in data_path:
            print("检测到AFAC2026真实数据")
            self.data_type = "real"
            data = load_afac2026_real_data(data_path)
            data = create_train_val_split(data, val_ratio=0.2, seed=42)

            # 为真实数据创建train_mask和val_mask
            data.train_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
            data.val_mask = torch.zeros(data.num_nodes, dtype=torch.bool)
            data.train_mask[data.train_idx] = True
            data.val_mask[data.val_idx] = True

            # 现在可以调用normalize_graph_features了
            data = normalize_graph_features(data)
        else:
            print("检测到合成数据")
            self.data_type = "synthetic"
            data = load_afac_sparse_graph(data_path)
            data = normalize_graph_features(data)

        if self.enable_debias:
            data = self._dist_debias(data)
        if self.enable_feature_enhance:
            data = self.enhance_features(data)
        return data

    def enhance_features(self, data):
        x = data.x.clone()
        if isinstance(x, torch.Tensor):
            stat_features = self._compute_stat_features(x)
            degree_features = self._compute_degree_features(data)
            gdc_features = self._compute_gdc_features(data)
            clustering_features = self._compute_clustering_features(data)
            hop_features = self._compute_hop_features(data)
            enhanced_x = torch.cat([x, stat_features, degree_features, gdc_features, clustering_features, hop_features], dim=1)
            data.x = enhanced_x
        return data

    def _compute_stat_features(self, x):
        feat_mean = x.mean(dim=1, keepdim=True)
        feat_std = x.std(dim=1, keepdim=True) + 1e-8
        feat_min = x.min(dim=1, keepdim=True)[0]
        feat_max = x.max(dim=1, keepdim=True)[0]
        feat_norm = x.norm(dim=1, keepdim=True)
        feat_sum = x.sum(dim=1, keepdim=True)
        feat_entropy = -(x * torch.log(x.abs() + 1e-8)).sum(dim=1, keepdim=True)
        return torch.cat([feat_mean, feat_std, feat_min, feat_max, feat_norm, feat_sum, feat_entropy], dim=1)

    def _compute_degree_features(self, data):
        if hasattr(data, 'edge_index'):
            deg = degree(data.edge_index[0], data.num_nodes)
            deg = deg.unsqueeze(1)
            deg_log = torch.log(deg + 1)
            deg_norm = deg / deg.max() if deg.max() > 0 else deg
            deg_sq = deg ** 2
            return torch.cat([deg, deg_log, deg_norm, deg_sq], dim=1)
        return torch.zeros(data.num_nodes, 4)

    def _compute_gdc_features(self, data):
        if hasattr(data, 'edge_index'):
            transform = GDC(
                self_loop_weight=1,
                normalization_in='sym',
                normalization_out='col',
                diffusion_kwargs=dict(method='ppr', alpha=0.15),
                sparsification_kwargs=dict(method='topk', k=64, dim=0),
                exact=False
            )
            try:
                gdc_data = transform(data.clone())
                adj = to_scipy_sparse_matrix(gdc_data.edge_index, gdc_data.edge_weight, gdc_data.num_nodes)
                if adj.shape[0] == data.num_nodes:
                    ppr_scores = adj.sum(axis=1).A.flatten()
                    ppr_scores = torch.from_numpy(ppr_scores).float().unsqueeze(1)
                    ppr_norm = ppr_scores / (ppr_scores.max() + 1e-8)
                    ppr_entropy = -(ppr_scores * torch.log(ppr_scores + 1e-8)).sum(dim=0, keepdim=True).expand(data.num_nodes, 1)
                    return torch.cat([ppr_scores, ppr_norm, ppr_entropy], dim=1)
            except:
                pass
        return torch.zeros(data.num_nodes, 3)

    def _compute_clustering_features(self, data):
        if hasattr(data, 'edge_index') and data.num_nodes < 2000:
            try:
                adj = to_scipy_sparse_matrix(data.edge_index, None, data.num_nodes)
                clustering = []
                for i in range(data.num_nodes):
                    neighbors = adj[i].nonzero()[1]
                    if len(neighbors) >= 2:
                        sub_adj = adj[neighbors][:, neighbors]
                        triangles = (sub_adj @ sub_adj @ sub_adj).diagonal().sum() / 6
                        possible = len(neighbors) * (len(neighbors) - 1) / 2
                        cc = triangles / possible if possible > 0 else 0
                    else:
                        cc = 0
                    clustering.append(cc)
                clustering = torch.tensor(clustering).float().unsqueeze(1)
                return clustering
            except:
                pass
        return torch.zeros(data.num_nodes, 1)

    def _compute_hop_features(self, data):
        if hasattr(data, 'edge_index'):
            try:
                hop1_counts = []
                hop2_counts = []
                for i in range(data.num_nodes):
                    _, hop1_neighbors, _, _ = k_hop_subgraph(i, 1, data.edge_index)
                    _, hop2_neighbors, _, _ = k_hop_subgraph(i, 2, data.edge_index)
                    hop1_counts.append(len(hop1_neighbors) - 1)
                    hop2_counts.append(len(hop2_neighbors) - len(hop1_neighbors))
                hop1 = torch.tensor(hop1_counts).float().unsqueeze(1)
                hop2 = torch.tensor(hop2_counts).float().unsqueeze(1)
                hop_ratio = hop2 / (hop1 + 1)
                return torch.cat([hop1, hop2, hop_ratio], dim=1)
            except:
                pass
        return torch.zeros(data.num_nodes, 3)

    def augment_graph(self, data):
        data = self._edge_dropout(data)
        data = self._feature_dropout(data)
        return data

    def _edge_dropout(self, data):
        if self.edge_dropout > 0 and hasattr(data, 'edge_index'):
            edge_index = data.edge_index.clone()
            num_edges = edge_index.shape[1]
            mask = torch.rand(num_edges) > self.edge_dropout
            data.edge_index = edge_index[:, mask]
        return data

    def _feature_dropout(self, data):
        if self.feature_dropout > 0:
            x = data.x
            mask = torch.rand_like(x) > self.feature_dropout
            data.x = x * mask.float()
        return data

    def apply_label_smoothing(self, labels, num_classes):
        if self.label_smoothing > 0:
            return labels * (1 - self.label_smoothing) + self.label_smoothing / num_classes
        return labels

    def fill_missing_values(self, data):
        x = data.x
        if isinstance(x, torch.Tensor):
            mask = (x != 0)
            if not mask.all():
                row_mean = x.sum(dim=1, keepdim=True) / (mask.sum(dim=1, keepdim=True) + 1e-8)
                x_filled = x.clone()
                x_filled[~mask] = row_mean.expand_as(x_filled)[~mask]
                data.x = x_filled
        return data

    def _dist_debias(self, data):
        train_y = data.y[data.train_mask].numpy()
        cnt = np.bincount(train_y)
        w = 1 / (cnt + 1e-6)
        w = w / w.sum() * len(cnt)
        sample_w = torch.ones(data.num_nodes)
        for c in range(len(cnt)):
            sample_w[data.y == c] = w[c]
        data.sample_weight = sample_w
        return data