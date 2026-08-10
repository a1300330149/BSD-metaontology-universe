import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import yaml
from src.master_agent.master_research_agent import MasterResearchAgent

def light_config_override(cfg: dict):
    cfg["param_bounds"]["hidden_dim"] = [16, 48]
    cfg["max_steps"] = 40
    cfg["dataset"]["model_allow_list"] = ["MLP", "GCN"]
    cfg["enable_self_evolution"] = False
    return cfg

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    cfg_raw = yaml.safe_load(open(cfg_path, "r", encoding="utf-8"))
    light_cfg = light_config_override(cfg_raw)
    master = MasterResearchAgent(light_cfg)
    master.enable_evo = False
    master.agents["opt"].init_points = 3
    result = master.run_full_autonomous_research()
    print("轻量化实验完成，最优精度：", result["best_score"])

if __name__ == "__main__":
    main()