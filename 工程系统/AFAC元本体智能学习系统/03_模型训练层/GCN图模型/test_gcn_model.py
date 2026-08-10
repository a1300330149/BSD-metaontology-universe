import sys
import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import torch
import numpy as np
from src.entity_layer.base_graph_agent import BaseGraphAgent
from src.entity_layer.data_preprocess import DataPreprocessAgent

data_path = os.path.join(BASE, "data/afac2026_sparse_graph.npz")
preprocessor = DataPreprocessAgent()
data = preprocessor.load_and_preprocess(data_path)

dataset_config = {
    "feat_dim": data.x.shape[1],
    "hidden_dim": 256,
    "num_classes": 10,
    "num_nodes": 1000
}

print("\n=== 测试GCN模型 ===")
for lr in [0.0001, 0.001, 0.01]:
    for wd in [1e-5, 1e-4, 1e-3]:
        for dropout in [0.3, 0.5, 0.7]:
            agent = BaseGraphAgent(dataset_config, model_type="GCN")
            agent.init_base_model(lr=lr, wd=wd, dropout=dropout, hidden_dim=256, num_layers=2, num_heads=4, data=data)
            best_val = 0
            for _ in range(20):
                val = agent.train_one_epoch(data)
                if val > best_val:
                    best_val = val
            print(f"GCN lr={lr}, wd={wd}, dropout={dropout}: val={best_val:.4f}")

print("\n=== 测试GATv2模型 ===")
for lr in [0.0001, 0.001]:
    for wd in [1e-5, 1e-4]:
        for dropout in [0.4, 0.6]:
            agent = BaseGraphAgent(dataset_config, model_type="GATv2")
            agent.init_base_model(lr=lr, wd=wd, dropout=dropout, hidden_dim=128, num_layers=2, num_heads=8, data=data)
            best_val = 0
            for _ in range(20):
                val = agent.train_one_epoch(data)
                if val > best_val:
                    best_val = val
            print(f"GATv2 lr={lr}, wd={wd}, dropout={dropout}: val={best_val:.4f}")

print("\n=== 测试GraphSAGE模型 ===")
for lr in [0.0001, 0.001]:
    for wd in [1e-5, 1e-4]:
        agent = BaseGraphAgent(dataset_config, model_type="GraphSAGE")
        agent.init_base_model(lr=lr, wd=wd, dropout=0.5, hidden_dim=256, num_layers=2, num_heads=4, data=data)
        best_val = 0
        for _ in range(20):
            val = agent.train_one_epoch(data)
            if val > best_val:
                best_val = val
        print(f"GraphSAGE lr={lr}, wd={wd}: val={best_val:.4f}")