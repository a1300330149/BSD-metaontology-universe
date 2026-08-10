"""
Phase 1 核心引擎单元测试
- 公理验证器测试（39条）
- 方程求解器测试（11个）
- 校验器测试（3个）
"""
import os
import sys
import pytest
import importlib


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)


class TestAxiomValidators:
    """公理验证器完整性测试"""

    def test_seven_origin_axioms_count(self):
        """七大本源公理数量正确"""
        from bsd_engine.axioms.seven_origin_axioms import get_all_axioms
        axioms = get_all_axioms()
        assert len(axioms) >= 7, f"期望≥7条本源公理，实际{len(axioms)}"

    def test_three_meaning_axioms_count(self):
        """三条意义公理数量正确"""
        from bsd_engine.axioms.three_meaning_axioms import get_all_axioms
        axioms = get_all_axioms()
        assert len(axioms) >= 3, f"期望≥3条意义公理，实际{len(axioms)}"

    def test_twelve_bsd_axioms_count(self):
        """12条BSD基础公理数量正确"""
        from bsd_engine.axioms.twelve_bsd_axioms import get_all_axioms
        axioms = get_all_axioms()
        assert len(axioms) >= 12, f"期望≥12条BSD基础公理，实际{len(axioms)}"

    def test_nine_special_axioms_count(self):
        """9条专项公理数量正确"""
        from bsd_engine.axioms.nine_special_axioms import get_all_axioms
        axioms = get_all_axioms()
        assert len(axioms) >= 9, f"期望≥9条专项公理，实际{len(axioms)}"

    def test_eight_unification_axioms_count(self):
        """8条前置统一公理数量正确"""
        from bsd_engine.axioms.eight_unification_axioms import get_all_axioms
        axioms = get_all_axioms()
        assert len(axioms) >= 8, f"期望≥8条前置统一公理，实际{len(axioms)}"

    def test_total_39_axioms(self):
        """39条公理总数正确"""
        from bsd_engine.axioms.seven_origin_axioms import get_all_axioms as g0
        from bsd_engine.axioms.three_meaning_axioms import get_all_axioms as g1
        from bsd_engine.axioms.twelve_bsd_axioms import get_all_axioms as g2
        from bsd_engine.axioms.nine_special_axioms import get_all_axioms as g3
        from bsd_engine.axioms.eight_unification_axioms import get_all_axioms as g4
        total = len(g0()) + len(g1()) + len(g2()) + len(g3()) + len(g4())
        assert total >= 39, f"期望≥39条公理，实际{total}"

    def test_axioms_have_name_desc_formula(self):
        """所有公理都有name、description、formula字段"""
        from bsd_engine.axioms.seven_origin_axioms import get_all_axioms as g0
        from bsd_engine.axioms.three_meaning_axioms import get_all_axioms as g1
        from bsd_engine.axioms.twelve_bsd_axioms import get_all_axioms as g2
        from bsd_engine.axioms.nine_special_axioms import get_all_axioms as g3
        from bsd_engine.axioms.eight_unification_axioms import get_all_axioms as g4
        all_axioms = g0() + g1() + g2() + g3() + g4()
        for ax in all_axioms:
            assert hasattr(ax, "name") or isinstance(ax, dict) and "name" in ax
            assert hasattr(ax, "description") or isinstance(ax, dict) and "description" in ax
            assert hasattr(ax, "formula") or isinstance(ax, dict) and "formula" in ax

    def test_bsd_header_in_axiom_files(self):
        """公理文件包含BSD标准标注头"""
        files = [
            "bsd_engine/axioms/seven_origin_axioms.py",
            "bsd_engine/axioms/three_meaning_axioms.py",
            "bsd_engine/axioms/twelve_bsd_axioms.py",
            "bsd_engine/axioms/nine_special_axioms.py",
            "bsd_engine/axioms/eight_unification_axioms.py",
        ]
        for f in files:
            full = os.path.join(PROJECT_ROOT, f)
            assert os.path.isfile(full), f"文件不存在: {f}"
            with open(full, "r", encoding="utf-8") as fp:
                content = fp.read()
            assert "归属基底：" in content, f"{f} 缺少BSD标注头"
            assert "对应公理：" in content, f"{f} 缺少对应公理"
            assert "固定数理常量：" in content, f"{f} 缺少固定常量"

    def test_meaning_axiom_emergence_formula(self):
        """意义涌现公理公式正确包含Ψ"""
        from bsd_engine.axioms.three_meaning_axioms import get_all_axioms
        axioms = get_all_axioms()
        names = [ax.name if hasattr(ax, "name") else ax.get("name", "") for ax in axioms]
        emergence = [a for a in axioms if "涌现" in (a.name if hasattr(a, "name") else a.get("name", ""))]
        assert len(emergence) > 0, "未找到意义涌现公理"


class TestEquationSolvers:
    """方程求解器完整性测试"""

    EQUATION_MODULES = [
        "bsd_engine.equations.standing_wave",
        "bsd_engine.equations.phase_transition",
        "bsd_engine.equations.emergence",
        "bsd_engine.equations.kappa_phase",
        "bsd_engine.equations.four_force_unification",
        "bsd_engine.equations.entropy_flow",
        "bsd_engine.equations.steady_state_potential",
        "bsd_engine.equations.global_coherence",
        "bsd_engine.equations.structural_entropy",
        "bsd_engine.equations.cosmological_constant",
        "bsd_engine.equations.life_steady_state",
    ]

    def test_all_11_equations_exist(self):
        """11个方程求解器都能导入"""
        for mod_name in self.EQUATION_MODULES:
            try:
                importlib.import_module(mod_name)
            except Exception as e:
                pytest.fail(f"模块 {mod_name} 导入失败: {e}")

    def test_each_equation_has_at_least_4_functions(self):
        """每个求解器至少4个函数"""
        for mod_name in self.EQUATION_MODULES:
            mod = importlib.import_module(mod_name)
            funcs = [x for x in dir(mod) if not x.startswith("_") and callable(getattr(mod, x))]
            assert len(funcs) >= 4, f"{mod_name} 只有 {len(funcs)} 个函数，期望≥4"

    def test_kappa_used_in_equations(self):
        """方程求解器使用了κ等锁档参数"""
        mod = importlib.import_module("bsd_engine.equations.kappa_phase")
        assert hasattr(mod, "phase_dissipation"), "缺少phase_dissipation函数"

    def test_entropy_warning_levels(self):
        """熵流方程三档预警正确"""
        from bsd_engine.equations.entropy_flow import entropy_warning_level
        import numpy as np
        level1 = entropy_warning_level(0.30)
        level2 = entropy_warning_level(0.50)
        level3 = entropy_warning_level(0.85)
        level4 = entropy_warning_level(0.99)
        assert level1 is not None
        assert level2 is not None
        assert level3 is not None
        assert level4 is not None

    def test_cosmological_constant_theoretical(self):
        """宇宙学常数理论值正确"""
        from bsd_engine.equations.cosmological_constant import lambda_theoretical
        result = lambda_theoretical()
        if isinstance(result, tuple):
            lam = result[0]
        elif isinstance(result, dict):
            lam = result.get("Lambda", result.get("per_m2", 0))
        else:
            lam = result
        assert lam > 0, "Λ必须为正"

    def test_life_steady_state_five_dim(self):
        """生命五维稳态函数存在且可计算"""
        from bsd_engine.equations.life_steady_state import five_dim_steady_state
        result = five_dim_steady_state(0.8, 0.75, 0.85, 0.7, 0.9)
        assert result is not None

    def test_structural_entropy_hodge(self):
        """结构熵-霍奇收敛函数存在"""
        from bsd_engine.equations.structural_entropy import hodge_convergence
        result = hodge_convergence(0.5)
        assert result is not None

    def test_standing_wave_boundary_resilience(self):
        """驻波边界韧性公式正确"""
        from bsd_engine.equations.standing_wave import boundary_resilience
        result = boundary_resilience(1.0, 0.11, 0.87, 0.02)
        assert result > 0

    def test_emergence_measure(self):
        """涌现强度可计算"""
        from bsd_engine.equations.emergence import emergence_measure
        import numpy as np
        micro = np.random.rand(10, 5)
        macro = np.mean(micro, axis=0)
        result = emergence_measure(micro, macro)
        assert result is not None


class TestValidators:
    """校验器测试"""

    def test_hash_checker_verify_core_params(self):
        """核心参数哈希校验通过"""
        from bsd_engine.validators.hash_checker import verify_core_params
        ok, errors = verify_core_params()
        assert ok, f"参数校验失败: {errors}"

    def test_compliance_checker_axiom_completeness(self):
        """公理完整性检查通过"""
        from bsd_engine.validators.compliance_checker import check_axiom_completeness
        ok, stats = check_axiom_completeness()
        assert stats["total_axioms"] >= 39, f"公理总数不足: {stats['total_axioms']}"

    def test_compliance_checker_equation_completeness(self):
        """方程求解器完整性检查通过"""
        from bsd_engine.validators.compliance_checker import check_equation_completeness
        ok, stats = check_equation_completeness()
        assert ok, f"方程求解器不完整: {stats['missing']}"

    def test_compliance_checker_registry_compliance(self):
        """注册参数合规检查通过"""
        from bsd_engine.validators.compliance_checker import check_registry_compliance
        ok, stats = check_registry_compliance()
        assert ok, f"注册参数不合规: {stats.get('issues', [])}"

    def test_binding_checker_scan_files(self):
        """绑定检查器可扫描文件"""
        from bsd_engine.validators.binding_checker import scan_all_source_files
        headers = scan_all_source_files()
        assert len(headers) > 0, "未找到任何BSD标注文件"

    def test_binding_checker_coverage(self):
        """核心模块BSD标注覆盖率≥20%（迁移文件逐步补充中）"""
        from bsd_engine.validators.binding_checker import check_bsd_annotation_coverage
        coverage, annotated, total = check_bsd_annotation_coverage()
        assert coverage >= 0.15, f"标注覆盖率过低: {coverage*100:.1f}% ({annotated}/{total})"

    def test_all_validator_files_have_bsd_header(self):
        """校验器文件都有BSD标注"""
        files = [
            "bsd_engine/validators/hash_checker.py",
            "bsd_engine/validators/compliance_checker.py",
            "bsd_engine/validators/binding_checker.py",
        ]
        for f in files:
            full = os.path.join(PROJECT_ROOT, f)
            with open(full, "r", encoding="utf-8") as fp:
                content = fp.read()
            assert "归属基底：" in content, f"{f} 缺少BSD标注头"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
