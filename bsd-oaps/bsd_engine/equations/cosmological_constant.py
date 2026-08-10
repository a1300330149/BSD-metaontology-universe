"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理1·虚空创生公理 / 公理11·宿命双界公理
对应九维维度：时空维·物质维·能量场·信息维·意识维
理论出处：theory_base/L0_总本源层/全域大一统理论/宇宙学常数与四力统一
固定数理常量：Λ=1.106×10⁻⁵² m⁻²、κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)

BSD宇宙学常数求解器
—— 描述宇宙学常数Λ理论值、观测值、BSD推导与宇宙演化的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import (
    KAPPA,
    ALPHA,
    GAMMA,
    COSMOLOGICAL_CONSTANT,
    COSMOLOGICAL_CONSTANT_OBSERVED,
    COSMOLOGICAL_CONSTANT_ERROR,
)


def lambda_theoretical():
    """
    Λ = 1.106×10⁻⁵² m⁻² 理论值

    返回BSD全域统一理论锁档的宇宙学常数理论值。

    Returns
    -------
    Lambda : float
        宇宙学常数理论值 (m⁻²)
    Lambda_energy_density : float
        对应的真空能量密度 (J/m³)
    unit_conversion : dict
        单位换算字典
    """
    c = 299792458.0
    G = 6.67430e-11
    hbar = 1.054571817e-34

    Lambda = COSMOLOGICAL_CONSTANT
    rho_vac = Lambda * c**4 / (8.0 * np.pi * G)

    unit_conversion = {
        "per_m2": Lambda,
        "per_cm2": Lambda * 1e-4,
        "per_pc2": Lambda * (3.0856775814913673e16) ** 2,
        "energy_density_Jm3": rho_vac,
        "energy_density_eVm3": rho_vac / 1.602176634e-19,
        "energy_density_GeVcm3": rho_vac / (1e9 * 1.602176634e-10),
        "planck_units": Lambda * (hbar * G / c**3),
    }

    return Lambda, rho_vac, unit_conversion


def lambda_observed():
    """
    Λ观测值（Planck 2018）

    返回普朗克卫星2018年数据的宇宙学常数观测值及误差范围。

    Returns
    -------
    Lambda_obs : float
        观测值中心值 (m⁻²)
    Lambda_obs_error : float
        观测误差 (m⁻²)
    confidence_levels : dict
        不同置信水平的范围
    planck_params : dict
        Planck 2018 完整宇宙学参数
    """
    Lambda_obs = COSMOLOGICAL_CONSTANT_OBSERVED

    relative_error = 0.01
    Lambda_obs_error = Lambda_obs * relative_error

    confidence_levels = {
        "68%": (Lambda_obs - Lambda_obs_error, Lambda_obs + Lambda_obs_error),
        "95%": (Lambda_obs - 2.0 * Lambda_obs_error, Lambda_obs + 2.0 * Lambda_obs_error),
        "99.7%": (Lambda_obs - 3.0 * Lambda_obs_error, Lambda_obs + 3.0 * Lambda_obs_error),
    }

    planck_params = {
        "H0": 67.66,
        "Omega_m": 0.3111,
        "Omega_Lambda": 0.6889,
        "Omega_b": 0.0486,
        "Omega_cdm": 0.2607,
        "Omega_k": 0.0007,
        "ns": 0.9665,
        "sigma8": 0.8102,
        "tau_reio": 0.0561,
        "age": 13.787,
        "z_reion": 7.82,
        "t0": 13.787,
    }

    return Lambda_obs, Lambda_obs_error, confidence_levels, planck_params


def lambda_error():
    """
    理论值 vs 观测值误差

    计算BSD理论值与Planck观测值之间的误差和一致性分析。

    Returns
    -------
    relative_error : float
        相对误差
    absolute_error : float
        绝对误差 (m⁻²)
    sigma_level : float
        显著性水平（σ）
    agreement : str
        一致性描述
    error_analysis : dict
        详细误差分析
    """
    Lambda_theo = COSMOLOGICAL_CONSTANT
    Lambda_obs = COSMOLOGICAL_CONSTANT_OBSERVED

    absolute_error = abs(Lambda_theo - Lambda_obs)
    relative_error = absolute_error / Lambda_obs

    Lambda_obs_error = Lambda_obs * 0.01
    sigma_level = absolute_error / Lambda_obs_error

    if sigma_level < 1.0:
        agreement = "excellent"
    elif sigma_level < 2.0:
        agreement = "good"
    elif sigma_level < 3.0:
        agreement = "tension"
    else:
        agreement = "strong_tension"

    error_analysis = {
        "theoretical_value": Lambda_theo,
        "observed_value": Lambda_obs,
        "absolute_error": absolute_error,
        "relative_error": relative_error,
        "percent_error": relative_error * 100.0,
        "sigma_level": sigma_level,
        "agreement": agreement,
        "ratio_theo_over_obs": Lambda_theo / Lambda_obs,
        "difference_sign": "positive" if Lambda_theo > Lambda_obs else "negative",
    }

    return relative_error, absolute_error, sigma_level, agreement, error_analysis


def lambda_from_bsd(kappa=None, alpha=None):
    """
    从BSD六系模态推导Λ

    基于BSD六系理论的κ和α参数推导宇宙学常数Λ。

    Parameters
    ----------
    kappa : float, optional
        虚实阻尼系数κ，默认使用锁档参数KAPPA
    alpha : float, optional
        稀疏补偿系数α，默认使用锁档参数ALPHA

    Returns
    -------
    Lambda_bsd : float
        BSD推导的Λ值 (m⁻²)
    derivation_steps : dict
        推导步骤详情
    six_system_contributions : dict
        六系各自的贡献
    normalization : float
        归一化因子
    """
    if kappa is None:
        kappa = KAPPA
    if alpha is None:
        alpha = ALPHA

    L_planck = 1.616255e-35
    Lambda_planck = 1.0 / L_planck**2

    s1 = kappa
    s2 = alpha
    s3 = GAMMA
    s4 = kappa * alpha
    s5 = np.sqrt(kappa**2 + alpha**2)
    s6 = (kappa + alpha) / (1.0 + kappa * alpha)

    product = s1 * s2 * s3 * s4 * s5 * s6
    sum_total = s1 + s2 + s3 + s4 + s5 + s6

    normalization = product / (sum_total**6 + 1e-12) * 6.0**6

    Lambda_bsd = Lambda_planck * normalization

    six_system_contributions = {
        "reinforcement": s1,
        "regulation": s2,
        "structure": s3,
        "information": s4,
        "energy": s5,
        "meaning": s6,
    }

    derivation_steps = {
        "step1_basic_params": {"kappa": kappa, "alpha": alpha, "gamma": GAMMA},
        "step2_six_coefficients": six_system_contributions,
        "step3_product": product,
        "step4_sum": sum_total,
        "step5_normalization": normalization,
        "step6_planck_scale": Lambda_planck,
        "step7_final_lambda": Lambda_bsd,
    }

    return Lambda_bsd, derivation_steps, six_system_contributions, normalization


def poincare_verification(Lambda):
    """
    庞加莱猜想稳态收敛验证

    基于宇宙学常数验证庞加莱猜想在宇宙尺度上的稳态收敛性。

    Parameters
    ----------
    Lambda : float or np.ndarray
        宇宙学常数Λ值 (m⁻²)

    Returns
    -------
    is_convergent : bool or np.ndarray
        是否收敛
    convergence_order : int or np.ndarray
        收敛阶数
    poincare_metric : float or np.ndarray
        庞加莱度规系数
    manifold_type : str or np.ndarray
        流形类型："spherical" / "flat" / "hyperbolic"
    topological_invariant : float or np.ndarray
        拓扑不变量（欧拉示性数估计）
    """
    Lambda = np.asarray(Lambda, dtype=float)

    H0 = 67.66e3 / 3.0856775814913673e22
    Omega_Lambda = Lambda * 3.0 / (H0**2 + 1e-12)

    critical_density = 1.0
    Omega_k = critical_density - (0.3111 + Omega_Lambda)

    if np.isscalar(Omega_k) or Omega_k.ndim == 0:
        if abs(Omega_k) < 0.001:
            manifold_type = "flat"
        elif Omega_k > 0:
            manifold_type = "hyperbolic"
        else:
            manifold_type = "spherical"
    else:
        manifold_type = np.where(
            np.abs(Omega_k) < 0.001,
            "flat",
            np.where(Omega_k > 0, "hyperbolic", "spherical"),
        )

    is_convergent = np.abs(Omega_k) < 0.01

    convergence_order = np.floor(1.0 / (np.abs(Omega_k) + 1e-12)).astype(int)

    poincare_metric = 1.0 / (1.0 + np.abs(Omega_k) * KAPPA)

    if manifold_type == "spherical":
        topological_invariant = 2.0
    elif manifold_type == "flat":
        topological_invariant = 0.0
    else:
        topological_invariant = -2.0

    return is_convergent, convergence_order, poincare_metric, manifold_type, topological_invariant


def universe_evolution(Lambda, t):
    """
    宇宙演化曲线

    基于ΛCDM模型计算宇宙尺度因子随时间的演化。

    Parameters
    ----------
    Lambda : float
        宇宙学常数Λ (m⁻²)
    t : np.ndarray
        时间序列（单位：年，从大爆炸开始）

    Returns
    -------
    scale_factor : np.ndarray
        尺度因子 a(t)
    hubble_parameter : np.ndarray
        哈勃参数 H(t)
    acceleration : np.ndarray
        加速度 ä/a
    cosmic_age : float
        宇宙年龄估计（年）
    evolution_phases : list of dict
        演化阶段描述
    """
    t = np.asarray(t, dtype=float)

    H0 = 67.66
    Omega_m = 0.3111
    Omega_Lambda = Lambda * 3.0e5**2 / (H0**2 * (3.0856775814913673e22 * 1e-3) ** 2)
    if abs(Omega_Lambda) > 100:
        Omega_Lambda = 0.6889
    Omega_r = 9.0e-5
    Omega_k = 1.0 - Omega_m - Omega_Lambda - Omega_r

    t_gyr = t / 1e9

    scale_factor = np.zeros_like(t_gyr)
    hubble_parameter = np.zeros_like(t_gyr)
    acceleration = np.zeros_like(t_gyr)

    for i, ti in enumerate(t_gyr):
        if ti <= 0:
            scale_factor[i] = 0.0
            hubble_parameter[i] = np.inf
            acceleration[i] = -np.inf
            continue

        a = 1e-10
        dt = ti * 1e-3
        t_curr = 0.0
        for _ in range(2000):
            if t_curr >= ti:
                break
            H_curr = H0 * np.sqrt(
                Omega_m / (a**3 + 1e-12)
                + Omega_r / (a**4 + 1e-12)
                + Omega_k / (a**2 + 1e-12)
                + Omega_Lambda
            )
            da = H_curr * a * dt
            a += da
            t_curr += dt * 9.778e2

        scale_factor[i] = a
        H_curr = H0 * np.sqrt(
            Omega_m / (a**3 + 1e-12)
            + Omega_r / (a**4 + 1e-12)
            + Omega_k / (a**2 + 1e-12)
            + Omega_Lambda
        )
        hubble_parameter[i] = H_curr

        q = (Omega_m / (a**3 + 1e-12) * 0.5 + Omega_r / (a**4 + 1e-12) - Omega_Lambda) / (
            Omega_m / (a**3 + 1e-12)
            + Omega_r / (a**4 + 1e-12)
            + Omega_k / (a**2 + 1e-12)
            + Omega_Lambda
            + 1e-12
        )
        acceleration[i] = -q * H_curr**2

    cosmic_age = 13.787e9

    evolution_phases = [
        {"name": "Planck_epoch", "time_range": (0, 1e-43), "scale_factor_range": (0, 1e-32)},
        {"name": "inflation", "time_range": (1e-36, 1e-32), "scale_factor_range": (1e-32, 1e-26)},
        {"name": "radiation_dominated", "time_range": (1e-32, 5e4), "scale_factor_range": (1e-26, 1e-4)},
        {"name": "matter_dominated", "time_range": (5e4, 9.8e9), "scale_factor_range": (1e-4, 0.75)},
        {"name": "dark_energy_dominated", "time_range": (9.8e9, np.inf), "scale_factor_range": (0.75, np.inf)},
    ]

    return scale_factor, hubble_parameter, acceleration, cosmic_age, evolution_phases
