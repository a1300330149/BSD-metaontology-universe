import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

print("Step 1: Import FoundationController")
from src.foundation.foundation_controller import FoundationController

print("Step 2: Create FoundationController")
foundation = FoundationController()
print("Foundation created")

print("\nStep 3: Switch to competition mode")
foundation.switch_task_mode("competition")
print("Mode switched")

print("\nStep 4: Get realm configs")
tao = foundation.level2.get_realm_config("TAO")
nature = foundation.level2.get_realm_config("NATURE")
human = foundation.level2.get_realm_config("HUMAN")
print(f"feature_enhancement: {nature.get('feature_enhancement')}")
print(f"skip_mlp_cold_start: {nature.get('skip_mlp_cold_start')}")

print("\nStep 5: Import MasterResearchAgent")
from src.master_agent.master_research_agent import MasterResearchAgent
print("Import done")

print("\nStep 6: Load config")
import yaml
cfg = yaml.safe_load(open("configs/afac2026_default.yaml"))
print(f"Task target: {cfg.get('task_target')}")
print(f"Domain: {cfg.get('domain')}")

print("\nStep 7: Create MasterResearchAgent")
master = MasterResearchAgent(cfg)
print("Master agent created")
print(f"feature_enhancement: {master.feature_enhancement}")
print(f"skip_mlp_cold_start: {master.skip_mlp_cold_start}")

print("\nStep 8: Load data")
data = master.agents["data"].load_and_preprocess(cfg["dataset"]["data_path"])
print(f"Data loaded: {data.x.shape[0]} nodes")

print("\nStep 9: Feature enhancement")
if master.feature_enhancement:
    data = master.agents["data"].enhance_features(data)
    print(f"Features: {data.x.shape[1]}")

print("\nStep 10: Init model")
master.agents["base"].init_base_model(data=data)
print("Model initialized")

print("\nStep 11: Train")
score = master.agents["base"].train_one_epoch(data)
print(f"Score: {score:.4f}")

print("\nAll steps completed!")