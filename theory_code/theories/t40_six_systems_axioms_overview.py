"""
【归属基底：L0_总本源层·六系六维创世动力学·核心公理总览】
【对应公理：双起点不对称+亲缘传导+意义层级+单系截断+闭环递归+跃迁中转】

T40 —— 六系体系核心公理与规律总览
六大刚性公理 + 双传导路径 + 衍生规律

核心六大公理：
1. 双起点不对称公理（个体强化始发 vs 群体天道始发）
2. 亲缘传导公理（不可跳级·固定链路·顺时针+逆时针）
3. 意义层级公理（本系盈余+逐级衰减+生产/利用二分+总量守恒）
4. 单系截断稳态公理（六系截断→六种专属稳态）
5. 闭环递归公理（走完闭环归零，需新范式开启下一轮）
6. 跃迁中转公理（中间系跃迁释放60单位新增意义）

依赖模块: T34 六系基础 + T37 五元残态 + T38 群体传导 + T39 个体传导
理论版本: V1.0
"""

import math
from typing import Dict, List, Tuple, Optional
from enum import Enum
from ..core.base_theory_module import BaseTheoryModule


# ============================================================================
# 第一部分：六系枚举（总览版）
# ============================================================================

class SixSystemsOverview(Enum):
    """六系总览枚举"""
    QIANGHUA = "强化系"
    SHEHUI = "社会系"
    BIANSHEN = "变身系"
    JUXIAN = "具现系"
    TIANDAO = "天道系"
    ZIRAN = "自然系"


# ============================================================================
# 第二部分：六系基础本体定义
# ============================================================================

class SixSystemsBasicDefinition(BaseTheoryModule):
    """
    六系基础本体定义（三元公理耦合衍生）

    单系独显3个 + 双系耦合3个 = 六大存在极性
    """

    module_id = "T40_C01"
    module_name = "六系基础本体定义"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "六系本体定义"
    is_origin_locked = True
    dependencies = ["T34"]

    def __init__(self):
        super().__init__()
        self.systems = {
            SixSystemsOverview.QIANGHUA: {
                "名称": "强化系",
                "三元耦合": "个体性独显",
                "核心功能": "自持基底、个体边界、自我同一性、主体存续",
                "定位": "个体演化的绝对起点"
            },
            SixSystemsOverview.SHEHUI: {
                "名称": "社会系",
                "三元耦合": "关系性独显",
                "核心功能": "秩序载体、集群联结、公共规则、共在稳态",
                "定位": "集体结构的核心框架"
            },
            SixSystemsOverview.BIANSHEN: {
                "名称": "变身系",
                "三元耦合": "变化性独显",
                "核心功能": "演化动力、形态迭代、范式更新、层级跃迁",
                "定位": "所有流变的动力源"
            },
            SixSystemsOverview.JUXIAN: {
                "名称": "具现系",
                "三元耦合": "个体性+关系性耦合",
                "核心功能": "落地载体、自性外化、造物产出、价值落地",
                "定位": "精神向物质转化的唯一通路"
            },
            SixSystemsOverview.TIANDAO: {
                "名称": "天道系",
                "三元耦合": "关系性+变化性耦合",
                "核心功能": "顶层格局、范式突破、边界开拓、全域升维",
                "定位": "群体文明演化的绝对起点"
            },
            SixSystemsOverview.ZIRAN: {
                "名称": "自然系",
                "三元耦合": "变化性+个体性耦合",
                "核心功能": "底色锚点、本源传承、禀赋积淀、稳态续航",
                "定位": "所有演化的根基保底层"
            }
        }

    def get_system_info(self, system: SixSystemsOverview) -> Dict:
        """获取指定系的信息"""
        return self.systems.get(system, {})

    def get_coupling_type(self, system: SixSystemsOverview) -> str:
        """获取指定系的三元耦合类型"""
        return self.systems.get(system, {}).get("三元耦合", "未知")


# ============================================================================
# 第三部分：六大刚性公理
# ============================================================================

class DualOriginAsymmetryAxiom(BaseTheoryModule):
    """
    公理1：双起点不对称公理

    个体演化从强化系始发（自下而上）
    群体文明从天道系始发（自上而下）
    二者天生相克，可通过中间系中转达成高阶相生
    """

    module_id = "T40_C02"
    module_name = "双起点不对称公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "双起点不对称公理"
    is_origin_locked = True
    dependencies = ["T40_C01"]

    def __init__(self):
        super().__init__()
        self.individual_path = {
            "始发端": "强化系",
            "方向": "自下而上",
            "根基": "个体自持",
            "路径": "强化→具现→社会→天道→变身→自然"
        }
        self.group_path = {
            "始发端": "天道系",
            "方向": "自上而下",
            "根基": "顶层范式解锁",
            "路径": "天道→变身→自然→强化→具现→社会"
        }
        self.polar_relation = {
            "关系": "天生相克",
            "相克本质": "个体边界固化 vs 全域边界消融",
            "和解方式": "通过中间系中转达成高阶相生"
        }

    def get_dual_origins(self) -> Dict:
        """获取双起点信息"""
        return {
            "个体起点": self.individual_path,
            "群体起点": self.group_path,
            "两极关系": self.polar_relation
        }


class KinshipConductionAxiom(BaseTheoryModule):
    """
    公理2：亲缘传导公理（不可跳级·固定链路）

    意义能量只能沿固定亲缘链路逐级传导，无直达路径、不可跨级跳层
    两条对称传导路径：逆时针（群体）+ 顺时针（个体）
    """

    module_id = "T40_C03"
    module_name = "亲缘传导公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "亲缘传导公理"
    is_origin_locked = True
    dependencies = ["T40_C02"]

    def __init__(self):
        super().__init__()
        self.counter_clockwise = [
            "天道系（本系始发）",
            "变身系（第一亲缘承接）",
            "自然系",
            "强化系",
            "具现系",
            "社会系",
            "回流天道系"
        ]
        self.clockwise = [
            "强化系（本系始发）",
            "具现系（第一亲缘承接）",
            "社会系",
            "天道系",
            "变身系",
            "自然系",
            "回流强化系"
        ]
        self.supporting_rule = (
            "单纯的变身迭代、单纯的社会结构变革，仅能完成精神/意识层面的蜕变；"
            "个体的物质性能力改造，必须经由自然禀赋改造或具现物工具赋能才能实现"
        )

    def get_path(self, direction: str) -> List[str]:
        """获取指定方向的传导路径"""
        if direction == "逆时针":
            return self.counter_clockwise
        elif direction == "顺时针":
            return self.clockwise
        return []

    def can_skip_levels(self) -> bool:
        """是否可以跳级传导（答案：不可以）"""
        return False


class MeaningHierarchyAxiom(BaseTheoryModule):
    """
    公理3：意义层级公理

    3.1 本系盈余不递减规则
    3.2 逐级固定衰减规则
    3.3 生产量/利用量二分规则
    3.4 全域总量守恒规则
    """

    module_id = "T40_C04"
    module_name = "意义层级公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "意义层级公理"
    is_origin_locked = True
    dependencies = ["T40_C03"]

    def __init__(self):
        super().__init__()
        self.rules = {
            "本系盈余不递减": {
                "内容": "始发本系自身意义充盈、盈余自持，始发值100意义单位，本系内部不发生衰减",
                "关键点": "衰减仅从第一个外溢亲缘承接系正式启动"
            },
            "逐级固定衰减": {
                "内容": "每向下传递一个亲缘层级，意义理论生产量固定衰减20单位",
                "序列": [100, 100, 80, 60, 40, 20, 0]
            },
            "生产量利用量二分": {
                "内容": "层级标注数值为理论意义生产量（传导基准上限），真实利用量可偏离",
                "两种偏移": [
                    "体系异化、链路切断 → 异化损耗（正值）",
                    "工具跃迁、方法升维 → 跃迁增益（负值）"
                ],
                "公式": "异化差值 = 理论生产量 - 真实利用量"
            },
            "全域总量守恒": {
                "内容": "全域意义总能量不增不减，仅在不同层级、不同形态间转化",
                "关键点": "局部衰减为层级现象，不改变全域总能量"
            }
        }

    def get_four_rules(self) -> Dict:
        """获取四条规则"""
        return self.rules

    def calculate_alienation_delta(self, production: int, utilization: float) -> float:
        """计算异化差值"""
        return production - utilization


class SingleTruncationSteadyStateAxiom(BaseTheoryModule):
    """
    公理4：单系截断稳态公理

    六系任意单一系被完全截断，不会直接崩溃归零，
    而是各自生成专属的稳态形态，对应全域不同存在层级
    """

    module_id = "T40_C05"
    module_name = "单系截断稳态公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "单系截断稳态公理"
    is_origin_locked = True
    dependencies = ["T40_C01", "T37"]  # 依赖五元残态理论

    def __init__(self):
        super().__init__()
        self.truncation_states = {
            SixSystemsOverview.QIANGHUA: {
                "稳态类型": "波动循环稳态",
                "核心特征": "个体边界周期性崩塌重构，陷入归0-非0无限治乱循环",
                "性质": "动态存续稳态"
            },
            SixSystemsOverview.TIANDAO: {
                "稳态类型": "固化不崩稳态",
                "核心特征": "顶层范式锁死，其余五系正常运转，有迭代无升维",
                "性质": "五元残缺态"
            },
            SixSystemsOverview.JUXIAN: {
                "稳态类型": "文明失语稳态",
                "核心特征": "造物生产停滞，无法向外落地输出意义，长期停滞但存续",
                "性质": "封闭原始部落态"
            },
            SixSystemsOverview.ZIRAN: {
                "稳态类型": "本源畸变稳态",
                "核心特征": "文明失根、个体失性，依托人造信仰/异化秩序维系稳定",
                "性质": "神权种姓文明态"
            },
            SixSystemsOverview.SHEHUI: {
                "稳态类型": "二元撕裂稳态",
                "核心特征": "集体秩序崩塌，群体分裂对立，陷入零和博弈",
                "性质": "二元对立态"
            },
            SixSystemsOverview.BIANSHEN: {
                "稳态类型": "静态遗存稳态",
                "核心特征": "演化完全冻结，存在坍缩为孤立自持实体",
                "性质": "一元遗存态"
            }
        }

    def get_truncation_state(self, system: SixSystemsOverview) -> Dict:
        """获取指定系截断后的稳态"""
        return self.truncation_states.get(system, {})


class ClosedLoopRecursionAxiom(BaseTheoryModule):
    """
    公理5：闭环递归公理

    走完完整链路、回归始发本系时，本轮传导意义彻底归零
    本系无法在本次闭环内获得二次赋能
    开启新轮需等待新范式解锁/个体破局
    """

    module_id = "T40_C06"
    module_name = "闭环递归公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "闭环递归公理"
    is_origin_locked = True
    dependencies = ["T40_C03"]

    def __init__(self):
        super().__init__()
        self.rules = [
            "走完完整传导链路、回归始发本系时，本轮传导意义彻底归零",
            "本系无法在本次闭环内获得二次赋能",
            "本系已完成升维跃迁，也无法从本次闭环中获取新增意义",
            "闭环终结后，开启新轮需等待新的范式解锁/个体破局"
        ]

    def can_re_empower_in_same_loop(self) -> bool:
        """同闭环内能否二次赋能（答案：不能）"""
        return False

    def get_new_loop_condition(self) -> str:
        """开启新闭环的条件"""
        return "等待新的范式解锁/个体破局"


class TransitionJumpAxiom(BaseTheoryModule):
    """
    公理6：跃迁中转公理

    中间系发生升维跃迁时，成为意义中转站
    释放60单位新增意义能量，触发全域意义大爆发
    可打通两极相克属性，转化为高阶相生
    """

    module_id = "T40_C07"
    module_name = "跃迁中转公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "跃迁中转公理"
    is_origin_locked = True
    dependencies = ["T40_C02"]

    def __init__(self):
        super().__init__()
        self.core_points = [
            "中间系发生升维跃迁 → 成为意义中转站",
            "释放60单位新增意义能量 → 触发全域意义大爆发",
            "打通体系两极（强化-天道）相克属性 → 顶点对立转化为高阶相生",
            "释放最大量级的文明动能"
        ]
        self.examples = [
            "工业革命的具现系跃迁",
            "信息革命的技术跃迁"
        ]

    def get_jump_energy(self) -> int:
        """获取跃迁释放的意义能量"""
        return 60

    def can_resolve_polar_conflict(self) -> bool:
        """跃迁能否化解两极相克（答案：能）"""
        return True


# ============================================================================
# 第四部分：衍生通用规律
# ============================================================================

class DerivedGeneralLaws(BaseTheoryModule):
    """
    衍生通用规律

    降维判定、升维判定、文明周期规律
    """

    module_id = "T40_C08"
    module_name = "衍生通用规律"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "衍生规律"
    is_origin_locked = True
    dependencies = ["T40_C01", "T40_C05"]

    def __init__(self):
        super().__init__()
        self.laws = {
            "降维判定": {
                "标志": "维度冻结、系别截断、链路断裂",
                "特征": "层级越低，稳态越僵化、演化空间越小"
            },
            "升维判定": {
                "标志": "补齐截断系别、打通传导链路、中间系跃迁",
                "最高阶": "六系全通、相生链路满转"
            },
            "文明周期规律": {
                "路径": [
                    "天道解锁",
                    "逐级传导",
                    "跃迁爆发",
                    "闭环见顶",
                    "矛盾激化",
                    "降维坍缩",
                    "稳态锁死"
                ],
                "匹配": "完全匹配0-6元全域层级体系"
            }
        }

    def get_laws(self) -> Dict:
        """获取全部衍生规律"""
        return self.laws


# ============================================================================
# 主模块：T40六系核心公理总览总控
# ============================================================================

class SixSystemsCoreAxiomsOverviewModule(BaseTheoryModule):
    """
    T40 —— 六系体系核心公理与规律总览主模块

    整合六大刚性公理、双传导路径、衍生通用规律
    """

    module_id = "T40"
    module_name = "六系体系核心公理与规律总览"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·核心公理总览"
    corresponding_axiom = "六大刚性公理+衍生规律"
    is_origin_locked = True
    dependencies = ["T34", "T37", "T38", "T39"]

    def __init__(self):
        super().__init__()
        # 初始化所有子模块
        self.definition = SixSystemsBasicDefinition()
        self.dual_origin = DualOriginAsymmetryAxiom()
        self.kinship = KinshipConductionAxiom()
        self.meaning = MeaningHierarchyAxiom()
        self.truncation = SingleTruncationSteadyStateAxiom()
        self.closed_loop = ClosedLoopRecursionAxiom()
        self.transition = TransitionJumpAxiom()
        self.derived = DerivedGeneralLaws()

    def get_six_axioms_summary(self) -> Dict:
        """获取六大公理总览"""
        return {
            "公理1": "双起点不对称公理（个体强化始发 vs 群体天道始发）",
            "公理2": "亲缘传导公理（不可跳级·固定链路·顺逆时针双路径）",
            "公理3": "意义层级公理（本系盈余+逐级衰减+生产利用二分+总量守恒）",
            "公理4": "单系截断稳态公理（六系截断→六种专属稳态）",
            "公理5": "闭环递归公理（走完归零，新轮需新范式）",
            "公理6": "跃迁中转公理（中间系跃迁释放60单位，打通两极相克）"
        }

    def analyze_civilization_cycle(self, phase: str) -> Dict:
        """
        分析文明周期所处阶段

        Args:
            phase: 阶段名称（天道解锁/逐级传导/跃迁爆发/闭环见顶/矛盾激化/降维坍缩/稳态锁死）
        Returns:
            阶段分析
        """
        phases = {
            "天道解锁": {"层级": "6元始发", "特征": "范式突破、意义充盈"},
            "逐级传导": {"层级": "6→5→4→3→2", "特征": "意义逐级传导衰减"},
            "跃迁爆发": {"层级": "中间系跃迁", "特征": "释放60单位新增意义"},
            "闭环见顶": {"层级": "本轮峰值", "特征": "意义红利耗尽"},
            "矛盾激化": {"层级": "二元对立", "特征": "两极拉扯、零和博弈"},
            "降维坍缩": {"层级": "2→1→0", "特征": "维度冻结、体系坍缩"},
            "稳态锁死": {"层级": "五元/一元/零", "特征": "固化稳态、等待新范式"}
        }
        return phases.get(phase, {})

    def validate(self) -> Tuple[bool, List[str]]:
        """守卫校验"""
        ok, errors = super().validate()

        # 验证六系定义完整性
        if len(self.definition.systems) != 6:
            errors.append("[T40] 六系定义应为6个")

        # 验证六大公理
        axioms = self.get_six_axioms_summary()
        if len(axioms) != 6:
            errors.append("[T40] 核心公理应为6条")

        # 验证截断稳态数
        if len(self.truncation.truncation_states) != 6:
            errors.append("[T40] 单系截断稳态应为6种")

        # 验证跃迁能量
        if self.transition.get_jump_energy() != 60:
            errors.append("[T40] 跃迁中转释放能量应为60单位")

        # 验证意义层级序列
        expected = [100, 100, 80, 60, 40, 20, 0]
        actual = self.meaning.rules["逐级固定衰减"]["序列"]
        if actual != expected:
            errors.append(f"[T40] 意义衰减序列应为{expected}，实际为{actual}")

        return (len(errors) == 0, errors)


# ============================================================================
# 模块注册与便捷接口
# ============================================================================

def get_six_systems_axioms_module() -> SixSystemsCoreAxiomsOverviewModule:
    """获取六系核心公理总览模块实例"""
    return SixSystemsCoreAxiomsOverviewModule()


def quick_axioms_overview() -> Dict:
    """
    快速获取六大公理总览

    Returns:
        六大公理概览
    """
    module = get_six_systems_axioms_module()
    return module.get_six_axioms_summary()


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("T40 —— 六系体系核心公理与规律总览")
    print("=" * 60)

    module = get_six_systems_axioms_module()

    # 测试1：六系基础定义
    print("\n【测试1】六系基础本体定义")
    for sys in SixSystemsOverview:
        info = module.definition.get_system_info(sys)
        print(f"  {info['名称']}: {info['三元耦合']} - {info['定位']}")

    # 测试2：双起点不对称
    print("\n【测试2】双起点不对称公理")
    origins = module.dual_origin.get_dual_origins()
    print(f"  个体起点: {origins['个体起点']['始发端']} ({origins['个体起点']['方向']})")
    print(f"  群体起点: {origins['群体起点']['始发端']} ({origins['群体起点']['方向']})")
    print(f"  两极关系: {origins['两极关系']['关系']}")

    # 测试3：六大公理总览
    print("\n【测试3】六大刚性公理总览")
    axioms = module.get_six_axioms_summary()
    for k, v in axioms.items():
        print(f"  {k}: {v}")

    # 测试4：单系截断稳态
    print("\n【测试4】单系截断稳态公理")
    for sys in SixSystemsOverview:
        state = module.truncation.get_truncation_state(sys)
        print(f"  截断{sys.value} → {state['稳态类型']}")

    # 测试5：跃迁中转
    print("\n【测试5】跃迁中转公理")
    print(f"  跃迁释放能量: {module.transition.get_jump_energy()}单位")
    print(f"  能否化解两极相克: {'能' if module.transition.can_resolve_polar_conflict() else '不能'}")

    # 测试6：文明周期
    print("\n【测试6】文明周期分析")
    phase = "跃迁爆发"
    analysis = module.analyze_civilization_cycle(phase)
    print(f"  {phase}: {analysis.get('特征', '')}")

    # 守卫校验
    print("\n【测试7】守卫校验")
    ok, errors = module.validate()
    print(f"  校验结果: {'✓ 通过' if ok else '✗ 失败'}")
    if errors:
        for e in errors:
            print(f"  错误: {e}")

    print("\n" + "=" * 60)
    print("T40模块验证完成!")
