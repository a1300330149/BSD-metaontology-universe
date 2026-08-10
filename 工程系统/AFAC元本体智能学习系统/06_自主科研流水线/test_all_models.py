import os
import sys
import yaml
import torch
import torch.nn as nn
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.models import GCN, GATv2, DeepGCN, MLP
from src.entity_layer.data_preprocess import DataPreprocessAgent

def evaluate(model, data, split="val"):
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        mask = getattr(data, f"{split}_mask")
        pred = out[mask].argmax(dim=1)
        return (pred == data.y[mask]).float().mean().item()

def train_model(model, data, lr=0.001, wd=1e-4, epochs=200):
    optimizer = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=wd)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        if epoch % 50 == 0:
            val_acc = evaluate(model, data)
            best_val = max(best_val, val_acc)
    
    return best_val

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    data_agent = DataPreprocessAgent()
    data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])
    data = data.to(device)
    
    d_in = data.x.shape[1]
    d_h = 256
    d_out = cfg["dataset"]["num_classes"]
    
    print("=== 模型评估 ===")
    
    models = [
        ("GCN", GCN(d_in, d_h, d_out)),
        ("GATv2", GATv2(d_in, d_h, d_out, heads=8)),
        ("DeepGCN", DeepGCN(d_in, d_h, d_out, num_layers=4)),
        ("MLP", MLP(d_in, d_h, d_out)),
    ]
    
    results = []
    for name, model in models:
        model = model.to(device)
        best_val = train_model(model, data)
        test_acc = evaluate(model, data, "test")
        results.append((name, best_val, test_acc))
        print(f"{name}: Val={best_val:.4f}, Test={test_acc:.4f}")
    
    print("\n=== 集成模型 ===")
    ensemble = nn.ModuleList([m[1].to(device) for m in models])
    ensemble.eval()
    
    with torch.no_grad():
        outputs = []
        for model in ensemble:
            if isinstance(model, MLP):
                out = model(data.x)
            else:
                out = model(data.x, data.edge_index)
            outputs.append(out)
        
        ensemble_out = torch.stack(outputs).mean(dim=0)
        
        val_pred = ensemble_out[data.val_mask].argmax(dim=1)
        val_acc = (val_pred == data.y[data.val_mask]).float().mean().item()
        
        test_pred = ensemble_out[data.test_mask].argmax(dim=1)
        test_acc = (test_pred == data.y[data.test_mask]).float().mean().item()
        
        print(f"集成模型: Val={val_acc:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()