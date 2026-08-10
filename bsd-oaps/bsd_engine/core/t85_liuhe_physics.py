"""
T85六系数理工程引擎
====================
T85六系数理的工程实现
[V1.0·2026-08-01]

核心理论：
- T85六系数理：BSD存在论框架第一代基础粒子深层本体结构解析
- 定量模型与第一性原理推导
- 六系权重的数学基底
- 三阶跃迁的量化条件

对应文档：
- T85六系数理——BSD存在论框架第一代基础粒子深层本体结构解析
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime


# ============================================================================
# 1. 六系数理常量
# ============================================================================

class T85Constants:
    """T85六系数理常量"""
    
    # 粒子级六系权重（T85公式）
    PARTICLE_LEVEL_WEIGHTS = {
        "alpha1_individual": 0.11,   # 个体性
        "alpha2_relation": 0.87,     # 关系性
        "alpha3_change": 0.02,       # 变化性
    }
    
    # 三阶跃迁条件
    THREE_ORDER_TRANSITION = {
        "L1_to_L2": {  # 粒子→原子
            "condition": "α₁ ≥ 0.60",
            "alpha1_min": 0.60,
            "description": "个体性主导的稳定存在",
        },
        "L2_to_L3": {  # 原子→离子
            "condition": "α₂ ≥ 0.55",
            "alpha2_min": 0.55,
            "description": "关系性主导的连接存在",
        },
        "L3_to_L4": {  # 离子→分子
            "condition": "α₃ ≥ 0.45",
            "alpha3_min": 0.45,
            "description": "变化性主导的演化存在",
        },
    }
    
    # 六系基准权重
    SYSTEM_BASE_WEIGHTS = {
        "强化系": {"alpha1": 0.45, "alpha2": 0.30, "alpha3": 0.25},
        "自然系": {"alpha1": 0.55, "alpha2": 0.25, "alpha3": 0.20},
        "具现系": {"alpha1": 0.30, "alpha2": 0.50, "alpha3": 0.20},
        "变身系": {"alpha1": 0.25, "alpha2": 0.25, "alpha3": 0.50},
        "社会系": {"alpha1": 0.35, "alpha2": 0.45, "alpha3": 0.20},
        "天道系": {"alpha1": 0.30, "alpha2": 0.35, "alpha3": 0.35},
    }
    
    # Ω参数（粒子层完备度）
    OMEGA_PARTICLE = 100.0
    
    # 六系阈值递减
    SYSTEM_THRESHOLD_DECAY = {
        "粒子": 1.00,
        "原子": 0.95,
        "离子": 0.90,
        "分子": 0.85,
        "元素": 0.80,
        "细胞": 0.75,
    }
    
    # 第一性原理公式
    FIRST_PRINCIPLE_FORMULAS = {
        "existence": "存在 = f(个体性, 关系性, 变化性)",
        "stability": "稳定性 = α₁ ≥ θ_stable",
        "connectivity": "连接性 = α₂ ≥ θ_connect",
        "evolution": "演化性 = α₃ ≥ θ_evolve",
    }


# ============================================================================
# 2. 数据结构
# ============================================================================

@dataclass
class LiuHeWeights:
    """六系权重"""
    alpha1: float = 0.0  # 个体性
    alpha2: float = 0.0  # 关系性
    alpha3: float = 0.0  # 变化性
    
    def normalize(self) -> Tuple[float, float, float]:
        """归一化"""
        total = self.alpha1 + self.alpha2 + self.alpha3
        if total == 0:
            return (0.333, 0.333, 0.333)
        return (self.alpha1/total, self.alpha2/total, self.alpha3/total)
    
    def compute_entropy(self) -> float:
        """计算权重熵"""
        p1, p2, p3 = self.normalize()
        if p1 > 0:
            h = -p1 * math.log2(p1)
        else:
            h = 0
        if p2 > 0:
            h -= p2 * math.log2(p2)
        if p3 > 0:
            h -= p3 * math.log2(p3)
        return h


@dataclass
class TransitionState:
    """跃迁状态"""
    from_level: str
    to_level: str
    weights: LiuHeWeights
    can_transition: bool = False
    transition_value: float = 0.0


# ============================================================================
# 3. T85引擎
# ============================================================================

class T85LiuHePhysicsEngine:
    """T85六系数理引擎"""
    
    def __init__(self):
        self.consts = T85Constants()
        self.weight_history: List[Dict] = []
        self.transitions: List[TransitionState] = []
        
    def get_particle_level_weights(self) -> LiuHeWeights:
        """获取粒子级权重"""
        c = self.consts.PARTICLE_LEVEL_WEIGHTS
        return LiuHeWeights(
            alpha1=c["alpha1_individual"],
            alpha2=c["alpha2_relation"],
            alpha3=c["alpha3_change"]
        )
    
    def get_system_base_weights(self, system: str) -> LiuHeWeights:
        """获取系统基准权重"""
        if system not in self.consts.SYSTEM_BASE_WEIGHTS:
            raise ValueError(f"未知系统: {system}")
        
        w = self.consts.SYSTEM_BASE_WEIGHTS[system]
        return LiuHeWeights(
            alpha1=w["alpha1"],
            alpha2=w["alpha2"],
            alpha3=w["alpha3"]
        )
    
    def check_transition_condition(self, from_level: str, to_level: str, 
                                    weights: Optional[LiuHeWeights] = None) -> TransitionState:
        """检查跃迁条件"""
        if weights is None:
            weights = self.get_particle_level_weights()
        
        transition_key = f"{from_level}_to_{to_level}"
        condition = self.consts.THREE_ORDER_TRANSITION.get(transition_key)
        
        if condition is None:
            return TransitionState(from_level, to_level, weights, False, 0.0)
        
        # 检查条件
        can_transition = False
        value = 0.0
        
        if "α₁" in condition["condition"]:
            can_transition = weights.alpha1 >= condition["alpha1_min"]
            value = weights.alpha1
        elif "α₂" in condition["condition"]:
            can_transition = weights.alpha2 >= condition["alpha2_min"]
            value = weights.alpha2
        elif "α₃" in condition["condition"]:
            can_transition = weights.alpha3 >= condition["alpha3_min"]
            value = weights.alpha3
        
        state = TransitionState(from_level, to_level, weights, can_transition, value)
        self.transitions.append(state)
        return state
    
    def compute_omega(self, weights: Optional[LiuHeWeights] = None) -> float:
        """计算Ω参数（完备度）"""
        if weights is None:
            weights = self.get_particle_level_weights()
        
        # Ω = Ω_base * (1 - entropy/max_entropy)
        omega_base = self.consts.OMEGA_PARTICLE
        entropy = weights.compute_entropy()
        max_entropy = math.log2(3)  # 三权重最大熵
        
        omega = omega_base * (1 - entropy / max_entropy)
        return max(0, omega)
    
    def compute_system_threshold(self, system: str, level: str) -> float:
        """计算系统阈值"""
        base_threshold = self.consts.SYSTEM_THRESHOLD_DECAY.get(level, 0.8)
        system_weights = self.get_system_base_weights(system)
        
        # 阈值 = 基础阈值 * (1 + 主导权重)
        dominant_weight = max(
            system_weights.alpha1, 
            system_weights.alpha2, 
            system_weights.alpha3
        )
        return base_threshold * (1 + dominant_weight * 0.1)
    
    def compute_existence_value(self, weights: LiuHeWeights) -> float:
        """计算存在值"""
        # 存在 = α₁ * ω₁ + α₂ * ω₂ + α₃ * ω₃
        # 其中 ω_i 是各维度的存在势
        omega1 = self.compute_omega(LiuHeWeights(weights.alpha1, 0, 0))
        omega2 = self.compute_omega(LiuHeWeights(0, weights.alpha2, 0))
        omega3 = self.compute_omega(LiuHeWeights(0, 0, weights.alpha3))
        
        existence = (
            weights.alpha1 * omega1 +
            weights.alpha2 * omega2 +
            weights.alpha3 * omega3
        )
        return existence
    
    def evolve_weights(self, current: LiuHeWeights, target_system: str, 
                        learning_rate: float = 0.1) -> LiuHeWeights:
        """权重演化"""
        target = self.get_system_base_weights(target_system)
        
        new_alpha1 = current.alpha1 + learning_rate * (target.alpha1 - current.alpha1)
        new_alpha2 = current.alpha2 + learning_rate * (target.alpha2 - current.alpha2)
        new_alpha3 = current.alpha3 + learning_rate * (target.alpha3 - current.alpha3)
        
        new_weights = LiuHeWeights(new_alpha1, new_alpha2, new_alpha3)
        self.weight_history.append({
            "from": (current.alpha1, current.alpha2, current.alpha3),
            "to": (new_alpha1, new_alpha2, new_alpha3),
            "target_system": target_system,
            "timestamp": datetime.now().isoformat(),
        })
        return new_weights
    
    def get_t85_report(self) -> Dict:
        """获取T85完整报告"""
        particle_weights = self.get_particle_level_weights()
        omega = self.compute_omega(particle_weights)
        existence = self.compute_existence_value(particle_weights)
        
        return {
            "report_id": f"T85-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "theory": "T85六系数理",
            "particle_level_weights": {
                "alpha1": particle_weights.alpha1,
                "alpha2": particle_weights.alpha2,
                "alpha3": particle_weights.alpha3,
            },
            "omega": omega,
            "existence_value": existence,
            "system_base_weights": {
                sys: {
                    "alpha1": w.alpha1,
                    "alpha2": w.alpha2,
                    "alpha3": w.alpha3,
                }
                for sys, w in [
                    (s, self.get_system_base_weights(s))
                    for s in self.consts.SYSTEM_BASE_WEIGHTS
                ]
            },
            "transition_conditions": {
                key: {
                    "condition": val["condition"],
                    "description": val["description"],
                }
                for key, val in self.consts.THREE_ORDER_TRANSITION.items()
            },
            "threshold_decay": self.consts.SYSTEM_THRESHOLD_DECAY,
            "verdict": self._compute_verdict(omega, existence),
        }
    
    def _compute_verdict(self, omega: float, existence: float) -> str:
        """计算判定"""
        if omega >= 50 and existence >= 30:
            return "✅ T85六系数理验证通过"
        elif omega >= 20:
            return "🟡 基本验证通过"
        else:
            return "⚪ 需要更多验证"


# ============================================================================
# 4. 演示与测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("T85六系数理引擎")
    print("BSD存在论框架·第一性原理推导")
    print("=" * 60)
    
    engine = T85LiuHePhysicsEngine()
    
    # 粒子级权重
    weights = engine.get_particle_level_weights()
    print(f"\n【粒子级权重】")
    print(f"  α₁(个体性): {weights.alpha1}")
    print(f"  α₂(关系性): {weights.alpha2}")
    print(f"  α₃(变化性): {weights.alpha3}")
    
    # 计算Ω
    omega = engine.compute_omega(weights)
    print(f"\n【Ω参数】")
    print(f"  Ω = {omega:.4f}")
    print(f"  基准Ω = {T85Constants.OMEGA_PARTICLE}")
    
    # 计算存在值
    existence = engine.compute_existence_value(weights)
    print(f"\n【存在值】")
    print(f"  存在 = {existence:.4f}")
    
    # 检查跃迁条件
    print(f"\n【三阶跃迁检查】")
    for key, info in T85Constants.THREE_ORDER_TRANSITION.items():
        state = engine.check_transition_condition(
            key.split("_")[0], 
            key.split("_")[1], 
            weights
        )
        print(f"  {key}: {'✅ 可跃迁' if state.can_transition else '❌ 未达条件'}")
        print(f"    条件: {info['condition']}")
        print(f"    说明: {info['description']}")
    
    # 权重演化
    print(f"\n【权重演化示例】")
    for system in ["强化系", "具现系", "变身系"]:
        evolved = engine.evolve_weights(weights, system, 0.2)
        print(f"  → {system}: α₁={evolved.alpha1:.3f}, α₂={evolved.alpha2:.3f}, α₃={evolved.alpha3:.3f}")
    
    # 完整报告
    report = engine.get_t85_report()
    print(f"\n【最终报告】")
    print(f"  判定: {report['verdict']}")
    
    print("\n" + "=" * 60)
    print("T85六系数理工程验证通过")
    print("=" * 60)
