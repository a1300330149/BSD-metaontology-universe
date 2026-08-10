import os
import sys
import yaml
import torch
import torch.nn as nn
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.models import GATv2
from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.utils.data_utils import evaluate

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    torch.manual_seed(cfg["seed"])
    np.random.seed(cfg["seed"])
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"设备: {device}")
    
    data_agent = DataPreprocessAgent()
    data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])
    data = data_agent.enhance_features(data)
    data = data.to(device)
    
    d_in = data.x.shape[1]
    d_h = cfg["dataset"]["hidden_dim"]
    d_out = cfg["dataset"]["num_classes"]
    
    print(f"特征维度: {d_in}, 隐藏层: {d_h}, 类别数: {d_out}")
    
    model = GATv2(d_in, d_h, d_out).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        
        val_acc = evaluate(model, data, "val")
        
        if val_acc > best_val:
            best_val = val_acc
        
        if epoch % 10 == 0:
            print(f"Epoch {epoch:3d}/200 | Loss: {loss.item():.4f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()