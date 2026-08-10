"""
归属基底：L0_总本源层·0元本体论大一统
对应公理：公理5·六系本源公理 / 公理6·双极性创生公理
对应九维维度：物质维·能量场·信息维
理论出处：theory_base/L0_总本源层/全域大一统理论/化学三阶相变T86
固定数理常量：κ=0.35 (KAPPA)、α=0.18 (ALPHA)、γ=0.92 (GAMMA)、健康α∈[0.30,0.40]

BSD化学三阶相变仿真器
—— 基于BSD六系三元权重 α₁+α₂+α₃=1 的化学元素三阶相变过程仿真
   一阶原子键合 → 二阶分子结构化 → 三阶复合物稳态
"""

import numpy as np

from bsd_engine.equations.life_steady_state import health_alpha_range, disease_level
from bsd_engine.registry.constants import KAPPA, ALPHA, GAMMA, E1, E2, E3


class ChemistrySimulator:
    """
    化学三阶相变仿真器

    仿真化学元素的三阶相变过程：
        一阶（原子键合）→ 二阶（分子结构化）→ 三阶（复合物稳态）

    基于 BSD 六系三元权重 α₁+α₂+α₃=1：
        - 六系两两正交配对为三组（强化·调控 / 结构·信息 / 能量·意义）
        - 每组配对求和并归一化得到三元权重 (α₁, α₂, α₃)
        - 三阶相变过程中 α 权重在三个阶段被重新分配

    相变动力学（softmax 约束的潜势演化，保证 α₁+α₂+α₃=1 恒成立）：
        令潜势 u = (u₁, u₂, u₃)，α = softmax(u/τ)
        - 一阶 [0, T/3)：原子键合驱动 u₁ 上升（α₁ 主导）
        - 二阶 [T/3, 2T/3)：分子结构化驱动 u₂ 上升（α₂ 主导）
        - 三阶 [2T/3, T)：复合物稳态，三势向均衡收敛 → α → (1/3, 1/3, 1/3) ∈ 健康态 [0.30, 0.40]

    参数
    ----
    num_elements : int
        化学元素数（默认 20）
    time_steps : int
        时间步数（默认 300，三阶各约 100 步）

    固定常量
    --------
    κ = KAPPA = 0.35，α = ALPHA = 0.18，γ = GAMMA = 0.92
    健康态 α ∈ [0.30, 0.40]（HEALTH_ALPHA_MIN/MAX）
    """

    # BSD 六系名称（顺序固定：强化/调控/结构/信息/能量/意义）
    SIX_SYSTEMS = ("reinforcement", "regulation", "structure",
                   "information", "energy", "meaning")

    def __init__(self, num_elements=20, time_steps=300):
        self.num_elements = int(num_elements)
        self.time_steps = int(time_steps)
        self.kappa = KAPPA
        self.alpha = ALPHA
        self.gamma = GAMMA

        # 六系权重矩阵 (num_elements, 6)，行归一化
        self.six_weights = None
        # 三元α权重时间序列 (time_steps, num_elements, 3)
        self.alpha_weights = None
        # 三阶相变综合曲线 (time_steps,)
        self.transition_curve = None
        # 各阶α演化曲线 (3, time_steps)
        self.stage_curves = None
        self.t = None
        self.steady_state = None
        self._results = None
        self._has_run = False

    def setup_elements(self, element_params):
        """
        设置各元素的六系权重。

        参数
        ----
        element_params : np.ndarray or dict
            - array: shape=(num_elements, 6) 六系权重矩阵，自动行归一化
            - dict:  键为六系名，值为长度 num_elements 的数组
        """
        if isinstance(element_params, dict):
            mat = np.zeros((self.num_elements, 6))
            for i, name in enumerate(self.SIX_SYSTEMS):
                if name in element_params:
                    col = np.asarray(element_params[name], dtype=float).flatten()
                    mat[:, i] = col[:self.num_elements] if col.size >= self.num_elements else np.resize(col, self.num_elements)
            element_params = mat
        else:
            element_params = np.asarray(element_params, dtype=float)
            if element_params.shape != (self.num_elements, 6):
                element_params = np.resize(element_params, (self.num_elements, 6))

        # 行归一化（每元素六系权重和为1）
        row_sum = element_params.sum(axis=1, keepdims=True) + 1e-12
        self.six_weights = element_params / row_sum
        self._has_run = False
        return self

    def _six_to_alpha(self, six_w):
        """
        六系权重 → 三元权重 α₁+α₂+α₃=1。

        BSD 六系两两正交配对：
            α₁ ∝ (强化 + 调控)   物质对
            α₂ ∝ (结构 + 信息)   结构信息对
            α₃ ∝ (能量 + 意义)   能量意义对
        再归一化保证 α₁+α₂+α₃=1。
        """
        a1 = (six_w[:, 0] + six_w[:, 1]) / 2.0
        a2 = (six_w[:, 2] + six_w[:, 3]) / 2.0
        a3 = (six_w[:, 4] + six_w[:, 5]) / 2.0
        total = a1 + a2 + a3 + 1e-12
        return np.stack([a1 / total, a2 / total, a3 / total], axis=-1)

    def run(self):
        """
        执行三阶相变动力学仿真。

        采用 softmax 约束的潜势演化：
            - 一阶 [0, t1)：原子键合 → u₁ 上升，u₂/u₃ 相对下降
            - 二阶 [t1, t2)：分子结构化 → u₂ 上升，u₁ 缓落，u₃ 蓄势
            - 三阶 [t2, T)：复合物稳态 → 三势向均衡收敛，α → 健康态
        每步 α = softmax(u/τ) 恒满足 α₁+α₂+α₃=1。
        """
        if self.six_weights is None:
            # 默认六系权重：Dirichlet 采样（保证有结构且归一）
            rng = np.random.default_rng(42)
            self.setup_elements(rng.dirichlet(np.ones(6), size=self.num_elements))

        # 初始α由六系权重导出
        alpha_init = self._six_to_alpha(self.six_weights)  # (N, 3)
        # softmax 温度
        tau = 0.5
        # 由初始α反推潜势 u_i = τ·(log α_i - mean log α)
        log_a = np.log(alpha_init + 1e-12)
        u_curr = tau * (log_a - log_a.mean(axis=1, keepdims=True))

        T = self.time_steps
        t1 = T // 3          # 一阶结束
        t2 = 2 * T // 3      # 二阶结束
        self.t = np.arange(T, dtype=float)

        # 阶段驱动力幅度
        drive = 0.03
        damping = self.alpha      # 0.18 潜势阻尼
        converge = self.kappa     # 0.35 三阶收敛速率

        alpha_series = np.zeros((T, self.num_elements, 3))
        stage_curves = np.zeros((3, T))
        alpha_series[0] = alpha_init
        stage_curves[:, 0] = alpha_init.mean(axis=0)

        for n in range(1, T):
            du = np.zeros_like(u_curr)
            if n < t1:
                # 一阶：原子键合 → u₁ 上升，u₂/u₃ 下降
                du[:, 0] += drive * 0.5
                du[:, 1] -= drive * 0.5
                du[:, 2] -= drive * 0.5
            elif n < t2:
                # 二阶：分子结构化 → u₂ 上升，u₁ 缓落，u₃ 蓄势
                du[:, 0] -= drive * 0.3
                du[:, 1] += drive * 0.9
                du[:, 2] -= drive * 0.2
            else:
                # 三阶：复合物稳态 → 三势向均值收敛
                mean_u = u_curr.mean(axis=1, keepdims=True)
                du -= converge * (u_curr - mean_u)

            # 全局潜势阻尼（防止发散）
            du -= damping * 0.1 * (u_curr - u_curr.mean(axis=1, keepdims=True))
            u_curr = u_curr + du

            # softmax → α（max 减法保证数值稳定）
            ex = np.exp((u_curr - u_curr.max(axis=1, keepdims=True)) / tau)
            alpha_n = ex / ex.sum(axis=1, keepdims=True)
            alpha_series[n] = alpha_n

            # 各阶相变曲线：该阶主权重的元素均值
            stage_curves[0, n] = alpha_n[:, 0].mean()
            stage_curves[1, n] = alpha_n[:, 1].mean()
            stage_curves[2, n] = alpha_n[:, 2].mean()

        self.alpha_weights = alpha_series
        self.stage_curves = stage_curves
        # 三阶相变综合曲线：主导权重 - 次要权重均值（极化度）
        dominant = stage_curves.max(axis=0)
        minor = stage_curves.sum(axis=0) - dominant
        self.transition_curve = dominant - minor

        # 稳态判定（三阶末段）
        self._compute_steady_state()
        self._has_run = True
        return self

    def _compute_steady_state(self):
        """基于三阶末段 α 权重判定稳态。"""
        final = self.alpha_weights[-1]  # (N, 3)
        # 健康态判定
        is_healthy, health_score, alpha_norm, deviation = health_alpha_range(
            final[:, 0], final[:, 1], final[:, 2]
        )
        # 疾病等级（基于最大权重差）
        max_diff = np.maximum(
            np.abs(final[:, 0] - final[:, 1]),
            np.maximum(np.abs(final[:, 1] - final[:, 2]),
                       np.abs(final[:, 0] - final[:, 2]))
        )
        level, level_score, recommendation, recovery_path = disease_level(max_diff)

        self.steady_state = {
            "final_alpha_mean": final.mean(axis=0).tolist(),
            "is_healthy_ratio": float(np.mean(is_healthy)),
            "mean_health_score": float(np.mean(health_score)),
            "mean_deviation": float(np.mean(deviation)),
            "disease_levels": {
                "levels": level.tolist() if hasattr(level, "tolist") else level,
                "mean_level_score": float(np.mean(level_score)),
            },
            "steady_reached": bool(np.mean(is_healthy) > 0.5),
        }

    def check_health_alpha(self):
        """
        检查健康态 α∈[0.30,0.40]。

        返回
        ----
        dict
            is_healthy : 各元素是否处于健康态
            health_score : 健康度评分（0-100）
            alpha_norm : 归一化三权重 (α₁, α₂, α₃)
            deviation : 与理想值(1/3)的偏差
            in_range_ratio : 处于健康态的元素比例
        """
        if self.alpha_weights is None:
            raise RuntimeError("请先调用 run()")
        final = self.alpha_weights[-1]
        is_healthy, health_score, alpha_norm, deviation = health_alpha_range(
            final[:, 0], final[:, 1], final[:, 2]
        )
        return {
            "is_healthy": is_healthy,
            "health_score": health_score,
            "alpha_norm": alpha_norm,
            "deviation": deviation,
            "in_range_ratio": float(np.mean(is_healthy)),
        }

    def get_results(self):
        """
        返回三阶相变曲线、α权重演化、稳态判定结果。

        返回
        ----
        dict
            time : 时间数组
            transition_curve : 三阶相变综合曲线
            stage_curves : 三阶各自的α演化曲线（stage1_atomic / stage2_molecular / stage3_complex）
            alpha_weights : 三元α权重时间序列 (T, N, 3)
            six_weights : 初始六系权重
            steady_state : 稳态判定
            health_check : 健康态检查
        """
        if not self._has_run:
            raise RuntimeError("请先调用 run() 执行仿真")
        self._results = {
            "time": self.t,
            "transition_curve": self.transition_curve,
            "stage_curves": {
                "stage1_atomic": self.stage_curves[0],
                "stage2_molecular": self.stage_curves[1],
                "stage3_complex": self.stage_curves[2],
            },
            "alpha_weights": self.alpha_weights,
            "six_weights": self.six_weights,
            "steady_state": self.steady_state,
            "health_check": self.check_health_alpha(),
        }
        return self._results
