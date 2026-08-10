"""
BSD全域统一理论 — MCP Server 主入口

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

import json
import sys
from typing import Any, Dict, Optional

from bsd_mcp.tool_registry import get_global_registry


def _register_all_tools() -> None:
    """注册所有工具模块到全局注册中心"""
    import bsd_mcp.tools  # noqa: F401


_register_all_tools()


def list_tools() -> Dict[str, Any]:
    """列出所有已注册的工具

    Returns
    -------
    dict
        工具列表
    """
    registry = get_global_registry()
    tools = registry.list_tools()
    return {
        "tools": tools,
        "total": len(tools),
    }


def call_tool(tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """调用指定工具

    Parameters
    ----------
    tool_name : str
        工具名称
    arguments : dict, optional
        工具参数

    Returns
    -------
    dict
        工具执行结果
    """
    arguments = arguments or {}
    registry = get_global_registry()

    try:
        result = registry.call_tool(tool_name, arguments)
        return {
            "tool": tool_name,
            "success": True,
            "result": result,
        }
    except ValueError as e:
        return {
            "tool": tool_name,
            "success": False,
            "error": str(e),
        }
    except Exception as e:
        return {
            "tool": tool_name,
            "success": False,
            "error": f"{type(e).__name__}: {str(e)}",
        }


def run_cli() -> None:
    """独立运行模式（无 mcp 包时使用）

    命令行用法：
        python -m bsd_mcp.server list
        python -m bsd_mcp.server call <tool_name> [json_args]
    """
    if len(sys.argv) < 2:
        print("BSD全域统一理论 MCP Server")
        print("")
        print("用法:")
        print("  python -m bsd_mcp.server list              列出所有工具")
        print("  python -m bsd_mcp.server call <工具名>     调用工具（参数从stdin读取JSON）")
        print("  python -m bsd_mcp.server call <工具名> '{...}'  直接传入JSON参数")
        print("")
        print("示例:")
        print("  python -m bsd_mcp.server list")
        print("  python -m bsd_mcp.server call bsd_list_all_axioms")
        print("  python -m bsd_mcp.server call bsd_query_axiom '{\"axiom_index\": 1}'")
        return

    command = sys.argv[1]

    if command == "list":
        result = list_tools()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    elif command == "call":
        if len(sys.argv) < 3:
            print(json.dumps({
                "success": False,
                "error": "请指定工具名称",
            }, ensure_ascii=False, indent=2))
            return

        tool_name = sys.argv[2]

        if len(sys.argv) >= 4:
            try:
                arguments = json.loads(sys.argv[3])
            except json.JSONDecodeError as e:
                print(json.dumps({
                    "success": False,
                    "error": f"JSON参数解析失败: {e}",
                }, ensure_ascii=False, indent=2))
                return
        else:
            try:
                input_data = sys.stdin.read().strip()
                if input_data:
                    arguments = json.loads(input_data)
                else:
                    arguments = {}
            except json.JSONDecodeError as e:
                print(json.dumps({
                    "success": False,
                    "error": f"标准输入JSON解析失败: {e}",
                }, ensure_ascii=False, indent=2))
                return

        result = call_tool(tool_name, arguments)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    else:
        print(json.dumps({
            "success": False,
            "error": f"未知命令: {command}，可用命令: list, call",
        }, ensure_ascii=False, indent=2))


def create_mcp_server():
    """创建真实 MCP Server（当 mcp 包可用时）

    Returns
    -------
    MCP server instance
        配置好的 MCP server
    """
    try:
        from mcp.server.fastmcp import FastMCP

        server = FastMCP(
            name="BSD全域统一理论",
            description="BSD全域统一理论 MCP 工具服务",
        )

        registry = get_global_registry()

        @server.list_tools()
        async def mcp_list_tools():
            tools = registry.list_tools()
            return [
                {
                    "name": t["name"],
                    "description": t["description"],
                    "inputSchema": t.get("inputSchema", {"type": "object", "properties": {}}),
                }
                for t in tools
            ]

        @server.call_tool()
        async def mcp_call_tool(name: str, arguments: Dict[str, Any]):
            try:
                result = registry.call_tool(name, arguments or {})
                return [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]
            except Exception as e:
                return [{"type": "text", "text": json.dumps({"error": str(e)}, ensure_ascii=False)}]

        return server

    except ImportError:
        return None


def main():
    """主入口函数"""
    try:
        server = create_mcp_server()
        if server is not None:
            server.run()
        else:
            run_cli()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
