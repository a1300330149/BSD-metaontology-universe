"""
BSD全域统一理论 — MCP工具注册中心

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

from typing import Any, Callable, Dict, List, Optional


class ToolRegistry:
    """BSD MCP 工具注册中心

    负责注册、查找和调用所有 MCP 工具。
    工具结构：{name, description, inputSchema, handler}
    """

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}

    def register_tool(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        handler: Callable,
    ) -> None:
        """注册一个工具

        Parameters
        ----------
        name : str
            工具名称
        description : str
            工具描述
        input_schema : dict
            输入参数的 JSON Schema 定义
        handler : callable
            工具处理函数
        """
        self._tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": input_schema,
            "handler": handler,
        }

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """获取工具定义

        Parameters
        ----------
        name : str
            工具名称

        Returns
        -------
        dict or None
            工具定义，包含 name, description, inputSchema, handler
        """
        return self._tools.get(name)

    def list_tools(self) -> List[Dict[str, Any]]:
        """列出所有已注册的工具

        Returns
        -------
        list of dict
            工具列表，每个工具包含 name, description, inputSchema
        """
        return [
            {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool["inputSchema"],
            }
            for tool in self._tools.values()
        ]

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """调用指定工具

        Parameters
        ----------
        name : str
            工具名称
        arguments : dict
            调用参数

        Returns
        -------
        any
            工具执行结果；如果工具不存在，返回 {"error": "..."} 字典
        """
        tool = self._tools.get(name)
        if tool is None:
            return {"error": f"工具 '{name}' 未注册", "success": False}
        try:
            return tool["handler"](**arguments)
        except Exception as e:
            return {"error": f"调用工具 '{name}' 失败: {e}", "success": False}


_global_registry = ToolRegistry()


def get_global_registry() -> ToolRegistry:
    """获取全局工具注册中心实例"""
    return _global_registry


def register_tool(
    name: str,
    description: str,
    input_schema: Dict[str, Any],
    handler: Callable,
) -> None:
    """向全局注册中心注册工具"""
    _global_registry.register_tool(name, description, input_schema, handler)
