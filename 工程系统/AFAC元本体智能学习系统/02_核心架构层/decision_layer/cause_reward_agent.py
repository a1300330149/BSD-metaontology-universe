# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·人道秩序
对应三界秩序：人道秩序
对应公理：第3条（科研价值边际判定公理）、第4条（双边界守恒公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：社会因果/社会创造/精神能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：γ=0.92, κ=0.35, α=0.18, θ_neg=0.02

本模块实现因果奖励计算机制，处理稀疏反馈和内在奖励计算。

理论映射：
- 因果奖励：对应科研动力学公理（公理五）
- 稀疏补偿：对应稀疏补偿系数（α = 0.18）
- 幻觉校正：对应双边界守恒公理（公理四）

固定参数（锁档核心）：
- γ = 0.92：衰减系数
- κ = 0.35：耦合强度系数
- α = 0.18：稀疏补偿系数
"""

import numpy as np

class CauseRewardAgent:
    """
    功能：人道因果奖励动力学计算
    理论映射：2重人道秩序基底·因果奖励规则
    能级关联：e_mind精神能级更新
    约束来源：科研动力学公理（公理五）

    实现因果奖励计算机制，处理稀疏反馈和内在奖励计算。

    固定参数（锁档核心）：
    - γ = 0.92：衰减系数
    - κ = 0.35：耦合强度系数
    - α = 0.18：稀疏补偿系数
    """

    def __init__(self, gamma=0.92, kappa=0.35):
        """
        初始化因果奖励智能体 - 对应科研动力学公理（公理五）

        Args:
            gamma (float): 衰减系数（理论值：γ = 0.92）
            kappa (float): 耦合强度系数（理论值：κ = 0.35）
        """
        self.gamma = gamma  # 衰减系数 - 对应科研动力学公理（公理五）
        self.kappa = kappa  # 耦合强度系数 - 对应科研动力学公理（公理五）
        self.trajectory = []  # 轨迹历史 - 对应递归自指公理（公理七）
        self.intrinsic_reward = 0.0  # 内在奖励 - 对应科研动力学公理（公理五）

    def calculate_corrected_reward(self, real_score, pred_score) -> float:
        """
        计算校正奖励 - 对应科研动力学公理（公理五）

        根据真实分数和预测分数计算校正奖励，包含幻觉校正和衰减项。

        Args:
            real_score (float): 真实分数
            pred_score (float): 预测分数

        Returns:
            float: 校正奖励

        理论方程：
        R_{corrected} = R_{real} - κ · Δ_illu
        R_{intrinsic} = γ · R_{intrinsic} + R_{corrected}
        其中：
        - R_{real}：真实奖励
        - Δ_illu：幻觉增量
        - κ：耦合强度系数
        - γ：衰减系数
        """
        # 计算幻觉增量 - 对应双边界守恒公理（公理四）
        delta_illu = abs(real_score - pred_score)

        # 计算校正奖励 - 对应科研动力学公理（公理五）
        # R_corrected = R_real - κ · Δ_illu
        corr = real_score - self.kappa * delta_illu

        # 更新内在奖励 - 对应科研动力学公理（公理五）
        # R_intrinsic = γ · R_intrinsic + R_corrected
        self.intrinsic_reward = self.gamma * self.intrinsic_reward + corr

        # 记录轨迹 - 对应递归自指公理（公理七）
        self.trajectory.append({
            "step": len(self.trajectory),
            "real_score": real_score,
            "predict_score": pred_score,
            "delta_illu": delta_illu,
            "corrected_reward": corr
        })

        return corr

    def get_cause_accumulation(self) -> float:
        """
        获取因果累积奖励 - 对应科研动力学公理（公理五）

        Returns:
            float: 因果累积奖励
        """
        return self.intrinsic_reward

    def compute_sparse_compensation(self, feedback_density: float) -> float:
        """
        计算稀疏补偿 - 对应稀疏补偿系数（α = 0.18）

        根据反馈密度计算稀疏补偿。

        Args:
            feedback_density (float): 反馈密度

        Returns:
            float: 稀疏补偿

        理论方程：
        Compensation = α · (1 - feedback_density)
        其中：
        - α：稀疏补偿系数（α = 0.18）
        """
        # 固定系数（锁档核心）：α = 0.18
        alpha = 0.18
        compensation = alpha * (1.0 - feedback_density)
        return compensation