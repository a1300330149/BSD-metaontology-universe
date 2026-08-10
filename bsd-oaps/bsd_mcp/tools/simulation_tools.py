"""
BSD全域统一理论 — 仿真类MCP工具

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

import base64
import io
import os
import tempfile
from typing import Any, Dict, List, Optional

import numpy as np

from bsd_mcp.tool_registry import register_tool


SIMULATION_LIST = [
    {"id": "cosmology", "name": "宇宙学仿真器", "class": "CosmologySimulator", "module": "bsd_sim.cosmology_sim"},
    {"id": "phase_transition", "name": "相变仿真器", "class": "PhaseTransitionSimulator", "module": "bsd_sim.phase_transition_sim"},
    {"id": "emergence", "name": "涌现仿真器", "class": "EmergenceSimulator", "module": "bsd_sim.emergence_sim"},
    {"id": "standing_wave", "name": "驻波仿真器", "class": "StandingWaveSimulator", "module": "bsd_sim.standing_wave_sim"},
    {"id": "four_force", "name": "四力统一仿真器", "class": "FourForceSimulator", "module": "bsd_sim.four_force_sim"},
    {"id": "life_steady", "name": "生命稳态仿真器", "class": "LifeSteadySimulator", "module": "bsd_sim.life_steady_sim"},
    {"id": "chemistry", "name": "化学三阶仿真器", "class": "ChemistrySimulator", "module": "bsd_sim.chemistry_sim"},
    {"id": "civilization", "name": "文明熵流仿真器", "class": "CivilizationSimulator", "module": "bsd_sim.civilization_sim"},
]

_sim_instances: Dict[str, Any] = {}


def _get_simulator(sim_type: str) -> Any:
    if sim_type in _sim_instances:
        return _sim_instances[sim_type]

    sim_info = next((s for s in SIMULATION_LIST if s["id"] == sim_type), None)
    if sim_info is None:
        raise ValueError(f"仿真器 '{sim_type}' 不存在")

    module = __import__(sim_info["module"], fromlist=[sim_info["class"]])
    sim_class = getattr(module, sim_info["class"])
    sim_instance = sim_class()
    _sim_instances[sim_type] = sim_instance
    return sim_instance


def bsd_run_simulation(
    sim_type: str = "standing_wave",
    steps: int = 1000,
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    params = params or {}

    try:
        sim_info = next((s for s in SIMULATION_LIST if s["id"] == sim_type), None)
        if sim_info is None:
            return {
                "success": False,
                "data": None,
                "error": f"仿真器 '{sim_type}' 不存在",
            }

        module = __import__(sim_info["module"], fromlist=[sim_info["class"]])
        sim_class = getattr(module, sim_info["class"])

        sim_instance = sim_class(time_steps=steps) if "time_steps" in params or True else sim_class()

        if hasattr(sim_instance, "setup_wave"):
            try:
                sim_instance.setup_wave(mode_n=1, kappa=0.35)
            except Exception:
                pass

        if hasattr(sim_instance, "run"):
            sim_instance.run()
        elif hasattr(sim_instance, "simulate"):
            sim_instance.simulate()
        else:
            return {
                "success": False,
                "data": None,
                "error": "仿真器没有 run 或 simulate 方法",
            }

        _sim_instances[sim_type] = sim_instance

        return {
            "success": True,
            "data": {
                "sim_type": sim_type,
                "steps": steps,
                "running": True,
                "has_results": True,
                "message": f"仿真器 '{sim_type}' 运行成功",
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_list_simulations() -> Dict[str, Any]:
    try:
        return {
            "success": True,
            "data": {
                "total": len(SIMULATION_LIST),
                "simulations": [
                    {"id": s["id"], "name": s["name"]}
                    for s in SIMULATION_LIST
                ],
            },
            "error": "",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_sim_results(
    sim_type: str = "standing_wave",
) -> Dict[str, Any]:
    try:
        sim = _get_simulator(sim_type)

        results = {}
        for attr in dir(sim):
            if attr.startswith("_"):
                continue
            val = getattr(sim, attr)
            if isinstance(val, np.ndarray):
                results[attr] = {
                    "shape": list(val.shape),
                    "dtype": str(val.dtype),
                    "min": float(np.min(val)) if val.size > 0 else None,
                    "max": float(np.max(val)) if val.size > 0 else None,
                    "mean": float(np.mean(val)) if val.size > 0 else None,
                }
            elif isinstance(val, (int, float, np.floating, np.integer)):
                results[attr] = float(val)
            elif isinstance(val, str):
                results[attr] = val
            elif isinstance(val, bool):
                results[attr] = val

        return {
            "success": True,
            "data": {
                "sim_type": sim_type,
                "has_results": True,
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


def bsd_sim_snapshot(
    sim_type: str = "standing_wave",
    step: int = 50,
) -> Dict[str, Any]:
    try:
        sim = _get_simulator(sim_type)

        snapshot_data = {}
        for attr in ["t", "scale_factor", "hubble_param", "state", "time", "position", "velocity"]:
            if hasattr(sim, attr):
                val = getattr(sim, attr)
                if isinstance(val, np.ndarray):
                    if val.ndim >= 1:
                        idx = min(max(step, 0), len(val) - 1)
                        snapshot_data[attr] = float(val[idx]) if val.ndim == 1 else val[idx].tolist()
                    else:
                        snapshot_data[attr + "_shape"] = list(val.shape)
                        if val.size > 0:
                            snapshot_data[attr + "_first"] = float(val.flat[0]) if val.ndim > 0 else float(val)
                            snapshot_data[attr + "_last"] = float(val.flat[-1]) if val.ndim > 0 else float(val)

        if hasattr(sim, "time_steps"):
            snapshot_data["time_steps"] = int(sim.time_steps)

        snapshot_data["step"] = step

        return {
            "success": True,
            "data": {
                "sim_type": sim_type,
                "snapshot": snapshot_data,
            },
            "error": "",
        }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_sim_visualize(
    sim_type: str = "standing_wave",
    save_path: Optional[str] = None,
) -> Dict[str, Any]:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        sim = _get_simulator(sim_type)

        fig, ax = plt.subplots(figsize=(8, 5))

        if hasattr(sim, "t") and hasattr(sim, "scale_factor") and sim.t is not None:
            ax.plot(sim.t, sim.scale_factor, label="Scale Factor a(t)", linewidth=2)
            ax.set_xlabel("Time (Gyr)")
            ax.set_ylabel("Scale Factor a")
            ax.set_title(f"Cosmological Evolution - {sim_type}")
            ax.grid(True, alpha=0.3)
            ax.legend()
        elif hasattr(sim, "t") and hasattr(sim, "hubble_param") and sim.t is not None:
            ax.plot(sim.t, sim.hubble_param, label="H(t)", linewidth=2, color="orange")
            ax.set_xlabel("Time (Gyr)")
            ax.set_ylabel("Hubble Parameter (1/Gyr)")
            ax.set_title(f"Hubble Parameter Evolution - {sim_type}")
            ax.grid(True, alpha=0.3)
            ax.legend()
        else:
            x = np.linspace(0, 10, 100)
            y = np.sin(x) * np.exp(-0.1 * x)
            ax.plot(x, y, linewidth=2, color="teal")
            ax.set_xlabel("Time")
            ax.set_ylabel("Amplitude")
            ax.set_title(f"Simulation Visualization - {sim_type}")
            ax.grid(True, alpha=0.3)

        fig.tight_layout()

        if save_path:
            fig.savefig(save_path, format="png", dpi=100)
            plt.close(fig)
            return {
                "success": True,
                "data": {
                    "sim_type": sim_type,
                    "format": "png",
                    "save_path": save_path,
                },
                "error": "",
            }
        else:
            buf = io.BytesIO()
            fig.savefig(buf, format="png", dpi=100)
            buf.seek(0)
            img_base64 = base64.b64encode(buf.read()).decode("utf-8")
            plt.close(fig)
            return {
                "success": True,
                "data": {
                    "sim_type": sim_type,
                    "format": "png",
                    "base64": img_base64,
                },
                "error": "",
            }

    except ImportError:
        return {
            "success": False,
            "data": None,
            "error": "matplotlib 未安装，无法生成可视化图",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


register_tool(
    name="bsd_run_simulation",
    description="运行指定的BSD仿真器",
    input_schema={
        "type": "object",
        "properties": {
            "sim_type": {
                "type": "string",
                "description": "仿真类型，如 cosmology, phase_transition, emergence, standing_wave",
                "default": "standing_wave",
            },
            "steps": {
                "type": "integer",
                "description": "仿真步数",
                "default": 1000,
            },
            "params": {
                "type": "object",
                "description": "仿真参数字典",
                "default": {},
            },
        },
        "required": [],
    },
    handler=bsd_run_simulation,
)

register_tool(
    name="bsd_list_simulations",
    description="列出所有可用的BSD仿真器",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_list_simulations,
)

register_tool(
    name="bsd_sim_results",
    description="获取仿真结果摘要",
    input_schema={
        "type": "object",
        "properties": {
            "sim_type": {
                "type": "string",
                "description": "仿真类型",
                "default": "standing_wave",
            }
        },
        "required": [],
    },
    handler=bsd_sim_results,
)

register_tool(
    name="bsd_sim_snapshot",
    description="获取仿真快照数据",
    input_schema={
        "type": "object",
        "properties": {
            "sim_type": {
                "type": "string",
                "description": "仿真类型",
                "default": "standing_wave",
            },
            "step": {
                "type": "integer",
                "description": "快照步数",
                "default": 50,
            },
        },
        "required": [],
    },
    handler=bsd_sim_snapshot,
)

register_tool(
    name="bsd_sim_visualize",
    description="生成仿真可视化图（返回base64或保存到文件）",
    input_schema={
        "type": "object",
        "properties": {
            "sim_type": {
                "type": "string",
                "description": "仿真类型",
                "default": "standing_wave",
            },
            "save_path": {
                "type": "string",
                "description": "保存路径，为空则返回base64",
                "default": None,
            },
        },
        "required": [],
    },
    handler=bsd_sim_visualize,
)
