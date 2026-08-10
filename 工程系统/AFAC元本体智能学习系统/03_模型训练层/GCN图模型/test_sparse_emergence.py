import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import numpy as np
from src.foundation.base_1_nine_dim_legal import NineDimensionLegalFoundation
from src.foundation.base_2_three_realms import ThreeRealmsOrderFoundation
from src.foundation.foundation_controller import FoundationController
from src.master_agent.master_research_agent import MasterResearchAgent

def test_dynamic_kappa_adaptive():
    print("\n=== 第1重基底：动态阻尼系数（三阶分层自适应κ）测试 ===")
    foundation = NineDimensionLegalFoundation(task_mode="competition")
    
    kappa_none = foundation.get_kappa("NONE")
    kappa_first = foundation.get_kappa("FIRST_BODY")
    kappa_second = foundation.get_kappa("SECOND_MIND")
    kappa_third = foundation.get_kappa("THIRD_TAO")
    
    assert kappa_none == 0.30
    assert kappa_first == 0.35
    assert kappa_second == 0.42
    assert kappa_third == 0.50
    
    assert kappa_none < kappa_first < kappa_second < kappa_third
    
    kappa_adaptive_low = foundation.get_kappa_adaptive(0.2, delta_illu=0.1)
    kappa_adaptive_high = foundation.get_kappa_adaptive(0.8, delta_illu=0.2)
    
    assert kappa_adaptive_low <= kappa_adaptive_high
    
    foundation.switch_task_mode("research")
    kappa_research = foundation.get_kappa("SECOND_MIND")
    assert kappa_research == 0.35
    
    print("✓ 动态阻尼系数（三阶分层自适应κ）测试通过")

def test_reverse_emergence():
    print("\n=== 第1重基底：反向涌现机制测试 ===")
    foundation = NineDimensionLegalFoundation(task_mode="competition")
    
    initial_alpha = foundation.get_alpha_sparse()
    foundation.update_alpha_sparse(0.5)
    updated_alpha = foundation.get_alpha_sparse()
    
    assert updated_alpha > initial_alpha
    assert updated_alpha <= 0.35
    
    foundation.update_kappa_by_illusion(0.2)
    kappa_after = foundation.get_kappa("SECOND_MIND")
    assert kappa_after > 0.42
    
    foundation.update_flow_matrix_strength(0.5)
    assert foundation.M7[4, 2] > 0.6 and foundation.M7[4, 2] <= 0.72
    
    print("✓ 反向涌现机制测试通过")

def test_competition_cold_start():
    print("\n=== 第2重基底：竞赛模式冷启动优化测试 ===")
    foundation = ThreeRealmsOrderFoundation(task_mode="competition")
    
    nature_config = foundation.get_realm_config("NATURE")
    assert nature_config["skip_mlp_cold_start"] == True
    assert nature_config["phase_threshold_reduction"] == 0.10
    assert nature_config["feature_enhancement"] == True
    assert nature_config["missing_value_fill"] == True
    
    effective_threshold = foundation.get_effective_phase_threshold(0.35)
    assert abs(effective_threshold - 0.25) < 0.001
    
    human_config = foundation.get_realm_config("HUMAN")
    assert human_config["causal_reward_weight"] == 1.3
    assert human_config["adaptive_exploration"] == True
    assert human_config["bayes_explore_rate"] == 0.40
    
    tao_config = foundation.get_realm_config("TAO")
    assert tao_config["knowledge_sharing"] == True
    assert tao_config["preload_prior"] == True
    
    print("✓ 竞赛模式冷启动优化测试通过")

def test_emergence_cycle():
    print("\n=== 基底总控：双向涌现闭环测试 ===")
    controller = FoundationController()
    controller.switch_task_mode("competition")
    
    test_e_levels = [0.2, 0.3, 0.35, 0.4, 0.5, 0.6, 0.65, 0.7, 0.8, 0.85, 0.9, 0.95]
    expected_levels = ["NONE", "NONE", "FIRST_BODY", "FIRST_BODY", "FIRST_BODY", 
                       "FIRST_BODY", "SECOND_MIND", "SECOND_MIND", "SECOND_MIND",
                       "SECOND_MIND", "THIRD_TAO", "THIRD_TAO"]
    
    for idx, e_self in enumerate(test_e_levels):
        delta_illu = max(0.1 - idx * 0.005, 0.02)
        sparse_ratio = max(0.6 - idx * 0.03, 0.2)
        
        result = controller.run_emergence_cycle(
            sparse_ratio=sparse_ratio,
            delta_illu=delta_illu,
            e_self=e_self,
            max_steps=50,
            current_step=idx
        )
        
        assert result["transform_level"] == expected_levels[idx], \
            f"Step {idx}: Expected {expected_levels[idx]}, got {result['transform_level']}, e_self={e_self}"
    
    summary = controller.get_emergence_summary()
    assert summary["total_cycles"] == 12
    assert summary["current_level"] == "THIRD_TAO"
    assert summary["stabilized"] == True
    
    print("✓ 双向涌现闭环测试通过")

def test_master_agent_sparse_adaptation():
    print("\n=== 主智能体：稀疏反馈自适应机制测试 ===")
    
    config_competition = {
        "max_budget": 100,
        "domain": "graph_learning",
        "max_steps": 5,
        "task_target": "afac_competition",
        "dataset": {
            "data_path": os.path.join(BASE, "data/afac2026_sparse_graph.npz"),
            "feat_dim": 128,
            "hidden_dim": 64,
            "num_classes": 10,
            "num_nodes": 1000
        },
        "param_bounds": {
            "lr": [0.001, 0.005],
            "weight_decay": [1e-5, 1e-4]
        }
    }
    
    master = MasterResearchAgent(config_competition)
    
    assert master.task_mode == "competition"
    assert master.skip_mlp_cold_start == True
    assert master.feature_enhancement == True
    assert master.missing_value_fill == True
    assert master.causal_reward_weight == 1.3
    assert master.adaptive_exploration == True
    assert master.target_explore_rate == 0.40
    assert master.phase_threshold_reduction == 0.10
    assert master.knowledge_sharing == True
    assert master.guard.max_budget == 999999
    assert master.evolution_cycle == 5
    
    print("✓ 主智能体稀疏反馈自适应机制测试通过")

def test_sparse_compensation_formula():
    print("\n=== 稀疏补偿能量注入公式验证 ===")
    foundation = NineDimensionLegalFoundation(task_mode="competition")
    
    x_entity = 0.8
    x_phase = 0.6
    sparse_ratio = 0.5
    
    e_body_sparse = foundation.calculate_e_body(x_entity, x_phase, sparse_ratio)
    e_body_base = 0.6 * x_entity + 0.4 * x_phase
    expected_sparse = e_body_base + 0.18 * sparse_ratio
    
    assert abs(e_body_sparse - expected_sparse) < 0.01
    
    foundation.switch_task_mode("research")
    e_body_research = foundation.calculate_e_body(x_entity, x_phase, sparse_ratio)
    
    assert abs(e_body_research - e_body_base) < 0.01
    assert e_body_sparse > e_body_research
    
    print("✓ 稀疏补偿能量注入公式验证通过")

def test_flow_matrix_enhancement():
    print("\n=== 流转矩阵稀疏专项强化验证 ===")
    foundation_comp = NineDimensionLegalFoundation(task_mode="competition")
    foundation_research = NineDimensionLegalFoundation(task_mode="research")
    
    assert foundation_comp.M7[4, 2] == 0.72
    assert foundation_comp.M7[5, 3] == 0.81
    
    assert foundation_research.M7[4, 2] == 0.6
    assert foundation_research.M7[5, 3] == 0.7
    
    assert foundation_comp.M7[4, 2] > foundation_research.M7[4, 2]
    assert foundation_comp.M7[5, 3] > foundation_research.M7[5, 3]
    
    enhancement_ratio_42 = (0.72 - 0.6) / 0.6
    enhancement_ratio_53 = (0.81 - 0.7) / 0.7
    
    assert enhancement_ratio_42 >= 0.2
    assert enhancement_ratio_53 >= 0.15
    
    print("✓ 流转矩阵稀疏专项强化验证通过")

def main():
    print("==== AFAC2026赛题三稀疏反馈自动化实验降维打击方案测试 ====")
    
    test_dynamic_kappa_adaptive()
    test_reverse_emergence()
    test_competition_cold_start()
    test_emergence_cycle()
    test_master_agent_sparse_adaptation()
    test_sparse_compensation_formula()
    test_flow_matrix_enhancement()
    
    print("\n==== 所有赛题三专项测试通过 ====")

if __name__ == "__main__":
    main()
