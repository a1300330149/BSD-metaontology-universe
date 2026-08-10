"""
归属基底：第相变演化位（第三位）·自然秩序配套拓展
对应三界秩序：自然秩序
对应公理：第2条（全域九维法理公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：载体实体/相变自然
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：γ=0.92

拓展分支：多模态拓展（仅外围增量，不改动1重核心流转逻辑）
归属：2重自然秩序基底配套拓展
"""

import os
import numpy as np
import torch
from torch_geometric.data import Data
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_nlp_text_graph(text_emb_path: str) -> Data:
    data = np.load(text_emb_path)
    if "embeddings" in data:
        x = torch.FloatTensor(data["embeddings"])
    elif "sentence_embeddings" in data:
        x = torch.FloatTensor(data["sentence_embeddings"])
    else:
        raise ValueError("未找到文本嵌入数据")
    
    sim_matrix = cosine_similarity(x.numpy())
    threshold = np.percentile(sim_matrix, 90)
    edges = np.where(sim_matrix > threshold)
    edge_index = torch.LongTensor(np.vstack([edges[0], edges[1]]))
    
    if "labels" in data:
        y = torch.LongTensor(data["labels"])
    else:
        y = torch.zeros(x.shape[0], dtype=torch.long)
    
    n_nodes = x.shape[0]
    train_mask = torch.zeros(n_nodes, dtype=torch.bool)
    val_mask = torch.zeros(n_nodes, dtype=torch.bool)
    test_mask = torch.zeros(n_nodes, dtype=torch.bool)
    
    train_idx = np.random.choice(n_nodes, int(n_nodes * 0.6), replace=False)
    remaining = np.setdiff1d(np.arange(n_nodes), train_idx)
    val_idx = np.random.choice(remaining, int(n_nodes * 0.2), replace=False)
    test_idx = np.setdiff1d(remaining, val_idx)
    
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask, val_mask=val_mask, test_mask=test_mask)

def load_cv_image_graph(img_folder: str) -> Data:
    feature_files = [f for f in os.listdir(img_folder) if f.endswith('.npy')]
    features = []
    labels = []
    
    for f in feature_files:
        feat = np.load(os.path.join(img_folder, f))
        features.append(feat.flatten())
        label = int(f.split('_')[0])
        labels.append(label)
    
    x = torch.FloatTensor(np.array(features))
    y = torch.LongTensor(labels)
    
    sim_matrix = cosine_similarity(x.numpy())
    threshold = np.percentile(sim_matrix, 85)
    edges = np.where(sim_matrix > threshold)
    edge_index = torch.LongTensor(np.vstack([edges[0], edges[1]]))
    
    n_nodes = x.shape[0]
    train_mask = torch.zeros(n_nodes, dtype=torch.bool)
    val_mask = torch.zeros(n_nodes, dtype=torch.bool)
    test_mask = torch.zeros(n_nodes, dtype=torch.bool)
    
    train_idx = np.random.choice(n_nodes, int(n_nodes * 0.6), replace=False)
    remaining = np.setdiff1d(np.arange(n_nodes), train_idx)
    val_idx = np.random.choice(remaining, int(n_nodes * 0.2), replace=False)
    test_idx = np.setdiff1d(remaining, val_idx)
    
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask, val_mask=val_mask, test_mask=test_mask)

def load_time_series_graph(ts_path: str) -> Data:
    data = np.load(ts_path)
    if "time_series" in data:
        ts_data = data["time_series"]
    else:
        raise ValueError("未找到时间序列数据")
    
    x = torch.FloatTensor(ts_data)
    n_nodes = x.shape[0]
    
    edges = []
    for i in range(n_nodes - 1):
        edges.append([i, i + 1])
        if i > 0:
            edges.append([i, i - 1])
    
    edge_index = torch.LongTensor(edges).t()
    
    if "labels" in data:
        y = torch.LongTensor(data["labels"])
    else:
        y = torch.zeros(n_nodes, dtype=torch.long)
    
    train_mask = torch.zeros(n_nodes, dtype=torch.bool)
    val_mask = torch.zeros(n_nodes, dtype=torch.bool)
    test_mask = torch.zeros(n_nodes, dtype=torch.bool)
    
    train_idx = np.random.choice(n_nodes, int(n_nodes * 0.6), replace=False)
    remaining = np.setdiff1d(np.arange(n_nodes), train_idx)
    val_idx = np.random.choice(remaining, int(n_nodes * 0.2), replace=False)
    test_idx = np.setdiff1d(remaining, val_idx)
    
    train_mask[train_idx] = True
    val_mask[val_idx] = True
    test_mask[test_idx] = True
    
    return Data(x=x, edge_index=edge_index, y=y, train_mask=train_mask, val_mask=val_mask, test_mask=test_mask)