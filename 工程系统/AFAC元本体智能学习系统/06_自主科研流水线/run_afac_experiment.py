import os
import sys
import yaml
import json
import torch
import numpy as np
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.master_agent.master_research_agent import MasterResearchAgent

def load_cfg(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def save_out(res, root):
    os.makedirs(root, exist_ok=True)
    json.dump(res, open(os.path.join(root, "metrics.json"), "w"), indent=4)

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    cfg = load_cfg(cfg_path)
    seed = cfg["seed"]
    torch.manual_seed(seed)
    np.random.seed(seed)
    print("==== AFAC2026 自主科研智能体启动 ====")
    print(f"任务模式: {cfg.get('task_target')}")
    print(f"数据集: {cfg['dataset']['data_path']}")
    print(f"最大步数: {cfg['max_steps']}")
    
    master = MasterResearchAgent(cfg)
    print("智能体初始化完成")
    
    result = master.run_full_autonomous_research()
    print(f"实验完成")
    print(f"最优分数: {result['best_score']:.4f}")
    print(f"最终等级: {result['final_level']}")
    print(f"总步数: {result['total_step']}")
    
    out_dir = os.path.join(BASE, "output", "reports", datetime.now().strftime("%Y%m%d_%H%M%S"))
    save_out(result, out_dir)
    print(f"结果保存路径: {out_dir}")

if __name__ == "__main__":
    main()