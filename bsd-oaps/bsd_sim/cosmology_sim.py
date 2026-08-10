"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理1·虚空创生公理 / 公理11·宿命双界公理
对应九维维度：时空维·物质维·能量场·信息维·意识维
理论出处：theory_base/L0_总本源层/全域大一统理论/宇宙学常数T87第八章
固定数理常量：Λ=1.106×10⁻⁵² m⁻²、κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)

BSD宇宙学仿真器
—— 基于 Friedmann 方程仿真宇宙学常数Λ驱动的宇宙演化
   验证BSD理论值与Planck观测值的一致性（Λ=1.106×10⁻⁵² m⁻² vs 1.109×10⁻⁵² m⁻²）
"""

import numpy as np

from bsd_engine.equations.cosmological_constant import (
    lambda_theoretical,
    lambda_observed,
    lambda_error,
    lambda_from_bsd,
    poincare_verification,
    universe_evolution,
)
from bsd_engine.registry.constants import (
    KAPPA, ALPHA, GAMMA,
    COSMOLOGICAL_CONSTANT, COSMOLOGICAL_CONSTANT_OBSERVED,
)


class CosmologySimulator:
    """
    宇宙学仿真器

    仿真宇宙学常数 Λ 驱动的宇宙演化，验证 BSD 理论值与 Planck 观测值的一致性。

    Friedmann 方程（ΛCDM）：
        (da/dt)² = H₀²·(Ω_m·a⁻¹ + Ω_r·a⁻² + Ω_Λ·a²)
        等价：H(a) = H₀·sqrt(Ω_m/a³ + Ω_r/a⁴ + Ω_k/a² + Ω_Λ)
              da/dt = a·H(a)

    数值积分：在尺度因子 a 上对数采样（早期辐射主导需密集采样），
    反推宇宙时间 t(a) = ∫ da/(a·H(a))，输出 a(t) 与 H(t)，
    并与 equations.universe_evolution 交叉验证。

    参数
    ----
    time_steps : int
        时间步数（默认 200）

    固定常量
    --------
    Λ = COSMOLOGICAL_CONSTANT = 1.106×10⁻⁵² m⁻²
    κ = 0.35，α = 0.18，γ = 0.92
    H₀ = 67.66 km/s/Mpc（Planck 2018）
    """

    # 物理常量（SI）
    C = 299792458.0                          # 光速 m/s
    G = 6.67430e-11                          # 引力常数
    H0_SI = 67.66e3 / 3.0856775814913673e22  # H₀ in 1/s
    MPC = 3.0856775814913673e22              # 1 Mpc in m
    GYR = 3.15576e16                         # 1 Gyr in s

    def __init__(self, time_steps=200):
        self.time_steps = int(time_steps)
        self.kappa = KAPPA
        self.alpha = ALPHA
        self.gamma = GAMMA

        # 宇宙学参数（Planck 2018 默认）
        self.Lambda = float(COSMOLOGICAL_CONSTANT)
        self.Omega_m = 0.3111
        self.Omega_r = 9.0e-5
        self.Omega_k = 0.0007
        self.Omega_Lambda = 1.0 - self.Omega_m - self.Omega_r - self.Omega_k

        # 仿真结果
        self.t = None              # 时间数组（Gyr）
        self.scale_factor = None   # a(t)
        self.hubble_param = None   # H(t) in 1/Gyr
        self._results = None
        self._has_run = False

    def setup_universe(self, Lambda, Omega_m, Omega_r):
        """
        设置宇宙学参数。

        参数
        ----
        Lambda : float
            宇宙学常数 Λ (m⁻²)
        Omega_m : float
            物质密度参数 Ω_m
        Omega_r : float
            辐射密度参数 Ω_r

        说明
        ----
        Ω_Λ 由 Λ 反推：Λ = 3·Ω_Λ·H₀²/c² → Ω_Λ = Λ·c²/(3·H₀²)
        Ω_k = 1 - Ω_m - Ω_r - Ω_Λ
        """
        self.Lambda = float(Lambda)
        self.Omega_m = float(Omega_m)
        self.Omega_r = float(Omega_r)
        H0 = self.H0_SI
        self.Omega_Lambda = self.Lambda * self.C ** 2 / (3.0 * H0 ** 2)
        self.Omega_k = 1.0 - self.Omega_m - self.Omega_r - self.Omega_Lambda
        self._has_run = False
        return self

    def _hubble_a(self, a):
        """哈勃参数 H(a) = H₀·sqrt(Ω_m/a³ + Ω_r/a⁴ + Ω_k/a² + Ω_Λ)，返回 1/s。"""
        a = max(float(a), 1e-30)
        H2 = (self.Omega_m / a ** 3 + self.Omega_r / a ** 4
              + self.Omega_k / a ** 2 + self.Omega_Lambda)
        return self.H0_SI * np.sqrt(max(H2, 0.0))

    def _dadt(self, a):
        """da/dt = a·H(a)，单位 1/s。"""
        return a * self._hubble_a(a)

    def run(self):
        """
        执行宇宙演化仿真（从大爆炸到当前及未来）。

        在尺度因子 a 上对数采样（从 a_start=1e-6 到 a_end=2.0），
        中点法积分宇宙时间 t(a) = ∫ da/(a·H(a))：
            dt = da / (a·H(a_mid))
        输出尺度因子 a(t) 与哈勃参数 H(t)。
        """
        # a 空间对数采样（早期辐射主导需密集采样）
        a_arr = np.geomspace(1e-6, 2.0, self.time_steps)
        # 宇宙时间 t(a) = ∫_{0}^{a} da'/(a'·H(a'))
        t_arr = np.zeros_like(a_arr)
        for i in range(1, self.time_steps):
            a_prev, a_curr = a_arr[i - 1], a_arr[i]
            a_mid = 0.5 * (a_prev + a_curr)
            dt_da = 1.0 / (self._dadt(a_mid) + 1e-30)  # dt/da = 1/(da/dt)
            t_arr[i] = t_arr[i - 1] + (a_curr - a_prev) * dt_da

        # 转换为 Gyr
        t_gyr = t_arr / self.GYR
        # 哈勃参数 H(t)（1/s → 1/Gyr）
        H_arr = np.array([self._hubble_a(a) for a in a_arr])  # 1/s
        H_gyr = H_arr * self.GYR                               # 1/Gyr

        self.t = t_gyr
        self.scale_factor = a_arr
        self.hubble_param = H_gyr

        self._has_run = True
        return self

    def verify_lambda(self):
        """
        验证 Λ 理论值 vs 观测值。

        综合 BSD 理论值、Planck 观测值、误差分析、BSD 六系推导与庞加莱稳态收敛验证。

        返回
        ----
        dict
            theoretical : BSD 理论值（Λ + 真空能密度）
            observed : Planck 观测值（Λ + 误差 + 置信区间 + 完整参数）
            error : 误差分析（相对/绝对误差、σ水平、一致性）
            bsd_derivation : 从 BSD 六系模态推导 Λ
            poincare : 庞加莱稳态收敛验证
            agreement : 一致性结论
            sigma_level : 显著性水平
        """
        lam_theo, rho_vac, units = lambda_theoretical()
        lam_obs, lam_obs_err, conf, planck = lambda_observed()
        rel_err, abs_err, sigma, agreement, err_analysis = lambda_error()
        lam_bsd, deriv_steps, six_contrib, norm = lambda_from_bsd()
        is_conv, conv_order, poincare_metric, manifold, euler = poincare_verification(self.Lambda)

        # 标量化（poincare_verification 标量输入返回 0-d numpy 标量）
        is_conv_v = bool(is_conv) if np.ndim(is_conv) == 0 else is_conv
        conv_order_v = int(conv_order) if np.ndim(conv_order) == 0 else conv_order
        poincare_metric_v = float(poincare_metric) if np.ndim(poincare_metric) == 0 else poincare_metric
        euler_v = float(euler) if np.ndim(euler) == 0 else euler

        return {
            "theoretical": {
                "Lambda": float(lam_theo),
                "energy_density": float(rho_vac),
                "unit_conversion": units,
            },
            "observed": {
                "Lambda": float(lam_obs),
                "error": float(lam_obs_err),
                "confidence_levels": conf,
                "planck_params": planck,
            },
            "error": err_analysis,
            "bsd_derivation": {
                "Lambda_from_bsd": float(lam_bsd),
                "derivation_steps": deriv_steps,
                "six_system_contributions": six_contrib,
                "normalization": float(norm),
            },
            "poincare": {
                "is_convergent": is_conv_v,
                "convergence_order": conv_order_v,
                "poincare_metric": poincare_metric_v,
                "manifold_type": manifold,
                "topological_invariant": euler_v,
            },
            "agreement": agreement,
            "sigma_level": float(sigma),
        }

    def get_results(self):
        """
        返回尺度因子 a(t)、哈勃参数 H(t)、Λ 验证结果。

        返回
        ----
        dict
            time : 时间数组（Gyr）
            scale_factor : 尺度因子 a(t)
            hubble_param : 哈勃参数 H(t)（1/Gyr）
            lambda_verification : Λ 验证结果（verify_lambda 输出）
            cross_check : 与 equations.universe_evolution 交叉验证
            cosmic_landmarks : 宇宙里程碑（当前时刻、物质-暗能量相等时刻等）
        """
        if not self._has_run:
            raise RuntimeError("请先调用 run() 执行仿真")

        # Λ 验证
        lam_verify = self.verify_lambda()

        # 与 equations.universe_evolution 交叉验证（时间单位：年）
        n_cross = min(self.time_steps, 50)
        t_for_eq = np.linspace(1e6, 1.5e10, n_cross)  # 年
        a_eq, H_eq, accel_eq, age_eq, phases = universe_evolution(self.Lambda, t_for_eq)

        # 宇宙里程碑：a=1（当前）对应的时间
        idx_now = int(np.argmin(np.abs(self.scale_factor - 1.0)))
        t_now = float(self.t[idx_now])
        H_now = float(self.hubble_param[idx_now])

        # 物质-暗能量相等：Ω_m/a³ = Ω_Λ → a_me = (Ω_m/Ω_Λ)^(1/3)
        a_me = None
        t_me = None
        if self.Omega_Lambda > 0:
            a_me = float((self.Omega_m / self.Omega_Lambda) ** (1.0 / 3.0))
            idx_me = int(np.argmin(np.abs(self.scale_factor - a_me)))
            t_me = float(self.t[idx_me])

        self._results = {
            "time": self.t,
            "scale_factor": self.scale_factor,
            "hubble_param": self.hubble_param,
            "lambda_verification": lam_verify,
            "cross_check": {
                "equation_evolution_time_Gyr": t_for_eq / 1e9,  # 年 → Gyr
                "equation_scale_factor": a_eq,
                "equation_hubble": H_eq,
                "equation_cosmic_age_Gyr": float(age_eq) if np.ndim(age_eq) == 0 else age_eq,
                "equation_phases": phases,
            },
            "cosmic_landmarks": {
                "now_time_Gyr": t_now,
                "now_hubble_1_per_Gyr": H_now,
                "matter_dark_energy_equality": {
                    "scale_factor": a_me,
                    "time_Gyr": t_me,
                },
                "planck_age_Gyr": 13.787,
            },
        }
        return self._results
