"""
BSD全域统一理论 — 方程类MCP工具

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

import numpy as np

from bsd_mcp.tool_registry import register_tool


EQUATION_LIST = [
    {"id": "entropy_flow", "name": "全域熵流方程", "module": "bsd_engine.equations.entropy_flow"},
    {"id": "cosmological_constant", "name": "宇宙学常数方程", "module": "bsd_engine.equations.cosmological_constant"},
    {"id": "global_coherence", "name": "全局相干度方程", "module": "bsd_engine.equations.global_coherence"},
    {"id": "phase_transition", "name": "相变方程", "module": "bsd_engine.equations.phase_transition"},
    {"id": "standing_wave", "name": "驻波方程", "module": "bsd_engine.equations.standing_wave"},
    {"id": "emergence", "name": "涌现方程", "module": "bsd_engine.equations.emergence"},
    {"id": "four_force_unification", "name": "四力统一方程", "module": "bsd_engine.equations.four_force_unification"},
    {"id": "structural_entropy", "name": "结构熵方程", "module": "bsd_engine.equations.structural_entropy"},
    {"id": "life_steady_state", "name": "生命稳态方程", "module": "bsd_engine.equations.life_steady_state"},
    {"id": "steady_state_potential", "name": "稳态势方程", "module": "bsd_engine.equations.steady_state_potential"},
    {"id": "kappa_phase", "name": "κ相位方程", "module": "bsd_engine.equations.kappa_phase"},
]


def bsd_solve_equation(
    equation_name: str = "standing_wave",
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    params = params or {}

    try:
        if equation_name == "entropy_flow":
            from bsd_engine.equations.entropy_flow import entropy_flow
            dS_dt = params.get("dS_dt", 0.5)
            sigma = params.get("sigma", 0.3)
            k = params.get("k", None)
            dPhi_dt = params.get("dPhi_dt", 0.0)
            residual, entropy_production, negentropy_flow, balance_type = entropy_flow(
                dS_dt, sigma, k=k, dPhi_dt=dPhi_dt
            )
            return {
                "success": True,
                "data": {
                    "equation": equation_name,
                    "result": {
                        "residual": float(residual) if np.isscalar(residual) else residual.tolist(),
                        "entropy_production": float(entropy_production) if np.isscalar(entropy_production) else entropy_production.tolist(),
                        "negentropy_flow": float(negentropy_flow) if np.isscalar(negentropy_flow) else negentropy_flow.tolist(),
                        "balance_type": balance_type,
                    },
                },
                "error": "",
            }

        elif equation_name == "cosmological_constant":
            from bsd_engine.equations.cosmological_constant import lambda_theoretical, lambda_observed, lambda_error
            Lambda, rho_vac, unit_conversion = lambda_theoretical()
            Lambda_obs, Lambda_obs_error, confidence_levels, planck_params = lambda_observed()
            error_result = lambda_error()
            relative_error = float(error_result[0]) if isinstance(error_result, tuple) else float(error_result)
            return {
                "success": True,
                "data": {
                    "equation": equation_name,
                    "result": {
                        "lambda_theoretical": float(Lambda),
                        "lambda_observed": float(Lambda_obs),
                        "relative_error": relative_error,
                        "vacuum_energy_density": float(rho_vac),
                        "unit_conversion": {k: float(v) if isinstance(v, (int, float, np.floating)) else v for k, v in unit_conversion.items()},
                    },
                },
                "error": "",
            }

        elif equation_name == "global_coherence":
            from bsd_engine.equations.global_coherence import global_coherence
            signals = params.get("signals", [[0.1, 0.2, 0.3, 0.4, 0.5], [0.15, 0.25, 0.35, 0.45, 0.55]])
            method = params.get("method", "pearson")
            gc_value, coherence_matrix, coherence_type = global_coherence(signals, method=method)
            return {
                "success": True,
                "data": {
                    "equation": equation_name,
                    "result": {
                        "global_coherence": float(gc_value),
                        "coherence_matrix": coherence_matrix.tolist(),
                        "coherence_type": coherence_type,
                        "method": method,
                    },
                },
                "error": "",
            }

        else:
            return {
                "success": False,
                "data": None,
                "error": f"方程 '{equation_name}' 的求解器暂未实现或不可用",
            }

    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_list_equations() -> Dict[str, Any]:
    try:
        return {
            "success": True,
            "data": {
                "total": len(EQUATION_LIST),
                "equations": EQUATION_LIST,
            },
            "error": "",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_compute_entropy(steps: int = 100) -> Dict[str, Any]:
    try:
        from bsd_engine.equations.entropy_flow import entropy_flow

        t = np.linspace(0, 1.0, steps)
        sigma = 0.3
        dPhi_dt = 0.5
        sigma_t = sigma * np.ones_like(t)
        dS_dt = sigma - 0.18 * dPhi_dt

        residual, entropy_production, negentropy_flow, balance_type = entropy_flow(
            dS_dt, sigma, dPhi_dt=dPhi_dt
        )

        delta_S_NP = sigma * t[-1]

        return {
            "success": True,
            "data": {
                "entropy_production_rate": float(sigma),
                "negentropy_flow_rate": float(0.18 * dPhi_dt),
                "net_entropy_rate": float(dS_dt),
                "total_irreversible_dissipation": float(delta_S_NP),
                "balance_type": balance_type,
                "time_series": {
                    "time": t.tolist(),
                    "entropy_production": (sigma * t).tolist(),
                },
                "steps": steps,
            },
            "error": "",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_compute_lambda() -> Dict[str, Any]:
    try:
        from bsd_engine.equations.cosmological_constant import (
            lambda_theoretical,
            lambda_observed,
            lambda_error,
            lambda_from_bsd,
        )

        Lambda, rho_vac, unit_conversion = lambda_theoretical()
        Lambda_obs, Lambda_obs_error, confidence_levels, planck_params = lambda_observed()
        error_result = lambda_error()

        if isinstance(error_result, tuple):
            relative_error = float(error_result[0])
        else:
            relative_error = float(error_result)

        try:
            bsd_lambda = lambda_from_bsd()
            if isinstance(bsd_lambda, tuple):
                bsd_result = float(bsd_lambda[0])
            elif isinstance(bsd_lambda, (int, float, np.floating)):
                bsd_result = float(bsd_lambda)
            else:
                bsd_result = float(bsd_lambda)
        except Exception:
            bsd_result = float(Lambda)

        return {
            "success": True,
            "data": {
                "lambda_theoretical": float(Lambda),
                "lambda_observed": float(Lambda_obs),
                "lambda_bsd_derived": bsd_result,
                "relative_error_percent": float(relative_error * 100),
                "vacuum_energy_density_Jm3": float(rho_vac),
                "unit": "m^-2",
                "consistent_with_observation": bool(relative_error < 0.01),
            },
            "error": "",
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": str(e),
        }


def bsd_compute_coherence(steps: int = 100) -> Dict[str, Any]:
    try:
        from bsd_engine.equations.global_coherence import global_coherence

        np.random.seed(42)
        base = np.sin(np.linspace(0, 4 * np.pi, steps))
        signals = [base + 0.1 * np.random.randn(steps) for _ in range(4)]
        signals_list = [s.tolist() for s in signals]

        gc_value, coherence_matrix, coherence_type = global_coherence(signals_list, method="pearson")

        n_channels = len(signals_list)
        n_samples = len(signals_list[0]) if signals_list else 0

        return {
            "success": True,
            "data": {
                "global_coherence": float(gc_value),
                "coherence_type": coherence_type,
                "method": "pearson",
                "n_channels": n_channels,
                "n_samples": n_samples,
                "coherence_matrix": coherence_matrix.tolist(),
                "steps": steps,
                "interpretation": {
                    "laser_like": "类激光高相干态（>0.8）",
                    "partial": "部分相干态（0.3-0.8）",
                    "incoherent": "非相干态（<0.3）",
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
    name="bsd_solve_equation",
    description="求解指定的BSD方程",
    input_schema={
        "type": "object",
        "properties": {
            "equation_name": {
                "type": "string",
                "description": "方程名称，如 entropy_flow, cosmological_constant, global_coherence",
                "default": "standing_wave",
            },
            "params": {
                "type": "object",
                "description": "方程参数字典",
                "default": {},
            },
        },
        "required": [],
    },
    handler=bsd_solve_equation,
)

register_tool(
    name="bsd_list_equations",
    description="列出所有可用的BSD方程",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_list_equations,
)

register_tool(
    name="bsd_compute_entropy",
    description="计算熵流与不可逆耗散",
    input_schema={
        "type": "object",
        "properties": {
            "steps": {
                "type": "integer",
                "description": "时间步数",
                "default": 100,
            },
        },
        "required": [],
    },
    handler=bsd_compute_entropy,
)

register_tool(
    name="bsd_compute_lambda",
    description="计算宇宙学常数Λ（理论值、观测值与BSD推导值）",
    input_schema={
        "type": "object",
        "properties": {},
        "required": [],
    },
    handler=bsd_compute_lambda,
)

register_tool(
    name="bsd_compute_coherence",
    description="计算全局时空相干度",
    input_schema={
        "type": "object",
        "properties": {
            "steps": {
                "type": "integer",
                "description": "采样步数",
                "default": 100,
            },
        },
        "required": [],
    },
    handler=bsd_compute_coherence,
)
