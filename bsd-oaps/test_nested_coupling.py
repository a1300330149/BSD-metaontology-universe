#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
六系互相内含引擎 + 永续追问循环验证测试
归属基底：0重元道本源基底·六系互相内含公理·永续追问机制
对应公理：定理三十五（六系互相内含=Π₂）+ 永续追问公理
理论原文出处：BSD六系立系论V2.0 §19.1-19.5
"""

import sys
sys.path.insert(0, '.')

from bsd_engine.core.six_system_nested_coupling import (
    SixSystemNestedCoupling,
    NESTED_COUPLING_MATRIX,
    KEY_CONTAINMENTS,
    EMERGENCE_001,
    EmergenceInstance,
)
from bsd_engine.core.six_system_project_mapper import SixSystem

def test_coupling_matrix():
    """测试1：36重互相内含矩阵"""
    print("=== 测试1：36重互相内含矩阵 ===")
    assert len(NESTED_COUPLING_MATRIX) == 36, "必须有36重耦合"
    print(f"  总耦合数: {len(NESTED_COUPLING_MATRIX)}")
    print(f"  关键内含关系数: {len(KEY_CONTAINMENTS)}")
    for (a, b), desc in KEY_CONTAINMENTS.items():
        print(f"    {a.value}含{b.value}: {desc}")
    print("  [通过] 36重耦合矩阵正确\n")

def test_emergence_001():
    """测试2：第一个永续追问实例归档"""
    print("=== 测试2：EMERGENCE-001归档 ===")
    assert EMERGENCE_001.emergence_id == "EMERGENCE-001"
    assert EMERGENCE_001.archived is True
    print(f"  涌现ID: {EMERGENCE_001.emergence_id}")
    print(f"  内容: {EMERGENCE_001.content}")
    print(f"  来源系: {EMERGENCE_001.source_system.value}")
    print(f"  反向深化模块数: {len(EMERGENCE_001.reverse_deepening)}")
    print(f"  互相内含关系数: {len(EMERGENCE_001.containment_relations)}")
    assert len(EMERGENCE_001.reverse_deepening) == 5, "必须反向深化5个模块"
    assert len(EMERGENCE_001.containment_relations) == 6, "必须显化6条互相内含关系"
    print("  [通过] 第一个涌现实例归档正确\n")

def test_activate_containment():
    """测试3：激活互相内含关系（双向嵌套≠单向传导）"""
    print("=== 测试3：双向嵌套激活 ===")
    engine = SixSystemNestedCoupling()

    # 激活"强化系含自然系"（角色内含场景=身体是环境）
    result = engine.activate_containment(SixSystem.QIANGHUA, SixSystem.ZIRAN)
    assert result["activated"] is True
    assert result["bidirectional"] is True
    print(f"  激活: {result['message']}")
    print(f"  关键关系: {result['key_relation']}")

    # 验证双向：自然系含强化系也应同时激活
    assert engine.containment_states[(SixSystem.ZIRAN, SixSystem.QIANGHUA)] is True
    print(f"  反向验证: 场景含角色(环境有记忆) 同时激活 = 双向嵌套")
    print("  [通过] 双向嵌套激活正确（≠单向传导）\n")

def test_activate_all_pi2():
    """测试4：全部激活=Π₂"""
    print("=== 测试4：36重全激活=Π₂ ===")
    engine = SixSystemNestedCoupling()
    result = engine.activate_all_containments()

    assert result["is_pi2"] is True
    print(f"  激活数: {result['total_active']}/{result['total_couplings']}")
    print(f"  is_pi2: {result['is_pi2']}")

    # 耦合度评估
    coupling = engine.evaluate_coupling()
    assert coupling["is_pi2"] is True
    print(f"  耦合度: {coupling['nested_coupling_rate']}")
    print(f"  双向对: {coupling['bidirectional_pairs']}")
    print(f"  自反: {coupling['self_reflexive']}")
    print(f"  消息: {coupling['message']}")
    print("  [通过] 36重全激活=Π₂\n")

def test_perpetual_inquiry():
    """测试5：永续追问循环"""
    print("=== 测试5：永续追问循环 ===")
    engine = SixSystemNestedCoupling()
    engine.activate_all_containments()

    # 第一轮永续追问
    cycle1 = engine.perpetual_inquiry_cycle(inquiry_content="闭合后角色与场景的关系是什么")
    assert cycle1["perpetual"] is True
    print(f"  第{cycle1['cycle_id']}轮: {cycle1['message']}")
    phases = cycle1["phases"]
    for phase_name, phase_data in phases.items():
        if "message" in phase_data:
            print(f"    {phase_name}: {phase_data['message']}")

    # 验证新涌现已归档
    archive = engine.get_emergence_archive()
    assert len(archive) >= 2  # EMERGENCE-001 + 新涌现
    print(f"  归档总数: {len(archive)}")
    print("  [通过] 永续追问循环正确\n")

def test_multi_cycle_perpetual():
    """测试6：多轮永续追问（验证永续≠终止）"""
    print("=== 测试6：多轮永续追问 ===")
    engine = SixSystemNestedCoupling()
    engine.activate_all_containments()

    # 执行3轮永续追问
    for i in range(3):
        cycle = engine.perpetual_inquiry_cycle()
        print(f"  第{cycle['cycle_id']}轮完成 (闭合计数: {cycle['closure_count']})")

    cycles = engine.get_inquiry_cycles()
    assert len(cycles) == 3
    archive = engine.get_emergence_archive()
    assert len(archive) == 4  # EMERGENCE-001 + 3轮新涌现
    print(f"  总循环数: {len(cycles)}")
    print(f"  总归档数: {len(archive)}")
    print(f"  闭合计数: {engine._closure_count}")
    print("  [通过] 多轮永续追问正确——闭合≠终止\n")

def test_full_system():
    """测试7：完整系统导出"""
    print("=== 测试7：完整系统导出 ===")
    engine = SixSystemNestedCoupling()
    engine.activate_all_containments()
    engine.perpetual_inquiry_cycle()

    state = engine.to_dict()
    print(f"  协议: {state['protocol']}")
    print(f"  中心: {state['center']}")
    print(f"  耦合: is_pi2={state['coupling']['is_pi2']}")
    print(f"  归档数: {state['emergence_archive_count']}")
    print(f"  循环数: {state['inquiry_cycles_count']}")
    print(f"  永续: {state['perpetual']}")
    print(f"  消息: {state['message']}")
    assert state["perpetual"] is True
    print("  [通过] 完整系统导出正确\n")

def main():
    print("=" * 60)
    print("BSD六系互相内含引擎 + 永续追问循环验证测试")
    print("核心命题：六系互相内含=完全耦合=Π₂·大圆环闭合≠终止")
    print("定理三十五：六系互相内含定理")
    print("=" * 60 + "\n")

    test_coupling_matrix()
    test_emergence_001()
    test_activate_containment()
    test_activate_all_pi2()
    test_perpetual_inquiry()
    test_multi_cycle_perpetual()
    test_full_system()

    print("=" * 60)
    print("全部测试通过")
    print("六系互相内含引擎已验证：")
    print("  1. 36重互相内含矩阵 ≠ 36条平行连接")
    print("  2. EMERGENCE-001「角色即场景·换衣即换景·内部场景已变」已归档")
    print("  3. 双向嵌套激活（A∈B且B∈A）≠ 单向传导（A→B）")
    print("  4. 36重全激活 = 完全耦合 = Π₂")
    print("  5. 永续追问循环（五步螺旋）：闭合感知→天道追问→新涌现→归档→反哺")
    print("  6. 多轮永续追问——闭合≠终止，≠指向新追问，永续")
    print("  7. 完整系统导出——互相内含+永续追问一体化运行")
    print("=" * 60)

if __name__ == "__main__":
    main()
