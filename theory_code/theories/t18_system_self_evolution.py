"""
【归属基底：L1_法理层·系统自进化迭代公理】
【对应公理：系统自进化迭代公理（公理七）】

T18 —— 系统自进化迭代公理
Δ_evo ≥ θ_evo = 0.002，每轮进化增量需达阈值
系统自进化、迭代阈值、进化方向、进化速率、进化停滞判定
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class SystemSelfEvolution(BaseTheoryModule):
    """
    系统自进化迭代公理（公理七）

    核心阈值：
    θ_evo = 0.002

    判定法则：
    当 Δ_evo ≥ θ_evo 时，系统处于进化状态
    否则判定为进化停滞，需启动重启机制
    """

    module_id = "T18"
    module_name = "系统自进化迭代公理"
    version = "V1.0_终版"
    cosmic_level = 1
    base_belong = "L1_法理层·系统自进化迭代公理"
    corresponding_axiom = "系统自进化迭代公理（公理七）"
    is_origin_locked = True
    dependencies = ["T10", "T17"]

    def __init__(self):
        super().__init__()
        self._theta_evo = self.constants.theta_evo
        self._evolution_rate = self.constants.alpha
        self._direction_bias = self.constants.gamma
        self._stagnation_threshold = 3
        self._evolution_dimensions = [
            "复杂度", "有序度", "适应性", "自组织性", "创新能力"
        ]

    def self_evolution_equation(self, current_level: float = 0.5,
                                  generations: int = 10) -> Dict[str, Any]:
        """自进化方程推演"""
        trajectory = []
        level = current_level

        for gen in range(generations):
            delta_evo = self._evolution_rate * level * (1 - level)
            if delta_evo < self._theta_evo:
                delta_evo = self._theta_evo * 0.5

            new_level = level + delta_evo

            trajectory.append({
                "generation": gen + 1,
                "level_before": round(level, 6),
                "delta_evo": round(delta_evo, 6),
                "level_after": round(new_level, 6),
                "meets_threshold": delta_evo >= self._theta_evo
            })

            level = new_level

        total_evolution = level - current_level

        return {
            "initial_level": current_level,
            "final_level": level,
            "total_evolution": total_evolution,
            "generations": generations,
            "trajectory": trajectory,
            "theta_evo": self._theta_evo,
            "equation": "Δ_evo = α · L · (1-L)  (逻辑斯蒂增长)"
        }

    def iteration_threshold_judgment(self, delta_evo: float = 0.0015) -> Dict[str, Any]:
        """迭代阈值判定推演"""
        meets_threshold = delta_evo >= self._theta_evo
        ratio = delta_evo / self._theta_evo if self._theta_evo > 0 else float('inf')
        gap = delta_evo - self._theta_evo

        if ratio >= 2.0:
            status = "高速进化"
            action = "保持势头，加速迭代"
        elif ratio >= 1.0:
            status = "正常进化"
            action = "稳步推进，持续优化"
        elif ratio >= 0.5:
            status = "低速进化"
            action = "注入动能，防止停滞"
        else:
            status = "进化停滞"
            action = "启动重启机制"

        return {
            "delta_evo": delta_evo,
            "theta_evo": self._theta_evo,
            "ratio": ratio,
            "gap": gap,
            "meets_threshold": meets_threshold,
            "evolution_status": status,
            "recommended_action": action,
            "judgment_rule": "Δ_evo ≥ θ_evo 为有效进化，否则停滞"
        }

    def evolution_rate_calculation(self, start_level: float = 0.4,
                                     end_level: float = 0.6,
                                     time_steps: int = 100) -> Dict[str, Any]:
        """进化速率计算"""
        total_delta = end_level - start_level
        avg_rate = total_delta / time_steps if time_steps > 0 else 0
        instantaneous_rate = self._evolution_rate * start_level * (1 - start_level)

        if avg_rate >= self._theta_evo:
            health = "健康"
        else:
            health = "亚健康"

        doubling_time = math.log(2) / avg_rate if avg_rate > 0 else float('inf')

        return {
            "start_level": start_level,
            "end_level": end_level,
            "time_steps": time_steps,
            "total_delta": total_delta,
            "average_rate": avg_rate,
            "instantaneous_rate": instantaneous_rate,
            "doubling_time": doubling_time,
            "evolution_health": health,
            "formula": "r_avg = ΔL / Δt"
        }

    def evolution_direction_selection(self, directions: List[str] = None) -> Dict[str, Any]:
        """进化方向选择推演"""
        if directions is None:
            directions = ["复杂度提升", "效率优化", "适应性增强", "创新性突破"]

        direction_scores = {}
        for i, d in enumerate(directions):
            base_score = self.constants.E1 + i * 0.1
            if base_score > self.constants.E3:
                base_score = self.constants.E3
            direction_scores[d] = {
                "score": round(base_score, 4),
                "bias": round(self._direction_bias, 4),
                "weighted_score": round(base_score * self._direction_bias, 4)
            }

        best_direction = max(direction_scores.items(), key=lambda x: x[1]["weighted_score"])

        return {
            "available_directions": directions,
            "direction_scores": direction_scores,
            "best_direction": best_direction[0],
            "best_score": best_direction[1]["weighted_score"],
            "selection_principle": "选择加权得分最高的方向作为进化主方向",
            "direction_count": len(directions)
        }

    def stagnation_and_restart_mechanism(self, stagnation_count: int = 4) -> Dict[str, Any]:
        """停滞与重启机制推演"""
        is_stagnant = stagnation_count >= self._stagnation_threshold

        if stagnation_count == 0:
            phase = "正常进化"
            action = "持续迭代"
        elif stagnation_count < self._stagnation_threshold:
            phase = "停滞预警"
            action = "注入外部刺激"
        elif stagnation_count < self._stagnation_threshold * 2:
            phase = "停滞确认"
            action = "启动重启"
        else:
            phase = "深度停滞"
            action = "范式迁移"

        restart_intensity = min(1.0, stagnation_count / (self._stagnation_threshold * 2))
        energy_required = restart_intensity * self.constants.E3

        return {
            "stagnation_count": stagnation_count,
            "stagnation_threshold": self._stagnation_threshold,
            "is_stagnant": is_stagnant,
            "stagnation_phase": phase,
            "recommended_action": action,
            "restart_intensity": restart_intensity,
            "energy_required": energy_required,
            "mechanism": "连续多轮不达标判定为停滞，根据程度启动不同级别重启"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T18 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if self._theta_evo != self.constants.theta_evo:
            errors.append("进化阈值必须等于constants.theta_evo")
        if self._theta_evo <= 0:
            errors.append("进化阈值必须大于0")
        if self._stagnation_threshold < 1:
            errors.append("停滞阈值必须至少为1")
        if len(self._evolution_dimensions) < 3:
            errors.append("进化维度至少应有3个")
        if "T10" not in self.dependencies:
            errors.append("T18必须依赖T10（闭环递归）")
        if "T17" not in self.dependencies:
            errors.append("T18必须依赖T17（全局宿命边界）")
        if self.cosmic_level != 1:
            errors.append("T18必须位于L1法理层")
        if not self.is_origin_locked:
            errors.append("T18法理理论必须锁定")
        if not hasattr(self, 'self_evolution_equation'):
            errors.append("必须实现自进化方程方法")
        if not hasattr(self, 'iteration_threshold_judgment'):
            errors.append("必须实现迭代阈值判定方法")
        if not hasattr(self, 'stagnation_and_restart_mechanism'):
            errors.append("必须实现停滞与重启机制方法")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t18 = SystemSelfEvolution()
    print(f"模块: {t18.module_id} - {t18.module_name}")
    print(f"版本: {t18.version}")
    print(f"层级: L{t18.cosmic_level}")
    print(f"依赖: {t18.dependencies}")
    print(f"锁定: {t18.is_origin_locked}")
    print(f"哈希: {t18.sha256}")
    print()

    print("自进化方程:")
    evo = t18.self_evolution_equation(0.5, 5)
    print(f"  初始等级: {evo['initial_level']}")
    print(f"  最终等级: {evo['final_level']:.6f}")
    print(f"  总进化量: {evo['total_evolution']:.6f}")
    print()

    print("迭代阈值判定:")
    th = t18.iteration_threshold_judgment(0.0015)
    print(f"  Δ_evo: {th['delta_evo']}")
    print(f"  θ_evo: {th['theta_evo']}")
    print(f"  状态: {th['evolution_status']}")
    print(f"  达标: {th['meets_threshold']}")
    print()

    print("进化速率:")
    rate = t18.evolution_rate_calculation(0.4, 0.6, 100)
    print(f"  平均速率: {rate['average_rate']:.6f}")
    print(f"  健康度: {rate['evolution_health']}")
    print()

    print("停滞重启机制:")
    stag = t18.stagnation_and_restart_mechanism(4)
    print(f"  停滞轮数: {stag['stagnation_count']}")
    print(f"  停滞阶段: {stag['stagnation_phase']}")
    print(f"  建议动作: {stag['recommended_action']}")
    print()

    valid, errs = t18.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
