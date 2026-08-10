import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import yaml
from src.master_agent.master_research_agent import MasterResearchAgent
from src.support.result_generator import ResultGeneratorAgent

abl_group = [
    {"name": "完整全模块", "use_time": True, "use_illusion_cal": True, "use_human_evo": True},
    {"name": "移除时空衬层", "use_time": False, "use_illusion_cal": True, "use_human_evo": True},
    {"name": "移除虚实校准", "use_time": True, "use_illusion_cal": False, "use_human_evo": True},
    {"name": "移除人道自进化", "use_time": True, "use_illusion_cal": True, "use_human_evo": False},
    {"name": "无三大模块基线", "use_time": False, "use_illusion_cal": False, "use_human_evo": False},
]

def run_single_abl(cfg, group):
    cfg_copy = dict(cfg)
    cfg_copy["enable_time_layer"] = group["use_time"]
    cfg_copy["enable_kappa_cal"] = group["use_illusion_cal"]
    master = MasterResearchAgent(cfg_copy)
    master.enable_evo = group["use_human_evo"]
    if not group["use_illusion_cal"]:
        master.agents["reward"].kappa = 0.0
    res = master.run_full_autonomous_research()
    return {"group": group["name"], "metric": res}

def main():
    cfg_path = os.path.join(BASE, "configs/afac2026_default.yaml")
    raw_cfg = yaml.safe_load(open(cfg_path, "r", encoding="utf-8"))
    all_res = []
    report_gen = ResultGeneratorAgent()
    for g in abl_group:
        print(f"正在运行消融实验组：{g['name']}")
        group_result = run_single_abl(raw_cfg, g)
        all_res.append(group_result)
        print(f"  完成，最优分数：{group_result['metric']['best_score']:.4f}")
    report_gen.generate_ablation_report(all_res, save_path=os.path.join(BASE, "./output/ablation_summary.md"))
    print("\n消融实验完成，报表已保存")

if __name__ == "__main__":
    main()