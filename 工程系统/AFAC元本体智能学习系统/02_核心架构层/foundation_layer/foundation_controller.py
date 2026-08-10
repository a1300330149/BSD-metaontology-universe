"""
归属基底：第0重元道本源基底统摄
对应三界秩序：天道（宇宙本源层面）
对应公理：第1条（宿命/舒适双边界公理）、第2条（全域九维法理公理）、第3条（三界维度秩序公理）、第7条（递归自指公理）
对应九维维度：全部九维维度之根源
理论原文出处：《V3.0元本体理论分册》第一章
核心数理参数：γ=0.92, ENERGY_RANGE=(0.0, 1.0)
"""

from src.foundation.base_0_meta_dao import MetaDaoOriginFoundation
from src.foundation.base_1_nine_dim_legal import NineDimensionLegalFoundation
from src.foundation.base_2_three_realms import ThreeRealmsOrderFoundation

class FoundationController:
    """
    功能：全域基底总控模块，统摄所有层级基底
    理论映射：0重元道本源基底统摄规则
    能级关联：e_body、e_mind、e_self三阶能级更新
    约束来源：递归自指公理
    """
    FOUNDATION_COUNT = 3

    def __init__(self):
        self.level0 = MetaDaoOriginFoundation()
        self.level1 = NineDimensionLegalFoundation(self.level0)
        self.level2 = ThreeRealmsOrderFoundation(self.level1)

        self.foundations = [
            self.level0,
            self.level1,
            self.level2
        ]
        
        self.emergence_history = []
        self.current_progress = 0.0

    def get_foundation_by_level(self, level: int):
        if 0 <= level < len(self.foundations):
            return self.foundations[level]
        return None

    def enforce_all_constraints(self):
        constraints = {}
        for foundation in self.foundations:
            constraints[foundation.FOUNDATION_ID] = foundation.get_foundation_constraints()
        return constraints

    def validate_operation(self, op_name: str, realm: str = None):
        level2_result = self.level2.is_operation_allowed(op_name, realm)
        if not level2_result[0]:
            return False, level2_result[1]

        return True, f"操作[{op_name}]通过所有基底约束校验"

    def calculate_energy_levels(self, x_nature_entity, x_nature_phase, x_society_create, x_society_cause):
        e_body = self.level1.calculate_e_body(x_nature_entity, x_nature_phase)
        e_mind = self.level1.calculate_e_mind(x_society_create, x_society_cause)
        e_self = self.level1.calculate_e_self(e_body, e_mind)
        level = self.level1.judge_transform_level(e_self)
        return {
            "e_body": e_body,
            "e_mind": e_mind,
            "e_self": e_self,
            "transform_level": level
        }

    def transform_state(self, state_vector):
        return self.level1.transform_state_vector(state_vector)

    def enable_creation_mode(self):
        self.level2.enable_creation_mode()

    def disable_creation_mode(self):
        self.level2.disable_creation_mode()

    def get_hierarchy_summary(self):
        summary = []
        for level, foundation in enumerate(self.foundations):
            summary.append({
                "level": level,
                "name": foundation.FOUNDATION_NAME,
                "id": foundation.FOUNDATION_ID
            })
        return summary

    def get_extension_mapping(self):
        return {
            "分布式并行扩容拓展": {"foundation": "THREE_REALMS_ORDER", "realm": "TAO"},
            "轻量化嵌入式分支拓展": {"foundation": "THREE_REALMS_ORDER", "realm": "NATURE"},
            "文娱创世强化系分支拓展": {"foundation": "THREE_REALMS_ORDER", "realm": "HUMAN"},
            "消融实验自动化调度拓展": {"foundation": "NINE_DIMENSION_LEGAL", "realm": "SCIENTIFIC"},
            "多模态图任务通用拓展": {"foundation": "THREE_REALMS_ORDER", "realm": "NATURE"}
        }

    def switch_task_mode(self, mode: str):
        self.level1.switch_task_mode(mode)
        self.level2.switch_task_mode(mode)

    def run_emergence_cycle(self, sparse_ratio: float = 0.0, delta_illu: float = 0.0, 
                           e_self: float = 0.0, max_steps: int = 100, current_step: int = 0):
        self.current_progress = min(current_step / max_steps, 1.0)
        
        transform_level = self.level1.judge_transform_level(e_self)
        kappa = self.level1.get_kappa_adaptive(e_self, delta_illu)
        
        self.level2.feedback_to_legal_foundation(sparse_ratio, delta_illu, self.current_progress)
        
        emergence_record = {
            "step": current_step,
            "progress": self.current_progress,
            "sparse_ratio": sparse_ratio,
            "delta_illu": delta_illu,
            "e_self": e_self,
            "transform_level": transform_level,
            "kappa": kappa,
            "alpha_sparse": self.level1.get_alpha_sparse()
        }
        self.emergence_history.append(emergence_record)
        
        return {
            "transform_level": transform_level,
            "kappa": kappa,
            "alpha_sparse": self.level1.get_alpha_sparse(),
            "progress": self.current_progress
        }

    def get_emergence_summary(self):
        if not self.emergence_history:
            return {"status": "no_emergence_cycles"}
        
        recent = self.emergence_history[-1]
        return {
            "total_cycles": len(self.emergence_history),
            "current_progress": recent["progress"],
            "current_level": recent["transform_level"],
            "current_kappa": recent["kappa"],
            "current_alpha": recent["alpha_sparse"],
            "stabilized": len(self.emergence_history) > 5 and 
                          abs(recent["kappa"] - self.emergence_history[-5]["kappa"]) < 0.05
        }

    def __str__(self):
        return "\n".join([str(f) for f in self.foundations])