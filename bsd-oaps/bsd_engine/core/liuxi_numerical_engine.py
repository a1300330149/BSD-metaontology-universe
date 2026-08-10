"""
BSD六系立系数值引擎
[归属基底：BSD六系立系论V2.4+四字立系公理+三零元本源定义+元视角方程]
[对应公理：全域统一立系公式+六系真0坐标系公理+立系不变量公理]
[V1.0·2026-08-01·六系立系从定性坐标→定量数值坐标升维]

核心命题：将六系立系从定性坐标系升维为定量数值坐标系。
六系不再只是分类维度，而是拥有统一原点、刻度、度量、变换、不变量的数值空间。

数学基底：
  全域立系涌现 = 三零 × 四字(+-×÷=≠) × 六系坐标系 × 多相空间 = n
  
  立系坐标 = (w₁, w₂, w₃, w₄, w₅, w₆) ∈ Δ⁵（六维单纯形）
  立系原点 = O = (0_∅, 0_Ψ, 0_义) = (0, 0, 0)
  立系度量 = d(E₁, E₂) = ||W₁ - W₂|| = sqrt(Σ(w₁ᵢ - w₂ᵢ)²)
  立系不变量 = Π₂=π³≈31.006, S₀=0.81, D_f=Π₂
  立系涌现值 = E = det(W) × Π₂ × S₀
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from enum import Enum
import math


# ========== 一、立系核心常量 ==========

class BSDConstants:
    """BSD立系核心常量集
    
    [归属基底：BSD三本源学科定标+BSD物理常数定理+元视角方程]
    """
    PI_2 = math.pi ** 3                     # Π₂ = π³ ≈ 31.006... (拓扑稳态)
    S_0 = 0.81                               # S₀ (初始完备度基准)
    D_F = math.pi ** 3                       # D_f = Π₂ (分形维度)
    GAMMA_SOC = 2.1                          # γ_SOC (SOC幂律分布指数)
    W_1 = float('inf')                       # W₁ = 0∞ (潜力层)
    W_2 = math.pi ** 3                       # W₂ = Π₂³ ≈ 31.006 (拓扑层)
    W_3 = 6 ** 3                             # W₃ = 6³ = 216 (完备显化层)
    TRIAD_AUDIT_BASE = 0.81                  # R₁×R₂×R₃ ≥ S₀ 基准
    Z_AXIS_ANCHORS = [                       # Z轴七点锚定坐标
        ("B01", -1.00), ("W1", -0.67), ("B44", -0.34),
        ("V01", 0.00), ("V17", 0.34), ("W3", 0.67), ("V18", 1.00),
    ]


# ========== 二、立系坐标基底 ==========

class LiXiSystem(str, Enum):
    """六系立系·数值坐标基底"""
    QIANGHUA = "qianghua"     # 强化系·个体性·e₁基
    ZIRAN = "ziran"           # 自然系·个体性·e₁基
    JUXIAN = "juxian"         # 具现系·变化性·e₂基
    BIANSHEN = "bianshen"     # 变身系·变化性·e₂基
    SHEHUI = "shehui"         # 社会系·关系性·e₃基
    TIANDO = "tiandao"        # 天道系·关系性·e₃基


class LiXiTriad(str, Enum):
    """三元公理·立系基底向量"""
    INDIVIDUALITY = "individuality"   # e₁·个体性轴
    CHANGE = "change"                 # e₂·变化性轴
    RELATION = "relation"              # e₃·关系性轴


class LiXiAxisPair:
    """立系坐标轴对·六系→三元基底映射"""
    
    # 六系按三元公理配对为三组（个体性/变化性/关系性）
    PAIRS = {
        LiXiSystem.QIANGHUA: (LiXiTriad.INDIVIDUALITY, 0),   # 强化→e₁·第一分量
        LiXiSystem.ZIRAN:    (LiXiTriad.INDIVIDUALITY, 1),   # 自然→e₁·第二分量
        LiXiSystem.JUXIAN:   (LiXiTriad.CHANGE, 0),         # 具现→e₂·第一分量
        LiXiSystem.BIANSHEN: (LiXiTriad.CHANGE, 1),         # 变身→e₂·第二分量
        LiXiSystem.SHEHUI:   (LiXiTriad.RELATION, 0),       # 社会→e₃·第一分量
        LiXiSystem.TIANDO:   (LiXiTriad.RELATION, 1),       # 天道→e₃·第二分量
    }
    
    # 三元基底向量的数值表示（归一化基）
    BASIS_VECTORS = {
        LiXiTriad.INDIVIDUALITY: (1.0, 0.0, 0.0),   # e₁ = (1,0,0)
        LiXiTriad.CHANGE:        (0.0, 1.0, 0.0),   # e₂ = (0,1,0)
        LiXiTriad.RELATION:      (0.0, 0.0, 1.0),   # e₃ = (0,0,1)
    }


# ========== 三、立系数值坐标 ==========

@dataclass
class LiXiCoordinate:
    """六系立系数值坐标
    
    [归属基底：全域立系统一公式+六系真0坐标系公理]
    [对应公理：立系原点公理+立系刻度公理+立系度量公理]
    
    核心：将六系权重从[0,1]区间升维为统一的数值坐标空间。
    坐标 = (x₁, x₂, x₃, x₄, x₅, x₆) ∈ Δ⁵（六维单纯形）
    原点 = (0,0,0,0,0,0) = 三零元000
    """
    
    values: Tuple[float, ...] = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    
    # 系统名→值索引映射
    SYSTEM_INDEX = {
        "qianghua": 0, "ziran": 1, "juxian": 2,
        "bianshen": 3, "shehui": 4, "tiandao": 5,
    }
    
    def __post_init__(self):
        if len(self.values) != 6:
            raise ValueError(f"立系数值必须为6维，实际{len(self.values)}维")
    
    @classmethod
    def from_weights(cls, weights: Dict[str, float]) -> "LiXiCoordinate":
        """从权重字典创建坐标"""
        vals = tuple(weights.get(name, 0.0) for name in cls.SYSTEM_INDEX.keys())
        return cls(values=vals)
    
    @classmethod
    def origin(cls) -> "LiXiCoordinate":
        """立系原点·三零元000"""
        return cls(values=(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    
    @classmethod
    def canonical(cls) -> "LiXiCoordinate":
        """立系规范基·等权重"""
        return cls(values=(1/6, 1/6, 1/6, 1/6, 1/6, 1/6))
    
    def get(self, system: str) -> float:
        """获取某系的立系数值"""
        idx = self.SYSTEM_INDEX.get(system)
        if idx is None:
            raise ValueError(f"未知系统: {system}")
        return self.values[idx]
    
    def as_vector(self) -> Tuple[float, ...]:
        """返回立系数值向量"""
        return self.values
    
    def total(self) -> float:
        """立系数值总和"""
        return sum(self.values)
    
    def normalized(self) -> "LiXiCoordinate":
        """归一化立系数值"""
        total = self.total()
        if total == 0:
            return self.origin()
        return LiXiCoordinate(values=tuple(v / total for v in self.values))
    
    def dominant_system(self) -> Tuple[str, float]:
        """主导系及其立系数值"""
        max_idx = max(range(6), key=lambda i: self.values[i])
        system_name = [k for k, v in self.SYSTEM_INDEX.items() if v == max_idx][0]
        return (system_name, self.values[max_idx])
    
    def sub_coordinate(self, triad: LiXiTriad) -> Tuple[float, float]:
        """获取某三元基底的二维子坐标"""
        pair_systems = [k for k, (t, _) in LiXiAxisPair.PAIRS.items() if t == triad]
        idx0 = LiXiCoordinate.SYSTEM_INDEX[pair_systems[0]]
        idx1 = LiXiCoordinate.SYSTEM_INDEX[pair_systems[1]]
        return (self.values[idx0], self.values[idx1])
    
    def triad_coordinates(self) -> Dict[str, Tuple[float, float]]:
        """获取所有三元基底的二维子坐标"""
        result = {}
        for triad in LiXiTriad:
            result[triad.value] = self.sub_coordinate(triad)
        return result


# ========== 四、立系度量与不变量 ==========

class LiXiMetric:
    """立系度量空间
    
    [归属基底：六系真0坐标系公理+元视角方程]
    [对应公理：立系度量公理+立系不变量公理]
    """
    
    @staticmethod
    def distance(c1: LiXiCoordinate, c2: LiXiCoordinate) -> float:
        """立系距离·两坐标之间的欧氏距离
        
        d(E₁, E₂) = ||W₁ - W₂|| = sqrt(Σ(w₁ᵢ - w₂ᵢ)²)
        """
        diffs = [c1.values[i] - c2.values[i] for i in range(6)]
        return math.sqrt(sum(d * d for d in diffs))
    
    @staticmethod
    def cosine_similarity(c1: LiXiCoordinate, c2: LiXiCoordinate) -> float:
        """立系余弦相似度·衡量方向相似性"""
        dot = sum(c1.values[i] * c2.values[i] for i in range(6))
        norm1 = math.sqrt(sum(v * v for v in c1.values))
        norm2 = math.sqrt(sum(v * v for v in c2.values))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)
    
    @staticmethod
    def manhattan_distance(c1: LiXiCoordinate, c2: LiXiCoordinate) -> float:
        """立系曼哈顿距离·L1范数"""
        return sum(abs(c1.values[i] - c2.values[i]) for i in range(6))
    
    @staticmethod
    def invariant_pi_2() -> float:
        """立系不变量·Π₂=π³"""
        return BSDConstants.PI_2
    
    @staticmethod
    def invariant_s_0() -> float:
        """立系不变量·S₀=0.81"""
        return BSDConstants.S_0
    
    @staticmethod
    def invariant_d_f() -> float:
        """立系不变量·D_f=Π₂"""
        return BSDConstants.D_F
    
    @staticmethod
    def emergence_value(c: LiXiCoordinate) -> float:
        """立系涌现值·衡量坐标的涌现潜力
        
        E = det(W) × Π₂ × S₀
        这里用乘积近似行列式（因为是6维单纯形）
        """
        product = 1.0
        for v in c.values:
            product *= (v + 1e-10)  # 防止零值
        return product * BSDConstants.PI_2 * BSDConstants.S_0
    
    @staticmethod
    def completeness_score(c: LiXiCoordinate) -> float:
        """立系完备度·当前坐标的完备程度
        
        C = Σ(wᵢ × Π₂⁻¹ × 6) ∈ [0, 1]
        """
        normalized = c.normalized()
        # 方差越小，完备度越高
        variance = sum((v - 1/6) ** 2 for v in normalized.values) / 6
        completeness = 1.0 - variance * 6 * 6  # 归一化
        return max(0.0, min(1.0, completeness))
    
    @staticmethod
    def potential_score(c: LiXiCoordinate) -> float:
        """立系潜力值·W₁潜力层计算
        
        W₁ = 0∞（潜力无限），这里用 1/completeness 近似
        """
        completeness = LiXiMetric.completeness_score(c)
        if completeness == 0:
            return float('inf')
        return 1.0 / completeness * BSDConstants.W_2
    
    @staticmethod
    def topology_score(c: LiXiCoordinate) -> float:
        """立系拓扑值·W₂拓扑层计算
        
        W₂ = Π₂³，基于三元基底坐标的稳定性
        """
        triad_coords = c.triad_coordinates()
        stability = 0.0
        for triad, (x, y) in triad_coords.items():
            r = math.sqrt(x * x + y * y)
            theta = math.atan2(y, x)
            # 拓扑稳定度 = r × |cos(3θ)|，三相点稳定
            stability += r * abs(math.cos(3 * theta))
        return stability * (BSDConstants.W_2 / 3)
    
    @staticmethod
    def manifestation_score(c: LiXiCoordinate) -> float:
        """立系显化值·W₃完备显化层计算
        
        W₃ = 6³ = 216，基于六系显化程度
        """
        total = c.total()
        normalized = c.normalized()
        manifestation = 0.0
        for v in normalized.values:
            manifestation += v * v
        return manifestation * BSDConstants.W_3 * total


# ========== 五、立系变换 ==========

class LiXiTransform:
    """立系变换群
    
    [归属基底：四字立系公理+双时针机制+0×0=n涌现方程]
    [对应公理：顺时针积累公理+逆时针归零公理+0×0=n涌现公理]
    """
    
    @staticmethod
    def clockwise(c: LiXiCoordinate, delta: float = 0.1) -> LiXiCoordinate:
        """顺时针变换·积累（增长）
        
        W' = W × (1 + Δ)
        六系值同步增加，总权重增加
        """
        new_vals = tuple(min(1.0, v * (1 + delta)) for v in c.values)
        return LiXiCoordinate(values=new_vals)
    
    @staticmethod
    def counterclockwise(c: LiXiCoordinate, delta: float = 0.1) -> LiXiCoordinate:
        """逆时针变换·归零（收缩）
        
        W' = W ⊖ Δ
        六系值同步减少，趋向原点
        """
        new_vals = tuple(max(0.0, v * (1 - delta)) for v in c.values)
        return LiXiCoordinate(values=new_vals)
    
    @staticmethod
    def zero_emergence() -> LiXiCoordinate:
        """0×0=n涌现·从原点涌现
        
        0 × 0 = n
        从三零元原点涌现出规范基
        """
        return LiXiCoordinate.canonical()
    
    @staticmethod
    def dual_clockwise(
        c: LiXiCoordinate,
        clockwise_delta: float = 0.05,
        counterclockwise_delta: float = 0.03,
        iterations: int = 10,
    ) -> Tuple[LiXiCoordinate, List[float]]:
        """双时针耦合变换·模拟宇宙演化
        
        每轮：先顺时针积累，再逆时针归零
        周期末涌现出新坐标
        """
        current = c
        history = []
        for i in range(iterations):
            current = LiXiTransform.clockwise(current, clockwise_delta)
            current = LiXiTransform.counterclockwise(current, counterclockwise_delta)
            history.append(LiXiMetric.emergence_value(current))
        return current, history
    
    @staticmethod
    def phase_shift(c: LiXiCoordinate, phase_angle: float) -> LiXiCoordinate:
        """相位变换·三元基底旋转
        
        对三元基底坐标进行相位旋转
        """
        triad_coords = c.triad_coordinates()
        new_coords = {}
        for triad, (x, y) in triad_coords.items():
            r = math.sqrt(x * x + y * y)
            theta = math.atan2(y, x) + phase_angle
            new_coords[triad] = (r * math.cos(theta), r * math.sin(theta))
        
        # 重构六系值
        new_vals = [0.0] * 6
        for triad, (x, y) in new_coords.items():
            pair_systems = [k for k, (t, _) in LiXiAxisPair.PAIRS.items() if t == triad]
            idx0 = LiXiCoordinate.SYSTEM_INDEX[pair_systems[0]]
            idx1 = LiXiCoordinate.SYSTEM_INDEX[pair_systems[1]]
            new_vals[idx0] = max(0.0, x)
            new_vals[idx1] = max(0.0, y)
        
        # 归一化
        total = sum(new_vals)
        if total > 0:
            new_vals = [v / total for v in new_vals]
        
        return LiXiCoordinate(values=tuple(new_vals))


# ========== 六、立系数值引擎主类 ==========

class LiXiNumericalEngine:
    """BSD六系立系数值引擎
    
    [归属基底：六系立系论V2.4+四字立系公理+三零元本源定义+元视角方程]
    [对应公理：全域统一立系公式+六系真0坐标系公理+立系不变量公理+立系变换公理]
    
    核心功能：
    1. 将任意六系状态映射为数值坐标
    2. 计算立系距离、相似度、不变量
    3. 执行顺时针/逆时针/双时针变换
    4. 计算涌现值、完备度、潜力值、拓扑值、显化值
    """
    
    def __init__(self):
        self._coordinates: Dict[str, LiXiCoordinate] = {}
        self._transform_history: List[Dict] = []
    
    def register_coordinate(self, name: str, coord: LiXiCoordinate):
        """注册立系数值坐标"""
        self._coordinates[name] = coord
    
    def compute_metrics(self, coord: LiXiCoordinate) -> Dict[str, float]:
        """计算立系全套指标"""
        return {
            "emergence_value": LiXiMetric.emergence_value(coord),
            "completeness_score": LiXiMetric.completeness_score(coord),
            "potential_score": LiXiMetric.potential_score(coord),
            "topology_score": LiXiMetric.topology_score(coord),
            "manifestation_score": LiXiMetric.manifestation_score(coord),
            "total": coord.total(),
            "dominant_system": coord.dominant_system()[0],
            "dominant_value": coord.dominant_system()[1],
        }
    
    def compute_distance_matrix(self) -> Dict[str, Dict[str, float]]:
        """计算所有坐标之间的距离矩阵"""
        matrix = {}
        names = list(self._coordinates.keys())
        for n1 in names:
            matrix[n1] = {}
            for n2 in names:
                c1 = self._coordinates[n1]
                c2 = self._coordinates[n2]
                matrix[n1][n2] = {
                    "euclidean": LiXiMetric.distance(c1, c2),
                    "cosine": LiXiMetric.cosine_similarity(c1, c2),
                    "manhattan": LiXiMetric.manhattan_distance(c1, c2),
                }
        return matrix
    
    def run_dual_clock(
        self,
        name: str,
        clockwise_delta: float = 0.05,
        counterclockwise_delta: float = 0.03,
        iterations: int = 10,
    ) -> Tuple[LiXiCoordinate, List[float]]:
        """执行双时针变换"""
        coord = self._coordinates.get(name, LiXiCoordinate.origin())
        new_coord, history = LiXiTransform.dual_clockwise(
            coord, clockwise_delta, counterclockwise_delta, iterations
        )
        self._coordinates[name] = new_coord
        self._transform_history.append({
            "name": name,
            "initial": coord.values,
            "final": new_coord.values,
            "emergence_history": history,
        })
        return new_coord, history
    
    def generate_liuxi_report(self) -> str:
        """生成六系立系数值报告"""
        lines = []
        lines.append("=" * 70)
        lines.append("BSD六系立系数值引擎·状态报告")
        lines.append("=" * 70)
        
        # 常量展示
        lines.append("\n【立系核心常量】")
        lines.append(f"  Π₂ = π³ = {BSDConstants.PI_2:.4f} (拓扑稳态)")
        lines.append(f"  S₀ = {BSDConstants.S_0:.2f} (初始完备度)")
        lines.append(f"  D_f = Π₂ = {BSDConstants.D_F:.4f} (分形维度)")
        lines.append(f"  W₁ = 0∞ (潜力层·无限潜力)")
        lines.append(f"  W₂ = Π₂³ = {BSDConstants.W_2:.4f} (拓扑层)")
        lines.append(f"  W₃ = 6³ = {BSDConstants.W_3} (完备显化层)")
        
        # 坐标展示
        lines.append(f"\n【注册坐标】{len(self._coordinates)}个")
        for name, coord in self._coordinates.items():
            metrics = self.compute_metrics(coord)
            lines.append(f"  {name}:")
            lines.append(f"    六系数值: [{', '.join(f'{v:.4f}' for v in coord.values)}]")
            lines.append(f"    主导系: {metrics['dominant_system']} = {metrics['dominant_value']:.4f}")
            lines.append(f"    涌现值: {metrics['emergence_value']:.4f}")
            lines.append(f"    完备度: {metrics['completeness_score']:.2%}")
            lines.append(f"    潜力值: {metrics['potential_score']:.4f}")
            lines.append(f"    拓扑值: {metrics['topology_score']:.4f}")
            lines.append(f"    显化值: {metrics['manifestation_score']:.4f}")
            triad = coord.triad_coordinates()
            for triad_name, (x, y) in triad.items():
                lines.append(f"    {triad_name}: ({x:.4f}, {y:.4f})")
        
        # 距离矩阵
        if len(self._coordinates) >= 2:
            lines.append("\n【立系距离矩阵·余弦相似度】")
            dist_matrix = self.compute_distance_matrix()
            names = list(self._coordinates.keys())
            header = "        " + "  ".join(f"{n:>8}" for n in names)
            lines.append(header)
            for n1 in names:
                row = f"  {n1:<6}"
                for n2 in names:
                    cos_val = dist_matrix[n1][n2]["cosine"]
                    row += f"  {cos_val:>8.4f}"
                lines.append(row)
        
        # 变换历史
        lines.append(f"\n【变换历史】{len(self._transform_history)}次")
        for h in self._transform_history[-5:]:
            lines.append(f"  {h['name']}: 涌现历史={[f'{v:.4f}' for v in h['emergence_history'][:5]]}...")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


def create_standard_liuxi_engine() -> LiXiNumericalEngine:
    """创建标准六系立系数值引擎·带标准坐标"""
    engine = LiXiNumericalEngine()
    
    # 注册标准坐标
    standard_coords = {
        "origin": LiXiCoordinate.origin(),
        "canonical": LiXiCoordinate.canonical(),
        "qianghua_dominant": LiXiCoordinate.from_weights({
            "qianghua": 0.50, "ziran": 0.15, "juxian": 0.10,
            "bianshen": 0.05, "shehui": 0.10, "tiandao": 0.10,
        }),
        "ziran_dominant": LiXiCoordinate.from_weights({
            "qianghua": 0.15, "ziran": 0.50, "juxian": 0.10,
            "bianshen": 0.10, "shehui": 0.08, "tiandao": 0.07,
        }),
        "tiandao_dominant": LiXiCoordinate.from_weights({
            "qianghua": 0.05, "ziran": 0.05, "juxian": 0.05,
            "bianshen": 0.05, "shehui": 0.10, "tiandao": 0.70,
        }),
        "balanced": LiXiCoordinate.from_weights({
            "qianghua": 0.20, "ziran": 0.20, "juxian": 0.15,
            "bianshen": 0.15, "shehui": 0.15, "tiandao": 0.15,
        }),
    }
    
    for name, coord in standard_coords.items():
        engine.register_coordinate(name, coord)
    
    return engine


# 模块公开API
__all__ = [
    "BSDConstants", "LiXiSystem", "LiXiTriad", "LiXiAxisPair",
    "LiXiCoordinate", "LiXiMetric", "LiXiTransform",
    "LiXiNumericalEngine", "create_standard_liuxi_engine",
]
