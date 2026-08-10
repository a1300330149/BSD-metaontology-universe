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

import json
import socket
from collections import deque
from src.support.base_library import BaseLibraryAgent

class DistComm:
    """
    功能：分布式通信模块
    理论映射：2重天道秩序基底·分布式通信规则
    能级关联：道心能级e_self更新
    约束来源：双边界守恒公理
    """
    def __init__(self, node_id: str, port: int = 9999):
        self.node_id = node_id
        self.port = port
        self.msg_queue = deque()
        self.global_lib = BaseLibraryAgent("./output/dist_base_lib.json")
        self.node_registry = {}

    def register_node(self, nid: str, ip: str, p: int):
        self.node_registry[nid] = {"ip": ip, "port": p}

    def sync_domain_prior(self, domain_name: str, hp: dict, score: float):
        self.global_lib.add_domain_prior(domain_name, hp, score)
        broadcast_msg = {
            "type": "lib_sync",
            "sender": self.node_id,
            "data": {"domain": domain_name, "hp": hp, "score": score}
        }
        self._broadcast(broadcast_msg)

    def _broadcast(self, msg: dict):
        msg_bytes = json.dumps(msg, ensure_ascii=False).encode("utf-8")
        for nid, info in self.node_registry.items():
            if nid == self.node_id:
                continue
            try:
                s = socket.socket()
                s.connect((info["ip"], info["port"]))
                s.send(msg_bytes)
                s.close()
            except Exception:
                continue