# -*- coding: utf-8 -*-
# ======================================================
# 归属: 3重·六阶科研业务
# 对应公理: 无界递归, 对称破缺
# ======================================================
"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：创化社会/因果社会
理论原文出处：《V3.0元本体理论分册》第四章
核心数理参数：γ=0.92
"""

import os
import json

class BaseLibraryAgent:
    """
    功能：基础知识库管理模块
    理论映射：3重六阶科研系统·知识存储规则
    能级关联：精神能级e_mind更新
    约束来源：科研动力学公理
    """
    def __init__(self, path="./output/base_lib.json"):
        self.path = path
        self.lib = self._load()

    def _load(self):
        if os.path.exists(self.path):
            return json.load(open(self.path, "r", encoding="utf-8"))
        return {"domain": [], "fail": []}

    def add_domain_prior(self, domain, hp, score):
        self.lib["domain"].append({"name": domain, "hp": hp, "s": score})
        json.dump(self.lib, open(self.path, "w", encoding="utf-8"), indent=4)

    def get_prior(self, name):
        for item in self.lib["domain"]:
            if item["name"] == name:
                return item
        return None