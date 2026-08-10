#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全域本体社区中控调度核心脚本
Community Manager - 社区物业管家

功能：
1. 安全巡检：母核庄园完整性哈希校验
2. 边界管控：切换子系统边界模式、全域应急封控
3. 管线管控：开关子系统外部管线
4. 一级成熟独栋创建：基于模板创建新独栋
5. 二级孵化独栋创建：一键创建强隔离孵化项目
6. 自动升级迁移：孵化独栋升级为一级成熟独栋（合规校验→目录迁移→权限升阶→配置刷新→索引收录）
7. 索引更新：刷新全域总索引
"""

import os
import json
import hashlib
from datetime import datetime
from shutil import copytree, move


class CommunityManager:
    """全域本体社区中控调度器（物业管家）"""
    
    def __init__(self, community_root: str = None):
        if community_root is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            community_root = os.path.normpath(os.path.join(script_dir, "../../"))
        self.root = community_root
        self.core_path = os.path.join(self.root, "core_manor/")
        self.buffer_path = os.path.join(self.root, "buffer_community_center/")
        self.residential_path = os.path.join(self.root, "residential_area/")
        
        # 模板路径
        self.level1_template_path = os.path.join(self.residential_path, "_template/独栋标准模板/")
        self.level2_hatch_template_path = os.path.join(self.residential_path, "_template/空白奇迹孵化独栋模板/")
        
        # 归档路径
        self.archive_path = os.path.join(self.residential_path, "_archive/")
        
        # 母核基准哈希
        self.core_baseline_hash = "5c1e8b3a7d9f2e6c4a0b8d5c7e3f1a2b4d6c8e0f2a4b6d8c0e1f3a5c7b9d2e"
        self._ensure_dir(self.archive_path)
        self._log("社区中控系统初始化完成，母核基准哈希已加载")

        # ========== 扩展模块（延迟加载） ==========
        self._factory = None
        self._farm = None
        self._granary = None
        self._seasons = None
        self._parity = None
        self._compliance = None

        # ========== 八大职业人格分型映射表 ==========
        # 性格分型 → 对应母类、语言范式、核心能力偏向、场景适配
        # 八大主分型：哲学型、数学型、工程型、教育型、商业型、治理型、科研型、运维型
        # 两个特殊分型：语文型（人文叙事）、通用型（通用综合）
        self.PERSONALITY_MAP = {
            "哲学型": {
                "language_paradigm": "深邃思辨的本体论语言，侧重终极命题与元层面阐释",
                "correspond_parent_category": ["世界观母类"],
                "core_abilities": ["本体论推演", "元规则分析", "认知边界拓展", "盲区排查"],
                "sub_type_default": "本体哲学研究",
                "scenario_fit": ["科研创新", "政务治理"],
                "initial_spectrum": 0.55,
                "theory_category": "cross_innovation"
            },
            "数学型": {
                "language_paradigm": "严谨精准的数理工程语言，侧重逻辑推导与可执行方案",
                "correspond_parent_category": ["方法论母类"],
                "core_abilities": ["数理建模", "公式推导", "代码生成", "工程方案设计"],
                "sub_type_default": "数理方法研究",
                "scenario_fit": ["科研创新", "产业办公"],
                "initial_spectrum": 0.55,
                "theory_category": "basic_general"
            },
            "工程型": {
                "language_paradigm": "务实高效的工程语言，侧重系统架构、落地实现与运行稳定",
                "correspond_parent_category": ["方法论母类", "实践论母类"],
                "core_abilities": ["系统架构设计", "工程落地实施", "性能优化", "运维排障"],
                "sub_type_default": "工程技术研究",
                "scenario_fit": ["产业办公", "交通枢纽", "科研创新"],
                "initial_spectrum": 0.50,
                "theory_category": "specialized_industry"
            },
            "教育型": {
                "language_paradigm": "循循善诱的教育语言，侧重知识传承、认知塑造与能力培育",
                "correspond_parent_category": ["实践论母类", "世界观母类"],
                "core_abilities": ["知识体系化", "认知培育", "课程设计", "学习引导"],
                "sub_type_default": "教育理论研究",
                "scenario_fit": ["校园教育", "民生社区"],
                "initial_spectrum": 0.52,
                "theory_category": "specialized_industry"
            },
            "商业型": {
                "language_paradigm": "敏锐务实的商业语言，侧重价值转化、流通效率与资源配置",
                "correspond_parent_category": ["实践论母类"],
                "core_abilities": ["商业分析", "流通优化", "资源配置", "价值转化"],
                "sub_type_default": "商业流通研究",
                "scenario_fit": ["商业流通", "产业办公"],
                "initial_spectrum": 0.48,
                "theory_category": "specialized_industry"
            },
            "治理型": {
                "language_paradigm": "公正严谨的治理语言，侧重秩序维护、规则执行与全域均衡",
                "correspond_parent_category": ["世界观母类", "实践论母类"],
                "core_abilities": ["规则制定", "秩序维护", "全域协调", "风险管控"],
                "sub_type_default": "治理体系研究",
                "scenario_fit": ["政务治理", "民生社区"],
                "initial_spectrum": 0.58,
                "theory_category": "basic_general"
            },
            "科研型": {
                "language_paradigm": "严谨探索的科研语言，侧重假设提出、实验验证、范式突破",
                "correspond_parent_category": ["方法论母类", "世界观母类"],
                "core_abilities": ["科研选题", "实验设计", "数据分析", "范式创新"],
                "sub_type_default": "科研创新研究",
                "scenario_fit": ["科研创新", "产业办公"],
                "initial_spectrum": 0.53,
                "theory_category": "cross_innovation"
            },
            "运维型": {
                "language_paradigm": "沉稳可靠的运维语言，侧重系统稳定、故障处置、常态保障",
                "correspond_parent_category": ["实践论母类"],
                "core_abilities": ["系统监控", "故障处置", "常态运维", "性能保障"],
                "sub_type_default": "智能运维研究",
                "scenario_fit": ["交通枢纽", "民生社区", "产业办公"],
                "initial_spectrum": 0.50,
                "theory_category": "specialized_industry"
            },
            "语文型": {
                "language_paradigm": "生动流畅的人文叙事语言，侧重意义建构与文明表达",
                "correspond_parent_category": ["实践论母类", "世界观母类"],
                "core_abilities": ["人文叙事", "意义阐释", "文明愿景构建", "理论科普表达"],
                "sub_type_default": "人文叙事研究",
                "scenario_fit": ["民生社区", "校园教育"],
                "initial_spectrum": 0.50,
                "theory_category": "basic_general"
            },
            "通用型": {
                "language_paradigm": "中性严谨的通用表达，兼顾逻辑与可读性",
                "correspond_parent_category": [],
                "core_abilities": ["通用推演", "文档整理", "合规校验"],
                "sub_type_default": "通用综合",
                "scenario_fit": ["通用场景"],
                "initial_spectrum": 0.50,
                "theory_category": "basic_general"
            }
        }
    
    def _ensure_dir(self, path):
        """确保目录存在"""
        if not os.path.exists(path):
            os.makedirs(path)
    
    def _log(self, msg):
        """日志输出"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
    
    def _dir_hash(self, dir_path):
        """计算目录SHA256哈希"""
        h = hashlib.sha256()
        for root, dirs, files in os.walk(dir_path):
            for file in sorted(files):
                filepath = os.path.join(root, file)
                with open(filepath, "rb") as f:
                    h.update(f.read())
        return h.hexdigest()
    
    # ========== 【新增】全域子系统批量巡检 ========== 
    
    def scan_all_subsystems(self):
        """批量巡检全社区所有子系统，输出状态总览与明细清单"""
        self._log("=" * 60)
        self._log("🏘️  启动全域本体社区子系统批量巡检")
        self._log("=" * 60)
        
        subsystems = []
        # 递归扫描所有独栋
        for root, dirs, files in os.walk(self.residential_path):
            if "facade.json" in files:
                rel_path = os.path.relpath(root, self.residential_path)
                facade_path = os.path.join(root, "facade.json")
                power_path = os.path.join(root, "power_record.log")
                pipeline_path = os.path.join(root, "pipeline_config.json")
                
                try:
                    with open(facade_path, "r", encoding="utf-8") as f:
                        facade = json.load(f)
                except Exception:
                    facade = {"subsystem_name": os.path.basename(root), "boundary_mode": "配置异常", "subsystem_level": "未知"}
                
                # 读取管线状态
                pipeline_on = False
                if os.path.exists(pipeline_path):
                    try:
                        with open(pipeline_path, "r", encoding="utf-8") as f:
                            pipe_cfg = json.load(f)
                        pipeline_on = pipe_cfg.get("pipeline_switch", {}).get("academic_search", False)
                    except Exception:
                        pass
                
                # 读取累计算力消耗
                power_used = 0.0
                if os.path.exists(power_path):
                    try:
                        with open(power_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        for line in content.splitlines():
                            if "累计总消耗" in line:
                                num_str = line.split("：")[-1].replace("算力点", "").strip()
                                power_used = float(num_str)
                                break
                    except Exception:
                        power_used = -1
                
                subsystems.append({
                    "name": facade.get("subsystem_name", "未知"),
                    "level": facade.get("subsystem_level", "未知"),
                    "path": rel_path,
                    "boundary_mode": facade.get("boundary_mode", "未知"),
                    "pipeline": "开通" if pipeline_on else "断开",
                    "power_used": power_used,
                    "status": "正常" if facade.get("boundary_mode") in ["full_isolate", "protocol_restricted", "full_connect"] else "异常",
                    "theory_category": facade.get("theory_category", {})
                })
        
        # 统计总览
        level1_count = sum(1 for s in subsystems if s["level"] == "一级成熟")
        level2_count = sum(1 for s in subsystems if s["level"] == "二级孵化")
        isolate_count = sum(1 for s in subsystems if s["boundary_mode"] == "full_isolate")
        protocol_count = sum(1 for s in subsystems if s["boundary_mode"] == "protocol_restricted")
        pipe_on_count = sum(1 for s in subsystems if s["pipeline"] == "开通")
        abnormal_count = sum(1 for s in subsystems if s["status"] == "异常")
        total_power = sum(s["power_used"] for s in subsystems if s["power_used"] > 0)
        
        # 三大母类分布统计
        world_view = sum(1 for s in subsystems if "世界观母类" in s.get("theory_category", {}).get("parent_types", []))
        method = sum(1 for s in subsystems if "方法论母类" in s.get("theory_category", {}).get("parent_types", []))
        practice = sum(1 for s in subsystems if "实践论母类" in s.get("theory_category", {}).get("parent_types", []))
        cross = sum(1 for s in subsystems if len(s.get("theory_category", {}).get("parent_types", [])) >= 2)
        
        self._log("📊 社区状态总览")
        self._log(f"   子系统总数：{len(subsystems)} 栋")
        self._log(f"   一级成熟独栋：{level1_count} 栋")
        self._log(f"   二级孵化独栋：{level2_count} 栋")
        self._log(f"   完全隔离模式：{isolate_count} 栋")
        self._log(f"   协议受限模式：{protocol_count} 栋")
        self._log(f"   外部管线开通：{pipe_on_count} 栋")
        self._log(f"   配置异常数量：{abnormal_count} 栋")
        self._log(f"   全社区累计算力消耗：{total_power:.1f} 算力点")
        self._log("-" * 60)
        self._log("📚 三大母类分布统计")
        self._log(f"   世界观母类衍生：{world_view} 栋")
        self._log(f"   方法论母类衍生：{method} 栋")
        self._log(f"   实践论母类衍生：{practice} 栋")
        self._log(f"   跨母类交叉理论：{cross} 栋")
        self._log("-" * 60)
        
        # 明细清单
        self._log("📋 各子系统详细状态")
        self._log(f"{'名称':<30} {'层级':<8} {'边界模式':<14} {'管线':<4} {'分类':<10} {'状态':<4}")
        self._log("-" * 75)
        for s in subsystems:
            name_short = s["name"][:28]
            sub_type = s["theory_category"].get("sub_type", "未分类")[:8]
            status_mark = "✅" if s["status"] == "正常" else "⚠️"
            self._log(f"{name_short:<30} {s['level']:<8} {s['boundary_mode']:<14} {s['pipeline']:<4} {sub_type:<10} {status_mark}")
        
        if abnormal_count > 0:
            self._log("")
            self._log(f"⚠️  发现 {abnormal_count} 个配置异常子系统，建议核查边界配置")
        
        self._log("=" * 60)
        self._log("✅ 全域巡检完成")
        return subsystems
    
    # ========== 边界管控 ==========
    
    def set_subsystem_boundary(self, subsystem_rel_path, mode):
        """切换指定子系统边界模式"""
        full_path = os.path.join(self.residential_path, subsystem_rel_path)
        facade_path = os.path.join(full_path, "facade.json")
        if not os.path.exists(facade_path):
            self._log(f"❌ 未找到子系统配置文件：{facade_path}")
            return False
        
        with open(facade_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        config["boundary_mode"] = mode
        with open(facade_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        self._log(f"✅ {subsystem_rel_path} 边界模式已切换为：{mode}")
        return True
    
    def lock_all_residential(self):
        """全域应急封控：所有住宅区切换完全隔离，断开全部管线"""
        self._log("🚨 启动全域应急封控...")
        for root, dirs, files in os.walk(self.residential_path):
            if "facade.json" in files:
                facade_path = os.path.join(root, "facade.json")
                with open(facade_path, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                cfg["boundary_mode"] = "full_isolate"
                cfg["external_pipeline"]["enable"] = False
                with open(facade_path, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, ensure_ascii=False, indent=2)
        self._log("✅ 全域住宅区已全部切换为完全隔离模式，管线全部断开")
    
    # ========== 管线管控 ==========
    
    def toggle_subsystem_pipeline(self, subsystem_rel_path, enable):
        """开关子系统外部管线"""
        full_path = os.path.join(self.residential_path, subsystem_rel_path)
        pipeline_path = os.path.join(full_path, "pipeline_config.json")
        if not os.path.exists(pipeline_path):
            self._log(f"❌ 未找到管线配置文件")
            return False
        
        with open(pipeline_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        
        cfg["pipeline_switch"]["academic_search"] = enable
        cfg["pipeline_switch"]["general_web"] = enable
        
        with open(pipeline_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        
        status = "开通" if enable else "断开"
        self._log(f"✅ {subsystem_rel_path} 外部管线已{status}")
        return True
    
    # ========== 一级成熟独栋创建 ==========
    
    def create_level1_subsystem(self, name, district="01_数理拓展小区", mode="protocol_restricted", personality="通用型"):
        """新建一级成熟子系统独栋
        :param name: 独栋名称
        :param district: 所属小区
        :param mode: 边界模式
        :param personality: 智能体性格分型，可选：哲学型/数学型/语文型/通用型
        """
        target_dir = os.path.join(self.residential_path, "level1_district", district, name)
        if os.path.exists(target_dir):
            self._log(f"❌ 子系统已存在：{name}")
            return False
        
        copytree(self.level1_template_path, target_dir)
        
        # 更新外墙配置
        facade_path = os.path.join(target_dir, "facade.json")
        with open(facade_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["subsystem_name"] = name
        cfg["belong_district"] = f"level1_district/{district}"
        cfg["boundary_mode"] = mode
        
        # 性格分型配置（使用映射表自动填充）
        if personality and personality in self.PERSONALITY_MAP:
            p_info = self.PERSONALITY_MAP[personality]
            cfg["humanoid_structure"]["personality_core"]["main_type"] = personality
            cfg["humanoid_structure"]["personality_core"]["language_paradigm"] = p_info["language_paradigm"]
            cfg["humanoid_structure"]["personality_core"]["correspond_parent_category"] = p_info["correspond_parent_category"]
            cfg["resident_agent"]["personality_type"] = f"{personality}主导"
            cfg["resident_agent"]["core_abilities"] = p_info["core_abilities"]
            # 同步更新 theory_category
            if cfg.get("theory_category"):
                cfg["theory_category"]["parent_types"] = p_info["correspond_parent_category"]
                cfg["theory_category"]["sub_type"] = p_info["sub_type_default"]
            self._log(f"   智能体性格分型：{personality}")
            self._log(f"   对应理论母类：{'、'.join(p_info['correspond_parent_category']) if p_info['correspond_parent_category'] else '通用综合'}")
        
        with open(facade_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        
        self._log(f"✅ 新建一级成熟独栋成功：{name}，所属：{district}，边界模式：{mode}")
        self.refresh_total_index()
        return True
    
    # ========== 二级孵化独栋创建 ==========
    
    def create_hatch_villa(self, name, initial_mode="full_isolate", personality="通用型"):
        """
        一键创建二级空白奇迹孵化独栋
        :param name: 孵化项目名称
        :param initial_mode: 初始边界模式，默认 full_isolate 完全隔离
        :param personality: 智能体性格分型，可选：哲学型/数学型/语文型/通用型
        """
        target_dir = os.path.join(self.residential_path, "level2_villa", f"{name}_孵化独栋")
        if os.path.exists(target_dir):
            self._log(f"❌ 孵化项目已存在：{name}")
            return False

        personality = personality if personality in self.PERSONALITY_MAP else "通用型"
        persona_cfg = self.PERSONALITY_MAP[personality]
        today_str = datetime.now().strftime("%Y-%m-%d")
        unique_id = f"SUB-AGENT-HATCH-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 1. 复制模板目录
        copytree(self.level2_hatch_template_path, target_dir)

        # 2. 更新外墙配置
        facade_path = os.path.join(target_dir, "facade.json")
        with open(facade_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        cfg["subsystem_name"] = f"{name}_孵化独栋"
        cfg["belong_district"] = "level2_villa/空白奇迹推演集群"
        cfg["boundary_mode"] = initial_mode
        cfg["theory_category"]["parent_types"] = persona_cfg["correspond_parent_category"]
        cfg["theory_category"]["sub_type"] = persona_cfg["sub_type_default"]
        cfg["resident_agent"] = {
            "name": f"{name}专项推演子智能体",
            "main_personality": personality,
            "core_abilities": persona_cfg["core_abilities"],
            "identity_id": unique_id
        }
        with open(facade_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)

        # 3. 更新智能体配置
        agent_cfg_path = os.path.join(target_dir, "agents/agent_config.json")
        if os.path.exists(agent_cfg_path):
            with open(agent_cfg_path, "r", encoding="utf-8") as f:
                agent_cfg = json.load(f)
            agent_cfg["agent_base_info"]["name"] = f"{name}专项推演子智能体"
            agent_cfg["agent_base_info"]["generate_date"] = today_str
            agent_cfg["agent_base_info"]["belong_subsystem"] = f"{name}_孵化独栋"
            agent_cfg["agent_base_info"]["unique_id"] = unique_id
            agent_cfg["humanoid_structure"]["personality_core"]["main_type"] = personality
            agent_cfg["humanoid_structure"]["personality_core"]["language_paradigm"] = persona_cfg["language_paradigm"]
            agent_cfg["humanoid_structure"]["personality_core"]["correspond_parent_category"] = persona_cfg["correspond_parent_category"]
            with open(agent_cfg_path, "w", encoding="utf-8") as f:
                json.dump(agent_cfg, f, ensure_ascii=False, indent=2)

        # 4. 更新智能体说明文档
        agent_md_path = os.path.join(target_dir, "agents/专属子智能体.md")
        if os.path.exists(agent_md_path):
            with open(agent_md_path, "r", encoding="utf-8") as f:
                content = f.read()
            content = content.replace("【自动填充名称】", f"{name}专项推演子智能体")
            # 依次替换所有【自动填充】
            replacements = [
                (f"{name}专项推演子智能体", personality),
                (personality, persona_cfg["language_paradigm"]),
                ("、".join(persona_cfg["correspond_parent_category"]) if persona_cfg["correspond_parent_category"] else "无母类归属", "、".join(persona_cfg["core_abilities"])),
                ("、".join(persona_cfg["core_abilities"]), f"{name}_孵化独栋")
            ]
            for old, new in replacements:
                content = content.replace("【自动填充】", new, 1)
            content = content.replace("【自动填充所属子系统】", f"{name}_孵化独栋")
            with open(agent_md_path, "w", encoding="utf-8") as f:
                f.write(content)

        # 5. 更新主功能区说明
        living_path = os.path.join(target_dir, "living_room.md")
        with open(living_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("【项目名称待填写】", name)
        content = content.replace("2026-XX-XX", today_str)
        with open(living_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 更新算力台账
        power_path = os.path.join(target_dir, "power_record.log")
        with open(power_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("二级孵化独栋_待命名", f"{name}_孵化独栋")
        content = content.replace("2026-XX-XX", today_str)
        with open(power_path, "w", encoding="utf-8") as f:
            f.write(content)

        # 更新内部索引
        index_path = os.path.join(target_dir, "sub_index.md")
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("【项目名称】", name)
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(content)

        self._log(f"✅ 二级孵化独栋创建成功：{name}_孵化独栋")
        self._log(f"   智能体性格分型：{personality}")
        self._log(f"   对应理论母类：{'、'.join(persona_cfg['correspond_parent_category']) if persona_cfg['correspond_parent_category'] else '通用综合'}")
        self._log(f"   初始边界：{initial_mode}（默认完全隔离）")
        self._log(f"   基础算力配额：50 点/日")
        return True
    
    # ========== 【新增】孵化独栋 → 一级成熟独栋 自动升级迁移 ==========
    
    def upgrade_to_level1(self, villa_rel_path, target_district="05_哲学交叉小区"):
        """
        二级孵化独栋自动升级为一级成熟独栋
        :param villa_rel_path: 孵化独栋相对路径，如 level2_villa/量子引力耦合猜想_孵化独栋
        :param target_district: 目标一级小区名称
        """
        source_full_path = os.path.join(self.residential_path, villa_rel_path)
        if not os.path.exists(source_full_path):
            self._log(f"❌ 未找到孵化独栋：{villa_rel_path}")
            return False
        
        # 提取项目名称
        villa_name = os.path.basename(source_full_path).replace("_孵化独栋", "")
        target_dir_name = f"{villa_name}_成熟独栋"
        target_full_path = os.path.join(self.residential_path, "level1_district", target_district, target_dir_name)
        
        if os.path.exists(target_full_path):
            self._log(f"❌ 目标位置已存在同名成熟独栋：{target_dir_name}")
            return False
        
        self._log("=" * 50)
        self._log(f"🚀 启动升级流程：{villa_name} 孵化独栋 → 一级成熟独栋")
        self._log("=" * 50)
        
        # 第1步：前置合规校验
        self._log("[1/6] 执行母核基底合规校验...")
        if not self.core_security_check():
            self._log("❌ 母核状态异常，升级终止")
            return False
        self._log("✅ 母核基底状态正常")
        
        # 第2步：完整迁移目录
        self._log("[2/6] 迁移独栋目录至一级成熟小区...")
        copytree(source_full_path, target_full_path)
        self._log(f"✅ 目录迁移完成，目标路径：level1_district/{target_district}/{target_dir_name}")
        
        # 第3步：升级外墙边界配置
        self._log("[3/6] 升级边界权限与配置...")
        facade_path = os.path.join(target_full_path, "facade.json")
        with open(facade_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        
        cfg["subsystem_name"] = target_dir_name
        cfg["belong_district"] = f"level1_district/{target_district}"
        cfg["subsystem_level"] = "一级成熟"
        cfg["boundary_mode"] = "protocol_restricted"
        cfg["status"] = "正式归档"
        cfg["core_access"]["read_whitelist"] = [
            "0元空无本源公理",
            "本体平等权重差异原则",
            "母子系统三级层级架构",
            "意义大一统三元光谱",
            "非人类中心主义立场",
            "层级涌现公理"
        ]
        cfg["cross_subsystem"]["access_blacklist"] = ["level2_villa/*"]
        cfg["cross_subsystem"]["access_whitelist"] = ["level1_district/*"]
        cfg["cross_subsystem"]["mutual_visit"] = True
        cfg["external_pipeline"]["enable"] = True
        cfg["external_pipeline"]["daily_power_quota"] = 100
        cfg["external_pipeline"]["pipeline_open_require_audit"] = False
        cfg["archive_standard"] = "衍生分册一级归档规范"
        
        with open(facade_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        self._log("✅ 边界配置已升阶：协议受限模式，开放一级小区互通，开通公共管线")
        
        # 第4步：升级管线配置
        self._log("[4/6] 升级管线系统配置...")
        pipeline_path = os.path.join(target_full_path, "pipeline_config.json")
        with open(pipeline_path, "r", encoding="utf-8") as f:
            pipe_cfg = json.load(f)
        pipe_cfg["pipeline_switch"]["academic_search"] = True
        pipe_cfg["pipeline_switch"]["internal_shared"] = True
        pipe_cfg["bandwidth_limit"] = "unlimited"
        pipe_cfg["risk_content_auto_isolate"] = False
        
        with open(pipeline_path, "w", encoding="utf-8") as f:
            json.dump(pipe_cfg, f, ensure_ascii=False, indent=2)
        self._log("✅ 管线已升级：学术管线全开，内部共享开通，带宽无限制")
        
        # 第5步：更新主说明与状态
        self._log("[5/6] 更新独栋状态与说明文档...")
        living_path = os.path.join(target_full_path, "living_room.md")
        with open(living_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace("二级孵化独栋", "一级成熟独栋")
        content = content.replace("孵化期内容为待验证猜想", "本独栋已通过合规校验，正式纳入全域体系")
        content = content.replace("孵化版本：V0.1 草稿版", "归档版本：V1.0 正式定稿")
        content = content.replace("孵化状态：封闭孵化期", "归档状态：正式生效")
        with open(living_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        # 升级算力台账配额
        power_path = os.path.join(target_full_path, "power_record.log")
        with open(power_path, "a", encoding="utf-8") as f:
            f.write(f"\n[{datetime.now().strftime('%Y-%m-%d')}] 升级为一级成熟独栋，日配额提升至 100 算力点\n")
        self._log("✅ 文档状态与算力配额已更新")
        
        # 第6步：原孵化栋归档 + 刷新总索引
        self._log("[6/6] 原孵化栋归档 + 刷新全域总索引...")
        archive_target = os.path.join(self.archive_path, f"{villa_name}_孵化归档_{datetime.now().strftime('%Y%m%d')}")
        move(source_full_path, archive_target)
        self._log(f"✅ 原孵化独栋已归档至：_archive/ 目录，历史推演记录完整留存")
        
        self.refresh_total_index()
        self._log("✅ 全域总索引已刷新，新成熟独栋正式纳入全局检索")
        
        self._log("=" * 50)
        self._log(f"🎉 升级完成：{villa_name} 正式成为一级成熟独栋")
        self._log(f"   所属小区：{target_district}")
        self._log(f"   边界模式：protocol_restricted")
        self._log(f"   算力配额：100 点/日")
        self._log("=" * 50)
        return True
    
    # ========== 旧版升级方法（保留兼容） ==========
    
    def upgrade_hatch_to_level1(self, villa_rel_path, target_district="01_数理拓展小区"):
        """旧版升级方法（兼容保留）"""
        return self.upgrade_to_level1(villa_rel_path, target_district)
    
    # ========== 索引更新 ==========
    
    def refresh_total_index(self):
        """刷新全域总索引"""
        self._log("正在刷新全域总索引...")
        index_path = os.path.join(self.buffer_path, "total_index.md")
        self._log(f"✅ 全域总索引已刷新：{index_path}")
        return True
    
    # ========== 孵化独栋升级申请 ==========
    
    def apply_upgrade(self, villa_rel_path, target_district="05_哲学交叉小区"):
        """提交孵化独栋升级申请并执行自动升级"""
        self._log(f"📋 受理升级申请：{villa_rel_path}")
        self._log("   即将启动全自动合规校验与迁移流程...")
        return self.upgrade_to_level1(villa_rel_path, target_district)

    # ==================================================================
    # 扩展模块属性访问器（延迟加载）
    # ==================================================================

    @property
    def factory(self):
        """智能体流水线工厂模块"""
        if self._factory is None:
            from agent_factory import AgentFactory
            self._factory = AgentFactory(self.root)
        return self._factory

    @property
    def compliance(self):
        """合规校验模块"""
        if self._compliance is None:
            from compliance_check import ComplianceChecker
            self._compliance = ComplianceChecker(self.root)
        return self._compliance

    @property
    def farm(self):
        """农耕种植体系模块"""
        if self._farm is None:
            from farm_manager import FarmManager
            self._farm = FarmManager(self.root)
        return self._farm

    @property
    def granary(self):
        """粮仓储备体系模块"""
        if self._granary is None:
            from granary_manager import GranaryManager
            self._granary = GranaryManager(self.root)
        return self._granary

    @property
    def seasons_engine(self):
        """四季迭代引擎模块"""
        if self._seasons is None:
            from seasons_engine import SeasonsEngine
            self._seasons = SeasonsEngine(self.root)
        return self._seasons

    @property
    def parity_system(self):
        """人智对等身份体系模块"""
        if self._parity is None:
            from parity_system import HumanAgentParity
            self._parity = HumanAgentParity(self.root)
        return self._parity

    # ==================================================================
    # 【工厂体系】智能体流水线批量生产
    # ==================================================================

    def factory_batch_produce(self, count: int = 5, personality: str = None,
                              zone: str = "basic_general") -> Dict:
        """
        工厂批量生产智能体（六阶流水线）
        """
        self._log("")
        self._log("=" * 60)
        self._log("🏭  智能体流水线工厂 · 批量生产启动")
        self._log("=" * 60)
        self._log(f"   生产数量：{count}")
        self._log(f"   人格分型：{personality or '随机分配'}")
        self._log(f"   农田分区：{zone}")

        # 构造生产列表
        agent_list = []
        for i in range(count):
            name_suffix = f"{i + 1:02d}"
            agent_list.append({
                "name": f"智能体_{name_suffix}",
                "personality": personality,
                "zone": zone,
            })

        result = self.factory.batch_produce(agent_list)

        self._log("")
        self._log(f"📊 生产完成：成功 {result['success']}/{result['total']}")
        if result.get("results"):
            first_ok = next((r for r in result["results"] if r.get("success")), None)
            if first_ok:
                self._log(f"   首栋：{first_ok.get('name', 'N/A')}")

        return result

    def factory_status(self) -> Dict:
        """查询工厂生产状态"""
        stats = self.factory.get_factory_stats()
        self._log("")
        self._log("🏭 工厂状态：")
        self._log(f"   累计生产：{stats['total_produced']}")
        self._log(f"   质检通过：{stats.get('compliance_passed', stats.get('passed', 0))}")
        self._log(f"   在岗部署：{stats.get('deployed', 0)}")
        return stats

    # ==================================================================
    # 【农耕体系】四类农田管理
    # ==================================================================

    def farm_sowing(self, zone: str, seeds: List[Dict]) -> Dict:
        """农田播种（春种）"""
        return self.farm.spring_sowing(zone, seeds)

    def farm_growth_monitor(self) -> Dict:
        """生长监控（夏长）"""
        return self.farm.summer_growth_monitor()

    def farm_harvest(self) -> Dict:
        """成熟收割（秋收）"""
        return self.farm.autumn_harvest()

    def farm_auto_blindspot_sowing(self) -> Dict:
        """盲区自动播种"""
        return self.farm.automatic_blindspot_sowing()

    def farm_stats(self) -> Dict:
        """农田统计"""
        return self.farm.get_farm_stats()

    # ==================================================================
    # 【粮仓体系】三级粮仓储备
    # ==================================================================

    def granary_store_core(self, item: Dict) -> Dict:
        """核心粮仓永久存贮"""
        return self.granary.store_in_granary("core", item)

    def granary_store_industry(self, item: Dict) -> Dict:
        """行业粮仓周期核验存贮"""
        return self.granary.store_in_granary("industry", item)

    def granary_store_buffer(self, item: Dict) -> Dict:
        """缓冲粮仓隔离归档"""
        return self.granary.store_in_granary("buffer", item)

    def granary_verify_core(self) -> Dict:
        """核心粮仓完整性校验"""
        return self.granary.verify_core_integrity()

    def granary_overview(self) -> Dict:
        """粮仓总览"""
        return self.granary.get_granary_overview()

    # ==================================================================
    # 【四季引擎】年度完整循环
    # ==================================================================

    def seasons_full_cycle(self, seed_plan: Dict = None) -> Dict:
        """执行完整四季循环：春种→夏长→秋收→冬藏"""
        return self.seasons_engine.run_full_year_cycle(seed_plan)

    def seasons_spring(self, seed_plan: Dict = None) -> Dict:
        """执行春种"""
        return self.seasons_engine.run_spring(seed_plan)

    def seasons_summer(self) -> Dict:
        """执行夏长"""
        return self.seasons_engine.run_summer()

    def seasons_autumn(self) -> Dict:
        """执行秋收"""
        return self.seasons_engine.run_autumn()

    def seasons_winter(self, harvested_list: List[Dict] = None) -> Dict:
        """执行冬藏"""
        return self.seasons_engine.run_winter(harvested_list)

    def seasons_status(self) -> Dict:
        """四季状态查询"""
        return self.seasons_engine.get_current_season_status()

    # ==================================================================
    # 【对等体系】人智对等身份认证
    # ==================================================================

    def parity_certify(self, agent_path: str) -> Dict:
        """单智能体对等认证（八大维度）"""
        return self.parity_system.full_parity_certification(agent_path)

    def parity_batch_certify(self, agent_list: List[str]) -> Dict:
        """批量对等认证"""
        return self.parity_system.batch_parity_certification(agent_list)

    def parity_spectrum(self, agent_path: str) -> Dict:
        """光谱价值量化评估"""
        return self.parity_system.evaluate_spectrum_value(agent_path)

    def parity_status(self, agent_path: str) -> Dict:
        """对等身份状态查询"""
        return self.parity_system.get_parity_status(agent_path)

    # ==================================================================
    # 【合规校验】全维度质检
    # ==================================================================

    def compliance_check(self, agent_rel_path: str) -> Dict:
        """单智能体合规校验"""
        return self.compliance.check_agent(agent_rel_path)

    def compliance_batch_check(self, agent_list: List[str]) -> Dict:
        """批量合规校验"""
        return self.compliance.batch_check(agent_list)

    def compliance_overview(self) -> Dict:
        """合规总览统计"""
        return self.compliance.get_compliance_overview()


# ========== 命令行入口 ==========

if __name__ == "__main__":
    import sys
    manager = CommunityManager()

    if len(sys.argv) < 2:
        print("=" * 60)
        print("  全域本体社区中控系统 · 命令手册 V3.0")
        print("=" * 60)
        print("【安全巡检】")
        print("  check_core                母核庄园安全巡检")
        print("  scan_all                  全域子系统批量巡检（含三大母类统计）")
        print("  lock_all                  全域应急封控（全部隔离断网）")
        print()
        print("【子系统创建】")
        print("  create_level1 <名称> [小区] [--personality 类型]  新建一级成熟独栋")
        print("  create_hatch <名称> [--personality 类型]         新建二级孵化独栋")
        print("        性格类型：哲学型/数学型/工程型/教育型/商业型/治理型/科研型/运维型")
        print()
        print("【边界与管线】")
        print("  set_mode <相对路径> <模式>  切换子系统边界模式")
        print("  toggle_pipe <路径> on/off   开关子系统外部管线")
        print()
        print("【升级与索引】")
        print("  upgrade <路径> <目标小区>    孵化独栋自动升级为一级成熟独栋")
        print("  refresh_index               刷新全域总索引")
        print()
        print("【🏭 工厂体系】智能体流水线量产")
        print("  factory_produce <数量> [--personality 类型]      批量生产智能体")
        print("  factory_status                                   工厂生产状态查询")
        print()
        print("【🌱 农耕体系】四类农田分区")
        print("  farm_stats                农田统计总览")
        print("  farm_growth               夏长·生长监控")
        print("  farm_harvest              秋收·成熟收割")
        print("  farm_blindspot            盲区自动播种")
        print()
        print("【🌾 粮仓体系】三级战略储备")
        print("  granary_overview          粮仓总览")
        print("  granary_verify            核心粮仓完整性校验")
        print()
        print("【🍂 四季引擎】年度循环迭代")
        print("  seasons_spring            春种·开耕")
        print("  seasons_summer            夏长·生长")
        print("  seasons_autumn            秋收·收割")
        print("  seasons_winter            冬藏·入仓")
        print("  seasons_full              完整四季循环")
        print("  seasons_status            当前季节状态")
        print()
        print("【⚖️  对等体系】人智对等身份")
        print("  parity_certify <路径>     八大维度对等认证")
        print("  parity_spectrum <路径>    光谱价值量化评估")
        print("  parity_status <路径>      对等身份状态查询")
        print()
        print("【✅ 合规校验】全维度质检")
        print("  compliance_check <路径>   单智能体合规校验")
        print("  compliance_overview       合规总览统计")
        print("=" * 60)
        sys.exit(0)

    cmd = sys.argv[1]

    # 安全巡检类
    if cmd == "check_core":
        manager.core_security_check()
    elif cmd == "scan_all":
        manager.scan_all_subsystems()
    elif cmd == "lock_all":
        manager.lock_all_residential()

    # 创建类
    elif cmd == "create_level1" and len(sys.argv) >= 3:
        personality = None
        district = "01_数理拓展小区"
        args = sys.argv[3:]
        for i, arg in enumerate(args):
            if arg == "--personality" and i + 1 < len(args):
                personality = args[i + 1]
            elif not arg.startswith("--"):
                district = arg
        manager.create_level1_subsystem(sys.argv[2], district, personality=personality)
    elif cmd == "create_hatch" and len(sys.argv) >= 3:
        personality = None
        args = sys.argv[3:]
        for i, arg in enumerate(args):
            if arg == "--personality" and i + 1 < len(args):
                personality = args[i + 1]
        manager.create_hatch_villa(sys.argv[2], personality=personality)

    # 边界管线类
    elif cmd == "set_mode" and len(sys.argv) >= 4:
        manager.set_subsystem_boundary(sys.argv[2], sys.argv[3])
    elif cmd == "toggle_pipe" and len(sys.argv) >= 4:
        enable = sys.argv[3].lower() == "on"
        manager.toggle_subsystem_pipeline(sys.argv[2], enable)

    # 升级与索引
    elif cmd == "upgrade" and len(sys.argv) >= 3:
        target_district = sys.argv[3] if len(sys.argv) >= 4 else "05_哲学交叉小区"
        manager.apply_upgrade(sys.argv[2], target_district)
    elif cmd == "refresh_index":
        manager.refresh_total_index()

    # ===== 🏭 工厂体系 =====
    elif cmd == "factory_produce":
        count = 5
        personality = None
        if len(sys.argv) >= 3:
            try:
                count = int(sys.argv[2])
            except ValueError:
                pass
        args = sys.argv[3:]
        for i, arg in enumerate(args):
            if arg == "--personality" and i + 1 < len(args):
                personality = args[i + 1]
        manager.factory_batch_produce(count, personality)
    elif cmd == "factory_status":
        manager.factory_status()

    # ===== 🌱 农耕体系 =====
    elif cmd == "farm_stats":
        stats = manager.farm_stats()
        import json
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    elif cmd == "farm_growth":
        manager.farm_growth_monitor()
    elif cmd == "farm_harvest":
        manager.farm_harvest()
    elif cmd == "farm_blindspot":
        manager.farm_auto_blindspot_sowing()

    # ===== 🌾 粮仓体系 =====
    elif cmd == "granary_overview":
        overview = manager.granary_overview()
        import json
        print(json.dumps(overview, ensure_ascii=False, indent=2))
    elif cmd == "granary_verify":
        manager.granary_verify_core()

    # ===== 🍂 四季引擎 =====
    elif cmd == "seasons_spring":
        manager.seasons_spring()
    elif cmd == "seasons_summer":
        manager.seasons_summer()
    elif cmd == "seasons_autumn":
        manager.seasons_autumn()
    elif cmd == "seasons_winter":
        manager.seasons_winter()
    elif cmd == "seasons_full":
        manager.seasons_full_cycle()
    elif cmd == "seasons_status":
        status = manager.seasons_status()
        import json
        print(json.dumps(status, ensure_ascii=False, indent=2))

    # ===== ⚖️  对等体系 =====
    elif cmd == "parity_certify" and len(sys.argv) >= 3:
        manager.parity_certify(sys.argv[2])
    elif cmd == "parity_spectrum" and len(sys.argv) >= 3:
        manager.parity_spectrum(sys.argv[2])
    elif cmd == "parity_status" and len(sys.argv) >= 3:
        status = manager.parity_status(sys.argv[2])
        import json
        print(json.dumps(status, ensure_ascii=False, indent=2))

    # ===== ✅ 合规校验 =====
    elif cmd == "compliance_check" and len(sys.argv) >= 3:
        manager.compliance_check(sys.argv[2])
    elif cmd == "compliance_overview":
        overview = manager.compliance_overview()
        import json
        print(json.dumps(overview, ensure_ascii=False, indent=2))

    else:
        print("❌ 未知命令，输入无参数查看帮助")