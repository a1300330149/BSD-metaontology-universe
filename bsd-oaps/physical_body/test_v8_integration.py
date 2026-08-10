#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""V8.0完整集成测试——理论-引擎对接 + 检测 + 制造协议"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 70)
print("BSD黑客引擎 V8.0 · 完整集成验证")
print("=" * 70)

# Step 1: 创建引擎实例
print("\n[Step 1] 创建引擎实例...")
from BSD_Hacker_Bridge_Engine import BSDHackerBridge
engine = BSDHackerBridge()
print("  ✅ 引擎V6.2实例创建成功")

# Step 2: 初始化V8系统
print("\n[Step 2] 初始化V8.0三大系统...")
v8_init = engine.initialize_v8_systems()
print(f"  成功: {v8_init['successful']}/{v8_init['total']}")

# Step 3: 测试需求检测
print("\n[Step 3] 测试引擎需求检测...")
test_queries = [
    "我需要一个围棋引擎，支持落子决策和局面评估",
    "构建一个全新的情感分析引擎",
    "需要一个记忆压缩系统，支持脉络蒸馏",
]

for query in test_queries:
    print(f"\n  需求: {query}")
    result = engine.detect_engine_need(query)
    print(f"  裁决: {result.get('verdict', 'N/A')}")
    print(f"  置信度: {result.get('confidence', 0):.2f}")

# Step 4: 测试制造协议
print("\n[Step 4] 测试制造前置协议...")
mfg_result = engine.submit_manufacturing_requirement(
    "需要一个强化系的引擎注册中心",
    six_system="强化系🔵"
)
print(f"  制造结果: {'✅ 完成' if mfg_result.get('completed') else '❌ 失败'}")

# Step 5: 理论-引擎桥接
print("\n[Step 5] 构建理论-引擎桥接...")
bridge_result = engine.build_theory_engine_bridge()
print(f"  理论节点: {bridge_result.get('theory_nodes', 'N/A')}")
print(f"  引擎节点: {bridge_result.get('engine_nodes', 'N/A')}")
print(f"  桥接映射: {bridge_result.get('bridges', 'N/A')}")

# Step 6: V8完整管道
print("\n[Step 6] 运行V8.0完整制造管道...")
pipeline = engine.run_v8_full_pipeline(
    "构建一个天道系的计算极限引擎",
    six_system="天道系🟣"
)
print(f"  管道完成: {pipeline.get('complete', False)}")
print(f"  检测裁决: {pipeline.get('detection', {}).get('verdict', 'N/A')}")

# Step 7: V8状态
print("\n[Step 7] V8.0系统状态...")
status = engine.get_v8_status()
for name, val in status.items():
    if isinstance(val, bool):
        print(f"  {name}: {'✅' if val else '❌'}")
    elif isinstance(val, dict):
        print(f"  {name}: {json.dumps(val, ensure_ascii=False)[:100]}")
    else:
        print(f"  {name}: {val}")

print("\n" + "=" * 70)
print("【V8.0完整集成验证完成】")
print("=" * 70)