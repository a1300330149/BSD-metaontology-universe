"""
BSD全域统一理论 — 验证类MCP工具

归属基底：第0重元道本源基底
对应公理：全域公理参数源
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/

确权信息：
    作者：杨腾飞
    证件：433127199812193215
    哈希：e62f918340dc2975108294736ac8927d90584136972485931027958740925713
    锁档日期：2026-06-20
    三维确权：杨腾飞60%｜墨心25%｜豆包15%
"""

from typing import Any, Dict, List, Optional

from bsd_mcp.tool_registry import register_tool


MILLENNIUM_PROBLEMS = [
    {"id": "p_vs_np", "name": "P vs NP问题", "module": "bsd_verify.millennium.verifier_p_vs_np", "class": "PvsNPVerifier"},
    {"id": "navier_stokes", "name": "纳维-斯托克斯方程", "module": "bsd_verify.millennium.verifier_navier_stokes", "class": "NavierStokesVerifier"},
    {"id": "riemann", "name": "黎曼假设", "module": "bsd_verify.millennium.verifier_riemann", "class": "RiemannVerifier"},
    {"id": "yang_mills", "name": "杨-米尔斯存在性与质量间隙", "module": "bsd_verify.millennium.verifier_yang_mills", "class": "YangMillsVerifier"},
    {"id": "hodge", "name": "霍奇猜想", "module": "bsd_verify.millennium.verifier_hodge", "class": "HodgeVerifier"},
    {"id": "bsd_conjecture", "name": "BSD猜想", "module": "bsd_verify.millennium.verifier_bsd_conjecture", "class": "BSDConjectureVerifier"},
    {"id": "poincare", "name": "庞加莱猜想", "module": "bsd_verify.millennium.verifier_poincare", "class": "PoincareVerifier"},
    {"id": "beal", "name": "Beal猜想", "module": "bsd_verify.millennium.verifier_beal", "class": "BealVerifier"},
]


def bsd_verify_millennium(
    problem: str = "all",
    detail_level: str = "summary",
) -> Dict[str, Any]:
    try:
        problems_to_verify = []
        if problem == "all":
            problems_to_verify = MILLENNIUM_PROBLEMS
        else:
            prob = next((p for p in MILLENNIUM_PROBLEMS if p["id"] == problem), None)
            if prob is None:
                return {
                    "success": False,
                    "data": None,
                    "error": f"未知的问题标识: {problem}，可用问题: {[p['id'] for p in MILLENNIUM_PROBLEMS]}",
                }
            problems_to_verify = [prob]

        results = []
        for prob in problems_to_verify:
            try:
                module = __import__(prob["module"], fromlist=[prob["class"]])
                verifier_class = getattr(module, prob["class"])
                verifier = verifier_class()
                result = verifier.verify()

                result_dict = {
                    "problem": prob["id"],
                    "problem_name": prob["name"],
                    "verdict": result.verdict,
                    "confidence": result.confidence,
                    "verification_time": result.verification_time,
                    "key_equation": result.key_equation,
                    "proof_chain_length": len(result.proof_chain),
                    "numerical_evidence": result.numerical_evidence,
                    "error": result.error_message if result.verdict == "error" else "",
                }

                if detail_level == "detailed":
                    result_dict["proof_chain"] = result.proof_chain
                    result_dict["full_details"] = getattr(result, "details", {})

                results.append(result_dict)
            except Exception as e:
                results.append({
                    "problem": prob["id"],
                    "problem_name": prob["name"],
                    "verdict": "error",
                    "confidence": 0.0,
                    "error": str(e),
                })

        all_passed = all(r["verdict"] in ("proven", "verified", "confirmed") for r in results)

        return {
            "success": True,
            "data": {
                "problem": problem,
                "detail_level": detail_level,
                "total": len(results),
                "all_passed": all_passed,
                "results": results,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_verify_hash(
    target: str = "core_params",
) -> Dict[str, Any]:
    try:
        results = {}

        from bsd_engine.validators.hash_checker import verify_core_params, verify_theory_base

        if target in ("core_params", "all"):
            params_ok, params_errors = verify_core_params()
            results["core_params"] = {
                "passed": params_ok,
                "errors": params_errors,
                "total_params": 12,
            }

        if target in ("theory_base", "all"):
            passed, missing, modified, stats = verify_theory_base()
            results["theory_base"] = {
                "passed": passed,
                "missing_files": missing,
                "modified_files": modified,
                "stats": stats,
            }

        overall = all(v.get("passed", False) for v in results.values())
        results["overall_pass"] = overall

        return {
            "success": True,
            "data": {
                "target": target,
                "verified": overall,
                "details": results,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_verify_compliance(
    target: str = "axioms",
) -> Dict[str, Any]:
    try:
        from bsd_engine.validators.compliance_checker import (
            check_axiom_completeness,
            check_equation_completeness,
            check_registry_compliance,
        )

        results = {}

        if target in ("axioms", "all"):
            axiom_ok, axiom_stats = check_axiom_completeness()
            results["axioms"] = {
                "passed": axiom_ok,
                "stats": axiom_stats,
            }

        if target in ("equations", "all"):
            eq_ok, eq_stats = check_equation_completeness()
            results["equations"] = {
                "passed": eq_ok,
                "stats": eq_stats,
            }

        if target in ("registry", "all"):
            reg_ok, reg_stats = check_registry_compliance()
            results["registry"] = {
                "passed": reg_ok,
                "stats": reg_stats,
            }

        overall = all(v.get("passed", False) for v in results.values())
        results["overall_pass"] = overall

        return {
            "success": True,
            "data": {
                "target": target,
                "compliant": overall,
                "details": results,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_verify_binding(
    target: str = "coverage",
) -> Dict[str, Any]:
    try:
        from bsd_engine.validators.binding_checker import (
            scan_all_source_files,
            verify_theory_references,
            check_bsd_annotation_coverage,
        )

        results = {}

        if target in ("annotations", "all"):
            headers = scan_all_source_files()
            results["annotations"] = {
                "annotated_files": len(headers),
                "files": list(headers.keys()),
            }

        if target in ("references", "all"):
            ref_ok, valid_count, invalid = verify_theory_references()
            results["references"] = {
                "passed": ref_ok,
                "valid_count": valid_count,
                "invalid_references": [
                    {"file": fp, "reference": ref} for fp, ref in invalid
                ],
            }

        if target in ("coverage", "all"):
            coverage, annotated, total = check_bsd_annotation_coverage()
            results["coverage"] = {
                "coverage_percent": round(coverage * 100, 2),
                "annotated_files": annotated,
                "total_files": total,
                "passed": coverage >= 0.8,
            }

        overall = all(
            v.get("passed", True)
            for k, v in results.items()
            if k != "annotations"
        )
        results["overall_pass"] = overall

        return {
            "success": True,
            "data": {
                "target": target,
                "binding_valid": overall,
                "details": results,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_full_validation(
    quick_mode: bool = True,
) -> Dict[str, Any]:
    stages = {}
    stage_passed = {}

    try:
        from bsd_engine.validators.compliance_checker import (
            check_axiom_completeness,
            check_equation_completeness,
            check_registry_compliance,
        )
        from bsd_engine.validators.hash_checker import verify_core_params

        print("[1/6] 公理层验证...")
        axiom_ok, axiom_stats = check_axiom_completeness()
        stages["axioms"] = {"passed": axiom_ok, "stats": axiom_stats}
        stage_passed["axioms"] = axiom_ok

        print("[2/6] 参数哈希验证...")
        params_ok, params_errors = verify_core_params()
        stages["params_hash"] = {"passed": params_ok, "errors": params_errors}
        stage_passed["params_hash"] = params_ok

        print("[3/6] 方程层验证...")
        eq_ok, eq_stats = check_equation_completeness()
        stages["equations"] = {"passed": eq_ok, "stats": eq_stats}
        stage_passed["equations"] = eq_ok

        print("[4/6] 注册合规性验证...")
        reg_ok, reg_stats = check_registry_compliance()
        stages["registry"] = {"passed": reg_ok, "stats": reg_stats}
        stage_passed["registry"] = reg_ok

        if not quick_mode:
            print("[5/6] 仿真层可用性验证...")
            sim_ok = True
            sim_details = {}
            try:
                from bsd_mcp.tools.simulation_tools import SIMULATION_LIST
                sim_count = len(SIMULATION_LIST)
                sim_details["simulator_count"] = sim_count
                sim_details["simulators"] = [s["id"] for s in SIMULATION_LIST]
                sim_ok = sim_count >= 8
            except Exception as e:
                sim_details["error"] = str(e)
                sim_ok = False
            stages["simulation"] = {"passed": sim_ok, "details": sim_details}
            stage_passed["simulation"] = sim_ok

            print("[6/6] Agent层可用性验证...")
            agent_ok = True
            agent_details = {}
            try:
                from bsd_agents.base import BaseAgent
                agent_details["base_agent_available"] = True
                agent_list = [
                    "application_agent",
                    "cross_validation_agent",
                    "meta_ontology_agent",
                    "millennium_agent",
                    "theory_evolution_agent",
                ]
                available_agents = []
                for agent_name in agent_list:
                    try:
                        mod = __import__(f"bsd_agents.{agent_name}", fromlist=[""])
                        available_agents.append(agent_name)
                    except Exception:
                        pass
                agent_details["available_agents"] = available_agents
                agent_details["agent_count"] = len(available_agents)
                agent_ok = len(available_agents) >= 3
            except Exception as e:
                agent_details["error"] = str(e)
                agent_ok = False
            stages["agents"] = {"passed": agent_ok, "details": agent_details}
            stage_passed["agents"] = agent_ok
        else:
            stages["simulation"] = {"passed": True, "skipped": True, "message": "快速模式下跳过仿真层验证"}
            stages["agents"] = {"passed": True, "skipped": True, "message": "快速模式下跳过Agent层验证"}
            stage_passed["simulation"] = True
            stage_passed["agents"] = True

        total_stages = len(stage_passed)
        passed_stages = sum(1 for v in stage_passed.values() if v)
        overall = passed_stages == total_stages

        return {
            "success": True,
            "data": {
                "quick_mode": quick_mode,
                "validation_complete": True,
                "overall_pass": overall,
                "total_stages": total_stages,
                "passed_stages": passed_stages,
                "pass_rate": round(passed_stages / total_stages * 100, 2) if total_stages > 0 else 0,
                "stages": stages,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


register_tool(
    name="bsd_verify_millennium",
    description="验证千禧年难题（支持单个问题或全部验证）",
    input_schema={
        "type": "object",
        "properties": {
            "problem": {
                "type": "string",
                "description": "问题标识：p_vs_np/navier_stokes/riemann/yang_mills/hodge/bsd_conjecture/poincare/beal/all",
                "default": "all",
            },
            "detail_level": {
                "type": "string",
                "description": "详细程度：summary/detailed",
                "default": "summary",
            },
        },
        "required": [],
    },
    handler=bsd_verify_millennium,
)

register_tool(
    name="bsd_verify_hash",
    description="校验理论库SHA256哈希完整性",
    input_schema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "校验目标：core_params/theory_base/all",
                "default": "core_params",
            }
        },
        "required": [],
    },
    handler=bsd_verify_hash,
)

register_tool(
    name="bsd_verify_compliance",
    description="验证代码/文档是否符合BSD公理合规性",
    input_schema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "检查目标：axioms/equations/registry/all",
                "default": "axioms",
            }
        },
        "required": [],
    },
    handler=bsd_verify_compliance,
)

register_tool(
    name="bsd_verify_binding",
    description="验证理论-代码绑定关系（理论锚对应代码锚）",
    input_schema={
        "type": "object",
        "properties": {
            "target": {
                "type": "string",
                "description": "绑定目标：references/coverage/annotations/all",
                "default": "coverage",
            }
        },
        "required": [],
    },
    handler=bsd_verify_binding,
)

register_tool(
    name="bsd_full_validation",
    description="全链路验证（公理→方程→仿真→验证→Agent）",
    input_schema={
        "type": "object",
        "properties": {
            "quick_mode": {
                "type": "boolean",
                "description": "快速模式，跳过仿真和Agent层验证",
                "default": True,
            }
        },
        "required": [],
    },
    handler=bsd_full_validation,
)


CHEMISTRY_PROBLEMS = [
    {"id": "protein_folding", "name": "蛋白质折叠问题", "category": "basic", "module": "bsd_verify.chemistry.verifier_protein_folding", "class": "ProteinFoldingVerifier"},
    {"id": "high_tc_superconduct", "name": "高温超导机理", "category": "basic", "module": "bsd_verify.chemistry.verifier_high_tc_superconduct", "class": "HighTcSuperconductVerifier"},
    {"id": "quantum_many_body", "name": "量子化学多体问题", "category": "basic", "module": "bsd_verify.chemistry.verifier_quantum_many_body", "class": "QuantumManyBodyVerifier"},
    {"id": "origin_of_life", "name": "生命起源化学", "category": "basic", "module": "bsd_verify.chemistry.verifier_origin_of_life", "class": "OriginOfLifeVerifier"},
    {"id": "self_assembly", "name": "分子识别与自组装", "category": "basic", "module": "bsd_verify.chemistry.verifier_self_assembly", "class": "SelfAssemblyVerifier"},
    {"id": "nonequilibrium_chem", "name": "非平衡态热力学化学", "category": "basic", "module": "bsd_verify.chemistry.verifier_nonequilibrium_chem", "class": "NonequilibriumChemVerifier"},
    {"id": "catalysis_mechanism", "name": "均相催化机理", "category": "basic", "module": "bsd_verify.chemistry.verifier_catalysis_mechanism", "class": "CatalysisMechanismVerifier"},
    {"id": "artificial_photo", "name": "人工光合作用", "category": "engineering", "module": "bsd_verify.chemistry.verifier_artificial_photo", "class": "ArtificialPhotoVerifier"},
    {"id": "room_temp_super", "name": "室温超导材料", "category": "engineering", "module": "bsd_verify.chemistry.verifier_room_temp_super", "class": "RoomTempSuperVerifier"},
    {"id": "inverse_catalyst", "name": "催化剂逆设计", "category": "engineering", "module": "bsd_verify.chemistry.verifier_inverse_catalyst", "class": "InverseCatalystVerifier"},
    {"id": "carbon_capture", "name": "碳捕获与高效转化", "category": "engineering", "module": "bsd_verify.chemistry.verifier_carbon_capture", "class": "CarbonCaptureVerifier"},
    {"id": "high_energy_battery", "name": "高能量密度电池", "category": "engineering", "module": "bsd_verify.chemistry.verifier_high_energy_battery", "class": "HighEnergyBatteryVerifier"},
    {"id": "green_chemistry", "name": "绿色化学全流程替代", "category": "engineering", "module": "bsd_verify.chemistry.verifier_green_chemistry", "class": "GreenChemistryVerifier"},
    {"id": "precision_synthesis", "name": "精准合成/分子手术", "category": "engineering", "module": "bsd_verify.chemistry.verifier_precision_synthesis", "class": "PrecisionSynthesisVerifier"},
]


def bsd_verify_chemistry(
    problem: str = "all",
    category: str = "all",
    detail_level: str = "summary",
) -> Dict[str, Any]:
    try:
        problems_to_verify = []
        if problem == "all":
            if category == "all":
                problems_to_verify = CHEMISTRY_PROBLEMS
            else:
                problems_to_verify = [p for p in CHEMISTRY_PROBLEMS if p["category"] == category]
        else:
            prob = next((p for p in CHEMISTRY_PROBLEMS if p["id"] == problem), None)
            if prob is None:
                return {
                    "success": False,
                    "data": None,
                    "error": f"未知的化学难题标识: {problem}，可用问题: {[p['id'] for p in CHEMISTRY_PROBLEMS]}",
                }
            problems_to_verify = [prob]

        results = []
        for prob in problems_to_verify:
            try:
                module = __import__(prob["module"], fromlist=[prob["class"]])
                verifier_class = getattr(module, prob["class"])
                verifier = verifier_class()
                result = verifier.verify()

                result_dict = {
                    "problem": prob["id"],
                    "problem_name": prob["name"],
                    "category": prob["category"],
                    "verdict": result.verdict,
                    "confidence": result.confidence,
                    "verification_time": result.verification_time,
                    "key_equation": result.key_equation,
                    "proof_chain_length": len(result.proof_chain),
                    "numerical_evidence": result.numerical_evidence,
                    "error": result.error_message if result.verdict == "error" else "",
                }

                if detail_level == "detailed":
                    result_dict["proof_chain"] = result.proof_chain

                results.append(result_dict)
            except Exception as e:
                results.append({
                    "problem": prob["id"],
                    "problem_name": prob["name"],
                    "category": prob.get("category", "unknown"),
                    "verdict": "error",
                    "confidence": 0.0,
                    "error": str(e),
                })

        all_passed = all(r["verdict"] in ("verified", "confirmed") for r in results)
        basic_count = sum(1 for r in results if r.get("category") == "basic")
        eng_count = sum(1 for r in results if r.get("category") == "engineering")

        return {
            "success": True,
            "data": {
                "problem": problem,
                "category_filter": category,
                "detail_level": detail_level,
                "total": len(results),
                "basic_count": basic_count,
                "engineering_count": eng_count,
                "all_passed": all_passed,
                "results": results,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


register_tool(
    name="bsd_verify_chemistry",
    description="验证化学全域难题（14个，含7个基础理论诺奖级+7个工程悬赏产业级）",
    input_schema={
        "type": "object",
        "properties": {
            "problem": {
                "type": "string",
                "description": "难题标识：protein_folding/high_tc_superconduct/quantum_many_body/origin_of_life/self_assembly/nonequilibrium_chem/catalysis_mechanism/artificial_photo/room_temp_super/inverse_catalyst/carbon_capture/high_energy_battery/green_chemistry/precision_synthesis/all",
                "default": "all",
            },
            "category": {
                "type": "string",
                "description": "分类筛选：basic(基础理论)/engineering(工程悬赏)/all",
                "default": "all",
            },
            "detail_level": {
                "type": "string",
                "description": "详细程度：summary/detailed",
                "default": "summary",
            },
        },
        "required": [],
    },
    handler=bsd_verify_chemistry,
)


INSTITUTIONAL_PROBLEMS = [
    {"id": "institutional_paradigm", "name": "三元制度范式", "module": "bsd_verify.economics.verifier_institutional_paradigm", "class": "InstitutionalParadigmVerifier"},
    {"id": "standing_wave", "name": "制度驻波动力学", "module": "bsd_verify.economics.verifier_standing_wave", "class": "InstitutionalStandingWaveVerifier"},
    {"id": "industrial_policy", "name": "产业政策驻波", "module": "bsd_verify.economics.verifier_industrial_policy", "class": "IndustrialPolicyWaveVerifier"},
    {"id": "tariff_policy", "name": "关税制度驻波", "module": "bsd_verify.economics.verifier_tariff_policy", "class": "TariffPolicyWaveVerifier"},
    {"id": "quality_assessment", "name": "制度质量评估", "module": "bsd_verify.economics.verifier_quality_assessment", "class": "InstitutionalQualityVerifier"},
]


def bsd_verify_institutional(
    problem: str = "all",
    detail_level: str = "summary",
) -> Dict[str, Any]:
    try:
        problems_to_verify = []
        if problem == "all":
            problems_to_verify = INSTITUTIONAL_PROBLEMS
        else:
            prob = next((p for p in INSTITUTIONAL_PROBLEMS if p["id"] == problem), None)
            if prob is None:
                return {
                    "success": False,
                    "data": None,
                    "error": f"未知的制度经济学验证项: {problem}，可用项: {[p['id'] for p in INSTITUTIONAL_PROBLEMS]}",
                }
            problems_to_verify = [prob]

        results = []
        for prob in problems_to_verify:
            try:
                module = __import__(prob["module"], fromlist=[prob["class"]])
                verifier_class = getattr(module, prob["class"])
                verifier = verifier_class()
                result = verifier.verify()

                result_dict = {
                    "problem": prob["id"],
                    "problem_name": prob["name"],
                    "verdict": result.verdict,
                    "confidence": result.confidence,
                    "verification_time": result.verification_time,
                    "key_equation": result.key_equation,
                    "proof_chain_length": len(result.proof_chain),
                    "numerical_evidence": result.numerical_evidence,
                    "error": result.error_message if result.verdict == "error" else "",
                }

                if detail_level == "detailed":
                    result_dict["proof_chain"] = result.proof_chain

                results.append(result_dict)
            except Exception as e:
                results.append({
                    "problem": prob["id"],
                    "problem_name": prob["name"],
                    "verdict": "error",
                    "confidence": 0.0,
                    "error": str(e),
                })

        all_passed = all(r["verdict"] in ("verified", "confirmed") for r in results)

        return {
            "success": True,
            "data": {
                "problem": problem,
                "detail_level": detail_level,
                "total": len(results),
                "all_passed": all_passed,
                "results": results,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


register_tool(
    name="bsd_verify_institutional",
    description="验证制度经济学理论体系（基于T88框架，含三元制度范式/制度驻波动力学/产业政策/关税制度/制度质量评估）",
    input_schema={
        "type": "object",
        "properties": {
            "problem": {
                "type": "string",
                "description": "验证项：institutional_paradigm/standing_wave/industrial_policy/tariff_policy/quality_assessment/all",
                "default": "all",
            },
            "detail_level": {
                "type": "string",
                "description": "详细程度：summary/detailed",
                "default": "summary",
            },
        },
        "required": [],
    },
    handler=bsd_verify_institutional,
)
