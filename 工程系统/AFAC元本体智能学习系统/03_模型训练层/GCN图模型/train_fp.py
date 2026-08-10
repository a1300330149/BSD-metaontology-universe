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

def feature_propagation(x, edge_index, alpha=0.1, num_iter=10):
    for _ in range(num_iter):
        row, col = edge_index
        deg = torch.bincount(row, minlength=x.shape[0]).float().clamp(min=1)
        x_new = x.clone()
        x_new[row] += alpha * x[col] / deg[row, None]
        x = x_new
    return x

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"设备: {device}")
    
    data_agent = DataPreprocessAgent()
    data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])
    
    data.x = feature_propagation(data.x, data.edge_index, alpha=0.2, num_iter=15)
    
    data = data.to(device)
    
    d_in = data.x.shape[1]
    d_h = 256
    d_out = cfg["dataset"]["num_classes"]
    
    print(f"特征维度: {d_in}, 隐藏层: {d_h}, 类别数: {d_out}")
    
    model = GATv2(d_in, d_h, d_out, heads=8).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.005, weight_decay=5e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    patience = 0
    
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        val_acc = evaluate(model, data, "val")
        
        if val_acc > best_val:
            best_val = val_acc
            patience = 0
        else:
            patience += 1
        
        if patience > 30:
            print(f"早停在Epoch {epoch}")
            break
        
        if epoch % 20 == 0:
            lr = optimizer.param_groups[0]['lr']
            print(f"Epoch {epoch:3d}/200 | Loss: {loss.item():.4f} | LR: {lr:.5f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()