"""
归属基底：第0重元道本源基底
对应三界秩序：天道
对应公理：全域公理可视化支撑
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35
【理论版本：ACTIVE-V1.8】

BSD-OAPS 可视化工具包
—— 适配 T90 V1.8 双时针动力学可视化
"""

from .wave_plots import (
    plot_standing_wave_snapshot,
    plot_standing_wave_evolution,
    plot_boundary_resilience,
    plot_wave_energy_distribution,
    plot_standing_wave_dashboard,
)

from .phase_emergence_plots import (
    plot_phase_diagram,
    plot_free_energy_landscape,
    plot_emergence_dynamics,
    plot_kuramoto_sync,
    plot_critical_exponents,
)

__all__ = [
    # wave_plots
    "plot_standing_wave_snapshot",
    "plot_standing_wave_evolution",
    "plot_boundary_resilience",
    "plot_wave_energy_distribution",
    "plot_standing_wave_dashboard",
    # phase_emergence_plots
    "plot_phase_diagram",
    "plot_free_energy_landscape",
    "plot_emergence_dynamics",
    "plot_kuramoto_sync",
    "plot_critical_exponents",
]
