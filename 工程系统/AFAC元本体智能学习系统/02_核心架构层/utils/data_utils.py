"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：稀疏补偿α=0.18
"""

import torch
import numpy as np
from torch_geometric.data import Data
from sklearn.preprocessing import StandardScaler

def load_afac_sparse_graph(data_path):
    npz = np.load(data_path)
    x = torch.FloatTensor(npz["node_features"])
    edge_idx = torch.LongTensor(npz["edge_index"])
    y = torch.LongTensor(npz["labels"])
    train_mask = torch.BoolTensor(npz["train_mask"])
    val_mask = torch.BoolTensor(npz["val_mask"])
    test_mask = torch.BoolTensor(npz["test_mask"])
    x = torch.nan_to_num(x, nan=0.0)
    graph = Data(x=x, edge_index=edge_idx, y=y, train_mask=train_mask, val_mask=val_mask, test_mask=test_mask)
    if "edge_time" in npz:
        graph.edge_time = torch.FloatTensor(npz["edge_time"])
    return graph

def normalize_graph_features(data):
    scaler = StandardScaler()
    train_x = data.x[data.train_mask].numpy()
    scaler.fit(train_x)
    data.x = torch.FloatTensor(scaler.transform(data.x))
    return data

def evaluate(model, data, split="val"):
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        mask = getattr(data, f"{split}_mask")
        pred = out[mask].argmax(dim=1)
        return (pred == data.y[mask]).float().mean().item()