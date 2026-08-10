# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第6条（相变临界公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然/肉身能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, 相变阈值MLP→GCN=0.15, GCN→GAT=0.25, GAT→TGN=0.35
"""

import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, GATConv, GCN2Conv, TransformerConv, global_add_pool
from torch_geometric.utils import dropout_adj, add_self_loops

class DeepGCN(nn.Module):
    """
    功能：深度图卷积网络模型
    理论映射：2重自然秩序基底·实体相变演化规则
    能级关联：肉身能级e_body更新
    约束来源：相变临界公理
    """
    def __init__(self, d_in, d_h, d_out, num_layers=6):
        super().__init__()
        self.convs = nn.ModuleList()
        self.convs.append(GCNConv(d_in, d_h))
        for _ in range(num_layers - 2):
            self.convs.append(GCNConv(d_h, d_h))
        self.convs.append(GCNConv(d_h, d_out))
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bns = nn.ModuleList([nn.BatchNorm1d(d_h) for _ in range(num_layers - 1)])
        
    def forward(self, x, edge_index):
        x = self.relu(self.convs[0](x, edge_index))
        x = self.dropout(x)
        for i, conv in enumerate(self.convs[1:-1]):
            x = conv(x, edge_index)
            x = self.bns[i](x)
            x = self.relu(x)
            x = self.dropout(x)
        x = self.convs[-1](x, edge_index)
        return x

class GATv2(nn.Module):
    def __init__(self, d_in, d_h, d_out, heads=8):
        super().__init__()
        self.conv1 = GATConv(d_in, d_h, heads=heads, concat=True)
        self.conv2 = GATConv(d_h * heads, d_h, heads=heads//2, concat=True)
        self.conv3 = GATConv(d_h * heads//2, d_out, heads=1, concat=False)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bn1 = nn.BatchNorm1d(d_h * heads)
        self.bn2 = nn.BatchNorm1d(d_h * heads//2)
        
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, edge_index)
        return x

class GCNII(nn.Module):
    def __init__(self, d_in, d_h, d_out, num_layers=10, alpha=0.1, theta=0.5):
        super().__init__()
        self.lin1 = nn.Linear(d_in, d_h)
        self.convs = nn.ModuleList()
        for i in range(num_layers):
            self.convs.append(GCN2Conv(d_h, alpha, theta, layer=i+1))
        self.lin2 = nn.Linear(d_h, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bns = nn.ModuleList([nn.BatchNorm1d(d_h) for _ in range(num_layers)])
        
    def forward(self, x, edge_index):
        x = self.lin1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x0 = x.clone()
        for i, conv in enumerate(self.convs):
            x = conv(x, x0, edge_index)
            x = self.bns[i](x)
            x = self.relu(x)
            x = self.dropout(x)
        x = self.lin2(x)
        return x

class GraphTransformer(nn.Module):
    def __init__(self, d_in, d_h, d_out, heads=4):
        super().__init__()
        self.conv1 = TransformerConv(d_in, d_h, heads=heads)
        self.conv2 = TransformerConv(d_h * heads, d_h, heads=heads)
        self.conv3 = TransformerConv(d_h * heads, d_h, heads=heads)
        self.fc = nn.Linear(d_h * heads, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bn1 = nn.BatchNorm1d(d_h * heads)
        self.bn2 = nn.BatchNorm1d(d_h * heads)
        self.bn3 = nn.BatchNorm1d(d_h * heads)
        
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, edge_index)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc(x)
        return x

class MLP(nn.Module):
    def __init__(self, d_in, d_h, d_out):
        super().__init__()
        self.fc1 = nn.Linear(d_in, d_h)
        self.fc2 = nn.Linear(d_h, d_h * 2)
        self.fc3 = nn.Linear(d_h * 2, d_h)
        self.fc4 = nn.Linear(d_h, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bn1 = nn.BatchNorm1d(d_h)
        self.bn2 = nn.BatchNorm1d(d_h * 2)
        self.bn3 = nn.BatchNorm1d(d_h)
        
    def forward(self, x, edge_index=None):
        x = self.fc1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc2(x)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.fc3(x)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout(x)
        return self.fc4(x)

class GCN(nn.Module):
    def __init__(self, d_in, d_h, d_out):
        super().__init__()
        self.conv1 = GCNConv(d_in, d_h)
        self.conv2 = GCNConv(d_h, d_h * 2)
        self.conv3 = GCNConv(d_h * 2, d_h)
        self.fc = nn.Linear(d_h, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bn1 = nn.BatchNorm1d(d_h)
        self.bn2 = nn.BatchNorm1d(d_h * 2)
        self.bn3 = nn.BatchNorm1d(d_h)
        
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, edge_index)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout(x)
        return self.fc(x)

class GAT(nn.Module):
    def __init__(self, d_in, d_h, d_out):
        super().__init__()
        self.conv1 = GATConv(d_in, d_h, heads=4, concat=True)
        self.conv2 = GATConv(d_h * 4, d_h, heads=2, concat=True)
        self.fc = nn.Linear(d_h * 2, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
        self.bn1 = nn.BatchNorm1d(d_h * 4)
        self.bn2 = nn.BatchNorm1d(d_h * 2)
        
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        return self.fc(x)

class TGN(nn.Module):
    def __init__(self, d_in, d_h, d_out, num_nodes=10000):
        super().__init__()
        from torch_geometric.nn import TGNMemory, MessageNorm
        self.memory = TGNMemory(
            num_nodes=num_nodes,
            raw_msg_dim=d_in,
            memory_dim=d_h,
            time_dim=d_h,
            message_module=MessageNorm(d_h),
        )
        self.fc1 = nn.Linear(d_h, d_h)
        self.fc2 = nn.Linear(d_h, d_out)
        self.relu = nn.ReLU()
        self.bn = nn.BatchNorm1d(d_h)
        
    def forward(self, x, edge_index, edge_time=None):
        if edge_time is not None:
            self.memory.update(edge_index, edge_time, x)
            node_emb = self.memory.memory
        else:
            node_emb = x
        x = self.fc1(node_emb)
        x = self.bn(x)
        x = self.relu(x)
        return self.fc2(x)

class GCLEncoder(nn.Module):
    def __init__(self, d_in, d_h):
        super().__init__()
        self.conv1 = GATConv(d_in, d_h, heads=4, concat=True)
        self.conv2 = GATConv(d_h * 4, d_h, heads=2, concat=True)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.bn1 = nn.BatchNorm1d(d_h * 4)
        self.bn2 = nn.BatchNorm1d(d_h * 2)
        
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        return x