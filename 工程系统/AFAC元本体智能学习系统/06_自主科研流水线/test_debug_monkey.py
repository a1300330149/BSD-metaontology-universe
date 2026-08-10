import os
import sys
import yaml
import torch
import traceback

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.entity_layer.base_graph_agent import BaseGraphAgent
from src.entity_layer.models import GATv2
from src.utils.data_utils import evaluate

cfg = yaml.safe_load(open("configs/afac2026_default.yaml"))

d_agent = DataPreprocessAgent()
data = d_agent.load_and_preprocess(cfg["dataset"]["data_path"])
data = d_agent.enhance_features(data)

print("=== Testing BaseGraphAgent with verbose output ===")
base = BaseGraphAgent(cfg["dataset"], model_type="GATv2")
base.init_base_model(data=data)

print(f"Device: {base.device}")
print(f"Model device: {next(base.model.parameters()).device}")

# Monkey patch to add debug output
original_train = base.train_one_epoch

def debug_train(data):
    data = data.to(base.device)
    print(f"Data moved to device: {data.x.device}")
    
    best_val = 0.0
    for epoch in range(base.num_epochs_per_step):
        print(f"  Epoch {epoch+1}/{base.num_epochs_per_step}...")
        base.model.train()
        base.optimizer.zero_grad()
        
        out = base.model(data.x, data.edge_index)
        loss = base.criterion(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        torch.nn.utils.clip_grad_norm_(base.model.parameters(), max_norm=1.0)
        base.optimizer.step()
        base.scheduler.step()
        
        print(f"    Loss: {loss.item():.4f}")
        
        try:
            val_acc = evaluate(base.model, data, "val")
            print(f"    Val: {val_acc:.4f}")
            if val_acc > best_val:
                best_val = val_acc
        except Exception as e:
            print(f"    Evaluate error: {e}")
            traceback.print_exc()
            break
    
    print(f"Best val: {best_val:.4f}")
    return best_val

base.train_one_epoch = debug_train

print("Starting training...")
try:
    score = base.train_one_epoch(data)
    print(f"Final score: {score}")
except Exception as e:
    print(f"Training error: {e}")
    traceback.print_exc()