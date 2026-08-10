# -*- coding: utf-8 -*-
# ======================================================
# 归属: 3重·六阶科研业务
# 对应公理: 无界递归, 对称破缺
# ======================================================
"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：创化社会/因果社会
理论原文出处：《V3.0元本体理论分册》第四章
核心数理参数：γ=0.92
"""

import os
import json
import datetime
from src.core.global_state import GlobalState

class ResultGeneratorAgent:
    """
    功能：实验结果生成器
    理论映射：3重六阶科研系统·结果输出规则
    能级关联：精神能级e_mind更新
    约束来源：科研动力学公理
    """
    def __init__(self, root="./output/reports"):
        self.root = root
        os.makedirs(root, exist_ok=True)

    def generate_full_report(self, res: dict, state: GlobalState):
        t = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        dir_out = os.path.join(self.root, t)
        os.makedirs(dir_out, exist_ok=True)
        txt_path = os.path.join(dir_out, "report.txt")
        vec = state.to_vector().flatten()
        names = ["元理天道", "动力天道", "相变自然", "载体实体", "创化社会", "因果社会", "肉身能级", "精神能级", "道心"]
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write("AFAC2026自主智能体实验报告\n")
            f.write(f"时间：{datetime.datetime.now()}\n最优分数：{res['best_score']:.4f}\n")
            for n, v in zip(names, vec):
                f.write(f"{n}:{v:.4f}\n")
        json.dump(res, open(os.path.join(dir_out, "metrics.json"), "w"), indent=4)
        return dir_out

    def generate_ablation_report(self, results: list, save_path: str):
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as f:
            f.write("# AFAC2026 消融实验对比报告\n\n")
            f.write(f"生成时间：{datetime.datetime.now()}\n\n")
            f.write("## 实验结果汇总\n\n")
            f.write("| 实验组 | 最优分数 | 变身等级 | 总步数 |\n")
            f.write("|--------|----------|----------|--------|\n")
            for r in results:
                group_name = r["group"]
                metric = r["metric"]
                best_score = metric.get("best_score", 0)
                level = str(metric.get("final_level", "N/A"))
                steps = metric.get("total_step", 0)
                f.write(f"| {group_name} | {best_score:.4f} | {level} | {steps} |\n")
            f.write("\n## 详细指标\n\n")
            for r in results:
                f.write(f"### {r['group']}\n\n")
                metric = r["metric"]
                f.write(f"- 最优分数: {metric.get('best_score', 0):.4f}\n")
                f.write(f"- 最终变身等级: {str(metric.get('final_level', 'N/A'))}\n")
                f.write(f"- 总步数: {metric.get('total_step', 0)}\n")
                f.write("\n")
        print(f"消融报告已保存至: {save_path}")