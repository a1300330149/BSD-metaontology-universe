import os
import sys
import yaml
import traceback
import torch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.entity_layer.base_graph_agent import BaseGraphAgent
from src.entity_layer.models import GATv2

cfg = yaml.safe_load(open("configs/afac2026_default.yaml"))

d_agent = DataPreprocessAgent()
data = d_agent.load_and_preprocess(cfg["dataset"]["data_path"])
data = d_agent.enhance_features(data)

print("=== Data Info ===")
print(f"x shape: {data.x.shape}")
print(f"edge_index shape: {data.edge_index.shape}")
print(f"y shape: {data.y.shape}")
print(f"train_mask sum: {data.train_mask.sum()}")
print(f"val_mask sum: {data.val_mask.sum()}")
print(f"test_mask sum: {data.test_mask.sum()}")

print("\n=== Testing model directly ===")
model = GATv2(data.x.shape[1], 128, cfg["dataset"]["num_classes"])
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
criterion = torch.nn.CrossEntropyLoss()

print("Running forward pass...")
try:
    out = model(data.x, data.edge_index)
    print(f"Output shape: {out.shape}")
    loss = criterion(out[data.train_mask], data.y[data.train_mask])
    print(f"Loss: {loss.item()}")
    loss.backward()
    optimizer.step()
    print("Backward pass and optimization completed")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()