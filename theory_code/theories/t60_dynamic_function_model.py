"""
T60 —— 城乡熵分流动态函数模型
【E_res线性微分方程·人口集聚临界速度·混沌扰动·政策量化约束】
T59深化

六大核心定理：
1. 动态熵流定理：E_res(t)=C+(α+ck)·x(t)，残余熵与人口集聚速率严格正相关
2. 人口临界速度定理：安全临界x<0.273，停滞临界x≈0.803
3. 双路径演化定理：维持x≈0.45→中层矿化；压低x<0.273→安全稳态
4. 混沌熵暴增定理：人口脉冲式跳变→E_res+Ae^(λt)，直接击穿底层承载层
5. 六系分层总结定理：顶层（天道强化）、中层（变身具现）、底层（社会自然）逐级失衡
6. 政策量化约束定理：x<0.273安全、x≈0.803停滞、当前x≈0.45→E_res≈0.517

版本：V1.0
归属：L0_总本源层 / 天人同构动力学·文明系统动态分析篇
依赖：T45, T48, T51, T54, T55, T56, T57, T58, T59
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math


# ============================================================
# 一、动态熵流定理
# ============================================================

@dataclass
class DynamicEntropyFlow:
    """动态熵流定理：E_res(t)=C+(α+ck)·x(t)"""

    name: str = "动态熵流定理"

    # 变量定义
    variables: Dict[str, str] = field(default_factory=lambda: {
        "x(t)": "中心大城市人口集聚速率（城镇化单向推进速度，无量纲）",
        "B(t)": "乡村+县域缓冲容量",
        "ΔE_city": "城市内生熵增量",
        "E_out(rural)": "乡村熵分流能力",
        "E_out(county)": "县域熵分流能力",
        "E_out(foreign)": "外循环外贸排熵（短期常数）",
    })

    # 缓冲容量函数
    buffer_function: str = "B(t) = B_0 - k·x(t)"
    buffer_explanation: Dict[str, str] = field(default_factory=lambda: {
        "B_0": "初始乡村缓冲容量",
        "k>0": "人口集聚造成缓冲衰减系数",
        "规律": "缓冲层萎缩速率与人口流入正相关",
    })

    # 城市熵增量函数
    city_entropy_function: str = "ΔE_city = ΔE_0 + α·x(t)"
    city_explanation: Dict[str, str] = field(default_factory=lambda: {
        "规律": "人口越集中，熵增长越快",
    })

    # 乡村熵分流函数
    rural_function: str = "E_out(rural) = c·B(t)"
    rural_explanation: str = "随缓冲容量同步萎缩"

    # 核心规律
    core_pattern: str = "残余熵 E_res 与人口单向集聚速率 x(t) 成严格正相关。大城市人口流入越快，缓冲圈层损耗越快，熵淤积上升越迅猛。"

    # 简化方程参数
    C: float = 0.22       # 常数项
    alpha_plus_ck: float = 0.66  # 系数

    # 量化计算
    @staticmethod
    def calc_buffer(B0: float, k: float, x: float) -> float:
        """缓冲容量：B(t) = B_0 - k·x(t)"""
        return B0 - k * x

    @staticmethod
    def calc_city_entropy(delta_E0: float, alpha: float, x: float) -> float:
        """城市熵增量：ΔE_city = ΔE_0 + α·x(t)"""
        return delta_E0 + alpha * x

    def calc_E_res(self, x: float) -> float:
        """核心微分方程：E_res(t) = 0.22 + 0.66·x(t)"""
        return self.C + self.alpha_plus_ck * x


# ============================================================
# 二、人口临界速度定理
# ============================================================

@dataclass
class CriticalSpeedTheorem:
    """人口临界速度定理：安全临界与停滞临界"""

    name: str = "人口临界速度定理"

    # 当前基准参数
    C: float = 0.22
    k: float = 0.66

    # 临界速度计算
    @staticmethod
    def calc_safe_critical() -> float:
        """安全临界速度：令E_res=0.40，解x"""
        # 0.22 + 0.66x = 0.40 → x = (0.40 - 0.22) / 0.66
        return (0.40 - 0.22) / 0.66

    @staticmethod
    def calc_stagnation_critical() -> float:
        """停滞临界速度：令E_res=0.75，解x"""
        # 0.22 + 0.66x = 0.75 → x = (0.75 - 0.22) / 0.66
        return (0.75 - 0.22) / 0.66

    # 状态判定
    @staticmethod
    def classify_state(x: float) -> Dict[str, str]:
        """根据集聚速度判定所处状态"""
        safe = CriticalSpeedTheorem.calc_safe_critical()
        stagnation = CriticalSpeedTheorem.calc_stagnation_critical()
        dynamic = DynamicEntropyFlow()
        E_res = dynamic.calc_E_res(x)

        if E_res >= 0.98:
            return {
                "状态": "全域坍缩红线",
                "E_res": f"{E_res:.3f}",
                "说明": "创新活力收敛，彻底陷入存量博弈轮回",
            }
        elif E_res >= 0.75:
            return {
                "状态": "底层僵化红线",
                "E_res": f"{E_res:.3f}",
                "说明": "内需长期萎缩，经济进入准停滞",
            }
        elif E_res >= 0.40:
            return {
                "状态": "中层矿化警戒",
                "E_res": f"{E_res:.3f}",
                "说明": "产业固化、阶层流动放缓",
            }
        else:
            return {
                "状态": "安全稳态",
                "E_res": f"{E_res:.3f}",
                "说明": "产业迭代通畅，无大面积内卷",
            }


# ============================================================
# 三、双路径演化定理
# ============================================================

@dataclass
class DualPathEvolution:
    """双路径演化定理"""

    name: str = "双路径演化定理"

    # 路径一：维持当前速度
    path_one: Dict = field(default_factory=lambda: {
        "名称": "路径一：维持当前城镇化集聚速度 x≈0.45",
        "E_res当前": 0.517,
        "E_res趋势": "15~25年内逐步逼近0.75停滞红线",
        "后果": [
            "乡村缓冲持续被消耗，B(t)逐年下降",
            "方程系数ck持续变大，熵淤积曲线更加陡峭",
            "城市产业彻底固化为地产+基建存量结构",
            "变身系迭代停滞，六系中间层完全锁死",
        ],
        "天体同构": "行星失去卫星后内核持续冷却，圈层一步步僵死",
    })

    # 路径二：主动压低速度
    path_two: Dict = field(default_factory=lambda: {
        "名称": "路径二：主动压低单向集聚速度 x<0.273",
        "E_res目标": "<0.40",
        "后果": [
            "严格控制超大都市人口无序扩张",
            "引导人口向县域、中小城市分流",
            "保住乡村缓冲容量B(t)不再快速萎缩",
            "三级熵分流网络长期完整",
        ],
        "结果": "城乡双向流动保持弹性，六系三层对冲长期均衡",
    })


# ============================================================
# 四、混沌熵暴增定理
# ============================================================

@dataclass
class ChaosEntropyBurst:
    """混沌熵暴增定理"""

    name: str = "混沌熵暴增定理"

    # 脉冲触发条件
    pulse_trigger: str = "人口集聚速度剧烈波动：阶段性突击放开大城市落户、短期人口暴增，x(t)出现脉冲式跳变"

    # 混沌方程
    chaos_equation: str = "E_res = 0.22 + 0.66·x(t) + A·e^(λt)"

    chaos_explanation: Dict[str, str] = field(default_factory=lambda: {
        "A": "扰动初始强度",
        "λ": "混沌指数放大系数",
        "效果": "短期之内熵值直接跳升至0.75以上，无需缓慢累积，直接击穿底层承载层",
    })

    # 现实印证
    reality_verification: str = "短期大城市人口暴涨之后，很快出现就业饱和、房价债务矛盾集中爆发的数理根源"

    @staticmethod
    def calc_chaos_E_res(x: float, A: float, lambda_val: float, t: float) -> float:
        """混沌扰动熵计算：E_res = 0.22 + 0.66x + A·e^(λt)"""
        base = 0.22 + 0.66 * x
        return base + A * math.exp(lambda_val * t)


# ============================================================
# 五、六系分层总结定理
# ============================================================

@dataclass
class SixSystemsLayerSummary:
    """六系分层总结定理"""

    name: str = "六系分层总结定理"

    # 三层总结
    three_layers: Dict[str, Dict] = field(default_factory=lambda: {
        "顶层两极": {
            "六系": "天道系 ↔ 强化系",
            "失衡表现": [
                "发展路径单一绑定大城市城市化",
                "集聚速度失控压缩个体多元发展空间",
                "创新活力逐步收敛",
            ],
        },
        "中间转化层": {
            "六系": "变身系 ↔ 具现系",
            "失衡表现": [
                "人口过度向中心城市集中",
                "新旧产业更替失衡",
                "不动产存量产业固化",
                "出现矿山式淤积",
            ],
        },
        "底层承载层": {
            "六系": "社会系 ↔ 自然系",
            "失衡表现": [
                "城乡缓冲圈层萎缩",
                "矛盾全部挤压在城市单一空间",
                "生存博弈加剧",
                "内需持续收缩",
            ],
        },
    })


# ============================================================
# 六、政策量化约束定理
# ============================================================

@dataclass
class PolicyQuantConstraint:
    """政策量化约束定理"""

    name: str = "政策量化约束定理"

    # 五条核心结论
    five_conclusions: Dict[int, str] = field(default_factory=lambda: {
        1: "人口向核心大城市单向集聚的安全临界增速：x<0.273，超过即陷入产业固化与内卷",
        2: "停滞临界增速：x≈0.803，抵达后经济体进入长期准停滞",
        3: "当前集聚速度偏高，熵值约0.517，处在中层矿化区间",
        4: "唯一长效解法：放缓核心大都市人口吸纳速度，完善县域二级节点，保住乡村三级缓冲圈层",
        5: "只要缓冲容量不再快速萎缩，就能稳住残余熵，让六系动力学重新回到动态平衡",
    })

    # 方程速查
    equations: Dict[str, str] = field(default_factory=lambda: {
        "缓冲容量": "B(t) = B_0 - k·x(t)",
        "城市熵增量": "ΔE_city = ΔE_0 + α·x(t)",
        "核心微分方程": "E_res(t) = 0.22 + 0.66·x(t)",
        "安全临界速度": "x < 0.273",
        "停滞临界速度": "x ≈ 0.803",
        "混沌扰动方程": "E_res = 0.22 + 0.66·x(t) + A·e^(λt)",
    })


# ============================================================
# 七、主模块：城乡熵分流动态函数模型
# ============================================================

@dataclass
class DynamicFunctionModule:
    """城乡熵分流动态函数模型主模块"""

    module_id: str = "T60"
    module_name: str = "城乡熵分流动态函数模型"
    subtitle: str = "E_res线性微分方程·人口集聚临界速度·混沌扰动·政策量化约束"
    version: str = "V1.0"
    level: str = "L0_总本源层"
    category: str = "天人同构动力学·文明系统动态分析篇"
    dependencies: List[str] = field(default_factory=lambda: [
        "T45", "T48", "T51", "T54", "T55", "T56", "T57", "T58", "T59"
    ])

    # 子系统
    dynamic_entropy: DynamicEntropyFlow = field(default_factory=DynamicEntropyFlow)
    critical_speed: CriticalSpeedTheorem = field(default_factory=CriticalSpeedTheorem)
    dual_path: DualPathEvolution = field(default_factory=DualPathEvolution)
    chaos: ChaosEntropyBurst = field(default_factory=ChaosEntropyBurst)
    six_summary: SixSystemsLayerSummary = field(default_factory=SixSystemsLayerSummary)
    policy: PolicyQuantConstraint = field(default_factory=PolicyQuantConstraint)

    def get_six_theorems(self) -> List[str]:
        """获取六大定理名称"""
        return [
            self.dynamic_entropy.name,
            self.critical_speed.name,
            self.dual_path.name,
            self.chaos.name,
            self.six_summary.name,
            self.policy.name,
        ]

    def simulate_speed_state(self, x: float) -> Dict:
        """模拟不同人口集聚速度的状态"""
        E_res = self.dynamic_entropy.calc_E_res(x)
        state = self.critical_speed.classify_state(x)
        safe = self.critical_speed.calc_safe_critical()
        stagnation = self.critical_speed.calc_stagnation_critical()

        return {
            "人口集聚速度x": x,
            "残余熵E_res": round(E_res, 3),
            "状态": state["状态"],
            "说明": state["说明"],
            "安全临界": f"x < {safe:.3f}",
            "停滞临界": f"x ≈ {stagnation:.3f}",
            "是否安全": E_res < 0.40,
            "是否危险": E_res >= 0.75,
        }

    def get_complete_summary(self) -> Dict:
        """获取完整总览"""
        safe = self.critical_speed.calc_safe_critical()
        stagnation = self.critical_speed.calc_stagnation_critical()
        current_E_res = self.dynamic_entropy.calc_E_res(0.45)

        return {
            "模块编号": self.module_id,
            "模块名称": self.module_name,
            "副标题": self.subtitle,
            "版本": self.version,
            "归属层级": self.level,
            "类别": self.category,
            "依赖模块": self.dependencies,
            "六大定理": self.get_six_theorems(),
            "核心方程": "E_res(t) = 0.22 + 0.66·x(t)",
            "安全临界速度": f"x < {safe:.3f}",
            "停滞临界速度": f"x ≈ {stagnation:.3f}",
            "当前状态": f"x≈0.45，E_res≈{current_E_res:.3f}（中层矿化）",
            "理论地位": "T59深化·动态函数·人口临界速度·政策量化约束",
        }

    # ===== 守卫校验 =====
    def validate(self) -> Tuple[bool, List[str]]:
        """守卫校验：验证模型的一致性与正确性"""
        errors = []

        # 1. 六大定理数量校验
        if len(self.get_six_theorems()) != 6:
            errors.append(f"六大定理数量应为6，实际为{len(self.get_six_theorems())}")

        # 2. 安全临界速度校验
        safe = self.critical_speed.calc_safe_critical()
        expected_safe = (0.40 - 0.22) / 0.66
        if abs(safe - expected_safe) > 0.001:
            errors.append(f"安全临界速度错误：预期{expected_safe:.4f}，实际{safe:.4f}")
        if abs(safe - 0.273) > 0.002:
            errors.append(f"安全临界速度应为≈0.273，实际{safe:.3f}")

        # 3. 停滞临界速度校验
        stagnation = self.critical_speed.calc_stagnation_critical()
        expected_stagnation = (0.75 - 0.22) / 0.66
        if abs(stagnation - expected_stagnation) > 0.001:
            errors.append(f"停滞临界速度错误：预期{expected_stagnation:.4f}，实际{stagnation:.4f}")
        if abs(stagnation - 0.803) > 0.002:
            errors.append(f"停滞临界速度应为≈0.803，实际{stagnation:.3f}")

        # 4. 当前状态校验
        current_E_res = self.dynamic_entropy.calc_E_res(0.45)
        if abs(current_E_res - 0.517) > 0.002:
            errors.append(f"当前E_res应为≈0.517，实际{current_E_res:.3f}")

        # 5. 状态判定校验
        states = [
            (0.2, "安全稳态"),
            (0.45, "中层矿化"),
            (0.8, "中层矿化"),  # E_res=0.748 < 0.75
            (1.0, "底层僵化"),  # E_res=0.880 >= 0.75
        ]
        for x, expected in states:
            E_res = self.dynamic_entropy.calc_E_res(x)
            result = self.critical_speed.classify_state(x)["状态"]
            if expected not in result:
                errors.append(f"状态判定错误：x={x}预期包含{expected}，实际{result}")

        # 6. 混沌方程校验
        chaos_E_res = self.chaos.calc_chaos_E_res(0.45, 0.5, 0.3, 5)
        base = 0.22 + 0.66 * 0.45
        chaos_term = 0.5 * math.exp(0.3 * 5)
        expected_chaos = base + chaos_term
        if abs(chaos_E_res - expected_chaos) > 0.1:
            errors.append(f"混沌熵计算错误：预期{expected_chaos:.2f}，实际{chaos_E_res:.2f}")

        # 7. 三层六系校验
        if len(self.six_summary.three_layers) != 3:
            errors.append(f"三层六系应为3，实际为{len(self.six_summary.three_layers)}")

        # 8. 政策五条结论校验
        if len(self.policy.five_conclusions) != 5:
            errors.append(f"政策结论应为5条，实际为{len(self.policy.five_conclusions)}")

        # 9. 方程速查校验
        if len(self.policy.equations) != 6:
            errors.append(f"方程速查应为6个，实际为{len(self.policy.equations)}")

        is_valid = len(errors) == 0
        return is_valid, errors


# ============================================================
# 八、快速查询接口
# ============================================================

def get_dynamic_module() -> DynamicFunctionModule:
    """获取城乡熵分流动态函数模型模块实例"""
    return DynamicFunctionModule()


def quick_speed_state_query(x: float) -> str:
    """快速查询：人口集聚速度状态"""
    module = get_dynamic_module()
    result = module.simulate_speed_state(x)
    return (f"x={x:.2f} → E_res={result['残余熵E_res']}，"
            f"{result['状态']}，{'安全' if result['是否安全'] else '不安全'}")


def quick_critical_speed_query() -> str:
    """快速查询：临界速度"""
    module = get_dynamic_module()
    safe = module.critical_speed.calc_safe_critical()
    stagnation = module.critical_speed.calc_stagnation_critical()
    current = module.dynamic_entropy.calc_E_res(0.45)
    return (f"安全临界：x<{safe:.3f}，停滞临界：x≈{stagnation:.3f}，"
            f"当前：x≈0.45→E_res≈{current:.3f}（中层矿化）")


def quick_chaos_query(x: float, A: float, lambda_val: float, t: float) -> str:
    """快速查询：混沌扰动效果"""
    module = get_dynamic_module()
    base_E = module.dynamic_entropy.calc_E_res(x)
    chaos_E = module.chaos.calc_chaos_E_res(x, A, lambda_val, t)
    return (f"基准x={x}→E_res={base_E:.3f}，"
            f"混沌扰动(A={A}, λ={lambda_val}, t={t})→E_res={chaos_E:.3f}，"
            f"增量+{chaos_E-base_E:.3f}")


# ============================================================
# 九、自测入口
# ============================================================

def _run_self_test():
    """运行自测"""
    print("=" * 70)
    print("  T60 —— 城乡熵分流动态函数模型")
    print("  【E_res线性微分方程·人口集聚临界速度·混沌扰动·政策量化约束】")
    print("=" * 70)

    module = get_dynamic_module()

    # 测试1：动态熵流定理
    print("\n【测试1】动态熵流定理")
    print(f"  核心规律: {module.dynamic_entropy.core_pattern}")
    print(f"  简化方程: E_res(t) = {module.dynamic_entropy.C} + {module.dynamic_entropy.alpha_plus_ck}·x(t)")

    # 测试2：核心微分方程计算
    print("\n【测试2】核心微分方程计算")
    test_x = [0.2, 0.273, 0.45, 0.8, 1.0]
    for x in test_x:
        E_res = module.dynamic_entropy.calc_E_res(x)
        print(f"  x={x:.3f} → E_res={E_res:.3f}")

    # 测试3：人口临界速度定理
    print("\n【测试3】人口临界速度定理")
    safe = module.critical_speed.calc_safe_critical()
    stagnation = module.critical_speed.calc_stagnation_critical()
    print(f"  安全临界速度: x < {safe:.3f}")
    print(f"  停滞临界速度: x ≈ {stagnation:.3f}")

    # 测试4：状态判定
    print("\n【测试4】状态判定测试")
    test_x = [0.2, 0.3, 0.45, 0.8, 1.0]
    for x in test_x:
        state = module.critical_speed.classify_state(x)
        print(f"  x={x:.2f} → E_res={state['E_res']}，{state['状态']}")

    # 测试5：速度状态模拟
    print("\n【测试5】速度状态模拟")
    for x in [0.2, 0.273, 0.45, 0.803, 1.0]:
        result = module.simulate_speed_state(x)
        print(f"  x={result['人口集聚速度x']:.3f} → E_res={result['残余熵E_res']}，{result['状态']}")

    # 测试6：双路径演化
    print("\n【测试6】双路径演化定理")
    print(f"  【{module.dual_path.path_one['名称']}】")
    print(f"    E_res={module.dual_path.path_one['E_res当前']}，{module.dual_path.path_one['E_res趋势']}")
    print(f"  【{module.dual_path.path_two['名称']}】")
    print(f"    E_res目标<0.40，{module.dual_path.path_two['结果']}")

    # 测试7：混沌熵暴增
    print("\n【测试7】混沌熵暴增定理")
    print(f"  脉冲触发: {module.chaos.pulse_trigger}")
    print(f"  混沌方程: {module.chaos.chaos_equation}")
    chaos_E = module.chaos.calc_chaos_E_res(0.45, 0.5, 0.3, 5)
    base_E = module.dynamic_entropy.calc_E_res(0.45)
    print(f"  示例: x=0.45, A=0.5, λ=0.3, t=5")
    print(f"    基准E_res={base_E:.3f} → 混沌E_res={chaos_E:.3f}，增量+{chaos_E-base_E:.3f}")

    # 测试8：六系分层总结
    print("\n【测试8】六系分层总结定理")
    for layer, info in module.six_summary.three_layers.items():
        print(f"  {layer}: {info['六系']}")
        print(f"    表现: {info['失衡表现'][0][:30]}...")

    # 测试9：政策量化约束
    print("\n【测试9】政策量化约束定理")
    for i, conclusion in module.policy.five_conclusions.items():
        print(f"  {i}. {conclusion[:50]}...")

    # 测试10：方程速查
    print("\n【测试10】方程速查")
    for name, eq in module.policy.equations.items():
        print(f"  {name}: {eq}")

    # 测试11：完整总览
    print("\n【测试11】完整总览")
    summary = module.get_complete_summary()
    for k, v in summary.items():
        if isinstance(v, list):
            print(f"  {k}: {v}")
        else:
            print(f"  {k}: {v}")

    # 测试12：守卫校验
    print("\n【测试12】守卫校验")
    is_valid, errors = module.validate()
    if is_valid:
        print("  校验结果: ✓ 通过")
    else:
        print("  校验结果: ✗ 失败")
        for e in errors:
            print(f"    - {e}")

    # 测试13：快速查询
    print("\n【测试13】快速查询")
    print(f"  {quick_speed_state_query(0.45)}")
    print(f"  {quick_critical_speed_query()}")
    print(f"  {quick_chaos_query(0.45, 0.5, 0.3, 5)[:60]}...")

    print("\n" + "=" * 70)
    print("  T60城乡熵分流动态函数模型验证完成!")
    print("  【6大定理·E_res微分方程·临界速度·混沌扰动·政策约束】")
    print("=" * 70)


if __name__ == "__main__":
    _run_self_test()