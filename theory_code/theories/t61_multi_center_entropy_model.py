# -*- coding: utf-8 -*-
"""
T61 —— 多中心分布式城市群熵分流模型
【单点过载破解·N节点均分·四级网络架构·路径演化·政策约束】
归属层级：L0_总本源层
类别：天人同构动力学·文明系统优化实践篇
依赖模块：T45, T48, T51, T54, T55, T56, T57, T58, T59, T60

────────────────────────────────────────
核心公理基础（源自T50-T60）：
────────────────────────────────────────
• 动态熵流定理：E_res(t) = 0.22 + 0.66·x(t)
• 安全临界速度：x < 0.273
• 停滞临界速度：x ≈ 0.803
• 六系三层对冲：天道系↔强化系（顶层）、变身系↔具现系（中层）、社会系↔自然系（底层）
• 混沌熵暴增：E_res = 0.22 + 0.66·x(t) + A·e^(λt)

────────────────────────────────────────
本模块核心突破：
────────────────────────────────────────
单一中心城市是单点熵源，多中心分布式城市群把熵分散到N个次级节点，
每一个节点都拥有独立的产业承载与人口泄压能力，不存在单点突破临界阈值的风险。
"""

from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import sys
import os

# ───────────────────────────────────────
# 全局常数定义（沿用T60）
# ───────────────────────────────────────
C_CONSTANT = 0.22       # 常数项
ALPHA_CK = 0.66         # (α+ck)系数
X_CURRENT = 0.45        # 当前人口流入总量
X_SAFE_MAX = 0.273       # 安全临界速度

# ───────────────────────────────────────
# 核心定理类定义
# ───────────────────────────────────────

class MultiCenterEntropyFlow:
    """多中心分布式熵分流定理"""

    def __init__(self):
        self.core_equation = "E_res(i) = 0.22 + 0.66·x_i"
        self.description = (
            "多中心布局可以压低单个节点的人口集聚速度x_i，"
            "使所有节点的熵值全部控制在安全线以内。"
        )

    def calculate_node_entropy(self, x_i: float) -> float:
        """计算第i个节点的残余熵"""
        return C_CONSTANT + ALPHA_CK * x_i

    def calculate_average_entropy(self, X_total: float, N: int) -> float:
        """计算N节点均分后的平均熵"""
        if N <= 0:
            raise ValueError("节点数量N必须大于0")
        x_i = X_total / N
        return self.calculate_node_entropy(x_i)


class SingleNodeEntropyEquation:
    """单体城市熵方程"""

    @staticmethod
    def get(x_i: float) -> float:
        """单体城市熵方程：E_res(i) = C + (α+ck)x_i"""
        return C_CONSTANT + ALPHA_CK * x_i


class MultiCenterScenario:
    """多中心情景测算"""

    def __init__(self, X_total: float = X_CURRENT):
        self.X_total = X_total

    def scenario_n1(self) -> Dict:
        """情景1：单中心超大城市（当前模式）"""
        x = self.X_total
        E_res = C_CONSTANT + ALPHA_CK * x
        return {
            "nodes": 1,
            "x_i": x,
            "E_res": E_res,
            "status": self._classify_status(E_res),
            "description": "总人口流入全部集中在单一核心城市"
        }

    def scenario_n2(self) -> Dict:
        """情景2：双中心布局（主中心+副中心）"""
        N = 2
        x_i = self.X_total / N
        E_res = C_CONSTANT + ALPHA_CK * x_i
        return {
            "nodes": N,
            "x_i": x_i,
            "E_res": E_res,
            "status": self._classify_status(E_res),
            "description": "总流入人口平均拆分至两个节点"
        }

    def scenario_n4(self) -> Dict:
        """情景4：四中心分布式网络"""
        N = 4
        x_i = self.X_total / N
        E_res = C_CONSTANT + ALPHA_CK * x_i
        return {
            "nodes": N,
            "x_i": x_i,
            "E_res": E_res,
            "status": self._classify_status(E_res),
            "description": "总流入人口均分至四个节点"
        }

    def _classify_status(self, E_res: float) -> str:
        """熵值状态分类"""
        if E_res <= 0.40:
            return "安全稳态"
        elif E_res < 0.75:
            return "中层矿化警戒"
        elif E_res < 0.98:
            return "底层僵化红线"
        else:
            return "全域坍缩"


class FourLevelNetworkArchitecture:
    """四级网络完整架构"""

    # 最优均衡配比
    DISTRIBUTION_RATIOS = {
        1: {"name": "一级核心都市", "ratio": 0.20, "function": "高端产业、前沿创新、低熵新兴产业"},
        2: {"name": "二级副中心城市", "ratio": 0.35, "function": "承接制造业、中端产业、分担工业熵"},
        3: {"name": "三级县域中小城市", "ratio": 0.35, "function": "劳动密集型产业、农副加工、人口主要承载地"},
        4: {"name": "四级乡镇与乡村", "ratio": 0.10, "function": "终极兜底缓冲层、返乡人口承接"},
    }

    @classmethod
    def get_distribution(cls) -> List[Dict]:
        """获取四级网络分布"""
        return [
            {**{"level": k}, **v}
            for k, v in cls.DISTRIBUTION_RATIOS.items()
        ]

    @classmethod
    def get_summary(cls) -> str:
        """获取四级架构总结"""
        lines = ["【四级网络最优均衡配比】"]
        for level, info in cls.DISTRIBUTION_RATIOS.items():
            lines.append(
                f"  {level}. {info['name']}：承载人口{int(info['ratio']*100)}% "
                f"（{info['function']}）"
            )
        return "\n".join(lines)


class PathEvolutionAnalysis:
    """分路径长期演化推演"""

    PATH_A = {
        "name": "路径A：维持当前单中心大城市模式",
        "description": [
            "乡村缓冲层持续萎缩，E_out(rural)→0",
            "人口集聚速度长期维持x≈0.45，熵值稳定在0.517",
            "每十年熵值缓慢抬升0.04~0.06",
            "约20年左右逼近0.75底层僵化红线",
            "外部外贸波动叠加混沌扰动项，易引发熵暴增与社会矛盾集中爆发",
        ],
        "E_res": 0.22 + 0.66 * 0.45,
        "outcome": "内卷停滞，封闭轮回"
    }

    PATH_B = {
        "name": "路径B：建成双中心城市群",
        "description": [
            "熵值回落至0.368，长期稳定在安全区间",
            "产业分层迭代，主城区孵化新产业，次级城市承接实体产能",
            "中间转化层（变身—具现）不会出现矿化淤积",
            "城乡双向流动保持弹性",
        ],
        "E_res": 0.22 + 0.66 * (0.45 / 2),
        "outcome": "安全稳态，持续迭代"
    }

    PATH_C = {
        "name": "路径C：建成四级分布式多节点网络",
        "description": [
            "单点熵压低至0.30以下",
            "四级缓冲网络层层泄压",
            "即便外循环外贸出现剧烈波动，内部多级分流体系依然平稳消化冗余矛盾",
            "六系三层对冲长期均衡",
        ],
        "E_res": 0.22 + 0.66 * (0.45 / 4),
        "outcome": "深度稳态，持续跃迁"
    }

    @classmethod
    def get_all_paths(cls) -> List[Dict]:
        return [cls.PATH_A, cls.PATH_B, cls.PATH_C]

    @classmethod
    def get_summary(cls) -> str:
        lines = []
        for path in cls.get_all_paths():
            lines.append(f"【{path['name']}】")
            for desc in path['description']:
                lines.append(f"  • {desc}")
            lines.append(f"  → E_res={path['E_res']:.3f}，{path['outcome']}")
            lines.append("")
        return "\n".join(lines[:-1])  # 去掉最后空行


class SixSystemBalanceReview:
    """六系结构全域平衡复盘"""

    BALANCE = {
        "top_pole": {
            "systems": "天道系↔强化系（顶层两极）",
            "analysis": "多中心布局提供多元发展赛道，个体不必全部挤入一线大城市内卷，自由探索空间被保留，新生意义源源不断产出",
            "effect": "不会出现个体活力被宏观秩序全面压制"
        },
        "middle_transform": {
            "systems": "变身系↔具现系（中间转化层）",
            "analysis": "核心城市负责技术革新（变身系），次级城市承接实体产业（具现系），新旧产业有序梯度转移",
            "effect": "不动产不会垄断全部经济结构，有效避免产业矿山化淤积"
        },
        "bottom_bearing": {
            "systems": "社会系↔自然系（底层承载层）",
            "analysis": "人口分散在四级网络，生存矛盾不再高度集中于少数大城市，乡村保留兜底生存载体",
            "effect": "社会博弈网络多层分化，不会演化成单一节点的派系混沌"
        }
    }

    @classmethod
    def get_balance_summary(cls) -> str:
        lines = ["【六系结构全域平衡复盘】"]
        for key, info in cls.BALANCE.items():
            lines.append(f"\n  {info['systems']}")
            lines.append(f"    分析：{info['analysis']}")
            lines.append(f"    效果：{info['effect']}")
        return "\n".join(lines)


class DegeneracyRiskConstraint:
    """防止多中心再度演变为单中心（规避引力混沌）"""

    CONSTRAINTS = [
        {
            "id": 1,
            "title": "资源均衡分配约束",
            "description": "严格均衡分配教育、医疗、公共资源，避免优质资源全部集中于主核心",
            "risk": "资源过度集中→副中心空心化→人口回流主中心"
        },
        {
            "id": 2,
            "title": "产业严格分层约束",
            "description": "核心城市只搞前沿创新，低端产业必须外迁，禁止主城无序扩张",
            "risk": "产业同质竞争→副中心产业空洞化→集聚模式退化"
        },
        {
            "id": 3,
            "title": "土地财政管控约束",
            "description": "严控主城区土地财政无序扩张，避免房产红利持续虹吸人口",
            "risk": "土地财政依赖→核心城市扩张冲动→熵集中过载"
        },
        {
            "id": 4,
            "title": "县域产业独立约束",
            "description": "保持县域产业独立造血能力，防止中小城市沦为单纯的睡城",
            "risk": "睡城化→功能单一化→熵分流失效"
        }
    ]

    @classmethod
    def get_constraints(cls) -> List[Dict]:
        return cls.CONSTRAINTS

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【制度量化管控约束（防止多中心退化）】"]
        for c in cls.CONSTRAINTS:
            lines.append(
                f"  {c['id']}. {c['title']}：{c['description']}\n"
                f"     风险：{c['risk']}"
            )
        return "\n".join(lines)


class PolicyQuantConclusion:
    """终局量化结论"""

    CONCLUSIONS = [
        {
            "id": 1,
            "content": "人口单向流入核心大城市的安全增速上限x<0.273，当前实际增速超标，熵淤积已经进入中层矿化区间",
            "evidence": "x≈0.45, E_res≈0.517 > 0.40"
        },
        {
            "id": 2,
            "content": "构建双中心城市群，可将单节点熵值由0.517降至0.368，重回安全稳态",
            "evidence": "x_i=0.225, E_res=0.368 < 0.40"
        },
        {
            "id": 3,
            "content": "搭建「核心都市—副中心—县域—乡镇」四级分布式网络，能够把单点熵进一步压低至0.30以内",
            "evidence": "x_i=0.1125, E_res≈0.294 < 0.30"
        },
        {
            "id": 4,
            "content": "必须配套均衡化公共资源与产业分层管控，防止多中心再度退化为单极集聚",
            "evidence": "四大约束条件缺一不可"
        },
        {
            "id": 5,
            "content": "只有把熵分散到多级节点，保住城乡多级缓冲圈层，内外双循环相互配合，才能让文明六系动力学长期均衡",
            "evidence": "持续维持生长跃迁能力，避免走入内卷停滞的封闭轮回"
        }
    ]

    @classmethod
    def get_all(cls) -> List[Dict]:
        return cls.CONCLUSIONS

    @classmethod
    def get_summary(cls) -> str:
        lines = ["【终局量化结论】"]
        for c in cls.CONCLUSIONS:
            lines.append(f"  {c['id']}. {c['content']}")
        return "\n".join(lines)


# ───────────────────────────────────────
# 主模块类
# ───────────────────────────────────────

class T61MultiCenterDistributedEntropyModel:
    """T61多中心分布式城市群熵分流模型"""

    MODULE_INFO = {
        "module_id": "T61",
        "module_name": "多中心分布式城市群熵分流模型",
        "subtitle": "单点过载破解·N节点均分·四级网络架构·路径演化·政策约束",
        "version": "V1.0",
        "attribution_level": "L0_总本源层",
        "category": "天人同构动力学·文明系统优化实践篇",
        "dependencies": ["T45", "T48", "T51", "T54", "T55", "T56", "T57", "T58", "T59", "T60"],
        "core_theorems": [
            "多中心熵分流定理",
            "单体城市熵方程",
            "三级情景对比",
            "四级网络架构",
            "路径演化分析",
            "六系全域平衡",
            "制度约束管控",
            "终局量化结论"
        ],
        "core_equations": {
            "单体熵方程": "E_res(i) = 0.22 + 0.66·x_i",
            "N节点均分": "x_i = X_total / N",
            "安全临界": "x < 0.273",
            "双中心熵值": "E_res = 0.368",
            "四级网络熵值": "E_res ≈ 0.294"
        }
    }

    def __init__(self):
        self.multi_center = MultiCenterEntropyFlow()
        self.scenarios = MultiCenterScenario()
        self.four_level = FourLevelNetworkArchitecture()
        self.path_evolution = PathEvolutionAnalysis()
        self.six_system = SixSystemBalanceReview()
        self.constraints = DegeneracyRiskConstraint()
        self.conclusions = PolicyQuantConclusion()

    def get_module_info(self) -> Dict:
        return self.MODULE_INFO

    def quick_query(self, X_total: float = 0.45, N: int = 1) -> Dict:
        """快速查询：给定总人口流入量和节点数，返回熵值"""
        x_i = X_total / N
        E_res = C_CONSTANT + ALPHA_CK * x_i

        if E_res <= 0.40:
            status = "安全稳态"
        elif E_res < 0.75:
            status = "中层矿化警戒"
        elif E_res < 0.98:
            status = "底层僵化红线"
        else:
            status = "全域坍缩"

        return {
            "X_total": X_total,
            "N": N,
            "x_i": x_i,
            "E_res": E_res,
            "status": status
        }


# ───────────────────────────────────────
# 守卫校验
# ───────────────────────────────────────

def validate():
    """守卫校验：验证模块核心逻辑"""
    errors = []

    # 1. 验证常数一致性
    if C_CONSTANT != 0.22:
        errors.append(f"C常数错误：期望0.22，实际{C_CONSTANT}")
    if ALPHA_CK != 0.66:
        errors.append(f"α+ck系数错误：期望0.66，实际{ALPHA_CK}")

    # 2. 验证安全临界速度
    x_safe = X_SAFE_MAX
    if x_safe != 0.273:
        errors.append(f"安全临界速度错误：期望0.273，实际{x_safe}")

    # 3. 验证单中心当前熵值
    E_single = C_CONSTANT + ALPHA_CK * 0.45
    expected_single = 0.517
    if abs(E_single - expected_single) > 0.001:
        errors.append(f"单中心熵值错误：期望{expected_single}，实际{E_single:.3f}")

    # 4. 验证双中心熵值
    E_double = C_CONSTANT + ALPHA_CK * (0.45 / 2)
    expected_double = 0.368
    if abs(E_double - expected_double) > 0.001:
        errors.append(f"双中心熵值错误：期望{expected_double}，实际{E_double:.3f}")

    # 5. 验证四级网络熵值
    E_four = C_CONSTANT + ALPHA_CK * (0.45 / 4)
    expected_four = 0.294
    if abs(E_four - expected_four) > 0.001:
        errors.append(f"四级网络熵值错误：期望约{expected_four}，实际{E_four:.3f}")

    # 6. 验证四级配比总和
    total_ratio = sum(v["ratio"] for v in FourLevelNetworkArchitecture.DISTRIBUTION_RATIOS.values())
    if abs(total_ratio - 1.0) > 0.001:
        errors.append(f"四级配比总和不等于1：实际{total_ratio}")

    # 7. 验证三条路径熵值
    path_a = C_CONSTANT + ALPHA_CK * 0.45
    if abs(path_a - 0.517) > 0.001:
        errors.append(f"路径A熵值错误：期望0.517，实际{path_a:.3f}")

    path_b = C_CONSTANT + ALPHA_CK * (0.45 / 2)
    if abs(path_b - 0.368) > 0.001:
        errors.append(f"路径B熵值错误：期望0.368，实际{path_b:.3f}")

    path_c = C_CONSTANT + ALPHA_CK * (0.45 / 4)
    if abs(path_c - 0.294) > 0.001:
        errors.append(f"路径C熵值错误：期望0.294，实际{path_c:.3f}")

    # 8. 验证状态判定
    module = T61MultiCenterDistributedEntropyModel()

    # x=0.45, N=1 → 中层矿化警戒
    result = module.quick_query(0.45, 1)
    if "中层矿化" not in result["status"]:
        errors.append(f"状态判定错误：x=0.45, N=1预期中层矿化，实际{result['status']}")

    # x=0.225, N=1 → 安全稳态
    result = module.quick_query(0.225, 1)
    if "安全稳态" not in result["status"]:
        errors.append(f"状态判定错误：x=0.225, N=1预期安全稳态，实际{result['status']}")

    # x=0.1125, N=1 → 安全稳态
    result = module.quick_query(0.1125, 1)
    if "安全稳态" not in result["status"]:
        errors.append(f"状态判定错误：x=0.1125, N=1预期安全稳态，实际{result['status']}")

    return errors


# ───────────────────────────────────────
# 主程序入口
# ───────────────────────────────────────

if __name__ == "__main__":
    print("=" * 70)
    print("T61 —— 多中心分布式城市群熵分流模型")
    print("【单点过载破解·N节点均分·四级网络架构·路径演化·政策约束】")
    print("=" * 70)

    module = T61MultiCenterDistributedEntropyModel()
    info = module.get_module_info()

    # 测试1：多中心熵分流定理
    print("\n【测试1】多中心熵分流定理")
    mc = module.multi_center
    print(f"  核心方程：{mc.core_equation}")
    print(f"  说明：{mc.description}")
    print(f"  单节点x_i=0.45时熵值：{mc.calculate_node_entropy(0.45):.3f}")
    print(f"  N=2均分后单节点熵值：{mc.calculate_average_entropy(0.45, 2):.3f}")

    # 测试2：三级情景对比
    print("\n【测试2】三级情景对比")
    scenarios = MultiCenterScenario()
    for scenario_fn, label in [
        (scenarios.scenario_n1, "情景1：单中心(N=1)"),
        (scenarios.scenario_n2, "情景2：双中心(N=2)"),
        (scenarios.scenario_n4, "情景3：四中心(N=4)"),
    ]:
        s = scenario_fn()
        print(f"  {label}：x_i={s['x_i']:.4f} → E_res={s['E_res']:.3f}，{s['status']}")

    # 测试3：四级网络架构
    print("\n【测试3】四级网络架构")
    print(FourLevelNetworkArchitecture.get_summary())

    # 测试4：路径演化分析
    print("\n【测试4】路径演化分析")
    print(PathEvolutionAnalysis.get_summary())

    # 测试5：六系全域平衡
    print("\n【测试5】六系全域平衡")
    print(SixSystemBalanceReview.get_balance_summary())

    # 测试6：制度约束管控
    print("\n【测试6】制度约束管控（防止多中心退化）")
    print(DegeneracyRiskConstraint.get_summary())

    # 测试7：终局量化结论
    print("\n【测试7】终局量化结论")
    print(PolicyQuantConclusion.get_summary())

    # 测试8：方程速查
    print("\n【测试8】方程速查")
    print(f"  单体熵方程：E_res(i) = {C_CONSTANT} + {ALPHA_CK}·x_i")
    print(f"  N节点均分：x_i = X_total / N")
    print(f"  安全临界：x < {X_SAFE_MAX}")
    print(f"  双中心熵值：E_res = {C_CONSTANT + ALPHA_CK * (0.45 / 2):.3f}")
    print(f"  四级网络熵值：E_res ≈ {C_CONSTANT + ALPHA_CK * (0.45 / 4):.3f}")

    # 测试9：完整总览
    print("\n【测试9】完整总览")
    print(f"  模块编号：{info['module_id']}")
    print(f"  模块名称：{info['module_name']}")
    print(f"  副标题：{info['subtitle']}")
    print(f"  版本：{info['version']}")
    print(f"  归属层级：{info['attribution_level']}")
    print(f"  类别：{info['category']}")
    print(f"  依赖模块：{info['dependencies']}")
    print(f"  核心定理：{info['core_theorems']}")
    print(f"  核心方程：{info['core_equations']}")

    # 测试10：守卫校验
    print("\n【测试10】守卫校验")
    errors = validate()
    if errors:
        print(f"  校验结果：✗ 失败")
        for e in errors:
            print(f"    错误：{e}")
    else:
        print(f"  校验结果：✓ 通过")

    # 测试11：快速查询
    print("\n【测试11】快速查询")
    for N in [1, 2, 4, 8]:
        r = module.quick_query(0.45, N)
        print(f"  X_total=0.45, N={N} → x_i={r['x_i']:.4f}, E_res={r['E_res']:.3f}，{r['status']}")

    print("\n" + "=" * 70)
    print("T61多中心分布式城市群熵分流模型验证完成！")
    print("【单点过载破解·N节点均分·四级网络·路径演化·政策约束】")
    print("=" * 70)
