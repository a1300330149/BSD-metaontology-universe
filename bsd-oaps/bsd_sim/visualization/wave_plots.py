"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：驻波拓扑收敛公理
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/BSD四层四场数理体系/
固定数理常量：κ=0.35, γ=0.92
【理论版本：ACTIVE-V1.8】
【T90 V1.8理论映射】C3三个0.9同构定理（驻波稳态对应0.9̇=1）/ C5 3×3粒子家族矩阵（驻波模态对应粒子代数）

驻波动力学可视化工具
—— 驻波波形、边界韧性、能量分布的三维/二维绘图
—— 适配T90 V1.8：可视化𝒯₊/𝒯₋双向迭代的驻波基底振荡与升维信息痕迹
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D


def plot_standing_wave_snapshot(wave_data, time_idx=-1, title="驻波快照",
                                 save_path=None, figsize=(10, 6)):
    """绘制某一时刻的驻波波形

    Parameters
    ----------
    wave_data : np.ndarray, shape (time_steps, num_points)
        驻波振幅时间序列
    time_idx : int
        时间索引，默认最后一帧
    title : str
        图标题
    save_path : str or None
        保存路径，None则返回fig对象
    """
    fig, ax = plt.subplots(figsize=figsize)
    x = np.arange(wave_data.shape[1])
    y = wave_data[time_idx]
    ax.plot(x, y, 'b-', linewidth=2, label=f't={time_idx}')
    ax.fill_between(x, y, 0, alpha=0.2, color='blue')
    ax.set_xlabel('空间位置')
    ax.set_ylabel('振幅 ψ')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_standing_wave_evolution(wave_data, title="驻波时空演化",
                                  save_path=None, figsize=(12, 8)):
    """绘制驻波时空演化的三维曲面图

    Parameters
    ----------
    wave_data : np.ndarray, shape (time_steps, num_points)
        驻波振幅时间序列
    """
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111, projection='3d')
    T, X = np.meshgrid(np.arange(wave_data.shape[0]),
                       np.arange(wave_data.shape[1]), indexing='ij')
    surf = ax.plot_surface(T, X, wave_data, cmap=cm.coolwarm,
                           linewidth=0, antialiased=True, alpha=0.8)
    ax.set_xlabel('时间步')
    ax.set_ylabel('空间位置')
    ax.set_zlabel('振幅 ψ')
    ax.set_title(title)
    fig.colorbar(surf, shrink=0.5, aspect=10, label='振幅')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_boundary_resilience(time_series, resilience_series,
                              title="边界韧性演化", save_path=None, figsize=(10, 6)):
    """绘制边界韧性随时间变化曲线

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    resilience_series : np.ndarray
        边界韧性值
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time_series, resilience_series, 'r-', linewidth=2, label='边界韧性 τ')
    ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='稳态阈值')
    ax.axhline(y=0.2, color='red', linestyle='--', alpha=0.5, label='断裂阈值')
    ax.set_xlabel('时间')
    ax.set_ylabel('边界韧性 τ')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_wave_energy_distribution(energy_data, title="驻波能量分布",
                                  save_path=None, figsize=(10, 6)):
    """绘制驻波能量在不同模态的分布

    Parameters
    ----------
    energy_data : np.ndarray or dict
        能量数据数组或{模态: 能量}字典
    """
    fig, ax = plt.subplots(figsize=figsize)
    if isinstance(energy_data, dict):
        modes = list(energy_data.keys())
        energies = list(energy_data.values())
        ax.bar(range(len(modes)), energies, color='steelblue', alpha=0.8)
        ax.set_xticks(range(len(modes)))
        ax.set_xticklabels(modes, rotation=45)
        ax.set_ylabel('能量')
    else:
        ax.hist(energy_data, bins=50, color='steelblue', alpha=0.8, edgecolor='black')
        ax.set_xlabel('能量值')
        ax.set_ylabel('频次')
    ax.set_title(title)
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_standing_wave_dashboard(simulator, save_path=None, figsize=(16, 12)):
    """驻波仿真仪表盘——四合一总览图

    Parameters
    ----------
    simulator : StandingWaveSimulator
        已执行run()的仿真器实例
    """
    results = simulator.get_results()
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # 左上：最终波形快照
    wave = results.get("wave_amplitude", np.zeros((10, 10)))
    if wave.ndim == 2:
        axes[0, 0].plot(wave[-1], 'b-', linewidth=2)
        axes[0, 0].fill_between(range(len(wave[-1])), wave[-1], 0, alpha=0.2)
    axes[0, 0].set_title('驻波快照（最终时刻）')
    axes[0, 0].set_xlabel('空间位置')
    axes[0, 0].set_ylabel('振幅')
    axes[0, 0].grid(True, alpha=0.3)

    # 右上：边界韧性
    br = results.get("boundary_resilience", [])
    if len(br) > 0:
        axes[0, 1].plot(br, 'r-', linewidth=2)
        axes[0, 1].axhline(y=0.5, color='orange', linestyle='--', alpha=0.5)
    axes[0, 1].set_title('边界韧性演化')
    axes[0, 1].set_xlabel('时间步')
    axes[0, 1].set_ylabel('韧性 τ')
    axes[0, 1].grid(True, alpha=0.3)

    # 左下：时空演化热图
    if wave.ndim == 2:
        im = axes[1, 0].imshow(wave.T, aspect='auto', cmap='coolwarm',
                                origin='lower', interpolation='bilinear')
        axes[1, 0].set_title('驻波时空演化热图')
        axes[1, 0].set_xlabel('时间步')
        axes[1, 0].set_ylabel('空间位置')
        plt.colorbar(im, ax=axes[1, 0], label='振幅')

    # 右下：能量分布
    energy = results.get("energy_distribution", [])
    if len(energy) > 0:
        axes[1, 1].plot(energy, 'g-', linewidth=2)
    axes[1, 1].set_title('能量演化')
    axes[1, 1].set_xlabel('时间步')
    axes[1, 1].set_ylabel('总能量')
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle('BSD驻波动力学仿真仪表盘', fontsize=16, fontweight='bold')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig
