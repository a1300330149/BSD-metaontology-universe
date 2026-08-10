# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·自然秩序配套拓展
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：γ=0.92

拓展分支：多模态图任务通用拓展（仅外围增量，不改动1重核心流转逻辑）
归属：2重自然秩序基底配套拓展
"""

import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, GATConv

class GraphReg(nn.Module):
    """
    功能：图回归模型
    理论映射：2重自然秩序基底·实体回归规则
    能级关联：肉身能级e_body更新
    约束来源：科研动力学公理
    """
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.reg_head = nn.Linear(hidden_dim, out_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x, edge_index):
        x = self.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = self.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        return self.reg_head(x)

class GraphSeg(nn.Module):
    def __init__(self, in_dim, hidden_dim, num_classes):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.seg_head = nn.Linear(hidden_dim, num_classes)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x, edge_index):
        x = self.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = self.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        return self.seg_head(x)

class TextGNN(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.conv1 = GATConv(in_dim, hidden_dim, heads=4)
        self.conv2 = GATConv(hidden_dim * 4, hidden_dim, heads=2)
        self.fc = nn.Linear(hidden_dim * 2, out_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x, edge_index):
        x = self.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = self.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        return self.fc(x)

class ImageGNN(nn.Module):
    def __init__(self, in_dim, hidden_dim, out_dim):
        super().__init__()
        self.conv1 = GCNConv(in_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.conv3 = GCNConv(hidden_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, out_dim)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)

    def forward(self, x, edge_index):
        x = self.relu(self.conv1(x, edge_index))
        x = self.dropout(x)
        x = self.relu(self.conv2(x, edge_index))
        x = self.dropout(x)
        x = self.relu(self.conv3(x, edge_index))
        x = self.dropout(x)
        return self.fc(x)