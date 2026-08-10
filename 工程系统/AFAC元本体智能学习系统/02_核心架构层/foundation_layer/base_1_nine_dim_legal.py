"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道/自然/人道（统一法理层面）
对应公理：第2条（全域九维法理公理）、第4条（双边界守恒公理）、第5条（科研动力学公理）、第6条（相变临界公理）
对应九维维度：元理天道/动力天道/相变自然/载体实体/创化社会/因果社会/肉身能级/精神能级/道心总能级
理论原文出处：《V3.0元本体理论分册》第二章
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, κ=0.35/0.42, α=0.18

本模块实现九维法理基底，是元道本源分化出的第一重可量化基底，宇宙维度通用底层数学规则。

理论映射：
- 九维向量：对应全域九维法理公理（公理二）
- 流转矩阵：对应科研动力学公理（公理五）
- 变身阈值：对应相变临界公理（公理六）
"""

import numpy as np
from src.foundation.base_0_meta_dao import MetaDaoOriginFoundation

class NineDimensionLegalFoundation:
    """
    功能：全域九维法理基底管理
    理论映射：规则相位位（第二位）·宇宙维度数学规则
    约束来源：全域九维法理公理（公理二）

    第1重基底：全域九维法理基底
    元道本源分化出的第一重可量化基底
    宇宙维度通用底层数学规则
    """
    FOUNDATION_ID = "NINE_DIMENSION_LEGAL"
    FOUNDATION_LEVEL = 1
    FOUNDATION_NAME = "全域九维法理基底"

    DIMENSION_NAMES = [
        "元理天道",
        "动力天道",
        "相变自然",
        "载体实体",
        "创化社会",
        "因果社会",
        "肉身能级",
        "精神能级",
        "道心总能级"
    ]

    TRANSFORM_THRESHOLDS = {
        "E1": 0.35,
        "E2": 0.65,
        "E3": 0.90
    }

    ENERGY_FORMULAS = {
        "e_body": "0.6 * x_nature_entity + 0.4 * x_nature_phase + α * sparse_ratio",
        "e_mind": "0.4 * x_society_create + 0.6 * x_society_cause",
        "e_self": "0.4 * E_body + 0.6 * E_mind"
    }

    COMPETITION_PARAMS = {
        "alpha_sparse": 0.30,
        "kappa_base": 0.42,
        "kappa_by_level": {
            "NONE": 0.30,
            "FIRST_BODY": 0.35,
            "SECOND_MIND": 0.42,
            "THIRD_TAO": 0.50
        },
        "flow_matrix_adjustments": {
            (4, 2): 0.72,
            (5, 3): 0.81
        }
    }

    RESEARCH_PARAMS = {
        "alpha_sparse": 0.0,
        "kappa_base": 0.35,
        "kappa_by_level": {
            "NONE": 0.25,
            "FIRST_BODY": 0.35,
            "SECOND_MIND": 0.35,
            "THIRD_TAO": 0.40
        },
        "flow_matrix_adjustments": {}
    }

    def __init__(self, meta_dao: MetaDaoOriginFoundation = None, task_mode: str = "research"):
        self.meta_dao = meta_dao or MetaDaoOriginFoundation()
        self.dimension_count = 9
        self.task_mode = task_mode.lower()
        base_params = self.COMPETITION_PARAMS if self.task_mode == "competition" else self.RESEARCH_PARAMS
        self.current_params = {
            "alpha_sparse": base_params["alpha_sparse"],
            "kappa_base": base_params["kappa_base"],
            "kappa_by_level": base_params["kappa_by_level"].copy(),
            "flow_matrix_adjustments": base_params["flow_matrix_adjustments"].copy()
        }
        self.ablation_masks = np.ones((9, 9))
        self._build_flow_matrix()

    def _build_flow_matrix(self):
        self.M7_base = np.zeros((9, 9))
        self.M7_base[2, 1] = 0.8
        self.M7_base[3, 1] = 0.7
        self.M7_base[4, 2] = 0.6
        self.M7_base[5, 3] = 0.7
        self.M7_base[6, 3] = 0.5
        self.M7_base[7, 5] = 0.6
        self.M7_base[8, 6] = 0.4
        self.M7_base[8, 7] = 0.5
        self.M7_base[1, 5] = 0.3

        self.M7 = self.M7_base.copy()

        if self.task_mode == "competition":
            for (i, j), value in self.COMPETITION_PARAMS["flow_matrix_adjustments"].items():
                self.M7[i, j] = value

        self.M7 = self.meta_dao.enforce_conservation(self.M7)

    def switch_task_mode(self, mode: str):
        self.task_mode = mode.lower()
        base_params = self.COMPETITION_PARAMS if self.task_mode == "competition" else self.RESEARCH_PARAMS
        self.current_params = {
            "alpha_sparse": base_params["alpha_sparse"],
            "kappa_base": base_params["kappa_base"],
            "kappa_by_level": base_params["kappa_by_level"].copy(),
            "flow_matrix_adjustments": base_params["flow_matrix_adjustments"].copy()
        }
        self._build_flow_matrix()

    def set_ablation_mask(self, dimension: int, enable: bool):
        if 0 <= dimension < 9:
            self.ablation_masks[dimension, :] = 1.0 if enable else 0.0
            self.ablation_masks[:, dimension] = 1.0 if enable else 0.0

    def get_kappa(self, transform_level: str = "NONE"):
        kappa_map = self.current_params.get("kappa_by_level", {})
        return kappa_map.get(transform_level, self.current_params.get("kappa_base", 0.35))

    def get_kappa_adaptive(self, e_self: float, delta_illu: float = 0.0):
        transform_level = self.judge_transform_level(e_self)
        base_kappa = self.get_kappa(transform_level)
        
        if delta_illu > 0:
            illu_factor = min(delta_illu * 2, 0.2)
            return min(base_kappa + illu_factor, 0.9)
        return base_kappa

    def get_alpha_sparse(self):
        return self.current_params["alpha_sparse"]

    def update_alpha_sparse(self, sparse_ratio: float):
        if self.task_mode == "competition":
            # 稀疏补偿系数α，规则相位位（第二位），赛题稀疏竞赛专用值0.18，不可调整
            base_alpha = 0.18
            adjusted_alpha = base_alpha * (1 + sparse_ratio * 0.5)
            self.current_params["alpha_sparse"] = min(adjusted_alpha, 0.35)

    def update_kappa_by_illusion(self, delta_illu: float):
        kappa_map = self.current_params.get("kappa_by_level", {})
        for level in kappa_map:
            base_kappa = kappa_map[level]
            adjustment = min(delta_illu * 1.5, 0.15)
            kappa_map[level] = min(base_kappa + adjustment, 0.9)

    def update_flow_matrix_strength(self, progress: float):
        for (i, j) in self.current_params.get("flow_matrix_adjustments", {}):
            base_val = self.M7_base[i, j]
            target_val = self.current_params["flow_matrix_adjustments"][(i, j)]
            self.M7[i, j] = base_val + (target_val - base_val) * progress
        self.M7 = self.meta_dao.enforce_conservation(self.M7)

    def calculate_e_body(self, x_nature_entity, x_nature_phase, sparse_ratio: float = 0.0):
        base_value = 0.6 * x_nature_entity + 0.4 * x_nature_phase
        if self.task_mode == "competition":
            base_value += self.current_params["alpha_sparse"] * sparse_ratio
        return self.meta_dao.clamp_energy(base_value)

    def calculate_e_mind(self, x_society_create, x_society_cause):
        return self.meta_dao.clamp_energy(0.4 * x_society_create + 0.6 * x_society_cause)

    def calculate_e_self(self, e_body, e_mind):
        return self.meta_dao.clamp_energy(0.4 * e_body + 0.6 * e_mind)

    def judge_transform_level(self, e_self):
        if e_self >= self.TRANSFORM_THRESHOLDS["E3"]:
            return "THIRD_TAO"
        elif e_self >= self.TRANSFORM_THRESHOLDS["E2"]:
            return "SECOND_MIND"
        elif e_self >= self.TRANSFORM_THRESHOLDS["E1"]:
            return "FIRST_BODY"
        return "NONE"

    def transform_state_vector(self, vec):
        M7_effective = self.M7 * self.ablation_masks
        new_vec = M7_effective @ vec
        for i in range(len(new_vec)):
            new_vec[i] = self.meta_dao.clamp_energy(float(new_vec[i][0]))
        return new_vec

    def export_state_vector(self, vec):
        export_data = {}
        for i, name in enumerate(self.DIMENSION_NAMES):
            export_data[name] = float(vec[i][0])
        return export_data

    def get_foundation_constraints(self):
        return {
            "must_use_nine_dim_vector": True,
            "energy_formulas_unchangeable": True,
            "flow_matrix_adjustable_by_mode": True,
            "transform_thresholds_fixed": True,
            "all_operations_map_to_nine_dim": True,
            "ablation_supported": True,
            "task_mode": self.task_mode,
            "current_params": self.current_params
        }

    def __str__(self):
        return f"{self.FOUNDATION_NAME} (第{self.FOUNDATION_LEVEL}重, 模式:{self.task_mode})"