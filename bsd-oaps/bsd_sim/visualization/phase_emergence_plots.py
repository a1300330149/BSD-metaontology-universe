"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：熵增分流公理、层级跃迁公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35
【理论版本：ACTIVE-V1.8】
【T90 V1.8理论映射】C1双向迭代算子（顺时针涌现→逆时针逆反）/ C2六层多元进制（相变对应B_k→B_{k+1}升维）

相变与涌现可视化工具
—— 相图、序参量曲线、涌现强度、同步动力学的二维/三维绘图
—— 适配T90 V1.8：可视化𝒯₊顺时针展开的涌现动力学与𝒯₋逆时针逆反的相变回归
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm


def plot_phase_diagram(T_series, order_param_series, critical_point=None,
                        title="相变相图", save_path=None, figsize=(10, 6)):
    """绘制温度-序参量相图

    Parameters
    ----------
    T_series : np.ndarray
        温度序列
    order_param_series : np.ndarray
        序参量序列
    critical_point : tuple or None
        临界点 (Tc, mc)
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(T_series, order_param_series, 'b-', linewidth=2, label='序参量 m(T)')
    if critical_point is not None:
        ax.axvline(x=critical_point[0], color='red', linestyle='--',
                   alpha=0.5, label=f'Tc={critical_point[0]:.3f}')
        ax.plot(critical_point[0], critical_point[1], 'ro', markersize=10)
    ax.set_xlabel('温度 T / Tc')
    ax.set_ylabel('序参量 m')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_free_energy_landscape(T_values, m_range, lagrangian_func,
                                title="自由能景观", save_path=None, figsize=(10, 8)):
    """绘制自由能F(m,T)的二维等高线图

    Parameters
    ----------
    T_values : np.ndarray
        温度网格
    m_range : np.ndarray
        序参量网格
    lagrangian_func : callable
        F(T, m) -> float
    """
    T_grid, m_grid = np.meshgrid(T_values, m_range, indexing='ij')
    F_grid = np.zeros_like(T_grid)
    for i in range(len(T_values)):
        for j in range(len(m_range)):
            F_grid[i, j] = lagrangian_func(T_values[i], m_range[j])

    fig, ax = plt.subplots(figsize=figsize)
    cp = ax.contourf(T_grid, m_grid, F_grid, levels=30, cmap='viridis')
    ax.contour(T_grid, m_grid, F_grid, levels=15, colors='white', linewidths=0.5, alpha=0.5)
    plt.colorbar(cp, ax=ax, label='自由能 F')
    ax.set_xlabel('温度 T / Tc')
    ax.set_ylabel('序参量 m')
    ax.set_title(title)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_emergence_dynamics(time_series, emergence_series, self_org_series=None,
                             threshold=None, title="涌现动力学",
                             save_path=None, figsize=(12, 6)):
    """绘制涌现强度和自组织强度随时间变化

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    emergence_series : np.ndarray
        涌现强度
    self_org_series : np.ndarray or None
        自组织强度
    threshold : float or None
        涌现相变阈值
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time_series, emergence_series, 'b-', linewidth=2, label='涌现强度')
    if self_org_series is not None:
        ax.plot(time_series, self_org_series, 'r--', linewidth=2, label='自组织强度')
    if threshold is not None:
        ax.axhline(y=threshold, color='green', linestyle=':', alpha=0.7,
                   label=f'涌现阈值={threshold:.3f}')
    ax.set_xlabel('时间步')
    ax.set_ylabel('强度指数')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_kuramoto_sync(phases, coupling_strengths=None, title="Kuramoto同步动力学",
                        save_path=None, figsize=(14, 6)):
    """绘制Kuramoto模型相位演化与同步序参量

    Parameters
    ----------
    phases : np.ndarray, shape (time_steps, num_oscillators)
        各振子相位时间序列
    coupling_strengths : np.ndarray or None
        同步序参量时间序列
    """
    if phases.ndim != 2:
        raise ValueError("phases 必须为二维数组 (time_steps, num_oscillators)")

    fig, axes = plt.subplots(1, 2, figsize=figsize)

    # 左图：相位演化
    for i in range(min(phases.shape[1], 20)):
        axes[0].plot(phases[:, i] % (2 * np.pi), alpha=0.6, linewidth=0.8)
    axes[0].set_xlabel('时间步')
    axes[0].set_ylabel('相位 θ (mod 2π)')
    axes[0].set_title('振子相位演化')
    axes[0].grid(True, alpha=0.3)

    # 右图：同步序参量
    if coupling_strengths is not None:
        axes[1].plot(coupling_strengths, 'g-', linewidth=2)
        axes[1].axhline(y=0.8, color='orange', linestyle='--', alpha=0.5, label='同步阈值')
        axes[1].set_ylabel('同步序参量 r')
        axes[1].legend()
    else:
        # 自动计算同步序参量
        r = np.abs(np.mean(np.exp(1j * phases), axis=1))
        axes[1].plot(r, 'g-', linewidth=2)
        axes[1].axhline(y=0.8, color='orange', linestyle='--', alpha=0.5, label='同步阈值')
        axes[1].set_ylabel('同步序参量 r')
        axes[1].legend()
    axes[1].set_xlabel('时间步')
    axes[1].set_title('全局同步度')
    axes[1].grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_critical_exponents(exponents_dict, title="临界指数标度关系",
                             save_path=None, figsize=(8, 6)):
    """绘制临界指数及其标度关系验证

    Parameters
    ----------
    exponents_dict : dict
        {指数名: 值}，如 {'β': 0.33, 'γ': 1.24, 'ν': 0.63, 'η': 0.04}
    """
    fig, ax = plt.subplots(figsize=figsize)
    names = list(exponents_dict.keys())
    values = list(exponents_dict.values())
    colors = cm.Set2(np.linspace(0, 1, len(names)))
    bars = ax.bar(names, values, color=colors, alpha=0.85, edgecolor='black')
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.02,
                f'{val:.3f}', ha='center', va='bottom', fontsize=12)
    ax.set_ylabel('指数值')
    ax.set_title(title)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig
