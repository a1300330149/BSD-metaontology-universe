"""
【归属基底：L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁】
【对应公理：选择定向跃迁+正负跃迁一体两面+基底溢出意义空发+路径依赖惯性】

T41 —— 六系跃迁定向与正负跃迁一体两面公理
新增四条刚性规则，补充T40六系核心公理

四大新增公理：
1. 选择定向跃迁公理（选择决定跃迁方向，亲缘决定意义本质）
2. 正负跃迁一体两面公理（向上为正，向下为负，同根同源）
3. 基底溢出与意义空发公理（溢出无法传导→空发耗散）
4. 路径依赖惯性公理（红利期后惯性依赖→边际递减→五元锁死）

依赖模块: T38 T39 T40
理论版本: V1.0
"""

import math
from typing import Dict, List, Tuple, Optional
from enum import Enum
from ..core.base_theory_module import BaseTheoryModule


# ============================================================================
# 第一部分：跃迁方向枚举
# ============================================================================

class JumpDirection(Enum):
    """跃迁方向枚举"""
    POSITIVE = "正值跃迁"      # 向上传导，带动升维
    NEGATIVE = "负值跃迁"      # 向下挤压，异化内卷
    EMPTY_BURST = "意义空发"   # 无法传导，空发耗散


# ============================================================================
# 第二部分：选择定向跃迁公理
# ============================================================================

class SelectiveDirectionalJumpAxiom(BaseTheoryModule):
    """
    公理1：选择定向跃迁公理

    个体、集体、文明的主观选择与资源倾斜，决定哪一系优先发生跃迁。
    跃迁方向不被亲缘链路强制绑定。

    核心要点：
    - 意义利用层面：可突破亲缘顺序，定向超量赋能
    - 意义生产层面：本源属性永远归属于亲缘层级
    - 拉满不等于升维，底层属性不变
    """

    module_id = "T41_C01"
    module_name = "选择定向跃迁公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "选择定向跃迁公理"
    is_origin_locked = True
    dependencies = ["T40"]

    def __init__(self):
        super().__init__()
        self.core_points = [
            "主观选择与资源倾斜决定哪一系优先跃迁",
            "跃迁方向不被亲缘链路强制绑定",
            "利用层面可突破顺序，定向超量赋能",
            "生产本源属性永远归属于亲缘层级",
            "利用量溢出不会自动升维到更高级别",
            "拉满不等于升维，底层属性不变"
        ]

    def can_select_jump_target(self) -> bool:
        """是否可以选择跃迁目标系（答案：可以）"""
        return True

    def does_utilization_equal_upgrade(self) -> bool:
        """利用量溢出是否等于升维（答案：不等于）"""
        return False

    def get_affinity_affiliation(self, system_name: str) -> str:
        """
        获取指定系的亲缘归属（即使利用量溢出，意义本质仍归属于此层级）
        """
        affiliation = {
            "强化系": "个体性独显层级",
            "社会系": "关系性独显层级",
            "变身系": "变化性独显层级",
            "具现系": "个体+关系耦合层级",
            "天道系": "关系+变化耦合层级",
            "自然系": "变化+个体耦合层级"
        }
        return affiliation.get(system_name, "未知")


# ============================================================================
# 第三部分：正负跃迁一体两面公理
# ============================================================================

class PositiveNegativeJumpAxiom(BaseTheoryModule):
    """
    公理2：正负跃迁一体两面公理

    利用量突破理论生产量基底，存在且仅存在两个方向，
    本质同源、一体两面。

    正值跃迁：向上传导，带动升维，全域增长
    负值跃迁：向下挤压，透支底层，全域流失

    核心判定标准：是否带动天道级范式突破与自然系底层积淀
    """

    module_id = "T41_C02"
    module_name = "正负跃迁一体两面公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "正负跃迁一体两面公理"
    is_origin_locked = True
    dependencies = ["T41_C01"]

    def __init__(self):
        super().__init__()
        self.positive = {
            "方向": "向上传导",
            "效果": "带动上层系别同步升维",
            "结果": "全域意义总量有效增长",
            "对应": "文明正向升维",
            "判定依据": "带动天道级范式突破与自然系底层积淀"
        }
        self.negative = {
            "方向": "向下挤压",
            "效果": "压缩下层系别、透支底层基底",
            "结果": "全域意义隐性流失",
            "对应": "文明异化内卷",
            "判定依据": "靠压缩底层换规模膨胀"
        }
        self.essence = "本质同源、一体两面，都是突破意义基底的产物，只是能量流向相反"

    def determine_direction(self,
                            has_tiandao_breakthrough: bool,
                            has_ziran_foundation: bool) -> JumpDirection:
        """
        判定跃迁方向

        Args:
            has_tiandao_breakthrough: 是否带动天道级范式突破
            has_ziran_foundation: 是否带动自然系底层积淀
        Returns:
            跃迁方向
        """
        if has_tiandao_breakthrough and has_ziran_foundation:
            return JumpDirection.POSITIVE
        else:
            return JumpDirection.NEGATIVE

    def is_same_origin(self) -> bool:
        """正负跃迁是否同根同源（答案：是）"""
        return True


# ============================================================================
# 第四部分：基底溢出与意义空发公理
# ============================================================================

class BaseOverflowEmptyBurstAxiom(BaseTheoryModule):
    """
    公理3：基底溢出与意义空发公理

    当某一系利用量大幅超越其意义基底承载上限时，
    溢出的意义无法沿亲缘链路有效向上传导，也无法向下沉淀，
    形成意义空发。

    现象：规模扩张、活跃度提升、数据好看
    本质：没有实质层级升维，也没有底层素养沉淀
    结果：循环中逐步耗散，只留下表层泡沫
    """

    module_id = "T41_C03"
    module_name = "基底溢出与意义空发公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "基底溢出与意义空发公理"
    is_origin_locked = True
    dependencies = ["T41_C02"]

    def __init__(self):
        super().__init__()
        self.characteristics = [
            "表面规模扩张、活跃度提升、数据好看",
            "没有生成实质的层级升维",
            "没有沉淀为底层素养",
            "空发意义在循环中逐步耗散",
            "无法转化为全域升维动能",
            "最终只留下表层泡沫"
        ]
        self.typical_phenomenon = "有增长无发展、有规模无升维的稳态困局"
        self.contemporary_examples = [
            "互联网平台规模越来越大，但没有诞生新的社会制度范式",
            "数字工具普及率越来越高，但个体核心能力没有同步升维",
            "经济总量持续增长，但底层意义感、幸福感没有同步提升",
            "从纸质低效内卷变成数字高效内卷"
        ]

    def is_empty_burst(self,
                      overflow_level: float,
                      has_upward_conduction: bool,
                      has_downward_precipitation: bool) -> bool:
        """
        判断是否为意义空发

        Args:
            overflow_level: 溢出程度（>100为溢出）
            has_upward_conduction: 是否有效向上传导
            has_downward_precipitation: 是否有效向下沉淀
        Returns:
            是否为意义空发
        """
        return overflow_level > 100 and not has_upward_conduction and not has_downward_precipitation


# ============================================================================
# 第五部分：路径依赖惯性公理
# ============================================================================

class PathDependenceInertiaAxiom(BaseTheoryModule):
    """
    公理4：路径依赖惯性公理

    某一系的跃迁红利期结束后，文明/群体会自发形成路径依赖，
    持续向该系追加资源，试图复刻过往成功。

    惯性依赖后果：
    - 资源投入越多，边际效益越低
    - 越容易滑向负值跃迁与意义空发
    - 无法切换跃迁系别 → 永久卡在五元稳态
    """

    module_id = "T41_C04"
    module_name = "路径依赖惯性公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "路径依赖惯性公理"
    is_origin_locked = True
    dependencies = ["T41_C03", "T37"]  # 依赖五元残态理论

    def __init__(self):
        super().__init__()
        self.mechanism = [
            "某一系跃迁红利期结束",
            "文明/群体自发形成路径依赖",
            "持续向该系追加资源，试图复刻过往成功",
            "资源投入越多，边际效益越低",
            "越容易滑向负值跃迁与意义空发",
            "无法切换跃迁系别 → 永久卡在五元稳态"
        ]
        self.china_case = {
            "路径依赖形成": "改革开放四十余年，靠工业化/基建/数字化（具现系）实现快速追赶",
            "惯性困局": "工业化晚期，具现系红利见顶，边际效益持续递减",
            "天道锁死": "基础科学、制度范式、文明认知没有量级突破",
            "五元稳态": "五系持续运转，天道系长期无法解锁",
            "历史同构": "与古代王朝天道皇权锁死、五系循环稳态完全同构"
        }

    def get_inertia_stage(self,
                         bonus_period_ended: bool,
                         resource_still_investing: bool,
                         marginal_benefit_decreasing: bool) -> str:
        """
        判断路径依赖阶段

        Returns:
            阶段描述
        """
        if not bonus_period_ended:
            return "红利期：正向跃迁，收益递增"
        elif bonus_period_ended and not resource_still_investing:
            return "转型期：红利结束，开始调整方向"
        elif bonus_period_ended and resource_still_investing and not marginal_benefit_decreasing:
            return "惯性初期：继续投入，收益尚可维持"
        else:
            return "惯性晚期：持续投入，边际递减，滑向负值跃迁与意义空发"

    def solution(self) -> str:
        """破局路径"""
        return "切换跃迁系别，从持续依赖具现系，转向定向突破天道系"


# ============================================================================
# 第六部分：当代具现系双线实证
# ============================================================================

class ContemporaryJuxianDoubleEvidence(BaseTheoryModule):
    """
    当代具现系双线实证

    正值跃迁支线：个体强化→具现系突破
    负值跃迁支线：具现系溢出→社会系异化
    """

    module_id = "T41_C05"
    module_name = "当代具现系双线实证"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "正负跃迁实证"
    is_origin_locked = True
    dependencies = ["T41_C02"]

    def __init__(self):
        super().__init__()
        self.positive_line = {
            "名称": "正值跃迁支线",
            "路径": "个体强化→具现系突破",
            "机制": "个体主动选择用数字工具、AI工具自我强化",
            "实证": "善用AI个体效率提升300-400%，具现系利用量120-150",
            "验证": "利用量溢出但意义本质仍属具现系层级"
        }
        self.negative_line = {
            "名称": "负值跃迁支线",
            "路径": "具现系溢出→社会系异化",
            "机制": "平台资本定向放大人、算法、数字调度系统，反向撬动社会系",
            "典型案例": "外卖骑手、网约车司机体系",
            "表面特征": "数千万灵活就业岗位，社会系规模远超传统行业",
            "本质特征": "压缩强化系（算法拆解劳动）+ 透支自然系（时间健康边界侵蚀）",
            "结果": "社会系规模虚高，全域净收益为负"
        }

    def get_both_lines(self) -> Dict:
        """获取双线实证"""
        return {
            "正值跃迁": self.positive_line,
            "负值跃迁": self.negative_line
        }


# ============================================================================
# 第七部分：工业化晚期意义空发分析
# ============================================================================

class LateIndustrializationAnalysis(BaseTheoryModule):
    """
    工业化晚期的具现系失效与意义空发

    早期为何有效 vs 晚期为何失效
    当代意义空发普遍现象
    """

    module_id = "T41_C06"
    module_name = "工业化晚期意义空发分析"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "意义空发实证"
    is_origin_locked = True
    dependencies = ["T41_C03"]

    def __init__(self):
        super().__init__()
        self.early_stage = {
            "状态": "正值跃迁",
            "原因1": "增量充足：工业造物从0到1爆发，意义增量巨大",
            "原因2": "传导通畅：同步带动天道系（科学范式）与自然系（科学素养）",
            "结果": "正向亲缘传导，完整升维链路"
        }
        self.late_stage = {
            "状态": "意义空发+负值跃迁",
            "原因1": "边际递减：基础普及完成，增量趋近于零",
            "原因2": "传导断裂：无法向上突破天道系，溢出能量无法承接",
            "原因3": "向下挤压：为维持增长，开始压缩底层、透支基底",
            "结果": "低层循环空转、异化内卷"
        }
        self.contemporary_empty_examples = [
            "平台规模扩大但无新社会制度范式",
            "数字工具普及但个体核心能力未升维",
            "经济增长但底层意义感不同步提升"
        ]

    def get_stage_analysis(self, stage: str) -> Dict:
        """获取阶段分析"""
        if stage == "早期":
            return self.early_stage
        else:
            return self.late_stage


# ============================================================================
# 主模块：T41跃迁定向与正负跃迁总控
# ============================================================================

class JumpDirectionAndPositiveNegativeModule(BaseTheoryModule):
    """
    T41 —— 六系跃迁定向与正负跃迁一体两面公理主模块

    整合四大新增公理、双线实证、工业化晚期分析
    """

    module_id = "T41"
    module_name = "六系跃迁定向与正负跃迁一体两面公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·跃迁定向与正负跃迁"
    corresponding_axiom = "四大新增公理"
    is_origin_locked = True
    dependencies = ["T38", "T39", "T40"]

    def __init__(self):
        super().__init__()
        # 初始化所有子模块
        self.selective = SelectiveDirectionalJumpAxiom()
        self.positive_negative = PositiveNegativeJumpAxiom()
        self.empty_burst = BaseOverflowEmptyBurstAxiom()
        self.path_dependence = PathDependenceInertiaAxiom()
        self.double_evidence = ContemporaryJuxianDoubleEvidence()
        self.late_industrial = LateIndustrializationAnalysis()

    def get_four_new_axioms(self) -> Dict:
        """获取四大新增公理总览"""
        return {
            "公理1": "选择定向跃迁公理（选择决定跃迁方向，亲缘决定意义本质）",
            "公理2": "正负跃迁一体两面公理（向上为正向下为负，同根同源）",
            "公理3": "基底溢出与意义空发公理（溢出无法传导，空发耗散）",
            "公理4": "路径依赖惯性公理（红利后惯性依赖→边际递减→五元锁死）"
        }

    def analyze_jump(self,
                     target_system: str,
                     utilization: float,
                     has_tiandao_breakthrough: bool,
                     has_ziran_foundation: bool,
                     has_upward_conduction: bool) -> Dict:
        """
        综合分析跃迁状态

        Args:
            target_system: 跃迁目标系
            utilization: 利用量
            has_tiandao_breakthrough: 是否带动天道突破
            has_ziran_foundation: 是否带动自然积淀
            has_upward_conduction: 是否有效向上传导
        Returns:
            综合分析结果
        """
        # 判断是否突破基底
        base_breakthrough = utilization > 100

        # 判断跃迁方向
        direction = self.positive_negative.determine_direction(
            has_tiandao_breakthrough, has_ziran_foundation
        )

        # 判断是否意义空发
        is_empty = self.empty_burst.is_empty_burst(
            utilization, has_upward_conduction, has_ziran_foundation
        )

        # 获取亲缘归属
        affiliation = self.selective.get_affinity_affiliation(target_system)

        return {
            "目标系": target_system,
            "利用量": utilization,
            "是否突破基底": base_breakthrough,
            "跃迁方向": direction.value,
            "是否意义空发": is_empty,
            "亲缘归属": affiliation,
            "结论": "选择决定跃迁方向，亲缘决定意义本质"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """守卫校验"""
        ok, errors = super().validate()

        # 验证四大公理
        four_axioms = self.get_four_new_axioms()
        if len(four_axioms) != 4:
            errors.append("[T41] 新增公理应为4条")

        # 验证意义空发特征
        if len(self.empty_burst.characteristics) != 6:
            errors.append("[T41] 意义空发特征应为6条")

        # 验证路径依赖机制
        if len(self.path_dependence.mechanism) != 6:
            errors.append("[T41] 路径依赖机制应为6步")

        return (len(errors) == 0, errors)


# ============================================================================
# 模块注册与便捷接口
# ============================================================================

def get_jump_direction_module() -> JumpDirectionAndPositiveNegativeModule:
    """获取跃迁定向模块实例"""
    return JumpDirectionAndPositiveNegativeModule()


def quick_jump_analysis(system: str, util: float) -> Dict:
    """
    快速跃迁分析（简化版）

    Args:
        system: 目标系名称
        util: 利用量
    Returns:
        简化分析结果
    """
    module = get_jump_direction_module()
    return module.analyze_jump(system, util, False, False, False)


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("T41 —— 六系跃迁定向与正负跃迁一体两面公理")
    print("=" * 60)

    module = get_jump_direction_module()

    # 测试1：四大公理
    print("\n【测试1】四大新增公理")
    four = module.get_four_new_axioms()
    for k, v in four.items():
        print(f"  {k}: {v}")

    # 测试2：选择定向
    print("\n【测试2】选择定向跃迁公理")
    print(f"  能否选择跃迁目标: {'能' if module.selective.can_select_jump_target() else '不能'}")
    print(f"  利用量溢出等于升维吗: {'等于' if module.selective.does_utilization_equal_upgrade() else '不等于'}")
    print(f"  具现系亲缘归属: {module.selective.get_affinity_affiliation('具现系')}")

    # 测试3：正负跃迁判定
    print("\n【测试3】正负跃迁判定")
    pos = module.positive_negative.determine_direction(True, True)
    print(f"  有天道突破+有自然积淀: {pos.value}")
    neg = module.positive_negative.determine_direction(False, False)
    print(f"  无天道突破+无自然积淀: {neg.value}")
    print(f"  正负跃迁同根同源: {'是' if module.positive_negative.is_same_origin() else '否'}")

    # 测试4：意义空发
    print("\n【测试4】意义空发判定")
    empty = module.empty_burst.is_empty_burst(150, False, False)
    print(f"  溢出50%+无向上传导+无向下沉淀: {'是' if empty else '否'}")

    # 测试5：路径依赖
    print("\n【测试5】路径依赖阶段")
    stage = module.path_dependence.get_inertia_stage(True, True, True)
    print(f"  红利结束+持续投入+边际递减: {stage}")
    print(f"  破局路径: {module.path_dependence.solution()}")

    # 测试6：综合跃迁分析
    print("\n【测试6】综合跃迁分析（当代具现系负值跃迁）")
    result = module.analyze_jump("具现系", 120, False, False, False)
    for k, v in result.items():
        print(f"  {k}: {v}")

    # 守卫校验
    print("\n【测试7】守卫校验")
    ok, errors = module.validate()
    print(f"  校验结果: {'✓ 通过' if ok else '✗ 失败'}")
    if errors:
        for e in errors:
            print(f"  错误: {e}")

    print("\n" + "=" * 60)
    print("T41模块验证完成!")
