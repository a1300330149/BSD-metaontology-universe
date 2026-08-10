import os
import sys
import yaml
import torch
import torch.nn as nn
import numpy as np
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.models import GAT, GATv2, DeepGCN, GraphTransformer
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
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=500)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    best_test = 0.0
    
    for epoch in range(500):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        scheduler.step()
        
        val_acc = evaluate(model, data, "val")
        test_acc = evaluate(model, data, "test")
        
        if val_acc > best_val:
            best_val = val_acc
            best_test = test_acc
        
        if epoch % 50 == 0:
            print(f"Epoch {epoch}/500, Loss: {loss.item():.4f}, Val: {val_acc:.4f}, Test: {test_acc:.4f}, Best: {best_val:.4f}")
    
    print(f"\n==== 最终结果 ====")
    print(f"最优验证分数: {best_val:.4f}")
    print(f"对应测试分数: {best_test:.4f}")
    print(f"模型参数: {sum(p.numel() for p in model.parameters()):,}")

if __name__ == "__main__":
    main()