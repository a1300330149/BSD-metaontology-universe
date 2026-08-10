import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import yaml
import numpy as np
from src.core.global_state import GlobalState, DomainType, TransformLevel
from src.core.flow_matrix import GlobalFlowMatrix
from src.core.boundary_guard import GlobalBoundaryGuard
from src.entity_layer.base_graph_agent import BaseGraphAgent
from src.entity_layer.phase_agent import EntityPhaseAgent
from src.entity_layer.data_preprocess import DataPreprocessAgent
from src.decision_layer.bayesian_opt_agent import BayesianOptAgent
from src.decision_layer.cause_reward_agent import CauseRewardAgent
from src.decision_layer.negative_transfer import NegativeTransferAgent
from src.master_agent.transform_judger import TransformJudger
from src.master_agent.self_evolution import SelfEvolutionModule
from src.support.result_generator import ResultGeneratorAgent
from src.support.base_library import BaseLibraryAgent
from src.support.audit_logger import AuditLoggerAgent
from src.support.agent_comm import AgentCommDispatcher
from src.support.dist_comm import DistComm
from src.support.dist_scheduler import DistLoadScheduler
from src.master_agent.master_research_agent import MasterResearchAgent

def test_global_state():
    print("\n=== 测试全局状态 ===")
    state = GlobalState()
    vec = state.to_vector()
    print(f"状态向量维度: {vec.shape}")
    assert vec.shape == (9, 1), "状态向量维度错误"
    state.e_body = 0.5
    state.e_mind = 0.6
    state.e_self = 0.4 * state.e_body + 0.6 * state.e_mind
    print(f"道心能级: {state.e_self:.4f}")
    assert abs(state.e_self - 0.56) < 0.01, "道心计算错误"
    print("全局状态测试通过")

def test_flow_matrix():
    print("\n=== 测试流转矩阵 ===")
    flow = GlobalFlowMatrix()
    state = GlobalState()
    state.x_tao_dynamic = 0.5
    flow.step_update(state)
    print(f"流转后载体实体: {state.x_nature_entity:.4f}")
    print("流转矩阵测试通过")

def test_boundary_guard():
    print("\n=== 测试边界管控 ===")
    guard = GlobalBoundaryGuard(10, DomainType.GRAPH_LEARNING)
    ok, msg = guard.full_check("train", 5)
    assert ok, f"边界管控错误: {msg}"
    ok, msg = guard.full_check("train", 6)
    assert not ok, "边界管控应该拒绝超额预算"
    print("边界管控测试通过")

def test_phase_agent():
    print("\n=== 测试相变智能体 ===")
    agent = EntityPhaseAgent(BaseGraphAgent({"feat_dim": 128, "hidden_dim": 64, "num_classes": 10}))
    assert agent.current_phase == "MLP"
    assert agent.check_phase_transition(0.1) == False
    assert agent.check_phase_transition(0.2) == True
    print("相变智能体测试通过")

def test_bayesian_opt():
    print("\n=== 测试贝叶斯寻优 ===")
    opt = BayesianOptAgent({"lr": [0.0001, 0.01], "weight_decay": [1e-5, 1e-3]})
    params = opt.suggest_next_params()
    assert "lr" in params or "weight_decay" in params, "参数建议错误"
    opt.register_result(params, 0.8)
    print("贝叶斯寻优测试通过")

def test_cause_reward():
    print("\n=== 测试因果奖励 ===")
    reward = CauseRewardAgent()
    corr = reward.calculate_corrected_reward(0.8, 0.75)
    print(f"修正奖励: {corr:.4f}")
    assert len(reward.trajectory) == 1, "轨迹记录错误"
    print("因果奖励测试通过")

def test_transform_judger():
    print("\n=== 测试变身判定器 ===")
    judger = TransformJudger()
    state = GlobalState()
    state.e_self = 0.2
    assert judger.judge(state) == TransformLevel.NONE
    state.e_self = 0.4
    assert judger.judge(state) == TransformLevel.FIRST_BODY
    state.e_self = 0.7
    assert judger.judge(state) == TransformLevel.SECOND_MIND
    state.e_self = 0.9
    assert judger.judge(state) == TransformLevel.THIRD_TAO
    print("变身判定器测试通过")

def test_dist_comm():
    print("\n=== 测试分布式通信 ===")
    comm = DistComm("node_0", 9999)
    comm.register_node("node_1", "127.0.0.1", 10000)
    assert len(comm.node_registry) == 1, "节点注册错误"
    comm.sync_domain_prior("test", {"lr": 0.001}, 0.85)
    print("分布式通信测试通过")

def test_dist_scheduler():
    print("\n=== 测试负载均衡调度 ===")
    comm = DistComm("node_0", 9999)
    scheduler = DistLoadScheduler(comm)
    state1 = GlobalState()
    state1.e_self = 0.8
    state2 = GlobalState()
    state2.e_self = 0.5
    scheduler.refresh_node_level("node_1", state1)
    scheduler.refresh_node_level("node_2", state2)
    target = scheduler.allocate_task(0.8)
    assert target == "node_1", "高难度任务应该分配给高能级节点"
    target = scheduler.allocate_task(0.2)
    assert target == "node_2", "低难度任务应该分配给低能级节点"
    print("负载均衡调度测试通过")

def test_support_agents():
    print("\n=== 测试支撑智能体 ===")
    report = ResultGeneratorAgent()
    lib = BaseLibraryAgent()
    audit = AuditLoggerAgent()
    comm = AgentCommDispatcher()
    comm.register("report", report)
    comm.register("lib", lib)
    comm.register("audit", audit)
    comm.send("test", "lib", "update_lib", {"domain": "test", "hp": {"lr": 0.001}, "score": 0.85})
    comm.dispatch_all()
    print("支撑智能体测试通过")

def main():
    print("==== 系统模块测试 ====")
    test_global_state()
    test_flow_matrix()
    test_boundary_guard()
    test_phase_agent()
    test_bayesian_opt()
    test_cause_reward()
    test_transform_judger()
    test_dist_comm()
    test_dist_scheduler()
    test_support_agents()
    print("\n==== 所有测试通过 ====")

if __name__ == "__main__":
    main()