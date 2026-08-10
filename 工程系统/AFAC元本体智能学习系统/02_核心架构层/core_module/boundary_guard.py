# -*- coding: utf-8 -*-
# ======================================================
# 归属: 1重·九维法理基底
# 对应公理: 同源涌现, 层级包含
# ======================================================
"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道/自然/人道
对应公理：第1条（宿命/舒适双边界公理）、第3条（三界维度秩序公理）
对应九维维度：天道原理/天道动力学/自然相变/自然实体/社会创造/社会因果
理论原文出处：《V3.0元本体理论分册》第一章
核心数理参数：FB宿命边界、CB舒适边界（Ω_CB ⊂ Ω_FB）

本模块实现双边界约束检查，管理系统的宿命边界和舒适边界。

理论映射：
- 双边界约束：对应宿命/舒适双边界公理（公理一）
- 领域类型：对应三界维度秩序公理（公理三）
"""

from src.core.global_state import DomainType

class GlobalBoundaryGuard:
    def __init__(self, max_budget, domain: DomainType):
        self.max_budget = max_budget
        self.domain = domain
        self.used = 0

    def check_budget(self, cost):
        return self.used + cost <= self.max_budget

    def check_compliance(self, op):
        forbidden = ["modify_raw_data", "fake_result"]
        return op not in forbidden

    def full_check(self, op, cost):
        if not self.check_budget(cost):
            return False, "超出预算"
        if not self.check_compliance(op):
            return False, "违规操作"
        self.used += cost
        return True, "校验通过"