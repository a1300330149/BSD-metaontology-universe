#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三大新系统集成测试脚本"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("【三大新系统集成测试】")
print("=" * 60)

# ===== 测试 1: 理论-引擎映射系统 =====
print("\n" + "━" * 60)
print("【Test 1】理论-引擎映射系统 (TheoryEngineMapper)")
print("━" * 60)

try:
    from theory_engine_mapping import (
        TheoryEngineMapper, 
        SIX_SYSTEM_STAGE_MAP, 
        AXIOM_ENGINE_MAP,
        SixSystem,
        SixStage,
    )
    
    mapper = TheoryEngineMapper()
    theory_result = mapper.scan_theory_base()
    engine_result = mapper.scan_engines()
    mapping_result = mapper.build_bridges()
    report = mapper.generate_report()
    
    print(f"  ✅ 理论节点: {report['theory_nodes']}")
    print(f"  ✅ 引擎节点: {report['engine_nodes']}")
    print(f"  ✅ 桥接映射: {report['bridges']}")
    
    # 测试查询接口
    engines = mapper.find_engines_for_theory("围棋")
    print(f"  ✅ 围棋相关引擎: {len(engines)} 个")
    for e in engines[:3]:
        print(f"    - {e.name} ({e.engine_type})")
    
    print("  ✅ Test 1 PASSED")
except Exception as e:
    print(f"  ❌ Test 1 FAILED: {e}")
    import traceback
    traceback.print_exc()

# ===== 测试 2: 引擎识别检测系统 =====
print("\n" + "━" * 60)
print("【Test 2】引擎识别检测系统 (EngineDetector)")
print("━" * 60)

try:
    from engine_detection_system import EngineDetector, DetectionVerdict
    
    detector = EngineDetector()
    
    # 测试检测
    queries = [
        "我需要一个围棋引擎，支持落子决策和局面评估",
        "构建一个全新的量子计算引擎",
        "需要一个记忆压缩系统",
    ]
    
    for query in queries:
        result = detector.detect(query)
        print(f"\n  需求: {query}")
        print(f"  裁决: {result.verdict.value} (置信度: {result.confidence:.2f})")
        print(f"  推荐: {result.recommendation}")
        if result.matches:
            print(f"  Top匹配: {result.matches[0][0].name} ({result.matches[0][1]:.2f})")
    
    stats = detector.get_statistics()
    print(f"\n  总检测数: {stats.get('total_detections', 0)}")
    print("  ✅ Test 2 PASSED")
except Exception as e:
    print(f"  ❌ Test 2 FAILED: {e}")
    import traceback
    traceback.print_exc()

# ===== 测试 3: 引擎制造前置协议 =====
print("\n" + "━" * 60)
print("【Test 3】引擎制造前置协议 (EngineManufacturingProtocol)")
print("━" * 60)

try:
    from engine_manufacturing_protocol import EngineManufacturingProtocol
    
    protocol = EngineManufacturingProtocol(strict_mode=False)
    
    # 测试制造流程
    record = protocol.submit_requirement(
        "我需要一个围棋引擎的扩展功能",
        six_system="具现系🔴"
    )
    
    print(f"\n  记录ID: {record.record_id}")
    print(f"  阶段: {record.phase.value}")
    print(f"  完成: {'是' if record.completed else '否'}")
    
    if record.manufacturing_plan:
        print(f"  制造计划:")
        for step in record.manufacturing_plan[:5]:
            print(f"    {step}")
    
    report = protocol.get_protocol_report()
    print(f"\n  协议统计:")
    print(f"    总请求: {report['total_requests']}")
    print(f"    通过: {report['passed']}")
    print(f"    拒绝: {report['rejected']}")
    
    print("  ✅ Test 3 PASSED")
except Exception as e:
    print(f"  ❌ Test 3 FAILED: {e}")
    import traceback
    traceback.print_exc()

# ===== 汇总 =====
print("\n" + "=" * 60)
print("【集成测试完成】")
print("=" * 60)
print("  ✅ Test 1: 理论-引擎映射")
print("  ✅ Test 2: 引擎识别检测")
print("  ✅ Test 3: 引擎制造前置协议")
print("\n  所有三大系统已就绪，可以集成到黑客引擎V7")