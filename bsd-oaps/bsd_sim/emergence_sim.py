"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理9·意义涌现公理 / 公理8·意义守恒公理
对应九维维度：意识维·意义维·命运维
理论出处：theory_base/L0_总本源层/全域大一统理论/涌现场与自组织
固定数理常量：κ=0.35 (KAPPA)、γ=0.92 (GAMMA)、α=0.18 (ALPHA)

BSD涌现场仿真器
—— Kuramoto 多体同步动力学下的涌现行为仿真
"""

import numpy as np

from bsd_engine.equations.emergence import (
    emergence_measure,
    self_organization_strength,
    irreducibility_index,
    emergence_phase_transition,
)
from bsd_engine.axioms.eight_unification_axioms import verify_ternary_emergence
from bsd_engine.registry.constants import KAPPA, GAMMA, ALPHA


class EmergenceSimulator:
    """
    涌现场仿真器

    仿真多组件系统的涌现行为，基于 Kuramoto 同步动力学

        dθ_i/dt = ω_i + Σ_j K_ij · sin(θ_j - θ_i)

    计算涌现强度随时间演化、自组织强度、不可还原性指数，并检测相变涌现点。

    参数
    ----
    num_components : int
        组件数 N（默认 50）
    time_steps : int
        时间步数（默认 500）

    固定常量
    --------
    κ = KAPPA = 0.35（默认全局耦合强度）
    γ = GAMMA = 0.92，α = ALPHA = 0.18
    """

    def __init__(self, num_components=50, time_steps=500):
        self.N = int(num_components)
        self.time_steps = int(time_steps)
        self.kappa = KAPPA
        self.gamma = GAMMA
        self.alpha = ALPHA

        self.coupling = None      # (N, N) 耦合矩阵
        self.omega = None         # (N,) 固有频率
        self.theta = None         # (time_steps, N) 相位时间序列
        self.t = None             # (time_steps,) 时间数组
        self.emergence_curve = None   # (time_steps,) Kuramoto 序参量 r(t)
        self._order_param_z = None
        self.so_strength = None
        self.irr_index = None
        self._results = None
        self._has_run = False

    def setup_interactions(self, coupling_matrix):
        """
        设置组件间耦合矩阵 K_ij。

        参数
        ----
        coupling_matrix : scalar / 1d array / 2d array
            标量 → 全局均匀耦合；1d → 外积耦合；2d → 直接采用（自动规整为 N×N）
        """
        K = np.asarray(coupling_matrix, dtype=float)
        if K.ndim == 0:
            K = float(K) * np.ones((self.N, self.N))
        elif K.ndim == 1:
            K = np.resize(K, (self.N, self.N))
            K = (K + K.T) / 2.0
        elif K.shape != (self.N, self.N):
            K = np.resize(K, (self.N, self.N))
        np.fill_diagonal(K, 0.0)
        self.coupling = K

        # 固有频率（正态分布）与初始相位（均匀随机），使用固定种子保证可复现
        rng = np.random.default_rng(42)
        self.omega = rng.normal(0.0, 1.0, size=self.N)
        self.theta = np.zeros((self.time_steps, self.N))
        self.theta[0] = rng.uniform(0.0, 2.0 * np.pi, size=self.N)
        self.t = np.linspace(0.0, 1.0, self.time_steps)
        self._has_run = False
        return self

    def run(self):
        """
        执行 Kuramoto 多体动力学仿真。

        采用前向欧拉积分 dθ_i/dt = ω_i + Σ_j K_ij·sin(θ_j - θ_i)，
        相位模 2π 归一，记录每步相位以供涌现分析。
        """
        if self.coupling is None:
            # 默认全局耦合，强度=κ
            self.setup_interactions(self.kappa)

        dt = self.t[1] - self.t[0]
        theta = self.theta.copy()
        K = self.coupling
        omega = self.omega

        for n in range(1, self.time_steps):
            th = theta[n - 1]
            # Σ_j K_ij sin(θ_j - θ_i) ：(N,N) * sin(θ_j - θ_i)
            coupling_term = (K * np.sin(th[None, :] - th[:, None])).sum(axis=1)
            dtheta = omega + coupling_term
            theta[n] = np.mod(th + dt * dtheta, 2.0 * np.pi)
        self.theta = theta

        # 涌现强度曲线（Kuramoto 序参量 r(t)）
        self._compute_emergence_curve()

        self._has_run = True
        return self

    def _compute_emergence_curve(self):
        """计算 Kuramoto 序参量 r(t) = |<e^{iθ}>| 作为涌现强度曲线。"""
        z = np.mean(np.exp(1j * self.theta), axis=1)  # (time_steps,)
        self.emergence_curve = np.abs(z)
        self._order_param_z = z

    def detect_emergence_threshold(self):
        """
        检测涌现相变点。

        基于相位时间序列协方差谱的极化率突变，定位涌现临界时刻。

        返回
        ----
        dict
            critical_point : 涌现临界时刻
            order_parameter : 序参量曲线
            susceptibility : 涌现极化率
        """
        if self.theta is None:
            raise RuntimeError("请先调用 run()")
        critical_point, order_param, susceptibility = emergence_phase_transition(
            self.theta, self.t
        )
        return {
            "critical_point": float(critical_point),
            "order_parameter": order_param,
            "susceptibility": susceptibility,
        }

    def get_results(self):
        """
        返回涌现强度曲线、自组织强度、不可还原性指数及公理验证结果。

        返回
        ----
        dict
            emergence_curve : 涌现强度 r(t)
            time : 时间数组
            phases : 相位时间序列
            self_organization : 自组织强度与熵
            irreducibility : 不可还原性指数
            global_emergence : 全局涌现度量
            emergence_threshold : 涌现相变检测结果
            axiom_checks : 公理验证结果
        """
        if not self._has_run:
            raise RuntimeError("请先调用 run() 执行仿真")

        # 自组织强度
        so, S0, Sf, conn = self_organization_strength(self.coupling, self.theta)
        self.so_strength = {
            "strength": float(so),
            "entropy_initial": float(S0),
            "entropy_final": float(Sf),
            "connectivity": float(conn),
        }

        # 不可还原性指数：宏观 r(t) 能否由各组件相位线性重构
        irr, residual, best_fit = irreducibility_index(self.theta, self.emergence_curve)
        self.irr_index = {
            "index": float(irr),
            "residual": residual,
            "best_fit": best_fit,
        }

        # 全局涌现度量（信息论）
        micro_states = [self.theta[:, i] for i in range(self.N)]
        macro_state = self.emergence_curve
        E, H_micro, H_macro = emergence_measure(micro_states, macro_state)

        # 涌现相变检测
        threshold = self.detect_emergence_threshold()

        # 公理验证：三元分层涌现（公理一）
        ax_em, ax_em_msg = verify_ternary_emergence({
            "ternary_elements": ["individuality", "relationality", "changeability"],
            "emerged_layers": ["synchronization", "collective_order"],
            "individuality": float(np.std(self.omega)),
            "relationality": float(np.mean(np.abs(self.coupling))),
            "changeability": float(np.std(self.emergence_curve)),
        })

        self._results = {
            "emergence_curve": self.emergence_curve,
            "time": self.t,
            "phases": self.theta,
            "self_organization": self.so_strength,
            "irreducibility": self.irr_index,
            "global_emergence": {
                "emergence_strength": float(E),
                "micro_entropy": float(H_micro),
                "macro_entropy": float(H_macro),
            },
            "emergence_threshold": threshold,
            "axiom_checks": {
                "ternary_emergence": {"passed": ax_em, "message": ax_em_msg},
            },
        }
        return self._results
