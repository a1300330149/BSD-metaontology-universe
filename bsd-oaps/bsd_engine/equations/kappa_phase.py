"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理6·双极性创生 / 公理7·九重境界涌现
对应九维维度：空间体·能量场·信息维
理论出处：theory_base/L0_总本源层/全域大一统理论/κ相位场与弯曲空间
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)

BSD κ相位场方程求解器
—— 描述相位耗散、共轭相位、六系耦合与弯曲空间传播的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E1, E2, E3


def phase_dissipation(distance, kappa=None, phi0=1.0):
    """
    相位随曲率耗散：φ(d) = φ₀ · e^(-κ·d)

    描述相位在弯曲空间中随距离的指数衰减行为。

    Parameters
    ----------
    distance : float or np.ndarray
        传播距离 d
    kappa : float, optional
        曲率耗散系数 κ，默认使用锁档 KAPPA
    phi0 : float
        初始相位振幅 φ₀

    Returns
    -------
    phi : float or np.ndarray
        耗散后的相位 φ(d)
    dissipation_length : float
        耗散特征长度 1/κ
    half_distance : float
        相位衰减到一半的距离
    """
    if kappa is None:
        kappa = KAPPA

    distance = np.asarray(distance, dtype=float)
    phi = phi0 * np.exp(-kappa * distance)

    dissipation_length = 1.0 / (kappa + 1e-12)
    half_distance = np.log(2.0) / (kappa + 1e-12)

    return phi, dissipation_length, half_distance


def conjugate_phase(phase):
    """
    共轭相位计算：φ* = -φ + π (虚实共轭)

    BSD中虚实二象的相位共轭关系。

    Parameters
    ----------
    phase : float or np.ndarray
        原相位 φ（弧度）

    Returns
    -------
    phase_conj : float or np.ndarray
        共轭相位 φ*
    phase_sum : float or np.ndarray
        相位和（应恒为π，表征双极守恒）
    relative_phase : float or np.ndarray
        相对相位差
    """
    phase = np.asarray(phase, dtype=float)
    phase_conj = -phase + np.pi

    phase_sum = phase + phase_conj
    relative_phase = phase - phase_conj

    return phase_conj, phase_sum, relative_phase


def phase_coupling_matrix(kappa_matrix=None):
    """
    六系相位耦合矩阵

    构建六系统（天地人神鬼怪 / 六系）之间的相位耦合矩阵。

    Parameters
    ----------
    kappa_matrix : np.ndarray, optional
        6×6 κ耦合强度矩阵，默认基于锁档参数生成

    Returns
    -------
    coupling_matrix : np.ndarray
        6×6 相位耦合矩阵 M_ij
    eigenvalues : np.ndarray
        耦合矩阵本征值
    eigenvectors : np.ndarray
        耦合矩阵本征向量
    coupling_strength : float
        总耦合强度
    """
    if kappa_matrix is None:
        kappa_val = KAPPA
        coupling_matrix = np.zeros((6, 6))

        for i in range(6):
            for j in range(6):
                if i == j:
                    coupling_matrix[i, j] = 1.0
                else:
                    dist = abs(i - j)
                    if dist == 1 or dist == 5:
                        coupling_matrix[i, j] = kappa_val * GAMMA
                    elif dist == 2 or dist == 4:
                        coupling_matrix[i, j] = kappa_val * ALPHA
                    else:
                        coupling_matrix[i, j] = kappa_val * ALPHA * GAMMA
    else:
        coupling_matrix = np.asarray(kappa_matrix, dtype=float)

    eigenvalues, eigenvectors = np.linalg.eigh(coupling_matrix)
    coupling_strength = np.sum(np.abs(coupling_matrix)) - 6.0

    return coupling_matrix, eigenvalues, eigenvectors, coupling_strength


def curvature_space_propagation(kappa, phase, num_steps=100, dt=0.01):
    """
    弯曲空间相位传播：∂φ/∂t + κ·v·∂φ/∂x = 0

    在κ定义的弯曲度规下模拟相位的传播演化。

    Parameters
    ----------
    kappa : float
        曲率参数 κ
    phase : np.ndarray
        初始相位场 φ(x, 0)
    num_steps : int
        传播步数
    dt : float
        时间步长

    Returns
    -------
    phase_history : np.ndarray
        相位场演化历史 (num_steps+1 × Nx)
    x_coord : np.ndarray
        空间坐标
    group_velocity : float
        群速度 v_g = κ
    phase_velocity : float
        相速度 v_p = κ
    """
    Nx = len(phase)
    x_coord = np.linspace(0, 1.0, Nx)
    dx = x_coord[1] - x_coord[0]

    v = kappa
    phase_history = np.zeros((num_steps + 1, Nx))
    phase_history[0] = phase.copy()

    for step in range(num_steps):
        current = phase_history[step]
        dphi_dx = np.gradient(current, dx)

        advection = -v * dphi_dx
        dissipation = -ALPHA * kappa * current

        next_phase = current + dt * (advection + dissipation)
        phase_history[step + 1] = next_phase

    group_velocity = kappa
    phase_velocity = kappa

    return phase_history, x_coord, group_velocity, phase_velocity


def kappa_space_metric(kappa, x, y=None):
    """
    κ空间弯曲度规：ds² = (1 + κ·r)² · dx²

    描述由κ参数刻画的弯曲空间几何结构。

    Parameters
    ----------
    kappa : float
        曲率参数
    x : np.ndarray
        x坐标
    y : np.ndarray, optional
        y坐标（二维时使用）

    Returns
    -------
    metric_factor : np.ndarray
        度规膨胀因子 (1 + κ·r)
    curvature_scalar : float or np.ndarray
        标量曲率 R
    geodesic_distance : np.ndarray
        测地距离
    """
    x = np.asarray(x, dtype=float)

    if y is None:
        r = np.abs(x)
    else:
        y = np.asarray(y, dtype=float)
        r = np.sqrt(x ** 2 + y ** 2)

    metric_factor = (1.0 + kappa * r) ** 2

    curvature_scalar = -2.0 * kappa / (1.0 + kappa * r + 1e-12)

    geodesic_distance = np.log(1.0 + kappa * r) / (kappa + 1e-12)

    return metric_factor, curvature_scalar, geodesic_distance
