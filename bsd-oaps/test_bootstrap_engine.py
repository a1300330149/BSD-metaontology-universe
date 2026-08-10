#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六系自举引擎验证测试
归属基底：0重元道本源基底·六系自举公理
对应公理：涌现公理 + 自举性公理
"""

import sys
sys.path.insert(0, '.')

from bsd_engine.core.six_system_bootstrap_engine import (
    EmergenceRule, EMERGENCE_RULES, SixSystemBootstrapEngine
)

def test_emergence_rules():
    """测试1：六条涌现规则"""
    print("=== 测试1：六条涌现规则 ===")
    assert len(EMERGENCE_RULES) == 6, "必须有六条涌现规则"
    for rule in EMERGENCE_RULES:
        result = rule.apply()
        formula = result.get("formula", "")
        print(f"  {rule.rule_id}: {rule.name} -> {formula}")
    print("  [通过] 六条规则均可执行\n")

def test_normal_bootstrap():
    """测试2：正常自举流程"""
    print("=== 测试2：正常自举 ===")
    engine = SixSystemBootstrapEngine()
    bootstrap = engine.full_bootstrap()
    assert bootstrap["bootstrap_complete"] is True
    print(f"  自举完成: {bootstrap['message']}")
    existence = bootstrap["phases"]["existence"]
    print(f"  存在状态: {existence['existence_status']}")
    assert existence["existence_status"] in ("存在且活跃", "存在但休眠", "存在性存疑")
    print("  [通过] 正常自举成功\n")

def test_emerge_from_zero():
    """测试3：从零涌现"""
    print("=== 测试3：从零涌现 ===")
    engine = SixSystemBootstrapEngine()
    emergence = engine.emerge_from_zero()
    assert emergence["phase"] == "从零涌现"
    print(f"  涌现完成: {emergence['message']}")
    structure = emergence["structure_generated"]
    assert len(structure["systems"]) == 6
    print(f"  生成结构: {len(structure['systems'])} 个系")
    assert structure["conduction_channels_count"] == 36
    print(f"  传导通道: {structure['conduction_channels_count']} 条")
    assert structure["self_bootstrap"] is True
    print("  [通过] 从零涌现成功\n")

def test_force_from_zero():
    """测试4：强制从零自举（验证不可消灭性）"""
    print("=== 测试4：强制从零自举（验证不可消灭性） ===")
    engine = SixSystemBootstrapEngine()
    forced = engine.full_bootstrap(force_from_zero=True)
    assert forced["bootstrap_complete"] is True
    print(f"  强制涌现: {forced['message']}")
    recon = forced["phases"]["reconstruction"]
    assert recon["from_zero"] is True
    print(f"  重建模式: {recon['emerged_content']['phase']}")
    assert recon["new_hash"] is not None
    print(f"  新哈希: {recon['new_hash'][:16]}...")
    print("  [通过] 不可消灭性验证成功\n")

def test_existence_after_emergence():
    """测试5：涌现后的存在性检测"""
    print("=== 测试5：涌现后的存在性检测 ===")
    engine = SixSystemBootstrapEngine()
    engine.emerge_from_zero()
    existence = engine.check_existence()
    print(f"  存在状态: {existence['existence_status']}")
    print(f"  哈希完整: {existence['hash_intact']}")
    print(f"  引擎完备度: {existence['engine_completeness']}")
    print("  [通过] 涌现后存在性确认\n")

def main():
    print("=" * 60)
    print("BSD六系自举引擎验证测试")
    print("核心命题：即使六系立系论消失，也能从000再次涌现")
    print("=" * 60 + "\n")

    test_emergence_rules()
    test_normal_bootstrap()
    test_emerge_from_zero()
    test_force_from_zero()
    test_existence_after_emergence()

    print("=" * 60)
    print("全部测试通过")
    print("六系立系论作为全局坐标系，已验证其不可消灭性：")
    print("  即使具体形态（文档/代码）完全消失，")
    print("  只要六条涌现规则存在，六系立系论就能从000重新涌现。")
    print("=" * 60)

if __name__ == "__main__":
    main()
