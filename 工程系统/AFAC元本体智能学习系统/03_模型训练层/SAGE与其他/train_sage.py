import os
import sys
import yaml
import torch
import torch.nn as nn
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent

from torch_geometric.nn import SAGEConv

class GraphSAGE(nn.Module):
    def __init__(self, d_in, d_h, d_out):
        super().__init__()
        self.conv1 = SAGEConv(d_in, d_h)
        self.conv2 = SAGEConv(d_h, d_h)
        self.conv3 = SAGEConv(d_h, d_h)
        self.fc = nn.Linear(d_h, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)
        self.bn1 = nn.BatchNorm1d(d_h)
        self.bn2 = nn.BatchNorm1d(d_h)
        self.bn3 = nn.BatchNorm1d(d_h)
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.bn2(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, edge_index)
        x = self.bn3(x)
        x = self.relu(x)
        x = self.dropout(x)
        return self.fc(x)

def evaluate(model, data, split="val"):
    model.eval()
    with torch.no_grad():
        out = model(data.x, data.edge_index)
        mask = getattr(data, f"{split}_mask")
        pred = out[mask].argmax(dim=1)
        return (pred == data.y[mask]).float().mean().item()

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
    
    model = GraphSAGE(d_in, d_h, d_out).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001, weight_decay=5e-4)
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=300)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    
    for epoch in range(300):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        scheduler.step()
        
        if epoch % 30 == 0 or epoch == 299:
            val_acc = evaluate(model, data, "val")
            if val_acc > best_val:
                best_val = val_acc
            lr = optimizer.param_groups[0]['lr']
            print(f"Epoch {epoch:3d}/300 | Loss: {loss.item():.4f} | LR: {lr:.5f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()