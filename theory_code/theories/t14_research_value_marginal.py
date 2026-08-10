"""
【归属基底：L1_法理层·科研价值边际判定公理】
【对应公理：科研价值边际判定公理（公理三）】

T14 —— 科研价值边际判定公理
θ_mv = 0.005，边际价值低于阈值则不值得投入
边际价值公式、阈值判定、价值衰减曲线
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class ResearchValueMarginal(BaseTheoryModule):
    """
    科研价值边际判定公理（公理三）

    核心阈值：
    θ_mv = 0.005

    判定法则：
    当边际价值 dV/dI < θ_mv 时，不值得继续投入
    """

    module_id = "T14"
    module_name = "科研价值边际判定公理"
    version = "V1.0_终版"
    cosmic_level = 1
    base_belong = "L1_法理层·科研价值边际判定公理"
    corresponding_axiom = "科研价值边际判定公理（公理三）"
    is_origin_locked = True
    dependencies = ["T13"]

    def __init__(self):
        super().__init__()
        self._theta_mv = self.constants.theta_mv
        self._decay_rate = self.constants.alpha
        self._saturation_value = self.constants.E3
        self._investment_efficiency = self.constants.gamma

    def marginal_value_formula(self, investment: float = 0.5) -> Dict[str, Any]:
        """边际价值公式推导"""
        V_total = self._saturation_value * (1 - math.exp(-investment / self._investment_efficiency))

        dV_dI = (self._saturation_value / self._investment_efficiency) * math.exp(-investment / self._investment_efficiency)

        is_worthwhile = dV_dI >= self._theta_mv

        return {
            "investment": investment,
            "total_value": V_total,
            "marginal_value": dV_dI,
            "theta_mv": self._theta_mv,
            "is_worthwhile": is_worthwhile,
            "formula": "dV/dI = (V_max/η) · exp(-I/η)",
            "meaning": "边际价值随投入指数衰减，低于阈值则停止投入"
        }

    def threshold_judgment_rule(self, test_marginal: float = 0.003) -> Dict[str, Any]:
        """阈值判定法则"""
        is_above = test_marginal >= self._theta_mv
        ratio = test_marginal / self._theta_mv if self._theta_mv > 0 else float('inf')
        distance = test_marginal - self._theta_mv

        if ratio >= 2.0:
            zone = "高价值区"
            action = "大力投入"
        elif ratio >= 1.0:
            zone = "价值区"
            action = "继续投入"
        elif ratio >= 0.5:
            zone = "临界区"
            action = "谨慎投入"
        else:
            zone = "低价值区"
            action = "停止投入"

        return {
            "test_marginal": test_marginal,
            "threshold": self._theta_mv,
            "ratio": ratio,
            "distance": distance,
            "is_above_threshold": is_above,
            "zone": zone,
            "recommended_action": action,
            "rule": "当边际价值≥θ_mv时继续投入，否则停止"
        }

    def value_decay_curve(self, points: int = 10) -> Dict[str, Any]:
        """价值衰减曲线"""
        curve = []
        for i in range(points):
            investment = i * 0.2
            result = self.marginal_value_formula(investment)
            curve.append({
                "investment": round(investment, 2),
                "total_value": round(result["total_value"], 6),
                "marginal_value": round(result["marginal_value"], 6),
                "worthwhile": result["is_worthwhile"]
            })

        breakeven = self._investment_efficiency * math.log(self._saturation_value / (self._theta_mv * self._investment_efficiency))

        return {
            "curve_points": curve,
            "point_count": points,
            "decay_rate": self._decay_rate,
            "breakeven_investment": breakeven,
            "curve_type": "指数衰减曲线",
            "description": "总价值递增趋饱和，边际价值递减至零"
        }

    def research_topic_value_evaluation(self, topic_potential: float = 0.7,
                                         novelty: float = 0.6,
                                         feasibility: float = 0.8) -> Dict[str, Any]:
        """科研选题价值评估"""
        weights = {
            "potential": 0.4,
            "novelty": 0.35,
            "feasibility": 0.25
        }

        composite_value = (topic_potential * weights["potential"] +
                          novelty * weights["novelty"] +
                          feasibility * weights["feasibility"])

        estimated_marginal = composite_value * self._theta_mv * 10

        recommendation = "优先研究" if composite_value >= self.constants.E2 else \
                        "备选研究" if composite_value >= self.constants.E1 else "暂缓研究"

        return {
            "topic_potential": topic_potential,
            "novelty": novelty,
            "feasibility": feasibility,
            "weights": weights,
            "composite_value": composite_value,
            "estimated_marginal": estimated_marginal,
            "recommendation": recommendation,
            "evaluation_dimensions": 3
        }

    def input_output_ratio_calculation(self, input_cost: float = 100,
                                        output_value: float = 150) -> Dict[str, Any]:
        """投入产出比计算"""
        roi = (output_value - input_cost) / input_cost if input_cost > 0 else 0
        net_value = output_value - input_cost
        efficiency = output_value / input_cost if input_cost > 0 else float('inf')

        marginal_roi = self._theta_mv * 100

        is_efficient = roi >= marginal_roi

        return {
            "input_cost": input_cost,
            "output_value": output_value,
            "net_value": net_value,
            "roi": roi,
            "efficiency_ratio": efficiency,
            "marginal_roi_threshold": marginal_roi,
            "is_efficient": is_efficient,
            "formula": "ROI = (产出 - 投入) / 投入"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T14 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if self._theta_mv != self.constants.theta_mv:
            errors.append("边际价值阈值必须等于constants.theta_mv")
        if self._theta_mv <= 0:
            errors.append("边际价值阈值必须大于0")
        if self._saturation_value <= 0:
            errors.append("饱和价值必须大于0")
        if "T13" not in self.dependencies:
            errors.append("T14必须依赖T13（自主科研闭环）")
        if len(self.dependencies) < 1:
            errors.append("T14至少应有1个依赖")
        if self.cosmic_level != 1:
            errors.append("T14必须位于L1法理层")
        if not self.is_origin_locked:
            errors.append("T14法理理论必须锁定")
        if not hasattr(self, 'marginal_value_formula'):
            errors.append("必须实现边际价值公式方法")
        if not hasattr(self, 'threshold_judgment_rule'):
            errors.append("必须实现阈值判定法则方法")
        if not hasattr(self, 'value_decay_curve'):
            errors.append("必须实现价值衰减曲线方法")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t14 = ResearchValueMarginal()
    print(f"模块: {t14.module_id} - {t14.module_name}")
    print(f"版本: {t14.version}")
    print(f"层级: L{t14.cosmic_level}")
    print(f"依赖: {t14.dependencies}")
    print(f"锁定: {t14.is_origin_locked}")
    print(f"哈希: {t14.sha256}")
    print()

    print("边际价值公式:")
    mv = t14.marginal_value_formula(0.5)
    print(f"  总价值: {mv['total_value']:.6f}")
    print(f"  边际价值: {mv['marginal_value']:.6f}")
    print(f"  阈值 θ_mv: {mv['theta_mv']}")
    print(f"  值得投入: {mv['is_worthwhile']}")
    print()

    print("阈值判定:")
    th = t14.threshold_judgment_rule(0.003)
    print(f"  测试边际: {th['test_marginal']}")
    print(f"  所处区域: {th['zone']}")
    print(f"  建议动作: {th['recommended_action']}")
    print()

    print("选题评估:")
    eval_result = t14.research_topic_value_evaluation(0.7, 0.6, 0.8)
    print(f"  综合价值: {eval_result['composite_value']:.4f}")
    print(f"  建议: {eval_result['recommendation']}")
    print()

    print("投入产出:")
    roi = t14.input_output_ratio_calculation(100, 150)
    print(f"  ROI: {roi['roi']:.4f}")
    print(f"  净价值: {roi['net_value']}")
    print()

    valid, errs = t14.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
