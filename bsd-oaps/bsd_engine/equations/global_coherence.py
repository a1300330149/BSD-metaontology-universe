"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理8·全局相干公理 / 公理6·双极性创生公理
对应九维维度：信息维·意识维·能量场·时空维·物质维
理论出处：theory_base/L0_总本源层/全域大一统理论/全局相干与激光类比
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)、E2=0.65

BSD全局相干度求解器
—— 描述全局时空相干度、相干热图、跨系统耦合与健康状态映射的核心数理引擎
"""

import numpy as np
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E2


def global_coherence(signals, method="pearson"):
    """
    全局时空相干度 GC = 全局相干度（Pearson类比激光vs普通光）

    计算多路信号的全局相干度，类比激光（高相干）与普通光（低相干）：
    - Pearson相关系数矩阵平均
    - 相位相干性
    - 互信息

    Parameters
    ----------
    signals : np.ndarray
        信号矩阵，shape=(n_channels, n_samples)
    method : str
        计算方法："pearson" / "phase" / "mutual_info"

    Returns
    -------
    gc_value : float
        全局相干度值（0-1）
    coherence_matrix : np.ndarray
        相干度矩阵，shape=(n_channels, n_channels)
    coherence_type : str
        相干类型："laser_like" / "partial" / "incoherent"
    """
    signals = np.asarray(signals, dtype=float)
    if signals.ndim == 1:
        signals = signals.reshape(1, -1)

    n_channels, n_samples = signals.shape

    if n_channels < 2:
        return 1.0, np.eye(1), "laser_like"

    if method == "pearson":
        centered = signals - np.mean(signals, axis=1, keepdims=True)
        stds = np.std(signals, axis=1, keepdims=True)
        norm_signals = centered / (stds + 1e-12)
        coherence_matrix = np.dot(norm_signals, norm_signals.T) / n_samples
    elif method == "phase":
        analytic = np.zeros_like(signals, dtype=complex)
        for i in range(n_channels):
            sig = signals[i]
            fft_sig = np.fft.fft(sig)
            n = len(sig)
            h = np.zeros(n)
            if n % 2 == 0:
                h[0] = h[n // 2] = 1
                h[1 : n // 2] = 2
            else:
                h[0] = 1
                h[1 : (n + 1) // 2] = 2
            analytic[i] = np.fft.ifft(fft_sig * h)

        phases = np.angle(analytic)
        coherence_matrix = np.zeros((n_channels, n_channels))
        for i in range(n_channels):
            for j in range(n_channels):
                phase_diff = phases[i] - phases[j]
                coherence_matrix[i, j] = np.abs(np.mean(np.exp(1j * phase_diff)))
    elif method == "mutual_info":
        coherence_matrix = np.zeros((n_channels, n_channels))
        n_bins = int(np.sqrt(n_samples))
        for i in range(n_channels):
            for j in range(n_channels):
                hist_2d, _, _ = np.histogram2d(signals[i], signals[j], bins=n_bins)
                pxy = hist_2d / (np.sum(hist_2d) + 1e-12)
                px = np.sum(pxy, axis=1)
                py = np.sum(pxy, axis=0)
                px_py = px[:, None] * py[None, :]
                mask = pxy > 0
                mi = np.sum(pxy[mask] * np.log(pxy[mask] / (px_py[mask] + 1e-12) + 1e-12))
                coherence_matrix[i, j] = 1.0 - np.exp(-2.0 * mi)
    else:
        raise ValueError(f"未知的方法: {method}")

    upper_tri = coherence_matrix[np.triu_indices(n_channels, k=1)]
    gc_value = np.mean(upper_tri) if len(upper_tri) > 0 else 1.0
    gc_value = np.clip(gc_value, 0.0, 1.0)

    if gc_value >= E2:
        coherence_type = "laser_like"
    elif gc_value >= KAPPA:
        coherence_type = "partial"
    else:
        coherence_type = "incoherent"

    return gc_value, coherence_matrix, coherence_type


def coherence_heatmap(signals, fs=1.0):
    """
    相干度热图计算

    计算信号间的时频相干度热图，展示不同频率和时间的相干性分布。

    Parameters
    ----------
    signals : np.ndarray
        信号矩阵，shape=(n_channels, n_samples)
    fs : float
        采样频率

    Returns
    -------
    freq_bins : np.ndarray
        频率轴
    time_bins : np.ndarray
        时间轴
    coherence_map : np.ndarray
        相干度热图，shape=(n_freq, n_time, n_pairs)
    average_coherence : np.ndarray
        平均相干度，shape=(n_freq, n_time)
    """
    signals = np.asarray(signals, dtype=float)
    if signals.ndim == 1:
        signals = signals.reshape(1, -1)

    n_channels, n_samples = signals.shape
    nperseg = min(256, n_samples // 4)
    noverlap = nperseg // 2

    n_freq = nperseg // 2 + 1
    n_time = (n_samples - noverlap) // (nperseg - noverlap)

    if n_time < 1:
        n_time = 1

    pairs = []
    for i in range(n_channels):
        for j in range(i + 1, n_channels):
            pairs.append((i, j))

    n_pairs = len(pairs)
    coherence_map = np.zeros((n_freq, n_time, max(1, n_pairs)))

    freq_bins = np.fft.rfftfreq(nperseg, d=1.0 / fs)
    time_bins = np.arange(n_time) * (nperseg - noverlap) / fs

    if n_pairs == 0:
        return freq_bins, time_bins, coherence_map, np.ones((n_freq, n_time))

    for p_idx, (ch1, ch2) in enumerate(pairs):
        for t_idx in range(n_time):
            start = t_idx * (nperseg - noverlap)
            end = start + nperseg
            if end > n_samples:
                end = n_samples
                start = end - nperseg
                if start < 0:
                    start = 0

            seg1 = signals[ch1, start:end]
            seg2 = signals[ch2, start:end]

            if len(seg1) < nperseg:
                seg1 = np.pad(seg1, (0, nperseg - len(seg1)))
                seg2 = np.pad(seg2, (0, nperseg - len(seg2)))

            fft1 = np.fft.rfft(seg1 * np.hanning(nperseg))
            fft2 = np.fft.rfft(seg2 * np.hanning(nperseg))

            pxx = np.abs(fft1) ** 2
            pyy = np.abs(fft2) ** 2
            pxy = fft1 * np.conj(fft2)

            coh = np.abs(pxy) ** 2 / (pxx * pyy + 1e-12)
            coherence_map[:, t_idx, p_idx] = np.clip(coh, 0.0, 1.0)

    average_coherence = np.mean(coherence_map, axis=2)

    return freq_bins, time_bins, coherence_map, average_coherence


def cross_system_coupling(system1, system2):
    """
    跨系统耦合相位差

    计算两个系统之间的耦合强度和相位差，用于分析系统间的相互作用。

    Parameters
    ----------
    system1 : np.ndarray
        系统1的信号，shape=(n_samples,) 或 (n_channels1, n_samples)
    system2 : np.ndarray
        系统2的信号，shape=(n_samples,) 或 (n_channels2, n_samples)

    Returns
    -------
    coupling_strength : float
        耦合强度（0-1）
    phase_difference : float
        平均相位差（弧度）
    coupling_matrix : np.ndarray
        耦合矩阵，shape=(n_channels1, n_channels2)
    lead_lag : str
        领先-滞后关系："system1_leads" / "system2_leads" / "synchronous"
    """
    system1 = np.asarray(system1, dtype=float)
    system2 = np.asarray(system2, dtype=float)

    if system1.ndim == 1:
        system1 = system1.reshape(1, -1)
    if system2.ndim == 1:
        system2 = system2.reshape(1, -1)

    n_ch1, n_samples1 = system1.shape
    n_ch2, n_samples2 = system2.shape
    n_samples = min(n_samples1, n_samples2)

    system1 = system1[:, :n_samples]
    system2 = system2[:, :n_samples]

    def analytic_signal(sig):
        n = len(sig)
        fft_sig = np.fft.fft(sig)
        h = np.zeros(n)
        if n % 2 == 0:
            h[0] = h[n // 2] = 1
            h[1 : n // 2] = 2
        else:
            h[0] = 1
            h[1 : (n + 1) // 2] = 2
        return np.fft.ifft(fft_sig * h)

    analytic1 = np.array([analytic_signal(system1[i]) for i in range(n_ch1)])
    analytic2 = np.array([analytic_signal(system2[i]) for i in range(n_ch2)])

    phase1 = np.angle(analytic1)
    phase2 = np.angle(analytic2)

    coupling_matrix = np.zeros((n_ch1, n_ch2))
    phase_diff_matrix = np.zeros((n_ch1, n_ch2))

    for i in range(n_ch1):
        for j in range(n_ch2):
            phase_diff = phase1[i] - phase2[j]
            coupling_matrix[i, j] = np.abs(np.mean(np.exp(1j * phase_diff)))
            phase_diff_matrix[i, j] = np.angle(np.mean(np.exp(1j * phase_diff)))

    coupling_strength = np.mean(coupling_matrix)
    phase_difference = np.mean(phase_diff_matrix)

    phase_diff_norm = np.abs(phase_difference)
    if phase_diff_norm < 0.1:
        lead_lag = "synchronous"
    elif phase_difference > 0:
        lead_lag = "system1_leads"
    else:
        lead_lag = "system2_leads"

    return coupling_strength, phase_difference, coupling_matrix, lead_lag


def coherence_threshold(gc_value):
    """
    相干度阈值判定

    基于锁档参数的多级阈值判定，确定相干度所在的状态区间。

    Parameters
    ----------
    gc_value : float or np.ndarray
        相干度值（0-1）

    Returns
    -------
    level : str or np.ndarray
        相干等级："ultra_high" / "high" / "medium" / "low" / "very_low"
    threshold_dict : dict
        各阈值定义
    health_score : float or np.ndarray
        健康评分（0-100）
    """
    from bsd_engine.registry.constants import E1, E2, E3

    gc_value = np.asarray(gc_value, dtype=float)

    threshold_dict = {
        "ultra_high": E3,
        "high": E2,
        "medium": E1,
        "low": KAPPA,
        "very_low": ALPHA,
    }

    def get_level(val):
        if val >= E3:
            return "ultra_high"
        elif val >= E2:
            return "high"
        elif val >= E1:
            return "medium"
        elif val >= KAPPA:
            return "low"
        else:
            return "very_low"

    if np.isscalar(gc_value) or gc_value.ndim == 0:
        level = get_level(gc_value)
    else:
        level = np.array([get_level(v) for v in gc_value.flatten()]).reshape(gc_value.shape)

    health_score = np.clip(gc_value * 100.0, 0.0, 100.0)

    return level, threshold_dict, health_score


def coherence_to_health(gc):
    """
    相干度→健康状态映射

    将全局相干度映射到具体的健康状态描述，基于BSD六系健康模型。

    Parameters
    ----------
    gc : float or np.ndarray
        全局相干度值（0-1）

    Returns
    -------
    health_state : str or np.ndarray
        健康状态："perfect" / "excellent" / "good" / "fair" / "poor" / "critical"
    organ_systems : dict
        各器官系统状态估计
    recommendation : str
        建议措施
    """
    from bsd_engine.registry.constants import E1, E2, E3

    gc = np.asarray(gc, dtype=float)
    gc_scalar = float(np.mean(gc)) if gc.size > 1 else float(gc)

    if gc_scalar >= E3:
        health_state = "perfect"
        recommendation = "维持现状，持续优化生命系统"
    elif gc_scalar >= E2:
        health_state = "excellent"
        recommendation = "保持良好生活习惯，定期体检"
    elif gc_scalar >= E1:
        health_state = "good"
        recommendation = "注意休息，适度运动，均衡饮食"
    elif gc_scalar >= KAPPA:
        health_state = "fair"
        recommendation = "建议调整作息，增加运动，减少压力"
    elif gc_scalar >= ALPHA:
        health_state = "poor"
        recommendation = "建议就医检查，调整生活方式"
    else:
        health_state = "critical"
        recommendation = "立即就医，全面检查身体状况"

    organ_systems = {
        "cardiovascular": np.clip(gc_scalar * (1.0 + KAPPA * 0.1), 0.0, 1.0),
        "nervous": np.clip(gc_scalar * (1.0 + ALPHA * 0.2), 0.0, 1.0),
        "immune": np.clip(gc_scalar * (1.0 - KAPPA * 0.05), 0.0, 1.0),
        "digestive": np.clip(gc_scalar * (1.0 - ALPHA * 0.1), 0.0, 1.0),
        "respiratory": np.clip(gc_scalar * (1.0 + GAMMA * 0.05), 0.0, 1.0),
        "endocrine": np.clip(gc_scalar * (1.0 - GAMMA * 0.1), 0.0, 1.0),
    }

    return health_state, organ_systems, recommendation
