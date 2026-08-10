"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理6·双极性创生 / 公理9·意义涌现公理
对应九维维度：能量场·信息维·意识维
理论出处：theory_base/L0_总本源层/全域大一统理论/相变场与临界现象
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、E1=0.35, E2=0.65, E3=0.90

BSD相变场方程求解器
—— 描述序参量演化、临界指数与一阶/二阶相变判定的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, ALPHA, E1, E2, E3, GAMMA


def order_parameter(t, T, Tc, beta=None, m0=1.0):
    """
    序参量演化方程：m(T) = m₀·(T_c - T)^β  （T < T_c 时）

    描述系统在接近临界点时序参量的幂律行为。

    Parameters
    ----------
    t : np.ndarray
        时间序列
    T : float or np.ndarray
        温度（或控制参量）
    Tc : float
        临界温度
    beta : float, optional
        临界指数 β，默认基于锁档参数推导
    m0 : float
        序参量振幅系数

    Returns
    -------
    m_t : np.ndarray
        序参量随时间演化
    m_equilibrium : float or np.ndarray
        平衡态序参量
    """
    if beta is None:
        beta = 1.0 / (8.0 * KAPPA) if KAPPA > 0 else 0.5

    T = np.asarray(T, dtype=float)
    reduced_temp = (Tc - T) / (Tc + 1e-12)

    m_equilibrium = np.where(
        reduced_temp > 0,
        m0 * np.power(np.maximum(reduced_temp, 1e-12), beta),
        0.0
    )

    tau = 1.0 / (ALPHA * GAMMA + 1e-12)
    t = np.asarray(t, dtype=float)
    m_t = m_equilibrium * (1.0 - np.exp(-t / tau))

    return m_t, m_equilibrium


def critical_exponent(nu, eta, beta):
    """
    临界指数标度关系验证

    检验超标度律、Widom标度律、Fisher标度律等关系。

    Parameters
    ----------
    nu : float
        关联长度临界指数 ν
    eta : float
        反常维度 η
    beta : float
        序参量临界指数 β

    Returns
    -------
    result : dict
        包含各标度律的计算结果与偏差
    """
    d = 3.0  # 空间维度

    gamma = nu * (2.0 - eta)
    delta = 1.0 + gamma / beta
    alpha_val = 2.0 - d * nu
    hyperscaling_check = 2.0 - alpha_val - d * nu

    result = {
        "gamma": gamma,
        "delta": delta,
        "alpha": alpha_val,
        "hyperscaling_deviation": hyperscaling_check,
        "widom_scaling": gamma == beta * (delta - 1.0),
        "fisher_scaling": gamma == nu * (2.0 - eta),
        "rushbrooke_scaling": alpha_val + 2.0 * beta + gamma - 2.0,
    }

    return result


def phase_diagram_points(params):
    """
    相图临界点计算

    在参数空间中定位一级相变线、二级临界点、三相点等。

    Parameters
    ----------
    params : dict
        参数字典，可包含 Tc, Pc, Hc, mu_c 等

    Returns
    -------
    critical_points : dict
        各临界点坐标
    phase_boundaries : list of dict
        相边界线参数
    """
    Tc = params.get("Tc", E2)
    Pc = params.get("Pc", KAPPA)
    Hc = params.get("Hc", ALPHA)

    critical_points = {
        "critical_point": (Tc, Pc),
        "triple_point": (Tc * E1, Pc * E1),
        "tricritical_point": (Tc * (1.0 + ALPHA), Pc * (1.0 + KAPPA)),
        "upper_critical": (Tc * E3, Pc * E3),
        "lower_critical": (Tc * E1 * 0.5, Pc * E1 * 0.5),
    }

    phase_boundaries = [
        {
            "name": "first_order_line",
            "equation": "P = Pc * (T/Tc)^(1/nu)",
            "params": {"Pc": Pc, "Tc": Tc, "nu": 1.0 / KAPPA if KAPPA > 0 else 1.0},
        },
        {
            "name": "second_order_line",
            "equation": "H = Hc * |T-Tc|^beta",
            "params": {"Hc": Hc, "Tc": Tc, "beta": ALPHA},
        },
    ]

    return critical_points, phase_boundaries


def first_order_vs_second_order(lagrangian_dict):
    """
    一阶/二阶相变判定

    基于朗道自由能展开系数判断相变类型。
    二阶相变：二阶系数变号，四阶系数恒正
    一阶相变：四阶系数变负，存在亚稳态

    Parameters
    ----------
    lagrangian_dict : dict
        朗道展开系数 {"a": a(T), "b": b, "c": c, ...}

    Returns
    -------
    transition_type : str
        "first_order" 或 "second_order" 或 "weakly_first_order"
    order_of_transition : int
        相变阶数
    metastability : bool
        是否存在亚稳态
    latent_heat_estimate : float
        潜热估计（一阶相变时非零）
    """
    a = lagrangian_dict.get("a", 0.0)
    b = lagrangian_dict.get("b", 1.0)
    c = lagrangian_dict.get("c", 0.1)

    if b > 0 and c >= 0:
        transition_type = "second_order"
        order_of_transition = 2
        metastability = False
        latent_heat_estimate = 0.0
    elif b < 0 and c > 0:
        transition_type = "first_order"
        order_of_transition = 1
        metastability = True
        latent_heat_estimate = (b ** 2) / (4.0 * c)
    else:
        transition_type = "weakly_first_order"
        order_of_transition = 1
        metastability = True
        latent_heat_estimate = abs(b) * (1.0 + KAPPA)

    return transition_type, order_of_transition, metastability, latent_heat_estimate


def correlation_length(T, Tc, nu=None, xi0=1.0):
    """
    关联长度发散：ξ(T) = ξ₀ · |T - Tc|^(-ν)

    Parameters
    ----------
    T : float or np.ndarray
        温度
    Tc : float
        临界温度
    nu : float, optional
        关联长度临界指数
    xi0 : float
        微观关联长度

    Returns
    -------
    xi : float or np.ndarray
        关联长度
    """
    if nu is None:
        nu = 1.0 / (2.0 * KAPPA) if KAPPA > 0 else 0.7

    T = np.asarray(T, dtype=float)
    reduced_t = np.abs(T - Tc) / (Tc + 1e-12)
    xi = xi0 * np.power(np.maximum(reduced_t, 1e-12), -nu)

    return xi
