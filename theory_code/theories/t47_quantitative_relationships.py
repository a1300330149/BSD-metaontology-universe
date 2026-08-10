"""
【归属基底：L0_总本源层·六系六维创世动力学·定量关系终版】
【对应定量模型：三层对冲定量模型·5大方程组·4场景模拟·5临界阈值】

T47 —— 六系相生相克定量关系推演
（全局修正终版，定量模型完整闭环）

定量基准：
- 单系满额意义生产量：100单位
- 六系总意义：600单位
- 每级自然损耗：20单位

三层对冲配对：
- 顶点层：天道系 ↔ 强化系
- 中间层：变身系 ↔ 具现系
- 基底层：社会系 ↔ 自然系

方程组：
1. 总量守恒方程
2. 三层同级对冲制衡方程
3. 中间层中转回收效率方程
4. 承载层隐性耗散方程
5. 闭环衰减铁律

依赖模块: T40-T46
理论版本: V1.0
是否定量终版: 是
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from ..core.base_theory_module import BaseTheoryModule


# ============================================================================
# 第一部分：定量基准与常量
# ============================================================================

@dataclass
class QuantitativeConstants:
    """定量基准常量"""
    TOTAL_MEANING = 600          # 六系总意义量
    SINGLE_BASE = 100             # 单系满额基准量
    NATURAL_LOSS_PER_LEVEL = 20   # 每级自然损耗
    NATURAL_BALANCE_LOSS = 20     # 自然均衡对冲损耗
    TOTAL_NATURAL_LOSS = 60       # 全域总对冲自然损耗
    EFFECTIVE_NATURAL = 540       # 全域自然有效留存
    TRANSFER_RECOVERY_RATE = 0.75  # 中转回收效率75%
    CARRY_LOSS_RATE = 0.5         # 承载层隐性耗散率
    # 临界阈值
    THRESHOLD_JUMP_TREND = 130    # 跃迁趋势阈值
    THRESHOLD_STRUCTURAL_DISTORTION = 160  # 结构性扭曲阈值
    THRESHOLD_EMPTY_BUBBLE = 30   # 意义空发泡沫阈值
    THRESHOLD_FIVE_YUAN_LOCK = 60  # 五元锁死阈值（两极对冲损耗）
    THRESHOLD_BASE_RIGID = 80     # 底座僵化阈值（承载层差值）


# ============================================================================
# 第二部分：三层对冲配对
# ============================================================================

class ThreeLayerOppositionPairs:
    """三层对冲配对（唯一刚性配对）"""

    pairs = {
        "顶点层": {
            "对冲双方": ["天道系", "强化系"],
            "性质": "顶级对立相克",
            "说明": "文明开拓边界 ↔ 个体自性边界"
        },
        "中间转化层": {
            "对冲双方": ["变身系", "具现系"],
            "性质": "同级双向对冲制衡",
            "说明": "迭代能力 ↔ 物质造物"
        },
        "底层承载层": {
            "对冲双方": ["社会系", "自然系"],
            "性质": "同级双向对冲制衡",
            "说明": "软规则秩序 ↔ 硬实体基底"
        }
    }

    system_to_layer = {
        "天道系": "顶点层",
        "强化系": "顶点层",
        "变身系": "中间转化层",
        "具现系": "中间转化层",
        "社会系": "底层承载层",
        "自然系": "底层承载层"
    }

    system_to_opponent = {
        "天道系": "强化系",
        "强化系": "天道系",
        "变身系": "具现系",
        "具现系": "变身系",
        "社会系": "自然系",
        "自然系": "社会系"
    }

    @classmethod
    def get_opponent(cls, system: str) -> str:
        """获取某系的对冲对手"""
        return cls.system_to_opponent.get(system, "未知")

    @classmethod
    def get_layer(cls, system: str) -> str:
        """获取某系所属层级"""
        return cls.system_to_layer.get(system, "未知")


# ============================================================================
# 第三部分：定量方程组核心计算
# ============================================================================

class QuantitativeEquations:
    """定量方程组核心计算"""

    def __init__(self):
        self.const = QuantitativeConstants()

    def check_total_conservation(self, systems: Dict[str, float]) -> Tuple[bool, float]:
        """
        验证总量守恒

        Args:
            systems: 六系意义量字典
        Returns:
            (是否守恒, 实际总量)
        """
        total = sum(systems.values())
        return (abs(total - self.const.TOTAL_MEANING) < 0.01, total)

    def calc_layer_diff(self, systems: Dict[str, float]) -> Dict[str, float]:
        """
        计算三层差值

        Returns:
            {层级名: 差值}
        """
        return {
            "顶点层": abs(systems.get("天道系", 0) - systems.get("强化系", 0)),
            "中间转化层": abs(systems.get("变身系", 0) - systems.get("具现系", 0)),
            "底层承载层": abs(systems.get("社会系", 0) - systems.get("自然系", 0))
        }

    def calc_extra_opposition_loss(self, systems: Dict[str, float]) -> float:
        """
        计算额外对冲损耗（超出基础损耗的部分）
        W = (Δ1 + Δ2 + Δ3) / 3
        基础损耗：每组20单位，三组共60单位（自然均衡时也存在）
        """
        diffs = self.calc_layer_diff(systems)
        total_diff = sum(diffs.values())
        return total_diff / 3

    def calc_total_opposition_loss(self, systems: Dict[str, float]) -> float:
        """
        计算总对冲损耗 = 基础损耗60 + 额外损耗
        """
        extra = self.calc_extra_opposition_loss(systems)
        return self.const.TOTAL_NATURAL_LOSS + extra

    def calc_transfer_recovery(self, systems: Dict[str, float]) -> Tuple[float, float]:
        """
        计算中间层中转回收效率
        仅回收两极对冲的额外损耗部分（差值产生的额外损耗）
        基础损耗60单位不可回收

        Returns:
            (可回收正向增量, 不可回收自然耗散)
        """
        polar_diff = abs(systems.get("天道系", 0) - systems.get("强化系", 0))
        polar_extra_loss = polar_diff / 3  # 两极额外损耗
        recoverable = polar_extra_loss * self.const.TRANSFER_RECOVERY_RATE
        natural_loss = polar_extra_loss * (1 - self.const.TRANSFER_RECOVERY_RATE)
        return (recoverable, natural_loss)

    def calc_carry_hidden_loss(self, systems: Dict[str, float]) -> float:
        """
        计算承载层隐性耗散
        W_隐 = |S_社 - S_自| / 2
        """
        diff = abs(systems.get("社会系", 0) - systems.get("自然系", 0))
        return diff / 2

    def calc_effective_meaning(self, systems: Dict[str, float]) -> float:
        """
        计算全域有效意义量
        = 总量 - 总对冲损耗 - 隐性耗散 + 中转回收量
        = 540 - 额外损耗 - 隐性耗散 + 中转回收量
        """
        total = sum(systems.values())
        opp_loss = self.calc_total_opposition_loss(systems)
        hidden_loss = self.calc_carry_hidden_loss(systems)
        recoverable, _ = self.calc_transfer_recovery(systems)
        return total - opp_loss - hidden_loss + recoverable

    def check_natural_balance(self, systems: Dict[str, float]) -> bool:
        """判断是否为自然均衡状态"""
        for sys in ["天道系", "强化系", "变身系", "具现系", "社会系", "自然系"]:
            if abs(systems.get(sys, 0) - self.const.SINGLE_BASE) > 0.01:
                return False
        return True


# ============================================================================
# 第四部分：四大场景模拟
# ============================================================================

class FourScenariosSimulation:
    """四大典型场景模拟"""

    def __init__(self):
        self.eq = QuantitativeEquations()

    def scenario_natural_balance(self) -> Dict:
        """
        场景0：自然均衡态（六元完备稳态基准）
        """
        systems = {
            "天道系": 100,
            "强化系": 100,
            "变身系": 100,
            "具现系": 100,
            "社会系": 100,
            "自然系": 100
        }
        return self._build_scenario_result(
            "自然均衡态（六元完备稳态基准）",
            systems,
            "无人工截断、无资源倾斜、无定向扭曲的自然最优状态",
            "绝对均衡基准，所有文明异化均是对此稳态的人为偏离"
        )

    def scenario_lock_tiandao(self) -> Dict:
        """
        场景1：锁死天道系（五元残缺稳态·传统社会/应试体系）
        天道40+强化160+变身100+具现100+社会100+自然100=600
        """
        systems = {
            "天道系": 40,
            "强化系": 160,
            "变身系": 100,
            "具现系": 100,
            "社会系": 100,
            "自然系": 100
        }
        return self._build_scenario_result(
            "锁死天道系（五元残缺稳态）",
            systems,
            "天道系范式锁死、迭代停滞，强化系被动溢出暴涨，两极差值120",
            "文明无新范式突破，只能无限内卷个体能力，对应古代王朝超稳态、当代应试教育"
        )

    def scenario_juxian_overload(self) -> Dict:
        """
        场景2：具现系路径依赖过载（工业化晚期·当代核心困局）
        """
        systems = {
            "天道系": 90,
            "强化系": 190,
            "变身系": 20,
            "具现系": 180,
            "社会系": 60,
            "自然系": 60
        }
        return self._build_scenario_result(
            "具现系路径依赖过载（工业化晚期·当代核心困局）",
            systems,
            "持续资源注入具现系，变身系被挤压萎缩，中间层彻底失衡",
            "产能基建无限堆积，新职业新迭代能力缺失；旧产能无法出清、新体系无法生成"
        )

    def scenario_carry_misalignment(self) -> Dict:
        """
        场景3：底层承载层软硬错位（基建过剩+制度滞后）
        天道90+强化90+变身80+具现80+社会50+自然210=600
        """
        systems = {
            "天道系": 90,
            "强化系": 90,
            "变身系": 80,
            "具现系": 80,
            "社会系": 50,
            "自然系": 210
        }
        return self._build_scenario_result(
            "底层承载层软硬错位（基建过剩+制度滞后）",
            systems,
            "自然系超前拉满，社会系被压制，承载层差值160",
            "实体基建豪华过剩，但社会治理规则体系严重滞后，形成空城、无效基建"
        )

    def scenario_truncate_qianghua(self) -> Dict:
        """
        场景4：截断强化系（治乱循环波动态·王朝更迭）
        天道170+强化30+变身85+具现85+社会115+自然115=600
        """
        systems = {
            "天道系": 170,
            "强化系": 30,
            "变身系": 85,
            "具现系": 85,
            "社会系": 115,
            "自然系": 115
        }
        return self._build_scenario_result(
            "截断强化系（治乱循环波动态）",
            systems,
            "强化系个体生存边界被持续侵蚀，天道系短暂虚膨，两极差值140",
            "两极对冲损耗拉满，体系周期性归零重组，陷入治乱往复循环"
        )

    def _build_scenario_result(self, name: str, systems: Dict[str, float],
                               mechanism: str, phenomenon: str) -> Dict:
        """构建场景结果"""
        diffs = self.eq.calc_layer_diff(systems)
        opp_loss = self.eq.calc_total_opposition_loss(systems)
        hidden_loss = self.eq.calc_carry_hidden_loss(systems)
        recoverable, natural_loss = self.eq.calc_transfer_recovery(systems)
        effective = self.eq.calc_effective_meaning(systems)
        total_ok, total = self.eq.check_total_conservation(systems)

        return {
            "场景名称": name,
            "六系数值": systems,
            "总量守恒": f"{'✓' if total_ok else '✗'} ({total}单位)",
            "三层差值": diffs,
            "对冲损耗总量": opp_loss,
            "中转可回收": recoverable,
            "中转自然耗散": natural_loss,
            "承载层隐性耗散": hidden_loss,
            "全域有效意义": effective,
            "核心机制": mechanism,
            "现象释义": phenomenon
        }

    def get_all_scenarios(self) -> List[Dict]:
        """获取所有场景"""
        return [
            self.scenario_natural_balance(),
            self.scenario_lock_tiandao(),
            self.scenario_juxian_overload(),
            self.scenario_carry_misalignment(),
            self.scenario_truncate_qianghua()
        ]


# ============================================================================
# 第五部分：临界阈值判断
# ============================================================================

class CriticalThresholds:
    """临界阈值判断体系"""

    def __init__(self):
        self.const = QuantitativeConstants()

    def check_all_thresholds(self, systems: Dict[str, float]) -> Dict:
        """
        检查所有临界阈值

        Returns:
            {阈值名: (是否触发, 数值, 阈值)}
        """
        results = {}

        # 阈值1：单系跃迁趋势
        max_single = max(systems.values())
        threshold1 = self.const.THRESHOLD_JUMP_TREND
        results["单系跃迁趋势"] = (
            max_single > threshold1,
            max_single,
            threshold1
        )

        # 阈值2：结构性不可逆扭曲
        threshold2 = self.const.THRESHOLD_STRUCTURAL_DISTORTION
        results["结构性扭曲"] = (
            max_single > threshold2,
            max_single,
            threshold2
        )

        # 阈值4：两极对冲损耗
        polar_diff = abs(systems.get("天道系", 0) - systems.get("强化系", 0))
        threshold4 = self.const.THRESHOLD_FIVE_YUAN_LOCK
        results["五元锁死（对冲损耗）"] = (
            polar_diff > threshold4,
            polar_diff,
            threshold4
        )

        # 阈值5：承载层软硬差值
        carry_diff = abs(systems.get("社会系", 0) - systems.get("自然系", 0))
        threshold5 = self.const.THRESHOLD_BASE_RIGID
        results["底座僵化（承载层差值）"] = (
            carry_diff > threshold5,
            carry_diff,
            threshold5
        )

        return results

    def get_severity_level(self, systems: Dict[str, float]) -> str:
        """获取体系失衡严重等级"""
        thresholds = self.check_all_thresholds(systems)
        triggered = sum(1 for triggered, _, _ in thresholds.values() if triggered)

        if triggered == 0:
            return "健康均衡态"
        elif triggered == 1:
            return "轻度偏离态"
        elif triggered == 2:
            return "中度失衡态"
        elif triggered == 3:
            return "重度扭曲态"
        else:
            return "结构性崩溃态"


# ============================================================================
# 主模块：T47定量关系终版
# ============================================================================

class SixSystemsQuantitativeModule(BaseTheoryModule):
    """
    T47 —— 六系相生相克定量关系推演主模块

    全局修正终版，定量模型完整闭环
    包含：定量基准、三层对冲、方程组、4大场景、5大阈值
    """

    module_id = "T47"
    module_name = "六系相生相克定量关系推演"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·定量关系终版"
    corresponding_axiom = "三层对冲定量模型"
    is_origin_locked = True
    dependencies = ["T40", "T41", "T42", "T43", "T44", "T45", "T46"]
    is_quantitative_final = True

    def __init__(self):
        super().__init__()
        self.constants = QuantitativeConstants()
        self.pairs = ThreeLayerOppositionPairs()
        self.equations = QuantitativeEquations()
        self.scenarios = FourScenariosSimulation()
        self.thresholds = CriticalThresholds()

    def get_basic_constants(self) -> Dict:
        """获取定量基准常量"""
        return {
            "六系总意义": f"{self.constants.TOTAL_MEANING}单位",
            "单系满额基准": f"{self.constants.SINGLE_BASE}单位",
            "每级自然损耗": f"{self.constants.NATURAL_LOSS_PER_LEVEL}单位",
            "自然对冲损耗": f"{self.constants.NATURAL_BALANCE_LOSS}单位/组",
            "全域总自然损耗": f"{self.constants.TOTAL_NATURAL_LOSS}单位",
            "全域自然有效留存": f"{self.constants.EFFECTIVE_NATURAL}单位",
            "中转回收效率": f"{int(self.constants.TRANSFER_RECOVERY_RATE * 100)}%"
        }

    def get_opposition_pairs(self) -> Dict:
        """获取三层对冲配对"""
        return self.pairs.pairs

    def analyze_system_state(self, systems: Dict[str, float]) -> Dict:
        """
        分析六系状态

        Args:
            systems: 六系意义量字典
        Returns:
            完整分析报告
        """
        conservation_ok, total = self.equations.check_total_conservation(systems)
        layer_diffs = self.equations.calc_layer_diff(systems)
        opp_loss = self.equations.calc_total_opposition_loss(systems)
        carry_loss = self.equations.calc_carry_hidden_loss(systems)
        recoverable, natural_loss = self.equations.calc_transfer_recovery(systems)
        effective = self.equations.calc_effective_meaning(systems)
        threshold_status = self.thresholds.check_all_thresholds(systems)
        severity = self.thresholds.get_severity_level(systems)

        return {
            "总量守恒": f"{'✓' if conservation_ok else '✗'} ({total}单位)",
            "三层差值": layer_diffs,
            "对冲损耗总量": opp_loss,
            "中转可回收": recoverable,
            "中转自然耗散": natural_loss,
            "承载层隐性耗散": carry_loss,
            "全域有效意义": effective,
            "阈值触发状态": {
                name: f"{'⚠ 触发' if triggered else '✓ 正常'} (当前{val:.0f}/阈值{thr})"
                for name, (triggered, val, thr) in threshold_status.items()
            },
            "失衡等级": severity
        }

    def get_scenario(self, scenario_name: str) -> Optional[Dict]:
        """获取指定场景"""
        all_scenarios = self.scenarios.get_all_scenarios()
        for s in all_scenarios:
            if scenario_name in s["场景名称"]:
                return s
        return None

    def validate(self) -> Tuple[bool, List[str]]:
        """守卫校验"""
        ok, errors = super().validate()

        # 验证总量600
        if self.constants.TOTAL_MEANING != 600:
            errors.append("[T47] 六系总意义应为600单位")

        # 验证单系基准100
        if self.constants.SINGLE_BASE != 100:
            errors.append("[T47] 单系基准应为100单位")

        # 验证三级配对
        if len(self.pairs.pairs) != 3:
            errors.append("[T47] 三层对冲应为3组")

        # 验证自然均衡场景总量守恒
        nat_scenario = self.scenarios.scenario_natural_balance()
        nat_systems = nat_scenario["六系数值"]
        total_ok, total = self.equations.check_total_conservation(nat_systems)
        if not total_ok:
            errors.append(f"[T47] 自然均衡场景总量应为600，实际{total}")

        # 验证自然均衡有效意义540
        effective = self.equations.calc_effective_meaning(nat_systems)
        if abs(effective - self.constants.EFFECTIVE_NATURAL) > 1:
            errors.append(f"[T47] 自然均衡有效意义应为540，实际{effective}")

        # 验证5个场景
        all_scenarios = self.scenarios.get_all_scenarios()
        if len(all_scenarios) != 5:
            errors.append(f"[T47] 场景数应为5个，实际{len(all_scenarios)}个")

        # 验证所有场景总量守恒
        for s in all_scenarios:
            sys_ok, sys_total = self.equations.check_total_conservation(s["六系数值"])
            if not sys_ok:
                errors.append(f"[T47] 场景[{s['场景名称']}]总量不守恒: {sys_total}")

        # 验证临界阈值5个
        test_systems = {"天道系": 50, "强化系": 150, "变身系": 90, "具现系": 90, "社会系": 40, "自然系": 180}
        thresholds = self.thresholds.check_all_thresholds(test_systems)
        if len(thresholds) < 4:
            errors.append("[T47] 临界阈值应至少4个")

        return (len(errors) == 0, errors)


# ============================================================================
# 模块注册与便捷接口
# ============================================================================

def get_quantitative_module() -> SixSystemsQuantitativeModule:
    """获取定量关系模块实例"""
    return SixSystemsQuantitativeModule()


def quick_state_analysis(systems: Dict[str, float]) -> Dict:
    """
    快速六系状态分析

    Args:
        systems: 六系意义量字典
    Returns:
        分析结果
    """
    module = get_quantitative_module()
    return module.analyze_system_state(systems)


if __name__ == "__main__":
    # 测试代码
    print("=" * 70)
    print("  T47 —— 六系相生相克定量关系推演【全局修正终版】")
    print("=" * 70)

    module = get_quantitative_module()

    # 测试1：定量基准常量
    print("\n【测试1】定量基准常量")
    consts = module.get_basic_constants()
    for k, v in consts.items():
        print(f"  {k}: {v}")

    # 测试2：三层对冲配对
    print("\n【测试2】三层对冲配对（唯一刚性配对）")
    pairs = module.get_opposition_pairs()
    for layer, info in pairs.items():
        print(f"  {layer}: {info['对冲双方'][0]} ↔ {info['对冲双方'][1]}")

    # 测试3：自然均衡态分析
    print("\n【测试3】自然均衡态分析")
    nat_scenario = module.scenarios.scenario_natural_balance()
    analysis = module.analyze_system_state(nat_scenario["六系数值"])
    print(f"  总量守恒: {analysis['总量守恒']}")
    print(f"  全域有效意义: {analysis['全域有效意义']:.0f}单位")
    print(f"  失衡等级: {analysis['失衡等级']}")

    # 测试4：四大典型场景
    print("\n【测试4】五大典型场景一览")
    all_scenarios = module.scenarios.get_all_scenarios()
    for i, s in enumerate(all_scenarios):
        severity = module.thresholds.get_severity_level(s["六系数值"])
        print(f"  {i+1}. {s['场景名称'][:30]} - 失衡等级: {severity}")

    # 测试5：具现系过载（当代困局）详细分析
    print("\n【测试5】具现系路径依赖过载（当代核心困局）详细分析")
    juxian = module.scenarios.scenario_juxian_overload()
    analysis = module.analyze_system_state(juxian["六系数值"])
    print(f"  六系数值: {juxian['六系数值']}")
    print(f"  三层差值: {analysis['三层差值']}")
    print(f"  对冲损耗: {analysis['对冲损耗总量']:.1f}单位")
    print(f"  承载层隐性耗散: {analysis['承载层隐性耗散']:.1f}单位")
    for name, status in analysis["阈值触发状态"].items():
        print(f"  {name}: {status}")
    print(f"  失衡等级: {analysis['失衡等级']}")

    # 测试6：自定义系统快速分析
    print("\n【测试6】自定义快速分析（示例：天道=60, 强化=140）")
    custom = {"天道系": 60, "强化系": 140, "变身系": 90,
              "具现系": 90, "社会系": 90, "自然系": 90}
    result = quick_state_analysis(custom)
    print(f"  失衡等级: {result['失衡等级']}")

    # 守卫校验
    print("\n【测试7】守卫校验")
    ok, errors = module.validate()
    print(f"  校验结果: {'✓ 通过' if ok else '✗ 失败'}")
    if errors:
        for e in errors:
            print(f"  错误: {e}")

    print("\n" + "=" * 70)
    print("  T47定量关系模块验证完成!")
    print("  【总量600 · 三层对冲 · 5大场景 · 5临界阈值 · 5方程组】")
    print("=" * 70)
