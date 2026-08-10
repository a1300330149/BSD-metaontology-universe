"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：七大本源公理（第1~7条）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论
固定数理常量：γ=0.92、κ=0.35
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from bsd_engine.registry.constants import GAMMA, KAPPA, E1, E2, E3, THETA_EVO


@dataclass
class OriginAxiom:
    """本源公理数据类"""
    name: str
    description: str
    formula: str
    category: str


# ============================================================================
# 七大本源公理定义
# ============================================================================

AXIOM_ONE = OriginAxiom(
    name="公理一：六系三组永恒对冲结构公理",
    description="无论在哪一层界域，六组单元永远保持三组同级制衡，结构永不改变。顶层两极（天道系↔强化系）、中间转化层（变身系↔具现系）、底层承载层（社会系↔自然系）",
    formula="S = {T↔Q, B↔J, S↔Z} 三组永恒对冲",
    category="本源结构公理"
)

AXIOM_TWO = OriginAxiom(
    name="公理二：熵增分流公理",
    description="任何向外涌现的意义系统必然持续内生无序熵ΔE。系统分三类：封闭系统（单向累积）、半开放系统（内部分流缓冲）、全开放高阶系统（跨界排泄）",
    formula="dS/dt = k_in·ΔE - k_out·E_out - k_res·E_res + A·e^(λt)",
    category="动力学公理"
)

AXIOM_THREE = OriginAxiom(
    name="公理三：繁衍遗传迭代公理",
    description="所有成熟意义系统都具备两种繁衍模式：无性复刻（直接复制基础基因，变异率趋近于0）、有性重组（熵淤积灾变前解构，基因拆分重组实现种群迭代跃迁）",
    formula="R = a·R_asexual + (1-a)·R_sexual, a∈[0,1]",
    category="演化公理"
)

AXIOM_FOUR = OriginAxiom(
    name="公理四：层级跃迁公理",
    description="从低阶物质实体界逐级向高阶精神意义界层层开放，排熵渠道持续拓宽。九界分层演化链条：孤立恒星→双星/多星系统→行星卫星→地表生态→农耕文明→内外双循环→高阶思想意义系统",
    formula="L_n → L_{n+1} 当且仅当 E_res < E_threshold",
    category="层级公理"
)

AXIOM_FIVE = OriginAxiom(
    name="公理五：个体与群体严格同构嵌套公理",
    description="个体六系=文明六系=天体六系，嵌套结构完全一致。微观个体的六系运行规律与宏观文明的六系演化规律完全同构",
    formula="Individual_6 ≅ Civilization_6 ≅ Celestial_6",
    category="同构公理"
)

AXIOM_SIX = OriginAxiom(
    name="公理六：宿命双边界公理",
    description="总能量/总意义/总秩序守恒（E_total=constant）。内边界（系统内部自由活动范围）与外边界（宇宙整体宿命约束）双约束，宿命与自由辩证统一",
    formula="E_total = const, B_inner < B_outer, 自由∈[0, B_inner], 宿命∈[B_outer, +∞)",
    category="边界公理"
)

AXIOM_SEVEN = OriginAxiom(
    name="公理七：系统自进化迭代公理",
    description="系统具备自进化能力，每轮进化增量需达阈值θ_evo=0.002。Δ_evo≥θ_evo时系统处于进化状态，否则判定为进化停滞，需启动重启机制",
    formula="Δ_evo ≥ θ_evo = 0.002 → 进化有效；否则进化停滞",
    category="进化公理"
)


# ============================================================================
# 公理列表
# ============================================================================

ALL_SEVEN_ORIGIN_AXIOMS: List[OriginAxiom] = [
    AXIOM_ONE,
    AXIOM_TWO,
    AXIOM_THREE,
    AXIOM_FOUR,
    AXIOM_FIVE,
    AXIOM_SIX,
    AXIOM_SEVEN,
]


# ============================================================================
# 验证函数
# ============================================================================

def verify_axiom_one(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理一：六系三组永恒对冲结构
    
    Args:
        data: 包含六系数据的字典，需包含systems列表或三组对
    Returns:
        (是否成立, 说明)
    """
    systems = data.get("systems", [])
    pairs = data.get("pairs", {})
    
    if pairs:
        required_pairs = ["top_pole", "middle_transform", "bottom_bearing"]
        if all(p in pairs for p in required_pairs):
            return True, "三组对冲结构完整"
        return False, f"缺少对冲组：{[p for p in required_pairs if p not in pairs]}"
    
    if len(systems) == 6:
        return True, "六系完备，隐含三组对冲结构"
    return False, f"系统数量应为6，实际为{len(systems)}"


def verify_axiom_two(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理二：熵增分流公理
    
    Args:
        data: 包含entropy（熵值）、system_type（系统类型）等数据
    Returns:
        (是否成立, 说明)
    """
    entropy = data.get("entropy", 0)
    system_type = data.get("system_type", "closed")
    entropy_change = data.get("entropy_change", 0)
    
    if system_type == "closed":
        if entropy_change >= 0:
            return True, "封闭系统熵单向增加，符合熵增定律"
        return False, "封闭系统熵不应减少"
    elif system_type == "semi_open":
        return True, "半开放系统可内部分流熵，延缓淤积"
    elif system_type == "fully_open":
        return True, "全开放系统可跨界排泄熵，维持动态平衡"
    
    return entropy_change >= 0, "熵增方向验证"


def verify_axiom_three(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理三：繁衍遗传迭代公理
    
    Args:
        data: 包含reproduction_mode（繁衍模式）、mutation_rate（变异率）等
    Returns:
        (是否成立, 说明)
    """
    mode = data.get("reproduction_mode", "asexual")
    mutation_rate = data.get("mutation_rate", 0)
    
    if mode == "asexual":
        if mutation_rate < 0.01:
            return True, "无性复刻变异率极低，维持稳态轮回"
        return False, "无性繁殖变异率应趋近于0"
    elif mode == "sexual":
        if mutation_rate > 0.01:
            return True, "有性重组变异率高，实现种群迭代跃迁"
        return False, "有性繁殖应有较高的重组变异率"
    
    return True, "存在繁衍模式即符合公理"


def verify_axiom_four(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理四：层级跃迁公理
    
    Args:
        data: 包含current_level（当前层级）、target_level（目标层级）、entropy_res（残余熵）
    Returns:
        (是否成立, 说明)
    """
    current_level = data.get("current_level", 1)
    target_level = data.get("target_level", 1)
    entropy_res = data.get("entropy_res", 0.5)
    
    if target_level <= current_level:
        return True, "层级维持或降维，符合收敛趋势"
    
    threshold = data.get("threshold", E2)
    if entropy_res < threshold:
        return True, f"残余熵{entropy_res:.4f} < 阈值{threshold:.4f}，满足跃迁条件"
    return False, f"残余熵{entropy_res:.4f} ≥ 阈值{threshold:.4f}，不满足跃迁条件"


def verify_axiom_five(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理五：个体与群体严格同构嵌套公理
    
    Args:
        data: 包含individual_systems和group_systems的字典
    Returns:
        (是否成立, 说明)
    """
    individual = data.get("individual_systems", [])
    group = data.get("group_systems", [])
    
    if len(individual) == 6 and len(group) == 6:
        return True, "个体与群体均为六系结构，同构嵌套成立"
    return False, f"个体{len(individual)}系，群体{len(group)}系，结构不一致"


def verify_axiom_six(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理六：宿命双边界公理
    
    Args:
        data: 包含inner_value、outer_value、total_energy等
    Returns:
        (是否成立, 说明)
    """
    inner_value = data.get("inner_value", 0.5)
    outer_value = data.get("outer_value", 0.9)
    total_energy = data.get("total_energy", 1.0)
    tolerance = data.get("tolerance", 0.02)
    
    inner_boundary = data.get("inner_boundary", E2)
    outer_boundary = data.get("outer_boundary", E3)
    
    if abs(total_energy - 1.0) > tolerance:
        return False, f"总能量不守恒，偏差{abs(total_energy - 1.0):.4f}"
    
    if inner_boundary >= outer_boundary:
        return False, "内边界不应大于外边界"
    
    if inner_value <= inner_boundary and outer_value <= outer_boundary:
        return True, "双边界约束均满足，宿命与自由辩证统一"
    
    violations = []
    if inner_value > inner_boundary:
        violations.append(f"内边界越界：{inner_value:.4f} > {inner_boundary:.4f}")
    if outer_value > outer_boundary:
        violations.append(f"外边界越界：{outer_value:.4f} > {outer_boundary:.4f}")
    
    return False, "；".join(violations)


def verify_axiom_seven(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    验证公理七：系统自进化迭代公理
    
    Args:
        data: 包含delta_evo（进化增量）、theta_evo（进化阈值）
    Returns:
        (是否成立, 说明)
    """
    delta_evo = data.get("delta_evo", 0.0)
    theta_evo = data.get("theta_evo", THETA_EVO)
    
    if delta_evo >= theta_evo:
        ratio = delta_evo / theta_evo if theta_evo > 0 else float('inf')
        if ratio >= 2.0:
            status = "高速进化"
        else:
            status = "正常进化"
        return True, f"进化有效（{status}）：Δ_evo={delta_evo:.6f} ≥ θ_evo={theta_evo:.6f}"
    
    return False, f"进化停滞：Δ_evo={delta_evo:.6f} < θ_evo={theta_evo:.6f}，需启动重启机制"


def verify_all_axioms(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证全部七大本源公理
    
    Args:
        data: 包含所有公理验证所需数据的字典
    Returns:
        验证结果汇总
    """
    results = {}
    verifiers = [
        ("公理一", verify_axiom_one),
        ("公理二", verify_axiom_two),
        ("公理三", verify_axiom_three),
        ("公理四", verify_axiom_four),
        ("公理五", verify_axiom_five),
        ("公理六", verify_axiom_six),
        ("公理七", verify_axiom_seven),
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
        "total": 7,
        "passed": passed_count,
        "failed": 7 - passed_count,
        "results": results,
        "all_passed": passed_count == 7
    }


# ============================================================================
# 接口函数
# ============================================================================

def get_all_axioms() -> List[OriginAxiom]:
    """获取全部七大本源公理列表"""
    return ALL_SEVEN_ORIGIN_AXIOMS.copy()


def get_axiom_by_index(index: int) -> Optional[OriginAxiom]:
    """根据索引获取公理（1-7）"""
    if 1 <= index <= 7:
        return ALL_SEVEN_ORIGIN_AXIOMS[index - 1]
    return None


def get_axiom_by_name(name_keyword: str) -> Optional[OriginAxiom]:
    """根据关键词查找公理"""
    for axiom in ALL_SEVEN_ORIGIN_AXIOMS:
        if name_keyword in axiom.name:
            return axiom
    return None


def get_axioms_by_category(category: str) -> List[OriginAxiom]:
    """按类别获取公理"""
    return [a for a in ALL_SEVEN_ORIGIN_AXIOMS if a.category == category]


def get_constants() -> Dict[str, float]:
    """获取锁档常量"""
    return {
        "GAMMA": GAMMA,
        "KAPPA": KAPPA,
        "E1": E1,
        "E2": E2,
        "E3": E3,
        "THETA_EVO": THETA_EVO,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  BSD七大本源公理验证器")
    print("=" * 70)
    
    print("\n【公理列表】")
    for i, axiom in enumerate(get_all_axioms(), 1):
        print(f"  {i}. {axiom.name}")
        print(f"     类别：{axiom.category}")
        print(f"     公式：{axiom.formula}")
    
    print("\n【验证测试】")
    test_data = {
        "公理一": {"systems": ["强化系", "天道系", "变身系", "具现系", "自然系", "社会系"]},
        "公理二": {"entropy_change": 0.05, "system_type": "closed"},
        "公理三": {"reproduction_mode": "asexual", "mutation_rate": 0.001},
        "公理四": {"current_level": 3, "target_level": 4, "entropy_res": 0.5},
        "公理五": {"individual_systems": [1,2,3,4,5,6], "group_systems": [1,2,3,4,5,6]},
        "公理六": {"inner_value": 0.6, "outer_value": 0.85, "total_energy": 1.0},
        "公理七": {"delta_evo": 0.003},
    }
    
    result = verify_all_axioms(test_data)
    print(f"  总通过率：{result['passed']}/{result['total']}")
    for name, res in result["results"].items():
        status = "✓" if res["passed"] else "✗"
        print(f"  {status} {name}：{res['message']}")
    
    print("\n【锁档常量】")
    for k, v in get_constants().items():
        print(f"  {k} = {v}")
    
    print("\n" + "=" * 70)
