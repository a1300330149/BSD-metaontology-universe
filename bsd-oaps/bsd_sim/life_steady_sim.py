"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理8·全局相干公理 / 公理9·意义涌现公理
对应九维维度：意识维·能量场·信息维·物质维·时空维
理论出处：theory_base/L0_总本源层/全域大一统理论/生命五维稳态T87
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)、健康α∈[0.30,0.40]

BSD生命五维稳态仿真器
—— 仿真生命体五维（气/血/身/心/道）耦合动力学与全局相干稳态
   五维耦合 ODE 含阻尼项，RK4 数值积分，计算全局相干度 GC、气纯净度与健康等级
"""

import numpy as np

from bsd_engine.equations.life_steady_state import (
    five_dim_steady_state,
    qi_global_field,
    qi_purity,
    health_alpha_range,
)
from bsd_engine.equations.global_coherence import global_coherence, coherence_to_health
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E1, E2, E3


class LifeSteadySimulator:
    """
    生命五维稳态仿真器

    仿真生命体五维（气 qi / 血 blood / 身 body / 心 mind / 道 dao）的耦合动力学，
    计算全局相干度 GC、气纯净度与健康等级，支持扰动韧性测试。

    五维耦合 ODE 系统（含阻尼项，各维 ∈ [0,1]）：

        d(气)/dt = k_q·(0.4·血 + 0.4·心 + 0.2·道 - 气) - γ·η·(气 - 气_eq)
        d(血)/dt = k_b·(0.6·气 + 0.4·身 - 血) - γ·η·(血 - 血_eq)
        d(身)/dt = k_o·(血 - 身) - γ·η·(身 - 身_eq) + α·身·(1-身)
        d(心)/dt = k_m·(0.5·气 + 0.5·道 - 心) - γ·η·(心 - 心_eq)
        d(道)/dt = k_d·(0.5·气 + 0.5·心 - 道) - γ·η·(道 - 道_eq)

    其中 η 为阻尼强度，γ=GAMMA=0.92，α=ALPHA=0.18，平衡点 eq≈0.75。
    采用 RK4 数值积分。

    参数
    ----
    time_steps : int
        时间步数（默认 500）
    dt : float
        步长（默认 0.01）

    固定常量
    --------
    κ = KAPPA = 0.35，α = ALPHA = 0.18，γ = GAMMA = 0.92
    """

    DIMS = ("qi", "blood", "body", "mind", "dao")

    def __init__(self, time_steps=500, dt=0.01):
        self.time_steps = int(time_steps)
        self.dt = float(dt)
        self.kappa = KAPPA
        self.alpha = ALPHA
        self.gamma = GAMMA

        # 初始五维（默认中等稳态）
        self.initial_state = np.array([0.7, 0.7, 0.7, 0.7, 0.7], dtype=float)
        # 五维时间序列 (time_steps, 5)
        self.trajectory = None
        self.t = None
        # 全局相干度曲线
        self.gc_curve = None
        self.gc_type = None
        # 气纯净度曲线
        self.qi_purity_curve = None
        # 健康等级
        self.health_level = None
        self._results = None
        self._has_run = False

    def setup_subject(self, qi, blood, body, mind, dao):
        """
        设置初始五维参数。

        参数
        ----
        qi, blood, body, mind, dao : float
            五维初始值，自动裁剪到 [0,1]
        """
        self.initial_state = np.clip(
            np.array([qi, blood, body, mind, dao], dtype=float), 0.0, 1.0
        )
        self._has_run = False
        return self

    def _derivs(self, state):
        """五维耦合 ODE 右端函数（含阻尼项）。"""
        qi, blood, body, mind, dao = state
        # homeostatic 平衡点
        eq = 0.75
        # 耦合系数
        k_q, k_b, k_o, k_m, k_d = 0.6, 0.5, 0.4, 0.5, 0.45
        # 阻尼强度
        eta = 0.05
        damp = self.gamma

        d_qi = k_q * (0.4 * blood + 0.4 * mind + 0.2 * dao - qi) - damp * eta * (qi - eq)
        d_blood = k_b * (0.6 * qi + 0.4 * body - blood) - damp * eta * (blood - eq)
        d_body = k_o * (blood - body) - damp * eta * (body - eq) + self.alpha * body * (1.0 - body)
        d_mind = k_m * (0.5 * qi + 0.5 * dao - mind) - damp * eta * (mind - eq)
        d_dao = k_d * (0.5 * qi + 0.5 * mind - dao) - damp * eta * (dao - eq)

        return np.array([d_qi, d_blood, d_body, d_mind, d_dao])

    def _rk4_step(self, state, dt):
        """单步 RK4 积分。"""
        k1 = self._derivs(state)
        k2 = self._derivs(state + 0.5 * dt * k1)
        k3 = self._derivs(state + 0.5 * dt * k2)
        k4 = self._derivs(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def run(self):
        """
        执行五维耦合动力学仿真（RK4 积分）。

        每个时间步更新五维状态；以滑动窗口（长度 20）计算全局相干度 GC(t)
        与气纯净度（基于五维分布的结构熵与 GC），构成 GC 曲线与气纯净度曲线。
        """
        state = self.initial_state.copy()
        T = self.time_steps
        self.t = np.arange(T, dtype=float) * self.dt
        self.trajectory = np.zeros((T, 5))
        self.trajectory[0] = state

        dt = self.dt
        gc_curve = np.zeros(T)
        purity_curve = np.zeros(T)
        gc_curve[0] = 1.0
        purity_curve[0] = 0.0

        window = 20

        for n in range(1, T):
            state = self._rk4_step(state, dt)
            state = np.clip(state, 0.0, 1.0)
            self.trajectory[n] = state

            if n >= window:
                # 滑动窗口相干度：5 维 × window 样本
                seg = self.trajectory[n - window: n].T  # (5, window)
                gc_val, _, gc_type = global_coherence(seg, method="pearson")
                gc_curve[n] = gc_val
                self.gc_type = gc_type
                # 结构熵（五维分布的香农熵）
                p = state / (state.sum() + 1e-12)
                entropy = float(-np.sum(p * np.log(p + 1e-12)))
                # 气纯净度（标量输入返回标量）
                purity, _, _, _ = qi_purity(entropy, float(gc_val))
                purity_curve[n] = float(purity)
            else:
                gc_curve[n] = gc_curve[n - 1]
                purity_curve[n] = purity_curve[n - 1]

        self.gc_curve = gc_curve
        self.qi_purity_curve = purity_curve

        # 健康等级（基于末段平均 GC）
        self._compute_health_level()
        self._has_run = True
        return self

    def _compute_health_level(self):
        """基于末段 GC 计算健康等级与五维稳态评分。"""
        tail = self.gc_curve[max(1, self.time_steps - 50):]
        gc_mean = float(np.mean(tail))
        # 传入标量（coherence_to_health 标量分支返回标量，兼容 numpy 2.x）
        health_state, organ_systems, recommendation = coherence_to_health(gc_mean)

        # 五维稳态评分（末段状态）
        final = self.trajectory[-1]
        overall_score, dim_scores, steady_level, balance_index = five_dim_steady_state(
            final[0], final[1], final[2], final[3], final[4]
        )
        # α健康态：将五维按 强化/物质/本源 三组归并（气+心 / 血+身 / 道）
        a1 = float(final[0] + final[3])
        a2 = float(final[1] + final[2])
        a3 = float(final[4])
        is_healthy, health_score, _, _ = health_alpha_range(
            np.array([a1]), np.array([a2]), np.array([a3])
        )
        alpha_healthy = bool(is_healthy[0]) if hasattr(is_healthy, "__len__") else bool(is_healthy)

        # GC 时间积分（累积相干度），使用 np.trapezoid
        gc_integral = float(np.trapezoid(self.gc_curve, self.t))

        self.health_level = {
            "gc_mean": gc_mean,
            "gc_integral": gc_integral,
            "health_state": health_state,
            "organ_systems": {k: float(v) for k, v in organ_systems.items()},
            "recommendation": recommendation,
            "five_dim_overall_score": float(overall_score),
            "five_dim_scores": {k: float(v) for k, v in dim_scores.items()},
            "steady_level": steady_level,
            "balance_index": float(balance_index),
            "alpha_healthy": alpha_healthy,
        }

    def perturb(self, dimension, magnitude):
        """
        施加扰动测试韧性。

        从当前末状态出发，对指定维度注入扰动，继续演化 100 步观察恢复过程。

        参数
        ----
        dimension : str or int
            扰动维度："qi"/"blood"/"body"/"mind"/"dao" 或 0-4
        magnitude : float
            扰动幅度（可正可负）

        返回
        ----
        dict
            before / perturbed / recovered 状态、恢复轨迹、恢复步数、韧性判定
        """
        if self.trajectory is None:
            raise RuntimeError("请先调用 run()")
        if isinstance(dimension, str):
            dim_idx = self.DIMS.index(dimension)
        else:
            dim_idx = int(dimension)

        before = self.trajectory[-1].copy()
        perturb_vec = np.zeros(5)
        perturb_vec[dim_idx] = magnitude
        perturbed = np.clip(before + perturb_vec, 0.0, 1.0)

        # 从扰动状态继续演化 100 步
        state = perturbed.copy()
        recovery_traj = np.zeros((100, 5))
        recovery_traj[0] = state
        for n in range(1, 100):
            state = self._rk4_step(state, self.dt)
            state = np.clip(state, 0.0, 1.0)
            recovery_traj[n] = state

        # 恢复步数：扰动维度回到末态 ±5% 内的首个时刻
        target = before[dim_idx]
        recovery_steps = 100
        threshold = 0.05 * (target + 1e-6) + 0.02
        for n in range(1, 100):
            if abs(recovery_traj[n, dim_idx] - target) < threshold:
                recovery_steps = n
                break

        return {
            "dimension": self.DIMS[dim_idx],
            "before": before,
            "perturbed": perturbed,
            "recovered": recovery_traj[-1],
            "recovery_trajectory": recovery_traj,
            "recovery_steps": recovery_steps,
            "resilient": recovery_steps < 80,
        }

    def get_results(self):
        """
        返回五维时间序列、GC曲线、气纯净度、健康等级。

        返回
        ----
        dict
            time : 时间数组
            trajectory : 五维时间序列 (T, 5)
            dim_names : 五维名称
            gc_curve : 全局相干度曲线
            gc_type : 相干类型
            qi_purity_curve : 气纯净度曲线
            health_level : 健康等级与五维稳态评分
            qi_global_field_info : 气全局场信息
        """
        if not self._has_run:
            raise RuntimeError("请先调用 run() 执行仿真")

        # 气全局场（基于末段相干度配置）
        gc_mean = self.health_level["gc_mean"]
        _, field_strength, penetration, field_type = qi_global_field({
            "center": np.array([0.0, 0.0, 0.0]),
            "radius": 1.0,
            "strength": float(self.trajectory[-1, 0]),
            "coherence": gc_mean,
            "kappa": self.kappa,
        })

        self._results = {
            "time": self.t,
            "trajectory": self.trajectory,
            "dim_names": list(self.DIMS),
            "gc_curve": self.gc_curve,
            "gc_type": self.gc_type,
            "qi_purity_curve": self.qi_purity_curve,
            "health_level": self.health_level,
            "qi_global_field_info": {
                "field_strength": float(field_strength),
                "penetration_depth": float(penetration),
                "field_type": field_type,
            },
        }
        return self._results
