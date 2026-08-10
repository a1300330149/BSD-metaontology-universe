"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理8·意义守恒公理 / 公理10·闭递归公理
对应九维维度：熵流维·时间流·命运维
理论出处：theory_base/L0_总本源层/全域大一统理论/全域熵流方程
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD全域熵流方程求解器
—— 描述熵产生、不可逆耗散、熵驻留与三档预警的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, GAMMA, ALPHA, E1, E2, E3


def entropy_flow(dS_dt, sigma, k=None, dPhi_dt=0.0):
    """
    全域熵流方程：dS/dt = σ - k · dΦ/dt

    描述系统熵变率 = 内部熵产生 - 负熵流输入。

    Parameters
    ----------
    dS_dt : float or np.ndarray
        系统熵变率 dS/dt
    sigma : float or np.ndarray
        内部熵产生率 σ
    k : float, optional
        负熵流耦合系数 k，默认使用锁档 ALPHA
    dPhi_dt : float or np.ndarray
        外部势流率 dΦ/dt

    Returns
    -------
    residual : float or np.ndarray
        方程残差 dS/dt - σ + k·dΦ/dt
    entropy_production : float or np.ndarray
        熵产生项 σ
    negentropy_flow : float or np.ndarray
        负熵流项 k·dΦ/dt
    balance_type : str
        熵平衡类型 ("producing", "consuming", "balanced")
    """
    if k is None:
        k = ALPHA

    entropy_production = sigma
    negentropy_flow = k * dPhi_dt
    residual = dS_dt - sigma + negentropy_flow

    if np.asarray(dS_dt).size == 1:
        if dS_dt > 1e-6:
            balance_type = "producing"
        elif dS_dt < -1e-6:
            balance_type = "consuming"
        else:
            balance_type = "balanced"
    else:
        balance_type = "array"

    return residual, entropy_production, negentropy_flow, balance_type


def irreversible_dissipation(t_n, sigma):
    """
    不可逆耗散熵：ΔS_NP = ∫₀^{t_n} σ(t) dt

    计算从0到t_n时刻的总不可逆熵产生。

    Parameters
    ----------
    t_n : float or np.ndarray
        时间点或时间序列
    sigma : float or np.ndarray
        熵产生率 σ(t)（标量或时间序列）

    Returns
    -------
    delta_S_NP : float or np.ndarray
        不可逆耗散熵 ΔS_NP
    cumulative_sigma : np.ndarray
        累积熵产生曲线
    time_points : np.ndarray
        时间采样点
    """
    if np.isscalar(t_n):
        if np.isscalar(sigma):
            delta_S_NP = sigma * t_n
            time_points = np.linspace(0, t_n, 100)
            cumulative_sigma = sigma * time_points
        else:
            raise ValueError("t_n为标量时，sigma也必须为标量")
    else:
        t_n = np.asarray(t_n, dtype=float)
        sigma = np.asarray(sigma, dtype=float)
        delta_S_NP = np.trapezoid(sigma, t_n)
        cumulative_sigma = np.zeros_like(t_n)
        for i in range(1, len(t_n)):
            cumulative_sigma[i] = cumulative_sigma[i - 1] + 0.5 * (sigma[i] + sigma[i - 1]) * (t_n[i] - t_n[i - 1])
        time_points = t_n

    return delta_S_NP, cumulative_sigma, time_points


def entropy_residence(E_total, E_out_outer, E_out_buffer):
    """
    熵驻留能量：E_res = E_total - E_out外 - E_out缓冲

    计算系统内驻留的有效能量（未被耗散的能量）。

    Parameters
    ----------
    E_total : float or np.ndarray
        总能量 E_total
    E_out_outer : float or np.ndarray
        外层输出能量 E_out外
    E_out_buffer : float or np.ndarray
        缓冲层输出能量 E_out缓冲

    Returns
    -------
    E_res : float or np.ndarray
        驻留能量 E_res
    residence_ratio : float or np.ndarray
        驻留率 E_res / E_total
    dissipation_ratio : float or np.ndarray
        耗散率 (E_out外 + E_out缓冲) / E_total
    buffer_efficiency : float or np.ndarray
        缓冲效率 = 缓冲层输出 / 外层输出
    """
    E_res = E_total - E_out_outer - E_out_buffer
    residence_ratio = E_res / (E_total + 1e-12)
    dissipation_ratio = (E_out_outer + E_out_buffer) / (E_total + 1e-12)
    buffer_efficiency = E_out_buffer / (E_out_outer + 1e-12)

    return E_res, residence_ratio, dissipation_ratio, buffer_efficiency


def entropy_warning_level(E_res_ratio):
    """
    熵驻留三档预警系统

    三档阈值：
    - 绿色安全：E_res_ratio > 0.40
    - 黄色预警：0.25 < E_res_ratio ≤ 0.40
    - 橙色警戒：0.02 < E_res_ratio ≤ 0.25
    - 红色危险：E_res_ratio ≤ 0.02

    Parameters
    ----------
    E_res_ratio : float or np.ndarray
        熵驻留率（0~1之间）

    Returns
    -------
    warning_level : str or list
        预警等级 ("green", "yellow", "orange", "red")
    level_index : int or np.ndarray
        预警等级编号 (3=green, 2=yellow, 1=orange, 0=red)
    description : str or list
        文字描述
    """
    thresholds = {
        "green": 0.40,
        "yellow": 0.25,
        "orange": 0.02,
    }

    descriptions = {
        "green": "安全状态 - 系统能量充沛，运行稳定",
        "yellow": "预警状态 - 注意能量损耗，优化效率",
        "orange": "警戒状态 - 能量不足，需补充负熵流",
        "red": "危险状态 - 系统即将热寂，紧急干预",
    }

    if np.isscalar(E_res_ratio):
        if E_res_ratio > thresholds["green"]:
            level = "green"
            idx = 3
        elif E_res_ratio > thresholds["yellow"]:
            level = "yellow"
            idx = 2
        elif E_res_ratio > thresholds["orange"]:
            level = "orange"
            idx = 1
        else:
            level = "red"
            idx = 0
        return level, idx, descriptions[level]
    else:
        E_res_ratio = np.asarray(E_res_ratio, dtype=float)
        levels = []
        indices = np.zeros_like(E_res_ratio, dtype=int)
        descs = []

        for i, r in enumerate(E_res_ratio):
            if r > thresholds["green"]:
                levels.append("green")
                indices[i] = 3
                descs.append(descriptions["green"])
            elif r > thresholds["yellow"]:
                levels.append("yellow")
                indices[i] = 2
                descs.append(descriptions["yellow"])
            elif r > thresholds["orange"]:
                levels.append("orange")
                indices[i] = 1
                descs.append(descriptions["orange"])
            else:
                levels.append("red")
                indices[i] = 0
                descs.append(descriptions["red"])

        return levels, indices, descs


def entropy_production_rate(flow, force, kappa=None):
    """
    熵产生率的线性不可逆热力学：σ = J · X = L · X²

    其中 J 是流，X 是力，L 是Onsager系数。

    Parameters
    ----------
    flow : float or np.ndarray
        热力学流 J
    force : float or np.ndarray
        热力学力 X
    kappa : float, optional
        唯象系数 L 中的κ修正

    Returns
    -------
    sigma : float or np.ndarray
        熵产生率 σ
    onsager_coeff : float or np.ndarray
        Onsager系数 L = J / (X + ε)
    efficiency : float or np.ndarray
        热力学效率 η = 输出功率 / 输入功率
    """
    if kappa is None:
        kappa = KAPPA

    sigma = flow * force
    onsager_coeff = flow / (force + 1e-12)

    eff_denom = flow * force + (1.0 - kappa) * np.abs(flow * force)
    efficiency = kappa * np.abs(flow * force) / (eff_denom + 1e-12)

    return sigma, onsager_coeff, efficiency
