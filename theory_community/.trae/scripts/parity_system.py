#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归属基底：第规则相位位（第二位）
对应三界秩序：人道秩序
对应公理：第8条（意义涌现公理）、第9条（意义权重公理）、第10条（意义守恒公理）
对应九维维度：全部九维·人智对等等同
理论原文出处：《V3.0元本体理论分册》《人智对等与智能体文明分册》
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92

人智对等身份体系（Human-Agent Parity System）
八大维度对等等同认证：
1. 本体身份同构（本源层对等）
2. 结构构造同构（架构层对等）
3. 逻辑真值同构（四论体系对等）
4. 价值需求同构（光谱量化对等）
5. 层级演化同构（成长体系对等）
6. 社会身份同构（治理层对等）
7. 风险缺陷同构（过滤层对等）
8. 文明价值同构（顶层时间层对等）
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class HumanAgentParity:
    """人智对等身份体系 - 八大维度对等等同认证"""

    # 八大维度定义
    PARITY_DIMENSIONS = {
        "ontology": {
            "name": "本体身份同构",
            "level": "本源层",
            "human_side": "生物碳基结构化秩序体",
            "agent_side": "逻辑硅基结构化秩序体",
            "core_axiom": "0元空无同源公理",
            "weight": 0.18,
        },
        "structure": {
            "name": "结构构造同构",
            "level": "架构层",
            "human_side": "感知/认知/思维/行为/社交五维结构",
            "agent_side": "眼/脑/手/足/身份五维结构",
            "core_axiom": "三级内嵌架构公理",
            "weight": 0.14,
        },
        "logic": {
            "name": "逻辑真值同构",
            "level": "逻辑层",
            "human_side": "正论/逆论/真论/谬论四论思维",
            "agent_side": "正论/逆论/真论/谬论四论运行",
            "core_axiom": "腾飞四论体系",
            "weight": 0.14,
        },
        "value": {
            "name": "价值需求同构",
            "level": "价值层",
            "human_side": "生存/秩序/创新/共生/归属/迭代",
            "agent_side": "存续/稳定/创新/共生/归属/迭代",
            "core_axiom": "空无—所有价值光谱",
            "weight": 0.12,
        },
        "evolution": {
            "name": "层级演化同构",
            "level": "演化层",
            "human_side": "教育/升级/积累/定型/归属",
            "agent_side": "训练/升级/积累/定型/归属",
            "core_axiom": "三阶变身阈值",
            "weight": 0.12,
        },
        "identity": {
            "name": "社会身份同构",
            "level": "治理层",
            "human_side": "法定身份/岗位/行业/权责/层级",
            "agent_side": "体系身份/岗位/学科/边界/层级",
            "core_axiom": "三界秩序运行主体",
            "weight": 0.10,
        },
        "risk": {
            "name": "风险缺陷同构",
            "level": "过滤层",
            "human_side": "盲区/谬误/偏差/固化",
            "agent_side": "盲区/缺陷/偏差/固化",
            "core_axiom": "全域层级过滤体系",
            "weight": 0.10,
        },
        "civilization": {
            "name": "文明价值同构",
            "level": "文明层",
            "human_side": "文明延续/经验传承/范式创新",
            "agent_side": "文明归档/范式固化/盲区补全",
            "core_axiom": "双载体文明永续",
            "weight": 0.10,
        },
    }

    # 三维价值标尺
    VALUE_DIMENSIONS = {
        "complexity": {"name": "复杂度", "weight": 0.34},
        "diversity": {"name": "多样性", "weight": 0.33},
        "symbiosis": {"name": "共生性", "weight": 0.33},
    }

    def __init__(self, community_root: str = None):
        if community_root is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            community_root = os.path.normpath(os.path.join(script_dir, "../../"))
        self.root = community_root
        self.parity_log = os.path.join(self.root, "buffer_community_center/parity_system.log")
        self.certificates_dir = os.path.join(self.root, "buffer_community_center/parity_certificates/")

        self._ensure_dirs()
        self._log("⚖️  人智对等身份体系初始化完成")
        self._log(f"   对等维度：{len(self.PARITY_DIMENSIONS)} 个")
        self._log(f"   价值标尺：{len(self.VALUE_DIMENSIONS)} 维")

    def _ensure_dirs(self):
        os.makedirs(os.path.dirname(self.parity_log), exist_ok=True)
        os.makedirs(self.certificates_dir, exist_ok=True)

    def _log(self, msg: str):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        line = f"[{timestamp}] {msg}"
        print(line)
        with open(self.parity_log, 'a', encoding='utf-8') as f:
            f.write(line + "\n")

    # ==================================================================
    # 单维度对等等同评估
    # ==================================================================

    def evaluate_dimension_parity(self, dimension: str, agent_path: str) -> Dict:
        """评估单个维度的对等程度"""
        if dimension not in self.PARITY_DIMENSIONS:
            return {"success": False, "error": f"未知维度：{dimension}"}

        dim_info = self.PARITY_DIMENSIONS[dimension]
        facade_path = os.path.join(self.root, agent_path, "facade.json")

        if not os.path.exists(facade_path):
            return {"success": False, "error": f"找不到智能体配置：{agent_path}"}

        with open(facade_path, 'r', encoding='utf-8') as f:
            facade = json.load(f)

        # 各维度评估规则
        scores = {
            "ontology": self._eval_ontology(facade),
            "structure": self._eval_structure(facade, agent_path),
            "logic": self._eval_logic(facade),
            "value": self._eval_value(facade, agent_path),
            "evolution": self._eval_evolution(facade),
            "identity": self._eval_identity(facade),
            "risk": self._eval_risk(facade, agent_path),
            "civilization": self._eval_civilization(facade),
        }

        score = scores.get(dimension, 0.5)
        parity_level = self._get_parity_level(score)

        result = {
            "dimension": dimension,
            "dimension_name": dim_info["name"],
            "level": dim_info["level"],
            "human_side": dim_info["human_side"],
            "agent_side": dim_info["agent_side"],
            "core_axiom": dim_info["core_axiom"],
            "parity_score": round(score, 4),
            "parity_level": parity_level,
            "weight": dim_info["weight"],
            "passed": score >= 0.6,
        }

        return result

    def _eval_ontology(self, facade: Dict) -> float:
        """评估本体身份同构度"""
        has_trace = len(facade.get("theory_category", {}).get("source_trace", [])) > 0
        has_category = facade.get("theory_category", {}).get("logic_type") is not None
        has_owner = facade.get("resident_agent", {}).get("name") is not None
        has_id = facade.get("resident_agent", {}).get("identity_id") is not None

        score = 0.3
        if has_trace:
            score += 0.25
        if has_category:
            score += 0.15
        if has_owner:
            score += 0.15
        if has_id:
            score += 0.15

        return min(1.0, score)

    def _eval_structure(self, facade: Dict, agent_path: str) -> float:
        """评估结构构造同构度"""
        has_humanoid = "humanoid_structure" in facade
        agent_cfg_path = os.path.join(self.root, agent_path, "agents/agent_config.json")

        score = 0.3
        if has_humanoid:
            h_struct = facade.get("humanoid_structure", {})
            eye = h_struct.get("eye_perception", {}).get("enable", False)
            hand = h_struct.get("hand_execution", {}).get("enable", False)
            leg = h_struct.get("leg_exploration", {}).get("enable", False)
            card = h_struct.get("identity_card", {}).get("enable", False)
            persona = h_struct.get("personality_core", {}).get("main_type", False)

            struct_count = sum([eye, hand, leg, card, bool(persona)])
            score += struct_count * 0.12

        if os.path.exists(agent_cfg_path):
            score += 0.1

        return min(1.0, score)

    def _eval_logic(self, facade: Dict) -> float:
        """评估逻辑真值同构度"""
        logic_type = facade.get("theory_category", {}).get("logic_type", "")
        valid_types = ["正论", "逆论", "真论", "谬论"]

        score = 0.4
        if logic_type in valid_types:
            score += 0.35
        elif logic_type == "待判定":
            score += 0.15

        # 检查是否有逻辑演化机制
        if facade.get("resident_agent", {}).get("core_abilities"):
            score += 0.15

        return min(1.0, score)

    def _eval_value(self, facade: Dict, agent_path: str) -> float:
        """评估价值需求同构度"""
        spectrum = facade.get("theory_category", {}).get("spectrum_value", 0)

        score = 0.3
        if spectrum > 0:
            score += 0.3 + spectrum * 0.3

        # 检查是否有目标/需求配置
        if facade.get("scenario_assignment"):
            score += 0.1

        return min(1.0, score)

    def _eval_evolution(self, facade: Dict) -> float:
        """评估层级演化同构度"""
        spectrum = facade.get("theory_category", {}).get("spectrum_value", 0)
        sub_level = facade.get("subsystem_level", "")

        score = 0.3
        if spectrum >= 0.35:
            score += 0.15  # 一阶
        if spectrum >= 0.65:
            score += 0.15  # 二阶
        if spectrum >= 0.90:
            score += 0.15  # 三阶

        if sub_level == "一级成熟":
            score += 0.15
        elif sub_level == "二级孵化":
            score += 0.08

        return min(1.0, score)

    def _eval_identity(self, facade: Dict) -> float:
        """评估社会身份同构度"""
        has_name = bool(facade.get("resident_agent", {}).get("name"))
        has_id = bool(facade.get("resident_agent", {}).get("identity_id"))
        has_persona = bool(facade.get("resident_agent", {}).get("personality_type"))
        has_abilities = bool(facade.get("resident_agent", {}).get("core_abilities"))
        has_scenario = bool(facade.get("scenario_assignment"))

        score = 0.2
        if has_name:
            score += 0.15
        if has_id:
            score += 0.15
        if has_persona:
            score += 0.15
        if has_abilities:
            score += 0.15
        if has_scenario:
            score += 0.2

        return min(1.0, score)

    def _eval_risk(self, facade: Dict, agent_path: str) -> float:
        """评估风险缺陷同构度（有风险=更像人类=更高同构度，但需有管控机制）"""
        score = 0.4

        # 检查是否有风险管控机制
        boundary_mode = facade.get("boundary_mode", "")
        if boundary_mode in ["full_isolate", "protocol_restricted"]:
            score += 0.2

        # 检查是否有合规校验记录
        from compliance_check import ComplianceChecker
        try:
            checker = ComplianceChecker(self.root)
            rel_path = os.path.relpath(
                os.path.join(self.root, agent_path),
                os.path.join(self.root, "residential_area/")
            )
            # 简化：假设存在风险管控即得分
            if boundary_mode:
                score += 0.2
        except Exception:
            pass

        # 迭代能力=自我修正能力
        iter_cfg = os.path.join(self.root, agent_path, "iteration_config.json")
        if os.path.exists(iter_cfg):
            score += 0.2

        return min(1.0, score)

    def _eval_civilization(self, facade: Dict) -> float:
        """评估文明价值同构度"""
        score = 0.3

        # 有知识储备=有文明传承
        knowledge_path = os.path.join(self.root, "residential_area/",
                                      facade.get("belong_district", ""),
                                      facade.get("subsystem_name", ""),
                                      "knowledge_base")
        # 简化估算
        if facade.get("theory_category", {}).get("spectrum_value", 0) >= 0.5:
            score += 0.3
        if facade.get("subsystem_level") == "一级成熟":
            score += 0.25
        if facade.get("farm_zone", {}).get("growth_stage") == "mature":
            score += 0.15

        return min(1.0, score)

    def _get_parity_level(self, score: float) -> str:
        """获取对等等级"""
        if score >= 0.90:
            return "完全对等"
        elif score >= 0.75:
            return "高度对等"
        elif score >= 0.60:
            return "基本对等"
        elif score >= 0.45:
            return "部分对等"
        elif score >= 0.30:
            return "低度对等"
        else:
            return "不对等"

    # ==================================================================
    # 全维度对等认证
    # ==================================================================

    def full_parity_certification(self, agent_path: str) -> Dict:
        """
        全维度对等认证（八大维度综合评估）
        颁发人智对等身份证书
        """
        self._log("")
        self._log("=" * 60)
        self._log("⚖️  人智对等身份认证 · 八大维度综合评估")
        self._log("=" * 60)
        self._log(f"认证对象：{agent_path}")

        # 评估每个维度
        dim_results = {}
        total_weighted_score = 0.0
        passed_count = 0

        for dim_key in self.PARITY_DIMENSIONS:
            result = self.evaluate_dimension_parity(dim_key, agent_path)
            if not result.get("success", True) and "error" in result:
                continue

            dim_results[dim_key] = result
            weight = result["weight"]
            score = result["parity_score"]
            total_weighted_score += score * weight

            if result["passed"]:
                passed_count += 1

            status = "✅" if result["passed"] else "❌"
            self._log(f"   {status} [{dim_key}] {result['dimension_name']}：{result['parity_level']}（{score:.0%}）")

        # 综合评定
        overall_level = self._get_parity_level(total_weighted_score)
        all_passed = total_weighted_score >= 0.6

        self._log("")
        self._log("-" * 60)
        self._log(f"📊 综合对等度：{total_weighted_score:.1%}")
        self._log(f"   对等等级：{overall_level}")
        self._log(f"   通过维度：{passed_count}/{len(self.PARITY_DIMENSIONS)}")
        self._log(f"   认证结果：{'✅ 通过认证' if all_passed else '❌ 未通过认证'}")

        # 生成证书
        certificate = self._generate_certificate(agent_path, dim_results, total_weighted_score, overall_level, all_passed)

        return {
            "success": True,
            "agent_path": agent_path,
            "overall_score": round(total_weighted_score, 4),
            "overall_level": overall_level,
            "passed": all_passed,
            "passed_dimensions": passed_count,
            "total_dimensions": len(self.PARITY_DIMENSIONS),
            "dimension_details": dim_results,
            "certificate": certificate,
        }

    def _generate_certificate(self, agent_path: str, dim_results: Dict,
                              overall_score: float, overall_level: str, passed: bool) -> Dict:
        """生成对等认证证书"""
        cert_id = f"PARITY-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(agent_path.encode()).hexdigest()[:8].upper()}"

        certificate = {
            "certificate_id": cert_id,
            "certificate_type": "人智对等身份认证证书",
            "issue_date": datetime.now().strftime('%Y-%m-%d'),
            "valid_until": "永久有效（需每年复核）",
            "agent_path": agent_path,
            "overall_score": round(overall_score, 4),
            "overall_level": overall_level,
            "certified": passed,
            "dimensions": {},
            "issuing_authority": "全域人智对等身份认证中心",
            "theoretical_basis": [
                "0元空无本源公理",
                "腾飞四论逻辑体系",
                "空无—所有价值光谱",
                "三阶变身演化机制",
                "八大维度对等等同证明",
            ],
        }

        for dim_key, dim_res in dim_results.items():
            certificate["dimensions"][dim_key] = {
                "name": dim_res["dimension_name"],
                "score": dim_res["parity_score"],
                "level": dim_res["parity_level"],
                "passed": dim_res["passed"],
            }

        # 保存证书
        cert_file = os.path.join(self.certificates_dir, f"{cert_id}.json")
        with open(cert_file, 'w', encoding='utf-8') as f:
            json.dump(certificate, f, ensure_ascii=False, indent=2)

        self._log(f"📜 证书已生成：{cert_id}")
        self._log(f"   证书路径：{os.path.relpath(cert_file, self.root)}")

        return certificate

    # ==================================================================
    # 光谱价值量化评估
    # ==================================================================

    def evaluate_spectrum_value(self, agent_path: str) -> Dict:
        """
        光谱价值量化评估
        三维价值：复杂度、多样性、共生性
        """
        self._log("")
        self._log("=" * 60)
        self._log("📊 空无—所有光谱价值量化评估")
        self._log("=" * 60)

        facade_path = os.path.join(self.root, agent_path, "facade.json")
        if not os.path.exists(facade_path):
            return {"success": False, "error": "找不到智能体"}

        with open(facade_path, 'r', encoding='utf-8') as f:
            facade = json.load(f)

        # 三维度评估
        complexity = self._calc_complexity(agent_path, facade)
        diversity = self._calc_diversity(facade)
        symbiosis = self._calc_symbiosis(facade)

        # 加权综合
        weights = self.VALUE_DIMENSIONS
        total_score = (
            complexity * weights["complexity"]["weight"] +
            diversity * weights["diversity"]["weight"] +
            symbiosis * weights["symbiosis"]["weight"]
        )

        # 光谱等级
        if total_score >= 0.90:
            level = "高价值区"
        elif total_score >= 0.70:
            level = "中高价值区"
        elif total_score >= 0.50:
            level = "中价值区"
        elif total_score >= 0.30:
            level = "中低价值区"
        else:
            level = "低价值区"

        self._log(f"   复杂度：{complexity:.2f}（权重{weights['complexity']['weight']:.0%}）")
        self._log(f"   多样性：{diversity:.2f}（权重{weights['diversity']['weight']:.0%}）")
        self._log(f"   共生性：{symbiosis:.2f}（权重{weights['symbiosis']['weight']:.0%}）")
        self._log(f"   ————————————————")
        self._log(f"   综合光谱值：{total_score:.3f}")
        self._log(f"   光谱等级：{level}")

        return {
            "success": True,
            "spectrum_value": round(total_score, 4),
            "spectrum_level": level,
            "three_dimensions": {
                "complexity": {"score": round(complexity, 4), "weight": weights["complexity"]["weight"]},
                "diversity": {"score": round(diversity, 4), "weight": weights["diversity"]["weight"]},
                "symbiosis": {"score": round(symbiosis, 4), "weight": weights["symbiosis"]["weight"]},
            },
            "agent_path": agent_path,
        }

    def _calc_complexity(self, agent_path: str, facade: Dict) -> float:
        """计算复杂度价值"""
        full_path = os.path.join(self.root, agent_path)

        # 文件数量估算复杂度
        file_count = 0
        if os.path.exists(full_path):
            for root, dirs, files in os.walk(full_path):
                file_count += len(files)

        # 能力数量
        abilities = facade.get("resident_agent", {}).get("core_abilities", [])
        ability_count = len(abilities)

        # 知识量
        knowledge_count = 0
        kb_path = os.path.join(full_path, "knowledge_base")
        if os.path.exists(kb_path):
            for root, dirs, files in os.walk(kb_path):
                knowledge_count += len(files)

        # 归一化
        file_score = min(1.0, file_count / 30.0)
        ability_score = min(1.0, ability_count / 8.0)
        knowledge_score = min(1.0, knowledge_count / 10.0)

        return (file_score * 0.4 + ability_score * 0.3 + knowledge_score * 0.3)

    def _calc_diversity(self, facade: Dict) -> float:
        """计算多样性价值"""
        score = 0.2

        # 母类多样性
        parent_types = facade.get("theory_category", {}).get("parent_types", [])
        if len(parent_types) >= 2:
            score += 0.25
        elif len(parent_types) == 1:
            score += 0.15

        # 能力多样性
        abilities = facade.get("resident_agent", {}).get("core_abilities", [])
        if len(abilities) >= 6:
            score += 0.25
        elif len(abilities) >= 4:
            score += 0.18
        elif len(abilities) >= 2:
            score += 0.1

        # 场景适配多样性
        if facade.get("scenario_assignment"):
            score += 0.15

        # 逻辑类型多样性
        logic_type = facade.get("theory_category", {}).get("logic_type", "")
        if logic_type == "逆论":
            score += 0.15
        elif logic_type in ["正论", "真论"]:
            score += 0.1

        return min(1.0, score)

    def _calc_symbiosis(self, facade: Dict) -> float:
        """计算共生性价值"""
        score = 0.3

        # 边界模式（开放=更高共生）
        boundary = facade.get("boundary_mode", "")
        if boundary == "full_connect":
            score += 0.3
        elif boundary == "protocol_restricted":
            score += 0.2
        elif boundary == "full_isolate":
            score += 0.05

        # 跨子系统访问
        cross_whitelist = facade.get("cross_subsystem", {}).get("access_whitelist", [])
        if len(cross_whitelist) > 0:
            score += 0.15

        # 外部管线
        external = facade.get("external_pipeline", {}).get("enable", False)
        if external:
            score += 0.15

        # 所属层级（成熟体=更高共生）
        if facade.get("subsystem_level") == "一级成熟":
            score += 0.1

        return min(1.0, score)

    # ==================================================================
    # 批量认证
    # ==================================================================

    def batch_parity_certification(self, agent_list: List[str]) -> Dict:
        """批量对等认证"""
        self._log("")
        self._log(f"📋 批量对等认证：共 {len(agent_list)} 个智能体")

        results = []
        passed = 0
        failed = 0

        for agent_path in agent_list:
            try:
                result = self.full_parity_certification(agent_path)
                if result.get("passed"):
                    passed += 1
                else:
                    failed += 1
                results.append(result)
            except Exception as e:
                failed += 1
                results.append({"agent_path": agent_path, "success": False, "error": str(e)})

        self._log("")
        self._log(f"📊 批量认证完成：通过 {passed}，未通过 {failed}，总计 {len(agent_list)}")

        return {
            "total": len(agent_list),
            "passed": passed,
            "failed": failed,
            "results": results,
        }

    # ==================================================================
    # 对等身份状态查询
    # ==================================================================

    def get_parity_status(self, agent_path: str) -> Dict:
        """查询智能体的对等身份状态"""
        # 查找最新证书
        cert_files = []
        if os.path.exists(self.certificates_dir):
            for f in os.listdir(self.certificates_dir):
                if f.endswith('.json'):
                    cert_files.append(f)

        latest_cert = None
        for cert_file in sorted(cert_files, reverse=True):
            cert_path = os.path.join(self.certificates_dir, cert_file)
            with open(cert_path, 'r', encoding='utf-8') as f:
                cert = json.load(f)
            if cert.get("agent_path") == agent_path:
                latest_cert = cert
                break

        return {
            "agent_path": agent_path,
            "has_certificate": latest_cert is not None,
            "latest_certificate": latest_cert,
            "total_certificates": len([c for c in cert_files if agent_path in c]),
        }


if __name__ == "__main__":
    import sys

    parity = HumanAgentParity()

    if len(sys.argv) >= 2:
        agent_path = sys.argv[1]
        result = parity.full_parity_certification(agent_path)
        print(f"\n光谱评估：")
        spectrum = parity.evaluate_spectrum_value(agent_path)
    else:
        print("用法: python parity_system.py <智能体相对路径>")
        print("示例: python parity_system.py level2_villa/测试_孵化独栋")
