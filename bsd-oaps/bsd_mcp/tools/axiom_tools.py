"""
BSD全域统一理论 — 公理类MCP工具

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


def _collect_all_axioms() -> List[Any]:
    axioms = []
    try:
        from bsd_engine.axioms.twelve_bsd_axioms import (
            BSD_AXIOM_01, BSD_AXIOM_02, BSD_AXIOM_03, BSD_AXIOM_04,
            BSD_AXIOM_05, BSD_AXIOM_06, BSD_AXIOM_07, BSD_AXIOM_08,
            BSD_AXIOM_09, BSD_AXIOM_10, BSD_AXIOM_11, BSD_AXIOM_12,
        )
        axioms.extend([
            BSD_AXIOM_01, BSD_AXIOM_02, BSD_AXIOM_03, BSD_AXIOM_04,
            BSD_AXIOM_05, BSD_AXIOM_06, BSD_AXIOM_07, BSD_AXIOM_08,
            BSD_AXIOM_09, BSD_AXIOM_10, BSD_AXIOM_11, BSD_AXIOM_12,
        ])
    except ImportError:
        pass

    try:
        from bsd_engine.axioms.seven_origin_axioms import (
            AXIOM_ONE, AXIOM_TWO, AXIOM_THREE, AXIOM_FOUR,
            AXIOM_FIVE, AXIOM_SIX, AXIOM_SEVEN,
        )
        axioms.extend([
            AXIOM_ONE, AXIOM_TWO, AXIOM_THREE, AXIOM_FOUR,
            AXIOM_FIVE, AXIOM_SIX, AXIOM_SEVEN,
        ])
    except ImportError:
        pass

    try:
        from bsd_engine.axioms.three_meaning_axioms import (
            MEANING_AXIOM_ONE, MEANING_AXIOM_TWO, MEANING_AXIOM_THREE,
        )
        axioms.extend([
            MEANING_AXIOM_ONE, MEANING_AXIOM_TWO, MEANING_AXIOM_THREE,
        ])
    except ImportError:
        pass

    try:
        from bsd_engine.axioms.nine_special_axioms import (
            SPECIAL_AXIOM_01, SPECIAL_AXIOM_02, SPECIAL_AXIOM_03,
            SPECIAL_AXIOM_04, SPECIAL_AXIOM_05, SPECIAL_AXIOM_06,
            SPECIAL_AXIOM_07, SPECIAL_AXIOM_08, SPECIAL_AXIOM_09,
        )
        axioms.extend([
            SPECIAL_AXIOM_01, SPECIAL_AXIOM_02, SPECIAL_AXIOM_03,
            SPECIAL_AXIOM_04, SPECIAL_AXIOM_05, SPECIAL_AXIOM_06,
            SPECIAL_AXIOM_07, SPECIAL_AXIOM_08, SPECIAL_AXIOM_09,
        ])
    except ImportError:
        pass

    try:
        from bsd_engine.axioms.eight_unification_axioms import (
            UNIFICATION_AXIOM_01, UNIFICATION_AXIOM_02, UNIFICATION_AXIOM_03,
            UNIFICATION_AXIOM_04, UNIFICATION_AXIOM_05, UNIFICATION_AXIOM_06,
            UNIFICATION_AXIOM_07, UNIFICATION_AXIOM_08,
        )
        axioms.extend([
            UNIFICATION_AXIOM_01, UNIFICATION_AXIOM_02, UNIFICATION_AXIOM_03,
            UNIFICATION_AXIOM_04, UNIFICATION_AXIOM_05, UNIFICATION_AXIOM_06,
            UNIFICATION_AXIOM_07, UNIFICATION_AXIOM_08,
        ])
    except ImportError:
        pass

    return axioms


def _axiom_to_dict(axiom: Any, index: int) -> Dict[str, Any]:
    return {
        "axiom_id": index,
        "name": getattr(axiom, "name", ""),
        "description": getattr(axiom, "description", ""),
        "formula": getattr(axiom, "formula", ""),
        "category": getattr(axiom, "category", ""),
    }


def bsd_query_axiom(axiom_id: int = 1) -> Dict[str, Any]:
    try:
        all_axioms = _collect_all_axioms()
        if 1 <= axiom_id <= len(all_axioms):
            axiom = all_axioms[axiom_id - 1]
            return {
                "success": True,
                "data": _axiom_to_dict(axiom, axiom_id),
                "error": "",
            }
        return {
            "success": False,
            "data": None,
            "error": f"公理编号 {axiom_id} 超出范围（1-{len(all_axioms)}）",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_list_all_axioms() -> Dict[str, Any]:
    try:
        all_axioms = _collect_all_axioms()
        axiom_list = [
            _axiom_to_dict(axiom, i + 1)
            for i, axiom in enumerate(all_axioms)
        ]
        return {
            "success": True,
            "data": {
                "total": len(axiom_list),
                "axioms": axiom_list,
            },
            "error": "",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_get_constants() -> Dict[str, Any]:
    try:
        from bsd_engine.registry import constants
        result = {}
        for name in dir(constants):
            if name.isupper() and not name.startswith("_"):
                value = getattr(constants, name)
                if isinstance(value, (int, float, str, dict, list)):
                    result[name] = value
        return {
            "success": True,
            "data": {
                "constants": result,
                "author": getattr(constants, "AUTHOR", ""),
                "lock_date": getattr(constants, "LOCK_DATE", ""),
                "hash": getattr(constants, "HASH_SHA256", ""),
            },
            "error": "",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_verify_params() -> Dict[str, Any]:
    try:
        from bsd_engine.registry.constants import verify_params
        result = verify_params()
        return {
            "success": True,
            "data": {
                "verified": result,
                "message": "所有锁档参数验证通过，未被篡改",
            },
            "error": "",
        }
    except ValueError as e:
        return {
            "success": False,
            "data": {
                "verified": False,
            },
            "error": str(e),
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_search_axiom(keyword: str = "") -> Dict[str, Any]:
    try:
        all_axioms = _collect_all_axioms()
        keyword_lower = keyword.lower()
        results = []
        for i, axiom in enumerate(all_axioms):
            name = getattr(axiom, "name", "").lower()
            desc = getattr(axiom, "description", "").lower()
            category = getattr(axiom, "category", "").lower()
            if keyword_lower in name or keyword_lower in desc or keyword_lower in category:
                results.append(_axiom_to_dict(axiom, i + 1))
        return {
            "success": True,
            "data": {
                "keyword": keyword,
                "count": len(results),
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
    name="bsd_query_axiom",
    description="查询指定编号的BSD公理（1-39）",
    input_schema={
        "type": "object",
        "properties": {
            "axiom_id": {
                "type": "integer",
                "description": "公理编号（1-39）",
                "minimum": 1,
                "maximum": 39,
                "default": 1,
            }
        },
        "required": [],
    },
    handler=bsd_query_axiom,
)

register_tool(
    name="bsd_list_all_axioms",
    description="列出全部39条BSD公理",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_list_all_axioms,
)

register_tool(
    name="bsd_get_constants",
    description="获取BSD全域统一理论的所有锁档常量",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_get_constants,
)

register_tool(
    name="bsd_verify_params",
    description="验证锁档参数是否被篡改",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_verify_params,
)

register_tool(
    name="bsd_search_axiom",
    description="按关键词搜索BSD公理",
    input_schema={
        "type": "object",
        "properties": {
            "keyword": {
                "type": "string",
                "description": "搜索关键词",
                "default": "",
            }
        },
        "required": [],
    },
    handler=bsd_search_axiom,
)
