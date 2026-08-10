# -*- coding: utf-8 -*-
# ======================================================
# 归属: 3重·六阶科研业务
# 对应公理: 无界递归, 对称破缺
# ======================================================
"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：因果社会/创化社会
理论原文出处：《V3.0元本体理论分册》第四章
核心数理参数：γ=0.92
"""

from collections import deque

class AgentCommDispatcher:
    """
    功能：智能体通信调度器
    理论映射：3重六阶科研系统·通信协调规则
    能级关联：精神能级e_mind更新
    约束来源：科研动力学公理
    """
    def __init__(self):
        self.queue = deque()
        self.reg = {}

    def register(self, name, obj):
        self.reg[name] = obj

    def send(self, sender, target, msg_type, content):
        self.queue.append({"s": sender, "t": target, "ty": msg_type, "c": content})

    def dispatch_all(self):
        while self.queue:
            msg = self.queue.popleft()
            target = self.reg.get(msg["t"])
            if target:
                if msg["ty"] == "update_lib":
                    target.add_domain_prior(**msg["c"])