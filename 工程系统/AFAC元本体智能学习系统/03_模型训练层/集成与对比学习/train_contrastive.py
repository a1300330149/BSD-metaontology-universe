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

def evaluate(model, data, split="val"):
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        mask = getattr(data, f"{split}_mask")
        pred = out[mask].argmax(dim=1)
        return (pred == data.y[mask]).float().mean().item()

def sim(z1, z2):
    z1 = nn.functional.normalize(z1)
    z2 = nn.functional.normalize(z2)
    return (z1 * z2).sum(dim=-1)

def train_contrastive(model, data, epochs=100):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        x1 = data.x + torch.randn_like(data.x) * 0.1
        x2 = data.x + torch.randn_like(data.x) * 0.1
        
        z1 = model(x1, data.edge_index)
        z2 = model(x2, data.edge_index)
        
        n = data.x.shape[0]
        pos = sim(z1, z2)
        pos = pos.view(n, 1)
        
        neg1 = sim(z1, z2.T)
        neg2 = sim(z2, z1.T)
        neg = torch.cat([neg1, neg2], dim=1)
        
        logits = torch.cat([pos, neg], dim=1)
        labels = torch.zeros(n, dtype=torch.long, device=data.x.device)
        
        loss = criterion(logits / 0.1, labels)
        loss.backward()
        optimizer.step()
        
        if epoch % 20 == 0:
            print(f"预训练 Epoch {epoch:3d}/{epochs} | Loss: {loss.item():.4f}")
    
    return model

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    with open(cfg_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"设备: {device}")
    
    data_agent = DataPreprocessAgent()
    data = data_agent.load_and_preprocess(cfg["dataset"]["data_path"])
    data = data.to(device)
    
    d_in = data.x.shape[1]
    d_h = 256
    d_out = cfg["dataset"]["num_classes"]
    
    print("=== 自监督预训练 ===")
    model = GATv2(d_in, d_h, d_h, heads=8).to(device)
    model = train_contrastive(model, data, epochs=100)
    
    print("\n=== 微调分类 ===")
    model.conv3 = nn.Linear(d_h * 4, d_out).to(device)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, weight_decay=5e-4)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    
    for epoch in range(200):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        if epoch % 20 == 0 or epoch == 199:
            val_acc = evaluate(model, data, "val")
            if val_acc > best_val:
                best_val = val_acc
            lr = optimizer.param_groups[0]['lr']
            print(f"微调 Epoch {epoch:3d}/200 | Loss: {loss.item():.4f} | LR: {lr:.5f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()