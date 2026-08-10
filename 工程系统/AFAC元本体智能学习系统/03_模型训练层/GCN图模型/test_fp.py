import os
import sys
import yaml
import torch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent

cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
with open(cfg_path, "r", encoding="utf-8") as f:
    cfg = yaml.safe_load(f)

data_agent = DataPreprocessAgent()
data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])

print(f"节点数: {data.num_nodes}")
print(f"边数: {data.edge_index.shape[1]}")
print(f"特征维度: {data.x.shape[1]}")
print(f"训练集: {data.train_mask.sum()}")
print(f"验证集: {data.val_mask.sum()}")
print(f"测试集: {data.test_mask.sum()}")

edge_index = data.edge_index
row, col = edge_index
deg = torch.bincount(row, minlength=data.x.shape[0]).float().clamp(min=1)
print(f"平均度数: {deg.mean().item():.2f}")
print(f"度数分布: min={deg.min().item()}, max={deg.max().item()}")

x = data.x
alpha = 0.2
for i in range(5):
    x_new = x.clone()
    x_new[row] += alpha * x[col] / deg[row, None]
    diff = (x_new - x).abs().mean().item()
    x = x_new
    print(f"迭代{i}: 特征变化={diff:.6f}")

print("特征传播完成")