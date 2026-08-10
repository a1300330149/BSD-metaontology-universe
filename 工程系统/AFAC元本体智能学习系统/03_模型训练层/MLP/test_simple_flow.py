import os
import sys
import yaml
import torch
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.entity_layer.models import GATv2
from src.utils.data_utils import evaluate

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    print("加载数据...")
    data_agent = DataPreprocessAgent()
    data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])
    print(f"数据: {data.x.shape[0]}节点, {data.edge_index.shape[1]}边")
    
    data = data_agent.enhance_features(data)
    print(f"特征增强后: {data.x.shape[1]}维度")
    
    d_in = data.x.shape[1]
    d_h = cfg["dataset"]["hidden_dim"]
    d_out = cfg["dataset"]["num_classes"]
    
    print(f"初始化GATv2模型: {d_in}->{d_h}->{d_out}")
    model = GATv2(d_in, d_h, d_out)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    data = data.to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=1e-4)
    criterion = torch.nn.CrossEntropyLoss()
    
    best_val = 0.0
    print("开始训练...")
    
    for epoch in range(50):
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
            print(f"Epoch {epoch:3d}/50 | Loss: {loss.item():.4f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()