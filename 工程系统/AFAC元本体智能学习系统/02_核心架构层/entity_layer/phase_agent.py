# -*- coding: utf-8 -*-
# ======================================================
# 归属: 2重·三界秩序基底
# 对应公理: 秩序守恒, 因果闭环
# ======================================================
"""
归属基底：第相变演化位（第三位）·自然秩序
对应三界秩序：自然秩序
对应公理：第5条（科研动力学公理）、第6条（相变临界公理）、第7条（递归自指公理）
对应九维维度：自然相变/自然实体/肉身能级
理论原文出处：《V3.0元本体理论分册》第三章
核心数理参数：E1=0.35, γ=0.92, 相变阈值MLP→GCN=0.15, GCN→GAT=0.25, GAT→TGN=0.35

本模块实现实体相变机制，管理模型在不同阶段之间的转换。

理论映射：
- 相变阈值：对应相变临界公理（公理六）
- 阶段转换：对应科研动力学公理（公理五）
- 模型演进：对应递归自指公理（公理七）

固定阈值（锁档核心）：
- MLP → GCN：0.15
- GCN → GAT：0.25
- GAT → TGN：0.35
- E1 = 0.35：一阶变身阈值
"""

from src.entity_layer.base_graph_agent import BaseGraphAgent

class EntityPhaseAgent:
    """
    功能：自然秩序实体相变管理
    理论映射：2重自然秩序基底·实体相变规则
    能级关联：e_body肉身能级更新
    约束来源：相变临界公理（公理六）

    管理模型在不同阶段之间的转换，实现相变临界判定和模型演进。

    固定阈值（锁档核心）：
    - MLP → GCN：0.15
    - GCN → GAT：0.25
    - GAT → TGN：0.35
    - E1 = 0.35：一阶变身阈值
    """

    # 相变阈值配置（锁档核心）
    PHASE_THRESHOLDS = {
        "MLP_to_GCN": 0.15,  # MLP → GCN阈值
        "GCN_to_GAT": 0.25,  # GCN → GAT阈值
        "GAT_to_TGN": 0.35   # GAT → TGN阈值（对应E1 = 0.35）
    }

    # 模型类型映射 - 对应三界维度秩序公理（公理三）
    PHASE_MODEL_MAP = {
        "MLP": "MLP",      # 自然秩序：纯特征学习
        "GCN": "GCN",      # 天道秩序：基础图建模
        "GAT": "GATv2",    # 人道秩序：细粒度图建模
        "TGN": "TGN"       # 综合秩序：动态图建模
    }

    # 阶段描述 - 对应三界维度秩序公理（公理三）
    PHASE_DESCRIPTIONS = {
        "MLP": "第0阶段：纯特征学习（无图结构）- 对应自然秩序",
        "GCN": "第1阶段：GCN图卷积（基础图建模）- 对应天道秩序",
        "GAT": "第2阶段：GAT注意力机制（细粒度图建模）- 对应人道秩序",
        "TGN": "第3阶段：TGN时序图网络（动态图建模）- 对应综合秩序"
    }

    def __init__(self, base_agent: BaseGraphAgent):
        """
        初始化相变智能体 - 对应相变临界公理（公理六）

        Args:
            base_agent (BaseGraphAgent): 基础图智能体
        """
        self.base = base_agent
        self.current_phase = "MLP"  # 初始阶段
        self.transition_history = []  # 转换历史

    def check_phase_transition(self, e_body: float) -> bool:
        """
        检查相变条件 - 对应相变临界公理（公理六）

        根据肉身能级判断是否满足相变条件。

        Args:
            e_body (float): 肉身能级

        Returns:
            bool: 是否满足相变条件

        理论方程：
        ΔΦ = Φ_new - Φ_old ≥ Φ_critical
        其中：
        - Φ：模型阶段
        - Φ_critical：相变阈值
        """
        order = ["MLP", "GCN", "GAT", "TGN"]
        idx = order.index(self.current_phase)

        if idx >= 3:
            return False  # 已达到最高阶段

        next_p = order[idx + 1]
        th = self.PHASE_THRESHOLDS[f"{self.current_phase}_to_{next_p}"]

        # 相变判定 - 对应相变临界公理（公理六）
        return e_body >= th

    def execute_phase_transition(self, data=None):
        """
        执行相变转换 - 对应科研动力学公理（公理五）

        执行模型阶段转换，更新模型类型和参数。

        Args:
            data: 数据对象（可选）

        理论方程：
        Φ_{t+1} = Transition(Φ_t, E_body)
        其中：
        - Φ_t：当前阶段
        - E_body：肉身能级
        """
        order = ["MLP", "GCN", "GAT", "TGN"]
        idx = order.index(self.current_phase)

        if idx >= 3:
            print("已达到最高阶段（TGN），无法继续转换")
            return

        next_phase = order[idx + 1]
        model_type = self.PHASE_MODEL_MAP[next_phase]

        # 相变转换 - 对应科研动力学公理（公理五）
        print(f"阶段转换: {self.current_phase} -> {next_phase} ({self.PHASE_DESCRIPTIONS[next_phase]})")

        # 记录转换历史 - 对应递归自指公理（公理七）
        self.transition_history.append({
            "from": self.current_phase,
            "to": next_phase,
            "step": self.base.global_step if hasattr(self.base, 'global_step') else 0
        })

        # 更新模型类型 - 对应相变临界公理（公理六）
        self.base.model_type = model_type

        # TGN特殊处理 - 对应三界维度秩序公理（公理三）
        if next_phase == "TGN":
            if data is not None and not hasattr(data, "edge_time"):
                print("为TGN生成时序特征...")
                data = self._generate_temporal_features(data)

        # 重新初始化模型 - 对应递归自指公理（公理七）
        self.base.init_base_model(data=data)
        self.current_phase = next_phase

    def _generate_temporal_features(self, data):
        """
        生成时序特征 - 对应科研动力学公理（公理五）

        为TGN模型生成时序特征。

        Args:
            data: 数据对象

        Returns:
            data: 添加时序特征的数据对象
        """
        import torch
        num_edges = data.edge_index.shape[1]
        data.edge_time = torch.rand(num_edges) * 1000
        data.edge_time = data.edge_time.sort()[0]
        return data

    def get_phase_description(self) -> str:
        """
        获取当前阶段描述 - 对应三界维度秩序公理（公理三）

        Returns:
            str: 阶段描述
        """
        return self.PHASE_DESCRIPTIONS.get(self.current_phase, "未知阶段")

    def can_transition(self) -> bool:
        """
        检查是否可以转换 - 对应相变临界公理（公理六）

        Returns:
            bool: 是否可以转换
        """
        order = ["MLP", "GCN", "GAT", "TGN"]
        idx = order.index(self.current_phase)
        return idx < 3
