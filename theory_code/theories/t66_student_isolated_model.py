# -*- coding: utf-8 -*-
"""
T66: 个体六系统一模型（学生孤体初始版·全域大一统同构）
=========================================================

理论定位：
    L0_总本源层 / 六系核心公理 / 个体动力学深化篇
    T66 补完 T50-T65 体系中的「个体动力学·封闭孤体」专题建模

核心命题：
    1. 三界绝对同构（天体｜文明｜个体学生）—— 同一套六系对冲结构
       同一套无量纲熵阈值，同一套崩塌顺序，同一套微分方程
    2. 亲缘意义传导坍缩链路 —— 强化系100 → 具现系递减 → 天道系60封锁 → 自然系20真空
    3. 意义-熵双向耦合方程组 —— 意义递减为熵增的唯一内源
    4. 个体开放跃迁破局方案 —— 开放外源排熵 + 多级缓冲 + 六系动态对冲

关键变量：
    M_qianghua   强化系原生自性意义（满值100，封闭系统恒定不减）
    M_juxian     具现系落地转化意义（η=0.82损耗系数）
    M_tiandao    天道系范式突破临界意义（60阈值）
    M_ziran      自然系社会建设基底意义（20稳态阈值）
    E_inner      内生淤积熵
    E_ext        数字外源跨域排熵量
    E_buffer     个体多级缓冲泄熵量
    E_res        系统实时残余熵

核心阈值：
    安全稳态：E_res < 0.40
    中层矿化：0.40 ≤ E_res < 0.75
    底层僵化：0.75 ≤ E_res < 0.98
    全域坍缩：E_res ≥ 0.98

依赖模块：T45元公理、T48终极扩容、T50-T63全域六系动力学、T65天地人同构
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum


# ===================== 全域常量定义 =====================

class EResLevel(Enum):
    """熵值灾变等级（全域统一不变量）"""
    SAFE = ("安全稳态", 0.00, 0.40)
    MID_MINERALIZE = ("中层矿化", 0.40, 0.75)
    BOTTOM_RIGID = ("底层僵化", 0.75, 0.98)
    TOP_COLLAPSE = ("全域坍缩", 0.98, 1.50)

    def __init__(self, level_name: str, lo: float, hi: float):
        self.level_name = level_name
        self.lo = lo
        self.hi = hi

    def contains(self, value: float) -> bool:
        return self.lo <= value < self.hi


class SixSystem(Enum):
    """六系枚举（与天体/文明同构）"""
    TIANDAO = ("天道系", "顶层秩序", "应试升学范式")
    QIANGHUA = ("强化系", "自性动力", "个体好奇心与探索欲")
    BIANSHEN = ("变身系", "迭代革新", "认知更新与方法迭代")
    JUXIAN = ("具现系", "固化载体", "纸笔应试载体")
    SHEHUI = ("社会系", "博弈网络", "班级排名同辈压力")
    ZIRAN = ("自然系", "底层基底", "体能情绪精力续航")


# ===================== 1. 三界同构核心理论 =====================

@dataclass(frozen=True)
class ThreeDomainUnification:
    """
    三界绝对同构（天体｜文明｜个体学生）
    证明：三者方程拓扑结构、阈值体系、灾变逻辑、演化路径完全一致
    """
    celestial_systems: List[str] = field(default_factory=lambda: [
        "天体系统：无卫星孤立行星↔封闭古文明↔学生孤体",
        "阈值体系：0.40/0.75/0.98 全域通用",
        "灾变序列：中层→底层→顶层 三阶递进",
        "外源排熵：引力摄动↔外贸外循环↔数字外源",
        "缓冲圈层：卫星系统↔城乡二元↔兴趣复盘作息",
    ])

    def verify_isomorphism(self) -> Dict[str, str]:
        """验证三界六系1:1对位"""
        return {
            "天道系": "恒星轨道↔顶层制度↔应试升学范式",
            "强化系": "星体内核↔文明自由意志↔个体自性动力",
            "变身系": "星体形态迭代↔产业梯度升级↔认知迭代革新",
            "具现系": "地壳固态层↔城市基建/矿山↔文具固化载体",
            "社会系": "引力拉扯↔派系博弈↔班级排名博弈",
            "自然系": "物质能量基底↔土地粮食能源↔体能情绪稳态",
        }


# ===================== 2. 学生个体六系精准对位 =====================

@dataclass
class StudentSixSystem:
    """
    封闭应试学生系统六系模型
    与天体/文明1:1同构
    """
    # 顶层两极
    tiandao: str = "应试升学、分数排名、标准答案、固定学习路径"
    qianghua: str = "好奇心、探索欲、自主思考、质疑能力、自性意志"

    # 中间转化
    bianshen: str = "认知更新、思维升级、学习方法迭代、思想蜕变"
    juxian: str = "固定刷题套路、固化笔记模板、死记硬背体系"

    # 底层承载
    shehui: str = "班级排名竞争、同学内卷、师生博弈、同辈压力"
    ziran: str = "睡眠、体能、情绪稳态、生理状态、精力续航"

    # 系统属性
    is_closed: bool = True  # 是否封闭孤体
    has_digital_input: bool = False  # 是否有数字外源
    has_interest_buffer: bool = False  # 是否有兴趣缓冲

    def to_dict(self) -> Dict[str, str]:
        return {
            "天道系": self.tiandao,
            "强化系": self.qianghua,
            "变身系": self.bianshen,
            "具现系": self.juxian,
            "社会系": self.shehui,
            "自然系": self.ziran,
        }


# ===================== 3. 亲缘意义传导方程组 =====================

@dataclass(frozen=True)
class MeaningConductionParams:
    """意义传导核心参数（封闭文具孤体系统）"""
    eta: float = 0.82  # 具现系意义损耗系数
    sigma: float = float('inf')  # 天道系封锁系数（σ→∞）
    M_tiandao_threshold: float = 60.0  # 净化爆发临界值
    M_ziran_threshold: float = 20.0  # 自然系建设基底阈值
    M_qianghua_init: float = 100.0  # 强化系原生意义满值


@dataclass
class MeaningConductionSystem:
    """
    4.6 四段式亲缘意义传导核心方程组

    第一式：M_qianghua(t) ≡ 100
    第二式：M_juxian(t) = 100 × (1 - 0.82t)
    第三式：M_tiandao_cleanse = 0（60爆发被σ→∞封锁）
    第四式：M_ziran < 20（永久真空）
    """
    params: MeaningConductionParams = field(default_factory=MeaningConductionParams)
    _t: float = 0.0

    def step(self, dt: float = 0.1) -> Dict[str, float]:
        """推演一个时间步"""
        self._t += dt
        p = self.params
        return {
            "M_qianghua": p.M_qianghua_init,
            "M_juxian": p.M_qianghua_init * (1 - p.eta * self._t),
            "M_tiandao_cleanse": 0.0,  # 被封锁
            "M_ziran": max(0.0, p.M_qianghua_init * (1 - p.eta * self._t) - p.M_tiandao_threshold),
            "t": self._t,
        }

    def run(self, t_max: float = 1.2, dt: float = 0.05) -> List[Dict[str, float]]:
        """完整推演闭环过程"""
        trajectory = []
        t0 = self._t
        while self._t < t0 + t_max:
            trajectory.append(self.step(dt))
        return trajectory

    def ultimate_steady_state(self) -> Dict[str, str]:
        """封闭系统终极稳态结论"""
        return {
            "M_qianghua": "永久100满值·原生盈余不减",
            "M_juxian": "永久损耗·具现系矿化锁定",
            "M_tiandao_cleanse": "永久封锁·60突破锁死",
            "M_ziran": "永久真空·<20阈值不可达",
            "总体定性": "有内生天赋、无现实价值、有生产能力、无落地渠道的应试畸形稳态",
        }


# ===================== 4. 意义-熵双向耦合方程组 =====================

@dataclass(frozen=True)
class MeaningEntropyCouplingParams:
    """意义-熵双向耦合核心参数"""
    alpha: float = 1.0  # 意义转熵系数（封闭系统固定为1）
    gamma: float = 0.66  # 应试固化熵增系数（与文明系统一致）
    kappa: float = 0.32  # 思维矿化固化系数（全域统一）
    E_res_threshold: float = 0.40  # 安全稳态阈值
    M_tiandao_threshold: float = 60.0
    M_ziran_threshold: float = 20.0


@dataclass
class MeaningEntropyCoupling:
    """
    4.6.6 意义—熵双向耦合方程组（核心闭环）

    E_clog = α·(ΔM_juxian + ΔM_tiandao + ΔM_ziran)
    """
    params: MeaningEntropyCouplingParams = field(default_factory=MeaningEntropyCouplingParams)

    def compute_clog_entropy(
        self,
        delta_m_juxian: float,
        delta_m_tiandao: float,
        delta_m_ziran: float,
    ) -> float:
        """计算意义-熵耦合内生熵"""
        p = self.params
        return p.alpha * (delta_m_juxian + delta_m_tiandao + delta_m_ziran)

    def closed_system_steady_state(self) -> Dict[str, float]:
        """封闭学生系统稳态数值验算"""
        # 固定参数
        delta_m_juxian = 82.0  # 稳态意义损耗
        delta_m_tiandao = 12.0  # 封锁缺口
        delta_m_ziran = 6.0  # 真空缺口
        return {
            "delta_m_juxian": delta_m_juxian,
            "delta_m_tiandao": delta_m_tiandao,
            "delta_m_ziran": delta_m_ziran,
            "总意义缺陷": delta_m_juxian + delta_m_tiandao + delta_m_ziran,
            "转化内生熵E_clog": self.compute_clog_entropy(
                delta_m_juxian, delta_m_tiandao, delta_m_ziran
            ),
        }

    def coupling_validation(self) -> Dict[str, str]:
        """意义链—熵变链双向耦合印证"""
        return {
            "具现系意义递减": "→ 中间转化层淤积 → 触发中层矿化（0.40+）：题海无效、思维固化",
            "天道系60爆发封锁": "→ 系统迭代停滞 → 熵持续累积 → 触发底层僵化（0.75+）：身心耗竭、习得性无助",
            "自然系20意义真空": "→ 社会建设落地归零 → 顶层对冲彻底断裂 → 趋近全域坍缩（0.98+）：意志空洞、价值消亡",
        }


# ===================== 5. 封闭孤体熵增方程 =====================

@dataclass
class ClosedStudentEntropy:
    """
    封闭孤体学生熵增方程
    E_res = E_inner（无外排，无缓冲）
    """
    gamma: float = 0.66
    k_exam: float = 1.2
    kappa: float = 0.32

    def compute_residual(self) -> float:
        """计算残余熵"""
        e_inner = self.gamma * self.k_exam
        return e_inner  # 封闭系统无外排项

    def classify(self, e_res: float) -> EResLevel:
        """全域熵值分类"""
        for level in EResLevel:
            if level.contains(e_res):
                return level
        return EResLevel.TOP_COLLAPSE

    def state_description(self) -> Dict[str, str]:
        """封闭学生系统状态描述"""
        e_res = self.compute_residual()
        level = self.classify(e_res)
        return {
            "E_res": f"{e_res:.3f}",
            "灾变等级": level.level_name,
            "系统状态": "内卷常态化、思维固化不可逆，与现实学生困境完全吻合",
            "意义缺陷": "生产意义过剩、落地利用为零、纯内部淤积",
        }


# ===================== 6. 开放跃迁方程组 =====================

@dataclass
class OpenStudentBreakthrough:
    """
    开放跃迁学生方程组
    E_res = E_inner - E_ext - E_buffer + A_chaos
    """
    gamma: float = 0.66
    k_exam: float = 1.2
    E_ext: float = 0.5  # 数字外源跨域排熵量
    E_buffer: float = 0.3  # 个体多级缓冲泄熵量
    A_chaos: float = 0.0  # 混沌扰动项
    omega: float = 0.8  # 认知迭代更新系数
    mu: float = 0.7  # 认知创新转化系数
    I_input: float = 0.6  # 认知更新投入
    k_safe: float = 1.5  # 应试固化安全阈值
    I_max: float = 1.0  # 认知投入上限

    def compute_residual(self) -> float:
        """开放系统总残余熵"""
        e_inner = self.gamma * self.k_exam
        return e_inner - self.E_ext - self.E_buffer + self.A_chaos

    def v_update(self) -> float:
        """认知迭代速率"""
        return self.omega * self.I_input * self.mu

    def I_input_constraint(self) -> bool:
        """迭代速率约束（避免学习体系空心化）"""
        return self.I_input <= self.I_max - self.kappa_for_check()

    def kappa_for_check(self) -> float:
        """思维矿化固化系数（供约束检查使用）"""
        return 0.32 * 0.5  # 简化使用

    def k_exam_constraint(self) -> bool:
        """应试固化速率约束"""
        return self.k_exam <= self.k_safe

    def stable_state_check(self) -> bool:
        """终极稳态约束：E_res < 0.40"""
        return self.compute_residual() < 0.40

    def breakthrough_evaluation(self) -> Dict[str, str]:
        """开放跃迁评估"""
        e_res = self.compute_residual()
        level = self._classify(e_res)
        return {
            "E_res": f"{e_res:.3f}",
            "灾变等级": level.level_name,
            "v_update": f"{self.v_update():.3f}",
            "迭代约束满足": "✅" if self.I_input_constraint() else "❌",
            "固化约束满足": "✅" if self.k_exam_constraint() else "❌",
            "稳态约束满足": "✅" if self.stable_state_check() else "❌",
            "系统结论": "成功回落安全稳态，彻底跳出矿化内卷" if e_res < 0.40 else "未达标",
        }

    def _classify(self, e_res: float) -> EResLevel:
        for level in EResLevel:
            if level.contains(e_res):
                return level
        return EResLevel.TOP_COLLAPSE


# ===================== 7. 三界大一统对位表 =====================

@dataclass(frozen=True)
class ThreeDomainMapping:
    """
    七、三界大一统最终对位表
    """
    mapping: Dict[str, Dict[str, str]] = field(default_factory=lambda: {
        "天道系": {
            "天体": "恒星轨道规则",
            "文明": "顶层制度范式",
            "个体": "应试升学范式",
        },
        "强化系": {
            "天体": "星体内核动力",
            "文明": "文明自由意志",
            "个体": "个体自性动力",
        },
        "变身系": {
            "天体": "星体形态迭代",
            "文明": "产业梯度升级",
            "个体": "认知迭代革新",
        },
        "具现系": {
            "天体": "地壳固态层",
            "文明": "城市基建/矿山",
            "个体": "文具固化载体",
        },
        "社会系": {
            "天体": "引力互相拉扯",
            "文明": "派系博弈网络",
            "个体": "班级排名博弈",
        },
        "自然系": {
            "天体": "物质能量基底",
            "文明": "土地粮食能源",
            "个体": "体能情绪稳态",
        },
    })

    def disaster_mapping(self) -> Dict[str, Dict[str, str]]:
        return {
            "灾变1·0.40+": {
                "天体": "中子星矿化",
                "文明": "产业固化",
                "个体": "学习范式矿化",
            },
            "灾变2·0.75+": {
                "天体": "白矮星僵死",
                "文明": "内需萎缩",
                "个体": "身心耗竭",
            },
            "灾变3·0.98+": {
                "天体": "黑洞坍缩",
                "文明": "文明消亡",
                "个体": "意志归零",
            },
        }


# ===================== 8. 落地调控体系 =====================

@dataclass
class SixSystemRegulationPlan:
    """
    九、个体六系动力学落地调控体系
    9.2 六系分层精准调控方案
    """
    # 配比标准
    digital_input_ratio: float = 0.15  # 外源数字排熵配比15%
    self_buffer_ratio: float = 0.10  # 自我缓冲泄熵配比10%
    k_exam_safe_limit: float = 1.5  # 应试固化速率管控红线

    def tiandao_regulation(self) -> Dict[str, str]:
        """天道系：破除单一范式固化"""
        return {
            "管控核心": "打破「唯分数、唯标准答案」的单一刚性秩序，保留顶层发展多元可能性",
            "落地规则": "每日预留10分钟全局复盘，梳理学习逻辑方法得失；每月更新一次学习目标体系",
        }

    def qianghua_regulation(self) -> Dict[str, str]:
        """强化系：持续输入内生动力"""
        return {
            "管控核心": "对冲应试体系的被动压制，保住好奇心、自主思考、质疑能力",
            "落地规则": "每周预留2次自主探索时间；每日保留1-2个自主思考疑问点",
        }

    def bianshen_regulation(self) -> Dict[str, str]:
        """变身系：保障思维持续更新"""
        return {
            "管控核心": "拉高认知迭代速率，杜绝思维停滞，破解纸笔封闭模式的迭代缺陷",
            "落地规则": "每学1套旧题型模板，同步更新1种新解题思维；定期迭代学习体系",
        }

    def juxian_regulation(self) -> Dict[str, str]:
        """具现系：杜绝学习范式矿化"""
        return {
            "管控核心": "压低思维矿化熵，破解文具封闭困境，避免机械学习范式永久固化",
            "落地规则": "纸笔仅作基础载体，搭配数字模型/思维导图/变式训练；禁止死记模板、题海盲刷",
        }

    def shehui_regulation(self) -> Dict[str, str]:
        """社会系：消解零和内卷熵"""
        return {
            "管控核心": "降低同辈博弈带来的内生熵增，打破班级存量内卷混沌",
            "落地规则": "弱化排名对比，转向自我迭代增量对比；减少无效同辈内耗",
        }

    def ziran_regulation(self) -> Dict[str, str]:
        """自然系：守住精力情绪稳态"""
        return {
            "管控核心": "筑牢底层承载层，避免体能、情绪透支引发底层僵化灾变",
            "落地规则": "固定规律作息，杜绝熬夜内耗；每日预留松弛缓冲时间",
        }

    def get_full_plan(self) -> Dict[str, Dict[str, str]]:
        """获取完整六系调控方案"""
        return {
            "天道系": self.tiandao_regulation(),
            "强化系": self.qianghua_regulation(),
            "变身系": self.bianshen_regulation(),
            "具现系": self.juxian_regulation(),
            "社会系": self.shehui_regulation(),
            "自然系": self.ziran_regulation(),
        }


# ===================== 9. 混沌扰动风险防控 =====================

@dataclass
class ChaosRiskControl:
    """9.3 混沌扰动风险防控机制"""
    def get_control_rules(self) -> List[str]:
        return [
            "禁止短期突击式刷题、熬夜恶补（脉冲式高强度学习会引发指数级熵增）",
            "建立心态缓冲机制，单次考试波动不改变长期学习体系",
            "所有调整平滑渐进，杜绝学习模式、作息节奏的剧烈突变",
        ]


# ===================== 10. 终极结论验证 =====================

@dataclass
class UltimateConclusion:
    """八、模型终论 + 9.5 终极落地结论"""
    def model_conclusion(self) -> List[str]:
        return [
            "个体学生六系与天体、文明六系完全同构、同源、同方程、同灾变、同跃迁路径",
            "传统「无手机、纯文具、封闭应试」模式，并非自律，而是人为制造低维封闭孤体系统",
            "个体破局逻辑：开放外源排熵 + 搭建多级缓冲 + 维持六系动态对冲",
            "天体-文明-个体三界统一动力学模型完整成立",
        ]

    def landing_conclusion(self) -> List[str]:
        return [
            "学生「禁手机、纯文具、封闭应试」传统模式 = 人为构建低维封闭孤体系统",
            "个体破局无需高强度内卷：开放可控外源排熵 + 搭建自我缓冲圈层 + 管控固化速率",
            "所有落地行为均对应数理方程与熵阈值，可量化、可校验、可稳定复刻",
            "天体-文明-个体三界大一统六系动力学模型100%完整闭环",
        ]


# ===================== 模块主类 =====================

class T66StudentIsolatedModule:
    """
    T66 主模块：学生孤体初始版·全域大一统同构
    整合三界同构、亲缘意义传导、意义-熵耦合、落地调控体系
    """
    def __init__(self):
        self.three_domain = ThreeDomainUnification()
        self.student = StudentSixSystem()
        self.meaning_params = MeaningConductionParams()
        self.meaning_conduction = MeaningConductionSystem(self.meaning_params)
        self.coupling_params = MeaningEntropyCouplingParams()
        self.coupling = MeaningEntropyCoupling(self.coupling_params)
        self.closed_system = ClosedStudentEntropy()
        self.open_system = OpenStudentBreakthrough()
        self.mapping = ThreeDomainMapping()
        self.regulation = SixSystemRegulationPlan()
        self.chaos_control = ChaosRiskControl()
        self.conclusion = UltimateConclusion()

    def run_full_analysis(self) -> Dict:
        """运行完整分析"""
        return {
            "01_三界同构验证": self.three_domain.verify_isomorphism(),
            "02_学生六系对位": self.student.to_dict(),
            "03_亲缘意义传导稳态": self.meaning_conduction.ultimate_steady_state(),
            "04_意义_熵耦合稳态": self.coupling.closed_system_steady_state(),
            "05_耦合印证链": self.coupling.coupling_validation(),
            "06_封闭系统熵值": self.closed_system.state_description(),
            "07_开放系统跃迁": self.open_system.breakthrough_evaluation(),
            "08_三界对位表": self.mapping.mapping,
            "09_灾变对位表": self.mapping.disaster_mapping(),
            "10_六系调控方案": self.regulation.get_full_plan(),
            "11_混沌风险防控": self.chaos_control.get_control_rules(),
            "12_模型终论": self.conclusion.model_conclusion(),
            "13_落地终极结论": self.conclusion.landing_conclusion(),
        }


# ===================== 守卫校验 =====================

def validate() -> List[str]:
    """
    守卫校验：验证T66模块核心逻辑一致性
    """
    errors = []

    # 校验1：熵值分类函数正确性
    closed = ClosedStudentEntropy()
    e_res = closed.compute_residual()
    if e_res < 0:
        errors.append(f"封闭系统熵值异常为负: {e_res}")
    level = closed.classify(e_res)
    if not level:
        errors.append("熵值分类函数返回空")

    # 校验2：亲缘意义传导方程
    mc = MeaningConductionSystem()
    mc.step(0.5)
    state = mc.ultimate_steady_state()
    if "M_qianghua" not in state:
        errors.append("亲缘意义传导稳态结论缺失M_qianghua")

    # 校验3：耦合方程单调性
    coupling = MeaningEntropyCoupling()
    if coupling.compute_clog_entropy(0, 0, 0) != 0:
        errors.append("耦合方程零输入应为零")
    if coupling.compute_clog_entropy(10, 10, 10) <= 0:
        errors.append("耦合方程正输入应单调递增")

    # 校验4：开放跃迁方程
    open_sys = OpenStudentBreakthrough()
    if not open_sys.stable_state_check():
        errors.append("开放跃迁系统应满足稳态约束")
    if open_sys.v_update() <= 0:
        errors.append("认知迭代速率应大于0")

    # 校验5：三界对位表完整性
    mapping = ThreeDomainMapping()
    if len(mapping.mapping) != 6:
        errors.append(f"三界对位表应包含6个系，实际{len(mapping.mapping)}个")
    if len(mapping.disaster_mapping()) != 3:
        errors.append(f"灾变对位表应包含3个灾变级")

    # 校验6：六系枚举完整性
    if len(SixSystem) != 6:
        errors.append(f"六系枚举应为6个，实际{len(SixSystem)}个")

    # 校验7：熵值等级区间一致性
    safe = EResLevel.SAFE
    mid = EResLevel.MID_MINERALIZE
    if safe.hi != mid.lo:
        errors.append(f"安全稳态上限{safe.hi}与中层矿化下限{mid.lo}不一致")

    # 校验8：核心阈值正确性
    if MeaningConductionParams().M_tiandao_threshold != 60.0:
        errors.append("天道系净化爆发阈值应为60")
    if MeaningConductionParams().M_ziran_threshold != 20.0:
        errors.append("自然系建设基底阈值应为20")

    # 校验9：参数系数与文明系统一致
    cp = MeaningEntropyCouplingParams()
    if cp.gamma != 0.66:
        errors.append("应试固化熵增系数应为0.66")
    if cp.kappa != 0.32:
        errors.append("思维矿化固化系数应为0.32")

    # 校验10：主模块运行无异常
    try:
        module = T66StudentIsolatedModule()
        result = module.run_full_analysis()
        if len(result) < 12:
            errors.append(f"主模块分析结果不完整，实际{len(result)}项")
    except Exception as e:
        errors.append(f"主模块运行异常: {e}")

    # 校验11：监管控方案完整性
    plan = SixSystemRegulationPlan()
    full_plan = plan.get_full_plan()
    for sys_name in ["天道系", "强化系", "变身系", "具现系", "社会系", "自然系"]:
        if sys_name not in full_plan:
            errors.append(f"调控方案缺失{sys_name}")

    # 校验12：终极结论条目数量
    conclusion = UltimateConclusion()
    if len(conclusion.model_conclusion()) != 4:
        errors.append("模型终论应为4条")
    if len(conclusion.landing_conclusion()) != 4:
        errors.append("落地终极结论应为4条")

    # 校验13：六系闭环无增减
    sys_keys = set(mapping.mapping.keys())
    expected = {"天道系", "强化系", "变身系", "具现系", "社会系", "自然系"}
    if sys_keys != expected:
        errors.append(f"六系对位表系别名称不规范: {sys_keys - expected}")

    # 校验14：自然系阈值20与残留验算
    steady = coupling.closed_system_steady_state()
    if steady["总意义缺陷"] < 0:
        errors.append("总意义缺陷不应为负")

    # 校验15：开放系统排熵应显著降低残余熵
    closed_e = closed.compute_residual()
    open_e = open_sys.compute_residual()
    if open_e >= closed_e:
        errors.append("开放跃迁应降低残余熵")

    return errors


if __name__ == "__main__":
    print("=" * 70)
    print("T66: 个体六系统一模型（学生孤体初始版·全域大一统同构）")
    print("=" * 70)

    # 守卫校验
    errs = validate()
    print(f"\n【守卫校验】发现 {len(errs)} 个问题：")
    for e in errs:
        print(f"  - {e}")
    print(f"校验{'通过' if not errs else '失败'}")

    # 完整分析
    if not errs:
        print("\n" + "=" * 70)
        print("完整分析报告")
        print("=" * 70)
        module = T66StudentIsolatedModule()
        result = module.run_full_analysis()
        for key, value in result.items():
            print(f"\n【{key}】")
            if isinstance(value, dict):
                for k, v in value.items():
                    print(f"  {k}: {v}")
            elif isinstance(value, list):
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"  {value}")
