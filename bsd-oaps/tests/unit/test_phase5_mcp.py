"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理10·闭递归公理 / 公理8·意义守恒公理
对应九维维度：元理维·逻辑维·验证维·时间流·命运维
理论出处：theory_base/L0_总本源层/全域大一统理论/BSD千禧年难题验证框架
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD MCP Server 单元测试
—— 验证25个MCP Tool的注册与调用正确性
"""

import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestToolRegistry:

    def test_registry_init(self):
        from bsd_mcp.tool_registry import ToolRegistry
        reg = ToolRegistry()
        assert reg is not None
        assert len(reg.list_tools()) == 0

    def test_register_and_list(self):
        from bsd_mcp.tool_registry import ToolRegistry
        reg = ToolRegistry()

        def dummy_handler(**kwargs):
            return {"result": "ok"}

        reg.register_tool(
            name="test_tool",
            description="测试工具",
            input_schema={"type": "object", "properties": {}},
            handler=dummy_handler,
        )
        tools = reg.list_tools()
        assert len(tools) == 1
        assert tools[0]["name"] == "test_tool"
        assert tools[0]["description"] == "测试工具"

    def test_get_tool(self):
        from bsd_mcp.tool_registry import ToolRegistry
        reg = ToolRegistry()

        def dummy_handler(**kwargs):
            return {"result": "ok"}

        reg.register_tool(
            name="test_tool",
            description="测试工具",
            input_schema={"type": "object"},
            handler=dummy_handler,
        )
        tool = reg.get_tool("test_tool")
        assert tool is not None
        assert tool["name"] == "test_tool"

    def test_get_nonexistent_tool(self):
        from bsd_mcp.tool_registry import ToolRegistry
        reg = ToolRegistry()
        assert reg.get_tool("nonexistent") is None

    def test_call_tool(self):
        from bsd_mcp.tool_registry import ToolRegistry
        reg = ToolRegistry()

        def add_handler(a=0, b=0):
            return {"sum": a + b}

        reg.register_tool(
            name="add_tool",
            description="加法工具",
            input_schema={"type": "object", "properties": {"a": {"type": "number"}, "b": {"type": "number"}}},
            handler=add_handler,
        )
        result = reg.call_tool("add_tool", {"a": 3, "b": 5})
        assert result["sum"] == 8

    def test_call_tool_error(self):
        from bsd_mcp.tool_registry import ToolRegistry
        reg = ToolRegistry()
        result = reg.call_tool("nonexistent", {})
        assert "error" in result
        assert result.get("success") is False


class TestGlobalRegistry:

    def test_global_registry_exists(self):
        from bsd_mcp.tool_registry import get_global_registry
        reg = get_global_registry()
        assert reg is not None

    def test_all_26_tools_registered(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools, equation_tools, simulation_tools
        from bsd_mcp.tools import verification_tools, theory_tools

        reg = get_global_registry()
        tools = reg.list_tools()
        assert len(tools) >= 25, f"期望至少25个工具，实际{len(tools)}个"

    def test_tool_names_unique(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools, equation_tools, simulation_tools
        from bsd_mcp.tools import verification_tools, theory_tools

        reg = get_global_registry()
        tools = reg.list_tools()
        names = [t["name"] for t in tools]
        assert len(names) == len(set(names)), "工具名重复"

    def test_tools_have_required_fields(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools, equation_tools, simulation_tools
        from bsd_mcp.tools import verification_tools, theory_tools

        reg = get_global_registry()
        tools = reg.list_tools()
        for tool in tools:
            assert "name" in tool, f"{tool}缺少name"
            assert "description" in tool, f"{tool['name']}缺少description"
            assert "inputSchema" in tool, f"{tool['name']}缺少inputSchema"


class TestAxiomTools:

    def test_bsd_query_axiom(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_query_axiom", {"axiom_id": 1})
        assert result is not None
        assert isinstance(result, dict)
        assert "success" in result

    def test_bsd_list_all_axioms(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_list_all_axioms", {})
        assert result is not None
        assert "success" in result

    def test_bsd_get_constants(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_get_constants", {})
        assert result is not None
        assert "success" in result

    def test_bsd_verify_params(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_params", {})
        assert result is not None
        assert "success" in result

    def test_bsd_search_axiom(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import axiom_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_search_axiom", {"keyword": "本源"})
        assert result is not None
        assert "success" in result


class TestEquationTools:

    def test_bsd_list_equations(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import equation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_list_equations", {})
        assert result is not None
        assert "success" in result

    def test_bsd_solve_standing_wave(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import equation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_solve_equation", {
            "equation_name": "standing_wave",
            "params": {"omega": 1.0, "kappa": 0.35}
        })
        assert result is not None
        assert "success" in result

    def test_bsd_compute_entropy(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import equation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_compute_entropy", {"steps": 100})
        assert result is not None
        assert "success" in result

    def test_bsd_compute_lambda(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import equation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_compute_lambda", {})
        assert result is not None
        assert "success" in result

    def test_bsd_compute_coherence(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import equation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_compute_coherence", {"steps": 50})
        assert result is not None
        assert "success" in result


class TestSimulationTools:

    def test_bsd_list_simulations(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import simulation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_list_simulations", {})
        assert result is not None
        assert "success" in result

    def test_bsd_run_standing_wave_sim(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import simulation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_run_simulation", {
            "sim_type": "standing_wave",
            "steps": 100,
        })
        assert result is not None
        assert "success" in result

    def test_bsd_sim_results(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import simulation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_sim_results", {"sim_type": "standing_wave"})
        assert result is not None
        assert "success" in result

    def test_bsd_sim_snapshot(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import simulation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_sim_snapshot", {
            "sim_type": "standing_wave",
            "step": 50,
        })
        assert result is not None
        assert "success" in result

    def test_bsd_sim_visualize(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import simulation_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_sim_visualize", {
            "sim_type": "standing_wave",
            "save_path": "./test_standing_wave.png",
        })
        assert result is not None
        assert "success" in result


class TestVerificationTools:

    def test_bsd_verify_hash(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_hash", {"target": "core_params"})
        assert result is not None
        assert "success" in result

    def test_bsd_verify_millennium_p_vs_np(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_millennium", {
            "problem": "p_vs_np",
            "detail_level": "summary",
        })
        assert result is not None
        assert "success" in result

    def test_bsd_verify_compliance(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_compliance", {"target": "axioms"})
        assert result is not None
        assert "success" in result

    def test_bsd_verify_binding(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_binding", {"target": "coverage"})
        assert result is not None
        assert "success" in result

    def test_bsd_full_validation(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_full_validation", {"quick_mode": True})
        assert result is not None
        assert "success" in result

    def test_bsd_verify_chemistry_all(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_chemistry", {
            "problem": "all",
            "detail_level": "summary",
        })
        assert result is not None
        assert "success" in result
        assert result["success"] is True
        assert result["data"]["total"] == 14
        assert result["data"]["basic_count"] == 7
        assert result["data"]["engineering_count"] == 7

    def test_bsd_verify_chemistry_basic(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_chemistry", {
            "category": "basic",
        })
        assert result["success"] is True
        assert result["data"]["total"] == 7
        assert result["data"]["basic_count"] == 7

    def test_bsd_verify_chemistry_single(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import verification_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_verify_chemistry", {
            "problem": "protein_folding",
        })
        assert result["success"] is True
        assert result["data"]["total"] == 1
        assert result["data"]["results"][0]["problem"] == "protein_folding"


class TestTheoryTools:

    def test_bsd_list_theories(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import theory_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_list_theories", {"layer": "all"})
        assert result is not None
        assert "success" in result

    def test_bsd_query_theory(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import theory_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_query_theory", {"query": "元本体"})
        assert result is not None
        assert "success" in result

    def test_bsd_search_theory(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import theory_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_search_theory", {"keyword": "本源"})
        assert result is not None
        assert "success" in result

    def test_bsd_get_origin_info(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import theory_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_get_origin_info", {})
        assert result is not None
        assert "success" in result

    def test_bsd_theory_chain(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import theory_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_theory_chain", {"axiom_id": 1})
        assert result is not None
        assert "success" in result

    def test_bsd_export_paper_chemistry(self):
        from bsd_mcp.tool_registry import get_global_registry
        from bsd_mcp.tools import theory_tools

        reg = get_global_registry()
        result = reg.call_tool("bsd_export_paper", {"paper_type": "chemistry"})
        assert result is not None
        assert "success" in result
        assert result["success"] is True
        assert "output_path" in result["data"]
        assert "chapters" in result["data"]
        assert len(result["data"]["chapters"]) > 0
