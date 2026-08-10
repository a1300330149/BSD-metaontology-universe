"""
T90 V1.8 四大算子模块单元测试
【理论版本：ACTIVE-V1.8】
【归属基底】0重元道本源基底 + 1重九维法理基底
【对应公理】公理十一/十二/十三 + C4/C5
【测试范围】
- C1 双向迭代算子（𝒯₊/𝒯₋/𝒟）
- C2 六层多元进制（B₁-B₆）
- C3 三个0.9同构定理
- C5 3×3粒子家族矩阵
- T90 V1.8 新增参数注册与校验
"""
import os
import sys
import math

try:
    import pytest
    _HAS_PYTEST = True
except ImportError:
    _HAS_PYTEST = False
    pytest = None

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


# ============================================================================
# C1 双向迭代算子测试
# ============================================================================
class TestBidirectionalIterationOperator:
    """C1 双向迭代算子（𝒯₊/𝒯₋/𝒟）测试"""

    def test_clockwise_expansion_mappings_count(self):
        """𝒯₊顺时针展开算子必须包含6个映射f₁-f₆"""
        from bsd_engine.core.bidirectional_iteration_operator import ClockwiseExpansionOperator
        op = ClockwiseExpansionOperator()
        assert len(op.MAPPINGS) == 6, f"𝒯₊必须包含6个映射，实际{len(op.MAPPINGS)}"
        names = [m["name"] for m in op.MAPPINGS]
        assert names == ["f1", "f2", "f3", "f4", "f5", "f6"]

    def test_counterclockwise_reversal_mappings_count(self):
        """𝒯₋逆时针逆反算子必须包含7个映射g₁-g₇"""
        from bsd_engine.core.bidirectional_iteration_operator import CounterclockwiseReversalOperator
        op = CounterclockwiseReversalOperator()
        assert len(op.MAPPINGS) == 7, f"𝒯₋必须包含7个映射，实际{len(op.MAPPINGS)}"
        names = [m["name"] for m in op.MAPPINGS]
        assert names == ["g1", "g2", "g3", "g4", "g5", "g6", "g7"]

    def test_clockwise_expansion_path(self):
        """𝒯₊顺时针展开路径：0∅ → 1 → 3 → 6 → 9 → 12 → N"""
        from bsd_engine.core.bidirectional_iteration_operator import (
            ClockwiseExpansionOperator,
            IterationState,
        )
        op = ClockwiseExpansionOperator()
        state = IterationState(value="0∅", stage="initial", dimension=0)
        result = op.apply(state)
        assert result.value == "N", f"𝒯₊最终状态应为N，实际{result.value}"
        assert result.dimension == 6, f"𝒯₊最终维度应为6，实际{result.dimension}"

    def test_counterclockwise_reversal_path(self):
        """𝒯₋逆时针逆反路径：N → 12 → 9 → 6 → 3 → 1 → 0_迹 → 1'"""
        from bsd_engine.core.bidirectional_iteration_operator import (
            CounterclockwiseReversalOperator,
            IterationState,
        )
        op = CounterclockwiseReversalOperator()
        state = IterationState(value="N", stage="after_t_plus", dimension=6,
                               info_content=float('inf'))
        result = op.apply(state)
        assert result.value == "1'", f"𝒯₋最终状态应为1'，实际{result.value}"

    def test_ascension_operator_not_identity(self):
        """定理11.19：𝒟 = 𝒯₋ ∘ 𝒯₊ ≠ Id（升维不可恒等还原）"""
        from bsd_engine.core.bidirectional_iteration_operator import (
            AscensionOperator,
            IterationState,
        )
        op = AscensionOperator()
        state = IterationState(value="0∅", stage="initial", dimension=0)
        result = op.apply(state)
        assert result.value == "1'", f"𝒟最终状态应为1'，实际{result.value}"
        assert result.value != "0∅", "𝒟=Id违反定理11.19（升维不可还原）"
        assert result.value != "1", "𝒟不能还原为1（必须升维至1'）"

    def test_information_trace_conservation(self):
        """推论11.9：信息痕迹守恒律，Info(1') > Info(1)"""
        from bsd_engine.core.bidirectional_iteration_operator import (
            AscensionOperator,
            IterationState,
        )
        op = AscensionOperator()
        state = IterationState(value="0∅", stage="initial", dimension=0)
        result = op.apply(state)
        # 升维后信息量必须严格大于初始1元状态
        assert result.info_content > 1.0, (
            f"信息痕迹守恒律违反：Info(1')={result.info_content} ≤ Info(1)=1.0"
        )

    def test_dual_operator_pair_completeness(self):
        """公理十一强制：𝒯₊/𝒯₋必须成对出现，禁止单时针"""
        from bsd_engine.core.bidirectional_iteration_operator import (
            ClockwiseExpansionOperator,
            CounterclockwiseReversalOperator,
        )
        # 两个算子都必须可实例化
        t_plus = ClockwiseExpansionOperator()
        t_minus = CounterclockwiseReversalOperator()
        assert t_plus is not None
        assert t_minus is not None
        # 映射数量必须严格匹配（6+7=13）
        assert len(t_plus.MAPPINGS) + len(t_minus.MAPPINGS) == 13

    def test_full_iteration_duality_theorem(self):
        """BidirectionalIterationOperator.execute_full_iteration 校验定理11.19"""
        from bsd_engine.core.bidirectional_iteration_operator import BidirectionalIterationOperator
        module = BidirectionalIterationOperator()
        result = module.execute_full_iteration()
        assert result["final_state"] == "1'"
        assert result["duality_theorem_11_19"]["passed"], "定理11.19对偶性校验失败"
        assert result["info_trace_corollary_11_9"]["passed"], "推论11.9信息痕迹守恒律校验失败"
        assert result["ascension_verified"] is True


# ============================================================================
# C2 六层多元进制测试
# ============================================================================
class TestSixLevelBaseEmergence:
    """C2 六层多元进制（B₁-B₆）测试"""

    def test_six_bases_count(self):
        """必须定义6层进制B₁-B₆"""
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        module = SixLevelBaseEmergence()
        assert len(module.bases) == 6, f"必须定义6层进制，实际{len(module.bases)}"

    def test_base_cardinality_sequence(self):
        """六层进制基数序列：2, 3, 6, 10, 12, ∞"""
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        module = SixLevelBaseEmergence()
        cardinalities = [b.cardinality for b in module.bases]
        # 前5层必须是有限数
        assert cardinalities[0] == 2, f"B₁二进制基数必须为2，实际{cardinalities[0]}"
        assert cardinalities[1] == 3, f"B₂三进制基数必须为3，实际{cardinalities[1]}"
        assert cardinalities[2] == 6, f"B₃六进制基数必须为6，实际{cardinalities[2]}"
        assert cardinalities[3] == 10, f"B₄十进制基数必须为10，实际{cardinalities[3]}"
        assert cardinalities[4] == 12, f"B₅十二进制基数必须为12，实际{cardinalities[4]}"
        # B₆可以是∞或大数
        b6 = cardinalities[5]
        assert b6 in (float('inf'), -1, 999999, None) or (isinstance(b6, (int, float)) and b6 > 1000), (
            f"B₆ N进制必须表示无限，实际{b6}"
        )

    def test_emergence_theorem(self):
        """定理11.21：|B_{k+1}| = |B_k| + Δ_k"""
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        module = SixLevelBaseEmergence()
        result = module.verify_emergence_theorem()
        assert result["all_passed"], f"层级涌现定理校验失败：{result.get('all_transitions', '')}"

    def test_no_reverse_generation(self):
        """推论11.11：低维进制无法反向生成高维进制"""
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        module = SixLevelBaseEmergence()
        # 验证每层严格大于下层
        for i in range(5):
            lower = module.bases[i].cardinality
            upper = module.bases[i + 1].cardinality
            # 处理∞情况
            if upper == float('inf') or upper == -1:
                continue
            assert upper > lower, (
                f"B_{i+2}（{upper}）必须严格大于B_{i+1}（{lower}），违反不可逆性"
            )

    def test_civilization_mapping(self):
        """六层进制对应文明跃迁映射"""
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        module = SixLevelBaseEmergence()
        for base in module.bases:
            assert base.civilization, f"B_{base.level}缺少文明对应"
            assert base.energy_level > 0, f"B_{base.level}能级必须>0"

    def test_no_cross_level_skip(self):
        """禁止跨层推导：B₁→B₄直接跳跃违规"""
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        module = SixLevelBaseEmergence()
        # 验证Δ_k序列，每层都有delta
        for i in range(5):
            delta = module.bases[i].delta
            assert delta > 0 or delta == float('inf'), (
                f"B_{i+1}的delta必须>0（涌现新维度），实际{delta}"
            )


# ============================================================================
# C3 三个0.9同构定理测试
# ============================================================================
class TestThreeNineIsomorphism:
    """C3 三个0.9同构定理测试"""

    def test_three_isomorphisms_count(self):
        """必须定义3个0.9同构关系"""
        from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
        module = ThreeNineIsomorphism()
        assert len(module.isomorphisms) == 3, (
            f"必须定义3个0.9同构关系，实际{len(module.isomorphisms)}"
        )

    def test_shared_coefficient_k_plus(self):
        """三者共享系数k₊=0.9"""
        from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
        from bsd_engine.registry.constants import K_PLUS
        module = ThreeNineIsomorphism()
        for iso in module.isomorphisms:
            assert iso["coefficient"] == K_PLUS, (
                f"{iso['name']}的共享系数必须为k₊={K_PLUS}，实际{iso['coefficient']}"
            )
        assert K_PLUS == 0.9, f"k₊必须等于0.9，实际{K_PLUS}"

    def test_dimension_progression(self):
        """维度递进：1维→2维→3维"""
        from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
        module = ThreeNineIsomorphism()
        dimensions = [iso["dimension"] for iso in module.isomorphisms]
        assert dimensions == [1, 2, 3], f"维度递进必须为1→2→3，实际{dimensions}"

    def test_pi2_isomorphism(self):
        """Π₂ = π × k₊ 检验"""
        from bsd_engine.registry.constants import PI_2, PI_LOCKED, K_PLUS
        expected = PI_LOCKED * K_PLUS
        assert abs(PI_2 - expected) < 1e-10, (
            f"Π₂=π×k₊同构约束破坏：期望{expected}，实际{PI_2}"
        )

    def test_isomorphism_verification(self):
        """三重同构验证通过"""
        from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
        module = ThreeNineIsomorphism()
        result = module.verify_isomorphism()
        assert result["all_passed"], f"三0.9同构验证失败：{result.get('errors', '')}"


# ============================================================================
# C5 3×3粒子家族矩阵测试
# ============================================================================
class TestParticleFamilyMatrix:
    """C5 3×3粒子家族矩阵测试"""

    def test_three_families_count(self):
        """必须定义3大粒子家族"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        assert len(module.FAMILIES) == 3, (
            f"必须定义3大粒子家族，实际{len(module.FAMILIES)}"
        )

    def test_arithmetic_sequence(self):
        """定理6：三大家族各自为公差3的等差数列"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        result = module.verify_arithmetic_sequence()
        assert result["all_passed"], f"等差数列验证失败：{result.get('families', '')}"

    def test_individuality_family(self):
        """个体性家族：1, 4, 7（公差3）"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        numbers = module.FAMILIES["individuality"]["numbers"]
        assert numbers == [1, 4, 7], f"个体性家族必须为[1,4,7]，实际{numbers}"
        diffs = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
        assert all(d == 3 for d in diffs), f"公差必须为3，实际{diffs}"

    def test_variability_family(self):
        """变化性家族：2, 5, 8（公差3）"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        numbers = module.FAMILIES["variability"]["numbers"]
        assert numbers == [2, 5, 8], f"变化性家族必须为[2,5,8]，实际{numbers}"

    def test_relationality_family(self):
        """关系性家族：3, 6, 9（公差3）"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        numbers = module.FAMILIES["relationality"]["numbers"]
        assert numbers == [3, 6, 9], f"关系性家族必须为[3,6,9]，实际{numbers}"

    def test_yin_yang_duality(self):
        """定理7：顺时针=奇数/阳，逆时针=偶数/阴"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        result = module.verify_yin_yang_duality()
        assert result["all_passed"], f"阴阳对偶验证失败：{result.get('coupling_pairs', '')}"

    def test_digit_conservation(self):
        """定理8：1+1+1+2+2+2=9数字位守恒"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        result = module.verify_digit_conservation()
        assert result["all_passed"], f"数字位守恒验证失败：{result.get('system_digit_counts', '')}"

    def test_all_digits_covered(self):
        """3×3矩阵必须精确填满1-9"""
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        module = ParticleFamilyMatrix()
        all_numbers = []
        for family_info in module.FAMILIES.values():
            all_numbers.extend(family_info["numbers"])
        assert sorted(all_numbers) == [1, 2, 3, 4, 5, 6, 7, 8, 9], (
            f"3×3矩阵必须填满1-9，实际{sorted(all_numbers)}"
        )


# ============================================================================
# T90 V1.8 参数注册与校验测试
# ============================================================================
class TestT90V18Constants:
    """T90 V1.8 新增参数注册与校验测试"""

    def test_k_plus_registered(self):
        """k₊=0.9 已注册"""
        from bsd_engine.registry.constants import K_PLUS, ALL_LOCKED_PARAMS
        assert K_PLUS == 0.9
        assert "K_PLUS" in ALL_LOCKED_PARAMS

    def test_k_minus_registered(self):
        """k₋=0.1 已注册"""
        from bsd_engine.registry.constants import K_MINUS, ALL_LOCKED_PARAMS
        assert K_MINUS == 0.1
        assert "K_MINUS" in ALL_LOCKED_PARAMS

    def test_k_plus_k_minus_duality(self):
        """对偶性校验：k₊ + k₋ = 1.0"""
        from bsd_engine.registry.constants import K_PLUS, K_MINUS
        assert abs((K_PLUS + K_MINUS) - 1.0) < 1e-10, (
            f"k₊+k₋对偶约束破坏：{K_PLUS}+{K_MINUS}={K_PLUS + K_MINUS}"
        )

    def test_s_zero_registered(self):
        """S₀=0.81 已注册"""
        from bsd_engine.registry.constants import S_ZERO, ALL_LOCKED_PARAMS
        assert S_ZERO == 0.81
        assert "S_ZERO" in ALL_LOCKED_PARAMS

    def test_lambda_registered(self):
        """λ=0.62 已注册"""
        from bsd_engine.registry.constants import LAMBDA, ALL_LOCKED_PARAMS
        assert LAMBDA == 0.62
        assert "LAMBDA" in ALL_LOCKED_PARAMS

    def test_lambda_inv_registered(self):
        """λ⁻=1.38 已注册"""
        from bsd_engine.registry.constants import LAMBDA_INV, ALL_LOCKED_PARAMS
        assert LAMBDA_INV == 1.38
        assert "LAMBDA_INV" in ALL_LOCKED_PARAMS

    def test_pi_locked_registered(self):
        """π=3.1415926535 已注册"""
        from bsd_engine.registry.constants import PI_LOCKED, ALL_LOCKED_PARAMS
        assert PI_LOCKED == 3.1415926535
        assert "PI_LOCKED" in ALL_LOCKED_PARAMS

    def test_pi2_registered(self):
        """Π₂=2.8274333882 已注册"""
        from bsd_engine.registry.constants import PI_2, ALL_LOCKED_PARAMS
        assert PI_2 == 2.8274333882
        assert "PI_2" in ALL_LOCKED_PARAMS

    def test_pi2_isomorphism_check(self):
        """Π₂ = π × k₊ 同构校验"""
        from bsd_engine.registry.constants import PI_2, PI_LOCKED, K_PLUS
        expected = PI_LOCKED * K_PLUS
        assert abs(PI_2 - expected) < 1e-10, (
            f"Π₂=π×k₊同构约束破坏：期望{expected}，实际{PI_2}"
        )

    def test_verify_params_passes(self):
        """verify_params() 通过校验"""
        from bsd_engine.registry.constants import verify_params
        assert verify_params() is True, "verify_params()必须返回True"

    def test_all_locked_params_complete(self):
        """ALL_LOCKED_PARAMS 包含所有T90 V1.8新增参数"""
        from bsd_engine.registry.constants import ALL_LOCKED_PARAMS
        required = [
            "E1", "E2", "E3", "GAMMA", "KAPPA", "KAPPA_COMPETITION",
            "ALPHA", "THETA_NEG", "THETA_MV", "THETA_EVO",
            # T90 V1.8 新增
            "K_PLUS", "K_MINUS", "S_ZERO", "LAMBDA", "LAMBDA_INV",
            "PI_LOCKED", "PI_2",
        ]
        for param in required:
            assert param in ALL_LOCKED_PARAMS, f"缺少必需参数：{param}"


# ============================================================================
# 理论-代码双向绑定测试
# ============================================================================
class TestTheoryCodeBinding:
    """理论-代码双向绑定测试"""

    def test_c1_module_validate(self):
        """C1模块validate()通过"""
        from bsd_engine.core.bidirectional_iteration_operator import BidirectionalIterationOperator
        module = BidirectionalIterationOperator()
        ok, errors = module.validate()
        assert ok, f"C1模块验证失败：{errors}"

    def test_c1_module_inherits_base(self):
        """C1模块继承BaseTheoryModule"""
        from bsd_engine.core.base_theory_module import BaseTheoryModule
        from bsd_engine.core.bidirectional_iteration_operator import BidirectionalIterationOperator
        assert issubclass(BidirectionalIterationOperator, BaseTheoryModule)

    def test_c2_module_inherits_base(self):
        """C2模块继承BaseTheoryModule"""
        from bsd_engine.core.base_theory_module import BaseTheoryModule
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        assert issubclass(SixLevelBaseEmergence, BaseTheoryModule)

    def test_c3_module_inherits_base(self):
        """C3模块继承BaseTheoryModule"""
        from bsd_engine.core.base_theory_module import BaseTheoryModule
        from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
        assert issubclass(ThreeNineIsomorphism, BaseTheoryModule)

    def test_c5_module_inherits_base(self):
        """C5模块继承BaseTheoryModule"""
        from bsd_engine.core.base_theory_module import BaseTheoryModule
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix
        assert issubclass(ParticleFamilyMatrix, BaseTheoryModule)

    def test_all_modules_validate(self):
        """所有T90 V1.8模块validate()通过"""
        from bsd_engine.core.bidirectional_iteration_operator import BidirectionalIterationOperator
        from bsd_engine.core.six_level_base_emergence import SixLevelBaseEmergence
        from bsd_engine.core.three_nine_isomorphism import ThreeNineIsomorphism
        from bsd_engine.core.particle_family_matrix import ParticleFamilyMatrix

        modules = [
            BidirectionalIterationOperator(),
            SixLevelBaseEmergence(),
            ThreeNineIsomorphism(),
            ParticleFamilyMatrix(),
        ]
        for mod in modules:
            ok, errors = mod.validate()
            assert ok, f"模块{mod.__class__.__name__}验证失败：{errors}"


if __name__ == "__main__":
    if _HAS_PYTEST:
        pytest.main([__file__, "-v", "--tb=short"])
    else:
        # 降级为简化运行：实例化所有测试类并执行所有test_方法
        import inspect
        classes = [
            TestBidirectionalIterationOperator,
            TestSixLevelBaseEmergence,
            TestThreeNineIsomorphism,
            TestParticleFamilyMatrix,
            TestT90V18Constants,
            TestTheoryCodeBinding,
        ]
        total = 0
        passed = 0
        failed = 0
        for cls in classes:
            instance = cls()
            methods = [m for m in dir(instance) if m.startswith("test_")]
            for method_name in methods:
                total += 1
                try:
                    getattr(instance, method_name)()
                    passed += 1
                    print(f"  [PASS] {cls.__name__}.{method_name}")
                except Exception as e:
                    failed += 1
                    print(f"  [FAIL] {cls.__name__}.{method_name}: {e}")
        print(f"\n=== T90 V1.8 测试套件结果 ===")
        print(f"总计: {total}, 通过: {passed}, 失败: {failed}")
        if failed > 0:
            sys.exit(1)
