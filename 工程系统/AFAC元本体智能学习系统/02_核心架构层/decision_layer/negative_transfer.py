# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·人道秩序
对应三界秩序：人道秩序
对应公理：第3条（科研价值边际判定公理）、第4条（双边界守恒公理）、第7条（递归自指公理）
对应九维维度：因果社会/创化社会/精神能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：负迁移判定阈值θ_neg=0.02(永久锁档)
"""

class NegativeTransferAgent:
    """
    功能：负迁移检测智能体
    理论映射：2重人道秩序基底·负迁移判定规则
    能级关联：精神能级e_mind更新
    约束来源：科研价值边际判定公理
    禁止修改：θ_neg=0.02固定阈值，修改会破坏理论闭环
    """
    def __init__(self, threshold=0.02):
        # 负迁移判定阈值θ_neg，永久锁档0.02，不可调整
        self.th = threshold
        self.baseline = None
        self.history = []

    def set_baseline(self, score):
        self.baseline = score

    def check(self, curr_score):
        if self.baseline is None:
            return False, 0
        gain = curr_score - self.baseline
        neg = gain < -self.th
        self.history.append({"score": curr_score, "gain": gain, "is_neg": neg})
        return neg, gain

    def fallback(self):
        return {"action": "fallback_to_baseline", "drop_knowledge": True}