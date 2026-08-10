"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理7·九维涌现公理 / 公理10·闭包递归公理
对应九维维度：能量场·信息维·意识维·物质维·时空维
理论出处：theory_base/L0_总本源层/全域大一统理论/稳态势场与吸引子理论
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD稳态势母方程求解器
—— 描述势函数Φ(t)演化、稳态判据、吸引子分析与生命三权动态均衡的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E1, E2, E3


def steady_potential(t, Phi0, gamma=None, kappa=None):
    """
    稳态势母方程：Φ(t) = Φ₀ · exp(-γ·t) · cos(κ·t) + Φ₀·(1-exp(-γ·t))

    描述势函数随时间的阻尼振荡演化，最终收敛到稳态值。

    Parameters
    ----------
    t : np.ndarray
        时间序列
    Phi0 : float
        初始势幅值
    gamma : float, optional
        衰减系数γ，默认使用锁档参数GAMMA
    kappa : float, optional
        振荡频率κ，默认使用锁档参数KAPPA

    Returns
    -------
    Phi_t : np.ndarray
        势函数Φ(t)随时间演化
    dPhi_dt : np.ndarray
        一阶导数dΦ/dt
    d2Phi_dt2 : np.ndarray
        二阶导数d²Φ/dt²
    """
    if gamma is None:
        gamma = GAMMA
    if kappa is None:
        kappa = KAPPA

    t = np.asarray(t, dtype=float)
    exp_term = np.exp(-gamma * t)
    cos_term = np.cos(kappa * t)
    sin_term = np.sin(kappa * t)

    Phi_t = Phi0 * exp_term * cos_term + Phi0 * (1.0 - exp_term)

    dPhi_dt = Phi0 * (-gamma * exp_term * cos_term - kappa * exp_term * sin_term + gamma * exp_term)

    d2Phi_dt2 = Phi0 * (
        gamma**2 * exp_term * cos_term
        + 2.0 * gamma * kappa * exp_term * sin_term
        - kappa**2 * exp_term * cos_term
        - gamma**2 * exp_term
    )

    return Phi_t, dPhi_dt, d2Phi_dt2


def potential_minimum(params):
    """
    稳态势极小值计算

    基于朗道型势函数 V(Φ) = a·Φ² + b·Φ⁴ + c·Φ⁶ 计算极小值位置。

    Parameters
    ----------
    params : dict
        参数字典，可包含 a, b, c 等势函数系数

    Returns
    -------
    minima : np.ndarray
        极小值位置数组
    minimum_values : np.ndarray
        极小值对应的势函数值
    stability : np.ndarray
        各极小值的稳定性（二阶导数>0为稳定）
    """
    a = params.get("a", -KAPPA)
    b = params.get("b", 1.0)
    c = params.get("c", ALPHA * 0.1)

    phi_vals = np.linspace(-2.0, 2.0, 10000)
    V = a * phi_vals**2 + b * phi_vals**4 + c * phi_vals**6

    dV_dphi = 2.0 * a * phi_vals + 4.0 * b * phi_vals**3 + 6.0 * c * phi_vals**5
    d2V_dphi2 = 2.0 * a + 12.0 * b * phi_vals**2 + 30.0 * c * phi_vals**4

    sign_changes = np.where(np.diff(np.sign(dV_dphi)))[0]
    candidate_indices = []
    for idx in sign_changes:
        if dV_dphi[idx] >= 0 and dV_dphi[idx + 1] <= 0:
            continue
        candidate_indices.append(idx + 1)

    if len(candidate_indices) == 0:
        candidate_indices = [np.argmin(V)]

    minima = phi_vals[candidate_indices]
    minimum_values = V[candidate_indices]
    stability = d2V_dphi2[candidate_indices] > 0

    return minima, minimum_values, stability


def stability_criterion(dPhi_dt, d2Phi_dt2):
    """
    稳态判据：Lyapunov稳定性分析

    基于李雅普诺夫稳定性理论判断系统稳态：
    - 渐近稳定：dΦ/dt → 0 且 d²Φ/dt² > 0
    - 临界稳定：dΦ/dt → 0 且 d²Φ/dt² = 0
    - 不稳定：dΦ/dt 发散 或 d²Φ/dt² < 0

    Parameters
    ----------
    dPhi_dt : np.ndarray
        势函数一阶导数
    d2Phi_dt2 : np.ndarray
        势函数二阶导数

    Returns
    -------
    stability_type : str
        稳定性类型："asymptotically_stable" / "critically_stable" / "unstable"
    stability_index : float
        稳定性指数（正值越大越稳定）
    convergence_rate : float
        收敛速率估计
    """
    dPhi_dt = np.asarray(dPhi_dt, dtype=float)
    d2Phi_dt2 = np.asarray(d2Phi_dt2, dtype=float)

    final_dPhi = np.mean(dPhi_dt[-max(1, len(dPhi_dt) // 10) :])
    final_d2Phi = np.mean(d2Phi_dt2[-max(1, len(d2Phi_dt2) // 10) :])

    abs_final_dPhi = np.abs(final_dPhi)

    if abs_final_dPhi < 1e-6 and final_d2Phi > 1e-6:
        stability_type = "asymptotically_stable"
    elif abs_final_dPhi < 1e-6 and abs(final_d2Phi) <= 1e-6:
        stability_type = "critically_stable"
    else:
        stability_type = "unstable"

    stability_index = final_d2Phi / (abs_final_dPhi + 1e-12)

    if len(dPhi_dt) > 1:
        t_half = len(dPhi_dt) // 2
        first_half = np.mean(np.abs(dPhi_dt[:t_half]))
        second_half = np.mean(np.abs(dPhi_dt[t_half:]))
        convergence_rate = first_half / (second_half + 1e-12)
    else:
        convergence_rate = 0.0

    return stability_type, stability_index, convergence_rate


def life_steady_state(alpha1, alpha2, alpha3, tau=None):
    """
    生命稳态判据：三权动态均衡 α∈[0.3, 0.4]

    基于BSD三元权重归一化理论，判断生命系统是否处于健康稳态：
    - α₁ + α₂ + α₃ = 1
    - 健康态：每个α ∈ [0.30, 0.40] 且权重差 ≤ 0.05

    Parameters
    ----------
    alpha1 : float or np.ndarray
        第一权系数（如：物质/肉身）
    alpha2 : float or np.ndarray
        第二权系数（如：精神/意识）
    alpha3 : float or np.ndarray
        第三权系数（如：道心/本源）
    tau : float, optional
        时间常数，默认基于锁档参数推导

    Returns
    -------
    is_steady : bool or np.ndarray
        是否处于生命稳态
    steady_level : str or np.ndarray
        稳态等级："health" / "sub_health" / "disease"
    balance_index : float or np.ndarray
        均衡指数（0-1，越高越均衡）
    """
    from bsd_engine.registry.constants import (
        HEALTH_ALPHA_MIN,
        HEALTH_ALPHA_MAX,
        HEALTH_ALPHA_DIFF_MAX,
        SUB_HEALTH_ALPHA_DIFF,
    )

    if tau is None:
        tau = 1.0 / (GAMMA * KAPPA + 1e-12)

    alpha1 = np.asarray(alpha1, dtype=float)
    alpha2 = np.asarray(alpha2, dtype=float)
    alpha3 = np.asarray(alpha3, dtype=float)

    total = alpha1 + alpha2 + alpha3
    alpha1_norm = alpha1 / (total + 1e-12)
    alpha2_norm = alpha2 / (total + 1e-12)
    alpha3_norm = alpha3 / (total + 1e-12)

    in_range = (
        (alpha1_norm >= HEALTH_ALPHA_MIN)
        & (alpha1_norm <= HEALTH_ALPHA_MAX)
        & (alpha2_norm >= HEALTH_ALPHA_MIN)
        & (alpha2_norm <= HEALTH_ALPHA_MAX)
        & (alpha3_norm >= HEALTH_ALPHA_MIN)
        & (alpha3_norm <= HEALTH_ALPHA_MAX)
    )

    max_diff = np.maximum(
        np.abs(alpha1_norm - alpha2_norm),
        np.maximum(np.abs(alpha2_norm - alpha3_norm), np.abs(alpha1_norm - alpha3_norm)),
    )

    is_steady = in_range & (max_diff <= HEALTH_ALPHA_DIFF_MAX)

    steady_level = np.where(
        is_steady,
        "health",
        np.where(max_diff <= SUB_HEALTH_ALPHA_DIFF, "sub_health", "disease"),
    )

    ideal = 1.0 / 3.0
    deviations = np.abs(alpha1_norm - ideal) + np.abs(alpha2_norm - ideal) + np.abs(alpha3_norm - ideal)
    balance_index = np.maximum(0.0, 1.0 - deviations / (2.0 / 3.0))

    return is_steady, steady_level, balance_index


def phase_attractor(Phi):
    """
    稳态势吸引子分析

    分析势函数Φ在相空间中的吸引子类型与特性：
    - 定点吸引子（稳态）
    - 极限环吸引子（周期振荡）
    - 奇异吸引子（混沌）

    Parameters
    ----------
    Phi : np.ndarray
        势函数时间序列

    Returns
    -------
    attractor_type : str
        吸引子类型："fixed_point" / "limit_cycle" / "strange_attractor"
    attractor_dimension : float
        吸引子维数估计（关联维数）
    lyapunov_exponent : float
        最大李雅普诺夫指数估计
    basin_of_attraction : float
        吸引盆估计大小
    """
    Phi = np.asarray(Phi, dtype=float)
    n = len(Phi)

    if n < 10:
        return "insufficient_data", 0.0, 0.0, 0.0

    final_segment = Phi[-max(1, n // 5) :]
    amplitude = np.max(final_segment) - np.min(final_segment)
    mean_val = np.mean(final_segment)

    if amplitude < 1e-6 * (np.abs(mean_val) + 1e-12):
        attractor_type = "fixed_point"
    elif amplitude > 1e-3:
        diff = np.diff(final_segment)
        zero_crossings = np.sum(np.diff(np.sign(diff)) != 0)
        if zero_crossings > len(final_segment) * 0.1:
            attractor_type = "strange_attractor"
        else:
            attractor_type = "limit_cycle"
    else:
        attractor_type = "fixed_point"

    if n > 20:
        m = 3
        tau_lag = max(1, n // 20)
        embedded = np.array([Phi[i : n - (m - 1) * tau_lag + i : tau_lag] for i in range(m)])
        embedded = embedded.T

        n_pts = len(embedded)
        if n_pts > 10:
            r_vals = np.logspace(-4, 0, 20)
            C_r = np.zeros(len(r_vals))

            for i, r in enumerate(r_vals):
                count = 0
                for j in range(n_pts):
                    dists = np.linalg.norm(embedded - embedded[j], axis=1)
                    count += np.sum(dists < r) - 1
                C_r[i] = count / (n_pts * (n_pts - 1))

            valid = C_r > 0
            if np.sum(valid) > 2:
                log_r = np.log(r_vals[valid])
                log_C = np.log(C_r[valid])
                coeffs = np.polyfit(log_r, log_C, 1)
                attractor_dimension = coeffs[0]
            else:
                attractor_dimension = 1.0
        else:
            attractor_dimension = 1.0
    else:
        attractor_dimension = 1.0

    if n > 30:
        dPhi = np.diff(Phi)
        if np.std(dPhi) > 1e-12:
            lyapunov_exponent = np.mean(np.log(np.abs(dPhi[1:] / (dPhi[:-1] + 1e-12)) + 1e-12))
        else:
            lyapunov_exponent = -np.inf
    else:
        lyapunov_exponent = -np.inf

    basin_of_attraction = np.ptp(Phi) / (np.std(Phi) + 1e-12)

    return attractor_type, attractor_dimension, lyapunov_exponent, basin_of_attraction
