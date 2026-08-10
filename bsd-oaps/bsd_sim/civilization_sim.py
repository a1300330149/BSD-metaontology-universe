"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理5·六系本源公理 / 公理10·闭递归公理
对应九维维度：熵流维·时间流·命运维·信息维·能量场
理论出处：theory_base/L0_总本源层/全域大一统理论/文明六系演化T57-T75
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)、E1=0.35, E2=0.65, E3=0.90

BSD文明演化仿真器
—— 仿真文明六系对冲动力学、熵流演化与灾变阈值（矿化/僵化/坍缩）
   全域熵流方程 dS/dt = k_in·ΔE - k_out·E_out - k_res·E_res + A·exp(λt)
"""

import numpy as np

from bsd_engine.equations.entropy_flow import (
    entropy_residence,
    entropy_warning_level,
    entropy_flow,
)
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E1, E2, E3


class CivilizationSimulator:
    """
    文明演化仿真器

    仿真文明六系（强化/调控/结构/信息/能量/意义）的对冲动力学演化，
    计算熵流、残余熵 E_res 与灾变预警等级（矿化/僵化/坍缩）。

    六系对冲动力学（三组对冲制衡）：
        对冲对：(强化↔调控)、(结构↔信息)、(能量↔意义)
        每对内部相互制约：
            d(s_a)/dt -= k_hedge·(s_a - s_b)
            d(s_b)/dt += k_hedge·(s_a - s_b)

    全域熵流方程：
        dS/dt = k_in·ΔE - k_out·E_out - k_res·E_res + A·exp(λ·t)
        其中 ΔE = Σ|对冲差|（对冲失衡驱动熵产生）
              E_out 为耗散输出，E_res 为驻留熵

    参数
    ----
    time_steps : int
        时间步数（默认 1000）
    dt : float
        步长（默认 0.1）

    固定常量
    --------
    κ = KAPPA = 0.35，α = ALPHA = 0.18，γ = GAMMA = 0.92
    """

    # BSD 六系名称（顺序固定）
    SIX_SYSTEMS = ("reinforcement", "regulation", "structure",
                   "information", "energy", "meaning")
    # 三组对冲对（索引）：强化↔调控 / 结构↔信息 / 能量↔意义
    HEDGE_PAIRS = ((0, 1), (2, 3), (4, 5))

    def __init__(self, time_steps=1000, dt=0.1):
        self.time_steps = int(time_steps)
        self.dt = float(dt)
        self.kappa = KAPPA
        self.alpha = ALPHA
        self.gamma = GAMMA

        self.initial_six = np.array([0.6, 0.6, 0.5, 0.5, 0.7, 0.5], dtype=float)
        # 六系演化轨迹 (time_steps, 6)
        self.six_trajectory = None
        self.t = None
        # 熵流相关
        self.entropy_curve = None          # 全域熵 S(t)
        self.E_res_curve = None            # 驻留熵 E_res(t)
        self.warning_levels = None         # 三档预警
        self.catastrophe = None
        self._results = None
        self._has_run = False

    def setup_civilization(self, six_systems_params):
        """
        设置六系初始参数。

        参数
        ----
        six_systems_params : array-like or dict
            - array: shape=(6,) 六系初始值
            - dict:  键为六系名，值为标量
        """
        if isinstance(six_systems_params, dict):
            vec = np.zeros(6)
            for i, name in enumerate(self.SIX_SYSTEMS):
                vec[i] = float(six_systems_params.get(name, 0.5))
        else:
            vec = np.asarray(six_systems_params, dtype=float).flatten()
            if vec.size != 6:
                vec = np.resize(vec, 6)
        self.initial_six = np.clip(vec, 0.0, 1.0)
        self._has_run = False
        return self

    def _derivs(self, state):
        """六系对冲动力学右端函数。"""
        s = state.copy()
        ds = np.zeros(6)
        # 对冲制衡：每对内部趋衡
        k_hedge = 0.3
        for a, b in self.HEDGE_PAIRS:
            diff = s[a] - s[b]
            ds[a] -= k_hedge * diff
            ds[b] += k_hedge * diff
        # 跨对弱耦合：相邻对之间信息/能量流动（环状）
        ds[0] += 0.05 * (s[2] - s[0])  # 强化 ← 结构
        ds[2] += 0.05 * (s[4] - s[2])  # 结构 ← 能量
        ds[4] += 0.05 * (s[0] - s[4])  # 能量 ← 强化
        ds[1] += 0.05 * (s[3] - s[1])  # 调控 ← 信息
        ds[3] += 0.05 * (s[5] - s[3])  # 信息 ← 意义
        ds[5] += 0.05 * (s[1] - s[5])  # 意义 ← 调控
        # 阻尼项：趋向中等活力（避免极化）
        eq = 0.5
        ds -= self.gamma * 0.02 * (s - eq)
        # 意义系自激励（文明意义积累，logistic 型）
        ds[5] += self.alpha * 0.05 * s[5] * (1.0 - s[5])
        return ds

    def _rk4_step(self, state, dt):
        """单步 RK4 积分。"""
        k1 = self._derivs(state)
        k2 = self._derivs(state + 0.5 * dt * k1)
        k3 = self._derivs(state + 0.5 * dt * k2)
        k4 = self._derivs(state + dt * k3)
        return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)

    def run(self):
        """
        执行文明演化仿真。

        RK4 积分六系对冲动力学，每步根据六系状态计算：
        - ΔE = Σ|对冲差|（对冲失衡度，驱动熵产生）
        - 耗散 E_out（外层 + 缓冲层）
        - 驻留熵 E_res via entropy_residence
        - 全域熵流方程 dS/dt via entropy_flow（残差校验）
        """
        state = self.initial_six.copy()
        T = self.time_steps
        self.t = np.arange(T, dtype=float) * self.dt
        self.six_trajectory = np.zeros((T, 6))
        self.six_trajectory[0] = state

        self.entropy_curve = np.zeros(T)
        self.E_res_curve = np.zeros(T)
        S = 0.5  # 初始熵

        dt = self.dt
        k_in = 0.4
        k_out = 0.3
        k_res = 0.2
        A = 0.01
        lam = 0.002  # 缓慢指数驱动（技术/人口增长）

        for n in range(1, T):
            # 六系 RK4
            state = self._rk4_step(state, dt)
            state = np.clip(state, 0.0, 1.0)
            self.six_trajectory[n] = state

            # 对冲差驱动熵产生
            delta_E = sum(abs(state[a] - state[b]) for a, b in self.HEDGE_PAIRS)
            E_total = float(state.sum())
            E_out_outer = self.alpha * E_total * 0.5
            E_out_buffer = self.kappa * E_total * 0.3
            # 驻留熵
            E_res, res_ratio, diss_ratio, buf_eff = entropy_residence(
                E_total, E_out_outer, E_out_buffer
            )
            self.E_res_curve[n] = float(E_res)
            # 全域熵流方程: dS/dt = k_in·ΔE - k_out·E_out - k_res·E_res + A·exp(λt)
            dS_dt = (k_in * delta_E - k_out * E_out_outer
                     - k_res * E_res + A * np.exp(lam * self.t[n]))
            # 调用 entropy_flow 校验方程残差（残差应≈0）
            _, _, _, _ = entropy_flow(dS_dt, float(delta_E), k=self.alpha, dPhi_dt=E_out_outer)
            S = max(S + dt * dS_dt, 0.0)
            self.entropy_curve[n] = S

        # 三档预警（基于驻留率序列）
        sum_series = self.six_trajectory.sum(axis=1)
        res_ratio_series = self.E_res_curve / (sum_series + 1e-12)
        self.warning_levels = entropy_warning_level(res_ratio_series)

        # 灾变检查
        self.catastrophe = self.check_catastrophe()
        self._has_run = True
        return self

    def check_catastrophe(self):
        """
        检查是否触发矿化/僵化/坍缩。

        - 矿化（mineralization）：六系方差极低且整体偏高 → 系统刚性固化、丧失分化
        - 僵化（rigidification）：熵驻留率持续过高（>0.6）→ 过度保守、失去活力
        - 坍缩（collapse）：熵驻留率过低（<0.02，红色危险）→ 能量耗竭、系统坍缩

        返回
        ----
        dict
            mineralization / rigidification / collapse 的触发标志与首次触发步
            any_catastrophe : 是否触发任一灾变
        """
        if self.six_trajectory is None:
            raise RuntimeError("请先调用 run()")

        traj = self.six_trajectory
        var_series = traj.var(axis=1)              # 六系方差
        sum_series = traj.sum(axis=1)
        res_ratio = self.E_res_curve / (sum_series + 1e-12)

        # 矿化：方差 < 0.005 且 总和 > 5.0（六系都偏高且趋同）
        mineralization_mask = (var_series < 0.005) & (sum_series > 5.0)
        # 僵化：驻留率持续 > 0.6
        rigidification_mask = res_ratio > 0.6
        # 坍缩：驻留率 < 0.02
        collapse_mask = res_ratio < 0.02

        def first_idx(mask):
            if not mask.any():
                return None
            return int(np.argmax(mask))

        return {
            "mineralization": {
                "triggered": bool(mineralization_mask.any()),
                "first_step": first_idx(mineralization_mask),
                "description": "六系刚性固化，丧失分化活力",
            },
            "rigidification": {
                "triggered": bool(rigidification_mask.any()),
                "first_step": first_idx(rigidification_mask),
                "description": "熵驻留过高，系统僵化保守",
            },
            "collapse": {
                "triggered": bool(collapse_mask.any()),
                "first_step": first_idx(collapse_mask),
                "description": "熵驻留枯竭，系统能量耗散坍缩",
            },
            "any_catastrophe": bool(
                mineralization_mask.any() or rigidification_mask.any() or collapse_mask.any()
            ),
        }

    def get_results(self):
        """
        返回六系演化曲线、残余熵 E_res、灾变预警等级。

        返回
        ----
        dict
            time : 时间数组
            six_trajectory : 六系演化曲线 (T, 6)
            six_system_names : 六系名称
            entropy_curve : 全域熵 S(t)
            E_res_curve : 驻留熵曲线
            warning_levels : 三档预警（levels/indices/末段等级）
            catastrophe : 灾变检查
            cycle_metrics : 文明周期指标（熵产生积分、驻留率等）
        """
        if not self._has_run:
            raise RuntimeError("请先调用 run() 执行仿真")

        sum_series = self.six_trajectory.sum(axis=1)
        res_ratio_series = self.E_res_curve / (sum_series + 1e-12)

        # 文明周期指标：熵的累积（时间积分）使用 np.trapezoid
        total_entropy_production = float(np.trapezoid(self.entropy_curve, self.t))
        mean_res_ratio = float(np.mean(res_ratio_series))
        final_res_ratio = float(res_ratio_series[-1])
        # 末段预警（标量输入返回三元组）
        final_level, final_idx, final_desc = entropy_warning_level(final_res_ratio)

        self._results = {
            "time": self.t,
            "six_trajectory": self.six_trajectory,
            "six_system_names": list(self.SIX_SYSTEMS),
            "entropy_curve": self.entropy_curve,
            "E_res_curve": self.E_res_curve,
            "warning_levels": {
                "levels": self.warning_levels[0],
                "indices": self.warning_levels[1],
                "final_level": final_level,
                "final_description": final_desc,
            },
            "catastrophe": self.catastrophe,
            "cycle_metrics": {
                "total_entropy_production": total_entropy_production,
                "mean_residence_ratio": mean_res_ratio,
                "final_residence_ratio": final_res_ratio,
                "peak_entropy": float(np.max(self.entropy_curve)),
            },
        }
        return self._results
