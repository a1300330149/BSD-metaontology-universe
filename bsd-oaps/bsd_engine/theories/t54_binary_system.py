"""
T54 —— 行星—卫星双星系统六系统一模型
【双体共生·熵淤积延缓·三级繁衍谱系·低阶界域抗熵最优解】

五大核心定理：
1. 双星双体共生定理：卫星=行星三级共生单元，双星构成小型双体闭环
2. 双星三组对冲定理：天道↔强化、变身↔具现、社会↔自然（双星子系统）
3. 双星熵分流定理：双体系统分流熵、潮汐补能、动量分摊，延缓淤积
4. 卫星子代繁衍定理：卫星=行星子代，无性（吸积）+有性（撞击重组）
5. 双星抗熵最优解定理：双体共生是低阶界域对抗熵增的最优解

版本：V1.0
归属：L0_总本源层 / 九界物质实体界演化理论·双星子系统篇
依赖：T45, T48, T51, T52, T53
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


# ============================================================
# 一、双星系统整体定位
# ============================================================

@dataclass
class BinarySystemHierarchy:
    """行星—卫星双星系统整体定位：三级层级体系"""

    name: str = "双星双体共生定理"

    hierarchy: Dict[int, Dict] = field(default_factory=lambda: {
        1: {
            "层级": "第一级",
            "类型": "恒星",
            "定位": "一级主体意义涌现体",
            "六系结构": "六系完整展开的高阶意义体",
        },
        2: {
            "层级": "第二级",
            "类型": "行星",
            "定位": "二级子系统",
            "六系结构": "依附恒星的次级载体系统",
        },
        3: {
            "层级": "第三级",
            "类型": "行星+卫星",
            "定位": "双体共生闭环",
            "六系结构": "小型双体闭环，独立六系对冲循环",
        },
        4: {
            "层级": "第四级",
            "类型": "地表生态",
            "定位": "高阶意义萌芽",
            "六系结构": "碳基生命与文明的温床",
        },
    })

    core_advantage: str = "行星与卫星构成小型双体闭环，形成独立的六系对冲循环，彼此互相制衡，分散熵淤积，延缓内核冷却、地层固化、自转停滞，大幅拉长整个子系统的存续周期。"

    def get_three_tier_lineage(self) -> str:
        """获取三级繁衍谱系"""
        return "恒星（一级） → 行星（二级） → 卫星（三级）"


# ============================================================
# 二、双星系统三组对冲六系
# ============================================================

@dataclass
class BinaryThreePoles:
    """双星系统三组对冲六系"""

    name: str = "双星三组对冲定理"

    top_layer: Dict = field(default_factory=lambda: {
        "天道系": {
            "内涵": "双体轨道约束、潮汐共振、公转周期法则",
            "特征": "行星与卫星互相锁定轨道，运行周期形成刚性秩序；双层天道规则层层嵌套（主恒星大框架+双星小框架）",
        },
        "强化系": {
            "内涵": "两颗天体各自的自转惯性、内核地热内禀动力",
            "双星优势": "行星的自转动量可以传递给卫星，两极对抗被分摊，弱化单一星体的受力压力",
        },
        "动力学现象": "潮汐共振：卫星不断拉扯行星外壳，延缓自转减速，自转衰减速率大幅下降",
    })

    middle_layer: Dict = field(default_factory=lambda: {
        "变身系": {
            "内涵": "双星之间的物质交换、陨石撞击、地貌改造、圈层缓慢变迁",
            "双星优势": "卫星不断扰动行星地表环境，让地貌、气候长期保持动态更替，避免环境永久固化",
        },
        "具现系": {
            "内涵": "两颗星体的岩石壳体、地层、矿产矿山实体",
            "双星优势": "卫星带来持续的潮汐应力，不断撕裂地壳，让岩层长期保持破碎、流动，延缓地层彻底僵死固化",
        },
        "核心作用": "潮汐应力持续激活中间转化层，避免变身—具现双层彻底锁死，推迟中层矿化灾害的到来。",
    })

    bottom_layer: Dict = field(default_factory=lambda: {
        "社会系": {
            "内涵": "双星彼此的引力拉扯、相互制衡的博弈网络",
            "特征": "形成小型零和博弈关系，构成独立于恒星引力之外的次级关系网络",
        },
        "自然系": {
            "内涵": "两颗星体各自的固态物质内核",
            "功能": "岩石本体保证星体结构不溃散，构成双系统的物质根基",
        },
        "失衡后果": "卫星被撕碎、脱离轨道→行星失去制衡伙伴→社会系网络断裂→走向载体僵化（白矮星式死寂）",
    })

    def get_all_three_layers(self) -> Dict[str, Dict]:
        """获取三组对冲完整结构"""
        return {
            "顶层两极": self.top_layer,
            "中间转化层": self.middle_layer,
            "底层承载层": self.bottom_layer,
        }


# ============================================================
# 三、双星系统熵淤积延缓机制（量化模型）
# ============================================================

@dataclass
class BinaryEntropyDelay:
    """双星系统熵淤积延缓机制（量化模型）"""

    name: str = "双星熵分流定理"

    # 3.1 熵分流原理
    entropy_sharing: Dict = field(default_factory=lambda: {
        "孤立行星": "E_res = ΔE - E_out（所有内生熵只能依靠自身大气外排）",
        "双星系统": "E_res(行星) = ΔE/2 - E_out（熵被拆分到两个天体，单星淤积量被稀释）",
        "核心效果": "单星残留熵显著降低，更难触碰E_limit临界崩塌阈值",
    })

    # 3.2 六系展开度维持（动态微分方程）
    expansion_maintenance: Dict = field(default_factory=lambda: {
        "孤立行星": "dS/dt → 0（内核冷却快，内生能量快速枯竭）",
        "双星系统": "dS/dt = k_in·ΔE + k_tide·E_tide - k_out·E_out - k_res·E_res",
        "E_tide": "潮汐摩擦新增内能",
        "核心效果": "六系展开度S能够长期维持在高位，长期保持动态循环，不会快速落入五元残缺稳态",
    })

    # 3.3 三种灾害延后效果
    disaster_delay: Dict[int, Dict] = field(default_factory=lambda: {
        1: {
            "灾害类型": "中层矿化",
            "对应层级": "变身+具现僵死",
            "延缓效果": "潮汐持续扰动地壳，地层固化时间成倍拉长",
        },
        2: {
            "灾害类型": "底层载体僵化",
            "对应层级": "自然+社会锁死",
            "延缓效果": "双体引力制衡长久稳定，圈层循环不会轻易中断",
        },
        3: {
            "灾害类型": "顶层两极归零",
            "对应层级": "天道吞噬强化",
            "延缓效果": "动量在双星之间来回传递，自转不会迅速被潮汐锁定，个体自性长期存续",
        },
    })

    ultimate_conclusion: str = "只要卫星不脱离轨道，整个二级子系统的寿命可以延长数倍。"

    # 量化计算方法
    @staticmethod
    def calc_isolated_E_res(delta_E: float, E_out: float) -> float:
        """孤立行星淤积熵计算"""
        return delta_E - E_out

    @staticmethod
    def calc_binary_E_res(delta_E: float, E_out: float,
                          sharing_ratio: float = 0.5) -> float:
        """双星系统行星淤积熵计算（默认熵五五分）"""
        return delta_E * sharing_ratio - E_out

    @staticmethod
    def calc_dS_dt(k_in: float, delta_E: float,
                   k_tide: float, E_tide: float,
                   k_out: float, E_out: float,
                   k_res: float, E_res: float) -> float:
        """双星系统六系展开度变化率"""
        return k_in * delta_E + k_tide * E_tide - k_out * E_out - k_res * E_res

    @staticmethod
    def calc_lifetime_extension_factor(sharing_effect: float = 2.0,
                                       tide_supply: float = 1.5) -> float:
        """寿命延长因子估算"""
        return sharing_effect * tide_supply


# ============================================================
# 四、卫星作为行星子代：繁衍遗传机制
# ============================================================

@dataclass
class SatelliteReproduction:
    """卫星作为行星子代：繁衍遗传机制"""

    name: str = "卫星子代繁衍定理"

    asexual: Dict = field(default_factory=lambda: {
        "名称": "无性繁衍：星云吸积形成卫星",
        "机制": "行星形成之后，残余尘埃在轨道吸积凝聚成卫星",
        "特征": "完整复刻行星的六系基础基因，变异率μ→0，属于纯粹本体复刻",
        "实例": "绝大多数原始卫星都以这种方式诞生",
    })

    sexual: Dict = field(default_factory=lambda: {
        "名称": "有性繁衍：撞击重组（高阶基因迭代）",
        "机制": "大型小行星猛烈撞击行星，表层岩石物质被抛入轨道，重新凝聚成新卫星",
        "公式": "G_new = η·G_old + μ·ΔS",
        "特征": "旧星体结构被打碎重组，六系结构基因发生重组变异，子代卫星拥有全新的圈层构型",
        "ΔS": "碰撞带来的结构增量",
    })

    lineage_complete: List[str] = field(default_factory=lambda: [
        "星云 → 恒星（一级生命体）",
        "恒星周边星云凝聚出行星（一级子代）",
        "行星撞击吸积诞生卫星（二级子代）",
    ])

    core_conclusion: str = "形成三级嵌套繁衍谱系，六系结构基因层层向下遗传。"


# ============================================================
# 五、双星系统三种崩塌归宿
# ============================================================

@dataclass
class BinaryCollapseEndings:
    """极端结局：双星系统的三种崩塌归宿"""

    name: str = "双星三结局定理"

    three_endings: Dict[int, Dict] = field(default_factory=lambda: {
        1: {
            "类型": "中层崩溃",
            "对应层级": "变身+具现层",
            "机制": "潮汐扰动减弱，地壳彻底冷却固化，地貌不再变迁，岩层完全矿化",
            "结局": "行星地表永久僵死，对应中子星结局。即便双星轨道还在，中间转化层已经失去演化活力。",
            "阈值区间": [0.40, 0.75],
        },
        2: {
            "类型": "底层崩溃",
            "对应层级": "自然+社会层",
            "机制": "卫星缓慢远离轨道，双星引力制衡网络断裂",
            "结局": "行星失去外部博弈对象，大气循环、水文循环逐步停滞，物质载体彻底僵化，沦为冰冷岩石残骸，对应白矮星。",
            "阈值区间": [0.75, 0.98],
        },
        3: {
            "类型": "顶层全域坍缩",
            "对应层级": "天道压制强化",
            "机制": "卫星坠入行星或者被撕碎，双体闭环彻底瓦解",
            "结局": "行星单独面对主恒星的引力潮汐，自转快速被锁定，个体自性完全被轨道规则吞噬。所有动态流转全部归零，外向意义尽数收敛，最终走向死寂，抵达行星版本的0元纳熵稳态。",
            "阈值区间": [0.98, 1.0],
        },
    })

    def classify_ending(self, E_res: float) -> str:
        """根据淤积熵比判定崩塌结局"""
        if E_res >= 0.98:
            return "顶层全域坍缩（0元纳熵稳态）"
        elif E_res >= 0.75:
            return "底层崩溃（对应白矮星）"
        elif E_res >= 0.40:
            return "中层崩溃（对应中子星）"
        else:
            return "双体共生活跃期（未触发崩塌）"


# ============================================================
# 六、关键推论：双体共生是低阶界域抗熵最优解
# ============================================================

@dataclass
class AntiEntropyOptimal:
    """关键推论：双体共生是低阶界域对抗熵增的最优解"""

    name: str = "双星抗熵最优解定理"

    five_points: Dict[int, str] = field(default_factory=lambda: {
        1: "孤立系统必然快速衰败：孤立单星、孤立行星，必然快速熵淤积，早早走向层级崩塌",
        2: "双体系统延缓熵增：双星、双体系统可以分流熵、补充内能、分摊轨道压力，延缓六系失衡",
        3: "双体创造温和环境：行星—卫星体系创造了相对温和的动态环境，为地表形成大气、水文、气候循环提供稳定条件",
        4: "双体孕育高阶意义：唯有这种长期稳定的次级闭环系统，才能在星体表层孕育开放型意义系统，也就是碳基生命与文明",
        5: "逐级开放演化链条：从恒星→行星→双星子系统→地表生态圈，整个物质实体界逐级降低封闭性，逐步从「封闭纳熵循环」过渡为「跨界排熵的高阶开放演化」，完美衔接九界层级跃迁逻辑",
    })

    evolution_chain: List[str] = field(default_factory=lambda: [
        "恒星（封闭纳熵循环）",
        "行星（半开放次级系统）",
        "双星子系统（双体共生·更稳定）",
        "地表生态圈（跨界排熵的高阶开放演化）",
    ])

    core_proposition: str = "双体共生是低阶界域对抗熵增的最优解。"


# ============================================================
# 七、主模块：行星—卫星双星系统六系统一模型
# ============================================================

@dataclass
class BinarySystemModule:
    """行星—卫星双星系统六系统一模型主模块"""

    module_id: str = "T54"
    module_name: str = "行星—卫星双星系统六系统一模型"
    subtitle: str = "双体共生·熵淤积延缓·三级繁衍谱系·低阶界域抗熵最优解"
    version: str = "V1.0"
    level: str = "L0_总本源层"
    category: str = "九界物质实体界演化理论·双星子系统篇"
    dependencies: List[str] = field(default_factory=lambda: ["T45", "T48", "T51", "T52", "T53"])

    # 子系统
    hierarchy: BinarySystemHierarchy = field(default_factory=BinarySystemHierarchy)
    three_poles: BinaryThreePoles = field(default_factory=BinaryThreePoles)
    entropy_delay: BinaryEntropyDelay = field(default_factory=BinaryEntropyDelay)
    reproduction: SatelliteReproduction = field(default_factory=SatelliteReproduction)
    collapse_endings: BinaryCollapseEndings = field(default_factory=BinaryCollapseEndings)
    anti_entropy: AntiEntropyOptimal = field(default_factory=AntiEntropyOptimal)

    def get_five_theorems(self) -> List[str]:
        """获取五大定理名称"""
        return [
            self.hierarchy.name,
            self.three_poles.name,
            self.entropy_delay.name,
            self.reproduction.name,
            self.anti_entropy.name,
        ]

    def simulate_binary_vs_isolated(self, delta_E: float = 100.0,
                                     E_out: float = 30.0,
                                     k_in: float = 0.1,
                                     k_tide: float = 0.05,
                                     E_tide: float = 20.0,
                                     k_out: float = 0.03,
                                     k_res: float = 0.02) -> Dict:
        """对比模拟：孤立行星 vs 双星系统"""
        # 孤立行星
        iso_E_res = self.entropy_delay.calc_isolated_E_res(delta_E, E_out)
        iso_dS = self.entropy_delay.calc_dS_dt(k_in, delta_E, 0, 0, k_out, E_out, k_res, iso_E_res)

        # 双星系统
        bin_E_res = self.entropy_delay.calc_binary_E_res(delta_E, E_out)
        bin_dS = self.entropy_delay.calc_dS_dt(k_in, delta_E, k_tide, E_tide, k_out, E_out, k_res, bin_E_res)

        # 寿命延长因子
        lifetime_factor = self.entropy_delay.calc_lifetime_extension_factor()

        # 结局判定
        iso_ending = self.collapse_endings.classify_ending(iso_E_res / delta_E)
        bin_ending = self.collapse_endings.classify_ending(bin_E_res / delta_E)

        return {
            "孤立行星": {
                "淤积熵E_res": round(iso_E_res, 2),
                "淤积比E_res/ΔE": round(iso_E_res / delta_E, 3),
                "展开度变化率dS/dt": round(iso_dS, 4),
                "状态判定": iso_ending,
            },
            "双星系统（行星侧）": {
                "淤积熵E_res": round(bin_E_res, 2),
                "淤积比E_res/ΔE": round(bin_E_res / delta_E, 3),
                "展开度变化率dS/dt": round(bin_dS, 4),
                "状态判定": bin_ending,
            },
            "对比结论": {
                "熵分流效果": f"淤积熵减少{round((iso_E_res - bin_E_res) / iso_E_res * 100, 1)}%",
                "展开度提升": f"dS/dt提升{round((bin_dS - iso_dS) / abs(iso_dS) * 100, 1)}%" if iso_dS != 0 else "N/A",
                "寿命延长因子": f"≈{lifetime_factor}倍",
            },
            "三级谱系": self.hierarchy.get_three_tier_lineage(),
        }

    def get_complete_summary(self) -> Dict:
        """获取完整总览"""
        return {
            "模块编号": self.module_id,
            "模块名称": self.module_name,
            "副标题": self.subtitle,
            "版本": self.version,
            "归属层级": self.level,
            "类别": self.category,
            "依赖模块": self.dependencies,
            "五大定理": self.get_five_theorems(),
            "三级层级": "恒星（一级）→行星（二级）→卫星（三级）",
            "三组对冲": ["天道↔强化（顶层双轨约束）", "变身↔具现（潮汐激活中层）", "社会↔自然（引力制衡底层）"],
            "核心机制": ["熵分流", "潮汐补能", "动量分摊"],
            "双繁衍机制": ["无性（星云吸积）", "有性（撞击重组）"],
            "三种崩塌结局": ["中层矿化（中子星级）", "底层僵化（白矮星级）", "顶层坍缩（0元纳熵态）"],
            "核心推论": self.anti_entropy.core_proposition,
            "演化链条": self.anti_entropy.evolution_chain,
            "理论地位": "天体六系动力学扩展·三级繁衍谱系闭环·低阶界域抗熵最优解",
        }

    # ===== 守卫校验 =====
    def validate(self) -> Tuple[bool, List[str]]:
        """守卫校验：验证模型的一致性与正确性"""
        errors = []

        # 1. 五大定理数量校验
        if len(self.get_five_theorems()) != 5:
            errors.append(f"五大定理数量应为5，实际为{len(self.get_five_theorems())}")

        # 2. 四级层级校验
        if len(self.hierarchy.hierarchy) != 4:
            errors.append(f"层级数应为4，实际为{len(self.hierarchy.hierarchy)}")

        # 3. 三组对冲校验
        layers = self.three_poles.get_all_three_layers()
        if len(layers) != 3:
            errors.append(f"三组对冲层数应为3，实际为{len(layers)}")

        # 4. 熵分流计算校验
        iso_E = self.entropy_delay.calc_isolated_E_res(100, 30)
        if abs(iso_E - 70) > 0.001:
            errors.append(f"孤立行星熵计算错误：预期70，实际{iso_E}")

        bin_E = self.entropy_delay.calc_binary_E_res(100, 30, 0.5)
        if abs(bin_E - 20) > 0.001:
            errors.append(f"双星系统熵计算错误：预期20，实际{bin_E}")

        # 5. 动态微分方程校验
        dS = self.entropy_delay.calc_dS_dt(0.1, 100, 0.05, 20, 0.03, 30, 0.02, 20)
        expected = 0.1*100 + 0.05*20 - 0.03*30 - 0.02*20  # 10 + 1 - 0.9 - 0.4 = 9.7
        if abs(dS - expected) > 0.001:
            errors.append(f"动态微分方程计算错误：预期{expected}，实际{dS}")

        # 6. 寿命延长因子校验
        factor = self.entropy_delay.calc_lifetime_extension_factor()
        if abs(factor - 3.0) > 0.001:
            errors.append(f"寿命延长因子错误：预期3.0，实际{factor}")

        # 7. 三种崩塌结局校验
        if len(self.collapse_endings.three_endings) != 3:
            errors.append(f"崩塌结局数应为3，实际为{len(self.collapse_endings.three_endings)}")

        # 8. 结局分类校验
        if "活跃期" not in self.collapse_endings.classify_ending(0.3):
            errors.append("结局分类错误：E_res=0.3应为活跃期")
        if "中层崩溃" not in self.collapse_endings.classify_ending(0.5):
            errors.append("结局分类错误：E_res=0.5应为中层崩溃")
        if "底层崩溃" not in self.collapse_endings.classify_ending(0.8):
            errors.append("结局分类错误：E_res=0.8应为底层崩溃")
        if "顶层全域坍缩" not in self.collapse_endings.classify_ending(0.99):
            errors.append("结局分类错误：E_res=0.99应为顶层坍缩")

        # 9. 抗熵最优解五大论点校验
        if len(self.anti_entropy.five_points) != 5:
            errors.append(f"抗熵最优解论点应为5条，实际为{len(self.anti_entropy.five_points)}")

        # 10. 演化链条长度校验
        if len(self.anti_entropy.evolution_chain) != 4:
            errors.append(f"演化链条长度应为4，实际为{len(self.anti_entropy.evolution_chain)}")

        is_valid = len(errors) == 0
        return is_valid, errors


# ============================================================
# 八、快速查询接口
# ============================================================

def get_binary_module() -> BinarySystemModule:
    """获取行星—卫星双星系统模块实例"""
    return BinarySystemModule()


def quick_binary_vs_isolated(delta_E: float = 100.0, E_out: float = 30.0) -> str:
    """快速查询：孤立行星 vs 双星系统熵淤积对比"""
    module = get_binary_module()
    iso_E = module.entropy_delay.calc_isolated_E_res(delta_E, E_out)
    bin_E = module.entropy_delay.calc_binary_E_res(delta_E, E_out)
    reduction = (iso_E - bin_E) / iso_E * 100
    return f"ΔE={delta_E}, E_out={E_out} → 孤立行星E_res={iso_E:.1f}，双星系统E_res={bin_E:.1f}，熵减少{reduction:.1f}%"


def quick_binary_ending_query(E_res_ratio: float) -> str:
    """快速查询：根据淤积熵比判定双星系统结局"""
    module = get_binary_module()
    return f"淤积熵比 E_res={E_res_ratio:.2f} → {module.collapse_endings.classify_ending(E_res_ratio)}"


def quick_three_tier_lineage() -> str:
    """快速查询：三级嵌套繁衍谱系"""
    module = get_binary_module()
    return f"三级繁衍谱系：{module.hierarchy.get_three_tier_lineage()}"


# ============================================================
# 九、自测入口
# ============================================================

def _run_self_test():
    """运行自测"""
    print("=" * 70)
    print("  T54 —— 行星—卫星双星系统六系统一模型")
    print("  【双体共生·熵淤积延缓·三级繁衍谱系·低阶界域抗熵最优解】")
    print("=" * 70)

    module = get_binary_module()

    # 测试1：层级定位
    print("\n【测试1】双星系统整体定位（四级层级）")
    for level_num, info in module.hierarchy.hierarchy.items():
        print(f"  {info['层级']}: {info['类型']}（{info['定位']}）")
    print(f"  核心优势: {module.hierarchy.core_advantage[:50]}...")

    # 测试2：三组对冲
    print("\n【测试2】双星系统三组对冲")
    layers = module.three_poles.get_all_three_layers()
    for layer_name, layer_info in layers.items():
        print(f"  {layer_name}:")
        for k, v in layer_info.items():
            if isinstance(v, dict):
                print(f"    {k}: {list(v.keys())}")
            else:
                print(f"    {k}: {str(v)[:40]}...")

    # 测试3：熵分流量化
    print("\n【测试3】熵淤积延缓机制（量化模型）")
    delta_E, E_out = 100.0, 30.0
    iso_E = module.entropy_delay.calc_isolated_E_res(delta_E, E_out)
    bin_E = module.entropy_delay.calc_binary_E_res(delta_E, E_out)
    print(f"  孤立行星: E_res = {delta_E:.0f} - {E_out:.0f} = {iso_E:.1f}")
    print(f"  双星系统: E_res = {delta_E:.0f}/2 - {E_out:.0f} = {bin_E:.1f}")
    print(f"  熵减少: {(iso_E - bin_E) / iso_E * 100:.1f}%")

    # 测试4：动态微分方程
    print("\n【测试4】六系展开度动态方程")
    dS = module.entropy_delay.calc_dS_dt(0.1, 100, 0.05, 20, 0.03, 30, 0.02, 20)
    print(f"  dS/dt = 0.1×100 + 0.05×20 - 0.03×30 - 0.02×20 = {dS:.2f}")
    print(f"  寿命延长因子: ≈{module.entropy_delay.calc_lifetime_extension_factor():.1f}倍")

    # 测试5：三种灾害延后
    print("\n【测试5】三种灾害延后效果")
    for i, disaster in module.entropy_delay.disaster_delay.items():
        print(f"  {i}. {disaster['灾害类型']}: {disaster['延缓效果'][:30]}...")

    # 测试6：卫星繁衍机制
    print("\n【测试6】卫星作为行星子代：繁衍遗传机制")
    print(f"  无性繁衍: {module.reproduction.asexual['名称']}")
    print(f"  有性繁衍: {module.reproduction.sexual['名称']}")
    print(f"  公式: {module.reproduction.sexual['公式']}")
    print(f"  谱系闭环:")
    for line in module.reproduction.lineage_complete:
        print(f"    {line}")

    # 测试7：三种崩塌归宿
    print("\n【测试7】双星系统三种崩塌归宿")
    for i, ending in module.collapse_endings.three_endings.items():
        interval = ending["阈值区间"]
        print(f"  {i}. {ending['类型']} [{interval[0]:.2f}, {interval[1]:.2f}) → {ending['对应层级']}")

    # 分类测试
    test_E = [0.2, 0.5, 0.8, 0.99]
    print(f"\n  结局分类测试:")
    for e in test_E:
        result = module.collapse_endings.classify_ending(e)
        print(f"    E_res={e:.2f} → {result}")

    # 测试8：抗熵最优解
    print("\n【测试8】关键推论：双体共生是低阶界域抗熵最优解")
    for i, point in module.anti_entropy.five_points.items():
        print(f"  {i}. {point[:50]}...")
    print(f"\n  演化链条:")
    for step in module.anti_entropy.evolution_chain:
        print(f"    → {step}")

    # 测试9：对比模拟
    print("\n【测试9】孤立行星 vs 双星系统 对比模拟")
    sim = module.simulate_binary_vs_isolated()
    for system, data in sim.items():
        if isinstance(data, dict):
            print(f"  【{system}】")
            for k, v in data.items():
                print(f"    {k}: {v}")
        else:
            print(f"  {system}: {data}")

    # 测试10：完整总览
    print("\n【测试10】完整总览")
    summary = module.get_complete_summary()
    for k, v in summary.items():
        if isinstance(v, list):
            print(f"  {k}: {v}")
        else:
            print(f"  {k}: {v}")

    # 测试11：守卫校验
    print("\n【测试11】守卫校验")
    is_valid, errors = module.validate()
    if is_valid:
        print("  校验结果: ✓ 通过")
    else:
        print("  校验结果: ✗ 失败")
        for e in errors:
            print(f"    - {e}")

    # 测试12：快速查询
    print("\n【测试12】快速查询")
    print(f"  {quick_binary_vs_isolated()}")
    print(f"  {quick_binary_ending_query(0.85)}")
    print(f"  {quick_three_tier_lineage()}")

    print("\n" + "=" * 70)
    print("  T54行星—卫星双星系统六系统一模型验证完成!")
    print("  【5大定理·双体共生·熵分流·三级谱系·抗熵最优解】")
    print("=" * 70)


if __name__ == "__main__":
    _run_self_test()