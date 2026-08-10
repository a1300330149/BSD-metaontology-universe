"""
【归属基底：L0_总本源层·本源自激相变元机制】
【对应公理：本源自激相变终极公理·闭环验证】

ClosureJudgment —— 闭环判定器
验证自激相变是否形成完美自证闭环
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class ClosureJudgment(BaseTheoryModule):
    """闭环判定器"""

    module_id = "T29_C05"
    module_name = "闭环判定器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·本源自激相变元机制"
    corresponding_axiom = "本源自激相变终极公理·闭环自证"
    is_origin_locked = True
    dependencies = ["T29", "T29_C01", "T29_C02", "T29_C03", "T29_C04"]

    def __init__(self):
        super().__init__()
        self._judgments = []

    def judge_full_closure(self,
                           potential: float,
                           duality_conservation: bool,
                           realms_emerged: int,
                           zero_error: float) -> Dict[str, any]:
        """执行完整闭环判定"""
        checks = {
            "potential_sufficient": potential >= 0.95,
            "duality_conserved": duality_conservation,
            "realms_complete": realms_emerged == self.constants.NUM_REALMS,
            "zero_point_reached": zero_error < self.constants.theta_neg
        }
        all_pass = all(checks.values())
        score = sum(1 for v in checks.values() if v) / len(checks)
        judgment = {
            "checks": checks,
            "all_passed": all_pass,
            "closure_score": score,
            "closure_level": self._level_from_score(score),
            "verdict": "完美闭环" if all_pass else "闭环不完整"
        }
        self._judgments.append(judgment)
        return judgment

    def _level_from_score(self, score: float) -> str:
        if score >= 1.0:
            return "完美闭环（E3级）"
        elif score >= 0.85:
            return "高阶闭环（E2级）"
        elif score >= 0.6:
            return "基础闭环（E1级）"
        elif score >= 0.3:
            return "部分闭环"
        else:
            return "未闭环"

    def judge_self_excitation(self, cycle_count: int, entropy_history: List[float]) -> Dict[str, any]:
        """判定自激性：无需外因，自衍自证"""
        if len(entropy_history) < 2:
            return {"self_excited": False, "reason": "数据不足"}
        first_half = sum(entropy_history[:len(entropy_history)//2])
        second_half = sum(entropy_history[len(entropy_history)//2:])
        oscillatory = abs(first_half - second_half) < self.constants.theta_mv
        return {
            "cycle_count": cycle_count,
            "oscillatory": oscillatory,
            "self_excited": oscillatory and cycle_count >= 1,
            "verdict": "自激自证成立" if oscillatory else "需外部动因"
        }

    def get_closure_history(self) -> List[Dict]:
        """获取历史判定记录"""
        return list(self._judgments)

    def get_latest_judgment(self) -> Dict:
        """获取最新判定"""
        if self._judgments:
            return self._judgments[-1]
        return {}

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        # 闭环判定器自身无需额外约束
        return (len(errors) == 0, errors)
