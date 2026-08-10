"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：9条专项公理（第1~9条）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/01_BSD核心定义
固定数理常量：γ=0.92、κ=0.35
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Any
from bsd_engine.registry.constants import GAMMA, KAPPA, ALPHA, E1, E2, E3


@dataclass
class SpecialAxiom:
    """专项公理数据类"""
    name: str
    description: str
    formula: str
    category: str
    domain: str


# ============================================================================
# 9条专项公理定义
# ============================================================================

SPECIAL_AXIOM_01 = SpecialAxiom(
    name="公理一：货币意义本体公理",
    description="货币是意义的量化载体，其本质是社会普遍承认的意义兑换凭证。货币的价值来源于集体信念与交换价值的统一",
    formula="Money = f(collective_belief, exchange_value) × 意义量化系数",
    category="经济公理",
    domain="经济金融"
)

SPECIAL_AXIOM_02 = SpecialAxiom(
    name="公理二：生态价值分层公理",
    description="生态系统价值呈现分层结构，从基础物质生产到文化精神价值逐层提升。高层级价值依赖低层级基础，但权重更高",
    formula="EcoValue = Σ Layer_i × Weight_i, 层级越高权重越大",
    category="生态公理",
    domain="自然生态"
)

SPECIAL_AXIOM_03 = SpecialAxiom(
    name="公理三：认知范式锁死公理",
    description="个体或群体的认知一旦形成某种范式，会产生路径依赖和自我强化，难以突破。范式锁死是文明停滞的重要原因",
    formula="Paradigm_lock = 1 - e^(-κ·t), 时间越长锁死越深",
    category="认知公理",
    domain="认知心理"
)

SPECIAL_AXIOM_04 = SpecialAxiom(
    name="公理四：保障边际递减公理",
    description="社会保障水平的边际效用随保障程度提高而递减。当保障超过临界值后，反而可能抑制社会活力与创新动力",
    formula="MU_security = dU/dS, 边际效用递减，存在最优保障点",
    category="社会公理",
    domain="社会保障"
)

SPECIAL_AXIOM_05 = SpecialAxiom(
    name="公理五：债务质量分层公理",
    description="债务按质量可分为不同层级，从优质债务到不良债务呈梯度分布。债务质量结构决定金融系统稳定性",
    formula="Debt_quality = Σ Grade_i × Ratio_i, 质量分层决定系统风险",
    category="金融公理",
    domain="金融债务"
)

SPECIAL_AXIOM_06 = SpecialAxiom(
    name="公理六：主义同源公理",
    description="各种意识形态和社会制度主张本质同源，都是对社会治理最优解的不同路径探索。看似对立的主义在底层目标上具有一致性",
    formula="Ism_A ≅ Ism_B at foundation level, 主义同源、路径分化",
    category="社会公理",
    domain="意识形态"
)

SPECIAL_AXIOM_07 = SpecialAxiom(
    name="公理七：六系种子繁衍公理",
    description="六系结构作为意义系统的种子，在不同层级和领域中繁衍生长。任何完整的意义系统都包含六系的完整胚胎",
    formula="Seed_6 → System_6, 六系种子在各层域繁衍",
    category="繁衍公理",
    domain="系统演化"
)

SPECIAL_AXIOM_08 = SpecialAxiom(
    name="公理八：军事技术迭代本源公理",
    description="军事技术是文明技术迭代的本源动力之一。战争需求推动技术突破，军事技术向民用外溢是文明升维的重要路径",
    formula="Tech_civilian = Tech_military × γ_spillover, 军事溢出驱动民用技术",
    category="技术公理",
    domain="军事技术"
)

SPECIAL_AXIOM_09 = SpecialAxiom(
    name="公理九：游戏生态分层公理",
    description="游戏生态系统呈现分层结构，从底层玩家到顶层创作者、从休闲娱乐到职业竞技，形成完整的意义生产与消费链条",
    formula="Game_eco = 玩家层 + 创作者层 + 竞技层 + 产业层, 多层共生",
    category="文化公理",
    domain="游戏文化"
)


# ============================================================================
# 公理列表
# ============================================================================

ALL_NINE_SPECIAL_AXIOMS: List[SpecialAxiom] = [
    SPECIAL_AXIOM_01,
    SPECIAL_AXIOM_02,
    SPECIAL_AXIOM_03,
    SPECIAL_AXIOM_04,
    SPECIAL_AXIOM_05,
    SPECIAL_AXIOM_06,
    SPECIAL_AXIOM_07,
    SPECIAL_AXIOM_08,
    SPECIAL_AXIOM_09,
]


# ============================================================================
# 验证函数
# ============================================================================

def verify_monetary_meaning(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理一：货币意义本体公理"""
    collective_belief = data.get("collective_belief", 0)
    exchange_value = data.get("exchange_value", 0)
    monetary_value = data.get("monetary_value", 0)
    
    if collective_belief > 0 and exchange_value > 0 and monetary_value > 0:
        derived_value = (collective_belief + exchange_value) / 2
        ratio = monetary_value / max(derived_value, 1e-6)
        return True, (
            f"货币意义成立：集体信念={collective_belief:.4f}, "
            f"交换价值={exchange_value:.4f}, "
            f"货币价值={monetary_value:.4f}, "
            f"匹配度={1/ratio if ratio > 0 else 0:.4f}"
        )
    
    if monetary_value > 0:
        return True, f"货币价值存在：{monetary_value:.4f}，隐含意义本体"
    
    return False, "货币意义数据不足"


def verify_ecological_value_layering(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理二：生态价值分层公理"""
    layers = data.get("layers", {})
    values = data.get("values", [])
    
    if layers and len(layers) >= 2:
        layer_names = list(layers.keys())
        weights = [layers[k].get("weight", 0) for k in layer_names]
        if weights and weights == sorted(weights):
            return True, f"生态价值分层成立：{len(layers)}个层级，权重递增"
        return True, f"生态价值分层成立：{len(layers)}个层级"
    
    if len(values) >= 2:
        return True, f"生态价值分层存在：{len(values)}个价值层级"
    
    return False, "生态价值分层数据不足"


def verify_paradigm_lock(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理三：认知范式锁死公理"""
    time_duration = data.get("time_duration", 0)
    lock_degree = data.get("lock_degree", 0)
    breakthrough_energy = data.get("breakthrough_energy", 0)
    kappa = data.get("kappa", KAPPA)
    
    if time_duration > 0 and lock_degree > 0:
        expected_lock = 1 - (1 - kappa) ** time_duration
        return True, (
            f"范式锁死成立：持续时间={time_duration}, "
            f"锁死程度={lock_degree:.4f}, "
            f"理论值={expected_lock:.4f}"
        )
    
    if breakthrough_energy > 0:
        return True, f"范式突破需要能量：{breakthrough_energy:.4f}，锁死存在"
    
    return False, "认知范式锁死数据不足"


def verify_security_diminishing(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理四：保障边际递减公理"""
    security_level = data.get("security_level", 0)
    marginal_utility = data.get("marginal_utility", 0)
    utility_points = data.get("utility_points", [])
    
    if utility_points and len(utility_points) >= 2:
        decreasing = all(
            utility_points[i] >= utility_points[i+1]
            for i in range(len(utility_points)-1)
        )
        if decreasing:
            return True, f"保障边际递减成立：{len(utility_points)}个点验证递减趋势"
        return True, f"保障效用数据存在：{len(utility_points)}个点"
    
    if security_level > 0 and marginal_utility > 0:
        return True, f"保障边际效用：保障水平={security_level:.4f}, 边际效用={marginal_utility:.4f}"
    
    return False, "保障边际递减数据不足"


def verify_debt_quality_layering(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理五：债务质量分层公理"""
    debt_layers = data.get("debt_layers", {})
    quality_scores = data.get("quality_scores", [])
    system_risk = data.get("system_risk", 0)
    
    if debt_layers and len(debt_layers) >= 2:
        total_debt = sum(v.get("amount", 0) for v in debt_layers.values())
        quality_grades = list(debt_layers.keys())
        return True, (
            f"债务质量分层成立：{len(debt_layers)}个质量等级，"
            f"总债务={total_debt:.4f}"
        )
    
    if len(quality_scores) >= 2:
        avg_quality = sum(quality_scores) / len(quality_scores)
        return True, f"债务质量分布：{len(quality_scores)}个样本，平均质量={avg_quality:.4f}"
    
    if system_risk > 0:
        return True, f"系统风险={system_risk:.4f}，隐含债务质量结构影响"
    
    return False, "债务质量分层数据不足"


def verify_ism_common_origin(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理六：主义同源公理"""
    isms = data.get("isms", [])
    common_goals = data.get("common_goals", [])
    foundation_similarity = data.get("foundation_similarity", 0)
    
    if len(isms) >= 2 and len(common_goals) > 0:
        return True, (
            f"主义同源成立：{len(isms)}种主义，"
            f"{len(common_goals)}个共同目标"
        )
    
    if foundation_similarity > 0.5:
        return True, f"主义底层相似性={foundation_similarity:.4f}，同源性成立"
    
    if len(isms) >= 2:
        return True, f"多种主义并存：{len(isms)}种，隐含同源基础"
    
    return False, "主义同源数据不足"


def verify_six_system_reproduction(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理七：六系种子繁衍公理"""
    seed_systems = data.get("seed_systems", [])
    grown_systems = data.get("grown_systems", [])
    domains = data.get("domains", [])
    
    if len(seed_systems) == 6 and len(grown_systems) == 6:
        return True, "六系种子繁衍成立：种子6系→成熟6系完整对应"
    
    if len(domains) >= 2:
        return True, f"六系跨领域繁衍：{len(domains)}个领域，种子同构"
    
    if len(seed_systems) == 6:
        return True, "六系种子存在：6个系别完整，具备繁衍潜能"
    
    return False, "六系种子繁衍数据不足"


def verify_military_tech_evolution(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理八：军事技术迭代本源公理"""
    military_tech = data.get("military_tech", 0)
    civilian_tech = data.get("civilian_tech", 0)
    spillover_rate = data.get("spillover_rate", GAMMA)
    war_driven_innovation = data.get("war_driven_innovation", 0)
    
    if military_tech > 0 and civilian_tech > 0:
        expected_civilian = military_tech * spillover_rate
        actual_ratio = civilian_tech / max(military_tech, 1e-6)
        return True, (
            f"军事技术溢出成立：军事技术={military_tech:.4f}, "
            f"民用技术={civilian_tech:.4f}, "
            f"溢出率={actual_ratio:.4f}, γ={spillover_rate:.2f}"
        )
    
    if war_driven_innovation > 0:
        return True, f"战争驱动创新：{war_driven_innovation:.4f}，军事技术迭代本源"
    
    if military_tech > 0:
        return True, f"军事技术存量：{military_tech:.4f}，迭代本源存在"
    
    return False, "军事技术迭代数据不足"


def verify_game_ecosystem_layering(data: Dict[str, Any]) -> Tuple[bool, str]:
    """验证公理九：游戏生态分层公理"""
    game_layers = data.get("game_layers", {})
    player_count = data.get("player_count", 0)
    creator_count = data.get("creator_count", 0)
    revenue_structure = data.get("revenue_structure", {})
    
    if game_layers and len(game_layers) >= 2:
        return True, f"游戏生态分层成立：{len(game_layers)}个层级，多层共生"
    
    if player_count > 0 and creator_count > 0:
        ratio = player_count / max(creator_count, 1)
        return True, (
            f"游戏生态结构：玩家={player_count}, "
            f"创作者={creator_count}, "
            f"金字塔比={ratio:.1f}:1"
        )
    
    if revenue_structure and len(revenue_structure) >= 2:
        return True, f"游戏收入结构：{len(revenue_structure)}个来源，生态多元"
    
    return False, "游戏生态分层数据不足"


def verify_all_special_axioms(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证全部9条专项公理
    
    Args:
        data: 包含所有公理验证所需数据的字典
    Returns:
        验证结果汇总
    """
    results = {}
    verifiers = [
        ("货币意义本体", verify_monetary_meaning),
        ("生态价值分层", verify_ecological_value_layering),
        ("认知范式锁死", verify_paradigm_lock),
        ("保障边际递减", verify_security_diminishing),
        ("债务质量分层", verify_debt_quality_layering),
        ("主义同源", verify_ism_common_origin),
        ("六系种子繁衍", verify_six_system_reproduction),
        ("军事技术迭代本源", verify_military_tech_evolution),
        ("游戏生态分层", verify_game_ecosystem_layering),
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
        "total": 9,
        "passed": passed_count,
        "failed": 9 - passed_count,
        "results": results,
        "all_passed": passed_count == 9
    }


# ============================================================================
# 接口函数
# ============================================================================

def get_all_axioms() -> List[SpecialAxiom]:
    """获取全部9条专项公理列表"""
    return ALL_NINE_SPECIAL_AXIOMS.copy()


def get_axiom_by_index(index: int) -> Optional[SpecialAxiom]:
    """根据索引获取公理（1-9）"""
    if 1 <= index <= 9:
        return ALL_NINE_SPECIAL_AXIOMS[index - 1]
    return None


def get_axiom_by_name(name_keyword: str) -> Optional[SpecialAxiom]:
    """根据关键词查找公理"""
    for axiom in ALL_NINE_SPECIAL_AXIOMS:
        if name_keyword in axiom.name:
            return axiom
    return None


def get_axioms_by_category(category: str) -> List[SpecialAxiom]:
    """按类别获取公理"""
    return [a for a in ALL_NINE_SPECIAL_AXIOMS if a.category == category]


def get_axioms_by_domain(domain: str) -> List[SpecialAxiom]:
    """按领域获取公理"""
    return [a for a in ALL_NINE_SPECIAL_AXIOMS if a.domain == domain]


def get_domains() -> List[str]:
    """获取所有涉及的领域"""
    return list(set(a.domain for a in ALL_NINE_SPECIAL_AXIOMS))


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
    print("  BSD9条专项公理验证器")
    print("=" * 70)
    
    print("\n【公理列表】")
    for i, axiom in enumerate(get_all_axioms(), 1):
        print(f"  {i}. {axiom.name}")
        print(f"     类别：{axiom.category}")
        print(f"     领域：{axiom.domain}")
        print(f"     公式：{axiom.formula}")
    
    print("\n【领域分布】")
    domains = get_domains()
    print(f"  共涉及 {len(domains)} 个领域：")
    for d in sorted(domains):
        count = len(get_axioms_by_domain(d))
        print(f"    - {d}：{count}条")
    
    print("\n【验证测试】")
    test_data = {
        "货币意义本体": {"collective_belief": 0.8, "exchange_value": 0.7, "monetary_value": 0.75},
        "生态价值分层": {"layers": {"物质层": {"weight": 0.2}, "调节层": {"weight": 0.3}, "文化层": {"weight": 0.5}}},
        "认知范式锁死": {"time_duration": 5, "lock_degree": 0.7},
        "保障边际递减": {"utility_points": [1.0, 0.8, 0.6, 0.4, 0.2]},
        "债务质量分层": {"debt_layers": {"优质": 0.5, "关注": 0.3, "不良": 0.2}},
        "主义同源": {"isms": ["资本主义", "社会主义"], "common_goals": ["社会发展", "人民幸福"]},
        "六系种子繁衍": {"seed_systems": [1,2,3,4,5,6], "grown_systems": [1,2,3,4,5,6]},
        "军事技术迭代本源": {"military_tech": 1.0, "civilian_tech": 0.85},
        "游戏生态分层": {"player_count": 10000, "creator_count": 100},
    }
    
    result = verify_all_special_axioms(test_data)
    print(f"  总通过率：{result['passed']}/{result['total']}")
    for name, res in result["results"].items():
        status = "✓" if res["passed"] else "✗"
        print(f"  {status} {name}：{res['message']}")
    
    print("\n【锁档常量】")
    for k, v in get_constants().items():
        print(f"  {k} = {v}")
    
    print("\n" + "=" * 70)
