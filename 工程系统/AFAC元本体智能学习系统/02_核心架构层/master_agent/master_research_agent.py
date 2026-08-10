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
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, κ=0.35

本模块实现顶层主控智能体，统摄全局系统运行，协调各层智能体协同工作。

理论映射：
- 全局调度：对应全局宿命边界统摄理论（公理六）
- 自进化：对应系统自进化迭代公理（公理七）
- 边界约束：对应宿命/舒适双边界公理（公理一）
"""

import numpy as np
from src.core.global_state import GlobalState, DomainType
from src.core.flow_matrix import GlobalFlowMatrix
from src.core.boundary_guard import GlobalBoundaryGuard
from src.entity_layer.base_graph_agent import BaseGraphAgent
from src.entity_layer.phase_agent import EntityPhaseAgent
from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.entity_layer.gcl_agent import GCLAgent
from src.entity_layer.models import GCLEncoder
from src.decision_layer.bayesian_opt_agent import BayesianOptAgent
from src.decision_layer.cause_reward_agent import CauseRewardAgent
from src.decision_layer.negative_transfer import NegativeTransferAgent
from src.master_agent.transform_judger import TransformJudger
from src.master_agent.self_evolution import SelfEvolutionModule
from src.support.result_generator import ResultGeneratorAgent
from src.support.base_library import BaseLibraryAgent
from src.support.audit_logger import AuditLoggerAgent
from src.support.agent_comm import AgentCommDispatcher
from src.foundation.foundation_controller import FoundationController

class MasterResearchAgent:
    MODE_MAP = {
        "afac_competition": "competition",
        "academic_research": "research",
        "competition": "competition",
        "research": "research"
    }
    
    def __init__(self, config):
        self.config = config
        target_mode = config.get("task_target", "research").lower()
        self.task_mode = self.MODE_MAP.get(target_mode, "research")
        self.foundation = FoundationController()
        self.global_state = GlobalState()
        self.flow = GlobalFlowMatrix()
        self.judger = TransformJudger()
        self.guard = GlobalBoundaryGuard(config["max_budget"], DomainType(config["domain"]))
        self.evolution_cycle = 10
        self._apply_foundation_rules()
        self.evo = SelfEvolutionModule()
        self.agents = self._init_sub()
        self.report = ResultGeneratorAgent()
        self.lib = BaseLibraryAgent()
        self.audit = AuditLoggerAgent()
        self.comm = AgentCommDispatcher()
        self.comm.register("report", self.report)
        self.comm.register("lib", self.lib)
        self.comm.register("audit", self.audit)
        self.enable_auto = False
        self.enable_evo = False
        self.enable_gcl = config.get("enable_gcl", False)

    def _apply_foundation_rules(self):
        self.foundation.switch_task_mode(self.task_mode)
        
        tao_config = self.foundation.level2.get_realm_config("TAO")
        nature_config = self.foundation.level2.get_realm_config("NATURE")
        human_config = self.foundation.level2.get_realm_config("HUMAN")
        
        if tao_config:
            if not tao_config["budget_limit"]:
                self.guard.max_budget = 999999
            self.knowledge_sharing = tao_config.get("knowledge_sharing", False)
        
        if nature_config:
            self.skip_mlp_cold_start = nature_config.get("skip_mlp_cold_start", False)
            self.feature_enhancement = nature_config.get("feature_enhancement", False)
            self.missing_value_fill = nature_config.get("missing_value_fill", False)
            self.phase_threshold_reduction = nature_config.get("phase_threshold_reduction", 0.0)
        
        if human_config:
            self.evolution_cycle = human_config["evolution_cycle"]
            self.causal_reward_weight = human_config.get("causal_reward_weight", 1.0)
            self.adaptive_exploration = human_config.get("adaptive_exploration", False)
            self.target_explore_rate = human_config["bayes_explore_rate"]

    def _init_sub(self):
        base = BaseGraphAgent(self.config["dataset"], model_type="GATv2")
        
        phase_agent = EntityPhaseAgent(base)
        if self.skip_mlp_cold_start:
            phase_agent.current_phase = "GCN"
        
        return {
            "base": base,
            "phase": phase_agent,
            "data": DataPreprocessAgent(),
            "opt": BayesianOptAgent(self.config["param_bounds"]),
            "reward": CauseRewardAgent(),
            "neg_trans": NegativeTransferAgent(),
            "master": self
        }

    def _run_gcl_pretrain(self, data):
        print("=== 开始GCL图对比学习预训练 ===")
        d_in = data.x.shape[1]
        d_h = self.config["dataset"].get("hidden_dim", 128)
        
        encoder = GCLEncoder(d_in, d_h)
        gcl_agent = GCLAgent(encoder, hidden_dim=d_h)
        
        final_loss = gcl_agent.pretrain(data, epochs=30)
        print(f"GCL预训练完成, 最终损失: {final_loss:.4f}")
        
        return gcl_agent.get_pretrained_encoder()

    def run_full_autonomous_research(self):
        print("加载数据...")
        data = self.agents["data"].load_and_preprocess(self.config["dataset"]["data_path"])
        print(f"数据加载完成: {data.x.shape[0]}节点, {data.edge_index.shape[1]}边")
        
        if self.feature_enhancement:
            data = self.agents["data"].enhance_features(data)
            print(f"特征增强后: {data.x.shape[1]}维度")
        if self.missing_value_fill:
            data = self.agents["data"].fill_missing_values(data)
        
        self.agents["data"].enable_debias = True
        
        pretrained_encoder = None
        if self.enable_gcl:
            pretrained_encoder = self._run_gcl_pretrain(data)
            print("GCL预训练编码器已准备就绪")
        
        print("初始化模型...")
        try:
            self.agents["base"].init_base_model(data=data, pretrained_encoder=pretrained_encoder)
            init_score = self.agents["base"].train_one_epoch(data)
            print(f"初始分数: {init_score:.4f}")
        except Exception as e:
            print(f"模型初始化/训练失败: {e}")
            import traceback
            traceback.print_exc()
            return {"best_score": 0.0, "final_level": 0, "total_step": 0, "state_vec": [], "traj": []}
        self.agents["neg_trans"].set_baseline(init_score)
        max_step = self.config["max_steps"]
        print(f"开始训练, 最大步数: {max_step}")
        
        for step in range(max_step):
            ok, msg = self.guard.full_check("train_step", 1)
            if not ok:
                print(f"预算耗尽: {msg}")
                break
            
            if self.adaptive_exploration:
                explore_rate = self._calculate_adaptive_explore_rate(step, max_step)
                self.agents["opt"].explore_rate = explore_rate
            
            data_aug = self.agents["data"].augment_graph(data)
            
            params = self.agents["opt"].suggest_next_params()
            lr = float(params.get("lr", 0.001))
            wd = float(params.get("weight_decay", 1e-4))
            dropout = float(params.get("dropout", 0.3))
            hidden_dim = int(params.get("hidden_dim", self.config["dataset"]["hidden_dim"]))
            num_layers = int(params.get("num_layers", 3))
            num_heads = int(params.get("num_heads", 4))
            
            self.agents["base"].update_optimizer(lr, wd)
            
            real_s = self.agents["base"].train_one_epoch(data_aug)
            pred_s = params.get("expected_score", real_s)
            
            corr_r = self.agents["reward"].calculate_corrected_reward(real_s, pred_s) * self.causal_reward_weight
            self.agents["opt"].register_result(params, corr_r)
            
            self.global_state.x_nature_entity = self.agents["base"].get_entity_performance()
            phase_idx = ["MLP", "GCN", "GAT", "TGN"].index(self.agents["phase"].current_phase)
            self.global_state.x_nature_phase = phase_idx / 3
            self.global_state.x_society_cause = min(1.0, self.agents["reward"].get_cause_accumulation())
            self.global_state.x_society_create = 1 - self.agents["opt"].explore_rate
            
            self.global_state.time_step = step
            self.global_state.delta_illu = abs(real_s - pred_s)
            
            kappa = self.foundation.level1.get_kappa_adaptive(self.global_state.e_self, self.global_state.delta_illu)
            self.agents["reward"].kappa = kappa
            
            nature_config = self.foundation.level2.get_realm_config("NATURE")
            if nature_config and nature_config["sparse_debias_always_on"]:
                self.agents["data"].enable_debias = True
            
            sparse_ratio = self._estimate_sparse_ratio(data)
            self.global_state.e_body = self.foundation.level1.calculate_e_body(
                self.global_state.x_nature_entity, 
                self.global_state.x_nature_phase,
                sparse_ratio
            )
            self.global_state.e_mind = self.foundation.level1.calculate_e_mind(
                self.global_state.x_society_create, 
                self.global_state.x_society_cause
            )
            self.global_state.e_self = self.foundation.level1.calculate_e_self(
                self.global_state.e_body, 
                self.global_state.e_mind
            )
            
            self.foundation.run_emergence_cycle(
                sparse_ratio=sparse_ratio,
                delta_illu=self.global_state.delta_illu,
                e_self=self.global_state.e_self,
                max_steps=max_step,
                current_step=step
            )
            
            self.flow.step_update(self.global_state, np.power(self.global_state.gamma, step))
            curr_lv = self.judger.judge(self.global_state)
            if curr_lv != self.global_state.transform_level:
                effective_threshold = self.foundation.level2.get_effective_phase_threshold(
                    self.foundation.level1.TRANSFORM_THRESHOLDS["E1"]
                )
                if self.global_state.e_self >= effective_threshold:
                    self.judger.trigger(curr_lv, self.global_state, self.agents, data=data)
                    self.global_state.transform_level = curr_lv
            
            if step % 10 == 0:
                print(f"Step {step}: score={real_s:.4f}, best={self.agents['base'].baseline_score:.4f}, e_self={self.global_state.e_self:.4f}, phase={self.agents['phase'].current_phase}")
        
        return self._output_result()

    def _calculate_adaptive_explore_rate(self, step: int, max_steps: int):
        progress = step / max_steps
        e_self = self.global_state.e_self
        
        if e_self >= 0.9:
            return max(self.target_explore_rate * 0.3, 0.05)
        elif e_self >= 0.65:
            return max(self.target_explore_rate * 0.5, 0.1)
        elif e_self >= 0.35:
            return max(self.target_explore_rate * 0.75, 0.15)
        else:
            return self.target_explore_rate

    def _estimate_sparse_ratio(self, data) -> float:
        try:
            if hasattr(data, 'x') and data.x is not None:
                x = data.x.cpu().numpy() if hasattr(data.x, 'cpu') else data.x
                total_elements = x.shape[0] * x.shape[1]
                non_zero = np.count_nonzero(x)
                return max(0.0, 1.0 - non_zero / total_elements)
        except:
            pass
        return 0.3

    def _output_result(self):
        res = {
            "best_score": self.agents["base"].baseline_score,
            "final_level": str(self.global_state.transform_level),
            "total_step": self.global_state.time_step,
            "state_vec": self.global_state.to_vector().tolist(),
            "traj": self.agents["reward"].trajectory
        }
        self.report.generate_full_report(res, self.global_state)
        self.lib.add_domain_prior(self.config["domain"], self.agents["opt"].explore_rate, res["best_score"])
        self.audit.log_operation("experiment_finish", res, True)
        self.comm.send("master", "lib", "update_lib", {"domain": self.config["domain"], "hp": self.agents["opt"].explore_rate, "score": res["best_score"]})
        self.comm.dispatch_all()
        return res