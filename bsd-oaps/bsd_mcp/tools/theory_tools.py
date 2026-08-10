"""
BSD全域统一理论 — 理论类MCP工具

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

import os
import re
from typing import Any, Dict, List, Optional

from bsd_mcp.tool_registry import register_tool


THEORY_LEVELS = {
    "L0": "总本源层",
    "L1": "本源公理层",
    "L2": "方程定律层",
    "L3": "仿真验证层",
    "L4": "应用层",
}

THEORY_MODULES_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "bsd_engine",
    "theories",
)


def _get_theory_module_files() -> List[str]:
    if not os.path.isdir(THEORY_MODULES_DIR):
        return []
    files = []
    for f in sorted(os.listdir(THEORY_MODULES_DIR)):
        if f.startswith("t") and f.endswith(".py") and not f.startswith("test_"):
            files.append(f)
    return files


def _extract_module_info(filepath: str) -> Dict[str, Any]:
    info = {
        "module_id": "",
        "module_name": "",
        "version": "",
        "cosmic_level": None,
        "base_belong": "",
        "corresponding_axiom": "",
        "description": "",
        "class_name": "",
    }
    try:
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        doc_match = re.search(r'^"""(.*?)"""', content, re.DOTALL | re.MULTILINE)
        if doc_match:
            doc = doc_match.group(1).strip()
            info["description"] = doc[:200]

        id_match = re.search(r'module_id\s*=\s*["\']([^"\']+)["\']', content)
        if id_match:
            info["module_id"] = id_match.group(1)
        else:
            # Fallback: extract from filename (e.g. t86_chemistry_basic_theory.py -> t86)
            fn_match = re.match(r'(t\d+)', filename)
            if fn_match:
                info["module_id"] = fn_match.group(1).upper()

        name_match = re.search(r'module_name\s*=\s*["\']([^"\']+)["\']', content)
        if name_match:
            info["module_name"] = name_match.group(1)
        else:
            # Fallback: extract first line from docstring
            if doc_match:
                first_line = doc.split('\n')[0].strip()
                if first_line:
                    info["module_name"] = first_line[:100]

        ver_match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
        if ver_match:
            info["version"] = ver_match.group(1)
        else:
            # Fallback: search for 版本：Vx.x in docstring
            ver_fallback = re.search(r'版本[：:]\s*(V[\d.]+)', content)
            if ver_fallback:
                info["version"] = ver_fallback.group(1)

        level_match = re.search(r'cosmic_level\s*=\s*(\d+)', content)
        if level_match:
            info["cosmic_level"] = int(level_match.group(1))

        base_match = re.search(r'base_belong\s*=\s*["\']([^"\']+)["\']', content)
        if base_match:
            info["base_belong"] = base_match.group(1)
        else:
            # Fallback: search for 归属基底 in docstring
            base_fallback = re.search(r'归属基底[：:]\s*(.+)', content)
            if base_fallback:
                info["base_belong"] = base_fallback.group(1).strip()[:100]

        axiom_match = re.search(r'corresponding_axiom\s*=\s*["\']([^"\']+)["\']', content)
        if axiom_match:
            info["corresponding_axiom"] = axiom_match.group(1)
        else:
            # Fallback: search for 对应公理 in docstring
            axiom_fallback = re.search(r'对应公理[：:]\s*(.+)', content)
            if axiom_fallback:
                info["corresponding_axiom"] = axiom_fallback.group(1).strip()[:100]

        class_match = re.search(r'class\s+(\w+)\s*\(\s*BaseTheoryModule\s*\)', content)
        if class_match:
            info["class_name"] = class_match.group(1)

    except Exception:
        pass
    return info


def _load_all_theory_modules() -> List[Dict[str, Any]]:
    files = _get_theory_module_files()
    modules = []
    for fname in files:
        filepath = os.path.join(THEORY_MODULES_DIR, fname)
        info = _extract_module_info(filepath)
        info["file"] = fname
        modules.append(info)
    return modules


def bsd_query_theory(
    query: str = "",
    layer: str = "all",
) -> Dict[str, Any]:
    try:
        all_modules = _load_all_theory_modules()
        results = all_modules

        if layer != "all":
            level_num = None
            if layer.startswith("L") and layer[1:].isdigit():
                level_num = int(layer[1:])
            if level_num is not None:
                results = [
                    m for m in results
                    if m.get("cosmic_level") == level_num
                ]

        if query:
            kw_lower = query.lower()
            results = [
                m for m in results
                if kw_lower in m.get("module_id", "").lower()
                or kw_lower in m.get("module_name", "").lower()
                or kw_lower in m.get("description", "").lower()
                or kw_lower in m.get("base_belong", "").lower()
            ]

        return {
            "success": True,
            "data": {
                "query": query,
                "layer": layer,
                "total": len(results),
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


def bsd_list_theories(
    layer: str = "all",
) -> Dict[str, Any]:
    try:
        all_modules = _load_all_theory_modules()

        if layer == "all":
            grouped: Dict[str, List[Dict[str, Any]]] = {}
            for m in all_modules:
                lvl = m.get("cosmic_level")
                key = f"L{lvl}" if lvl is not None else "unknown"
                if key not in grouped:
                    grouped[key] = []
                grouped[key].append(m)

            return {
                "success": True,
                "data": {
                    "layer": layer,
                    "total": len(all_modules),
                    "grouped_by_layer": grouped,
                    "layer_names": THEORY_LEVELS,
                },
                "error": "",
            }
        else:
            level_num = None
            if layer.startswith("L") and layer[1:].isdigit():
                level_num = int(layer[1:])

            filtered = []
            if level_num is not None:
                filtered = [
                    m for m in all_modules
                    if m.get("cosmic_level") == level_num
                ]

            return {
                "success": True,
                "data": {
                    "layer": layer,
                    "layer_name": THEORY_LEVELS.get(layer, ""),
                    "total": len(filtered),
                    "theories": filtered,
                },
                "error": "",
            }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_search_theory(
    keyword: str = "",
) -> Dict[str, Any]:
    try:
        all_modules = _load_all_theory_modules()
        query_lower = keyword.lower()
        results = []

        for m in all_modules:
            score = 0
            matched_fields = []

            fields_to_search = [
                "module_id", "module_name", "description",
                "base_belong", "corresponding_axiom",
            ]

            for field in fields_to_search:
                val = str(m.get(field, "")).lower()
                if query_lower in val:
                    score += 1
                    matched_fields.append(field)
                    if val.startswith(query_lower):
                        score += 1

            if score > 0:
                result_item = dict(m)
                result_item["match_score"] = score
                result_item["matched_fields"] = matched_fields
                results.append(result_item)

        results.sort(key=lambda x: x["match_score"], reverse=True)

        return {
            "success": True,
            "data": {
                "keyword": keyword,
                "total": len(results),
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


def bsd_get_origin_info() -> Dict[str, Any]:
    try:
        origin_modules = []
        all_modules = _load_all_theory_modules()
        for m in all_modules:
            if m.get("cosmic_level") == 0:
                origin_modules.append(m)

        origin_modules.sort(key=lambda x: x.get("module_id", ""))

        total_modules = len(origin_modules)

        return {
            "success": True,
            "data": {
                "level": "L0",
                "level_name": THEORY_LEVELS.get("L0", "总本源层"),
                "total_theories": total_modules,
                "theories": origin_modules,
                "description": "L0总本源层是BSD全域统一理论的最根本源层，包含元道本源、空无创生、三元存在等核心本源理论。",
                "core_attributes": {
                    "is_origin_locked": True,
                    "origin_authority": "最高",
                    "lock_date": "2026-06-20",
                },
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_theory_chain(
    axiom_id: int = 1,
) -> Dict[str, Any]:
    try:
        all_modules = _load_all_theory_modules()

        target = None
        for m in all_modules:
            module_id = m.get("module_id", "")
            if module_id and module_id.upper() == f"T{axiom_id}":
                target = m
                break

        if target is None and all_modules:
            idx = min(max(axiom_id - 1, 0), len(all_modules) - 1)
            target = all_modules[idx]

        if target is None:
            return {
                "success": False,
                "data": None,
                "error": f"未找到与公理ID {axiom_id} 关联的理论模块",
            }

        chain = {
            "theory": {
                "module_id": target.get("module_id"),
                "module_name": target.get("module_name"),
                "base_belong": target.get("base_belong"),
                "cosmic_level": target.get("cosmic_level"),
            },
            "axioms": [],
            "equations": [],
            "code_bindings": [],
        }

        corresponding_axiom = target.get("corresponding_axiom", "")
        if corresponding_axiom:
            chain["axioms"].append({
                "name": corresponding_axiom,
                "source": "理论模块声明",
            })

        try:
            from bsd_mcp.tools.equation_tools import EQUATION_LIST
            for eq in EQUATION_LIST:
                eq_name = eq.get("name", "")
                module_name = target.get("module_name", "")
                if any(kw in eq_name or kw in module_name for kw in ["熵", "相干", "宇宙", "相变", "驻波", "涌现"]):
                    chain["equations"].append({
                        "id": eq["id"],
                        "name": eq["name"],
                        "relation": "潜在关联",
                    })
        except Exception:
            pass

        try:
            from bsd_engine.validators.binding_checker import scan_all_source_files
            headers = scan_all_source_files()
            base_belong = target.get("base_belong", "")
            for filepath, header in headers.items():
                header_base = header.get("归属基底", "")
                if base_belong and base_belong in header_base:
                    chain["code_bindings"].append({
                        "file": filepath,
                        "base_belong": header_base,
                        "theory_reference": header.get("理论原文出处", ""),
                    })
        except Exception:
            pass

        axiom_count = len(chain["axioms"])
        equation_count = len(chain["equations"])
        code_count = len(chain["code_bindings"])
        chain_complete = axiom_count > 0 and equation_count > 0 and code_count > 0

        return {
            "success": True,
            "data": {
                "axiom_id": axiom_id,
                "found": True,
                "chain_complete": chain_complete,
                "chain": chain,
                "summary": {
                    "axioms": axiom_count,
                    "equations": equation_count,
                    "code_bindings": code_count,
                },
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
    name="bsd_query_theory",
    description="按关键词/层级查询理论文档",
    input_schema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "查询关键词，匹配模块ID、名称、描述",
                "default": "",
            },
            "layer": {
                "type": "string",
                "description": "层级过滤：L0/L1/L2/L3/L4/all",
                "default": "all",
            },
        },
        "required": [],
    },
    handler=bsd_query_theory,
)

register_tool(
    name="bsd_list_theories",
    description="列出指定层级的所有理论文档",
    input_schema={
        "type": "object",
        "properties": {
            "layer": {
                "type": "string",
                "description": "层级：L0/L1/L2/L3/L4/all",
                "default": "all",
            }
        },
        "required": [],
    },
    handler=bsd_list_theories,
)

register_tool(
    name="bsd_search_theory",
    description="全文搜索理论库",
    input_schema={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "搜索关键词",
                "default": "",
            },
        },
        "required": [],
    },
    handler=bsd_search_theory,
)

register_tool(
    name="bsd_get_origin_info",
    description="获取本源层信息（L0总本源层）",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_get_origin_info,
)

register_tool(
    name="bsd_theory_chain",
    description="获取从公理到方程到代码的完整关联链",
    input_schema={
        "type": "object",
        "properties": {
            "axiom_id": {
                "type": "integer",
                "description": "公理ID",
                "default": 1,
            }
        },
        "required": [],
    },
    handler=bsd_theory_chain,
)


def bsd_export_paper(
    paper_type: str = "chemistry",
    output_path: str = "",
) -> Dict[str, Any]:
    try:
        if paper_type in ("chemistry", "chemistry_detailed"):
            if paper_type == "chemistry_detailed":
                from bsd_engine.exporter.paper_exporter_detailed import export_paper
                default_name = "BSD_Chemistry_Unified_Paper_Detailed_T88.docx"
                description = "基于T86基础理论篇 + T87工程应用篇 + T88制度经济学的完整详细论文"
                chapters = [
                    "第一章 引言",
                    "第二章 化学统一核心参数量化体系",
                    "第三章 化学键统一谱系",
                    "第四章 理论基础与公理体系",
                    "第五章 T86 化学基础理论难题详细推导",
                    "第六章 T87 化学工程悬赏难题详细推导",
                    "第七章 全链路验证结果",
                    "第八章 T88 数理经济制度分析",
                    "第九章 结论与展望",
                    "参考文献",
                    "附录",
                ]
            else:
                from bsd_engine.exporter.paper_exporter import export_paper
                default_name = "BSD_Chemistry_Unified_Paper.docx"
                description = "基于T86基础理论篇 + T87工程应用篇的完整论文"
                chapters = [
                    "第一章 引言",
                    "第二章 理论基础与公理体系",
                    "第三章 T86 化学基础理论难题验证",
                    "第四章 T87 化学工程悬赏难题验证",
                    "第五章 T88 数理经济制度分析",
                    "第六章 全链路验证结果",
                    "第七章 结论与展望",
                    "参考文献",
                    "附录",
                ]

            if not output_path:
                output_path = default_name

            result_path = export_paper(output_path)

            return {
                "success": True,
                "data": {
                    "paper_type": paper_type,
                    "output_path": result_path,
                    "paper_name": "BSD化学全域难题统一实证体系",
                    "description": description,
                    "chapters": chapters,
                },
                "error": "",
            }
        else:
            return {
                "success": False,
                "data": None,
                "error": f"不支持的论文类型: {paper_type}，当前支持 chemistry / chemistry_detailed",
            }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


register_tool(
    name="bsd_export_paper",
    description="导出BSD理论论文（DOCX格式），支持化学全域难题统一实证体系论文（含T86/T87/T88）",
    input_schema={
        "type": "object",
        "properties": {
            "paper_type": {
                "type": "string",
                "description": "论文类型：chemistry（标准版，含T86/T87/T88）或 chemistry_detailed（详细版，含T86/T87/T88完整推导）",
                "default": "chemistry",
            },
            "output_path": {
                "type": "string",
                "description": "输出路径（可选），默认当前目录",
                "default": "",
            },
        },
        "required": [],
    },
    handler=bsd_export_paper,
)
