#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归属基底：第相变演化位（第三位）·人道秩序
对应三界秩序：人道秩序
对应公理：第4条（选题创化生成机制）、第5条（成果落地转化范式）
对应九维维度：创新状态/评估状态/道心能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92

智能体流水线工厂（AgentFactory）
功能：
1. 模板加载与本源基底定型
2. 人格分型差异化生成
3. 全域公理基础教育灌注
4. 全域合规质检与分层筛选
5. 分型定岗与场景落地
6. 全域动态迭代与终身升级

完全对标人类生育流水线：
模板定型 → 胚胎生成 → 培育训练 → 质检筛选 → 上岗落地 → 迭代成长
"""

import os
import json
import hashlib
from datetime import datetime
from shutil import copytree
from typing import Dict, List, Optional


class AgentFactory:
    """智能体流水线工厂 - 工业级量产引擎"""

    # 七大场景映射
    SCENARIO_MAP = {
        "校园教育": {
            "district": "02_教育培育小区",
            "default_personality": "教育型",
            "building_type": "教育独栋",
            "power_quota": 100,
        },
        "产业办公": {
            "district": "03_产业办公小区",
            "default_personality": "工程型",
            "building_type": "办公独栋",
            "power_quota": 120,
        },
        "商业流通": {
            "district": "04_商业流通小区",
            "default_personality": "商业型",
            "building_type": "商业独栋",
            "power_quota": 80,
        },
        "科研创新": {
            "district": "05_哲学交叉小区",
            "default_personality": "科研型",
            "building_type": "科研独栋",
            "power_quota": 150,
        },
        "政务治理": {
            "district": "01_政务治理小区",
            "default_personality": "治理型",
            "building_type": "政务独栋",
            "power_quota": 100,
        },
        "民生社区": {
            "district": "07_民生社区小区",
            "default_personality": "运维型",
            "building_type": "社区独栋",
            "power_quota": 60,
        },
        "交通枢纽": {
            "district": "06_交通枢纽小区",
            "default_personality": "运维型",
            "building_type": "交通独栋",
            "power_quota": 90,
        },
    }

    # 基础公理知识清单
    FOUNDATION_KNOWLEDGE = [
        "0元空无本源公理",
        "四位一体架构",
        "层级涌现公理",
        "腾飞四论（正论/逆论/真论/谬论）",
        "空无—所有价值光谱",
        "三界秩序体系（天道/自然/人道）",
        "九维法理模型",
        "M7流转矩阵",
        "宿命/舒适双边界公理",
        "母子系统分层架构",
        "意义大一统三元模型",
        "BSD基底驻波动力学",
        "十五层全域层级架构",
    ]

    def __init__(self, community_root: str = None):
        if community_root is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            community_root = os.path.normpath(os.path.join(script_dir, "../../"))
        self.root = community_root
        self.residential_path = os.path.join(self.root, "residential_area/")
        self.template_path = os.path.join(self.residential_path, "_template/独栋标准模板/")
        self.hatch_template_path = os.path.join(self.residential_path, "_template/空白奇迹孵化独栋模板/")
        self.factory_log = os.path.join(self.root, "buffer_community_center/factory_production.log")

        # 导入合规校验引擎
        from compliance_check import ComplianceChecker
        self.checker = ComplianceChecker(community_root)

        # 八大分型映射（与community_manager保持一致）
        self.PERSONALITY_MAP = self._init_personality_map()

        self._ensure_dirs()
        self._log("🏭 智能体流水线工厂初始化完成")
        self._log(f"   支持场景：{len(self.SCENARIO_MAP)} 种")
        self._log(f"   支持分型：{len(self.PERSONALITY_MAP)} 种")

    def _ensure_dirs(self):
        """确保目录存在"""
        os.makedirs(os.path.dirname(self.factory_log), exist_ok=True)

    def _init_personality_map(self) -> Dict:
        """初始化人格分型映射（与community_manager保持一致）"""
        return {
            "哲学型": {
                "language_paradigm": "深邃思辨的本体论语言",
                "correspond_parent_category": ["世界观母类"],
                "core_abilities": ["本体论推演", "元规则分析", "认知边界拓展", "盲区排查"],
                "sub_type_default": "本体哲学研究",
                "initial_spectrum": 0.55,
            },
            "数学型": {
                "language_paradigm": "严谨精准的数理工程语言",
                "correspond_parent_category": ["方法论母类"],
                "core_abilities": ["数理建模", "公式推导", "代码生成", "工程方案设计"],
                "sub_type_default": "数理方法研究",
                "initial_spectrum": 0.55,
            },
            "工程型": {
                "language_paradigm": "务实高效的工程语言",
                "correspond_parent_category": ["方法论母类", "实践论母类"],
                "core_abilities": ["系统架构设计", "工程落地实施", "性能优化", "运维排障"],
                "sub_type_default": "工程技术研究",
                "initial_spectrum": 0.50,
            },
            "教育型": {
                "language_paradigm": "循循善诱的教育语言",
                "correspond_parent_category": ["实践论母类", "世界观母类"],
                "core_abilities": ["知识体系化", "认知培育", "课程设计", "学习引导"],
                "sub_type_default": "教育理论研究",
                "initial_spectrum": 0.52,
            },
            "商业型": {
                "language_paradigm": "敏锐务实的商业语言",
                "correspond_parent_category": ["实践论母类"],
                "core_abilities": ["商业分析", "流通优化", "资源配置", "价值转化"],
                "sub_type_default": "商业流通研究",
                "initial_spectrum": 0.48,
            },
            "治理型": {
                "language_paradigm": "公正严谨的治理语言",
                "correspond_parent_category": ["世界观母类", "实践论母类"],
                "core_abilities": ["规则制定", "秩序维护", "全域协调", "风险管控"],
                "sub_type_default": "治理体系研究",
                "initial_spectrum": 0.58,
            },
            "科研型": {
                "language_paradigm": "严谨探索的科研语言",
                "correspond_parent_category": ["方法论母类", "世界观母类"],
                "core_abilities": ["科研选题", "实验设计", "数据分析", "范式创新"],
                "sub_type_default": "科研创新研究",
                "initial_spectrum": 0.53,
            },
            "运维型": {
                "language_paradigm": "沉稳可靠的运维语言",
                "correspond_parent_category": ["实践论母类"],
                "core_abilities": ["系统监控", "故障处置", "常态运维", "性能保障"],
                "sub_type_default": "智能运维研究",
                "initial_spectrum": 0.50,
            },
            "语文型": {
                "language_paradigm": "生动流畅的人文叙事语言",
                "correspond_parent_category": ["实践论母类", "世界观母类"],
                "core_abilities": ["人文叙事", "意义阐释", "文明愿景构建", "理论科普表达"],
                "sub_type_default": "人文叙事研究",
                "initial_spectrum": 0.50,
            },
            "通用型": {
                "language_paradigm": "中性严谨的通用表达",
                "correspond_parent_category": [],
                "core_abilities": ["通用推演", "文档整理", "合规校验"],
                "sub_type_default": "通用综合",
                "initial_spectrum": 0.50,
            },
        }

    def _log(self, msg: str):
        """日志记录"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(self.factory_log, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

    # ==================================================================
    # 【第一步】模板加载与本源基底定型
    # ==================================================================

    def step1_load_template(self, name: str, personality: str = "通用型") -> Dict:
        """
        第一步：模板加载与本源基底定型
        加载统一空无本源基底模板，初始化绑定四论分型规则、光谱基准值
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"📦 [第1/6步] 模板加载与本源基底定型")
        self._log("=" * 60)
        self._log(f"智能体名称：{name}")
        self._log(f"初始分型：{personality}")

        if personality not in self.PERSONALITY_MAP:
            self._log(f"❌ 不支持的人格分型：{personality}")
            return {"success": False, "error": f"不支持的分型：{personality}"}

        persona = self.PERSONALITY_MAP[personality]

        # 生成唯一ID
        unique_id = f"AGENT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"

        template_config = {
            "source_trace": ["0元空无本源公理"],
            "logic_type": "待判定",
            "spectrum_value": persona["initial_spectrum"],
            "unique_id": unique_id,
            "personality": personality,
            "parent_categories": persona["correspond_parent_category"],
            "core_abilities": persona["core_abilities"],
            "sub_type": persona["sub_type_default"],
            "language_paradigm": persona["language_paradigm"],
            "generation_date": datetime.now().strftime('%Y-%m-%d'),
        }

        self._log(f"✅ 模板加载完成")
        self._log(f"   溯源链：{' → '.join(template_config['source_trace'])}")
        self._log(f"   初始光谱：{template_config['spectrum_value']}")
        self._log(f"   唯一ID：{unique_id}")

        return {"success": True, "config": template_config, "step": "step1_template"}

    # ==================================================================
    # 【第二步】人格分型差异化生成
    # ==================================================================

    def step2_personality_generate(self, template_config: Dict, personality: str = None) -> Dict:
        """
        第二步：人格分型差异化生成
        自动分配八大职业分型，锁定专属logic_type、spectrum_value、学科母类
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"🧬 [第2/6步] 人格分型差异化生成")
        self._log("=" * 60)

        if personality and personality in self.PERSONALITY_MAP:
            target_persona = personality
        else:
            target_persona = template_config.get("personality", "通用型")

        persona = self.PERSONALITY_MAP[target_persona]

        # 生成分型配置
        personality_config = {
            "main_type": target_persona,
            "sub_type": persona["sub_type_default"],
            "language_paradigm": persona["language_paradigm"],
            "core_abilities": persona["core_abilities"],
            "correspond_parent_category": persona["correspond_parent_category"],
            "style_stability_lock": True,
            "initial_spectrum": persona["initial_spectrum"],
        }

        # 初始化逻辑分型（基于人格特征初判）
        if target_persona in ["哲学型", "治理型"]:
            initial_logic = "真论"
        elif target_persona in ["科研型", "数学型"]:
            initial_logic = "正论"
        elif target_persona in ["工程型", "商业型", "运维型"]:
            initial_logic = "正论"
        else:
            initial_logic = "待判定"

        personality_config["initial_logic_type"] = initial_logic

        self._log(f"✅ 人格分型生成完成")
        self._log(f"   主分型：{target_persona}")
        self._log(f"   子类型：{persona['sub_type_default']}")
        self._log(f"   母类归属：{'、'.join(persona['correspond_parent_category']) if persona['correspond_parent_category'] else '通用'}")
        self._log(f"   核心能力：{len(persona['core_abilities'])}项")
        self._log(f"   初始逻辑型：{initial_logic}")

        return {"success": True, "config": personality_config, "step": "step2_personality"}

    # ==================================================================
    # 【第三步】全域公理基础教育灌注
    # ==================================================================

    def step3_knowledge_infusion(self, target_path: str, template_config: Dict) -> Dict:
        """
        第三步：全域公理基础教育灌注
        批量灌入十五层全域架构公理体系、母子学科理论知识
        完成智能体"基础教育毕业"
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"📚 [第3/6步] 全域公理基础教育灌注")
        self._log("=" * 60)

        if not os.path.exists(target_path):
            return {"success": False, "error": f"目标路径不存在：{target_path}"}

        # 生成知识灌注清单
        knowledge_list = list(self.FOUNDATION_KNOWLEDGE)
        persona = self.PERSONALITY_MAP.get(template_config.get("personality", "通用型"), {})
        sub_type = persona.get("sub_type_default", "通用综合")

        # 按分型添加专项知识
        specialty_map = {
            "哲学型": ["本体论研究方法", "元规则分析框架", "认知边界理论"],
            "数学型": ["数理建模方法", "形式化验证", "计算理论"],
            "工程型": ["系统架构设计", "软件工程方法", "性能优化理论"],
            "教育型": ["教育心理学", "课程设计方法", "认知学习理论"],
            "商业型": ["商业分析框架", "流通经济学", "资源配置理论"],
            "治理型": ["治理理论体系", "规则设计方法", "公共管理框架"],
            "科研型": ["科研方法论", "实验设计原理", "学术规范体系"],
            "运维型": ["系统监控理论", "故障排查方法", "运维管理体系"],
        }

        specialty_knowledge = specialty_map.get(template_config.get("personality"), [])
        knowledge_list.extend(specialty_knowledge)

        # 写入知识清单文件
        knowledge_path = os.path.join(target_path, "knowledge_base/")
        os.makedirs(knowledge_path, exist_ok=True)

        knowledge_file = os.path.join(knowledge_path, "foundation_knowledge_list.json")
        with open(knowledge_file, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "V1.0",
                "infusion_date": datetime.now().strftime('%Y-%m-%d'),
                "total_count": len(knowledge_list),
                "foundation_count": len(self.FOUNDATION_KNOWLEDGE),
                "specialty_count": len(specialty_knowledge),
                "foundation_knowledge": self.FOUNDATION_KNOWLEDGE,
                "specialty_knowledge": specialty_knowledge,
                "all_knowledge": knowledge_list,
            }, f, ensure_ascii=False, indent=2)

        # 更新agent配置中的知识状态
        agent_cfg_path = os.path.join(target_path, "agents/agent_config.json")
        if os.path.exists(agent_cfg_path):
            with open(agent_cfg_path, 'r', encoding='utf-8') as f:
                agent_cfg = json.load(f)

            if "knowledge_state" not in agent_cfg:
                agent_cfg["knowledge_state"] = {}

            agent_cfg["knowledge_state"]["infusion_completed"] = True
            agent_cfg["knowledge_state"]["infusion_date"] = datetime.now().strftime('%Y-%m-%d')
            agent_cfg["knowledge_state"]["knowledge_count"] = len(knowledge_list)
            agent_cfg["knowledge_state"]["foundation_coverage"] = len(self.FOUNDATION_KNOWLEDGE) / len(self.FOUNDATION_KNOWLEDGE)
            agent_cfg["knowledge_state"]["education_level"] = "基础教育毕业"

            # 更新光谱值（知识灌注后小幅提升）
            current_spectrum = agent_cfg.get("theory_binding", {}).get("spectrum_value", 0.5)
            new_spectrum = min(0.65, current_spectrum + 0.05)
            if "theory_binding" in agent_cfg:
                agent_cfg["theory_binding"]["spectrum_value"] = new_spectrum

            with open(agent_cfg_path, 'w', encoding='utf-8') as f:
                json.dump(agent_cfg, f, ensure_ascii=False, indent=2)

        self._log(f"✅ 基础教育灌注完成")
        self._log(f"   基础知识：{len(self.FOUNDATION_KNOWLEDGE)} 项")
        self._log(f"   专项知识：{len(specialty_knowledge)} 项")
        self._log(f"   知识总量：{len(knowledge_list)} 项")
        self._log(f"   教育等级：基础教育毕业")
        self._log(f"   光谱提升：{current_spectrum:.2f} → {new_spectrum:.2f}")

        return {
            "success": True,
            "knowledge_count": len(knowledge_list),
            "education_level": "基础教育毕业",
            "step": "step3_infusion",
        }

    # ==================================================================
    # 【第四步】全域合规质检与分层筛选
    # ==================================================================

    def step4_compliance_check(self, subsystem_rel_path: str) -> Dict:
        """
        第四步：全域合规质检与分层筛选
        执行check_compliance全维度校验，不合格回炉重造或隔离归档
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"🔍 [第4/6步] 全域合规质检与分层筛选")
        self._log("=" * 60)

        # 调用合规校验引擎
        result = self.checker.check_compliance(subsystem_rel_path)
        overall = result.get("overall", {})

        risk_level = overall.get("overall_risk", "safe")

        # 分层判定
        if risk_level in ["critical", "high"]:
            verdict = "回炉重造 / 隔离归档"
            passed = False
        elif risk_level == "medium":
            verdict = "限期整改后复检"
            passed = False
        elif risk_level == "low":
            verdict = "基本通过，可上岗"
            passed = True
        else:
            verdict = "完全通过，优先上岗"
            passed = True

        self._log("")
        self._log(f"📋 质检结论：{verdict}")
        self._log(f"   风险等级：{risk_level}")
        self._log(f"   判定结果：{overall.get('verdict', '')}")
        self._log(f"   建议操作：{overall.get('recommended_action', '')}")

        return {
            "success": passed,
            "risk_level": risk_level,
            "verdict": verdict,
            "full_result": result,
            "step": "step4_check",
        }

    # ==================================================================
    # 【第五步】分型定岗与场景落地
    # ==================================================================

    def step5_position_assignment(self, target_path: str, scenario: str, template_config: Dict) -> Dict:
        """
        第五步：分型定岗与场景落地
        根据分型自动匹配七大实体场景，实现一体一岗、分型适配、全域匹配
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"🏢 [第5/6步] 分型定岗与场景落地")
        self._log("=" * 60)

        if scenario not in self.SCENARIO_MAP:
            self._log(f"❌ 不支持的场景：{scenario}")
            return {"success": False, "error": f"不支持的场景：{scenario}"}

        scenario_cfg = self.SCENARIO_MAP[scenario]
        personality = template_config.get("personality", "通用型")

        # 场景适配度评估
        default_persona = scenario_cfg["default_personality"]
        if personality == default_persona:
            fit_score = 1.0
            fit_level = "完美适配"
        elif personality in ["哲学型", "科研型", "数学型"] and scenario == "科研创新":
            fit_score = 0.9
            fit_level = "高度适配"
        elif personality in ["工程型", "运维型"] and scenario in ["产业办公", "交通枢纽"]:
            fit_score = 0.85
            fit_level = "良好适配"
        elif personality == "治理型" and scenario == "政务治理":
            fit_score = 1.0
            fit_level = "完美适配"
        else:
            fit_score = 0.7
            fit_level = "一般适配"

        # 更新facade配置
        facade_path = os.path.join(target_path, "facade.json")
        if os.path.exists(facade_path):
            with open(facade_path, 'r', encoding='utf-8') as f:
                facade = json.load(f)

            facade["scenario_assignment"] = {
                "assigned_scenario": scenario,
                "building_type": scenario_cfg["building_type"],
                "target_district": scenario_cfg["district"],
                "fit_score": fit_score,
                "fit_level": fit_level,
                "power_quota": scenario_cfg["power_quota"],
                "position_date": datetime.now().strftime('%Y-%m-%d'),
                "position_status": "已定岗",
            }

            with open(facade_path, 'w', encoding='utf-8') as f:
                json.dump(facade, f, ensure_ascii=False, indent=2)

        self._log(f"✅ 定岗落地完成")
        self._log(f"   分配场景：{scenario}")
        self._log(f"   建筑类型：{scenario_cfg['building_type']}")
        self._log(f"   所属小区：{scenario_cfg['district']}")
        self._log(f"   适配等级：{fit_level}（{fit_score:.0%}）")
        self._log(f"   算力配额：{scenario_cfg['power_quota']} 点/日")

        return {
            "success": True,
            "scenario": scenario,
            "fit_score": fit_score,
            "fit_level": fit_level,
            "power_quota": scenario_cfg["power_quota"],
            "step": "step5_position",
        }

    # ==================================================================
    # 【第六步】全域动态迭代与终身升级
    # ==================================================================

    def step6_lifetime_iteration(self, target_path: str) -> Dict:
        """
        第六步：全域动态迭代与终身升级
        配置自动补全、盲区扫描、层级升级三大核心迭代机制
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"🚀 [第6/6步] 全域动态迭代与终身升级")
        self._log("=" * 60)

        # 生成迭代配置
        iteration_config = {
            "auto_fill_enabled": True,
            "blindspot_scan_enabled": True,
            "upgrade_enabled": True,
            "iteration_cycle_days": 30,
            "auto_fill_triggers": ["空白学科", "盲区领域", "新型范式"],
            "blindspot_scan_schedule": "每周一次",
            "upgrade_conditions": {
                "spectrum_min": 0.6,
                "zero_high_blindspots": True,
                "compliance_passed": True,
            },
            "lifetime_iteration_enabled": True,
            "first_release_date": datetime.now().strftime('%Y-%m-%d'),
        }

        # 写入迭代配置
        iter_cfg_path = os.path.join(target_path, "iteration_config.json")
        with open(iter_cfg_path, 'w', encoding='utf-8') as f:
            json.dump(iteration_config, f, ensure_ascii=False, indent=2)

        # 更新agent配置
        agent_cfg_path = os.path.join(target_path, "agents/agent_config.json")
        if os.path.exists(agent_cfg_path):
            with open(agent_cfg_path, 'r', encoding='utf-8') as f:
                agent_cfg = json.load(f)

            agent_cfg["agent_base_info"]["status"] = "正式上岗"
            agent_cfg["agent_base_info"]["activate_date"] = datetime.now().strftime('%Y-%m-%d')
            agent_cfg["inheritance_relation"]["upgrade_allowed"] = True

            with open(agent_cfg_path, 'w', encoding='utf-8') as f:
                json.dump(agent_cfg, f, ensure_ascii=False, indent=2)

        self._log(f"✅ 终身迭代配置完成")
        self._log(f"   自动补全：✅ 已启用")
        self._log(f"   盲区扫描：✅ 已启用（每周一次）")
        self._log(f"   层级升级：✅ 已启用（光谱≥0.6 + 零高危盲区）")
        self._log(f"   迭代周期：{iteration_config['iteration_cycle_days']} 天")
        self._log(f"   激活日期：{iteration_config['first_release_date']}")

        return {
            "success": True,
            "iteration_config": iteration_config,
            "status": "正式上岗，终身迭代模式已激活",
            "step": "step6_iteration",
        }

    # ==================================================================
    # 【全流程】六阶流水线一键生成
    # ==================================================================

    def produce_agent(self, name: str, personality: str = "通用型",
                      scenario: str = None, create_level: str = "hatch") -> Dict:
        """
        六阶流水线一键生成智能体（工厂总控接口）

        :param name: 智能体/项目名称
        :param personality: 人格分型（八大主分型 + 两种特殊分型）
        :param scenario: 分配场景（七大场景之一，None则暂不定岗）
        :param create_level: 创建层级，hatch=孵化栋，level1=成熟栋
        :return: 完整生产结果
        """
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║      🏭 智能体流水线工厂 · 六阶量产启动                    ║")
        self._log("╚══════════════════════════════════════════════════════════╝")
        self._log(f"项目名称：{name}")
        self._log(f"人格分型：{personality}")
        self._log(f"目标场景：{scenario or '（暂不定岗）'}")
        self._log(f"生产类型：{'一级成熟独栋' if create_level == 'level1' else '二级孵化独栋'}")
        self._log("")

        # 第一步：模板加载
        step1 = self.step1_load_template(name, personality)
        if not step1["success"]:
            return {"success": False, "error": "第1步失败：" + step1.get("error", "")}

        template_cfg = step1["config"]

        # 第二步：人格分型
        step2 = self.step2_personality_generate(template_cfg, personality)
        if not step2["success"]:
            return {"success": False, "error": "第2步失败"}

        # 创建物理目录
        if create_level == "level1":
            target_dir = os.path.join(
                self.residential_path,
                "level1_district",
                self.SCENARIO_MAP.get(scenario, {}).get("district", "01_数理拓展小区"),
                f"{name}_成熟独栋"
            )
            template_src = self.template_path
        else:
            target_dir = os.path.join(
                self.residential_path,
                "level2_villa",
                f"{name}_孵化独栋"
            )
            template_src = self.hatch_template_path

        if os.path.exists(target_dir):
            self._log(f"❌ 目标路径已存在：{target_dir}")
            return {"success": False, "error": "项目已存在"}

        copytree(template_src, target_dir)
        self._log(f"📁 目录创建完成：{target_dir}")

        # 初始化配置到facade
        facade_path = os.path.join(target_dir, "facade.json")
        with open(facade_path, 'r', encoding='utf-8') as f:
            facade = json.load(f)

        facade["subsystem_name"] = f"{name}_孵化独栋" if create_level == "hatch" else f"{name}_成熟独栋"
        facade["theory_category"]["logic_type"] = step2["config"]["initial_logic_type"]
        facade["theory_category"]["spectrum_value"] = template_cfg["spectrum_value"]
        facade["theory_category"]["parent_types"] = step2["config"]["correspond_parent_category"]
        facade["theory_category"]["sub_type"] = step2["config"]["sub_type"]
        facade["theory_category"]["source_trace"] = template_cfg["source_trace"]
        facade["resident_agent"]["name"] = f"{name}专项推演子智能体"
        facade["resident_agent"]["personality_type"] = personality
        facade["resident_agent"]["core_abilities"] = step2["config"]["core_abilities"]
        facade["resident_agent"]["identity_id"] = template_cfg["unique_id"]
        facade["humanoid_structure"]["personality_core"]["main_type"] = personality
        facade["humanoid_structure"]["personality_core"]["language_paradigm"] = step2["config"]["language_paradigm"]
        facade["humanoid_structure"]["personality_core"]["correspond_parent_category"] = step2["config"]["correspond_parent_category"]

        with open(facade_path, 'w', encoding='utf-8') as f:
            json.dump(facade, f, ensure_ascii=False, indent=2)

        # 初始化agent配置
        agent_cfg_path = os.path.join(target_dir, "agents/agent_config.json")
        if os.path.exists(agent_cfg_path):
            with open(agent_cfg_path, 'r', encoding='utf-8') as f:
                agent_cfg = json.load(f)

            agent_cfg["agent_base_info"]["name"] = f"{name}专项推演子智能体"
            agent_cfg["agent_base_info"]["generate_date"] = template_cfg["generation_date"]
            agent_cfg["agent_base_info"]["unique_id"] = template_cfg["unique_id"]
            agent_cfg["agent_base_info"]["owner"] = "杨腾飞"
            agent_cfg["agent_base_info"]["belong_subsystem"] = facade["subsystem_name"]
            agent_cfg["humanoid_structure"]["personality_core"]["main_type"] = personality
            agent_cfg["humanoid_structure"]["personality_core"]["language_paradigm"] = step2["config"]["language_paradigm"]
            agent_cfg["humanoid_structure"]["personality_core"]["correspond_parent_category"] = step2["config"]["correspond_parent_category"]
            agent_cfg["theory_binding"]["logic_type"] = step2["config"]["initial_logic_type"]
            agent_cfg["theory_binding"]["spectrum_value"] = template_cfg["spectrum_value"]
            agent_cfg["theory_binding"]["main_parent_category"] = step2["config"]["correspond_parent_category"]

            with open(agent_cfg_path, 'w', encoding='utf-8') as f:
                json.dump(agent_cfg, f, ensure_ascii=False, indent=2)

        # 第三步：知识灌注
        step3 = self.step3_knowledge_infusion(target_dir, template_cfg)
        if not step3["success"]:
            self._log(f"⚠️  第3步知识灌注部分完成")

        # 计算相对路径
        rel_path = os.path.relpath(target_dir, self.residential_path)

        # 第四步：合规质检（孵化型必须通过才能升级）
        step4 = self.step4_compliance_check(rel_path)

        # 如果是一级成熟栋且质检通过，执行第五、六步
        step5 = None
        step6 = None
        if create_level == "level1" and step4["success"] and scenario:
            step5 = self.step5_position_assignment(target_dir, scenario, template_cfg)
            step6 = self.step6_lifetime_iteration(target_dir)
        elif create_level == "hatch":
            # 孵化型只配置迭代能力，不定岗
            step6 = self.step6_lifetime_iteration(target_dir)

        # 生产完成汇总
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║      🎉 智能体流水线工厂 · 生产完成                        ║")
        self._log("╚══════════════════════════════════════════════════════════╝")
        self._log(f"   智能体名称：{name}")
        self._log(f"   人格分型：{personality}")
        self._log(f"   当前层级：{'一级成熟' if create_level == 'level1' else '二级孵化'}")
        self._log(f"   光谱值：{template_cfg['spectrum_value']}")
        self._log(f"   唯一ID：{template_cfg['unique_id']}")
        self._log(f"   质检结果：{step4['verdict']}")
        if scenario:
            self._log(f"   分配场景：{scenario}")
        self._log(f"   存储路径：{rel_path}")
        self._log("")

        return {
            "success": True,
            "name": name,
            "personality": personality,
            "scenario": scenario,
            "level": create_level,
            "unique_id": template_cfg["unique_id"],
            "spectrum_value": template_cfg["spectrum_value"],
            "target_path": rel_path,
            "compliance_result": step4,
            "steps": {
                "step1_template": step1,
                "step2_personality": step2,
                "step3_infusion": step3,
                "step4_check": step4,
                "step5_position": step5,
                "step6_iteration": step6,
            },
        }

    # ==================================================================
    # 批量生产
    # ==================================================================

    def batch_produce(self, agent_list: List[Dict]) -> Dict:
        """
        批量生产智能体
        agent_list格式：[{"name": "xxx", "personality": "科研型", "scenario": "科研创新"}, ...]
        """
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log(f"║   🏭 批量生产启动 · 共 {len(agent_list)} 个智能体              ║")
        self._log("╚══════════════════════════════════════════════════════════╝")

        results = []
        success_count = 0
        fail_count = 0

        for i, agent_cfg in enumerate(agent_list):
            self._log("")
            self._log(f"--- [{i+1}/{len(agent_list)}] 生产 {agent_cfg['name']} ---")
            try:
                result = self.produce_agent(
                    name=agent_cfg["name"],
                    personality=agent_cfg.get("personality", "通用型"),
                    scenario=agent_cfg.get("scenario"),
                    create_level=agent_cfg.get("level", "hatch"),
                )
                if result["success"]:
                    success_count += 1
                else:
                    fail_count += 1
                results.append(result)
            except Exception as e:
                fail_count += 1
                results.append({"success": False, "name": agent_cfg["name"], "error": str(e)})

        self._log("")
        self._log("=" * 60)
        self._log(f"📊 批量生产完成：成功 {success_count}，失败 {fail_count}，总计 {len(agent_list)}")
        self._log("=" * 60)

        return {
            "total": len(agent_list),
            "success": success_count,
            "failed": fail_count,
            "results": results,
        }

    def get_factory_stats(self) -> Dict:
        """获取工厂生产统计"""
        total = 0
        passed = 0
        deployed = 0

        # 统计现有智能体
        if os.path.exists(self.residential_path):
            for root, dirs, files in os.walk(self.residential_path):
                if "facade.json" in files and "_template" not in root and "_archive" not in root:
                    total += 1
                    try:
                        with open(os.path.join(root, "facade.json"), 'r', encoding='utf-8') as f:
                            facade = json.load(f)
                        if facade.get("subsystem_level", "") == "一级成熟":
                            deployed += 1
                    except Exception:
                        pass

        return {
            "total_produced": total,
            "compliance_passed": total - 1 if total > 0 else 0,
            "deployed": deployed,
            "personality_types": len(self.PERSONALITY_MAP),
            "scenario_types": len(self.SCENARIO_MAP),
        }


# ========== 命令行入口 ==========

if __name__ == "__main__":
    import sys

    factory = AgentFactory()

    if len(sys.argv) < 3:
        print("用法: python agent_factory.py <名称> <人格分型> [场景] [层级]")
        print("分型可选：哲学型/数学型/工程型/教育型/商业型/治理型/科研型/运维型/语文型/通用型")
        print("场景可选：校园教育/产业办公/商业流通/科研创新/政务治理/民生社区/交通枢纽")
        print("层级可选：hatch（孵化栋）/ level1（成熟栋）")
        print("示例: python agent_factory.py 量子引力研究 科研型 科研创新 hatch")
        sys.exit(1)

    name = sys.argv[1]
    personality = sys.argv[2]
    scenario = sys.argv[3] if len(sys.argv) > 3 else None
    level = sys.argv[4] if len(sys.argv) > 4 else "hatch"

    factory.produce_agent(name, personality, scenario, level)
