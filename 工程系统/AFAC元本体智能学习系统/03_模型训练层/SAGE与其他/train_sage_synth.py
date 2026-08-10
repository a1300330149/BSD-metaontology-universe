import os
import sys
import torch
import torch.nn as nn
import numpy as np

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from torch_geometric.nn import SAGEConv
from torch_geometric.data import Data

class GraphSAGE(nn.Module):
    def __init__(self, d_in, d_h, d_out):
        super().__init__()
        self.conv1 = SAGEConv(d_in, d_h)
        self.conv2 = SAGEConv(d_h, d_h)
        self.conv3 = SAGEConv(d_h, d_h)
        self.fc = nn.Linear(d_h, d_out)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.3)
    
    def forward(self, x, edge_index):
        x = self.conv1(x, edge_index)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv2(x, edge_index)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.conv3(x, edge_index)
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
    data_path = os.path.join(BASE, "data/afac2026_synth_graph.npz")
    npz = np.load(data_path)
    
    x = torch.from_numpy(npz["node_features"]).float()
    edge_index = torch.from_numpy(npz["edge_index"]).long()
    y = torch.from_numpy(npz["labels"]).long()
    train_mask = torch.from_numpy(npz["train_mask"]).bool()
    val_mask = torch.from_numpy(npz["val_mask"]).bool()
    test_mask = torch.from_numpy(npz["test_mask"]).bool()
    
    data = Data(x=x, edge_index=edge_index, y=y, 
                train_mask=train_mask, val_mask=val_mask, test_mask=test_mask)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = data.to(device)
    
    d_in = data.x.shape[1]
    d_h = 256
    d_out = 10
    
    model = GraphSAGE(d_in, d_h, d_out).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=1e-4)
    criterion = nn.CrossEntropyLoss()
    
    best_val = 0.0
    
    for epoch in range(100):
        model.train()
        optimizer.zero_grad()
        
        out = model(data.x, data.edge_index)
        loss = criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        optimizer.step()
        
        if epoch % 10 == 0:
            val_acc = evaluate(model, data, "val")
            if val_acc > best_val:
                best_val = val_acc
            print(f"Epoch {epoch:3d}/100 | Loss: {loss.item():.4f} | Val: {val_acc:.4f} | Best: {best_val:.4f}")
    
    test_acc = evaluate(model, data, "test")
    print(f"\n最终结果: Val={best_val:.4f}, Test={test_acc:.4f}")

if __name__ == "__main__":
    main()