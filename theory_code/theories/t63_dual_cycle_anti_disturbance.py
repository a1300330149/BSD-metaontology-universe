# -*- coding: utf-8 -*-
"""
T63 —— 内外双循环抗扰动模型
【外贸周期冲击·E_shock正弦扰动·两级缓冲吸纳·全域闭环方程组】
归属层级：L0_总本源层
类别：天人同构动力学·文明系统抗扰实践篇
依赖模块：T45, T48, T51, T54, T55, T56, T57, T58, T59, T60, T61, T62

────────────────────────────────────────
核心公理基础（源自T50-T62）：
────────────────────────────────────────
• 三级熵分流：E_res = ΔE_city - E_out(foreign) - E_out(county) - E_out(rural) = 0.35
• 动态熵流：E_res(t) = 0.22 + 0.66·x(t)，安全临界x<0.273
• 多中心熵分流：N节点均分后单节点熵值更低
• 产业梯度转移：v = k2·I_upgrade，v < k1·S_new，E_mine = γ·I_sub < 0.40
• 四级网络架构：一级核心都市、二级副中心、三级县域、四级乡村
• 六系三层对冲：天道系↔强化系（顶层）、变身系↔具现系（中层）、社会系↔自然系（底层）

────────────────────────────────────────
本模块核心突破：
────────────────────────────────────────
纳入外循环外贸波动带来的外部熵冲击E_shock(t) = A·sin(ωt)，
建立稳态抗扰动条件：E_shock(max) < E_out(county) + E_out(rural)
通过四级产业梯次网络实现产能平滑切换，完全平熨外部周期扰动。
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import math
import sys
import os

# ───────────────────────────────────────
# 全局常数定义（沿用T58-T62）
# ───────────────────────────────────────
# 基准稳态参数（无外部冲击时）
DELTA_E_CITY_BASE = 0.72      # 城市内生熵增量
E_OUT_FOREIGN_BASE = 0.17     # 外循环外贸排熵
E_OUT_COUNTY_BASE = 0.13      # 县域分流
E_OUT_RURAL_BASE = 0.07       # 乡村分流

# 基准残余熵
E_RES_BASE = DELTA_E_CITY_BASE - E_OUT_FOREIGN_BASE - E_OUT_COUNTY_BASE - E_OUT_RURAL_BASE

# 安全线
E_RES_SAFE = 0.40

# 动态函数参数
C_CONSTANT = 0.22
ALPHA_CK = 0.66
X_SAFE_MAX = 0.273

# 产业梯度转移参数
GAMMA_MINE = 0.32
V_STANDARD = 0.30
K1 = 1.0
K2 = 1.0
S_NEW = 0.35
E_MINE_WARNING = 0.40


# ───────────────────────────────────────
# 核心定理类定义
# ───────────────────────────────────────

class ExternalShockEntropy:
    """外部冲击熵（外循环外贸波动）"""

    def __init__(self):
        self.description = (
            "外贸具备强周期性：繁荣期排熵能力大幅提升；"
            "外需收缩期，出口泄压通道骤然收窄，大量过剩产能回流国内，形成外部冲击熵"
        )

    @staticmethod
    def calculate_shock_sin(t: float, A: float, omega: float) -> float:
        """
        外循环波动项（周期性扰动）：E_shock(t) = A·sin(ωt)
        A: 外部冲击振幅
        omega: 外贸周期频率
        t: 时间
        """
        return A * math.sin(omega * t)

    @staticmethod
    def total_residual_entropy(delta_E_city: float, e_out_foreign: float,
                                e_out_county: float, e_out_rural: float,
                                e_shock: float) -> float:
        """整体总残余熵：E_res = ΔE_city - E_out(foreign) - E_out(county) - E_out(rural) + E_shock"""
        return delta_E_city - e_out_foreign - e_out_county - e_out_rural + e_shock

    @staticmethod
    def steady_anti_disturbance_condition(e_shock_max: float,
                                           e_out_county: float,
                                           e_out_rural: float) -> Tuple[bool, str]:
        """
        稳态抗扰动条件：E_shock(max) < E_out(county) + E_out(rural)
        外部冲击产生的熵增量，必须小于县域+乡村两级缓冲的吸纳容量
        """
        buffer_total = e_out_county + e_out_rural
        if e_shock_max < buffer_total:
            return True, (f"满足抗扰动条件：最大冲击{e_shock_max:.3f} < "
                         f"两级缓冲总容量{buffer_total:.3f}")
        else:
            return False, (f"违反抗扰动条件：最大冲击{e_shock_max:.3f} >= "
                          f"两级缓冲总容量{buffer_total:.3f}")


class CapacityReallocation:
    """产能跨区域再配置"""

    @staticmethod
    def dQ_trade_dt(trade_decline_rate: float) -> float:
        """出口产业变化率（外需收缩时为负）"""
        return -abs(trade_decline_rate)

    @staticmethod
    def dQ_domestic_dt(domestic_growth_rate: float) -> float:
        """内需产业变化率（外需收缩时为正）"""
        return abs(domestic_growth_rate)

    @staticmethod
    def internal_shunt(e_shock: float, delta_county: float, delta_rural: float) -> Dict:
        """
        内部产能梯次向内分流机制
        e_shock: 外部冲击熵
        delta_county: 县域额外承接熵增量
        delta_rural: 乡村额外承接熵增量
        """
        remaining = e_shock - delta_county - delta_rural
        is_absorbed = remaining <= 0

        return {
            "e_shock": e_shock,
            "delta_county": delta_county,
            "delta_rural": delta_rural,
            "total_shunt": delta_county + delta_rural,
            "remaining": max(0, remaining),
            "is_fully_absorbed": is_absorbed,
            "E_res_after": E_RES_BASE + remaining if remaining > 0 else E_RES_BASE
        }


class ScenarioSimulation:
    """数值量化测算"""

    def scenario_base(self) -> Dict:
        """基准稳态（无外部冲击）"""
        E_res = E_RES_BASE
        return {
            "scenario": "基准稳态（无外部冲击）",
            "ΔE_city": DELTA_E_CITY_BASE,
            "E_out_foreign": E_OUT_FOREIGN_BASE,
            "E_out_county": E_OUT_COUNTY_BASE,
            "E_out_rural": E_OUT_RURAL_BASE,
            "E_shock": 0.0,
            "E_res": E_res,
            "status": "安全稳态" if E_res < E_RES_SAFE else "中层矿化警戒",
            "description": "稳定处于0.40安全线以内"
        }

    def scenario_1_no_shunt(self, e_shock: float = 0.12) -> Dict:
        """情景1：外贸下行，无内部产能转移机制"""
        E_res = E_RES_BASE + e_shock
        return {
            "scenario": "情景1：外贸下行，无内部分流机制",
            "E_shock": e_shock,
            "E_res": E_res,
            "status": "安全稳态" if E_res < E_RES_SAFE else "中层矿化警戒",
            "description": "冲击熵全部堆积在城市，直接突破中层矿化警戒线"
        }

    def scenario_2_with_shunt(self, e_shock: float = 0.12,
                               delta_county: float = 0.07,
                               delta_rural: float = 0.05) -> Dict:
        """情景2：开启产业梯次向内分流机制"""
        remaining = e_shock - delta_county - delta_rural
        E_res = E_RES_BASE + max(0, remaining)

        return {
            "scenario": "情景2：开启产业梯次向内分流机制",
            "E_shock": e_shock,
            "ΔE_county": delta_county,
            "ΔE_rural": delta_rural,
            "total_shunt": delta_county + delta_rural,
            "remaining": max(0, remaining),
            "E_res": E_res,
            "status": "安全稳态" if E_res < E_RES_SAFE else "中层矿化警戒",
            "description": "熵值重回原有稳态水平，外部冲击被完全消化"
        }

    def critical_buffer_line(self) -> Dict:
        """临界容量红线"""
        buffer_total = E_OUT_COUNTY_BASE + E_OUT_RURAL_BASE
        return {
            "E_out_county": E_OUT_COUNTY_BASE,
            "E_out_rural": E_OUT_RURAL_BASE,
            "total_buffer": buffer_total,
            "max_tolerable_shock": buffer_total,
            "verdict": (f"两级缓冲总和为{buffer_total}，"
                       f"可以抵御峰值不超过{buffer_total}的外贸回流冲击，"
                       f"足以平熨常规全球经济周期波动")
        }


class SixSystemsAntiDisturbance:
    """六系三层抗扰动结构"""

    LAYERS = {
        "top_pole": {
            "systems": "天道系 ↔ 强化系（顶层两极）",
            "mechanism": "顶层宏观政策保持发展路径稳定，不随外贸周期频繁大幅度摇摆",
            "function": "核心都市前沿创新产业持续产出新赛道，开辟内需新市场，用新增意义消化回流产能"
        },
        "middle_transform": {
            "systems": "变身系 ↔ 具现系（中间转化层，产能切换核心）",
            "mechanism": "副中心城市出口制造业保留柔性产能，可快速在外销与内需之间切换",
            "function": "低端加工产能有序下沉到县域工业区，同步配套技术改造，防止回流产能形成存量矿化淤积"
        },
        "bottom_bearing": {
            "systems": "社会系 ↔ 自然系（底层承载层）",
            "mechanism": "乡镇与县域保留农业、小微产业的就业蓄水池",
            "function": "外贸下行带来失业波动时，返乡就业、县域小微产业吸纳冗余劳动力"
        }
    }

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【六系三层抗扰动结构】"]
        for key, info in cls.LAYERS.items():
            lines.append(f"\n  {info['systems']}")
            lines.append(f"    机制：{info['mechanism']}")
            lines.append(f"    功能：{info['function']}")
        return "\n".join(lines)


class ResponseSchemeComparison:
    """两类应对方案的长期对比"""

    SCHEME_A = {
        "name": "方案一：单纯依靠外循环，内部缓冲网络残缺",
        "steps": [
            "外贸繁荣期，熵向外排泄，经济高速增长",
            "外需收缩期，产能大规模回流，内部缺少承接载体",
            "冲击熵直接堆积在核心城市，E_res短时间跃升至0.6以上",
            "产业过剩、债务累积、就业矛盾集中爆发，六系中间层快速矿化",
            "周期性波动不断放大，每一轮外贸下行都会加剧内部淤积"
        ],
        "result": "周期性震荡加剧，长期逼近0.75底层停滞红线"
    }

    SCHEME_B = {
        "name": "方案二：内外双循环联动+四级产业梯次分流",
        "steps": [
            "外循环负责常态下向外排泄熵",
            "县域、乡村两级内部缓冲网络专门承接外贸下行带来的回流冲击",
            "产能在四级节点之间平滑流转，不会在单一城市形成脉冲式淤积",
            "即便海外市场出现大幅收缩，内部多级泄压通道依然可以稳住整体熵水平",
            "全域长期维持E_res<0.40，产业持续迭代，跳出外部周期带来的反复震荡"
        ],
        "result": "长期稳态，抵御外部周期波动，产业持续迭代"
    }

    @classmethod
    def get_all_schemes(cls) -> List[Dict]:
        return [cls.SCHEME_A, cls.SCHEME_B]

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【两类应对方案的长期对比】"]
        for scheme in cls.get_all_schemes():
            lines.append(f"\n【{scheme['name']}】")
            lines.append(f"  结果：{scheme['result']}")
            for i, step in enumerate(scheme['steps'], 1):
                lines.append(f"  {i}. {step}")
        return "\n".join(lines)


class PolicyConstraintChaos:
    """防范政策波动带来的混沌扰动"""

    @staticmethod
    def chaos_shock(A: float, lambda_: float, t: int) -> Dict:
        """
        指数级混沌项：E_shock = A·e^(λt)
        短期突击式产业内迁形成的混沌熵暴增
        """
        # 使用lambda的指数近似
        pulse = A * (lambda_ ** t)  # 简化
        E_shock = pulse
        return {
            "A": A,
            "lambda": lambda_,
            "t": t,
            "E_shock_chaos": E_shock,
            "exceeds_buffer": E_shock > (E_OUT_COUNTY_BASE + E_OUT_RURAL_BASE),
            "description": "短期突击式产业内迁，县域产能瞬间饱和，地产跟风扩张，触发地方产业矿化灾害"
        }

    @staticmethod
    def constraint_rule() -> Dict:
        """约束规则"""
        buffer_total = E_OUT_COUNTY_BASE + E_OUT_RURAL_BASE
        annual_limit = buffer_total * 0.5
        return {
            "rule": "年度产业内迁规模严格控制在缓冲承载容量的一半以内",
            "buffer_total": buffer_total,
            "annual_limit": annual_limit,
            "principle": "产能跨区域再配置必须平滑渐进，预留冗余空间，杜绝一次性脉冲式调整"
        }


class GlobalClosedLoopEquations:
    """全局完整联立方程组（最终闭环模型）"""

    EQUATIONS = {
        "总残余熵": "E_res = ΔE_city - E_out(foreign) - E_out(county) - E_out(rural) + E_shock(t)",
        "外部冲击": "E_shock(t) = A·sin(ωt)",
        "抗扰动条件": "E_shock(max) < E_out(county) + E_out(rural)",
        "产业稳态": "v = k2·I_upgrade",
        "主城约束": "v < k1·S_new",
        "矿化约束": "E_mine = γ·I_sub < 0.40",
        "人口约束": "E_res = 0.22 + 0.66·x < 0.40"
    }

    CONSTRAINTS = [
        "人口单向集聚速度",
        "产业梯度外迁速率，避免主城空心化与县域矿化",
        "内外循环波动带来的外部熵冲击",
        "多级缓冲网络的最低承载容量",
        "全域残余熵始终稳定在安全稳态区间"
    ]

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【全局完整联立方程组（最终闭环模型）】"]
        lines.append("\n  方程组：")
        for name, eq in cls.EQUATIONS.items():
            lines.append(f"    {name}: {eq}")
        lines.append("\n  整套方程组同时约束：")
        for i, c in enumerate(cls.CONSTRAINTS, 1):
            lines.append(f"    {i}. {c}")
        return "\n".join(lines)


class T63DualCycleAntiDisturbanceModule:
    """T63内外双循环抗扰动模型"""

    MODULE_INFO = {
        "module_id": "T63",
        "module_name": "内外双循环抗扰动模型",
        "subtitle": "外贸周期冲击·E_shock正弦扰动·两级缓冲吸纳·全域闭环方程组",
        "version": "V1.0",
        "attribution_level": "L0_总本源层",
        "category": "天人同构动力学·文明系统抗扰实践篇",
        "dependencies": ["T45", "T48", "T51", "T54", "T55", "T56", "T57", "T58", "T59", "T60", "T61", "T62"],
        "core_theorems": [
            "外部冲击熵定理",
            "产能跨区域再配置定理",
            "稳态抗扰动条件定理",
            "两级缓冲吸纳定理",
            "六系三层抗扰动结构定理",
            "两类方案对比定理",
            "政策波动混沌约束定理",
            "全局闭环方程组定理"
        ],
        "core_equations": {
            "总残余熵": "E_res = ΔE_city - E_out(foreign) - E_out(county) - E_out(rural) + E_shock(t)",
            "外部冲击": "E_shock(t) = A·sin(ωt)",
            "抗扰动条件": "E_shock(max) < E_out(county) + E_out(rural)",
            "基准E_res": "0.35",
            "两级缓冲总和": "0.20"
        },
        "key_parameters": {
            "ΔE_city": 0.72,
            "E_out_foreign": 0.17,
            "E_out_county": 0.13,
            "E_out_rural": 0.07,
            "E_res_base": 0.35,
            "E_shock_example": 0.12,
            "buffer_total": 0.20
        }
    }

    def __init__(self):
        self.external_shock = ExternalShockEntropy()
        self.capacity = CapacityReallocation()
        self.scenarios = ScenarioSimulation()
        self.six_systems = SixSystemsAntiDisturbance()
        self.schemes = ResponseSchemeComparison()
        self.policy_constraint = PolicyConstraintChaos()
        self.global_eq = GlobalClosedLoopEquations()

    def get_module_info(self) -> Dict:
        return self.MODULE_INFO

    def quick_anti_disturbance_check(self, e_shock_max: float) -> Dict:
        """快速抗扰动校验"""
        buffer_total = E_OUT_COUNTY_BASE + E_OUT_RURAL_BASE
        ok, msg = ExternalShockEntropy.steady_anti_disturbance_condition(
            e_shock_max, E_OUT_COUNTY_BASE, E_OUT_RURAL_BASE
        )
        return {
            "e_shock_max": e_shock_max,
            "buffer_total": buffer_total,
            "is_safe": ok,
            "message": msg
        }


# ───────────────────────────────────────
# 守卫校验
# ───────────────────────────────────────

def validate():
    """守卫校验：验证模块核心逻辑"""
    errors = []

    # 1. 验证基准稳态熵值
    E_res_calc = DELTA_E_CITY_BASE - E_OUT_FOREIGN_BASE - E_OUT_COUNTY_BASE - E_OUT_RURAL_BASE
    if abs(E_res_calc - E_RES_BASE) > 0.001:
        errors.append(f"基准残余熵计算错误：期望{E_RES_BASE}，实际{E_res_calc}")

    # 2. 验证基准熵值是否在安全线内
    if E_RES_BASE >= E_RES_SAFE:
        errors.append(f"基准熵值应在安全线内：E_res={E_RES_BASE} >= {E_RES_SAFE}")

    # 3. 验证两级缓冲总和
    buffer_total = E_OUT_COUNTY_BASE + E_OUT_RURAL_BASE
    expected_buffer = 0.20
    if abs(buffer_total - expected_buffer) > 0.001:
        errors.append(f"两级缓冲总和错误：期望{expected_buffer}，实际{buffer_total}")

    # 4. 验证情景1（无分流）
    s1 = ScenarioSimulation().scenario_1_no_shunt(0.12)
    expected_E_res_s1 = E_RES_BASE + 0.12
    if abs(s1["E_res"] - expected_E_res_s1) > 0.001:
        errors.append(f"情景1熵值错误：期望{expected_E_res_s1}，实际{s1['E_res']}")
    if s1["E_res"] <= E_RES_SAFE:
        errors.append(f"情景1应触发矿化警告：E_res={s1['E_res']} <= {E_RES_SAFE}")

    # 5. 验证情景2（有分流）
    s2 = ScenarioSimulation().scenario_2_with_shunt(0.12, 0.07, 0.05)
    expected_E_res_s2 = E_RES_BASE
    if abs(s2["E_res"] - expected_E_res_s2) > 0.001:
        errors.append(f"情景2熵值错误：期望{expected_E_res_s2}，实际{s2['E_res']}")
    if s2["remaining"] > 0.001:
        errors.append(f"情景2应完全消化冲击：剩余{s2['remaining']} > 0")

    # 6. 验证抗扰动条件
    ok, _ = ExternalShockEntropy.steady_anti_disturbance_condition(0.15, E_OUT_COUNTY_BASE, E_OUT_RURAL_BASE)
    if not ok:
        errors.append("0.15的冲击应满足抗扰动条件（<0.20缓冲）")

    ok2, _ = ExternalShockEntropy.steady_anti_disturbance_condition(0.25, E_OUT_COUNTY_BASE, E_OUT_RURAL_BASE)
    if ok2:
        errors.append("0.25的冲击应违反抗扰动条件（>0.20缓冲）")

    # 7. 验证外部冲击正弦计算
    shock_at_t0 = ExternalShockEntropy.calculate_shock_sin(0, 0.12, 0.1)
    if abs(shock_at_t0 - 0.0) > 0.001:
        errors.append(f"t=0时正弦冲击应为0：实际{shock_at_t0}")

    # 8. 验证内部分流计算
    shunt_result = CapacityReallocation.internal_shunt(0.12, 0.07, 0.05)
    if not shunt_result["is_fully_absorbed"]:
        errors.append("0.07+0.05应完全吸收0.12的冲击")
    if abs(shunt_result["total_shunt"] - 0.12) > 0.001:
        errors.append(f"总分流错误：期望0.12，实际{shunt_result['total_shunt']}")

    # 9. 验证全局方程组完整性
    eq_count = len(GlobalClosedLoopEquations.EQUATIONS)
    if eq_count < 7:
        errors.append(f"全局方程组数量不足：期望至少7个，实际{eq_count}个")

    # 10. 验证政策约束规则
    rule = PolicyConstraintChaos.constraint_rule()
    if rule["annual_limit"] >= rule["buffer_total"]:
        errors.append("年度内迁上限应小于缓冲总容量")

    # 11. 验证动态方程与基准的一致性
    # E_res = 0.22 + 0.66·x = 0.35 → x = 0.197
    x_from_base = (E_RES_BASE - C_CONSTANT) / ALPHA_CK
    if x_from_base >= X_SAFE_MAX:
        errors.append(f"基准x={x_from_base:.3f}应小于安全上限{X_SAFE_MAX}")

    return errors


# ───────────────────────────────────────
# 主程序入口
# ───────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("T63 —— 内外双循环抗扰动模型")
    print("【外贸周期冲击·E_shock正弦扰动·两级缓冲吸纳·全域闭环方程组】")
    print("=" * 70)

    module = T63DualCycleAntiDisturbanceModule()
    info = module.get_module_info()

    # 测试1：外部冲击熵定理
    print("\n【测试1】外部冲击熵定理")
    print(f"  描述：{module.external_shock.description}")
    print(f"  基准残余熵：E_res = {DELTA_E_CITY_BASE} - {E_OUT_FOREIGN_BASE} - {E_OUT_COUNTY_BASE} - {E_OUT_RURAL_BASE} = {E_RES_BASE:.2f}")

    # 测试2：数值量化测算
    print("\n【测试2】数值量化测算")
    scenarios = module.scenarios

    base = scenarios.scenario_base()
    print(f"  基准稳态：E_res = {base['E_res']:.2f}，{base['status']}")

    s1 = scenarios.scenario_1_no_shunt(0.12)
    print(f"  情景1（无分流）：E_shock={s1['E_shock']:.2f} → E_res={s1['E_res']:.2f}，{s1['status']}")

    s2 = scenarios.scenario_2_with_shunt(0.12, 0.07, 0.05)
    print(f"  情景2（有分流）：E_shock={s2['E_shock']:.2f}，分流={s2['total_shunt']:.2f} → E_res={s2['E_res']:.2f}，{s2['status']}")

    critical = scenarios.critical_buffer_line()
    print(f"  临界容量：两级缓冲总和={critical['total_buffer']:.2f}，{critical['verdict']}")

    # 测试3：稳态抗扰动条件
    print("\n【测试3】稳态抗扰动条件")
    for shock_val in [0.10, 0.15, 0.20, 0.25]:
        ok, msg = ExternalShockEntropy.steady_anti_disturbance_condition(
            shock_val, E_OUT_COUNTY_BASE, E_OUT_RURAL_BASE
        )
        print(f"  E_shock_max={shock_val:.2f}：{'✓' if ok else '✗'} {msg}")

    # 测试4：六系三层抗扰动结构
    print("\n【测试4】六系三层抗扰动结构")
    print(SixSystemsAntiDisturbance.get_summary())

    # 测试5：两类方案对比
    print("\n【测试5】两类应对方案的长期对比")
    print(ResponseSchemeComparison.get_summary())

    # 测试6：政策波动混沌约束
    print("\n【测试6】政策波动混沌约束")
    chaos = PolicyConstraintChaos.chaos_shock(A=0.12, lambda_=0.3, t=5)
    print(f"  混沌冲击（A={chaos['A']}, λ={chaos['lambda']}, t={chaos['t']}）：")
    print(f"    E_shock_chaos = {chaos['E_shock_chaos']:.6f}")
    print(f"    超出缓冲：{'是' if chaos['exceeds_buffer'] else '否'}")

    rule = PolicyConstraintChaos.constraint_rule()
    print(f"  约束规则：{rule['rule']}")
    print(f"    缓冲总容量：{rule['buffer_total']:.2f}")
    print(f"    年度上限：{rule['annual_limit']:.2f}")

    # 测试7：全局完整联立方程组
    print("\n【测试7】全局完整联立方程组（最终闭环模型）")
    print(GlobalClosedLoopEquations.get_summary())

    # 测试8：产能跨区域再配置
    print("\n【测试8】产能跨区域再配置")
    dQ_trade = CapacityReallocation.dQ_trade_dt(0.3)
    dQ_domestic = CapacityReallocation.dQ_domestic_dt(0.3)
    print(f"  dQ_trade/dt = {dQ_trade:.2f}（外需收缩）")
    print(f"  dQ_domestic/dt = {dQ_domestic:.2f}（内需承接）")

    # 测试9：方程速查
    print("\n【测试9】方程速查")
    eqs = GlobalClosedLoopEquations.EQUATIONS
    for name, eq in eqs.items():
        print(f"  {name}: {eq}")
    print(f"  关键参数：ΔE_city={DELTA_E_CITY_BASE}, E_out(foreign)={E_OUT_FOREIGN_BASE}")
    print(f"  缓冲总量：E_out(county)+E_out(rural) = {E_OUT_COUNTY_BASE}+{E_OUT_RURAL_BASE} = {E_OUT_COUNTY_BASE+E_OUT_RURAL_BASE}")

    # 测试10：完整总览
    print("\n【测试10】完整总览")
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

    # 测试11：守卫校验
    print("\n【测试11】守卫校验")
    errors = validate()
    if errors:
        print(f"  校验结果：✗ 失败")
        for e in errors:
            print(f"    错误：{e}")
    else:
        print(f"  校验结果：✓ 通过")

    # 测试12：快速查询
    print("\n【测试12】快速查询")
    for shock in [0.05, 0.10, 0.15, 0.20, 0.25]:
        r = module.quick_anti_disturbance_check(shock)
        print(f"  E_shock_max={shock:.2f} → 缓冲={r['buffer_total']:.2f}，{'安全' if r['is_safe'] else '超限'}")

    print("\n" + "=" * 70)
    print("T63内外双循环抗扰动模型验证完成！")
    print("【外贸周期冲击·正弦扰动·两级缓冲·全域闭环方程组】")
    print("=" * 70)
