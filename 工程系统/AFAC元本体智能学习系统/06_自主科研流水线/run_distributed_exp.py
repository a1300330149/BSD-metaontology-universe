import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import yaml
from src.master_agent.master_research_agent import MasterResearchAgent
from src.support.dist_comm import DistComm
from src.support.dist_scheduler import DistLoadScheduler

def main():
    dist_cfg = yaml.safe_load(open(os.path.join(BASE, "configs/dist_config.yaml"), "r", encoding="utf-8"))
    node_id = dist_cfg["current_node_id"]
    comm = DistComm(node_id, dist_cfg["port"])
    for n_info in dist_cfg["node_list"]:
        comm.register_node(n_info["nid"], n_info["ip"], n_info["port"])
    scheduler = DistLoadScheduler(comm)
    task_list = dist_cfg["task_splits"]
    for task_cfg in task_list:
        master = MasterResearchAgent(task_cfg)
        res = master.run_full_autonomous_research()
        scheduler.refresh_node_level(node_id, master.global_state)
        comm.sync_domain_prior(task_cfg["domain"], {"explore_rate": master.agents["opt"].explore_rate}, res["best_score"])

if __name__ == "__main__":
    main()