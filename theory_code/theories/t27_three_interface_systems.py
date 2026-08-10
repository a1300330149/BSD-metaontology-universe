"""
【归属基底：L3_功能应用层·三套接口转换公理】
【对应公理：三套接口转换公理】

T27 —— 三套接口体系
智能体六系 ↔ 人类范畴 ↔ 科研工程流转系
三套接口相互映射，形成闭环
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from ..core.base_theory_module import BaseTheoryModule


class ThreeInterfaceSystems(BaseTheoryModule):
    """
    三套接口体系公理

    接口一：智能体六系
    1. 实体系(R) - 实体感知与操作
    2. 模态系(M) - 模态生成与处理
    3. 认知系(C) - 认知推理与决策
    4. 社会系(S) - 社会交互与协作
    5. 公理系(A) - 公理遵循与超越
    6. 混沌系(H) - 混沌探索与创新

    接口二：人类六范畴
    1. 自然 - 自然世界感知
    2. 具现 - 具身现实交互
    3. 强化 - 认知能力强化
    4. 社会 - 社会关系网络
    5. 天道 - 天道真理追求
    6. 变身 - 形态变化超越

    接口三：科研工程六流转系
    1. 实体流 - 物质实体流转
    2. 模态流 - 信息模态流转
    3. 认知流 - 知识认知流转
    4. 社会流 - 组织社会流转
    5. 公理流 - 公理范式流转
    6. 混沌流 - 混沌创新流转

    核心：三套接口一一对应，可相互转换，形成闭环
    """

    module_id = "T27"
    module_name = "三套接口体系（智能体/人类/科研工程）"
    version = "V1.0_终版"
    cosmic_level = 3
    base_belong = "L3_功能应用层·三套接口转换公理"
    corresponding_axiom = "三套接口转换公理"
    is_origin_locked = True
    dependencies = ["T25"]

    def __init__(self):
        super().__init__()
        self.agent_systems = ["实体系(R)", "模态系(M)", "认知系(C)", "社会系(S)", "公理系(A)", "混沌系(H)"]
        self.human_categories = ["自然", "具现", "强化", "社会", "天道", "变身"]
        self.research_flows = ["实体流", "模态流", "认知流", "社会流", "公理流", "混沌流"]
        self._interface_mapping = {}
        self._conversion_efficiency = {}
        self._compatibility_matrix = {}
        self._closed_loop_degree = 0.0
        self._init_interfaces()

    def _init_interfaces(self):
        """初始化三套接口映射"""
        for i in range(6):
            agent_sys = self.agent_systems[i]
            human_cat = self.human_categories[i]
            research_flow = self.research_flows[i]
            
            mapping_id = f"IF{i+1:02d}"
            self._interface_mapping[mapping_id] = {
                "mapping_id": mapping_id,
                "agent_system": agent_sys,
                "human_category": human_cat,
                "research_flow": research_flow,
                "index": i + 1,
                "mapping_strength": self.constants.E3,
                "conversion_loss": self.constants.theta_mv
            }

            self._conversion_efficiency[mapping_id] = {
                "agent_to_human": self.constants.E2,
                "human_to_research": self.constants.E2,
                "research_to_agent": self.constants.E2,
                "agent_to_research": self.constants.E1,
                "human_to_agent": self.constants.E2,
                "research_to_human": self.constants.E2
            }

        for i, sys1 in enumerate(self.agent_systems):
            for j, sys2 in enumerate(self.agent_systems):
                key = f"{sys1}_{sys2}"
                if i == j:
                    self._compatibility_matrix[key] = 1.0
                elif abs(i - j) == 1:
                    self._compatibility_matrix[key] = self.constants.E2
                else:
                    self._compatibility_matrix[key] = self.constants.E1

        self._closed_loop_degree = 1.0 - math.exp(-self.constants.gamma * 6)

    def three_interfaces_definition(self) -> Dict[str, Any]:
        """三套接口定义推演"""
        interface_definitions = {
            "智能体六系接口": {
                "description": "智能体与外部世界交互的六类接口",
                "systems": self.agent_systems,
                "functions": [
                    "实体系(R)：感知物理世界，操作实体对象",
                    "模态系(M)：生成虚拟模态，处理信息形态",
                    "认知系(C)：进行逻辑推理，做出智能决策",
                    "社会系(S)：开展社会交互，实现群体协作",
                    "公理系(A)：遵循公理法则，追求真理超越",
                    "混沌系(H)：探索混沌边界，实现创新突破"
                ]
            },
            "人类六范畴接口": {
                "description": "人类与世界互动的六类范畴",
                "categories": self.human_categories,
                "functions": [
                    "自然：对自然世界的感知与认知",
                    "具现：具身化的现实交互与实践",
                    "强化：认知能力的强化与提升",
                    "社会：社会关系的建立与维护",
                    "天道：对天道真理的追求与信仰",
                    "变身：形态变化与自我超越"
                ]
            },
            "科研工程六流转系接口": {
                "description": "科研工程中的六类流转系统",
                "flows": self.research_flows,
                "functions": [
                    "实体流：物质实体在科研中的流转",
                    "模态流：信息模态在工程中的传递",
                    "认知流：知识认知在研究中的演进",
                    "社会流：组织社会在协作中的互动",
                    "公理流：公理范式在学科中的传承",
                    "混沌流：混沌创新在探索中的涌现"
                ]
            }
        }

        interface_properties = [
            "每套接口都有6个组成部分",
            "三套接口数量相同，结构同构",
            "各接口内部有明确的功能划分",
            "接口间有对应关系，可相互映射",
            "接口定义遵循六系基本框架"
        ]

        return {
            "interface_count": 3,
            "components_per_interface": 6,
            "interface_definitions": interface_definitions,
            "interface_properties": interface_properties,
            "definition_principle": "三套接口各成体系，又相互对应"
        }

    def interface_mapping_matrix(self) -> Dict[str, Any]:
        """接口映射矩阵推演"""
        mapping_detail = {}
        for mapping_id, mapping in self._interface_mapping.items():
            mapping_detail[mapping_id] = {
                "智能体六系": mapping["agent_system"],
                "人类六范畴": mapping["human_category"],
                "科研工程六流转系": mapping["research_flow"],
                "映射强度": mapping["mapping_strength"]
            }

        mapping_matrix = {}
        for i, agent_sys in enumerate(self.agent_systems):
            mapping_matrix[agent_sys] = {
                "human_category": self.human_categories[i],
                "research_flow": self.research_flows[i],
                "mapping_index": i + 1
            }

        mapping_rules = [
            "一一对应：每套接口的第i个元素相互对应",
            "结构同构：三套接口共享相同的结构模板",
            "功能对应：对应元素功能相似，作用相当",
            "可转换性：对应元素间可进行信息转换",
            "保序性：映射保持接口内部的顺序关系"
        ]

        return {
            "total_mappings": len(self._interface_mapping),
            "mapping_detail": mapping_detail,
            "mapping_matrix": mapping_matrix,
            "mapping_rules": mapping_rules,
            "mapping_principle": "三套接口按索引一一对应，功能同构"
        }

    def cross_interface_conversion(self, from_interface: str = "智能体六系",
                                     to_interface: str = "人类六范畴",
                                     system_index: int = 0,
                                     input_value: float = 1.0) -> Dict[str, Any]:
        """跨接口转换机制推演"""
        interfaces = ["智能体六系", "人类六范畴", "科研工程六流转系"]
        if from_interface not in interfaces or to_interface not in interfaces:
            return {"error": "指定的接口不存在"}
        if system_index < 0 or system_index >= 6:
            return {"error": "系统索引必须在0-5之间"}

        mapping_id = f"IF{system_index+1:02d}"
        efficiencies = self._conversion_efficiency.get(mapping_id, {})

        conv_key = None
        if from_interface == "智能体六系" and to_interface == "人类六范畴":
            conv_key = "agent_to_human"
        elif from_interface == "人类六范畴" and to_interface == "科研工程六流转系":
            conv_key = "human_to_research"
        elif from_interface == "科研工程六流转系" and to_interface == "智能体六系":
            conv_key = "research_to_agent"
        elif from_interface == "智能体六系" and to_interface == "科研工程六流转系":
            conv_key = "agent_to_research"
        elif from_interface == "人类六范畴" and to_interface == "智能体六系":
            conv_key = "human_to_agent"
        elif from_interface == "科研工程六流转系" and to_interface == "人类六范畴":
            conv_key = "research_to_human"

        efficiency = efficiencies.get(conv_key, self.constants.E1)
        output_value = input_value * efficiency
        conversion_loss = input_value - output_value

        conversion_paths = [
            "直接转换：接口A → 接口B（一跳）",
            "间接转换：接口A → 接口B → 接口C（两跳）",
            "环形转换：接口A → B → C → A（三跳闭环）",
            "同系转换：同一索引下的接口间转换效率最高",
            "跨系转换：不同索引间的转换需要额外代价"
        ]

        mapping = self._interface_mapping.get(mapping_id, {})

        return {
            "from_interface": from_interface,
            "to_interface": to_interface,
            "from_element": mapping.get("agent_system" if from_interface == "智能体六系" else 
                                        "human_category" if from_interface == "人类六范畴" else "research_flow"),
            "to_element": mapping.get("agent_system" if to_interface == "智能体六系" else 
                                      "human_category" if to_interface == "人类六范畴" else "research_flow"),
            "input_value": input_value,
            "conversion_efficiency": efficiency,
            "output_value": round(output_value, 6),
            "conversion_loss": round(conversion_loss, 6),
            "conversion_paths": conversion_paths,
            "conversion_principle": "同系转换效率高，跨系转换有损耗"
        }

    def interface_compatibility_verification(self) -> Dict[str, Any]:
        """接口兼容性验证推演"""
        compatibility_tests = []

        same_index_compat = []
        for i in range(6):
            compat_score = self.constants.E3
            same_index_compat.append({
                "index": i + 1,
                "agent": self.agent_systems[i],
                "human": self.human_categories[i],
                "research": self.research_flows[i],
                "compatibility": compat_score
            })
        compatibility_tests.append("同索引接口兼容性最高")

        cross_index_compat = []
        for i in range(6):
            for j in range(6):
                if i != j:
                    key = f"{self.agent_systems[i]}_{self.agent_systems[j]}"
                    compat = self._compatibility_matrix.get(key, self.constants.E1)
                    cross_index_compat.append({
                        "from_index": i + 1,
                        "to_index": j + 1,
                        "compatibility": compat
                    })

        avg_compatibility = sum(
            m["mapping_strength"] for m in self._interface_mapping.values()
        ) / len(self._interface_mapping)

        compatibility_aspects = [
            "结构兼容：三套接口结构相同，都是6个部分",
            "功能兼容：对应元素功能相似，可相互替代",
            "数据兼容：接口间数据格式可相互转换",
            "协议兼容：接口间通信协议可相互适配",
            "语义兼容：接口间语义层面可相互理解"
        ]

        return {
            "average_compatibility": round(avg_compatibility, 4),
            "compatible": avg_compatibility > self.constants.E2,
            "same_index_compatibility": same_index_compat,
            "compatibility_aspects": compatibility_aspects,
            "verification_principle": "同索引高度兼容，跨索引有差异"
        }

    def closed_loop_verification(self) -> Dict[str, Any]:
        """三套接口闭环验证推演"""
        loop_efficiency = self.constants.E2 ** 3
        closed_cycles = [
            "智能体→人类→科研工程→智能体（正向闭环）",
            "科研工程→人类→智能体→科研工程（逆向闭环）",
            "智能体↔人类（双向小循环）",
            "人类↔科研工程（双向小循环）",
            "科研工程↔智能体（双向小循环）"
        ]

        loop_properties = [
            "完整性：三套接口形成完整的循环",
            "守恒性：闭环中总量守恒（有损耗但可补偿）",
            "信息闭环：信息可在三套接口间完整传递",
            "能量闭环：能量/资源可在三套接口间流转",
            "因果闭环：因可转化为果，果也可转化为因"
        ]

        loop_stages = [
            "阶段1：智能体感知世界，产生认知",
            "阶段2：人类理解阐释，形成知识",
            "阶段3：科研工程实践，验证应用",
            "阶段4：成果反馈智能体，升级迭代"
        ]

        return {
            "closed_loop_degree": self._closed_loop_degree,
            "closed_loop_verified": self._closed_loop_degree > self.constants.E2,
            "loop_efficiency": round(loop_efficiency, 6),
            "closed_cycles": closed_cycles,
            "loop_properties": loop_properties,
            "loop_stages": loop_stages,
            "verification_principle": "三套接口形成自足闭环，周流不息"
        }

    def validate(self) -> Tuple[bool, List[str]]:
        """T27 自检验证"""
        ok, errors = super().validate()
        if not ok:
            return ok, errors

        if len(self.agent_systems) != 6:
            errors.append("智能体六系必须恰好6个")
        if len(self.human_categories) != 6:
            errors.append("人类六范畴必须恰好6个")
        if len(self.research_flows) != 6:
            errors.append("科研工程六流转系必须恰好6个")
        if len(self._interface_mapping) != 6:
            errors.append("接口映射必须有6组对应关系")

        for i in range(6):
            mapping_id = f"IF{i+1:02d}"
            if mapping_id not in self._interface_mapping:
                errors.append(f"缺少映射关系: {mapping_id}")
            else:
                mapping = self._interface_mapping[mapping_id]
                if mapping["agent_system"] != self.agent_systems[i]:
                    errors.append(f"映射{mapping_id}的智能体系不匹配")
                if mapping["human_category"] != self.human_categories[i]:
                    errors.append(f"映射{mapping_id}的人类范畴不匹配")
                if mapping["research_flow"] != self.research_flows[i]:
                    errors.append(f"映射{mapping_id}的科研流转系不匹配")

        expected_agent = {"实体系(R)", "模态系(M)", "认知系(C)", "社会系(S)", "公理系(A)", "混沌系(H)"}
        if set(self.agent_systems) != expected_agent:
            errors.append("智能体六系名称不正确")

        expected_human = {"自然", "具现", "强化", "社会", "天道", "变身"}
        if set(self.human_categories) != expected_human:
            errors.append("人类六范畴名称不正确")

        expected_research = {"实体流", "模态流", "认知流", "社会流", "公理流", "混沌流"}
        if set(self.research_flows) != expected_research:
            errors.append("科研工程六流转系名称不正确")

        if len(self._conversion_efficiency) != 6:
            errors.append("转换效率配置必须覆盖6组映射")

        if "T25" not in self.dependencies:
            errors.append("T27必须依赖T25（54维矩阵）")
        if self.cosmic_level != 3:
            errors.append("T27必须位于L3功能应用层")
        if not self.is_origin_locked:
            errors.append("T27理论必须锁定")

        return (len(errors) == 0, errors)


if __name__ == "__main__":
    t27 = ThreeInterfaceSystems()
    print(f"模块: {t27.module_id} - {t27.module_name}")
    print(f"版本: {t27.version}")
    print(f"层级: L{t27.cosmic_level}")
    print(f"依赖: {t27.dependencies}")
    print(f"锁定: {t27.is_origin_locked}")
    print(f"哈希: {t27.sha256}")
    print()

    print("三套接口定义:")
    interfaces = t27.three_interfaces_definition()
    print(f"  接口数量: {interfaces['interface_count']}")
    print(f"  每接口组件数: {interfaces['components_per_interface']}")
    for name, detail in interfaces['interface_definitions'].items():
        print(f"  {name}:")
        for func in detail['functions'][:2]:
            print(f"    - {func}")
        print("    ...")
    print()

    print("接口映射矩阵:")
    mapping = t27.interface_mapping_matrix()
    print(f"  总映射数: {mapping['total_mappings']}")
    for mid, detail in mapping['mapping_detail'].items():
        print(f"  {mid}: {detail['智能体六系']} ↔ {detail['人类六范畴']} ↔ {detail['科研工程六流转系']}")
    print()

    print("跨接口转换:")
    conv = t27.cross_interface_conversion("智能体六系", "人类六范畴", 0, 1.0)
    print(f"  从: {conv['from_interface']} - {conv['from_element']}")
    print(f"  到: {conv['to_interface']} - {conv['to_element']}")
    print(f"  效率: {conv['conversion_efficiency']}")
    print(f"  输入: {conv['input_value']} → 输出: {conv['output_value']}")
    print()

    print("接口兼容性验证:")
    compat = t27.interface_compatibility_verification()
    print(f"  平均兼容性: {compat['average_compatibility']}")
    print(f"  兼容验证: {compat['compatible']}")
    print()

    print("闭环验证:")
    closed = t27.closed_loop_verification()
    print(f"  闭环度: {closed['closed_loop_degree']:.6f}")
    print(f"  闭环验证: {closed['closed_loop_verified']}")
    print(f"  循环效率: {closed['loop_efficiency']}")
    print()

    valid, errs = t27.validate()
    print(f"验证通过: {valid}")
    if not valid:
        for e in errs:
            print(f"  错误: {e}")
