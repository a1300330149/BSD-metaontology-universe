"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理5·六系本源公理 / 公理12·命运双边界公理
对应九维维度：能量场·物质态·力用场
理论出处：theory_base/L0_总本源层/全域大一统理论/四大基本力统一
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD四大基本力统一方程求解器
—— 描述四力耦合守恒、质量间隙、六系映射与统一能标的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, ALPHA, E1, E2, E3, GAMMA


def coupling_conservation(g_s, g_e, g_w, g_g, g0=None):
    """
    四力耦合平方守恒：g_s² + g_e² + g_w² + g_g² = g₀²

    描述四大基本力耦合常数的统一守恒关系。

    Parameters
    ----------
    g_s : float
        强力耦合常数 g_s
    g_e : float
        电磁力耦合常数 g_e
    g_w : float
        弱力耦合常数 g_w
    g_g : float
        引力耦合常数 g_g
    g0 : float, optional
        统一耦合常数 g₀，默认基于锁档参数计算

    Returns
    -------
    total_coupling : float
        耦合平方和 Σ g_i²
    g0_expected : float
        期望统一耦合常数 g₀
    deviation : float
        偏差 (Σ g_i² - g₀²) / g₀²
    normalized : dict
        归一化的各力耦合强度
    """
    if g0 is None:
        g0 = np.sqrt(E1 ** 2 + E2 ** 2 + E3 ** 2 + KAPPA ** 2)

    total_coupling = g_s ** 2 + g_e ** 2 + g_w ** 2 + g_g ** 2
    deviation = (total_coupling - g0 ** 2) / (g0 ** 2 + 1e-12)

    total = np.sqrt(total_coupling) + 1e-12
    normalized = {
        "strong": g_s / total,
        "electromagnetic": g_e / total,
        "weak": g_w / total,
        "gravity": g_g / total,
    }

    return total_coupling, g0, deviation, normalized


def mass_gap(kappa=None, alpha=None, scale=1.0):
    """
    杨-米尔斯质量间隙：Δm > κ · α · Λ

    表述非阿贝尔规范场理论中的质量间隙存在性。

    Parameters
    ----------
    kappa : float, optional
        κ系数，默认使用锁档 KAPPA
    alpha : float, optional
        α系数，默认使用锁档 ALPHA
    scale : float
        能标 Λ（质量尺度）

    Returns
    -------
    mass_gap_lower : float
        质量间隙下界 Δm_min = κ·α·Λ
    mass_gap_upper : float
        质量间隙上界估计
    dimensionless_gap : float
        无量纲质量间隙 Δm/Λ
    confinement_scale : float
        禁闭尺度 Λ_QCD 估计
    """
    if kappa is None:
        kappa = KAPPA
    if alpha is None:
        alpha = ALPHA

    mass_gap_lower = kappa * alpha * scale
    mass_gap_upper = kappa * scale
    dimensionless_gap = mass_gap_lower / (scale + 1e-12)

    confinement_scale = scale * np.exp(-2.0 * np.pi / (alpha * kappa + 1e-12))

    return mass_gap_lower, mass_gap_upper, dimensionless_gap, confinement_scale


def force_mapping_six_systems():
    """
    六系-四力映射表

    BSD六系统与四大基本力之间的对应映射关系。

    Returns
    -------
    mapping_matrix : np.ndarray
        6×4 映射矩阵 M[六系, 四力]
    six_system_names : list
        六系名称
    four_force_names : list
        四力名称
    mapping_strength : dict
        各六系的四力主导分配
    """
    six_system_names = ["天", "地", "人", "神", "鬼", "怪"]
    four_force_names = ["strong", "electromagnetic", "weak", "gravity"]

    mapping_matrix = np.array([
        [0.10, 0.70, 0.10, 0.10],
        [0.15, 0.15, 0.10, 0.60],
        [0.20, 0.30, 0.30, 0.20],
        [0.05, 0.50, 0.40, 0.05],
        [0.40, 0.10, 0.40, 0.10],
        [0.60, 0.05, 0.25, 0.10],
    ])

    mapping_strength = {}
    for i, sys_name in enumerate(six_system_names):
        dominant_idx = np.argmax(mapping_matrix[i])
        mapping_strength[sys_name] = {
            "dominant_force": four_force_names[dominant_idx],
            "dominant_strength": mapping_matrix[i, dominant_idx],
            "distribution": dict(zip(four_force_names, mapping_matrix[i])),
        }

    return mapping_matrix, six_system_names, four_force_names, mapping_strength


def unification_energy_scale(force_name, base_scale=1.0):
    """
    各力统一能标计算

    基于耦合常数跑动估计各力的统一能标。

    Parameters
    ----------
    force_name : str
        力名称 ("strong", "electromagnetic", "weak", "gravity", "electroweak", "grand", "total")
    base_scale : float
        基准能标（电弱标度约246GeV）

    Returns
    -------
    energy_scale : float
        统一能标（以base_scale为单位）
    coupling_at_unification : float
        统一点的耦合常数
    hierarchy_ratio : float
        等级比（基准能标/统一能标）
    """
    force_name = force_name.lower()

    scales = {
        "electroweak": 1.0,
        "strong": 1.0 / (ALPHA + 1e-12),
        "weak": GAMMA / (ALPHA + 1e-12),
        "electromagnetic": GAMMA,
        "grand": 1.0 / (ALPHA * KAPPA + 1e-12),
        "gravity": 1.0 / (KAPPA ** 2 + 1e-12),
        "total": 1.0 / (ALPHA * KAPPA ** 2 + 1e-12),
    }

    couplings = {
        "electroweak": np.sqrt(ALPHA),
        "strong": KAPPA,
        "weak": ALPHA,
        "electromagnetic": ALPHA * GAMMA,
        "grand": KAPPA * GAMMA,
        "gravity": KAPPA ** 2,
        "total": ALPHA * KAPPA,
    }

    if force_name not in scales:
        raise ValueError(f"未知力名称: {force_name}。可选: {list(scales.keys())}")

    energy_scale = base_scale * scales[force_name]
    coupling_at_unification = couplings[force_name]
    hierarchy_ratio = base_scale / (energy_scale + 1e-12)

    return energy_scale, coupling_at_unification, hierarchy_ratio


def running_coupling(energy_scale, g0, scale0=1.0, beta0=None):
    """
    耦合常数跑动：g(μ) = g₀ / (1 + β₀·g₀²·ln(μ/μ₀))

    Parameters
    ----------
    energy_scale : float or np.ndarray
        跑动能标 μ
    g0 : float
        基准耦合常数 g(μ₀)
    scale0 : float
        基准能标 μ₀
    beta0 : float, optional
        β函数一阶系数

    Returns
    -------
    g_running : float or np.ndarray
        跑动耦合常数 g(μ)
    alpha_running : float or np.ndarray
        跑动精细结构常数 α = g²/(4π)
    """
    if beta0 is None:
        beta0 = -KAPPA / (4.0 * np.pi)

    energy_scale = np.asarray(energy_scale, dtype=float)
    log_ratio = np.log(energy_scale / (scale0 + 1e-12) + 1e-12)

    denominator = 1.0 + beta0 * g0 ** 2 * log_ratio
    g_running = g0 / np.sqrt(np.maximum(denominator, 1e-12))
    alpha_running = g_running ** 2 / (4.0 * np.pi)

    return g_running, alpha_running
