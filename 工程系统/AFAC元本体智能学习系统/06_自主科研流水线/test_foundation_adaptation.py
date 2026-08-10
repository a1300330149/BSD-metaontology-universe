import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import numpy as np
from src.foundation.base_1_nine_dim_legal import NineDimensionLegalFoundation
from src.foundation.base_2_three_realms import ThreeRealmsOrderFoundation
from src.foundation.foundation_controller import FoundationController

def test_level1_competition_params():
    print("\n=== 第1重基底：竞赛模式专项参数测试 ===")
    foundation = NineDimensionLegalFoundation(task_mode="competition")
    
    assert foundation.task_mode == "competition"
    assert foundation.get_kappa() == 0.42
    assert foundation.get_alpha_sparse() == 0.18
    
    assert foundation.M7[4, 2] == 0.72
    assert foundation.M7[5, 3] == 0.81
    
    e_body_comp = foundation.calculate_e_body(0.8, 0.6, sparse_ratio=0.5)
    e_body_base = 0.6 * 0.8 + 0.4 * 0.6
    expected_with_sparse = e_body_base + 0.18 * 0.5
    assert abs(e_body_comp - expected_with_sparse) < 0.01
    
    foundation.switch_task_mode("research")
    assert foundation.task_mode == "research"
    assert foundation.get_kappa() == 0.35
    assert foundation.get_alpha_sparse() == 0.0
    
    e_body_research = foundation.calculate_e_body(0.8, 0.6, sparse_ratio=0.5)
    assert abs(e_body_research - e_body_base) < 0.01
    
    print("✓ 第1重基底竞赛/科研参数切换测试通过")

def test_level1_ablation():
    print("\n=== 第1重基底：消融实验支持测试 ===")
    foundation = NineDimensionLegalFoundation(task_mode="research")
    
    vec = np.ones((9, 1)) * 0.5
    
    foundation.set_ablation_mask(1, False)
    M7_effective = foundation.M7 * foundation.ablation_masks
    assert M7_effective[1, :].sum() == 0
    assert M7_effective[:, 1].sum() == 0
    
    foundation.set_ablation_mask(1, True)
    M7_effective = foundation.M7 * foundation.ablation_masks
    assert M7_effective[1, :].sum() > 0
    
    exported = foundation.export_state_vector(vec)
    assert len(exported) == 9
    for name in foundation.DIMENSION_NAMES:
        assert name in exported
    
    print("✓ 第1重基底消融实验支持测试通过")

def test_level2_competition_order():
    print("\n=== 第2重基底：竞赛秩序约束测试 ===")
    foundation = ThreeRealmsOrderFoundation(task_mode="competition")
    
    assert foundation.task_mode == "competition"
    
    tao_config = foundation.get_realm_config("TAO")
    assert tao_config["budget_limit"] == False
    assert tao_config["distributed_parallel"] == True
    assert tao_config["priority_by_eself"] == True
    
    nature_config = foundation.get_realm_config("NATURE")
    assert nature_config["auto_phase_upgrade"] == True
    assert nature_config["sparse_debias_always_on"] == True
    assert nature_config["enable_lightweight"] == False
    assert nature_config["max_hidden_dim"] == 256
    
    human_config = foundation.get_realm_config("HUMAN")
    assert human_config["bayes_explore_rate"] == 0.45
    assert human_config["reward_weight"] == 1.2
    assert human_config["evolution_cycle"] == 5
    assert human_config["negative_transfer_strict"] == False
    
    print("✓ 第2重基底竞赛秩序约束测试通过")

def test_level2_research_order():
    print("\n=== 第2重基底：科研秩序约束测试 ===")
    foundation = ThreeRealmsOrderFoundation(task_mode="research")
    
    assert foundation.task_mode == "research"
    
    tao_config = foundation.get_realm_config("TAO")
    assert tao_config["budget_limit"] == True
    assert tao_config["distributed_parallel"] == False
    
    nature_config = foundation.get_realm_config("NATURE")
    assert nature_config["auto_phase_upgrade"] == False
    assert nature_config["sparse_debias_always_on"] == False
    assert nature_config["enable_lightweight"] == True
    assert nature_config["max_hidden_dim"] == 128
    
    human_config = foundation.get_realm_config("HUMAN")
    assert human_config["bayes_explore_rate"] == 0.20
    assert human_config["reward_weight"] == 1.0
    assert human_config["evolution_cycle"] == 10
    assert human_config["negative_transfer_strict"] == True
    
    print("✓ 第2重基底科研秩序约束测试通过")

def test_controller_dual_mode():
    print("\n=== 基底总控：双模式联动测试 ===")
    controller = FoundationController()
    
    controller.level1.switch_task_mode("competition")
    controller.level2.switch_task_mode("competition")
    
    assert controller.level1.task_mode == "competition"
    assert controller.level2.task_mode == "competition"
    
    e_body_comp = controller.level1.calculate_e_body(0.8, 0.6, sparse_ratio=0.5)
    
    controller.level1.switch_task_mode("research")
    controller.level2.switch_task_mode("research")
    
    assert controller.level1.task_mode == "research"
    assert controller.level2.task_mode == "research"
    
    e_body_research = controller.level1.calculate_e_body(0.8, 0.6, sparse_ratio=0.5)
    
    assert e_body_comp > e_body_research
    
    constraints = controller.enforce_all_constraints()
    assert "NINE_DIMENSION_LEGAL" in constraints
    assert "THREE_REALMS_ORDER" in constraints
    
    print("✓ 基底总控双模式联动测试通过")

def test_master_agent_integration():
    print("\n=== 主智能体集成基底约束测试 ===")
    from src.master_agent.master_research_agent import MasterResearchAgent
    
    config_research = {
        "max_budget": 100,
        "domain": "graph_learning",
        "max_steps": 5,
        "task_target": "academic_research",
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
    
    master_research = MasterResearchAgent(config_research)
    assert master_research.task_mode == "research"
    assert master_research.foundation.level1.task_mode == "research"
    assert master_research.evolution_cycle == 10
    
    config_competition = config_research.copy()
    config_competition["task_target"] = "afac_competition"
    
    master_competition = MasterResearchAgent(config_competition)
    assert master_competition.task_mode == "competition"
    assert master_competition.foundation.level1.task_mode == "competition"
    assert master_competition.evolution_cycle == 5
    assert master_competition.guard.max_budget == 999999
    
    print("✓ 主智能体集成基底约束测试通过")

def test_transform_thresholds_consistency():
    print("\n=== 三阶变身阈值一致性测试 ===")
    foundation_comp = NineDimensionLegalFoundation(task_mode="competition")
    foundation_research = NineDimensionLegalFoundation(task_mode="research")
    
    for threshold in ["E1", "E2", "E3"]:
        assert foundation_comp.TRANSFORM_THRESHOLDS[threshold] == foundation_research.TRANSFORM_THRESHOLDS[threshold]
    
    assert foundation_comp.TRANSFORM_THRESHOLDS["E1"] == 0.35
    assert foundation_comp.TRANSFORM_THRESHOLDS["E2"] == 0.65
    assert foundation_comp.TRANSFORM_THRESHOLDS["E3"] == 0.90
    
    for e_self in [0.30, 0.35, 0.60, 0.65, 0.85, 0.90]:
        level_comp = foundation_comp.judge_transform_level(e_self)
        level_research = foundation_research.judge_transform_level(e_self)
        assert level_comp == level_research
    
    print("✓ 三阶变身阈值一致性测试通过")

def main():
    print("==== 第1、2重基底专项适配测试 ====")
    
    test_level1_competition_params()
    test_level1_ablation()
    test_level2_competition_order()
    test_level2_research_order()
    test_controller_dual_mode()
    test_master_agent_integration()
    test_transform_thresholds_consistency()
    
    print("\n==== 所有基底专项适配测试通过 ====")

if __name__ == "__main__":
    main()