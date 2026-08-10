# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·天道秩序
对应三界秩序：天道秩序
对应公理：第1条（宿命/舒适双边界公理）、第6条（全局宿命边界统摄理论）、第7条（系统自进化迭代公理）
对应九维维度：天道原理/天道动力学/道心能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E1=0.35, E2=0.65, E3=0.90
"""

from src.core.global_state import GlobalState, TransformLevel

class TransformJudger:
    """
    功能：三阶变身等级判定器
    理论映射：2重天道秩序基底·变身判定规则
    能级关联：道心能级e_self更新
    约束来源：宿命/舒适双边界公理
    禁止修改：E1/E2/E3固定阈值，修改会破坏理论闭环
    """
    # 肉身一阶变身阈值E1，永久锁档0.35，不可调整
    E1 = 0.35
    # 精神二阶变身阈值E2，永久锁档0.65，不可调整
    E2 = 0.65
    # 道心三阶变身阈值E3，永久锁档0.90，不可调整
    E3 = 0.90

    def judge(self, state: GlobalState):
        es = state.e_self
        if es >= self.E3:
            return TransformLevel.THIRD_TAO
        elif es >= self.E2:
            return TransformLevel.SECOND_MIND
        elif es >= self.E1:
            return TransformLevel.FIRST_BODY
        return TransformLevel.NONE

    def trigger(self, level, state, agents, data=None):
        if level == TransformLevel.FIRST_BODY:
            agents["phase"].execute_phase_transition(data=data)
            agents["data"].enable_debias = True
        elif level == TransformLevel.SECOND_MIND:
            agents["opt"].update_explore_rate(state.e_mind)
            agents["reward"].kappa = 0.4
        elif level == TransformLevel.THIRD_TAO:
            agents["master"].enable_auto = True
            agents["master"].enable_evo = True