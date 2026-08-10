"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：熵增分流公理、层级跃迁公理
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35

熵流与文明演化可视化工具
—— 熵流曲线、灾变预警、六系演化、文明周期的绘图
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


def plot_entropy_flow(time_series, E_res_series, title="全域熵流演化",
                      save_path=None, figsize=(12, 6)):
    """绘制残余熵E_res随时间变化，含三档预警带

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    E_res_series : np.ndarray
        残余熵时间序列
    """
    fig, ax = plt.subplots(figsize=figsize)

    # 预警带
    ax.axhspan(0.0, 0.40, alpha=0.1, color='green', label='安全稳态 (<0.40)')
    ax.axhspan(0.40, 0.75, alpha=0.15, color='yellow', label='中层矿化 (0.40-0.75)')
    ax.axhspan(0.75, 0.98, alpha=0.2, color='orange', label='底层僵化 (0.75-0.98)')
    ax.axhspan(0.98, 1.05, alpha=0.25, color='red', label='全域坍缩 (≥0.98)')

    ax.plot(time_series, E_res_series, 'k-', linewidth=2.5, label='E_res')
    ax.set_xlabel('时间步')
    ax.set_ylabel('残余熵 E_res')
    ax.set_title(title)
    ax.set_ylim(-0.05, 1.10)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_six_systems_radar(six_systems_data, labels=None, title="六系动力学雷达图",
                            save_path=None, figsize=(8, 8)):
    """绘制六系权重的雷达图

    Parameters
    ----------
    six_systems_data : dict or np.ndarray
        六系数据 {系名: 值} 或 shape (6,) 数组
    labels : list or None
        六系标签，默认 ['天道系', '强化系', '变身系', '具现系', '社会系', '自然系']
    """
    if labels is None:
        labels = ['天道系', '强化系', '变身系', '具现系', '社会系', '自然系']

    if isinstance(six_systems_data, dict):
        values = [six_systems_data.get(l, 0) for l in labels]
    else:
        values = list(six_systems_data)

    N = len(labels)
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
    values_plot = values + values[:1]
    angles_plot = angles + angles[:1]

    fig, ax = plt.subplots(figsize=figsize, subplot_kw=dict(polar=True))
    ax.fill(angles_plot, values_plot, alpha=0.25, color='steelblue')
    ax.plot(angles_plot, values_plot, 'b-o', linewidth=2, markersize=8)
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_ylim(0, max(values) * 1.2 if max(values) > 0 else 1.0)
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_six_systems_evolution(time_series, six_systems_series, labels=None,
                                title="六系动力学演化", save_path=None, figsize=(14, 8)):
    """绘制六系权重随时间演化的堆叠面积图

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    six_systems_series : np.ndarray, shape (time_steps, 6)
        六系权重时间序列
    labels : list or None
        六系标签
    """
    if labels is None:
        labels = ['天道系', '强化系', '变身系', '具现系', '社会系', '自然系']

    fig, ax = plt.subplots(figsize=figsize)
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    ax.stackplot(time_series, six_systems_series.T, labels=labels, colors=colors, alpha=0.8)
    ax.set_xlabel('时间步')
    ax.set_ylabel('权重')
    ax.set_title(title)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_civilization_cycle(time_series, entropy_series, warning_levels=None,
                             title="文明周期与灾变预警", save_path=None, figsize=(14, 8)):
    """绘制文明演化周期图——熵流+灾变标记

    Parameters
    ----------
    time_series : np.ndarray
        时间轴
    entropy_series : np.ndarray
        残余熵时间序列
    warning_levels : list or None
        灾变事件列表 [(time_idx, level_name), ...]
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(time_series, entropy_series, 'b-', linewidth=2, label='E_res')
    ax.axhline(y=0.40, color='yellow', linestyle='--', alpha=0.5, label='矿化警戒线')
    ax.axhline(y=0.75, color='orange', linestyle='--', alpha=0.5, label='僵化红线')
    ax.axhline(y=0.98, color='red', linestyle='--', alpha=0.5, label='坍缩阈值')

    if warning_levels:
        for t_idx, level in warning_levels:
            color_map = {'矿化': 'yellow', '僵化': 'orange', '坍缩': 'red'}
            c = color_map.get(level, 'gray')
            ax.axvline(x=time_series[t_idx], color=c, alpha=0.3, linestyle=':')
            ax.annotate(level, xy=(time_series[t_idx], entropy_series[t_idx]),
                        fontsize=8, color=c, fontweight='bold')

    ax.set_xlabel('时间步')
    ax.set_ylabel('残余熵 E_res')
    ax.set_title(title)
    ax.set_ylim(-0.05, 1.10)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig


def plot_catastrophe_heatmap(six_systems_series, E_res_series, labels=None,
                              title="六系-熵灾变热图", save_path=None, figsize=(14, 6)):
    """绘制六系权重与残余熵的联合热图

    Parameters
    ----------
    six_systems_series : np.ndarray, shape (time_steps, 6)
        六系权重时间序列
    E_res_series : np.ndarray
        残余熵时间序列
    labels : list or None
        六系标签
    """
    if labels is None:
        labels = ['天道系', '强化系', '变身系', '具现系', '社会系', '自然系']

    combined = np.vstack([six_systems_series.T, E_res_series[np.newaxis, :]])

    fig, ax = plt.subplots(figsize=figsize)
    im = ax.imshow(combined, aspect='auto', cmap='RdYlGn_r',
                   interpolation='bilinear')
    ax.set_yticks(range(len(labels) + 1))
    ax.set_yticklabels(labels + ['E_res'])
    ax.set_xlabel('时间步')
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label='值')
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
        plt.close(fig)
    return fig
