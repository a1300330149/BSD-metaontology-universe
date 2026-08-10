import os
import sys
import time
import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

start = time.time()
print("Step 1: Loading config")
cfg = yaml.safe_load(open("configs/afac2026_default.yaml"))
print(f"Dataset: {cfg['dataset']['data_path']}")

print("\nStep 2: Loading data agent")
from src.entity_layer.data_preprocess import DataPreprocessAgent
d_agent = DataPreprocessAgent()

print("\nStep 3: Loading data")
data = d_agent.load_and_preprocess(cfg["dataset"]["data_path"])
print(f"Nodes: {data.x.shape[0]}, Edges: {data.edge_index.shape[1]}")

print("\nStep 4: Feature enhancement")
data = d_agent.enhance_features(data)
print(f"Features: {data.x.shape[1]}")

print("\nStep 5: Creating model")
import torch
from src.entity_layer.models import GATv2
model = GATv2(data.x.shape[1], 128, cfg["dataset"]["num_classes"])

print("\nStep 6: Training")
opt = torch.optim.Adam(model.parameters(), lr=0.001)
crit = torch.nn.CrossEntropyLoss()

for i in range(30):
    opt.zero_grad()
    loss = crit(model(data.x, data.edge_index)[data.train_mask], data.y[data.train_mask])
    loss.backward()
    opt.step()
    if i % 10 == 0:
        print(f"Epoch {i}: Loss={loss.item():.4f}")

print("\nStep 7: Evaluation")
from src.utils.data_utils import evaluate
score = evaluate(model, data, "test")
print(f"Score: {score:.4f}")
print(f"Time: {time.time()-start:.2f}s")