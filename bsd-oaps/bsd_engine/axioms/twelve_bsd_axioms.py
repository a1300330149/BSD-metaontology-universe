"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：12条BSD基础公理（第1~12条）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/01_BSD核心定义
固定数理常量：γ=0.92、κ=0.35
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from bsd_engine.registry.constants import GAMMA, KAPPA, ALPHA, E1, E2, E3


@dataclass
class BSDBaseAxiom:
    """BSD基础公理数据类"""
    name: str
    description: str
    formula: str
    category: str


# ============================================================================
# 12条BSD基础公理定义
# ============================================================================

BSD_AXIOM_01 = BSDBaseAxiom(
    name="公理一：双时针动力学公理",
    description="个体顺时针演化与群体逆时针演化构成双时针动力学系统。个体从强化系始发顺时针传导，文明从天道系始发逆时针传导，双时针相互作用推动系统演化",
    formula="T_individual(顺时针) + T_civilization(逆时针) = 双时针动力学",
    category="动力学公理"
)

BSD_AXIOM_02 = BSDBaseAxiom(
    name="公理二：顶点相生相克公理",
    description="强化系与天道系作为体系两极，天生相克但可通过中间系中转达成高阶相生。相克是常态，相生是高阶态",
    formula="强化系 ⇄ 天道系：相克常态 + 中转相生",
    category="关系公理"
)

BSD_AXIOM_03 = BSDBaseAxiom(
    name="公理三：亲缘层级衰减公理",
    description="意义能量沿亲缘链路逐级传导时，每传递一个层级固定衰减。本系盈余不递减，从第一外溢亲缘承接系开始衰减",
    formula="M(n) = M₀·γ^(n-n₀), 其中γ=0.92为衰减系数",
    category="传导公理"
)

BSD_AXIOM_04 = BSDBaseAxiom(
    name="公理四：好坏天然对偶性公理",
    description="任何事物都天然具备好坏两面，二者对偶存在、不可分割。正向意义与负向意义共生共灭",
    formula="Good ∝ Bad, 好坏对偶、不可分割",
    category="对偶公理"
)

BSD_AXIOM_05 = BSDBaseAxiom(
    name="公理五：路径惯性公理",
    description="系统一旦进入某条演化路径，会产生路径依赖惯性，偏离路径需要额外能量输入。路径越长、惯性越大",
    formula="I = ∫_0^T γ^t dt, 路径越长惯性越大",
    category="惯性公理"
)

BSD_AXIOM_06 = BSDBaseAxiom(
    name="公理六：极端客观不对量公理",
    description="极端情况下的客观规律与常态不对等，极端条件会改变系统的运行规则。两端极值具有特殊性",
    formula="f(x)|_{x→极端} ≠ f(x)|_{x∈常态}",
    category="极端公理"
)

BSD_AXIOM_07 = BSDBaseAxiom(
    name="公理七：意义识别阈值公理",
    description="意义识别存在阈值，低于阈值的意义无法被感知和识别。只有突破阈值的意义差才能被系统察觉",
    formula="ΔΨ ≥ θ_recognition → 意义可识别",
    category="阈值公理"
)

BSD_AXIOM_08 = BSDBaseAxiom(
    name="公理八：引进本地化衰减公理",
    description="外来文化、技术、制度等引入本地时，会发生本地化衰减，原始效能按比例降低",
    formula="E_local = E_original · κ, 其中κ=0.35为本地化衰减系数",
    category="衰减公理"
)

BSD_AXIOM_09 = BSDBaseAxiom(
    name="公理九：范式更替本体公理",
    description="范式更替是系统演化的本体论特征，旧范式的死亡孕育新范式的诞生。范式跃迁是临界涌现过程",
    formula="Paradigm_n → Paradigm_{n+1} 临界涌现式更替",
    category="范式公理"
)

BSD_AXIOM_10 = BSDBaseAxiom(
    name="公理十：量级制衡公理",
    description="不同量级的系统之间存在制衡关系，量级差决定制衡方式。大系统制约小系统，小系统反作用于大系统",
    formula="Scale_A / Scale_B → 制衡强度与方式",
    category="制衡公理"
)

BSD_AXIOM_11 = BSDBaseAxiom(
    name="公理十一：载体同质化周期公理",
    description="意义载体存在同质化周期，达到一定阶段后载体趋同，需要新载体破局。同质化-异质化周期性循环",
    formula="载体同质化 → 意义空转 → 新载体涌现 → 再同质化",
    category="周期公理"
)

BSD_AXIOM_12 = BSDBaseAxiom(
    name="公理十二：群体投票价值公理",
    description="群体投票结果具有价值发现功能，群体智慧在一定条件下优于个体判断。但群体也可能陷入非理性狂热",
    formula="V_group = f(N, diversity, independence) 的非线性函数",
    category="群体公理"
)


# ============================================================================
# 公理列表
# ============================================================================

ALL_TWELVE_BSD_AXIOMS: List[BSDBaseAxiom] = [
    BSD_AXIOM_01,
    BSD_AXIOM_02,
    BSD_AXIOM_03,
    BSD_AXIOM_04,
    BSD_AXIOM_05,
    BSD_AXIOM_06,
    BSD_AXIOM_07,
    BSD_AXIOM_08,
    BSD_AXIOM_09,
    BSD_AXIOM_10,
    BSD_AXIOM_11,
    BSD_AXIOM_12,
]


# ============================================================================
# 验证函数
# ============================================================================

def verify_dual_clock_dynamics(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理一：双时针动力学公理"""
    clockwise = data.get("clockwise", False)
    counterclockwise = data.get("counterclockwise", False)
    individual_origin = data.get("individual_origin", "强化系")
    civilization_origin = data.get("civilization_origin", "天道系")
    
    if clockwise and counterclockwise:
        if individual_origin == "强化系" and civilization_origin == "天道系":
            return True, "双时针动力学成立：个体顺时针（强化始发）+ 文明逆时针（天道始发）"
        return False, "双时针存在但始发端不匹配"
    
    if clockwise or counterclockwise:
        return False, "仅单时针运行，双时针动力学不完整"
    
    return False, "无时针运行数据"


def verify_vertex_mutualism(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理二：顶点相生相克公理"""
    conflict = data.get("conflict_level", 0.5)
    harmony = data.get("harmony_level", 0.3)
    has_middle_transition = data.get("has_middle_transition", False)
    
    if conflict > 0 and not has_middle_transition:
        return True, "顶点相克常态成立，无中间系中转时两极对立"
    
    if has_middle_transition and harmony > conflict:
        return True, "顶点高阶相生成立：中间系中转打通两极相克"
    
    if conflict > 0 and harmony > 0:
        return True, "顶点相生相克同时存在，辩证统一"
    
    return False, "顶点关系数据不足"


def verify_kinship_decay(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理三：亲缘层级衰减公理"""
    levels = data.get("levels", [])
    values = data.get("values", [])
    decay_coefficient = data.get("decay_coefficient", GAMMA)
    
    if len(levels) < 2 or len(values) < 2:
        return False, "层级数据不足，至少需要2个层级"
    
    decay_ratios = []
    for i in range(1, len(values)):
        if values[i-1] > 0:
            ratio = values[i] / values[i-1]
            decay_ratios.append(ratio)
    
    if not decay_ratios:
        return False, "无法计算衰减比率"
    
    avg_ratio = sum(decay_ratios) / len(decay_ratios)
    
    if all(r <= 1.0 for r in decay_ratios):
        return True, (
            f"亲缘层级衰减成立：平均衰减比={avg_ratio:.4f}，"
            f"γ={decay_coefficient:.2f}，"
            f"逐级递减趋势一致"
        )
    
    return False, f"存在层级值递增，不符合衰减规律"


def verify_good_bad_duality(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理四：好坏天然对偶性公理"""
    good = data.get("good", 0)
    bad = data.get("bad", 0)
    
    if good > 0 and bad > 0:
        ratio = min(good, bad) / max(good, bad) if max(good, bad) > 0 else 0
        return True, f"好坏对偶成立：好={good:.4f}, 坏={bad:.4f}, 对偶比={ratio:.4f}"
    
    if good == 0 and bad == 0:
        return False, "好坏均为零，无对偶意义"
    
    return False, f"仅存在{'好' if good > 0 else '坏'}的单极，对偶不成立"


def verify_path_inertia(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理五：路径惯性公理"""
    path_length = data.get("path_length", 0)
    inertia = data.get("inertia", 0)
    deviation_energy = data.get("deviation_energy", 0)
    
    if path_length > 0 and inertia > 0:
        if inertia >= path_length * GAMMA:
            return True, f"路径惯性成立：路径长度={path_length}, 惯性={inertia:.4f}，正相关"
        return True, f"路径惯性存在：路径长度={path_length}, 惯性={inertia:.4f}"
    
    if deviation_energy > 0:
        return True, f"偏离路径需要能量：{deviation_energy:.4f}，惯性存在"
    
    return False, "路径惯性数据不足"


def verify_extreme_asymmetry(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理六：极端客观不对量公理"""
    normal_value = data.get("normal_value", 0.5)
    extreme_value = data.get("extreme_value", 0.8)
    extreme_type = data.get("extreme_type", "high")
    
    if normal_value != extreme_value:
        asymmetry = abs(extreme_value - normal_value) / max(abs(normal_value), 1e-6)
        return True, (
            f"极端不对量成立：常态={normal_value:.4f}, "
            f"极端({extreme_type})={extreme_value:.4f}, "
            f"不对量度={asymmetry:.4f}"
        )
    
    return False, "常态与极端值相同，不对量不明显"


def verify_meaning_recognition_threshold(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理七：意义识别阈值公理"""
    meaning_diff = data.get("meaning_diff", 0)
    threshold = data.get("threshold", E1)
    is_recognized = data.get("is_recognized", None)
    
    if is_recognized is not None:
        expected = meaning_diff >= threshold
        if is_recognized == expected:
            status = "可识别" if is_recognized else "不可识别"
            return True, f"意义识别阈值匹配：ΔΨ={meaning_diff:.4f} θ={threshold:.4f} → {status}"
        return False, f"识别结果与阈值判定不符"
    
    if meaning_diff >= threshold:
        return True, f"意义可识别：ΔΨ={meaning_diff:.4f} ≥ θ={threshold:.4f}"
    
    return False, f"意义不可识别：ΔΨ={meaning_diff:.4f} < θ={threshold:.4f}"


def verify_localization_decay(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理八：引进本地化衰减公理"""
    original_effect = data.get("original_effect", 1.0)
    local_effect = data.get("local_effect", 0.5)
    decay_coefficient = data.get("decay_coefficient", KAPPA)
    
    if original_effect <= 0:
        return False, "原始效能不能为零或负"
    
    actual_decay_ratio = local_effect / original_effect
    expected_local = original_effect * decay_coefficient
    
    if actual_decay_ratio < 1.0:
        return True, (
            f"本地化衰减成立：原始效能={original_effect:.4f}, "
            f"本地效能={local_effect:.4f}, "
            f"实际衰减比={actual_decay_ratio:.4f}, "
            f"κ={decay_coefficient:.2f}"
        )
    
    return False, "本地效能不低于原始效能，衰减不成立"


def verify_paradigm_shift(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理九：范式更替本体公理"""
    old_paradigm = data.get("old_paradigm", None)
    new_paradigm = data.get("new_paradigm", None)
    is_critical_emergence = data.get("is_critical_emergence", None)
    transition_phase = data.get("transition_phase", "")
    
    if old_paradigm and new_paradigm and old_paradigm != new_paradigm:
        if is_critical_emergence:
            return True, f"范式更替成立：{old_paradigm} → {new_paradigm}（临界涌现式）"
        return True, f"范式更替成立：{old_paradigm} → {new_paradigm}"
    
    if transition_phase in ["old_death", "new_birth", "transition"]:
        return True, f"范式更替进行中：阶段={transition_phase}"
    
    return False, "范式更替数据不足"


def verify_scale_balance(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理十：量级制衡公理"""
    scale_a = data.get("scale_a", 1.0)
    scale_b = data.get("scale_b", 0.5)
    balance_strength = data.get("balance_strength", 0)
    
    if scale_a > 0 and scale_b > 0:
        scale_ratio = max(scale_a, scale_b) / min(scale_a, scale_b)
        if balance_strength > 0:
            return True, f"量级制衡存在：量级比={scale_ratio:.2f}, 制衡强度={balance_strength:.4f}"
        return True, f"量级差异存在：量级比={scale_ratio:.2f}，制衡隐含"
    
    return False, "量级数据不足"


def verify_carrier_homogenization(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理十一：载体同质化周期公理"""
    homogenization_degree = data.get("homogenization_degree", 0)
    cycle_phase = data.get("cycle_phase", "")
    carrier_count = data.get("carrier_count", 0)
    
    if homogenization_degree >= 0.7:
        return True, f"载体高度同质化：{homogenization_degree:.4f}，周期峰值阶段"
    
    if cycle_phase in ["homogenization", "heterogenization", "new_carrier"]:
        return True, f"载体周期循环：当前阶段={cycle_phase}"
    
    if carrier_count > 1 and homogenization_degree > 0:
        return True, f"载体同质化进行中：程度={homogenization_degree:.4f}, 载体数={carrier_count}"
    
    return False, "载体同质化数据不足"


def verify_group_voting_value(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理十二：群体投票价值公理"""
    group_size = data.get("group_size", 0)
    diversity = data.get("diversity", 0.5)
    independence = data.get("independence", 0.5)
    group_accuracy = data.get("group_accuracy", 0)
    individual_accuracy = data.get("individual_accuracy", 0)
    
    if group_accuracy > 0 and individual_accuracy > 0:
        if group_accuracy > individual_accuracy:
            return True, (
                f"群体智慧成立：群体准确率={group_accuracy:.4f} > "
                f"个体准确率={individual_accuracy:.4f}"
            )
        return True, (
            f"群体投票存在：群体准确率={group_accuracy:.4f}, "
            f"个体准确率={individual_accuracy:.4f}"
        )
    
    if group_size > 0 and diversity > 0 and independence > 0:
        value = group_size * diversity * independence
        return True, f"群体投票价值要素具备：规模={group_size}, 多样性={diversity:.2f}, 独立性={independence:.2f}"
    
    return False, "群体投票数据不足"


def verify_all_bsd_axioms(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证全部12条BSD基础公理
    
    Args:
        data: 包含所有公理验证所需数据的字典
    Returns:
        验证结果汇总
    """
    results = {}
    verifiers = [
        ("双时针动力学", verify_dual_clock_dynamics),
        ("顶点相生相克", verify_vertex_mutualism),
        ("亲缘层级衰减", verify_kinship_decay),
        ("好坏天然对偶", verify_good_bad_duality),
        ("路径惯性", verify_path_inertia),
        ("极端客观不对量", verify_extreme_asymmetry),
        ("意义识别阈值", verify_meaning_recognition_threshold),
        ("引进本地化衰减", verify_localization_decay),
        ("范式更替本体", verify_paradigm_shift),
        ("量级制衡", verify_scale_balance),
        ("载体同质化周期", verify_carrier_homogenization),
        ("群体投票价值", verify_group_voting_value),
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
        "total": 12,
        "passed": passed_count,
        "failed": 12 - passed_count,
        "results": results,
        "all_passed": passed_count == 12
    }


# ============================================================================
# 接口函数
# ============================================================================

def get_all_axioms() -> List[BSDBaseAxiom]:
    """获取全部12条BSD基础公理列表"""
    return ALL_TWELVE_BSD_AXIOMS.copy()


def get_axiom_by_index(index: int) -> Optional[BSDBaseAxiom]:
    """根据索引获取公理（1-12）"""
    if 1 <= index <= 12:
        return ALL_TWELVE_BSD_AXIOMS[index - 1]
    return None


def get_axiom_by_name(name_keyword: str) -> Optional[BSDBaseAxiom]:
    """根据关键词查找公理"""
    for axiom in ALL_TWELVE_BSD_AXIOMS:
        if name_keyword in axiom.name:
            return axiom
    return None


def get_axioms_by_category(category: str) -> List[BSDBaseAxiom]:
    """按类别获取公理"""
    return [a for a in ALL_TWELVE_BSD_AXIOMS if a.category == category]


def get_constants() -> Dict[str, float]:
    """获取锁档常量"""
    return {
        "GAMMA": GAMMA,
        "KAPPA": KAPPA,
        "ALPHA": ALPHA,
        "E1": E1,
        "E2": E2,
        "E3": E3,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("  BSD12条基础公理验证器")
    print("=" * 70)
    
    print("\n【公理列表】")
    for i, axiom in enumerate(get_all_axioms(), 1):
        print(f"  {i:2d}. {axiom.name}")
        print(f"      类别：{axiom.category}")
        print(f"      公式：{axiom.formula}")
    
    print("\n【验证测试】")
    test_data = {
        "双时针动力学": {"clockwise": True, "counterclockwise": True},
        "顶点相生相克": {"conflict_level": 0.6, "harmony_level": 0.4},
        "亲缘层级衰减": {"levels": [1,2,3,4], "values": [100, 92, 85, 78]},
        "好坏天然对偶": {"good": 0.7, "bad": 0.5},
        "路径惯性": {"path_length": 10, "inertia": 8.5},
        "极端客观不对量": {"normal_value": 0.5, "extreme_value": 0.9},
        "意义识别阈值": {"meaning_diff": 0.4, "threshold": 0.35},
        "引进本地化衰减": {"original_effect": 1.0, "local_effect": 0.4},
        "范式更替本体": {"old_paradigm": "工业文明", "new_paradigm": "信息文明"},
        "量级制衡": {"scale_a": 100, "scale_b": 30, "balance_strength": 0.6},
        "载体同质化周期": {"homogenization_degree": 0.75},
        "群体投票价值": {"group_accuracy": 0.75, "individual_accuracy": 0.6},
    }
    
    result = verify_all_bsd_axioms(test_data)
    print(f"  总通过率：{result['passed']}/{result['total']}")
    for name, res in result["results"].items():
        status = "✓" if res["passed"] else "✗"
        print(f"  {status} {name}：{res['message']}")
    
    print("\n【锁档常量】")
    for k, v in get_constants().items():
        print(f"  {k} = {v}")
    
    print("\n" + "=" * 70)
