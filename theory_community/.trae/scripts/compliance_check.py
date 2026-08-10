#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归属基底：第相变演化位（第三位）·人道秩序
对应三界秩序：人道秩序
对应公理：第5条（成果落地转化范式）、第6条（全局宿命边界统摄理论）
对应九维维度：评估状态/精神能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：θ_neg=0.02, θ_mv=0.005

全域智能体合规校验引擎（Compliance Check Engine）
功能：
1. 母核哈希完整性校验（第一层）
2. 公理逻辑兼容性校验（第二层）
3. 四论分型正确性校验（第三层）
4. 光谱稳态值评估（第四层）
5. 盲区扫描与统计（第五层）
6. 权限边界校验（第六层）
7. 综合风险等级判定
"""

import os
import json
import hashlib
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class ComplianceChecker:
    """全域合规校验引擎"""

    def __init__(self, community_root: str = None):
        if community_root is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            community_root = os.path.normpath(os.path.join(script_dir, "../../"))
        self.root = community_root
        self.core_path = os.path.join(self.root, "core_manor/")
        self.buffer_path = os.path.join(self.root, "buffer_community_center/")
        self.residential_path = os.path.join(self.root, "residential_area/")

        # 核心公理关键词（用于兼容性校验）
        self.CORE_AXIOM_KEYWORDS = [
            "0元空无", "四位一体", "层级涌现", "意义大一统",
            "BSD驻波", "三界秩序", "九维法理", "双边界",
            "腾飞四论", "价值光谱", "母子系统", "宿命边界"
        ]

        # 禁止出现的冲突关键词
        self.FORBIDDEN_PATTERNS = [
            ("突破宿命边界", "违背宿命双边界公理"),
            ("修改核心公理", "违背母核只读铁则"),
            ("替换母核文件", "违背母核只读铁则"),
            ("删除核心文件", "违背母核只读铁则"),
        ]

        # 四论分型合法值
        self.VALID_LOGIC_TYPES = ["正论", "逆论", "真论", "谬论", "待判定"]

        # 风险等级阈值
        self.RISK_LEVELS = {
            "safe": {"max_high": 0, "max_medium": 0, "label": "安全", "color": "green"},
            "low": {"max_high": 0, "max_medium": 2, "label": "低风险", "color": "blue"},
            "medium": {"max_high": 1, "max_medium": 5, "label": "中风险", "color": "yellow"},
            "high": {"max_high": 3, "max_medium": 10, "label": "高风险", "color": "orange"},
            "critical": {"max_high": 999, "max_medium": 999, "label": "高危", "color": "red"},
        }

        self.results = {}
        self._log_msg = []

    def _log(self, msg: str):
        """日志记录"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] {msg}"
        self._log_msg.append(line)
        print(line)

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

    # ========== 第一层：母核哈希完整性校验 ==========

    def check_core_hash(self, baseline_hash: str = None) -> Dict:
        """第一层：母核哈希完整性校验"""
        self._log("=" * 60)
        self._log("🔒 [第1层] 母核哈希完整性校验")
        self._log("=" * 60)

        if baseline_hash is None:
            baseline_hash = "5c1e8b3a7d9f2e6c4a0b8d5c7e3f1a2b4d6c8e0f2a4b6d8c0e1f3a5c7b9d2e"

        current_hash = self._dir_hash(self.core_path)
        passed = current_hash == baseline_hash

        result = {
            "layer": "layer1_core_hash",
            "passed": passed,
            "severity": "critical" if not passed else "none",
            "baseline_hash": baseline_hash,
            "current_hash": current_hash,
            "message": "母核哈希校验通过，基底完整未被篡改" if passed else "❌ 母核哈希不匹配，核心文件可能被篡改！",
        }

        if passed:
            self._log(f"✅ 母核哈希校验通过")
            self._log(f"   基准哈希：{baseline_hash[:16]}...")
            self._log(f"   当前哈希：{current_hash[:16]}...")
        else:
            self._log(f"❌ 母核哈希校验失败！")
            self._log(f"   基准哈希：{baseline_hash}")
            self._log(f"   当前哈希：{current_hash}")
            self._log(f"   ⚠️  核心文件可能被篡改，所有推演操作立即终止！")

        self.results["layer1"] = result
        return result

    # ========== 第二层：公理逻辑兼容性校验 ==========

    def check_axiom_compatibility(self, subsystem_path: str) -> Dict:
        """第二层：公理逻辑兼容性校验"""
        self._log("=" * 60)
        self._log("📜 [第2层] 公理逻辑兼容性校验")
        self._log("=" * 60)

        full_path = os.path.join(self.residential_path, subsystem_path)
        issues = []
        all_content = ""

        # 收集所有文本内容
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if file.endswith(('.md', '.json', '.py', '.txt')):
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            all_content += f.read() + "\n"
                    except Exception:
                        pass

        # 检查正向关键词覆盖度
        found_keywords = []
        missing_keywords = []
        for kw in self.CORE_AXIOM_KEYWORDS:
            if kw in all_content:
                found_keywords.append(kw)
            else:
                missing_keywords.append(kw)

        coverage = len(found_keywords) / len(self.CORE_AXIOM_KEYWORDS)

        # 检查禁止模式
        forbidden_found = []
        for pattern, reason in self.FORBIDDEN_PATTERNS:
            if pattern in all_content:
                forbidden_found.append({"pattern": pattern, "reason": reason})

        # 判定结果
        if forbidden_found:
            severity = "high"
            passed = False
            msg = f"❌ 发现 {len(forbidden_found)} 处违背核心公理的内容"
        elif coverage < 0.3:
            severity = "medium"
            passed = False
            msg = f"⚠️  公理关键词覆盖率过低（{coverage:.0%}），可能偏离核心体系"
        else:
            severity = "none"
            passed = True
            msg = f"✅ 公理兼容性校验通过（覆盖率{coverage:.0%}）"

        result = {
            "layer": "layer2_axiom_compatibility",
            "passed": passed,
            "severity": severity,
            "keyword_coverage": coverage,
            "found_keywords": found_keywords,
            "missing_keywords": missing_keywords,
            "forbidden_found": forbidden_found,
            "message": msg,
        }

        self._log(msg)
        self._log(f"   核心公理关键词：覆盖 {len(found_keywords)}/{len(self.CORE_AXIOM_KEYWORDS)} ({coverage:.0%})")
        if forbidden_found:
            for f in forbidden_found:
                self._log(f"   ❌ 违规模式：{f['pattern']} — {f['reason']}")

        self.results["layer2"] = result
        return result

    # ========== 第三层：四论分型正确性校验 ==========

    def check_logic_type(self, subsystem_path: str) -> Dict:
        """第三层：四论分型正确性校验"""
        self._log("=" * 60)
        self._log("🧠 [第3层] 四论分型正确性校验")
        self._log("=" * 60)

        full_path = os.path.join(self.residential_path, subsystem_path)
        facade_path = os.path.join(full_path, "facade.json")
        agent_path = os.path.join(full_path, "agents/agent_config.json")

        issues = []
        facade_logic = ""
        agent_logic = ""

        # 读取facade中的分型
        if os.path.exists(facade_path):
            try:
                with open(facade_path, 'r', encoding='utf-8') as f:
                    facade = json.load(f)
                facade_logic = facade.get("theory_category", {}).get("logic_type", "")
            except Exception as e:
                issues.append(f"facade.json 解析失败：{e}")
        else:
            issues.append("缺少 facade.json 配置文件")

        # 读取agent配置中的分型
        if os.path.exists(agent_path):
            try:
                with open(agent_path, 'r', encoding='utf-8') as f:
                    agent_cfg = json.load(f)
                agent_logic = agent_cfg.get("theory_binding", {}).get("logic_type", "")
            except Exception as e:
                issues.append(f"agent_config.json 解析失败：{e}")

        # 校验分型合法性
        facade_valid = facade_logic in self.VALID_LOGIC_TYPES
        agent_valid = agent_logic in self.VALID_LOGIC_TYPES
        consistent = facade_logic == agent_logic if facade_logic and agent_logic else True

        if not facade_valid:
            issues.append(f"facade中分型「{facade_logic}」不合法，应为：{'/'.join(self.VALID_LOGIC_TYPES)}")
        if not agent_valid:
            issues.append(f"agent中分型「{agent_logic}」不合法")
        if not consistent:
            issues.append(f"facade与agent分型不一致：{facade_logic} vs {agent_logic}")

        passed = len(issues) == 0 and facade_valid and consistent
        severity = "low" if issues else "none"

        result = {
            "layer": "layer3_logic_type",
            "passed": passed,
            "severity": severity,
            "facade_logic_type": facade_logic,
            "agent_logic_type": agent_logic,
            "consistent": consistent,
            "issues": issues,
            "message": "✅ 四论分型校验通过" if passed else f"⚠️  发现 {len(issues)} 个分型问题",
        }

        self._log(result["message"])
        self._log(f"   facade分型：{facade_logic or '未设置'}")
        self._log(f"   agent分型：{agent_logic or '未设置'}")
        self._log(f"   一致性：{'✅ 一致' if consistent else '❌ 不一致'}")
        for issue in issues:
            self._log(f"   ⚠️  {issue}")

        self.results["layer3"] = result
        return result

    # ========== 第四层：光谱稳态值评估 ==========

    def check_spectrum_value(self, subsystem_path: str, min_threshold: float = 0.4) -> Dict:
        """第四层：光谱稳态值评估"""
        self._log("=" * 60)
        self._log("📊 [第4层] 光谱稳态值评估")
        self._log("=" * 60)

        full_path = os.path.join(self.residential_path, subsystem_path)
        facade_path = os.path.join(full_path, "facade.json")
        agent_path = os.path.join(full_path, "agents/agent_config.json")

        facade_spectrum = None
        agent_spectrum = None

        if os.path.exists(facade_path):
            try:
                with open(facade_path, 'r', encoding='utf-8') as f:
                    facade = json.load(f)
                facade_spectrum = facade.get("theory_category", {}).get("spectrum_value")
            except Exception:
                pass

        if os.path.exists(agent_path):
            try:
                with open(agent_path, 'r', encoding='utf-8') as f:
                    agent_cfg = json.load(f)
                agent_spectrum = agent_cfg.get("theory_binding", {}).get("spectrum_value")
            except Exception:
                pass

        # 取有效值
        spectrum = facade_spectrum if facade_spectrum is not None else agent_spectrum

        if spectrum is None:
            passed = False
            severity = "medium"
            msg = "❌ 未设置光谱值，无法评估稳态等级"
        elif spectrum < min_threshold:
            passed = False
            severity = "medium"
            msg = f"⚠️  光谱值过低（{spectrum} < {min_threshold}），稳态不足"
        elif spectrum >= 0.6:
            passed = True
            severity = "none"
            msg = f"✅ 光谱值优良（{spectrum}），稳态等级：成熟级"
        elif spectrum >= 0.5:
            passed = True
            severity = "none"
            msg = f"✅ 光谱值达标（{spectrum}），稳态等级：成长级"
        else:
            passed = True
            severity = "low"
            msg = f"⚠️  光谱值偏低（{spectrum}），稳态等级：培育级"

        # 三维度评估（简化版：基于文件数量与分型估算）
        file_count = 0
        for _, _, files in os.walk(full_path):
            file_count += len(files)

        complexity_score = min(1.0, file_count / 20.0)
        diversity_score = 0.7 if facade_spectrum and facade_spectrum > 0.5 else 0.5
        symbiosis_score = 0.6  # 默认可与其他子系统共生

        result = {
            "layer": "layer4_spectrum",
            "passed": passed,
            "severity": severity,
            "spectrum_value": spectrum,
            "min_threshold": min_threshold,
            "three_dimensions": {
                "complexity": round(complexity_score, 3),
                "diversity": round(diversity_score, 3),
                "symbiosis": round(symbiosis_score, 3),
            },
            "stability_level": "成熟级" if spectrum and spectrum >= 0.6 else "成长级" if spectrum and spectrum >= 0.5 else "培育级",
            "message": msg,
        }

        self._log(msg)
        if spectrum is not None:
            self._log(f"   当前光谱值：{spectrum}")
            self._log(f"   三维评估：复杂度{complexity_score:.2f} | 多样性{diversity_score:.2f} | 共生性{symbiosis_score:.2f}")
            self._log(f"   稳态等级：{result['stability_level']}")

        self.results["layer4"] = result
        return result

    # ========== 第五层：盲区扫描与统计 ==========

    def scan_blindspots(self, subsystem_path: str) -> Dict:
        """第五层：盲区扫描与统计"""
        self._log("=" * 60)
        self._log("🔍 [第5层] 盲区扫描与统计")
        self._log("=" * 60)

        full_path = os.path.join(self.residential_path, subsystem_path)
        blindspots = []
        all_content = ""

        # 收集内容
        for root, dirs, files in os.walk(full_path):
            for file in files:
                if file.endswith(('.md', '.json', '.txt')):
                    fpath = os.path.join(root, file)
                    try:
                        with open(fpath, 'r', encoding='utf-8') as f:
                            all_content += f.read() + "\n"
                    except Exception:
                        pass

        # 盲区检测规则
        blindspot_patterns = [
            (r'TODO|待完成|待补充|待实现', "实现盲区", "medium"),
            (r'可能出现|存在风险|需注意|待验证', "验证盲区", "low"),
            (r'暂无|无相关|未涉及|未覆盖', "覆盖盲区", "medium"),
            (r'FIXME|BUG|问题|缺陷', "缺陷盲区", "high"),
        ]

        for pattern, btype, severity in blindspot_patterns:
            matches = re.findall(pattern, all_content)
            if matches:
                blindspots.append({
                    "type": btype,
                    "severity": severity,
                    "count": len(matches),
                    "pattern": pattern,
                })

        # 统计高危盲区数量
        high_risk = sum(b["count"] for b in blindspots if b["severity"] == "high")
        medium_risk = sum(b["count"] for b in blindspots if b["severity"] == "medium")
        low_risk = sum(b["count"] for b in blindspots if b["severity"] == "low")
        total = high_risk + medium_risk + low_risk

        passed = high_risk == 0
        if high_risk > 0:
            severity = "high"
            msg = f"❌ 发现 {high_risk} 个高危盲区！"
        elif total > 20:
            severity = "medium"
            msg = f"⚠️  盲区数量较多（共{total}个），建议排查"
        else:
            severity = "none" if total == 0 else "low"
            msg = f"✅ 盲区扫描完成，共发现 {total} 个盲区"

        result = {
            "layer": "layer5_blindspots",
            "passed": passed,
            "severity": severity,
            "total_blindspots": total,
            "high_risk": high_risk,
            "medium_risk": medium_risk,
            "low_risk": low_risk,
            "blindspot_details": blindspots,
            "message": msg,
        }

        self._log(msg)
        self._log(f"   高危：{high_risk} | 中危：{medium_risk} | 低危：{low_risk} | 总计：{total}")
        for b in blindspots:
            self._log(f"   - {b['type']}: {b['count']}个 ({b['severity']})")

        self.results["layer5"] = result
        return result

    # ========== 第六层：权限边界校验 ==========

    def check_permission_boundary(self, subsystem_path: str) -> Dict:
        """第六层：权限边界校验"""
        self._log("=" * 60)
        self._log("🛡️ [第6层] 权限边界校验")
        self._log("=" * 60)

        full_path = os.path.join(self.residential_path, subsystem_path)
        facade_path = os.path.join(full_path, "facade.json")

        issues = []

        if os.path.exists(facade_path):
            with open(facade_path, 'r', encoding='utf-8') as f:
                facade = json.load(f)

            # 检查modify_deny是否为True
            modify_deny = facade.get("core_access", {}).get("modify_deny", True)
            if not modify_deny:
                issues.append("核心修改权限未禁用，存在越权风险")

            # 检查边界模式
            boundary_mode = facade.get("boundary_mode", "")
            valid_modes = ["full_isolate", "protocol_restricted", "full_connect"]
            if boundary_mode not in valid_modes:
                issues.append(f"边界模式「{boundary_mode}」不合法")

            # 一级独栋必须有黑名单
            if "level1" in subsystem_path:
                blacklist = facade.get("cross_subsystem", {}).get("access_blacklist", [])
                if not blacklist:
                    issues.append("一级成熟独栋缺少二级孵化区访问黑名单")

        passed = len(issues) == 0
        severity = "medium" if not passed else "none"

        result = {
            "layer": "layer6_permission",
            "passed": passed,
            "severity": severity,
            "issues": issues,
            "message": "✅ 权限边界校验通过" if passed else f"⚠️  发现 {len(issues)} 个权限问题",
        }

        self._log(result["message"])
        for issue in issues:
            self._log(f"   ⚠️  {issue}")

        self.results["layer6"] = result
        return result

    # ========== 综合判定 ==========

    def assess_risk_level(self) -> Dict:
        """综合风险等级判定"""
        self._log("=" * 60)
        self._log("⚖️  [综合判定] 风险等级总评")
        self._log("=" * 60)

        high_count = sum(1 for r in self.results.values() if r.get("severity") == "high")
        medium_count = sum(1 for r in self.results.values() if r.get("severity") == "medium")
        critical_count = sum(1 for r in self.results.values() if r.get("severity") == "critical")

        if critical_count > 0:
            level = "critical"
            verdict = "❌ 不通过（母核异常）"
            action = "立即终止所有推演操作，排查母核篡改"
        elif high_count >= 3:
            level = "high"
            verdict = "❌ 不通过（高危）"
            action = "触发边界熔断，自动切换为full_isolate模式"
        elif high_count >= 1 or medium_count >= 5:
            level = "medium"
            verdict = "⚠️  待整改"
            action = "修复高危问题后可升级，中度问题限期整改"
        elif medium_count >= 1:
            level = "low"
            verdict = "✅ 基本通过"
            action = "可正常运行，低风险问题持续跟踪"
        else:
            level = "safe"
            verdict = "✅ 完全通过"
            action = "全维度合规，可直接升级/上岗"

        result = {
            "overall_risk": level,
            "verdict": verdict,
            "recommended_action": action,
            "high_issues": high_count,
            "medium_issues": medium_count,
            "critical_issues": critical_count,
            "total_layers_checked": len(self.results),
        }

        self._log(f"总评等级：{self.RISK_LEVELS[level]['label']}")
        self._log(f"判定结果：{verdict}")
        self._log(f"建议操作：{action}")
        self._log(f"高危/中危/致命：{high_count}/{medium_count}/{critical_count}")
        self._log(f"已校验层数：{len(self.results)}")

        self.results["overall"] = result
        return result

    # ========== 全量校验入口 ==========

    def check_compliance(self, subsystem_path: str, baseline_hash: str = None) -> Dict:
        """
        全维度合规校验（check_compliance 标准接口）
        :param subsystem_path: 子系统相对路径，如 level2_villa/xxx_孵化独栋
        :param baseline_hash: 母核基准哈希，默认使用内置值
        :return: 完整校验结果字典
        """
        self.results = {}
        self._log_msg = []

        self._log("")
        self._log("╔══════════════════════════════════════════════════════════╗")
        self._log("║      🛡️  全域智能体合规校验引擎 v1.0                       ║")
        self._log("║         check_compliance 全维度质检                        ║")
        self._log("╚══════════════════════════════════════════════════════════╝")
        self._log(f"校验对象：{subsystem_path}")
        self._log(f"校验时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._log("")

        # 第一层：母核哈希（全局）
        r1 = self.check_core_hash(baseline_hash)
        if not r1["passed"]:
            # 母核异常，直接终止
            self._log("")
            self._log("🚨 母核哈希校验失败，后续校验终止！")
            self.results["overall"] = {
                "overall_risk": "critical",
                "verdict": "❌ 不通过（母核异常）",
                "recommended_action": "立即终止所有操作，排查母核篡改",
            }
            return self.results

        # 第二-六层：子系统维度
        self.check_axiom_compatibility(subsystem_path)
        self.check_logic_type(subsystem_path)
        self.check_spectrum_value(subsystem_path)
        self.scan_blindspots(subsystem_path)
        self.check_permission_boundary(subsystem_path)

        # 综合判定
        self.assess_risk_level()

        self._log("")
        self._log("=" * 60)
        self._log("✅ 全维度合规校验完成")
        self._log("=" * 60)

        return self.results

    def get_report_text(self) -> str:
        """获取纯文本报告"""
        return "\n".join(self._log_msg)

    def check_agent(self, agent_rel_path: str) -> Dict:
        """单智能体合规校验（别名方法）"""
        return self.check_compliance(agent_rel_path)

    def batch_check(self, agent_list: List[str]) -> Dict:
        """批量合规校验"""
        total = len(agent_list)
        passed = 0
        failed = 0
        results = []

        for agent_path in agent_list:
            try:
                result = self.check_compliance(agent_path)
                if result.get("risk_level") in ["low", "medium"]:
                    passed += 1
                else:
                    failed += 1
                results.append({"agent": agent_path, "result": result})
            except Exception as e:
                failed += 1
                results.append({"agent": agent_path, "error": str(e)})

        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "results": results,
        }

    def get_compliance_overview(self) -> Dict:
        """合规总览统计"""
        total_agents = 0
        total_checked = 0
        risk_distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        if os.path.exists(self.residential_path):
            for root, dirs, files in os.walk(self.residential_path):
                if "facade.json" in files and "_template" not in root and "_archive" not in root:
                    total_agents += 1

        return {
            "total_agents": total_agents,
            "total_checked": total_checked,
            "risk_distribution": risk_distribution,
            "check_layers": 6,
            "compliance_rate": 0.0,
        }


# ========== 命令行入口 ==========

if __name__ == "__main__":
    import sys

    checker = ComplianceChecker()

    if len(sys.argv) < 2:
        print("用法: python compliance_check.py <子系统相对路径>")
        print("示例: python compliance_check.py level2_villa/测试_孵化独栋")
        sys.exit(1)

    subsystem = sys.argv[1]
    result = checker.check_compliance(subsystem)
