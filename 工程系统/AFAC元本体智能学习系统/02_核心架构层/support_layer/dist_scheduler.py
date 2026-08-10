# -*- coding: utf-8 -*-
# ======================================================
# 归属: 3重·六阶科研业务
# 对应公理: 无界递归, 对称破缺
# ======================================================
"""
归属基底：第相变演化位（第三位）·天道秩序配套拓展
对应三界秩序：天道秩序
对应公理：第4条（双边界守恒公理）、第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：天道原理/天道动力学
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：γ=0.92

拓展分支：分布式并行（仅外围增量，不改动1重核心流转逻辑）
归属：2重天道秩序基底配套拓展
"""

from src.core.global_state import GlobalState
from src.support.dist_comm import DistComm

class DistLoadScheduler:
    """
    功能：分布式负载调度器
    理论映射：2重天道秩序基底·分布式调度规则
    能级关联：道心能级e_self更新
    约束来源：双边界守恒公理
    """
    def __init__(self, comm: DistComm):
        self.comm = comm
        self.node_e_self = {}

    def refresh_node_level(self, nid: str, state: GlobalState):
        self.node_e_self[nid] = state.e_self

    def allocate_task(self, task_difficulty: float):
        sorted_nodes = sorted(self.node_e_self.items(), key=lambda x: x[1], reverse=True)
        if task_difficulty >= 0.7:
            target = sorted_nodes[0][0]
        elif 0.3 <= task_difficulty < 0.7:
            target = sorted_nodes[1][0] if len(sorted_nodes) >= 2 else sorted_nodes[0][0]
        else:
            target = sorted_nodes[-1][0]
        return target