"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理9·意义涌现公理 / 公理8·意义守恒公理
对应九维维度：意识维·意义维·命运维
理论出处：theory_base/L0_总本源层/全域大一统理论/涌现场与自组织
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)

BSD涌现场方程求解器
—— 描述涌现强度、自组织、不可还原性与整体论的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, GAMMA, ALPHA, E1, E2, E3


def emergence_measure(micro_states, macro_state):
    """
    涌现强度度量：E = H(macro) - Σ w_i · H(micro_i)

    基于信息论的涌现测度，宏观态熵减去微观态加权平均熵。

    Parameters
    ----------
    micro_states : list of np.ndarray
        各微观态的概率分布或时间序列
    macro_state : np.ndarray
        宏观态的概率分布或时间序列

    Returns
    -------
    emergence_strength : float
        涌现强度 E
    micro_entropy_total : float
        微观熵总和
    macro_entropy : float
        宏观熵
    """
    def _entropy(p):
        p = np.asarray(p, dtype=float)
        p = p / (np.sum(p) + 1e-12)
        p = np.maximum(p, 1e-12)
        return -np.sum(p * np.log(p))

    micro_entropies = [_entropy(ms) for ms in micro_states]
    weights = np.ones(len(micro_entropies)) / len(micro_entropies)
    micro_entropy_total = np.sum(weights * np.array(micro_entropies))
    macro_entropy = _entropy(macro_state)

    emergence_strength = macro_entropy - micro_entropy_total

    return emergence_strength, micro_entropy_total, macro_entropy


def self_organization_strength(interactions, time_series):
    """
    自组织强度：S = 1 - (S_final / S_initial)

    基于熵减程度度量系统自组织的强度。

    Parameters
    ----------
    interactions : np.ndarray
        相互作用矩阵 (N×N)
    time_series : np.ndarray
        系统状态时间序列 (T×N)

    Returns
    -------
    so_strength : float
        自组织强度 S ∈ [0, 1]
    entropy_initial : float
        初始熵
    entropy_final : float
        末态熵
    connectivity : float
        相互作用连接度
    """
    def _shannon_entropy(series):
        series = np.asarray(series)
        series = series[np.isfinite(series)]
        if len(series) < 2:
            return 0.0
        hist, _ = np.histogram(series, bins=min(50, len(series)), density=True)
        hist = hist / (np.sum(hist) + 1e-12)
        hist = np.maximum(hist, 1e-12)
        return -np.sum(hist * np.log(hist))

    entropy_initial = _shannon_entropy(time_series[0])
    entropy_final = _shannon_entropy(time_series[-1])

    so_strength = 1.0 - entropy_final / (entropy_initial + 1e-12)
    so_strength = np.clip(so_strength, 0.0, 1.0)

    interactions = np.asarray(interactions)
    n = interactions.shape[0]
    connectivity = np.sum(np.abs(interactions) > 1e-6) / (n * n)

    return so_strength, entropy_initial, entropy_final, connectivity


def irreducibility_index(micro, macro):
    """
    不可还原性指数：I = ||macro - F(micro)|| / ||macro||

    度量宏观态无法由微观态线性组合还原的程度。

    Parameters
    ----------
    micro : np.ndarray
        微观态矩阵 (N_samples × N_micro)
    macro : np.ndarray
        宏观态向量 (N_samples,)

    Returns
    -------
    irr_index : float
        不可还原性指数 I ∈ [0, 1]
    residual : np.ndarray
        残差向量
    best_fit : np.ndarray
        微观态最优线性组合
    """
    micro = np.asarray(micro, dtype=float)
    macro = np.asarray(macro, dtype=float)

    # 清理 NaN/Inf
    valid = np.isfinite(macro) & np.all(np.isfinite(micro), axis=-1)
    micro = micro[valid]
    macro = macro[valid]

    if micro.ndim == 1:
        micro = micro.reshape(-1, 1)
    if len(macro) < micro.shape[1]:
        return 0.0, np.array([]), np.array([])

    try:
        coeffs, _, _, _ = np.linalg.lstsq(micro, macro, rcond=None)
        best_fit = micro @ coeffs
        residual = macro - best_fit
    except np.linalg.LinAlgError:
        return 0.0, np.array([]), np.array([])

    macro_norm = np.linalg.norm(macro) + 1e-12
    residual_norm = np.linalg.norm(residual)
    irr_index = residual_norm / macro_norm
    irr_index = np.clip(irr_index, 0.0, 1.0)

    return irr_index, residual, best_fit


def holism_index(parts, whole):
    """
    整体大于部分之和指数：H = (whole - sum(parts)) / |whole|

    度量整体论效应——整体超越部分简单加总的程度。

    Parameters
    ----------
    parts : list of np.ndarray or list of float
        各部分的属性值
    whole : float or np.ndarray
        整体的属性值

    Returns
    -------
    h_index : float
        整体论指数 H
    sum_parts : float
        部分之和
    excess : float
        整体超出部分
    synergy_score : float
        协同评分
    """
    if isinstance(parts[0], np.ndarray):
        sum_parts = np.sum([np.sum(p) for p in parts])
        whole_val = np.sum(whole)
    else:
        sum_parts = np.sum(parts)
        whole_val = whole

    excess = whole_val - sum_parts
    h_index = excess / (abs(whole_val) + 1e-12)

    synergy_score = np.tanh(ALPHA * excess / (abs(sum_parts) + 1e-12))

    return h_index, sum_parts, excess, synergy_score


def emergence_phase_transition(micro_states, control_param):
    """
    涌现相变检测：寻找控制参数空间中的涌现临界点

    Parameters
    ----------
    micro_states : np.ndarray
        微观态时间序列 (T×N)
    control_param : np.ndarray
        控制参数序列 (T,)

    Returns
    -------
    critical_point : float
        涌现临界点控制参数值
    order_parameter : np.ndarray
        序参量（涌现强度）
    susceptibility : np.ndarray
        涌现极化率
    """
    T = len(control_param)
    order_parameter = np.zeros(T)
    window = max(5, T // 20)

    for i in range(T):
        start = max(0, i - window)
        end = min(T, i + window + 1)
        segment = micro_states[start:end]

        cov = np.cov(segment.T)
        # 清理 NaN/Inf 并加对角正则化保证收敛
        cov = np.nan_to_num(cov, nan=0.0, posinf=0.0, neginf=0.0)
        cov += np.eye(cov.shape[0]) * 1e-10
        try:
            eigenvalues = np.linalg.eigvalsh(cov)
            order_parameter[i] = np.max(eigenvalues) / (np.sum(eigenvalues) + 1e-12)
        except np.linalg.LinAlgError:
            order_parameter[i] = 0.0

    susceptibility = np.gradient(order_parameter, control_param)
    crit_idx = np.argmax(np.abs(susceptibility))
    critical_point = control_param[crit_idx]

    return critical_point, order_parameter, susceptibility
