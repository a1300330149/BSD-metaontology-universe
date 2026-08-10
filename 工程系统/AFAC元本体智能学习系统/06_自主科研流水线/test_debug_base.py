import os
import sys
import yaml
import traceback

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.entity_layer.base_graph_agent import BaseGraphAgent

cfg = yaml.safe_load(open("configs/afac2026_default.yaml"))

d_agent = DataPreprocessAgent()
data = d_agent.load_and_preprocess(cfg["dataset"]["data_path"])
data = d_agent.enhance_features(data)

base = BaseGraphAgent(cfg["dataset"], model_type="GATv2")
base.init_base_model(data=data)

print("Model initialized, starting training...")
try:
    score = base.train_one_epoch(data)
    print(f"Score: {score}")
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()