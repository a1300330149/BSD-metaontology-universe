import os
import sys
import time
import yaml
import torch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.entity_layer.models import GATv2
from src.utils.data_utils import evaluate

cfg = yaml.safe_load(open("configs/afac2026_default.yaml"))

start = time.time()

d_agent = DataPreprocessAgent()
data = d_agent.load_and_preprocess(cfg["dataset"]["data_path"])
data = d_agent.enhance_features(data)

model = GATv2(data.x.shape[1], 128, cfg["dataset"]["num_classes"])
opt = torch.optim.Adam(model.parameters(), lr=0.001)
crit = torch.nn.CrossEntropyLoss()

for _ in range(30):
    opt.zero_grad()
    loss = crit(model(data.x, data.edge_index)[data.train_mask], data.y[data.train_mask])
    loss.backward()
    opt.step()

score = evaluate(model, data, "test")
print(f"Score: {score:.4f}")
print(f"Time: {time.time()-start:.2f}s")