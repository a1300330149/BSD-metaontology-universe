import os
import sys
import yaml
import torch
import torch.nn as nn
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.models import GCN, GATv2, DeepGCN
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
    data_agent.edge_dropout = 0.2
    data_agent.feature_dropout = 0.1
    data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])
    data = data_agent.enhance_features(data)
    data = data.to(device)
    
    d_in = data.x.shape[1]
    d_h = 128
    d_out = cfg["dataset"]["num_classes"]
    
    print(f"特征维度: {d_in}, 隐藏层: {d_h}, 类别数: {d_out}")
    
    model = GCN(d_in, d_h, d_out).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    
    for epoch in range(300):
        model.train()
        optimizer.zero_grad()
        
        edge_index = data.edge_index
        if epoch % 2 == 0:
            edge_index = torch.cat([data.edge_index, data.edge_index.flip(0)], dim=1)
        
        out = model(data.x, edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=0.5)
        optimizer.step()
        scheduler.step()
        
        val_acc = evaluate(model, data, "val")
        
        if val_acc > best_val:
            best_val = val_acc
        
        if epoch % 20 == 0:
            print(f"Epoch {epoch:3d}/300 | Loss: {loss.item():.4f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()