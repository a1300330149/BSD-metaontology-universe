"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：三条意义公理（第1~3条）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/意义大一统V2.0
固定数理常量：γ=0.92、κ=0.35
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from bsd_engine.registry.constants import GAMMA, KAPPA, ALPHA, E1, E2


@dataclass
class MeaningAxiom:
    """意义公理数据类"""
    name: str
    description: str
    formula: str
    category: str


# ============================================================================
# 三条意义公理定义
# ============================================================================

MEANING_AXIOM_ONE = MeaningAxiom(
    name="公理一：意义涌现公理",
    description="低层级系统交互涌现高层级意义，意义层级不可逆。从物理到生命，从生命到意识，从意识到灵性，高层级意义不等于低层级意义的简单加总",
    formula="Ψ_n = E(Ψ_{n-1}, ...) ≠ ΣΨ_i",
    category="意义生成公理"
)

MEANING_AXIOM_TWO = MeaningAxiom(
    name="公理二：意义权重公理",
    description="意义权重按层级分配，层级越高权重越大。由认知贡献C、结构贡献S、实践贡献P三部分加权组成",
    formula="W_n = α·C_n + β·S_n + γ·P_n",
    category="意义权重公理"
)

MEANING_AXIOM_THREE = MeaningAxiom(
    name="公理三：意义守恒公理",
    description="全域意义总量守恒，意义不生不灭，仅在不同层级、不同形态间转化。加权意义总量为常数",
    formula="ΣΨ_n·W_n = const",
    category="意义守恒公理"
)


# ============================================================================
# 公理列表
# ============================================================================

ALL_THREE_MEANING_AXIOMS: List[MeaningAxiom] = [
    MEANING_AXIOM_ONE,
    MEANING_AXIOM_TWO,
    MEANING_AXIOM_THREE,
]


# ============================================================================
# 意义层级定义
# ============================================================================

MEANING_LEVELS = {
    "physical": {
        "name": "物理层",
        "level_index": 1,
        "weight": 0.1,
        "description": "物质能量时空的物理交互，基础存在"
    },
    "life": {
        "name": "生命层",
        "level_index": 2,
        "weight": 0.2,
        "description": "生命系统涌现，自我复制、新陈代谢、进化"
    },
    "consciousness": {
        "name": "意识层",
        "level_index": 3,
        "weight": 0.3,
        "description": "意识心智涌现，感知、思维、情感、意志"
    },
    "spiritual": {
        "name": "灵性层",
        "level_index": 4,
        "weight": 0.4,
        "description": "灵性超越涌现，开悟、解脱、与道合一"
    }
}


# ============================================================================
# 验证函数
# ============================================================================

def verify_meaning_emergence(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理一：意义涌现公理
    
    Args:
        data: 包含low_level_meaning（低层级意义列表）、high_level_meaning（高层级意义）
    Returns:
        (是否成立, 说明)
    """
    low_meanings = data.get("low_level_meaning", [])
    high_meaning = data.get("high_level_meaning", 0)
    
    if not low_meanings:
        return False, "缺少低层级意义数据"
    
    sum_low = sum(low_meanings)
    
    if abs(high_meaning - sum_low) < 1e-6:
        return False, f"高层级意义（{high_meaning:.4f}）等于低层级总和（{sum_low:.4f}），未发生涌现"
    
    emergence_threshold = data.get("emergence_threshold", E2)
    emergence_degree = abs(high_meaning - sum_low) / max(sum_low, 1e-6)
    
    if emergence_degree >= emergence_threshold:
        return True, (
            f"意义涌现成立：高层级意义={high_meaning:.4f}，"
            f"低层级总和={sum_low:.4f}，"
            f"涌现度={emergence_degree:.4f} ≥ 阈值={emergence_threshold:.4f}"
        )
    
    return False, (
        f"涌现度不足：{emergence_degree:.4f} < 阈值{emergence_threshold:.4f}"
    )


def verify_meaning_weight(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理二：意义权重公理
    
    Args:
        data: 包含cognitive（认知贡献C）、structural（结构贡献S）、practical（实践贡献P）
              或包含alpha、beta、gamma权重系数
    Returns:
        (是否成立, 说明)
    """
    C = data.get("cognitive", 0.0)
    S = data.get("structural", 0.0)
    P = data.get("practical", 0.0)
    
    alpha = data.get("alpha", ALPHA)
    beta = data.get("beta", GAMMA)
    gamma = data.get("gamma", KAPPA)
    
    weight_sum = alpha + beta + gamma
    if abs(weight_sum - 1.0) > 0.1:
        norm_factor = weight_sum
        alpha_norm = alpha / norm_factor
        beta_norm = beta / norm_factor
        gamma_norm = gamma / norm_factor
    else:
        alpha_norm = alpha
        beta_norm = beta
        gamma_norm = gamma
    
    W = alpha_norm * C + beta_norm * S + gamma_norm * P
    
    components = {
        "认知贡献": C,
        "结构贡献": S,
        "实践贡献": P
    }
    non_zero = [k for k, v in components.items() if v > 0]
    
    if len(non_zero) >= 2:
        return True, (
            f"意义权重计算成立：W = {alpha_norm:.3f}·C + {beta_norm:.3f}·S + {gamma_norm:.3f}·P "
            f"= {W:.4f}（含{len(non_zero)}种贡献）"
        )
    
    return False, f"贡献维度不足，仅有{len(non_zero)}种：{non_zero}"


def verify_meaning_conservation(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理三：意义守恒公理
    
    Args:
        data: 包含meanings（各层意义列表）、weights（各层权重列表）
              或包含time_points（不同时间点的加权意义总量）
    Returns:
        (是否成立, 说明)
    """
    meanings = data.get("meanings", [])
    weights = data.get("weights", [])
    
    if "time_points" in data:
        time_points = data["time_points"]
        if len(time_points) < 2:
            return False, "至少需要2个时间点的数据进行守恒验证"
        
        values = [tp.get("total_weighted_meaning", 0) for tp in time_points]
        max_val = max(values)
        min_val = min(values)
        fluctuation = (max_val - min_val) / max(max_val, 1e-6)
        
        conservation_tolerance = data.get("tolerance", 0.05)
        
        if fluctuation <= conservation_tolerance:
            return True, (
                f"意义守恒成立：加权意义总量波动={fluctuation:.4f} "
                f"≤ 容差={conservation_tolerance:.4f}，"
                f"均值={sum(values)/len(values):.4f}"
            )
        return False, (
            f"意义守恒不成立：加权意义总量波动={fluctuation:.4f} "
            f"> 容差={conservation_tolerance:.4f}"
        )
    
    if not meanings or not weights:
        return False, "缺少意义或权重数据"
    
    if len(meanings) != len(weights):
        return False, f"意义数量({len(meanings)})与权重数量({len(weights)})不匹配"
    
    total_weighted = sum(m * w for m, w in zip(meanings, weights))
    
    return True, f"加权意义总量 = ΣΨ_n·W_n = {total_weighted:.4f} = const"


def verify_all_meaning_axioms(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证全部三条意义公理
    
    Args:
        data: 包含所有公理验证所需数据的字典
    Returns:
        验证结果汇总
    """
    results = {}
    verifiers = [
        ("意义涌现公理", verify_meaning_emergence),
        ("意义权重公理", verify_meaning_weight),
        ("意义守恒公理", verify_meaning_conservation),
    ]
    
    passed_count = 0
    for name, verifier in verifiers:
        axiom_data = data.get(name, data)
        passed, message = verifier(axiom_data)
        results[name] = {
            "passed": passed,
            "message": message
        }
        if passed:
            passed_count += 1
    
    return {
        "total": 3,
        "passed": passed_count,
        "failed": 3 - passed_count,
        "results": results,
        "all_passed": passed_count == 3
    }


# ============================================================================
# 辅助函数
# ============================================================================

def calculate_weighted_meaning(meaning_levels: Dict[str, float]) -> float:
    """
    计算加权意义总量
    
    Args:
        meaning_levels: 各层级意义值字典，如{"physical": 0.5, "life": 0.3, ...}
    Returns:
        加权意义总量
    """
    total = 0.0
    for level_key, value in meaning_levels.items():
        level_info = MEANING_LEVELS.get(level_key, {})
        weight = level_info.get("weight", 0.1)
        total += value * weight
    return total


def check_irreversibility(from_level: str, to_level: str) -> bool:
    """
    检查意义层级不可逆性
    
    Args:
        from_level: 起始层级
        to_level: 目标层级
    Returns:
        是否符合不可逆性（目标层级不低于起始层级）
    """
    from_idx = MEANING_LEVELS.get(from_level, {}).get("level_index", 0)
    to_idx = MEANING_LEVELS.get(to_level, {}).get("level_index", 0)
    return to_idx >= from_idx


# ============================================================================
# 接口函数
# ============================================================================

def get_all_axioms() -> List[MeaningAxiom]:
    """获取全部三条意义公理列表"""
    return ALL_THREE_MEANING_AXIOMS.copy()


def get_axiom_by_index(index: int) -> Optional[MeaningAxiom]:
    """根据索引获取公理（1-3）"""
    if 1 <= index <= 3:
        return ALL_THREE_MEANING_AXIOMS[index - 1]
    return None


def get_axiom_by_name(name_keyword: str) -> Optional[MeaningAxiom]:
    """根据关键词查找公理"""
    for axiom in ALL_THREE_MEANING_AXIOMS:
        if name_keyword in axiom.name:
            return axiom
    return None


def get_meaning_levels() -> Dict[str, Dict[str, Any]]:
    """获取意义四层级定义"""
    return MEANING_LEVELS.copy()


def get_constants() -> Dict[str, float]:
    """获取锁档常量"""
    return {
        "GAMMA": GAMMA,
        "KAPPA": KAPPA,
        "ALPHA": ALPHA,
        "E1": E1,
        "E2": E2,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  BSD三条意义公理验证器")
    print("=" * 70)
    
    print("\n【公理列表】")
    for i, axiom in enumerate(get_all_axioms(), 1):
        print(f"  {i}. {axiom.name}")
        print(f"     类别：{axiom.category}")
        print(f"     公式：{axiom.formula}")
    
    print("\n【意义层级】")
    for key, level in get_meaning_levels().items():
        print(f"  {level['level_index']}. {level['name']}：权重={level['weight']}")
    
    print("\n【验证测试】")
    test_data = {
        "意义涌现公理": {
            "low_level_meaning": [0.2, 0.3, 0.4],
            "high_level_meaning": 1.5,
            "emergence_threshold": 0.5
        },
        "意义权重公理": {
            "cognitive": 0.6,
            "structural": 0.5,
            "practical": 0.7,
            "alpha": 0.3,
            "beta": 0.3,
            "gamma": 0.4
        },
        "意义守恒公理": {
            "time_points": [
                {"total_weighted_meaning": 1.00},
                {"total_weighted_meaning": 1.02},
                {"total_weighted_meaning": 0.99},
                {"total_weighted_meaning": 1.01},
            ],
            "tolerance": 0.05
        },
    }
    
    result = verify_all_meaning_axioms(test_data)
    print(f"  总通过率：{result['passed']}/{result['total']}")
    for name, res in result["results"].items():
        status = "✓" if res["passed"] else "✗"
        print(f"  {status} {name}：{res['message']}")
    
    print("\n【锁档常量】")
    for k, v in get_constants().items():
        print(f"  {k} = {v}")
    
    print("\n" + "=" * 70)
