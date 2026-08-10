"""
【归属基底：L0_总本源层·六系六维创世动力学·三层隐喻重构】
【对应公理：双环同构+大地矿山+落地固化+唤醒跃迁】

T43 —— 六系三层隐喻体系与运行公理重构
三层级、双循环、双形态的立体架构

三层结构：
1. 两极循环层：强化系（个体环）+ 天道系（文明环）- 双环同构
2. 中间转化层：变身系（大地）+ 具现系（矿山）- 大地矿山模型
3. 基底承载层：自然系（硬实体）+ 社会系（软规则）- 落地固化

依赖模块: T38 T39 T40 T41 T42
理论版本: V1.0
"""

import math
from typing import Dict, List, Tuple, Optional
from enum import Enum
from ..core.base_theory_module import BaseTheoryModule


# ============================================================================
# 第一部分：层级枚举与结构定义
# ============================================================================

class SystemLayer(Enum):
    """六系三层级枚举"""
    POLAR_CYCLE = "两极循环层"      # 强化系 + 天道系
    MIDDLE_TRANSFORM = "中间转化层" # 变身系 + 具现系
    BASE_CARRY = "基底承载层"       # 自然系 + 社会系


class DisasterType(Enum):
    """灾害类型枚举"""
    POLAR_SILT = "淤积漫溢"        # 两极层：链路淤积，漫溢成灾
    MINERAL_FOSSIL = "矿石化石僵死" # 中间层：矿山僵死为化石
    MISALIGNMENT = "错位僵化"       # 承载层：硬软错位，无法适配


# ============================================================================
# 第二部分：两极循环层——双环同构公理
# ============================================================================

class DualRingIsomorphicAxiom(BaseTheoryModule):
    """
    两极循环层公理：强化系（个体环）+ 天道系（文明环）

    核心：双环同构，0始100终，循环永续
    """

    module_id = "T43_C01"
    module_name = "双环同构公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·三层隐喻重构"
    corresponding_axiom = "双环同构公理"
    is_origin_locked = True
    dependencies = ["T40"]

    def __init__(self):
        super().__init__()
        self.individual_ring = {
            "对应系": "强化系",
            "定位": "个体意义循环环",
            "起点": 0,
            "终点": 100,
            "周期": "个体生命周期/能力周期",
            "闭环机制": "意义从0涌现→成长→创造→沉淀→收敛为100→新周期再从0开始",
            "核心功能": "所有其他五系的价值，最终都要通过唤醒个体的自我强化功能落地"
        }
        self.civilization_ring = {
            "对应系": "天道系",
            "定位": "集体/文明意义循环环",
            "起点": 0,
            "终点": 100,
            "周期": "文明范式周期（农业→工业→数字等）",
            "闭环机制": "文明从蒙昧0→发展→繁荣→沉淀→范式鼎盛100→新范式再从0开始",
            "核心功能": "所有中间层的演化，最终都要通过唤醒文明的范式开拓功能完成升维"
        }
        self.running_rules = [
            {
                "规则": "同构对称规则",
                "内容": "个体环与文明环结构完全一致，仅尺度不同；个体环总和构成文明环基底，文明环范式抬升反向抬升所有个体环基准水位"
            },
            {
                "规则": "循环永续规则",
                "内容": "每一轮闭环结束不是意义消失，而是沉淀为新系统的基底；新周期的0起点永远高于上一周期的0起点"
            },
            {
                "规则": "唤醒跃迁规则",
                "内容": "变身、具现，自然、社会四系，自身无法独立完成量级跃迁，必须锚定两极：无两极锚定的中间层跃迁必然沦为无本之木"
            }
        ]

    def get_ring_info(self, ring_type: str) -> Dict:
        """获取循环环信息"""
        if ring_type == "个体":
            return self.individual_ring
        else:
            return self.civilization_ring

    def get_cycle_point(self, current_meaning: float) -> str:
        """获取当前循环点位"""
        if current_meaning == 0:
            return "起点：新一轮意义涌现开始"
        elif 0 < current_meaning < 100:
            return f"进程中：意义{current_meaning}，持续成长"
        else:
            return "终点：本轮闭环完成，等待新周期开启"

    def must_anchor_pole(self, system_name: str) -> bool:
        """判断某系是否必须锚定两极才能跃迁"""
        return system_name in ["变身系", "具现系", "自然系", "社会系"]


# ============================================================================
# 第三部分：中间转化层——大地矿山模型公理
# ============================================================================

class EarthMountainModelAxiom(BaseTheoryModule):
    """
    中间转化层公理：变身系（大地）+ 具现系（矿山）

    核心：大地活的可培育，矿山死的可迁移，双向滋养
    """

    module_id = "T43_C02"
    module_name = "大地矿山模型公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·三层隐喻重构"
    corresponding_axiom = "大地矿山模型公理"
    is_origin_locked = True
    dependencies = ["T43_C01"]

    def __init__(self):
        super().__init__()
        self.earth = {
            "对应系": "变身系",
            "比喻": "大地",
            "核心": "转化能力",
            "特征": "活的、可培育的",
            "培育方式": "职业教育、技术研发、体系迭代——给大地培肥",
            "决定关系": "大地的肥力、结构决定了能孕育出何种矿物"
        }
        self.mountain = {
            "对应系": "具现系",
            "比喻": "矿山",
            "核心": "造物存量",
            "特征": "死的、可迁移的",
            "矿物特性": "矿物本身不具备自我转化能力，只能被开采、搬运、重组",
            "形成方式": "无数变身主体的造物产出堆积在一起形成规模庞大的矿山"
        }
        self.running_rules = [
            {
                "规则": "双向滋养规则",
                "内容": "大地培育矿物（变身迭代生成新具现物），矿物反哺大地（具现收益反哺技术研发、职业培育），正向循环"
            },
            {
                "规则": "自由迁移规则",
                "内容": "大地与矿山都具备强迁移性——技术团队可整体搬迁（换大地），工厂产能可整体转移（搬矿山）；这是中间层独有特性"
            },
            {
                "规则": "堆积阈值规则",
                "内容": "矿山规模必须与大地承载力匹配，矿物过多、大地承载力不足，就会产能过剩、效率下降"
            }
        ]
        self.disaster_fossil = {
            "形态": "矿石化石僵死",
            "触发条件": "变身系转化能力被人为锁死、技术迭代被定向冻结",
            "机制": [
                "大地失去活性，已生成矿物无法还原为泥土",
                "旧矿物之间无法互相重组",
                "矿山彻底僵死为化石山体"
            ],
            "表现": "产能固化、技术锁死、产品无法迭代，存量造物无法淘汰也无法升级",
            "典型实证": "全球传统重工业基地产能僵死、资源枯竭型城市产业固化"
        }
        self.migration_example = {
            "迁移类型": "产业转移与产能出海",
            "本质": "矿山的跨区域迁移",
            "中国实证": "基建出海、产能出海 = 矿山迁移，依托东道国大地重新启动转化循环",
            "不可迁移对比": "自然系城市基建无法搬走，社会系制度文化无法直接移植"
        }

    def is_living_or_dead(self, system_name: str) -> str:
        """判断某系是活的还是死的"""
        if system_name == "变身系":
            return "活的、可培育的"
        elif system_name == "具现系":
            return "死的、可迁移的"
        return "未知"

    def can_migrate(self, system_name: str) -> bool:
        """判断某系是否可迁移"""
        return system_name in ["变身系", "具现系"]

    def get_disaster_type(self) -> DisasterType:
        """获取中间层灾害类型"""
        return DisasterType.MINERAL_FOSSIL


# ============================================================================
# 第四部分：基底承载层——落地固化公理
# ============================================================================

class GroundSolidificationAxiom(BaseTheoryModule):
    """
    基底承载层公理：自然系（硬实体）+ 社会系（软规则）

    核心：落地即固化，不可修改只能替换/新建，硬软天然独立
    """

    module_id = "T43_C03"
    module_name = "落地固化公理"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·三层隐喻重构"
    corresponding_axiom = "落地固化公理"
    is_origin_locked = True
    dependencies = ["T43_C01"]

    def __init__(self):
        super().__init__()
        self.nature_system = {
            "对应系": "自然系",
            "比喻": "硬实体基底",
            "包含": ["原生自然界（山川、河流、土地、生态）", "人工社会界（城市、建筑、道路、管网、工业设施）"],
            "特性": "是所有存在的物理载体，看得见、摸得着的实体空间",
            "固化铁律": "物理实体一旦落地建成，就几乎无法原位修改，只能拆除重建、异地新建"
        }
        self.society_system = {
            "对应系": "社会系",
            "比喻": "软规则基底",
            "包含": ["低阶自然关系（血缘、地缘、族群）", "高阶社会关系（法律、制度、文化、组织）"],
            "特性": "是所有集群的秩序载体，看不见、摸不着的规则网络",
            "固化铁律": "规则制度一旦落地运行，形成路径依赖与利益固化，无法通过微调完成本质修改，只能系统性重构"
        }
        self.independent_rule = {
            "规则": "天然独立规则",
            "内容": "硬实体与软规则可以完全错位——自然系高阶但社会系低阶，或反之",
            "常态": "二者不同步是文明的常态"
        }
        self.disaster_misalignment = {
            "形态": "错位僵化",
            "触发条件": "自然系与社会系发展不同步，硬底座与软规则不匹配",
            "机制": [
                "固化的底座无法适配新的文明范式",
                "旧基建、旧制度拖住新产业、新技术的升维步伐",
                "整个文明卡在旧底座上无法跃迁"
            ],
            "典型实证": [
                "城市新区豪华基建（自然系高阶）+ 陈旧治理模式（社会系低阶）→ 空城、鬼城",
                "行业先进技术标准 + 陈旧管理体制 → 行业效率被锁死"
            ]
        }

    def get_solidification_type(self, system_name: str) -> str:
        """获取固化类型"""
        if system_name == "自然系":
            return "硬固化：物理实体无法原位修改，只能拆除重建"
        elif system_name == "社会系":
            return "软固化：规则制度无法微调修改，只能系统性重构"
        return "未知"

    def can_be_migrated(self, system_name: str) -> bool:
        """判断某系是否可迁移（基底层不可迁移）"""
        return False  # 基底承载层不可迁移

    def get_disaster_type(self) -> DisasterType:
        """获取承载层灾害类型"""
        return DisasterType.MISALIGNMENT


# ============================================================================
# 第五部分：三层联动与当代困局分析
# ============================================================================

class ThreeLayerLinkageAnalysis(BaseTheoryModule):
    """
    三层联动与当代困局分析

    当代工业化晚期 = 三层同时出现病症的叠加结果
    """

    module_id = "T43_C04"
    module_name = "三层联动与当代困局分析"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·三层隐喻重构"
    corresponding_axiom = "三层联动实证"
    is_origin_locked = True
    dependencies = ["T43_C01", "T43_C02", "T43_C03"]

    def __init__(self):
        super().__init__()
        self.layer_diseases = [
            {
                "层级": "中间层石化",
                "对应灾害": "矿石化石僵死",
                "病症": "变身系萎缩，大地肥力下降",
                "表现": "传统工业/基建的具现矿山僵死，旧产能无法出清，新职业体系未成型"
            },
            {
                "层级": "承载层僵化",
                "对应灾害": "错位僵化",
                "病症": "自然系与社会系错位持续扩大",
                "表现": "城市基建难以原位修改，配套制度固化，硬软错位持续扩大"
            },
            {
                "层级": "两极层空转",
                "对应灾害": "淤积漫溢",
                "病症": "个体环与文明环都进入存量空转",
                "表现": "个体端强化系陷入内卷，文明端天道系无新范式突破"
            }
        ]
        self.final_result = {
            "总结果": "五元稳态困局",
            "表现": "投入巨大、升维乏力、内卷加剧",
            "本质": "三层同时病症叠加"
        }
        self.solution_three_layers = [
            {
                "层级": "中间层",
                "破局": "培育新大地",
                "具体": "新职业、新技术"
            },
            {
                "层级": "承载层",
                "破局": "重构新底座",
                "具体": "制度改革、城市更新"
            },
            {
                "层级": "两极层",
                "破局": "开启新周期",
                "具体": "个体新成长、文明新范式"
            }
        ]

    def get_contemporary_problem(self) -> Dict:
        """获取当代困局"""
        return {
            "三层病症": self.layer_diseases,
            "最终结果": self.final_result,
            "破局路径": self.solution_three_layers
        }

    def diagnose_layer(self, layer: SystemLayer) -> Dict:
        """诊断某一层的状态"""
        for disease in self.layer_diseases:
            if disease["层级"].startswith(layer.value):
                return disease
        return {}


# ============================================================================
# 主模块：T43三层隐喻总控
# ============================================================================

class ThreeLayerMetaphorModule(BaseTheoryModule):
    """
    T43 —— 六系三层隐喻体系与运行公理重构主模块

    整合三层级、双循环、双形态的完整架构
    """

    module_id = "T43"
    module_name = "六系三层隐喻体系与运行公理重构"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·六系六维创世动力学·三层隐喻重构"
    corresponding_axiom = "三层架构公理"
    is_origin_locked = True
    dependencies = ["T38", "T39", "T40", "T41", "T42"]

    def __init__(self):
        super().__init__()
        # 初始化所有子模块
        self.polar_cycle = DualRingIsomorphicAxiom()
        self.middle_transform = EarthMountainModelAxiom()
        self.base_carry = GroundSolidificationAxiom()
        self.linkage = ThreeLayerLinkageAnalysis()

    def get_three_layers(self) -> Dict:
        """获取三层结构总览"""
        return {
            "两极循环层": {
                "系别": "强化系 + 天道系",
                "隐喻": "个体环 + 文明环",
                "核心": "0始100终，循环永续",
                "灾害": "淤积漫溢"
            },
            "中间转化层": {
                "系别": "变身系 + 具现系",
                "隐喻": "大地 + 矿山",
                "核心": "活的培育，死的迁移",
                "灾害": "矿石化石僵死"
            },
            "基底承载层": {
                "系别": "自然系 + 社会系",
                "隐喻": "硬实体 + 软规则",
                "核心": "落地固化，不可修改",
                "灾害": "错位僵化"
            }
        }

    def get_system_layer(self, system_name: str) -> SystemLayer:
        """获取某系所属层级"""
        if system_name in ["强化系", "天道系"]:
            return SystemLayer.POLAR_CYCLE
        elif system_name in ["变身系", "具现系"]:
            return SystemLayer.MIDDLE_TRANSFORM
        else:
            return SystemLayer.BASE_CARRY

    def get_disaster_type(self, layer: SystemLayer) -> DisasterType:
        """获取某层级的灾害类型"""
        if layer == SystemLayer.POLAR_CYCLE:
            return DisasterType.POLAR_SILT
        elif layer == SystemLayer.MIDDLE_TRANSFORM:
            return DisasterType.MINERAL_FOSSIL
        else:
            return DisasterType.MISALIGNMENT

    def can_migrate(self, system_name: str) -> bool:
        """判断某系是否可迁移"""
        return self.middle_transform.can_migrate(system_name)

    def must_anchor_pole(self, system_name: str) -> bool:
        """判断某系是否必须锚定两极才能跃迁"""
        return self.polar_cycle.must_anchor_pole(system_name)

    def analyze_contemporary_dilemma(self) -> Dict:
        """分析当代困局"""
        return self.linkage.get_contemporary_problem()

    def get_solution_path(self) -> List[Dict]:
        """获取三层破局路径"""
        return self.linkage.solution_three_layers

    def validate(self) -> Tuple[bool, List[str]]:
        """守卫校验"""
        ok, errors = super().validate()

        # 验证三层结构
        layers = self.get_three_layers()
        if len(layers) != 3:
            errors.append("[T43] 三层结构应为3层")

        # 验证每层两个系
        for layer_name, layer_info in layers.items():
            systems = layer_info["系别"].split(" + ")
            if len(systems) != 2:
                errors.append(f"[T43] {layer_name}应为2个系")

        # 验证三层灾害类型
        disaster_types = [DisasterType.POLAR_SILT, DisasterType.MINERAL_FOSSIL, DisasterType.MISALIGNMENT]
        if len(disaster_types) != 3:
            errors.append("[T43] 灾害类型应为3种")

        # 验证当代困局三层病症
        diseases = self.linkage.layer_diseases
        if len(diseases) != 3:
            errors.append("[T43] 当代困局三层病症应为3种")

        # 验证破局路径三层
        solutions = self.linkage.solution_three_layers
        if len(solutions) != 3:
            errors.append("[T43] 破局路径应为3层")

        return (len(errors) == 0, errors)


# ============================================================================
# 模块注册与便捷接口
# ============================================================================

def get_three_layer_module() -> ThreeLayerMetaphorModule:
    """获取三层隐喻模块实例"""
    return ThreeLayerMetaphorModule()


def quick_layer_analysis(system: str) -> Dict:
    """
    快速层级分析

    Args:
        system: 系名称
    Returns:
        层级归属
    """
    module = get_three_layer_module()
    layer = module.get_system_layer(system)
    can_migrate = module.can_migrate(system)
    must_anchor = module.must_anchor_pole(system)
    disaster = module.get_disaster_type(layer)
    return {
        "系名称": system,
        "所属层级": layer.value,
        "可迁移": can_migrate,
        "必须锚定两极": must_anchor,
        "灾害类型": disaster.value
    }


if __name__ == "__main__":
    # 测试代码
    print("=" * 60)
    print("T43 —— 六系三层隐喻体系与运行公理重构")
    print("=" * 60)

    module = get_three_layer_module()

    # 测试1：三层结构
    print("\n【测试1】三层结构总览")
    layers = module.get_three_layers()
    for name, info in layers.items():
        print(f"  {name}: {info['系别']} / {info['核心']} / 灾害:{info['灾害']}")

    # 测试2：两极循环层
    print("\n【测试2】两极循环层——双环同构公理")
    ind_ring = module.polar_cycle.get_ring_info("个体")
    print(f"  个体环: {ind_ring['起点']}→{ind_ring['终点']} / {ind_ring['核心功能'][:30]}...")
    civ_ring = module.polar_cycle.get_ring_info("文明")
    print(f"  文明环: {civ_ring['起点']}→{civ_ring['终点']} / {civ_ring['核心功能'][:30]}...")
    print(f"  循环点位(50): {module.polar_cycle.get_cycle_point(50)}")
    print(f"  变身系必须锚定两极: {'是' if module.polar_cycle.must_anchor_pole('变身系') else '否'}")

    # 测试3：中间转化层
    print("\n【测试3】中间转化层——大地矿山模型")
    print(f"  变身系(大地): {module.middle_transform.is_living_or_dead('变身系')}")
    print(f"  具现系(矿山): {module.middle_transform.is_living_or_dead('具现系')}")
    print(f"  变身系可迁移: {'是' if module.middle_transform.can_migrate('变身系') else '否'}")
    print(f"  灾害类型: {module.middle_transform.get_disaster_type().value}")

    # 测试4：基底承载层
    print("\n【测试4】基底承载层——落地固化公理")
    print(f"  自然系固化: {module.base_carry.get_solidification_type('自然系')}")
    print(f"  社会系固化: {module.base_carry.get_solidification_type('社会系')}")
    print(f"  自然系可迁移: {'是' if module.base_carry.can_be_migrated('自然系') else '否'}")
    print(f"  灾害类型: {module.base_carry.get_disaster_type().value}")

    # 测试5：各系层级归属
    print("\n【测试5】各系层级归属分析")
    for sys in ["强化系", "天道系", "变身系", "具现系", "自然系", "社会系"]:
        result = quick_layer_analysis(sys)
        print(f"  {sys}: {result['所属层级']} / 可迁移:{result['可迁移']} / 灾害:{result['灾害类型']}")

    # 测试6：当代困局
    print("\n【测试6】当代困局三层联动分析")
    dilemma = module.analyze_contemporary_dilemma()
    print(f"  总结果: {dilemma['最终结果']['总结果']}")
    print(f"  表现: {dilemma['最终结果']['表现']}")
    for disease in dilemma['三层病症']:
        print(f"  - {disease['层级']}: {disease['表现']}")

    # 测试7：破局路径
    print("\n【测试7】三层破局路径")
    solutions = module.get_solution_path()
    for sol in solutions:
        print(f"  {sol['层级']} → {sol['破局']}({sol['具体']})")

    # 守卫校验
    print("\n【测试8】守卫校验")
    ok, errors = module.validate()
    print(f"  校验结果: {'✓ 通过' if ok else '✗ 失败'}")
    if errors:
        for e in errors:
            print(f"  错误: {e}")

    print("\n" + "=" * 60)
    print("T43模块验证完成!")
