"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理0·元道存在 / 公理6·双极性创生
对应九维维度：时间流·空间体·能量场
理论出处：theory_base/L0_总本源层/全域大一统理论/四位一体驻波动力学框架
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)

BSD驻波动力学方程求解器
—— 描述虚实振荡、边界驻波与模态干涉的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, GAMMA, ALPHA, E1, E2, E3


def wave_equation(psi, t, x, kappa=None):
    """
    驻波波动方程：∂²ψ/∂t² = κ² · ∇²ψ

    Parameters
    ----------
    psi : np.ndarray
        波函数场 ψ(x, t)，形状为 (Nt, Nx)
    t : np.ndarray
        时间坐标数组
    x : np.ndarray
        空间坐标数组
    kappa : float, optional
        波速系数（虚实阻尼系数），默认使用锁档 KAPPA

    Returns
    -------
    lhs : np.ndarray
        左端 ∂²ψ/∂t²
    rhs : np.ndarray
        右端 κ²·∇²ψ
    residual : np.ndarray
        残差 lhs - rhs
    """
    if kappa is None:
        kappa = KAPPA

    dt = t[1] - t[0]
    dx = x[1] - x[0]

    d2psi_dt2 = np.gradient(np.gradient(psi, dt, axis=0), dt, axis=0)
    d2psi_dx2 = np.gradient(np.gradient(psi, dx, axis=1), dx, axis=1)

    lhs = d2psi_dt2
    rhs = (kappa ** 2) * d2psi_dx2
    residual = lhs - rhs

    return lhs, rhs, residual


def boundary_resilience(tau_0, alpha_1, alpha_2, alpha_3):
    """
    边界韧性方程：τ = α₁·τ₀ / (α₂·α₃)

    描述边界在三元权重结构下的抗冲击韧性。

    Parameters
    ----------
    tau_0 : float
        基准韧性 τ₀
    alpha_1 : float
        第一权重 α₁（主导项）
    alpha_2 : float
        第二权重 α₂（抑制项）
    alpha_3 : float
        第三权重 α₃（抑制项）

    Returns
    -------
    tau : float
        边界韧性 τ
    """
    tau = alpha_1 * tau_0 / (alpha_2 * alpha_3 + 1e-12)
    return tau


def standing_wave_mode(n, L, kappa=None, t=0.0, num_points=1000):
    """
    第n阶驻波模态：ψₙ(x,t) = Aₙ·sin(nπx/L)·cos(ωₙt)

    Parameters
    ----------
    n : int
        模态阶数 n ≥ 1
    L : float
        边界间距（腔体长度）
    kappa : float, optional
        波速系数，默认使用锁档 KAPPA
    t : float
        时间点
    num_points : int
        空间采样点数

    Returns
    -------
    x : np.ndarray
        空间坐标
    psi_n : np.ndarray
        第n阶驻波模态振幅
    omega_n : float
        第n阶固有角频率 ωₙ = nπκ/L
    """
    if kappa is None:
        kappa = KAPPA

    x = np.linspace(0, L, num_points)
    omega_n = n * np.pi * kappa / L
    psi_n = np.sin(n * np.pi * x / L) * np.cos(omega_n * t)

    return x, psi_n, omega_n


def wave_interference(psi1, psi2):
    """
    两列驻波干涉叠加：ψ_total = ψ₁ + ψ₂

    计算干涉后的振幅分布、干涉项及可见度。

    Parameters
    ----------
    psi1 : np.ndarray
        第一列波的振幅场
    psi2 : np.ndarray
        第二列波的振幅场

    Returns
    -------
    psi_total : np.ndarray
        干涉后总波场
    interference_term : np.ndarray
        纯干涉项 = ψ_total - (|ψ₁|+|ψ₂| 平均效应)
    visibility : float
        干涉可见度 V = (I_max - I_min) / (I_max + I_min)
    """
    psi_total = psi1 + psi2

    intensity = psi_total ** 2
    I_max = np.max(intensity)
    I_min = np.min(intensity)
    visibility = (I_max - I_min) / (I_max + I_min + 1e-12)

    interference_term = psi_total - 0.5 * (np.abs(psi1) + np.abs(psi2))

    return psi_total, interference_term, visibility


def standing_wave_energy(psi, t, x, kappa=None):
    """
    驻波能量密度：E = (1/2)(∂ψ/∂t)² + (κ²/2)(∇ψ)²

    Parameters
    ----------
    psi : np.ndarray
        波函数场
    t : np.ndarray
        时间坐标
    x : np.ndarray
        空间坐标
    kappa : float, optional
        波速系数

    Returns
    -------
    energy_density : np.ndarray
        能量密度场
    total_energy : float
        总能量（空间积分）
    """
    if kappa is None:
        kappa = KAPPA

    dt = t[1] - t[0]
    dx = x[1] - x[0]

    dpsi_dt = np.gradient(psi, dt, axis=0)
    dpsi_dx = np.gradient(psi, dx, axis=1)

    kinetic = 0.5 * dpsi_dt ** 2
    potential = 0.5 * (kappa ** 2) * dpsi_dx ** 2
    energy_density = kinetic + potential

    total_energy = np.trapz(np.trapz(energy_density, x, axis=1), t, axis=0)

    return energy_density, total_energy
