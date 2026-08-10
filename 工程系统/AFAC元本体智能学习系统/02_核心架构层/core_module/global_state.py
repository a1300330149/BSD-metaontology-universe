# -*- coding: utf-8 -*-
# ======================================================
# 归属: 1重·九维法理基底
# 对应公理: 同源涌现, 层级包含
# ======================================================
"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道/自然/人道
对应公理：第2条（全域九维法理公理）、第6条（相变临界公理）、第7条（递归自指公理）
对应九维维度：天道原理/天道动力学/自然相变/自然实体/社会创造/社会因果/肉身能级/精神能级/道心能级
理论原文出处：《V3.0元本体理论分册》第二章
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92

本模块实现系统的递归自指特性，管理全局状态向量，包含九维状态空间和三阶变身机制。

理论映射：
- 九维状态向量：对应全域九维法理公理（公理二）
- 三阶变身机制：对应相变临界公理（公理六）
- 递归更新：对应递归自指公理（公理七）
"""

import numpy as np
from enum import Enum
from dataclasses import dataclass

class DomainType(Enum):
    """
    功能：领域类型枚举
    理论映射：相变演化位（第三位）·维度秩序划分规则
    约束来源：三界维度秩序公理（公理三）
    """
    GENERAL = "general"  # 自然秩序
    GRAPH_LEARNING = "graph_learning"  # 天道秩序
    RECOMMENDATION = "recommendation"  # 人道秩序

class TransformLevel(Enum):
    """
    功能：变身等级枚举
    理论映射：相变演化位（第三位）·天道秩序三阶变身规则
    约束来源：相变临界公理（公理六）
    """
    NONE = 0  # 未变身
    FIRST_BODY = 1  # 一阶变身（肉身能级 E1 ≥ 0.35）
    SECOND_MIND = 2  # 二阶变身（精神能级 E2 ≥ 0.65）
    THIRD_TAO = 3  # 三阶变身（道心能级 E3 ≥ 0.90）

@dataclass
class GlobalState:
    """
    功能：九维全息状态向量管理
    理论映射：规则相位位（第二位）·全域状态表达规则
    能级关联：e_body、e_mind、e_self三阶能级
    约束来源：全域九维法理公理（公理二）
    禁止修改：E1/E2/E3固定阈值，修改会破坏理论闭环

    包含九维状态向量和三阶变身阈值，实现系统的递归自指更新机制。

    固定阈值（锁档核心）：
    - E1 = 0.35：一阶变身阈值（肉身能级）
    - E2 = 0.65：二阶变身阈值（精神能级）
    - E3 = 0.90：三阶变身阈值（道心能级）
    - γ = 0.92：衰减系数
    """
    # 九维状态向量 - 对应全域九维法理公理（公理二）
    x_tao_principle: float = 0.0  # 天道原理维度
    x_tao_dynamic: float = 0.0  # 天道动力学维度
    x_nature_phase: float = 0.0  # 自然相变维度
    x_nature_entity: float = 0.0  # 自然实体维度
    x_society_create: float = 0.0  # 社会创造维度
    x_society_cause: float = 0.0  # 社会因果维度
    e_body: float = 0.0  # 肉身能级 - 对应一阶变身（E1 ≥ 0.35）
    e_mind: float = 0.0  # 精神能级 - 对应二阶变身（E2 ≥ 0.65）
    e_self: float = 0.0  # 自我能级 - 对应三阶变身（E3 ≥ 0.90）

    # 系统参数 - 对应科研动力学公理（公理五）
    time_step: int = 0  # 时间步长
    delta_illu: float = 0.0  # 幻觉增量
    transform_level: TransformLevel = TransformLevel.NONE  # 变身等级
    gamma: float = 0.99  # 衰减系数（理论值：γ = 0.92）

    def to_vector(self) -> np.ndarray:
        """
        将状态转换为九维向量 - 对应全域九维法理公理（公理二）

        Returns:
            np.ndarray: 9x1维状态向量
        """
        return np.array([
            self.x_tao_principle, self.x_tao_dynamic, self.x_nature_phase,
            self.x_nature_entity, self.x_society_create, self.x_society_cause,
            self.e_body, self.e_mind, self.e_self
        ]).reshape(-1, 1)

    def update_from_vector(self, vec: np.ndarray):
        """
        从向量更新状态 - 对应递归自指公理（公理七）

        Args:
            vec (np.ndarray): 9x1维状态向量
        """
        self.x_tao_principle = vec[0, 0]
        self.x_tao_dynamic = vec[1, 0]
        self.x_nature_phase = vec[2, 0]
        self.x_nature_entity = vec[3, 0]
        self.x_society_create = vec[4, 0]
        self.x_society_cause = vec[5, 0]
        self.e_body = vec[6, 0]
        self.e_mind = vec[7, 0]
        self.e_self = vec[8, 0]

    def check_transform_level(self) -> TransformLevel:
        """
        检查变身等级 - 对应相变临界公理（公理六）

        Returns:
            TransformLevel: 当前变身等级
        """
        # 固定阈值（锁档核心）
        E1 = 0.35  # 一阶变身阈值
        E2 = 0.65  # 二阶变身阈值
        E3 = 0.90  # 三阶变身阈值

        if self.e_self >= E3:
            return TransformLevel.THIRD_TAO
        elif self.e_mind >= E2:
            return TransformLevel.SECOND_MIND
        elif self.e_body >= E1:
            return TransformLevel.FIRST_BODY
        else:
            return TransformLevel.NONE