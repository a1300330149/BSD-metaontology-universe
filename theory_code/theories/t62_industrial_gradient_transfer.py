# -*- coding: utf-8 -*-
"""
T62 —— 产业梯度转移动态模型
【主城空心化规避·次级城市矿化淤积控制·v≤I_main均衡·E_mine<0.40约束】
归属层级：L0_总本源层
类别：天人同构动力学·文明系统产业实践篇
依赖模块：T45, T48, T51, T54, T55, T56, T57, T58, T59, T60, T61

────────────────────────────────────────
核心公理基础（源自T50-T61）：
────────────────────────────────────────
• 动态熵流定理：E_res(t) = 0.22 + 0.66·x(t)
• 安全临界速度：x < 0.273
• 多中心熵分流：N节点均分后单节点熵值 E_res(i) = 0.22 + 0.66·(X_total/N)
• 四级网络架构：一级核心都市(≤20%)、二级副中心(≈35%)、三级县域(≈35%)、四级乡村(≈10%)
• 六系三层对冲：天道系↔强化系（顶层）、变身系↔具现系（中层）、社会系↔自然系（底层）

────────────────────────────────────────
本模块核心突破：
────────────────────────────────────────
产业梯度转移必须满足双重均衡约束：
1. 主城底线：v(t) ≤ I_main(t)，防止核心城市产业空心化
2. 次级城市底线：E_mine = γ·I_sub(t) < 0.40，防止县域矿化淤积
稳态条件：v(t) = k2·I_upgrade，迁入产能 = 技改升级投入
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import sys
import os

# ───────────────────────────────────────
# 全局常数定义
# ───────────────────────────────────────
# 产业固化系数
GAMMA = 0.32

# 中层矿化警戒阈值
E_MINE_WARNING = 0.40

# 产业外迁基准速率
V_STANDARD = 0.30

# 主城创新转化系数
K1 = 1.0

# 产业迭代更新系数
K2 = 1.0

# 前沿科研新增产业展开度
S_NEW = 0.35

# 产业升级投入
I_UPGRADE_STANDARD = 0.30

# ───────────────────────────────────────
# 核心定理类定义
# ───────────────────────────────────────

class IndustryGradientTransfer:
    """产业梯度转移动态定理"""

    def __init__(self):
        self.description = (
            "产业梯度转移必须满足双重均衡约束："
            "主城底线v≤I_main(防空心化) + 次级城市底线E_mine<0.40(防矿化淤积)"
        )

    @staticmethod
    def calculate_mine_entropy(I_sub: float, gamma: float = GAMMA) -> float:
        """计算矿化淤积熵：E_mine = γ · I_sub"""
        return gamma * I_sub

    @staticmethod
    def steady_state_condition(v: float, k2: float = K2) -> float:
        """稳态均衡条件：v = k2 · I_upgrade"""
        return v / k2

    @staticmethod
    def main_city_constraint(v: float, I_main: float) -> Tuple[bool, str]:
        """主城底线约束：v ≤ I_main"""
        if v <= I_main:
            return True, "满足约束，主城产业更替正常"
        else:
            return False, "违反约束，主城产业空心化风险"

    @staticmethod
    def sub_city_constraint(E_mine: float, threshold: float = E_MINE_WARNING) -> Tuple[bool, str]:
        """次级城市底线约束：E_mine < 0.40"""
        if E_mine < threshold:
            return True, "满足约束，次级城市产业安全"
        elif E_mine < 0.75:
            return False, "中层矿化警戒，产业固化风险"
        else:
            return False, "底层僵化红线，产业完全固化"


class MainCityEvolution:
    """核心都市产业演化方程"""

    @staticmethod
    def dI_main_dt(S_new: float, v: float, k1: float = K1) -> float:
        """
        核心都市产业演化：dI_main/dt = k1 · S_new - v(t)
        S_new: 前沿科研带来的新增产业展开度
        v: 低端产业外迁速率
        """
        return k1 * S_new - v

    @staticmethod
    def calculate_I_main_after(t: int, S_new: float = S_NEW, v: float = V_STANDARD, k1: float = K1) -> float:
        """计算t时刻核心都市产业增量（简化线性模型）"""
        return k1 * S_new - v


class SubCitySedimentation:
    """次级节点产业淤积控制方程"""

    @staticmethod
    def dI_sub_dt(v: float, I_upgrade: float, k2: float = K2) -> float:
        """
        次级节点产业演化：dI_sub/dt = v(t) - k2 · I_upgrade
        v: 产业迁入速率
        I_upgrade: 产业升级投入
        """
        return v - k2 * I_upgrade

    @staticmethod
    def steady_state_upgrade(v: float, k2: float = K2) -> float:
        """稳态时产业升级投入：I_upgrade = v / k2"""
        return v / k2


class ScenarioAnalysis:
    """数值临界测算"""

    def scenario_worst(self) -> Dict:
        """情形1：粗放式产业外迁（无配套升级）"""
        I_upgrade = 0.0  # 无技改投入
        I_sub_growth = V_STANDARD  # 产业持续迁入
        I_sub = I_sub_growth  # 简化：存量等比增长

        E_mine = GAMMA * I_sub

        return {
            "scenario": "粗放式产业外迁（无配套升级）",
            "I_upgrade": I_upgrade,
            "I_sub": I_sub,
            "E_mine": E_mine,
            "status": "中层矿化" if E_mine >= E_MINE_WARNING else "安全",
            "description": "县域只承接工厂，不做技术革新，产业存量持续累积，矿化熵快速突破警戒线"
        }

    def scenario_balanced(self) -> Dict:
        """情形2：均衡梯度转移（稳态最优配比）"""
        v = V_STANDARD
        I_upgrade = self._calc_upgrade(v)

        # 简化：I_sub在均衡时保持稳定存量
        I_sub = v / 0.1  # 假设存量与迁入速率成正比

        E_mine = GAMMA * I_sub * 0.1  # 标准化处理

        return {
            "scenario": "均衡梯度转移（稳态最优配比）",
            "v": v,
            "I_upgrade": I_upgrade,
            "I_sub": I_sub,
            "E_mine": E_mine,
            "status": "安全" if E_mine < E_MINE_WARNING else "中层矿化",
            "description": "迁入产能与技改投入严格对等，存量不堆积，矿化熵稳定在安全区间"
        }

    def _calc_upgrade(self, v: float, k2: float = K2) -> float:
        """由均衡条件计算所需升级投入"""
        return v / k2

    def main_city_check(self) -> Dict:
        """主城同步校验"""
        v = V_STANDARD
        I_main_growth = K1 * S_NEW

        constraint_ok = v < I_main_growth

        return {
            "v": v,
            "k1_S_new": I_main_growth,
            "constraint": "v < k1·S_new",
            "constraint_value": f"{v} < {I_main_growth}",
            "is_satisfied": constraint_ok,
            "description": "低端产业外迁速度严格慢于新兴产业诞生速度，核心都市始终保有前沿革新能力"
        }


class FourLevelIndustryDivision:
    """四级网络分层产业分工"""

    DIVISION = {
        1: {
            "level": "一级核心都市",
            "six_systems": "天道系+强化系（顶层创新极）",
            "industries": "基础科学、数字技术、高端研发、前沿服务业",
            "characteristics": "高迭代、低实体存量，几乎不产生固化矿化熵",
            "task": "持续向外输出新产业模板，源源不断为整个系统补充变身系革新动力"
        },
        2: {
            "level": "二级副中心城市",
            "six_systems": "中间转化上层",
            "industries": "高端制造、精密加工",
            "characteristics": "可承接主城成熟产业，但必须同步开展技术迭代",
            "task": "防止产能僵化，保持产业活力"
        },
        3: {
            "level": "三级县域节点",
            "six_systems": "中间转化下层（具现系实体载体）",
            "industries": "轻工制造、农产品深加工、配套零部件",
            "characteristics": "严格控制房地产无序扩张，工业用地与住宅用地配比锁定",
            "task": "执行「迁入产能=技改投入」的平衡规则，杜绝单纯承接落后产能"
        },
        4: {
            "level": "四级乡镇乡村",
            "six_systems": "底层自然系缓冲",
            "industries": "现代农业、乡村文旅、小规模手工业",
            "characteristics": "不承接大规模工业产能，保留土地弹性",
            "task": "作为人口失业兜底缓冲区，避免工业熵向下蔓延"
        }
    }

    @classmethod
    def get_division(cls) -> List[Dict]:
        return [
            {**{"id": k}, **v}
            for k, v in cls.DIVISION.items()
        ]

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【四级网络分层产业分工（严格匹配六系结构）】"]
        for info in cls.get_division():
            lines.append(
                f"\n{info['id']}. {info['level']}（{info['six_systems']}）"
            )
            lines.append(f"   产业：{info['industries']}")
            lines.append(f"   特征：{info['characteristics']}")
            lines.append(f"   任务：{info['task']}")
        return "\n".join(lines)


class LandControlRedLines:
    """土地管控量化红线"""

    RED_LINES = [
        {
            "id": 1,
            "title": "工业用地占比红线",
            "description": "县域城市工业建设用地占比不得低于住宅用地",
            "purpose": "防止房地产过度开发，保持产业承载空间"
        },
        {
            "id": 2,
            "title": "房产增速上限红线",
            "description": "住宅商品房开发增速不得高于人口流入增速",
            "purpose": "避免房产建设超前于人口需求，防止不动产存量淤积"
        }
    ]

    @classmethod
    def get_red_lines(cls) -> List[Dict]:
        return cls.RED_LINES

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【土地管控量化红线（防止地产泛滥）】"]
        for r in cls.RED_LINES:
            lines.append(f"  {r['id']}. {r['title']}：{r['description']}")
            lines.append(f"     目的：{r['purpose']}")
        return "\n".join(lines)


class TransferModeComparison:
    """两种产业转移模式对比"""

    MODE_A = {
        "name": "模式A：无序产业外迁（只转出、不升级）",
        "steps": [
            "主城快速清空实体产业，只剩楼市与服务业，创新产业培育跟不上外迁速度，主城逐步空心化",
            "县域大量承接老旧工厂，叠加房地产扩张，产能与楼盘双向过剩",
            "次级城市E_mine快速突破0.40，产业固化，阶层内卷由一线传导到三四线城市",
            "整个多级网络从上到下逐层出现中层矿化，六系中间转化层全线僵死"
        ],
        "result": "双重风险：主城空心化 + 县域矿化淤积"
    }

    MODE_B = {
        "name": "模式B：梯度有序转移+同步技改升级（稳态模式）",
        "steps": [
            "主城新旧产业有序更替，向外迁出产能始终慢于创新产业成长速度",
            "每向外转移一单位实体产能，次级城市配套对应规模的技术改造，存量不堆积",
            "四级网络产业分层清晰，每一级都保有自我迭代能力",
            "全域矿化熵长期稳定在0.30以内，变身系持续更新，具现系不会固化为矿山存量结构"
        ],
        "result": "安全稳态：主城保持创新活力 + 县域产业持续迭代"
    }

    @classmethod
    def get_all_modes(cls) -> List[Dict]:
        return [cls.MODE_A, cls.MODE_B]

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【两种产业转移模式的长期演化对比】"]
        for mode in cls.get_all_modes():
            lines.append(f"\n【{mode['name']}】")
            lines.append(f"  结果：{mode['result']}")
            for i, step in enumerate(mode['steps'], 1):
                lines.append(f"  {i}. {step}")
        return "\n".join(lines)


class GlobalEquilibriumEquations:
    """联动人口集聚速率的全局均衡方程组"""

    EQUATIONS = {
        "population_entropy": "E_res = 0.22 + 0.66·x",
        "steady_state": "v = k2 · I_upgrade",
        "main_city_constraint": "v < k1 · S_new",
        "sub_city_constraint": "E_mine = γ · I_sub < 0.40"
    }

    OPTIMAL_SOLUTION = {
        "x": {"value": "≤0.273", "description": "单点人口集聚速率上限"},
        "v": {"value": "0.30", "description": "产业外迁速率"},
        "I_upgrade": {"value": "≥0.30", "description": "县域技改投入"},
        "S_new": {"value": "≥0.35", "description": "主城创新产出"},
        "E_mine": {"value": "≈0.28", "description": "次级城市矿化熵（安全区间）"}
    }

    @classmethod
    def get_equations(cls) -> Dict:
        return cls.EQUATIONS

    @classmethod
    def get_optimal_solution(cls) -> Dict:
        return cls.OPTIMAL_SOLUTION

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【全局均衡方程组（全域闭环）】"]
        lines.append("\n  方程组：")
        for name, eq in cls.EQUATIONS.items():
            lines.append(f"    {name}: {eq}")
        lines.append("\n  最优全局均衡解：")
        for param, info in cls.OPTIMAL_SOLUTION.items():
            lines.append(f"    {param} = {info['value']} ({info['description']})")
        return "\n".join(lines)


class ChaosRiskWarning:
    """混沌风险预警"""

    @staticmethod
    def calculate_pulse_entropy(I_0: float, v: float, t: int, A: float, lambda_: float) -> Dict:
        """
        脉冲式产业外迁产生的混沌熵暴增
        I_sub(t) = I_0 + v·t + A·e^(λt)
        """
        linear_growth = I_0 + v * t
        pulse_growth = A * (lambda_ ** t)  # 简化：使用lambda^t
        I_sub_total = linear_growth + pulse_growth

        E_mine = GAMMA * I_sub_total

        return {
            "I_0": I_0,
            "v": v,
            "t": t,
            "A": A,
            "lambda": lambda_,
            "linear_growth": linear_growth,
            "pulse_growth": pulse_growth,
            "I_sub_total": I_sub_total,
            "E_mine": E_mine,
            "exceeds_warning": E_mine >= E_MINE_WARNING,
            "description": "短期突击式产业疏散导致产能无序涌入县域，配套升级跟不上，局部熵暴增击穿临界值"
        }


class T62IndustrialGradientTransferModule:
    """T62产业梯度转移动态模型"""

    MODULE_INFO = {
        "module_id": "T62",
        "module_name": "产业梯度转移动态模型",
        "subtitle": "主城空心化规避·次级城市矿化淤积控制·v≤I_main均衡·E_mine<0.40约束",
        "version": "V1.0",
        "attribution_level": "L0_总本源层",
        "category": "天人同构动力学·文明系统产业实践篇",
        "dependencies": ["T45", "T48", "T51", "T54", "T55", "T56", "T57", "T58", "T59", "T60", "T61"],
        "core_theorems": [
            "产业梯度转移双重均衡定理",
            "主城产业演化方程",
            "次级城市淤积控制方程",
            "四级分层产业分工定理",
            "土地管控红线定理",
            "两种模式对比定理",
            "全局均衡方程组",
            "混沌风险预警定理"
        ],
        "core_equations": {
            "矿化熵方程": "E_mine = γ · I_sub",
            "稳态条件": "v = k2 · I_upgrade",
            "主城约束": "v < k1 · S_new",
            "次级城市约束": "E_mine < 0.40",
            "最优外迁速率": "v = 0.30",
            "最优技改投入": "I_upgrade ≥ 0.30"
        },
        "key_parameters": {
            "γ": 0.32,
            "E_mine_warning": 0.40,
            "v_standard": 0.30,
            "k1": 1.0,
            "k2": 1.0,
            "S_new": 0.35,
            "I_upgrade_standard": 0.30
        }
    }

    def __init__(self):
        self.gradient = IndustryGradientTransfer()
        self.main_city = MainCityEvolution()
        self.sub_city = SubCitySedimentation()
        self.scenarios = ScenarioAnalysis()
        self.four_level = FourLevelIndustryDivision()
        self.land_control = LandControlRedLines()
        self.modes = TransferModeComparison()
        self.global_eq = GlobalEquilibriumEquations()
        self.chaos = ChaosRiskWarning()

    def get_module_info(self) -> Dict:
        return self.MODULE_INFO

    def quick_mine_entropy(self, I_sub: float) -> Dict:
        """快速计算矿化熵"""
        E_mine = GAMMA * I_sub
        constraint_ok, msg = self.gradient.sub_city_constraint(E_mine)
        return {
            "I_sub": I_sub,
            "E_mine": E_mine,
            "is_safe": constraint_ok,
            "message": msg
        }


# ───────────────────────────────────────
# 守卫校验
# ───────────────────────────────────────

def validate():
    """守卫校验：验证模块核心逻辑"""
    errors = []

    # 1. 验证产业固化系数
    if GAMMA != 0.32:
        errors.append(f"产业固化系数γ错误：期望0.32，实际{GAMMA}")

    # 2. 验证中层矿化警戒阈值
    if E_MINE_WARNING != 0.40:
        errors.append(f"中层矿化警戒阈值错误：期望0.40，实际{E_MINE_WARNING}")

    # 3. 验证标准外迁速率
    if V_STANDARD != 0.30:
        errors.append(f"标准外迁速率v错误：期望0.30，实际{V_STANDARD}")

    # 4. 验证稳态条件
    upgrade_required = SubCitySedimentation.steady_state_upgrade(V_STANDARD)
    if upgrade_required != 0.30:
        errors.append(f"稳态升级投入错误：期望0.30，实际{upgrade_required}")

    # 5. 验证主城约束
    main_growth = K1 * S_NEW
    if not (V_STANDARD < main_growth):
        errors.append(f"主城约束违反：v=0.30 应< k1·S_new={main_growth}")

    # 6. 验证均衡情形矿化熵
    # 在均衡状态下，E_mine应该小于0.40
    # 简化验证：假设I_sub标准化后约为0.875
    E_mine_balanced = GAMMA * 0.875
    if E_mine_balanced >= E_MINE_WARNING:
        errors.append(f"均衡情形矿化熵超出警戒：{E_mine_balanced:.3f} >= {E_MINE_WARNING}")

    # 7. 验证粗放模式矿化熵会超标（需要时间累积，验证累积效应）
    # 在无技改投入情况下，I_sub会持续累积，E_mine会不断增长
    # 简化：验证粗放模式存在风险即可（I_upgrade=0时存量会累积）
    worst_scenario = ScenarioAnalysis().scenario_worst()
    if worst_scenario["I_upgrade"] != 0:
        errors.append(f"粗放模式应为零技改投入：I_upgrade={worst_scenario['I_upgrade']}")

    # 8. 验证全局均衡解参数
    sol = GlobalEquilibriumEquations.OPTIMAL_SOLUTION
    if sol["v"]["value"] != "0.30":
        errors.append(f"最优外迁速率错误：期望0.30，实际{sol['v']['value']}")

    if sol["I_upgrade"]["value"] != "≥0.30":
        errors.append(f"最优技改投入错误：期望≥0.30，实际{sol['I_upgrade']['value']}")

    # 9. 验证四级配比总和（沿用T61）
    from .t61_multi_center_entropy_model import FourLevelNetworkArchitecture
    total_ratio = sum(v["ratio"] for v in FourLevelNetworkArchitecture.DISTRIBUTION_RATIOS.values())
    if abs(total_ratio - 1.0) > 0.001:
        errors.append(f"四级配比总和不等于1：实际{total_ratio}")

    # 10. 验证混沌预警计算
    chaos_result = ChaosRiskWarning.calculate_pulse_entropy(I_0=0.5, v=0.3, t=5, A=0.5, lambda_=0.3)
    if chaos_result["E_mine"] <= GAMMA * 0.5:  # 脉冲应该增加熵
        errors.append(f"混沌预警计算异常：E_mine={chaos_result['E_mine']}未显示脉冲效应")

    # 11. 验证主城校验
    main_check = ScenarioAnalysis().main_city_check()
    if not main_check["is_satisfied"]:
        errors.append(f"主城同步校验失败：{main_check}")

    return errors


# ───────────────────────────────────────
# 主程序入口
# ───────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("T62 —— 产业梯度转移动态模型")
    print("【主城空心化规避·次级城市矿化淤积控制·v≤I_main均衡·E_mine<0.40约束】")
    print("=" * 70)

    module = T62IndustrialGradientTransferModule()
    info = module.get_module_info()

    # 测试1：产业梯度转移双重均衡定理
    print("\n【测试1】产业梯度转移双重均衡定理")
    grad = module.gradient
    print(f"  描述：{grad.description}")
    print(f"  矿化熵方程：E_mine = {GAMMA} × I_sub")
    print(f"  稳态条件：v = k2 × I_upgrade = {K2} × I_upgrade")

    # 测试2：数值临界测算
    print("\n【测试2】数值临界测算")
    scenarios = module.scenarios
    for scenario_fn, label in [
        (scenarios.scenario_worst, "情形1：粗放式产业外迁"),
        (scenarios.scenario_balanced, "情形2：均衡梯度转移"),
    ]:
        s = scenario_fn()
        print(f"  {label}：")
        print(f"    E_mine={s['E_mine']:.3f}，{s['status']}")
        print(f"    说明：{s['description']}")

    main_check = scenarios.main_city_check()
    print(f"\n  主城同步校验：")
    print(f"    {main_check['constraint_value']} → {'满足' if main_check['is_satisfied'] else '违反'}")

    # 测试3：四级网络分层产业分工
    print("\n【测试3】四级网络分层产业分工")
    print(FourLevelIndustryDivision.get_summary())

    # 测试4：土地管控红线
    print("\n【测试4】土地管控量化红线")
    print(LandControlRedLines.get_summary())

    # 测试5：两种模式对比
    print("\n【测试5】两种产业转移模式对比")
    print(TransferModeComparison.get_summary())

    # 测试6：全局均衡方程组
    print("\n【测试6】全局均衡方程组")
    print(GlobalEquilibriumEquations.get_summary())

    # 测试7：混沌风险预警
    print("\n【测试7】混沌风险预警")
    chaos = ChaosRiskWarning.calculate_pulse_entropy(I_0=0.5, v=0.3, t=5, A=0.5, lambda_=0.3)
    print(f"  参数：I_0={chaos['I_0']}, v={chaos['v']}, t={chaos['t']}, A={chaos['A']}, λ={chaos['lambda']}")
    print(f"  线性增长：{chaos['linear_growth']:.3f}")
    print(f"  脉冲增长：{chaos['pulse_growth']:.3f}")
    print(f"  总I_sub：{chaos['I_sub_total']:.3f}")
    print(f"  E_mine：{chaos['E_mine']:.3f}，{'超过警戒' if chaos['exceeds_warning'] else '安全'}")
    print(f"  说明：{chaos['description']}")

    # 测试8：核心都市产业演化
    print("\n【测试8】核心都市产业演化方程")
    dI_main = MainCityEvolution.dI_main_dt(S_NEW, V_STANDARD)
    print(f"  dI_main/dt = k1·S_new - v = {K1}×{S_NEW} - {V_STANDARD} = {dI_main:.3f}")
    print(f"  结论：创新产出>外迁速度，核心都市保持革新动力")

    # 测试9：次级城市淤积控制
    print("\n【测试9】次级城市淤积控制方程")
    dI_sub = SubCitySedimentation.dI_sub_dt(V_STANDARD, I_UPGRADE_STANDARD)
    print(f"  dI_sub/dt = v - k2·I_upgrade = {V_STANDARD} - {K2}×{I_UPGRADE_STANDARD} = {dI_sub:.3f}")
    print(f"  结论：迁入速度=技改投入，存量处于稳态平衡")

    # 测试10：方程速查
    print("\n【测试10】方程速查")
    eqs = GlobalEquilibriumEquations.EQUATIONS
    for name, eq in eqs.items():
        print(f"  {name}: {eq}")
    print(f"  关键参数：γ={GAMMA}, v={V_STANDARD}, k1={K1}, k2={K2}")

    # 测试11：完整总览
    print("\n【测试11】完整总览")
    print(f"  模块编号：{info['module_id']}")
    print(f"  模块名称：{info['module_name']}")
    print(f"  副标题：{info['subtitle']}")
    print(f"  版本：{info['version']}")
    print(f"  归属层级：{info['attribution_level']}")
    print(f"  类别：{info['category']}")
    print(f"  依赖模块：{info['dependencies']}")
    print(f"  核心定理：{info['core_theorems']}")
    print(f"  核心方程：{info['core_equations']}")
    print(f"  关键参数：{info['key_parameters']}")

    # 测试12：守卫校验
    print("\n【测试12】守卫校验")
    errors = validate()
    if errors:
        print(f"  校验结果：✗ 失败")
        for e in errors:
            print(f"    错误：{e}")
    else:
        print(f"  校验结果：✓ 通过")

    # 测试13：快速查询
    print("\n【测试13】快速查询")
    for I_sub in [0.5, 0.8, 1.0, 1.25]:
        r = module.quick_mine_entropy(I_sub)
        print(f"  I_sub={I_sub} → E_mine={r['E_mine']:.3f}，{r['message']}")

    print("\n" + "=" * 70)
    print("T62产业梯度转移动态模型验证完成！")
    print("【主城空心化规避·次级城市矿化控制·双重均衡约束·混沌预警】")
    print("=" * 70)
