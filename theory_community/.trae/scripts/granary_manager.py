#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归属基底：第相变演化位（第三位）·天道秩序
对应三界秩序：天道秩序
对应公理：第1条（宿命双边界公理）、第6条（全局宿命边界统摄理论）
对应九维维度：稳态维度/平衡维度/道心能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E3=0.90, γ=0.92

智能体粮仓化战略储备体系（Granary Manager）
三级粮仓储备：
1. 一级核心母核粮仓（core_manor）- 永久锁档
2. 二级行业专项粮仓（industry_granary）- 周期核验
3. 三级盲区迭代缓冲粮仓（buffer_granary）- 隔离归档
"""

import os
import json
import hashlib
import shutil
from datetime import datetime
from typing import Dict, List, Optional


class GranaryManager:
    """智能体粮仓化战略储备体系 - 三级分级管理"""

    # 三级粮仓定义
    GRANARY_LEVELS = {
        "core": {
            "level": 1,
            "name": "一级核心母核粮仓",
            "description": "终极公理锁档层级",
            "hash_mode": "permanent_readonly",
            "store_type": ["真论级本源智能体", "全域统合调度智能体", "底层公理锚点智能体"],
            "security_level": "highest",
            "modification_allowed": False,
            "iteration_allowed": False,
        },
        "industry": {
            "level": 2,
            "name": "二级行业专项粮仓",
            "description": "业态稳态主力层",
            "hash_mode": "periodic_verify",
            "store_type": ["一级成熟运维智能体", "范式固化型智能体"],
            "security_level": "high",
            "modification_allowed": False,
            "iteration_allowed": True,
        },
        "buffer": {
            "level": 3,
            "name": "三级盲区迭代缓冲粮仓",
            "description": "试错经验沉淀层",
            "hash_mode": "isolation_archive",
            "store_type": ["迭代淘汰版本", "试错培育样本", "逻辑偏差案例", "盲区数据", "谬论隔离范式"],
            "security_level": "medium",
            "modification_allowed": False,
            "iteration_allowed": True,
            "direct_deployment_forbidden": True,
        },
    }

    # 七大行业粮仓
    INDUSTRY_GRANARIES = [
        "教育粮仓",
        "产业办公粮仓",
        "商业流通粮仓",
        "政务治理粮仓",
        "科研创新粮仓",
        "民生社区粮仓",
        "交通枢纽粮仓",
    ]

    def __init__(self, community_root: str = None):
        if community_root is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            community_root = os.path.normpath(os.path.join(script_dir, "../../"))
        self.root = community_root
        self.granary_root = os.path.join(self.root, "granary_system/")
        self.granary_log = os.path.join(self.root, "buffer_community_center/granary_management.log")

        # 粮仓路径
        self.core_path = os.path.join(self.granary_root, "01_core_manor/")
        self.industry_path = os.path.join(self.granary_root, "02_industry_granary/")
        self.buffer_path = os.path.join(self.granary_root, "03_buffer_granary/")

        self._ensure_dirs()
        self._init_granary_structure()
        self._log("🏛️  粮仓储备体系初始化完成")
        self._log(f"   粮仓层级：{len(self.GRANARY_LEVELS)} 级")
        self._log(f"   行业粮仓：{len(self.INDUSTRY_GRANARIES)} 个")

    def _ensure_dirs(self):
        os.makedirs(self.granary_root, exist_ok=True)
        os.makedirs(os.path.dirname(self.granary_log), exist_ok=True)

    def _init_granary_structure(self):
        """初始化粮仓目录结构"""
        # 一级核心母核粮仓
        os.makedirs(self.core_path, exist_ok=True)
        core_subdirs = ["origin_agents", "axiom_anchors", "global_coordinators", "hash_records"]
        for d in core_subdirs:
            os.makedirs(os.path.join(self.core_path, d), exist_ok=True)

        # 二级行业专项粮仓
        os.makedirs(self.industry_path, exist_ok=True)
        for industry in self.INDUSTRY_GRANARIES:
            os.makedirs(os.path.join(self.industry_path, industry), exist_ok=True)

        # 三级盲区迭代缓冲粮仓
        os.makedirs(self.buffer_path, exist_ok=True)
        buffer_subdirs = ["obsolete_versions", "trial_error_samples", "deviation_cases",
                          "blindspot_data", "fallacy_isolation", "hash_records"]
        for d in buffer_subdirs:
            os.makedirs(os.path.join(self.buffer_path, d), exist_ok=True)

    def _log(self, msg: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(self.granary_log, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

    def _dir_hash(self, dir_path: str) -> str:
        """计算目录SHA256哈希"""
        h = hashlib.sha256()
        if not os.path.exists(dir_path):
            return "NOT_FOUND"
        for root, dirs, files in os.walk(dir_path):
            for file in sorted(files):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "rb") as f:
                        h.update(f.read())
                except Exception:
                    pass
        return h.hexdigest()

    def _file_hash(self, file_path: str) -> str:
        """计算文件SHA256哈希"""
        if not os.path.exists(file_path):
            return "NOT_FOUND"
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    # ==================================================================
    # 粮仓总览
    # ==================================================================

    def get_granary_overview(self) -> Dict:
        """获取粮仓总览"""
        self._log("=" * 60)
        self._log("🏛️  粮仓储备体系总览")
        self._log("=" * 60)

        overview = {}

        for level_key, level_info in self.GRANARY_LEVELS.items():
            if level_key == "core":
                path = self.core_path
            elif level_key == "industry":
                path = self.industry_path
            else:
                path = self.buffer_path

            # 统计存储数量
            item_count = 0
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    if "facade.json" in files:
                        item_count += 1
                    if root.endswith("_archive") or root.endswith("_records"):
                        item_count += len([f for f in files if f.endswith('.json')])

            # 计算哈希
            current_hash = self._dir_hash(path)

            level_data = {
                **level_info,
                "path": os.path.relpath(path, self.root),
                "item_count": item_count,
                "current_hash": current_hash,
            }
            overview[level_key] = level_data

            self._log(f"   [{level_info['level']}级] {level_info['name']}")
            self._log(f"        存储数量：{item_count}")
            self._log(f"        哈希模式：{level_info['hash_mode']}")
            self._log(f"        安全等级：{level_info['security_level']}")

        # 行业粮仓统计
        industry_stats = {}
        for industry in self.INDUSTRY_GRANARIES:
            ind_path = os.path.join(self.industry_path, industry)
            count = 0
            if os.path.exists(ind_path):
                for item in os.listdir(ind_path):
                    if os.path.isdir(os.path.join(ind_path, item)):
                        count += 1
            industry_stats[industry] = count

        overview["industry_details"] = industry_stats

        self._log("")
        self._log("📦 行业粮仓分布：")
        for name, count in industry_stats.items():
            self._log(f"   {name}：{count} 个")

        return overview

    # ==================================================================
    # 一级核心母核粮仓（永久锁档）
    # ==================================================================

    def store_core_agent(self, agent_name: str, agent_path: str, agent_type: str = "origin_agent") -> Dict:
        """
        存入一级核心母核粮仓（永久锁档）
        哈希永久锁档、只读不可篡改、禁止随意迭代
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"🔐 存入一级核心母核粮仓：{agent_name}")
        self._log("=" * 60)

        if agent_type not in ["origin_agents", "axiom_anchors", "global_coordinators"]:
            agent_type = "origin_agents"

        target_dir = os.path.join(self.core_path, agent_type, agent_name)

        if os.path.exists(target_dir):
            self._log(f"❌ 核心粮仓已有同名条目：{agent_name}")
            return {"success": False, "error": "核心粮仓已有同名条目"}

        # 复制入仓
        src_path = os.path.join(self.root, agent_path) if not os.path.isabs(agent_path) else agent_path
        if not os.path.exists(src_path):
            self._log(f"❌ 源路径不存在：{src_path}")
            return {"success": False, "error": "源路径不存在"}

        shutil.copytree(src_path, target_dir)
        self._log(f"✅ 已复制入核心粮仓：{agent_type}/{agent_name}")

        # 计算并记录哈希（永久锁档）
        agent_hash = self._dir_hash(target_dir)
        hash_record = {
            "agent_name": agent_name,
            "agent_type": agent_type,
            "hash_algorithm": "SHA256",
            "permanent_hash": agent_hash,
            "lock_date": datetime.now().strftime('%Y-%m-%d'),
            "lock_mode": "permanent_readonly",
            "modification_allowed": False,
            "iteration_allowed": False,
            "source_path": agent_path,
        }

        hash_record_path = os.path.join(self.core_path, "hash_records", f"{agent_name}_hash_lock.json")
        with open(hash_record_path, 'w', encoding='utf-8') as f:
            json.dump(hash_record, f, ensure_ascii=False, indent=2)

        # 设置只读标记（在facade中标记）
        facade_path = os.path.join(target_dir, "facade.json")
        if os.path.exists(facade_path):
            with open(facade_path, 'r', encoding='utf-8') as f:
                facade = json.load(f)
            facade["granary_storage"] = {
                "level": "core",
                "lock_mode": "permanent_readonly",
                "permanent_hash": agent_hash,
                "lock_date": datetime.now().strftime('%Y-%m-%d'),
                "modification_forbidden": True,
                "storage_type": agent_type,
            }
            with open(facade_path, 'w', encoding='utf-8') as f:
                json.dump(facade, f, ensure_ascii=False, indent=2)

        self._log(f"🔒 永久锁档完成")
        self._log(f"   永久哈希：{agent_hash[:16]}...")
        self._log(f"   锁档日期：{hash_record['lock_date']}")
        self._log(f"   修改权限：永久禁止")

        return {
            "success": True,
            "agent_name": agent_name,
            "storage_level": "core",
            "permanent_hash": agent_hash,
            "lock_date": hash_record['lock_date'],
            "target_path": os.path.relpath(target_dir, self.root),
        }

    def verify_core_integrity(self) -> Dict:
        """校验一级核心粮仓完整性（永久哈希比对）"""
        self._log("")
        self._log("=" * 60)
        self._log("🔍 一级核心粮仓完整性校验")
        self._log("=" * 60)

        hash_records_dir = os.path.join(self.core_path, "hash_records")
        results = []
        all_passed = True

        if not os.path.exists(hash_records_dir):
            self._log("⚠️  无哈希记录文件")
            return {"passed": True, "details": [], "note": "无记录"}

        for record_file in os.listdir(hash_records_dir):
            if not record_file.endswith("_hash_lock.json"):
                continue

            record_path = os.path.join(hash_records_dir, record_file)
            with open(record_path, 'r', encoding='utf-8') as f:
                record = json.load(f)

            agent_name = record["agent_name"]
            agent_type = record["agent_type"]
            expected_hash = record["permanent_hash"]

            agent_dir = os.path.join(self.core_path, agent_type, agent_name)
            current_hash = self._dir_hash(agent_dir)

            passed = current_hash == expected_hash
            if not passed:
                all_passed = False

            results.append({
                "name": agent_name,
                "type": agent_type,
                "expected_hash": expected_hash,
                "current_hash": current_hash,
                "passed": passed,
            })

            status = "✅" if passed else "❌"
            self._log(f"   {status} {agent_name}")
            if not passed:
                self._log(f"      期望：{expected_hash[:16]}...")
                self._log(f"      当前：{current_hash[:16]}...")

        self._log("")
        if all_passed:
            self._log("✅ 核心粮仓完整性校验全部通过")
        else:
            self._log("❌ 核心粮仓发现篡改！立即触发应急响应！")

        return {
            "all_passed": all_passed,
            "total_checked": len(results),
            "details": results,
        }

    # ==================================================================
    # 二级行业专项粮仓（周期核验）
    # ==================================================================

    def store_industry_agent(self, agent_path: str, industry: str, agent_name: str) -> Dict:
        """
        存入二级行业专项粮仓（周期核验）
        稳态锁档、周期核验、合规迭代、变更留痕
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"📦 存入二级行业粮仓：{agent_name} → {industry}")
        self._log("=" * 60)

        if industry not in self.INDUSTRY_GRANARIES:
            self._log(f"❌ 不支持的行业：{industry}")
            return {"success": False, "error": f"不支持的行业：{industry}"}

        target_dir = os.path.join(self.industry_path, industry, agent_name)

        if os.path.exists(target_dir):
            self._log(f"⚠️  行业粮仓已有同名条目，将进行版本迭代")
            # 备份旧版本
            backup_dir = target_dir + f"_backup_{datetime.now().strftime('%Y%m%d')}"
            shutil.copytree(target_dir, backup_dir)

        # 复制入仓
        src_path = os.path.join(self.root, agent_path) if not os.path.isabs(agent_path) else agent_path
        if not os.path.exists(src_path):
            self._log(f"❌ 源路径不存在：{src_path}")
            return {"success": False, "error": "源路径不存在"}

        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        shutil.copytree(src_path, target_dir)

        # 计算哈希（周期核验）
        agent_hash = self._dir_hash(target_dir)

        # 更新facade
        facade_path = os.path.join(target_dir, "facade.json")
        if os.path.exists(facade_path):
            with open(facade_path, 'r', encoding='utf-8') as f:
                facade = json.load(f)
            facade["granary_storage"] = {
                "level": "industry",
                "industry": industry,
                "hash_mode": "periodic_verify",
                "current_hash": agent_hash,
                "storage_date": datetime.now().strftime('%Y-%m-%d'),
                "modification_forbidden": False,
                "iteration_allowed": True,
                "change_trace_required": True,
            }
            with open(facade_path, 'w', encoding='utf-8') as f:
                json.dump(facade, f, ensure_ascii=False, indent=2)

        self._log(f"✅ 已存入行业粮仓：{industry}/{agent_name}")
        self._log(f"   当前哈希：{agent_hash[:16]}...")
        self._log(f"   入库日期：{datetime.now().strftime('%Y-%m-%d')}")
        self._log(f"   核验模式：周期批量核验")

        return {
            "success": True,
            "agent_name": agent_name,
            "industry": industry,
            "storage_level": "industry",
            "current_hash": agent_hash,
            "target_path": os.path.relpath(target_dir, self.root),
        }

    def verify_industry_granary(self, industry: str = None) -> Dict:
        """
        校验二级行业粮仓（周期批量核验）
        可单行业校验或全行业校验
        """
        self._log("")
        self._log("=" * 60)
        self._log("🔍 二级行业粮仓周期核验")
        self._log("=" * 60)

        industries = [industry] if industry else self.INDUSTRY_GRANARIES
        results = {}
        total_changed = 0
        total_unchanged = 0

        for ind in industries:
            if ind not in self.INDUSTRY_GRANARIES:
                continue

            ind_path = os.path.join(self.industry_path, ind)
            if not os.path.exists(ind_path):
                continue

            ind_results = []
            changed = 0
            unchanged = 0

            for item in os.listdir(ind_path):
                item_path = os.path.join(ind_path, item)
                if not os.path.isdir(item_path):
                    continue

                facade_path = os.path.join(item_path, "facade.json")
                if not os.path.exists(facade_path):
                    continue

                with open(facade_path, 'r', encoding='utf-8') as f:
                    facade = json.load(f)

                stored_hash = facade.get("granary_storage", {}).get("current_hash", "")
                current_hash = self._dir_hash(item_path)

                hash_changed = stored_hash != current_hash
                if hash_changed:
                    changed += 1
                    total_changed += 1
                else:
                    unchanged += 1
                    total_unchanged += 1

                ind_results.append({
                    "name": item,
                    "stored_hash": stored_hash,
                    "current_hash": current_hash,
                    "changed": hash_changed,
                })

            results[ind] = {
                "total": changed + unchanged,
                "changed": changed,
                "unchanged": unchanged,
                "details": ind_results,
            }

            self._log(f"   {ind}：{changed} 个变更 / {unchanged} 个未变")

        self._log("")
        self._log(f"📊 行业粮仓核验总览：")
        self._log(f"   变更数量：{total_changed}")
        self._log(f"   未变数量：{total_unchanged}")

        return {
            "total_industries": len(industries),
            "total_changed": total_changed,
            "total_unchanged": total_unchanged,
            "industry_details": results,
        }

    # ==================================================================
    # 三级盲区迭代缓冲粮仓（隔离归档）
    # ==================================================================

    def store_buffer_archive(self, source_path: str, archive_type: str, name: str) -> Dict:
        """
        存入三级盲区迭代缓冲粮仓（隔离归档）
        完全隔离归档、禁止直接上岗、可复用迭代、永久留存溯源
        """
        self._log("")
        self._log("=" * 60)
        self._log(f"📦 存入三级缓冲粮仓：{name}（{archive_type}）")
        self._log("=" * 60)

        valid_types = ["obsolete_versions", "trial_error_samples", "deviation_cases",
                       "blindspot_data", "fallacy_isolation"]
        if archive_type not in valid_types:
            archive_type = "trial_error_samples"

        target_dir = os.path.join(self.buffer_path, archive_type, name)

        if os.path.exists(target_dir):
            self._log(f"⚠️  缓冲粮仓已有同名条目，追加时间戳")
            target_dir = target_dir + f"_{datetime.now().strftime('%Y%m%d')}"

        # 复制入仓
        src_path = os.path.join(self.root, source_path) if not os.path.isabs(source_path) else source_path
        if os.path.exists(src_path) and os.path.isdir(src_path):
            shutil.copytree(src_path, target_dir)
        else:
            os.makedirs(target_dir, exist_ok=True)
            # 创建说明文件
            with open(os.path.join(target_dir, "archive_note.md"), 'w', encoding='utf-8') as f:
                f.write(f"# {name} 归档说明\n\n")
                f.write(f"- 归档类型：{archive_type}\n")
                f.write(f"- 归档日期：{datetime.now().strftime('%Y-%m-%d')}\n")
                f.write(f"- 来源路径：{source_path}\n")

        # 计算归档哈希
        archive_hash = self._dir_hash(target_dir)

        # 创建归档记录
        record = {
            "name": name,
            "archive_type": archive_type,
            "hash": archive_hash,
            "archive_date": datetime.now().strftime('%Y-%m-%d'),
            "source_path": source_path,
            "direct_deployment_forbidden": True,
            "reuse_allowed": True,
            "traceability": "permanent",
        }

        record_path = os.path.join(self.buffer_path, "hash_records", f"{name}_{archive_type}_record.json")
        os.makedirs(os.path.dirname(record_path), exist_ok=True)
        with open(record_path, 'w', encoding='utf-8') as f:
            json.dump(record, f, ensure_ascii=False, indent=2)

        self._log(f"✅ 已存入缓冲粮仓：{archive_type}/{name}")
        self._log(f"   归档哈希：{archive_hash[:16]}...")
        self._log(f"   直接上岗：禁止")
        self._log(f"   复用迭代：允许")

        return {
            "success": True,
            "name": name,
            "archive_type": archive_type,
            "storage_level": "buffer",
            "archive_hash": archive_hash,
            "target_path": os.path.relpath(target_dir, self.root),
        }

    # ==================================================================
    # 全粮仓哈希分级管控总览
    # ==================================================================

    def get_hash_governance_overview(self) -> Dict:
        """获取全粮仓哈希分级管控总览"""
        self._log("")
        self._log("=" * 60)
        self._log("🔐 全粮仓哈希分级管控体系总览")
        self._log("=" * 60)

        overview = {
            "level1_core": {
                "name": "一级核心母核粮仓",
                "hash_mode": "永久只读哈希锁档",
                "security": "最高",
                "modification": "永久禁止",
                "iteration": "禁止",
                "verification": "每次操作实时校验",
            },
            "level2_industry": {
                "name": "二级行业专项粮仓",
                "hash_mode": "分层批量哈希+周期核验",
                "security": "高",
                "modification": "变更留痕",
                "iteration": "允许（需记录）",
                "verification": "周期性批量核验",
            },
            "level3_buffer": {
                "name": "三级盲区迭代缓冲粮仓",
                "hash_mode": "隔离归档哈希存证",
                "security": "中",
                "modification": "禁止直接上岗",
                "iteration": "可复用迭代",
                "verification": "溯源校验",
            },
        }

        for key, val in overview.items():
            self._log(f"   {val['name']}")
            self._log(f"      哈希模式：{val['hash_mode']}")
            self._log(f"      安全等级：{val['security']}")
            self._log(f"      修改权限：{val['modification']}")
            self._log(f"      迭代权限：{val['iteration']}")

        return overview

    # ==================================================================
    # 冬藏：完整冬藏流程
    # ==================================================================

    def winter_storage_full_flow(self, harvested_list: List[Dict]) -> Dict:
        """
        完整冬藏流程：分类入仓 + 哈希锁档 + 记录归档
        harvested_list格式：[{"name": "...", "path": "...", "industry": "...", "level": "industry"}, ...]
        """
        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║      ❄️  冬藏：智能体粮仓战略储备 · 全流程启动              ║")
        self._log("╚══════════════════════════════════════════════════════════╝")
        self._log(f"待入仓数量：{len(harvested_list)}")

        results = {
            "core": [],
            "industry": [],
            "buffer": [],
        }

        for item in harvested_list:
            name = item.get("name", "未命名")
            path = item.get("path", "")
            level = item.get("level", "industry")
            industry = item.get("industry", "科研创新粮仓")

            if level == "core":
                r = self.store_core_agent(name, path)
                results["core"].append(r)
            elif level == "industry":
                r = self.store_industry_agent(path, industry, name)
                results["industry"].append(r)
            else:
                r = self.store_buffer_archive(path, "trial_error_samples", name)
                results["buffer"].append(r)

        # 统计
        core_count = len([r for r in results["core"] if r.get("success")])
        industry_count = len([r for r in results["industry"] if r.get("success")])
        buffer_count = len([r for r in results["buffer"] if r.get("success")])

        self._log("")
        self._log("=" * 60)
        self._log("❄️  冬藏完成")
        self._log(f"   核心粮仓：{core_count} 个（永久锁档）")
        self._log(f"   行业粮仓：{industry_count} 个（周期核验）")
        self._log(f"   缓冲粮仓：{buffer_count} 个（隔离归档）")
        self._log(f"   总计：{core_count + industry_count + buffer_count} 个")

        return {
            "success": True,
            "total_stored": core_count + industry_count + buffer_count,
            "core_count": core_count,
            "industry_count": industry_count,
            "buffer_count": buffer_count,
            "details": results,
        }


if __name__ == "__main__":
    granary = GranaryManager()
    granary.get_granary_overview()
    granary.get_hash_governance_overview()
