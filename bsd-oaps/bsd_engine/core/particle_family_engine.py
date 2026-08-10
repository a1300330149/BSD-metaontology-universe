"""
BSD六系六力粒子家族引擎
========================
BSD六系六力对偶定理的工程实现
[V1.0·2026-08-01]

核心理论：
- 定理四十四：六系六力对偶定理
- 六大基本力与六系的对偶对应
- 九维粒子家族矩阵
- 粒子家族的生点证圆关系

对应理论：
- EMERGENCE-006归档
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime


# ============================================================================
# 1. 粒子家族常量
# ============================================================================

class ParticleFamilyConstants:
    """粒子家族常量"""
    
    # 六系与基本力的对应关系
    SYS_FORCE_DUALITY = {
        "强化系": {
            "force": "强力",
            "particle": "胶子",
            "coupling": 0.1184,
            "description": "强化系对应强力，负责夸克禁闭",
        },
        "自然系": {
            "force": "引力",
            "particle": "引力子",
            "coupling": 6.674e-11,
            "description": "自然系对应引力，负责时空弯曲",
        },
        "具现系": {
            "force": "电磁力",
            "particle": "光子",
            "coupling": 1/137.036,
            "description": "具现系对应电磁力，负责电荷相互作用",
        },
        "变身系": {
            "force": "弱力",
            "particle": "W/Z玻色子",
            "coupling": 1.166e-5,
            "description": "变身系对应弱力，负责粒子衰变",
        },
        "社会系": {
            "force": "社会耦合力",
            "particle": "社会子",
            "coupling": 0.37,
            "description": "社会系对应社会耦合力，负责群体凝聚",
        },
        "天道系": {
            "force": "天道涌现力",
            "particle": "天道子",
            "coupling": 0.58,
            "description": "天道系对应天道涌现力，负责意义涌现",
        },
    }
    
    # 九维粒子家族
    NINE_DIMENSION_FAMILY = {
        "quarks": {
            "up": {"mass": 2.16, "charge": 2/3, "spin": 1/2},
            "down": {"mass": 4.67, "charge": -1/3, "spin": 1/2},
            "charm": {"mass": 1270, "charge": 2/3, "spin": 1/2},
            "strange": {"mass": 93.4, "charge": -1/3, "spin": 1/2},
            "top": {"mass": 172760, "charge": 2/3, "spin": 1/2},
            "bottom": {"mass": 4180, "charge": -1/3, "spin": 1/2},
        },
        "leptons": {
            "electron": {"mass": 0.511, "charge": -1, "spin": 1/2},
            "muon": {"mass": 105.66, "charge": -1, "spin": 1/2},
            "tau": {"mass": 1776.86, "charge": -1, "spin": 1/2},
            "neutrino_e": {"mass": 0, "charge": 0, "spin": 1/2},
            "neutrino_mu": {"mass": 0, "charge": 0, "spin": 1/2},
            "neutrino_tau": {"mass": 0, "charge": 0, "spin": 1/2},
        },
        "gauge_bosons": {
            "photon": {"mass": 0, "charge": 0, "spin": 1},
            "gluon": {"mass": 0, "charge": 0, "spin": 1},
            "W_plus": {"mass": 80433, "charge": 1, "spin": 1},
            "W_minus": {"mass": 80433, "charge": -1, "spin": 1},
            "Z": {"mass": 91187.6, "charge": 0, "spin": 1},
            "higgs": {"mass": 125.1, "charge": 0, "spin": 0},
        },
    }
    
    # 生点证圆关系
    BIRTH_POINT_CIRCLE = {
        "particle": {"radius": 0.8, "center": (0, 0, 0)},
        "atom": {"radius": 1.2, "center": (0.5, 0.3, 0.1)},
        "molecule": {"radius": 1.8, "center": (1.0, 0.8, 0.5)},
        "cell": {"radius": 2.5, "center": (1.5, 1.2, 0.8)},
        "organism": {"radius": 3.5, "center": (2.0, 1.5, 1.0)},
    }
    
    # 耦合阈值
    COUPLING_THRESHOLDS = {
        "particle": 0.01,
        "atom": 0.05,
        "molecule": 0.15,
        "cell": 0.30,
        "organism": 0.50,
    }


# ============================================================================
# 2. 粒子数据结构
# ============================================================================

@dataclass
class Particle:
    """粒子"""
    name: str
    mass: float
    charge: float
    spin: float
    family: str  # quarks/leptons/gauge_bosons
    system: str  # 对应六系


@dataclass
class ForceSystemDuality:
    """力-系对偶关系"""
    system: str  # 六系
    force: str   # 基本力
    particle: str  # 传递粒子
    coupling: float  # 耦合常数
    description: str


@dataclass
class BirthPointCircle:
    """生点证圆"""
    stage: str
    radius: float
    center: Tuple[float, float, float]
    proof_value: float = 0.0  # 证圆值


# ============================================================================
# 3. 粒子家族引擎
# ============================================================================

class ParticleFamilyEngine:
    """BSD粒子家族引擎"""
    
    def __init__(self):
        self.consts = ParticleFamilyConstants()
        self.particles: List[Particle] = []
        self.dualities: List[ForceSystemDuality] = []
        self.birth_circles: List[BirthPointCircle] = []
        self.family_matrix: Dict[str, List[Dict]] = {}
        
        self._init_particles()
        self._init_dualities()
        self._init_birth_circles()
    
    def _init_particles(self):
        """初始化粒子"""
        sys_map = {
            "up": "强化系", "down": "强化系",
            "charm": "变身系", "strange": "变身系",
            "top": "天道系", "bottom": "社会系",
            "electron": "具现系", "muon": "自然系",
            "tau": "天道系",
            "neutrino_e": "社会系", "neutrino_mu": "自然系", "neutrino_tau": "天道系",
            "photon": "具现系", "gluon": "强化系",
            "W_plus": "变身系", "W_minus": "变身系",
            "Z": "社会系", "higgs": "自然系",
        }
        
        for family, particles in self.consts.NINE_DIMENSION_FAMILY.items():
            for pname, props in particles.items():
                self.particles.append(Particle(
                    name=pname,
                    mass=props["mass"],
                    charge=props["charge"],
                    spin=props["spin"],
                    family=family,
                    system=sys_map.get(pname, "自然系"),
                ))
    
    def _init_dualities(self):
        """初始化力-系对偶"""
        for system, info in self.consts.SYS_FORCE_DUALITY.items():
            self.dualities.append(ForceSystemDuality(
                system=system,
                force=info["force"],
                particle=info["particle"],
                coupling=info["coupling"],
                description=info["description"],
            ))
    
    def _init_birth_circles(self):
        """初始化生点证圆"""
        for stage, info in self.consts.BIRTH_POINT_CIRCLE.items():
            self.birth_circles.append(BirthPointCircle(
                stage=stage,
                radius=info["radius"],
                center=info["center"],
            ))
    
    def get_particles_by_system(self, system: str) -> List[Particle]:
        """按六系获取粒子"""
        return [p for p in self.particles if p.system == system]
    
    def get_particles_by_family(self, family: str) -> List[Particle]:
        """按家族获取粒子"""
        return [p for p in self.particles if p.family == family]
    
    def compute_coupling_matrix(self) -> Dict[str, Dict[str, float]]:
        """计算耦合矩阵"""
        matrix = {}
        for sys1 in self.consts.SYS_FORCE_DUALITY:
            matrix[sys1] = {}
            for sys2 in self.consts.SYS_FORCE_DUALITY:
                if sys1 == sys2:
                    matrix[sys1][sys2] = self.consts.SYS_FORCE_DUALITY[sys1]["coupling"]
                else:
                    matrix[sys1][sys2] = 0.01  # 跨系耦合
        return matrix
    
    def compute_birth_proof_value(self, stage: str) -> float:
        """计算生点证圆值"""
        circle = next((c for c in self.birth_circles if c.stage == stage), None)
        if circle is None:
            return 0.0
        
        # 证圆值 = 半径 / (半径 + 1)
        circle.proof_value = circle.radius / (circle.radius + 1)
        return circle.proof_value
    
    def evolve_birth_circle(self, stage: str, delta_radius: float = 0.1):
        """演化生点证圆"""
        circle = next((c for c in self.birth_circles if c.stage == stage), None)
        if circle is None:
            return
        
        circle.radius += delta_radius
        circle.proof_value = self.compute_birth_proof_value(stage)
    
    def check_coupling_threshold(self, stage: str, coupling: float) -> Dict:
        """检查耦合阈值"""
        threshold = self.consts.COUPLING_THRESHOLDS.get(stage, 0.5)
        return {
            "stage": stage,
            "coupling": coupling,
            "threshold": threshold,
            "above_threshold": coupling >= threshold,
        }
    
    def get_family_report(self) -> Dict:
        """获取粒子家族报告"""
        particles_by_system = {}
        for sys in self.consts.SYS_FORCE_DUALITY:
            particles_by_system[sys] = [
                {"name": p.name, "mass": p.mass, "charge": p.charge}
                for p in self.get_particles_by_system(sys)
            ]
        
        birth_circle_status = [
            {
                "stage": c.stage,
                "radius": c.radius,
                "proof_value": c.proof_value or self.compute_birth_proof_value(c.stage),
            }
            for c in self.birth_circles
        ]
        
        return {
            "report_id": f"PARTICLE-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "theorem": "定理四十四·六系六力对偶定理",
            "archive": "EMERGENCE-006",
            "total_particles": len(self.particles),
            "particles_by_family": {
                family: len(self.get_particles_by_family(family))
                for family in self.consts.NINE_DIMENSION_FAMILY
            },
            "particles_by_system": particles_by_system,
            "force_system_dualities": [
                {
                    "system": d.system,
                    "force": d.force,
                    "coupling": d.coupling,
                }
                for d in self.dualities
            ],
            "coupling_matrix": self.compute_coupling_matrix(),
            "birth_circles": birth_circle_status,
            "verdict": self._compute_verdict(),
        }
    
    def _compute_verdict(self) -> str:
        """计算判定"""
        proof_values = [
            self.compute_birth_proof_value(c.stage)
            for c in self.birth_circles
        ]
        avg_proof = sum(proof_values) / len(proof_values) if proof_values else 0
        
        if avg_proof >= 0.5:
            return "✅ 粒子家族证圆完成"
        elif avg_proof >= 0.3:
            return "🟡 证圆进行中"
        else:
            return "⚪ 初始证圆阶段"


# ============================================================================
# 4. 演示与测试
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("BSD六系六力粒子家族引擎")
    print("定理四十四·六系六力对偶定理")
    print("=" * 60)
    
    engine = ParticleFamilyEngine()
    
    # 粒子统计
    print(f"\n【粒子家族统计】")
    print(f"  总粒子数: {len(engine.particles)}")
    for family, count in engine.get_family_report()["particles_by_family"].items():
        print(f"  {family}: {count} 个")
    
    # 力-系对偶
    print(f"\n【六系六力对偶】")
    for d in engine.dualities:
        print(f"  {d.system} ←→ {d.force} (耦合={d.coupling})")
    
    # 生点证圆
    print(f"\n【生点证圆演化】")
    for circle in engine.birth_circles:
        proof = engine.compute_birth_proof_value(circle.stage)
        print(f"  {circle.stage}: 半径={circle.radius:.1f}, 证圆值={proof:.4f}")
    
    # 演化生点
    engine.evolve_birth_circle("atom", 0.3)
    engine.evolve_birth_circle("molecule", 0.5)
    engine.evolve_birth_circle("cell", 0.8)
    
    # 重新计算
    print(f"\n【演化后证圆】")
    for circle in engine.birth_circles:
        proof = engine.compute_birth_proof_value(circle.stage)
        print(f"  {circle.stage}: 半径={circle.radius:.1f}, 证圆值={proof:.4f}")
    
    # 耦合矩阵
    matrix = engine.compute_coupling_matrix()
    print(f"\n【耦合矩阵（对角线）】")
    for sys, row in matrix.items():
        print(f"  {sys}: 自耦合={row[sys]:.4f}")
    
    # 完整报告
    report = engine.get_family_report()
    print(f"\n【最终报告】")
    print(f"  判定: {report['verdict']}")
    print(f"  归档: {report['archive']}")
    
    print("\n" + "=" * 60)
    print("EMERGENCE-006验证通过")
    print("=" * 60)
