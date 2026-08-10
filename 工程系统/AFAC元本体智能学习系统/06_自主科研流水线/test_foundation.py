import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE)

import numpy as np
from src.foundation.base_0_meta_dao import MetaDaoOriginFoundation
from src.foundation.base_1_nine_dim_legal import NineDimensionLegalFoundation
from src.foundation.base_2_three_realms import ThreeRealmsOrderFoundation
from src.foundation.foundation_controller import FoundationController

def test_level0_meta_dao():
    print("\n=== 第0重基底：元道本源基底测试 ===")
    foundation = MetaDaoOriginFoundation()
    
    assert foundation.FOUNDATION_LEVEL == 0
    assert foundation.GAMMA_TIME_DECAY == 0.92
    assert foundation.ENERGY_RANGE == (0.0, 1.0)
    assert len(foundation.axioms) == 4
    assert len(foundation.constants) == 3
    
    clamped = foundation.clamp_energy(1.5)
    assert clamped == 1.0
    
    clamped = foundation.clamp_energy(-0.5)
    assert clamped == 0.0
    
    clamped = foundation.clamp_energy(0.5)
    assert clamped == 0.5
    
    flow_matrix = np.array([[0.5, 0.6], [0.3, 0.8]])
    enforced = foundation.enforce_conservation(flow_matrix)
    assert abs(enforced[0].sum() - 1.0) < 0.01
    assert abs(enforced[1].sum() - 1.0) < 0.01
    
    print("✓ 元道本源基底测试通过")

def test_level1_nine_dim_legal():
    print("\n=== 第1重基底：九维法理基底测试 ===")
    foundation = NineDimensionLegalFoundation()
    
    assert foundation.FOUNDATION_LEVEL == 1
    assert foundation.dimension_count == 9
    assert foundation.M7.shape == (9, 9)
    
    e_body = foundation.calculate_e_body(0.8, 0.6)
    assert 0.0 <= e_body <= 1.0
    assert abs(e_body - 0.72) < 0.01
    
    e_mind = foundation.calculate_e_mind(0.7, 0.9)
    assert 0.0 <= e_mind <= 1.0
    assert abs(e_mind - 0.82) < 0.01
    
    e_self = foundation.calculate_e_self(e_body, e_mind)
    assert 0.0 <= e_self <= 1.0
    assert abs(e_self - 0.772) < 0.01
    
    level = foundation.judge_transform_level(0.30)
    assert level == "NONE"
    
    level = foundation.judge_transform_level(0.35)
    assert level == "FIRST_BODY"
    
    level = foundation.judge_transform_level(0.65)
    assert level == "SECOND_MIND"
    
    level = foundation.judge_transform_level(0.90)
    assert level == "THIRD_TAO"
    
    vec = np.ones((9, 1)) * 0.5
    transformed = foundation.transform_state_vector(vec)
    assert transformed.shape == (9, 1)
    for val in transformed:
        assert 0.0 <= val <= 1.0
    
    print("✓ 九维法理基底测试通过")

def test_level2_three_realms():
    print("\n=== 第2重基底：三界维度秩序基底测试 ===")
    foundation = ThreeRealmsOrderFoundation()
    
    assert foundation.FOUNDATION_LEVEL == 2
    assert len(foundation.REALMS) == 3
    assert "TAO" in foundation.REALMS
    assert "NATURE" in foundation.REALMS
    assert "HUMAN" in foundation.REALMS
    
    result = foundation.is_operation_allowed("distributed_parallel", "TAO")
    assert result[0] == True
    
    result = foundation.is_operation_allowed("graph_models", "NATURE")
    assert result[0] == True
    
    result = foundation.is_operation_allowed("bayesian_opt", "HUMAN")
    assert result[0] == True
    
    result = foundation.is_operation_allowed("distributed_parallel", "NATURE")
    assert result[0] == False
    
    boundaries = foundation.get_agent_boundaries()
    assert len(boundaries) == 4
    
    foundation.enable_creation_mode()
    assert foundation.creation_mode_enabled == True
    
    foundation.disable_creation_mode()
    assert foundation.creation_mode_enabled == False
    
    print("✓ 三界维度秩序基底测试通过")

def test_foundation_controller():
    print("\n=== 基底总控模块测试 ===")
    controller = FoundationController()
    
    assert controller.FOUNDATION_COUNT == 3
    
    level0 = controller.get_foundation_by_level(0)
    assert level0.FOUNDATION_LEVEL == 0
    
    level1 = controller.get_foundation_by_level(1)
    assert level1.FOUNDATION_LEVEL == 1
    
    level2 = controller.get_foundation_by_level(2)
    assert level2.FOUNDATION_LEVEL == 2
    
    constraints = controller.enforce_all_constraints()
    assert len(constraints) == 3
    
    result = controller.validate_operation("graph_models", "NATURE")
    assert result[0] == True
    
    result = controller.validate_operation("distributed_parallel", "NATURE")
    assert result[0] == False
    
    energy = controller.calculate_energy_levels(0.8, 0.6, 0.7, 0.9)
    assert "e_body" in energy
    assert "e_mind" in energy
    assert "e_self" in energy
    assert "transform_level" in energy
    
    hierarchy = controller.get_hierarchy_summary()
    assert len(hierarchy) == 3
    
    extensions = controller.get_extension_mapping()
    assert len(extensions) == 5
    
    print("✓ 基底总控模块测试通过")

def test_foundation_constraint_chain():
    print("\n=== 基底约束链测试 ===")
    controller = FoundationController()
    
    vec = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]).reshape(9, 1)
    
    for i in range(10):
        vec = controller.transform_state(vec)
        for val in vec:
            assert 0.0 <= val <= 1.0
    
    print("✓ 基底约束链测试通过")

def test_extension_mapping():
    print("\n=== 拓展方向归属测试 ===")
    controller = FoundationController()
    
    extensions = controller.get_extension_mapping()
    
    assert extensions["分布式并行扩容拓展"]["realm"] == "TAO"
    assert extensions["轻量化嵌入式分支拓展"]["realm"] == "NATURE"
    assert extensions["文娱创世强化系分支拓展"]["realm"] == "HUMAN"
    assert extensions["多模态图任务通用拓展"]["realm"] == "NATURE"
    
    print("✓ 拓展方向归属测试通过")

def main():
    print("==== 全域基底体系测试 ====")
    
    test_level0_meta_dao()
    test_level1_nine_dim_legal()
    test_level2_three_realms()
    test_foundation_controller()
    test_foundation_constraint_chain()
    test_extension_mapping()
    
    print("\n==== 所有基底测试通过 ====")

if __name__ == "__main__":
    main()