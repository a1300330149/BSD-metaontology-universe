import os
import sys
import yaml
import torch
import numpy as np
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

from src.master_agent.master_research_agent import MasterResearchAgent

def load_cfg(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    cfg = load_cfg(cfg_path)
    seed = cfg["seed"]
    torch.manual_seed(seed)
    np.random.seed(seed)
    print("==== AFAC2026 自主科研智能体启动 ====")
    
    master = MasterResearchAgent(cfg)
    
    data = master.agents["data"].load_and_preprocess(cfg["dataset"]["data_path"])
    
    if master.feature_enhancement:
        data = master.agents["data"].enhance_features(data)
        print(f"特征增强后维度: {data.x.shape[1]}")
    
    master.agents["base"].init_base_model(data=data)
    print(f"模型类型: {master.agents['base'].model_type}")
    
    init_score = master.agents["base"].train_one_epoch(data)
    print(f"初始分数: {init_score:.4f}")
    
    max_step = cfg["max_steps"]
    best_score = init_score
    
    for step in range(max_step):
        params = master.agents["opt"].suggest_next_params()
        lr = float(params.get("lr", 0.001))
        wd = float(params.get("weight_decay", 1e-4))
        
        data_aug = master.agents["data"].augment_graph(data)
        master.agents["base"].init_base_model(lr, wd, data)
        real_s = master.agents["base"].train_one_epoch(data_aug)
        
        if real_s > best_score:
            best_score = real_s
        
        if step % 20 == 0:
            print(f"Step {step}/{max_step}, 当前分数: {real_s:.4f}, 最优: {best_score:.4f}, lr={lr:.4f}, wd={wd:.4e}")
    
    print(f"\n==== 实验完成 ====")
    print(f"最优分数: {best_score:.4f}")
    print(f"模型类型: {master.agents['base'].model_type}")

if __name__ == "__main__":
    main()