"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：稳态势母方程、全局相干度公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35, Λ=1.106×10⁻⁵²

生命稳态与宇宙学可视化工具
—— 五维生命稳态、相干度、宇宙演化、Λ验证的绘图
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import cm


def plot_five_dim_steady_state(time_series, five_dim_series,
                                labels=None, title="五维生命稳态演化",
                                save_path=None, figsize=(14, 6)):
    """绘制五维（气/血/身/心/道）稳态时间序列

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    five_dim_series : np.ndarray, shape (time_steps, 5)
        五维参数时间序列
    labels : list or None
        五维标签，默认 ['气', '血', '身', '心', '道']
    """
    if labels is None:
        labels = ['气', '血', '身', '心', '道']

    fig, ax = plt.subplots(figsize=figsize)
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    for i in range(5):
        ax.plot(time_series, five_dim_series[:, i], color=colors[i],
                linewidth=2, label=labels[i], alpha=0.85)
    ax.axhspan(0.30, 0.40, alpha=0.1, color='green', label='健康α区间')
    ax.set_xlabel('时间步')
    ax.set_ylabel('稳态值')
    ax.set_title(title)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_global_coherence(time_series, gc_series, health_mapping=None,
                           title="全局相干度GC演化", save_path=None, figsize=(12, 6)):
    """绘制全局相干度GC随时间变化

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    gc_series : np.ndarray
        GC值时间序列
    health_mapping : list or None
        健康等级标注 [(time_idx, level), ...]
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time_series, gc_series, 'b-', linewidth=2, label='GC')
    ax.axhline(y=0.8, color='green', linestyle='--', alpha=0.5, label='高相干阈值')
    ax.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='中等阈值')
    ax.axhline(y=0.3, color='red', linestyle='--', alpha=0.5, label='低相干阈值')
    ax.fill_between(time_series, gc_series, 0, where=gc_series > 0.8,
                    alpha=0.15, color='green')
    ax.fill_between(time_series, gc_series, 0, where=gc_series < 0.3,
                    alpha=0.15, color='red')
    ax.set_xlabel('时间步')
    ax.set_ylabel('全局相干度 GC')
    ax.set_title(title)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_cosmology_evolution(time_series, scale_factor, hubble_param,
                              title="宇宙学演化曲线", save_path=None, figsize=(14, 6)):
    """绘制宇宙尺度因子a(t)和哈勃参数H(t)的双轴图

    Parameters
    ----------
    time_series : np.ndarray
        时间轴 (Gyr)
    scale_factor : np.ndarray
        尺度因子 a(t)
    hubble_param : np.ndarray
        哈勃参数 H(t)
    """
    fig, ax1 = plt.subplots(figsize=figsize)
    color1 = 'steelblue'
    ax1.set_xlabel('宇宙时间 (Gyr)')
    ax1.set_ylabel('尺度因子 a(t)', color=color1)
    ax1.plot(time_series, scale_factor, color=color1, linewidth=2.5, label='a(t)')
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, alpha=0.3)

    ax2 = ax1.twinx()
    color2 = 'crimson'
    ax2.set_ylabel('哈勃参数 H(t) (Gyr⁻¹)', color=color2)
    ax2.plot(time_series, hubble_param, color=color2, linewidth=2.5,
             linestyle='--', label='H(t)')
    ax2.tick_params(axis='y', labelcolor=color2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_lambda_verification(theoretical, observed, error_pct,
                              title="宇宙学常数Λ验证", save_path=None, figsize=(8, 6)):
    """绘制Λ理论值vs观测值对比图

    Parameters
    ----------
    theoretical : float
        理论值 Λ_theory
    observed : float
        观测值 Λ_obs
    error_pct : float
        误差百分比
    """
    fig, ax = plt.subplots(figsize=figsize)
    categories = ['BSD理论值\nΛ_theory', 'Planck观测值\nΛ_obs']
    values = [theoretical, observed]
    colors = ['#3498db', '#e74c3c']
    bars = ax.bar(categories, values, color=colors, width=0.5, alpha=0.85,
                  edgecolor='black')
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f'{val:.4e}', ha='center', va='bottom', fontsize=11)

    ax.set_ylabel('Λ (m⁻²)')
    ax.set_title(f'{title}\n误差: {error_pct:.3f}%', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')

    # 添加一致性判定
    if error_pct < 1.0:
        verdict = "✓ 优级一致 (<1%)"
        color = 'green'
    elif error_pct < 5.0:
        verdict = "○ 良好一致 (<5%)"
        color = 'orange'
    else:
        verdict = "✗ 偏差较大 (≥5%)"
        color = 'red'
    ax.text(0.5, 0.95, verdict, transform=ax.transAxes, ha='center',
            fontsize=13, color=color, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_life_steady_dashboard(simulator, save_path=None, figsize=(16, 10)):
    """生命稳态仿真仪表盘——三合一总览图

    Parameters
    ----------
    simulator : LifeSteadySimulator
        已执行run()的仿真器实例
    """
    results = simulator.get_results()
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # 左上：五维稳态
    five_dim = results.get("five_dim_series", np.zeros((10, 5)))
    labels = ['气', '血', '身', '心', '道']
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    for i in range(min(5, five_dim.shape[1])):
        axes[0, 0].plot(five_dim[:, i], color=colors[i], linewidth=2,
                        label=labels[i], alpha=0.85)
    axes[0, 0].set_title('五维稳态演化')
    axes[0, 0].set_xlabel('时间步')
    axes[0, 0].set_ylabel('稳态值')
    axes[0, 0].legend(fontsize=9)
    axes[0, 0].grid(True, alpha=0.3)

    # 右上：GC曲线
    gc = results.get("gc_series", [])
    if len(gc) > 0:
        axes[0, 1].plot(gc, 'b-', linewidth=2)
        axes[0, 1].axhline(y=0.8, color='green', linestyle='--', alpha=0.5)
    axes[0, 1].set_title('全局相干度 GC')
    axes[0, 1].set_xlabel('时间步')
    axes[0, 1].set_ylabel('GC')
    axes[0, 1].grid(True, alpha=0.3)

    # 左下：气纯净度
    purity = results.get("qi_purity_series", [])
    if len(purity) > 0:
        axes[1, 0].plot(purity, 'g-', linewidth=2)
    axes[1, 0].set_title('气纯净度')
    axes[1, 0].set_xlabel('时间步')
    axes[1, 0].set_ylabel('纯净度')
    axes[1, 0].grid(True, alpha=0.3)

    # 右下：健康等级
    health = results.get("health_level", "未知")
    axes[1, 1].text(0.5, 0.5, f'健康等级:\n{health}', ha='center', va='center',
                    fontsize=20, fontweight='bold',
                    transform=axes[1, 1].transAxes,
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    axes[1, 1].set_title('综合健康评估')
    axes[1, 1].axis('off')

    plt.suptitle('BSD生命五维稳态仿真仪表盘', fontsize=16, fontweight='bold')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig
