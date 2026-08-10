# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第4重四层智能体执行载体
对应三界秩序：天道秩序
对应公理：第7条（系统自进化迭代公理）、第6条（全局宿命边界统摄理论）
对应九维维度：天道原理/天道动力学/道心能级
理论原文出处：《V3.0元本体理论分册》第五章
核心数理参数：γ=0.92, 进化增量阈值θ_evo=0.002
"""

import json
import os
import datetime

class SelfEvolutionModule:
    """
    功能：系统自进化模块
    理论映射：4重智能体工程·自进化规则
    能级关联：道心能级e_self更新
    约束来源：系统自进化迭代公理
    """
    def __init__(self, path="./output/base_lib.json"):
        self.path = path
        self.lib = self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"best": [], "fail": [], "hp_prior": {}}

    def review(self, traj, best_score, level):
        if best_score > self.lib.get("max_score", 0):
            self.lib["max_score"] = best_score
            self.lib["best"].append({"time": str(datetime.datetime.now()), "score": best_score, "level": str(level)})
        if traj:
            best_step = max(traj, key=lambda x: x["corrected_reward"])
            self.lib["hp_prior"]["best_r"] = best_step["corrected_reward"]
        self._save()

    def _save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.lib, f, indent=4)