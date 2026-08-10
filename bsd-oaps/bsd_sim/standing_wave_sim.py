"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理0·元道存在 / 公理6·双极性创生
对应九维维度：时间流·空间体·能量场
理论出处：theory_base/L0_总本源层/全域大一统理论/四位一体驻波动力学框架
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)

BSD驻波动力学仿真器
—— 三层驻波结构（内核层/中层/外层）的有限差分时间演化仿真
"""

import numpy as np

from bsd_engine.equations.standing_wave import (
    wave_equation,
    boundary_resilience,
    standing_wave_mode,
    wave_interference,
)
from bsd_engine.axioms.eight_unification_axioms import (
    verify_boundary_resilience as ax_verify_boundary_resilience,
    verify_standing_wave_topology,
)
from bsd_engine.registry.constants import KAPPA, GAMMA, ALPHA

# numpy 2.x 移除了 np.trapz，改用 np.trapezoid；保留对旧版本的兼容
_trapz = getattr(np, "trapezoid", None) or np.trapz


class StandingWaveSimulator:
    """
    三层驻波动力学仿真器

    仿真内核层 / 中层 / 外层三层嵌套驻波结构的时间演化，使用有限差分法
    求解波动方程 ∂²ψ/∂t² = κ²·∇²ψ，计算层间边界韧性随时间演化及驻波干涉模式。

    三层腔体长度递增（内核最短、外层最长），各层以同一模态阶数 n 初始化，
    因长度不同而具备不同固有频率 ωₙ = nπκ/L，从而产生丰富的层间干涉。

    参数
    ----
    num_points : int
        每层空间网格点数（默认 200）
    time_steps : int
        时间步数（默认 1000）

    固定常量
    --------
    κ = KAPPA = 0.35（虚实阻尼系数，兼作波速）
    γ = GAMMA = 0.92（时序衰减系数）
    α = ALPHA = 0.18（稀疏补偿系数）
    """

    LAYER_NAMES = ("kernel", "middle", "outer")  # 内核层 / 中层 / 外层

    def __init__(self, num_points=200, time_steps=1000):
        self.num_points = int(num_points)
        self.time_steps = int(time_steps)

        # 锁档常量
        self.kappa = KAPPA
        self.gamma = GAMMA
        self.alpha = ALPHA

        # 三层嵌套腔体长度（内核最短，外层最长）
        self.layer_lengths = {"kernel": 1.0, "middle": 2.0, "outer": 3.0}

        # 由 setup_wave / run 填充
        self.mode_n = 1
        self.dt = None
        self.t = None
        self.x = {name: None for name in self.LAYER_NAMES}
        self.psi = {name: None for name in self.LAYER_NAMES}
        self.boundary_resilience_series = None
        self.energy_distribution = None
        self.interference = None
        self._results = None
        self._has_run = False

    def setup_wave(self, mode_n, kappa):
        """
        设置初始驻波条件。

        参数
        ----
        mode_n : int
            驻波模态阶数 n ≥ 1
        kappa : float
            波速系数 κ（虚实阻尼系数），覆盖默认锁档值
        """
        self.mode_n = int(mode_n)
        self.kappa = float(kappa)

        # CFL 稳定性条件：c·dt/dx ≤ 1。取最短层（最小 dx）作为最严约束。
        min_L = min(self.layer_lengths.values())
        dx_min = min_L / (self.num_points - 1)
        self.dt = 0.4 * dx_min / self.kappa  # 安全系数 0.4
        self.t = np.linspace(0.0, self.dt * (self.time_steps - 1), self.time_steps)

        # 为每层生成空间网格与初始驻波模态
        for name in self.LAYER_NAMES:
            L = self.layer_lengths[name]
            x, psi_n, _ = standing_wave_mode(
                self.mode_n, L, kappa=self.kappa, t=0.0, num_points=self.num_points
            )
            self.x[name] = x
            field = np.zeros((self.time_steps, self.num_points))
            field[0] = psi_n
            # 用 t=dt 的解析模态启动差分（二阶起步需要两个时间层）
            if self.time_steps > 1:
                _, psi_dt, _ = standing_wave_mode(
                    self.mode_n, L, kappa=self.kappa, t=self.dt, num_points=self.num_points
                )
                field[1] = psi_dt
            self.psi[name] = field

        self._has_run = False
        return self

    def run(self):
        """
        执行时间演化仿真。

        使用有限差分法（显式 leapfrog）求解 ∂²ψ/∂t² = κ²·∇²ψ：
            ψ^{n+1}_i = 2ψ^n_i - ψ^{n-1}_i + r·(ψ^n_{i+1} - 2ψ^n_i + ψ^n_{i-1})
        其中 r = (κ·dt/dx)²。腔体两端固定边界 ψ=0。
        """
        if self.psi["kernel"] is None:
            raise RuntimeError("请先调用 setup_wave(mode_n, kappa) 设置初始条件")

        c = self.kappa
        for name in self.LAYER_NAMES:
            x = self.x[name]
            dx = x[1] - x[0]
            r = (c * self.dt / dx) ** 2
            field = self.psi[name]
            field[:, 0] = 0.0
            field[:, -1] = 0.0
            for n in range(1, self.time_steps - 1):
                cur = field[n]
                nxt = field[n + 1]
                nxt[1:-1] = (
                    2.0 * cur[1:-1]
                    - field[n - 1, 1:-1]
                    + r * (cur[2:] - 2.0 * cur[1:-1] + cur[:-2])
                )
                nxt[0] = 0.0
                nxt[-1] = 0.0
            self.psi[name] = field

        # 边界韧性随时间演化（基于各层瞬时能量权重）
        self._compute_boundary_resilience()
        # 驻波干涉模式（层间）
        self._compute_interference()
        # 能量分布
        self._compute_energy_distribution()

        self._has_run = True
        return self

    def _compute_boundary_resilience(self):
        """基于各层瞬时能量权重计算层间边界韧性 τ(t) 的演化。"""
        ts = self.time_steps
        tau_series = np.zeros(ts)
        for n in range(ts):
            energies = np.array([
                _trapz(self.psi[name][n] ** 2, self.x[name])
                for name in self.LAYER_NAMES
            ])
            total = energies.sum() + 1e-12
            w = energies / total  # 归一化权重 ∈ [0,1]
            # α₁=内核(主导项), α₂=中层, α₃=外层(抑制项)
            tau = boundary_resilience(
                tau_0=1.0,
                alpha_1=float(w[0]),
                alpha_2=float(w[1]),
                alpha_3=float(w[2]),
            )
            tau_series[n] = tau
        self.boundary_resilience_series = tau_series

    def _compute_interference(self):
        """计算层间驻波干涉（插值到中层参考网格）。"""
        x_ref = self.x["middle"]
        psi_k = np.interp(x_ref, self.x["kernel"], self.psi["kernel"][-1])
        psi_m = self.psi["middle"][-1]
        psi_o = np.interp(x_ref, self.x["outer"], self.psi["outer"][-1])

        total_km, inter_km, vis_km = wave_interference(psi_k, psi_m)
        total_mo, inter_mo, vis_mo = wave_interference(psi_m, psi_o)

        self.interference = {
            "kernel_middle": {
                "total": total_km,
                "interference_term": inter_km,
                "visibility": float(vis_km),
            },
            "middle_outer": {
                "total": total_mo,
                "interference_term": inter_mo,
                "visibility": float(vis_mo),
            },
        }

    def _compute_energy_distribution(self):
        """
        计算各层驻波能量密度与总能量。

        能量密度 E = (1/2)(∂ψ/∂t)² + (κ²/2)(∂ψ/∂x)²，
        总能量对空间与时间积分。（与 equations.standing_wave_energy 同构，
        但使用 trapz 兼容垫片以适配 numpy 2.x。）
        """
        dt = self.t[1] - self.t[0]
        energy_dist = {}
        for name in self.LAYER_NAMES:
            x = self.x[name]
            dx = x[1] - x[0]
            psi = self.psi[name]
            dpsi_dt = np.gradient(psi, dt, axis=0)
            dpsi_dx = np.gradient(psi, dx, axis=1)
            kinetic = 0.5 * dpsi_dt ** 2
            potential = 0.5 * (self.kappa ** 2) * dpsi_dx ** 2
            ed = kinetic + potential
            total = float(_trapz(_trapz(ed, x, axis=1), self.t, axis=0))
            energy_dist[name] = {"density": ed, "total": total}
        self.energy_distribution = energy_dist

    def get_wave_snapshot(self, t):
        """
        获取某时刻 t 的三层波形快照。

        参数
        ----
        t : float
            目标时刻（自动取最近时间步）

        返回
        ----
        dict
            每层包含 x 网格、振幅 ψ、实际采样时刻
        """
        if self.t is None:
            raise RuntimeError("请先调用 setup_wave 与 run")
        idx = int(np.clip(np.argmin(np.abs(self.t - t)), 0, self.time_steps - 1))
        snapshot = {}
        for name in self.LAYER_NAMES:
            snapshot[name] = {
                "x": self.x[name],
                "psi": self.psi[name][idx],
                "t": float(self.t[idx]),
            }
        return snapshot

    def get_results(self):
        """
        返回驻波振幅、边界韧性、能量分布及公理验证结果。

        返回
        ----
        dict
            amplitudes : 各层波场 (time_steps × num_points)
            x_grids : 各层空间网格
            time : 时间数组
            boundary_resilience : 边界韧性时间序列
            energy_distribution : 各层能量密度与总能量
            interference : 层间干涉场与可见度
            wave_equation_residual : 波动方程残差（内核层）
            axiom_checks : 公理验证结果
        """
        if not self._has_run:
            raise RuntimeError("请先调用 run() 执行仿真")

        # 波动方程残差检验（内核层）
        _, _, residual = wave_equation(
            self.psi["kernel"], self.t, self.x["kernel"], kappa=self.kappa
        )

        # 公理验证：边界韧性稳态（公理五）
        tau_mean = float(np.mean(self.boundary_resilience_series))
        ax_boundary, ax_boundary_msg = ax_verify_boundary_resilience({
            "boundary_flexibility": float(np.std(self.boundary_resilience_series)) + 1e-3,
            "system_stability": min(tau_mean, 1.0),
            "boundary_stretch": float(np.max(self.boundary_resilience_series)),
            "boundary_repair": float(np.min(self.boundary_resilience_series)) + 1e-3,
        })

        # 公理验证：驻波拓扑收敛（公理六）
        vis_km = self.interference["kernel_middle"]["visibility"]
        ax_topo, ax_topo_msg = verify_standing_wave_topology({
            "incident_wave": float(np.max(np.abs(self.psi["kernel"][-1]))),
            "reflected_wave": float(np.max(np.abs(self.psi["middle"][-1]))),
            "steady_pattern": True,
            "convergence_degree": float(vis_km),
        })

        self._results = {
            "amplitudes": {name: self.psi[name] for name in self.LAYER_NAMES},
            "x_grids": {name: self.x[name] for name in self.LAYER_NAMES},
            "time": self.t,
            "boundary_resilience": self.boundary_resilience_series,
            "energy_distribution": self.energy_distribution,
            "interference": self.interference,
            "wave_equation_residual": residual,
            "axiom_checks": {
                "boundary_resilience": {"passed": ax_boundary, "message": ax_boundary_msg},
                "standing_wave_topology": {"passed": ax_topo, "message": ax_topo_msg},
            },
        }
        return self._results
