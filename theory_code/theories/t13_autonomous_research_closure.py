"""
【归属基底：L1_法理层·自主科研闭环动力学公理】
【对应公理：自主科研闭环动力学公理（公理二）】

T13 —— 自主科研闭环动力学公理
二阶微分方程：d²R/dt² + γ dR/dt + κR = F
科研闭环自驱振荡，阻尼振动模型
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class AutonomousResearchClosure(BaseTheoryModule):
    """
    自主科研闭环动力学公理（公理二）

    核心方程：
    d²R/dt² + γ dR/dt + κR = F(t)

    R: 科研进展
    γ: 阻尼系数（衰减）
    κ: 回复系数（惯性）
    F(t): 外部驱动力
    """

    module_id = "T13"
    module_name = "自主科研闭环动力学公理"
    version = "V1.0_终版"
    cosmic_level = 1
    base_belong = "L1_法理层·自主科研闭环动力学公理"
    corresponding_axiom = "自主科研闭环动力学公理（公理二）"
    is_origin_locked = True
    dependencies = ["T10", "T12"]

    def __init__(self):
        super().__init__()
        self._gamma_damping = self.constants.alpha
        self._kappa_restoring = self.constants.kappa
        self._driving_force = self.constants.gamma
        self._research_stages = [
            "选题", "调研", "创新", "验证", "落地", "复盘"
        ]
        self._initial_R = 0.1
        self._initial_dRdt = 0.0

    def closure_dynamics_equation(self, t: float = 1.0) -> Dict[str, Any]:
        """闭环动力学方程推演"""
        gamma = self._gamma_damping
        kappa = self._kappa_restoring
        F0 = self._driving_force

        omega0 = math.sqrt(kappa)
        zeta = gamma / (2 * omega0)

        if zeta < 1:
            omega_d = omega0 * math.sqrt(1 - zeta**2)
            decay = math.exp(-zeta * omega0 * t)
            oscillation = math.cos(omega_d * t)
            R_t = decay * oscillation * self._initial_R
            dRdt = -zeta * omega0 * R_t - omega_d * decay * math.sin(omega_d * t) * self._initial_R
            d2Rdt2 = F0 - gamma * dRdt - kappa * R_t
            regime = "欠阻尼振荡"
        elif zeta == 1:
            decay = math.exp(-omega0 * t)
            R_t = decay * (self._initial_R + (self._initial_dRdt + omega0 * self._initial_R) * t)
            dRdt = -omega0 * R_t + decay * (self._initial_dRdt + omega0 * self._initial_R)
            d2Rdt2 = F0 - gamma * dRdt - kappa * R_t
            regime = "临界阻尼"
        else:
            r1 = -omega0 * (zeta + math.sqrt(zeta**2 - 1))
            r2 = -omega0 * (zeta - math.sqrt(zeta**2 - 1))
            R_t = self._initial_R * math.exp(r1 * t)
            dRdt = r1 * R_t
            d2Rdt2 = F0 - gamma * dRdt - kappa * R_t
            regime = "过阻尼"

        return {
            "time": t,
            "R_t": R_t,
            "dRdt": dRdt,
            "d2Rdt2": d2Rdt2,
            "gamma_damping": gamma,
            "kappa_restoring": kappa,
            "driving_force": F0,
            "natural_frequency": omega0,
            "damping_ratio": zeta,
            "regime": regime,
            "equation": "d²R/dt² + γ·dR/dt + κ·R = F(t)"
        }

    def damped_oscillation_model(self, total_steps: int = 10) -> Dict[str, Any]:
        """阻尼振动模型"""
        gamma = self._gamma_damping
        kappa = self._kappa_restoring
        omega0 = math.sqrt(kappa)
        zeta = gamma / (2 * omega0)

        trajectory = []
        R = self._initial_R
        dRdt = self._initial_dRdt
        dt = 0.1

        for step in range(total_steps):
            t = step * dt
            d2Rdt2 = self._driving_force - gamma * dRdt - kappa * R
            dRdt += d2Rdt2 * dt
            R += dRdt * dt
            trajectory.append({
                "step": step + 1,
                "time": round(t, 2),
                "R": round(R, 6),
                "dRdt": round(dRdt, 6)
            })

        steady_state_R = self._driving_force / kappa if kappa > 0 else 0

        return {
            "trajectory": trajectory,
            "total_steps": total_steps,
            "gamma": gamma,
            "kappa": kappa,
            "damping_ratio": zeta,
            "steady_state_R": steady_state_R,
            "model": "二阶阻尼振动系统"
        }

    def gamma_kappa_parameters(self) -> Dict[str, Any]:
        """γ衰减/κ阻尼参数分析"""
        gamma = self._gamma_damping
        kappa = self._kappa_restoring
        omega0 = math.sqrt(kappa)
        zeta = gamma / (2 * omega0)

        return {
            "gamma_damping": {
                "value": gamma,
                "meaning": "γ阻尼系数：代表科研中的阻力、衰减、耗散",
                "source": "认知负荷、资源限制、信息熵增"
            },
            "kappa_restoring": {
                "value": kappa,
                "meaning": "κ回复系数：代表科研中的惯性、韧性、回归趋势",
                "source": "知识积累、方法成熟、范式稳定"
            },
            "derived": {
                "natural_frequency": omega0,
                "damping_ratio": zeta,
                "quality_factor": 1 / (2 * zeta) if zeta > 0 else float('inf'),
                "period": 2 * math.pi / omega0 if omega0 > 0 else float('inf')
            },
            "parameter_meaning": "γ控制衰减速度，κ控制振荡频率，二者共同决定系统动力学行为"
        }

    def research_six_stage_correspondence(self) -> Dict[str, Any]:
        """科研六阶架构对应"""
        stage_dynamics = {}
        for i, stage in enumerate(self._research_stages):
            phase_angle = i * math.pi / 3
            velocity = math.sin(phase_angle) * self._driving_force
            acceleration = math.cos(phase_angle) * self._driving_force
            stage_dynamics[stage] = {
                "order": i + 1,
                "phase": f"{i*60}°",
                "velocity_factor": round(velocity, 4),
                "acceleration_factor": round(acceleration, 4),
                "dominant_term": "位能主导" if abs(math.cos(phase_angle)) > abs(math.sin(phase_angle)) else "动能主导"
            }

        return {
            "six_stages": self._research_stages,
            "stage_dynamics": stage_dynamics,
            "correspondence_principle": "科研六阶对应振荡六相，形成完整闭环动力学",
            "cycle_count": 6
        }

    def steady_state_solution_analysis(self) -> Dict[str, Any]:
        """稳态解分析"""
        gamma = self._gamma_damping
        kappa = self._kappa_restoring
        F0 = self._driving_force

        if kappa > 0:
            steady_R = F0 / kappa
            steady_dRdt = 0.0
            steady_d2Rdt2 = 0.0
        else:
            steady_R = float('inf')
            steady_dRdt = F0 / gamma if gamma > 0 else float('inf')
            steady_d2Rdt2 = 0.0

        stability = "稳定" if gamma > 0 and kappa > 0 else "不稳定"

        return {
            "steady_state_R": steady_R,
            "steady_state_dRdt": steady_dRdt,
            "steady_state_d2Rdt2": steady_d2Rdt2,
            "stability": stability,
            "convergence_condition": "γ > 0 且 κ > 0",
            "time_constant": 2 * gamma / kappa if kappa > 0 else float('inf'),
            "analysis": "科研系统最终达到动态平衡，进展速率稳定在某一水平"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T13 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if self._gamma_damping <= 0:
            errors.append("γ阻尼系数必须大于0")
        if self._kappa_restoring <= 0:
            errors.append("κ回复系数必须大于0")
        if len(self._research_stages) != 6:
            errors.append("科研阶段必须恰好6个")
        if "T10" not in self.dependencies:
            errors.append("T13必须依赖T10（闭环递归）")
        if "T12" not in self.dependencies:
            errors.append("T13必须依赖T12（宿命双边界）")
        if self.cosmic_level != 1:
            errors.append("T13必须位于L1法理层")
        if not self.is_origin_locked:
            errors.append("T13法理理论必须锁定")
        if not hasattr(self, 'closure_dynamics_equation'):
            errors.append("必须实现闭环动力学方程方法")
        if not hasattr(self, 'damped_oscillation_model'):
            errors.append("必须实现阻尼振动模型方法")
        if not hasattr(self, 'research_six_stage_correspondence'):
            errors.append("必须实现科研六阶架构对应方法")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t13 = AutonomousResearchClosure()
    print(f"模块: {t13.module_id} - {t13.module_name}")
    print(f"版本: {t13.version}")
    print(f"层级: L{t13.cosmic_level}")
    print(f"依赖: {t13.dependencies}")
    print(f"锁定: {t13.is_origin_locked}")
    print(f"哈希: {t13.sha256}")
    print()

    print("闭环动力学方程:")
    eq = t13.closure_dynamics_equation(1.0)
    print(f"  方程: {eq['equation']}")
    print(f"  γ阻尼: {eq['gamma_damping']}")
    print(f"  κ回复: {eq['kappa_restoring']}")
    print(f"  振型: {eq['regime']}")
    print()

    print("阻尼振动轨迹:")
    osc = t13.damped_oscillation_model(5)
    for point in osc["trajectory"][:3]:
        print(f"  步骤{point['step']}: R={point['R']:.6f}")
    print()

    print("参数分析:")
    params = t13.gamma_kappa_parameters()
    print(f"  固有频率: {params['derived']['natural_frequency']:.4f}")
    print(f"  阻尼比: {params['derived']['damping_ratio']:.4f}")
    print()

    print("稳态解:")
    steady = t13.steady_state_solution_analysis()
    print(f"  稳态R: {steady['steady_state_R']:.6f}")
    print(f"  稳定性: {steady['stability']}")
    print()

    valid, errs = t13.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
