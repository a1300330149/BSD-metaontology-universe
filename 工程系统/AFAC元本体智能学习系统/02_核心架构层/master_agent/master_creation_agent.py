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
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92

拓展分支：文娱创世分支（仅外围增量，不改动1重核心流转逻辑）
归属：2重天道秩序基底配套拓展
"""

from src.core.global_state import GlobalState, TransformLevel, DomainType
from src.core.flow_matrix import GlobalFlowMatrix
from src.core.boundary_guard import GlobalBoundaryGuard
from src.entity_layer.base_graph_agent import BaseGraphAgent
from src.entity_layer.phase_agent import EntityPhaseAgent
from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.decision_layer.cause_reward_agent import CauseRewardAgent
from src.support.result_generator import ResultGeneratorAgent
from src.support.base_library import BaseLibraryAgent
from src.support.audit_logger import AuditLoggerAgent
from src.support.agent_comm import AgentCommDispatcher

class CreationMasterAgent:
    """
    功能：创世主控智能体
    理论映射：2重天道秩序基底·创世规则统摄
    能级关联：道心能级e_self更新
    约束来源：全局宿命边界统摄理论
    """
    def __init__(self, config):
        self.config = config
        self.global_state = GlobalState()
        self.flow = GlobalFlowMatrix()
        self.guard = GlobalBoundaryGuard(config["max_budget"], DomainType(config["domain"]))
        self.agents = self._init_sub()
        self.report = ResultGeneratorAgent()
        self.lib = BaseLibraryAgent()
        self.audit = AuditLoggerAgent()
        self.comm = AgentCommDispatcher()
        self.comm.register("report", self.report)
        self.comm.register("lib", self.lib)
        self.comm.register("audit", self.audit)
        self.guard.max_budget = 999999

    def set_manual_es(self, value: float):
        self.global_state.e_self = value
        if value >= 0.9:
            self.global_state.transform_level = TransformLevel.THIRD_TAO
        elif value >= 0.65:
            self.global_state.transform_level = TransformLevel.SECOND_MIND
        elif value >= 0.35:
            self.global_state.transform_level = TransformLevel.FIRST_BODY
        else:
            self.global_state.transform_level = TransformLevel.NONE

    def generate_plot(self, character_name: str):
        vec = self.global_state.to_vector().flatten()
        names = ["元理天道", "动力天道", "相变自然", "载体实体", "创化社会", "因果社会", "肉身能级", "精神能级", "道心"]
        plot_text = f"角色：{character_name}\n"
        for i, n in enumerate(names):
            plot_text += f"{n}：{vec[i]:.2f}\n"
        if self.global_state.transform_level == TransformLevel.THIRD_TAO:
            plot_text += "\n【创世三阶·道合天道】已达创世三阶，解锁天地规则改写权限"
        elif self.global_state.transform_level == TransformLevel.SECOND_MIND:
            plot_text += "\n【二阶·精神觉醒】掌握因果规律，洞察世间奥秘"
        elif self.global_state.transform_level == TransformLevel.FIRST_BODY:
            plot_text += "\n【一阶·肉身成圣】突破凡躯枷锁，获得超凡力量"
        else:
            plot_text += "\n【初始态·凡人】尚未觉醒，静待机缘"
        return plot_text

    def run_creation_simulation(self, steps=50):
        data = self.agents["data"].load_and_preprocess(self.config["dataset"]["data_path"])
        self.agents["base"].init_base_model()
        for step in range(steps):
            real_s = self.agents["base"].train_one_epoch(data)
            self.global_state.x_nature_entity = self.agents["base"].get_entity_performance()
            phase_idx = ["MLP", "GCN", "GAT", "TGN"].index(self.agents["phase"].current_phase)
            self.global_state.x_nature_phase = phase_idx / 3
            self.global_state.e_body = 0.6 * self.global_state.x_nature_entity + 0.4 * self.global_state.x_nature_phase
            self.global_state.e_mind = 0.5
            self.global_state.e_self = 0.4 * self.global_state.e_body + 0.6 * self.global_state.e_mind
            self.global_state.time_step = step
            self.flow.step_update(self.global_state)
        return self._output_result()

    def _init_sub(self):
        base = BaseGraphAgent(self.config["dataset"])
        return {
            "base": base,
            "phase": EntityPhaseAgent(base),
            "data": DataPreprocessAgent(),
            "reward": CauseRewardAgent()
        }

    def _output_result(self):
        res = {
            "best_score": self.agents["base"].baseline_score,
            "final_level": self.global_state.transform_level,
            "state_vec": self.global_state.to_vector().tolist()
        }
        return res