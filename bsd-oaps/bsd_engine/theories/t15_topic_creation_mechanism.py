"""
【归属基底：L1_法理层·选题创化生成机制】
【对应公理：选题创化生成机制（公理四）】

T15 —— 选题创化生成机制
S_{t+1} = f(S_t, ∇S_t)
选题状态依赖于当前状态与梯度
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class TopicCreationMechanism(BaseTheoryModule):
    """
    选题创化生成机制（公理四）

    核心方程：
    S_{t+1} = f(S_t, ∇S_t)

    S_t: 当前选题状态
    ∇S_t: 选题梯度（创新方向）
    f: 创化生成函数
    """

    module_id = "T15"
    module_name = "选题创化生成机制"
    version = "V1.0_终版"
    cosmic_level = 1
    base_belong = "L1_法理层·选题创化生成机制"
    corresponding_axiom = "选题创化生成机制（公理四）"
    is_origin_locked = True
    dependencies = ["T14"]

    def __init__(self):
        super().__init__()
        self._gradient_weight = self.constants.gamma
        self._inheritance_weight = 1 - self.constants.alpha
        self._innovation_rate = self.constants.theta_mv
        self._topic_dimensions = [
            "理论深度", "应用广度", "技术难度", "社会价值", "创新程度"
        ]

    def topic_generation_function(self, current_state: float = 0.5,
                                    gradient: float = 0.1) -> Dict[str, Any]:
        """选题生成函数推演"""
        next_state = (self._inheritance_weight * current_state +
                     self._gradient_weight * gradient)

        innovation_component = self._innovation_rate * abs(gradient)

        net_innovation = next_state - current_state

        is_innovative = net_innovation > self.constants.theta_neg

        return {
            "current_state_S_t": current_state,
            "gradient_∇S_t": gradient,
            "next_state_S_t1": next_state,
            "innovation_component": innovation_component,
            "net_innovation": net_innovation,
            "is_innovative": is_innovative,
            "formula": "S_{t+1} = α·S_t + β·∇S_t",
            "inheritance_weight": self._inheritance_weight,
            "gradient_weight": self._gradient_weight
        }

    def gradient_driven_mechanism(self, position: float = 0.3,
                                   learning_rate: float = 0.01) -> Dict[str, Any]:
        """梯度驱动机制推演"""
        potential_peak = self.constants.E3
        gradient = (potential_peak - position) * self._gradient_weight

        step_size = learning_rate * gradient
        new_position = position + step_size

        convergence_rate = 1 - learning_rate * self._gradient_weight

        return {
            "current_position": position,
            "gradient": gradient,
            "step_size": step_size,
            "new_position": new_position,
            "learning_rate": learning_rate,
            "convergence_rate": convergence_rate,
            "potential_peak": potential_peak,
            "mechanism": "沿价值梯度方向攀升，梯度越大进步越快"
        }

    def creation_inheritance_balance(self, creation_ratio: float = 0.3) -> Dict[str, Any]:
        """创生与继承平衡推演"""
        inheritance_ratio = 1 - creation_ratio

        if creation_ratio > self.constants.E2:
            balance_type = "激进创新型"
            risk_level = "高风险"
        elif creation_ratio > self.constants.E1:
            balance_type = "均衡创生型"
            risk_level = "中风险"
        else:
            balance_type = "稳健继承型"
            risk_level = "低风险"

        optimal_ratio = self.constants.alpha

        distance_to_optimal = abs(creation_ratio - optimal_ratio)

        return {
            "creation_ratio": creation_ratio,
            "inheritance_ratio": inheritance_ratio,
            "optimal_ratio": optimal_ratio,
            "distance_to_optimal": distance_to_optimal,
            "balance_type": balance_type,
            "risk_level": risk_level,
            "balance_principle": "无继承则无根，无创生则不进，二者需平衡"
        }

    def topic_iteration_model(self, iterations: int = 5,
                                initial_state: float = 0.2) -> Dict[str, Any]:
        """选题迭代模型推演"""
        trajectory = []
        state = initial_state

        for i in range(iterations):
            gradient = (self.constants.E3 - state) * self._gradient_weight * 0.1
            result = self.topic_generation_function(state, gradient)
            next_state = result["next_state_S_t1"]

            trajectory.append({
                "iteration": i + 1,
                "state_before": round(state, 6),
                "gradient": round(gradient, 6),
                "state_after": round(next_state, 6),
                "innovation": round(next_state - state, 6)
            })

            state = next_state

        total_innovation = state - initial_state

        return {
            "trajectory": trajectory,
            "total_iterations": iterations,
            "initial_state": initial_state,
            "final_state": state,
            "total_innovation": total_innovation,
            "model": "梯度驱动的迭代创生模型"
        }

    def cross_innovation_mechanism(self, field_a: float = 0.6,
                                    field_b: float = 0.5,
                                    cross_degree: float = 0.4) -> Dict[str, Any]:
        """交叉创新机制推演"""
        base_value = max(field_a, field_b)
        cross_bonus = min(field_a, field_b) * cross_degree * self._gradient_weight
        cross_value = base_value + cross_bonus

        synergy = cross_value - (field_a + field_b) / 2

        is_synergistic = synergy > self.constants.theta_neg

        return {
            "field_a_value": field_a,
            "field_b_value": field_b,
            "cross_degree": cross_degree,
            "cross_value": cross_value,
            "cross_bonus": cross_bonus,
            "synergy_effect": synergy,
            "is_synergistic": is_synergistic,
            "mechanism": "交叉领域产生协同效应，1+1>2的创新涌现"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T15 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if self._gradient_weight <= 0:
            errors.append("梯度权重必须大于0")
        if self._inheritance_weight <= 0 or self._inheritance_weight >= 1:
            errors.append("继承权重必须在(0,1)之间")
        if len(self._topic_dimensions) < 3:
            errors.append("选题维度至少应有3个")
        if "T14" not in self.dependencies:
            errors.append("T15必须依赖T14（科研价值边际）")
        if len(self.dependencies) < 1:
            errors.append("T15至少应有1个依赖")
        if self.cosmic_level != 1:
            errors.append("T15必须位于L1法理层")
        if not self.is_origin_locked:
            errors.append("T15法理理论必须锁定")
        if not hasattr(self, 'topic_generation_function'):
            errors.append("必须实现选题生成函数方法")
        if not hasattr(self, 'gradient_driven_mechanism'):
            errors.append("必须实现梯度驱动机制方法")
        if not hasattr(self, 'creation_inheritance_balance'):
            errors.append("必须实现创生与继承平衡方法")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t15 = TopicCreationMechanism()
    print(f"模块: {t15.module_id} - {t15.module_name}")
    print(f"版本: {t15.version}")
    print(f"层级: L{t15.cosmic_level}")
    print(f"依赖: {t15.dependencies}")
    print(f"锁定: {t15.is_origin_locked}")
    print(f"哈希: {t15.sha256}")
    print()

    print("选题生成函数:")
    gen = t15.topic_generation_function(0.5, 0.1)
    print(f"  当前状态: {gen['current_state_S_t']}")
    print(f"  下一状态: {gen['next_state_S_t1']:.6f}")
    print(f"  净创新: {gen['net_innovation']:.6f}")
    print()

    print("梯度驱动:")
    grad = t15.gradient_driven_mechanism(0.3, 0.01)
    print(f"  梯度值: {grad['gradient']:.6f}")
    print(f"  步长: {grad['step_size']:.6f}")
    print()

    print("创生继承平衡:")
    bal = t15.creation_inheritance_balance(0.3)
    print(f"  创生占比: {bal['creation_ratio']}")
    print(f"  继承占比: {bal['inheritance_ratio']}")
    print(f"  平衡类型: {bal['balance_type']}")
    print()

    print("交叉创新:")
    cross = t15.cross_innovation_mechanism(0.6, 0.5, 0.4)
    print(f"  交叉价值: {cross['cross_value']:.6f}")
    print(f"  协同效应: {cross['synergy_effect']:.6f}")
    print()

    valid, errs = t15.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
