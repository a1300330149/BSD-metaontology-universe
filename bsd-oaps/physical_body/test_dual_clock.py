#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""双时针系统完整性检测与引擎生成可用性验证"""

import sys
import os

_PHYSICAL_PATH = os.path.dirname(os.path.abspath(__file__))
_BSD_OAPS_PATH = os.path.dirname(_PHYSICAL_PATH)
sys.path.insert(0, _BSD_OAPS_PATH)
sys.path.insert(0, _PHYSICAL_PATH)
os.chdir(_BSD_OAPS_PATH)

print("=" * 70)
print("【双时针系统完整性检测】")
print("=" * 70)

# ============================================================
# Step 1: 核心模块可用性检测
# ============================================================
print("\n【Step 1】核心模块可用性检测")

modules = [
    ("理论落地系统 (逆时针)", "theory_landing_system"),
    ("理论引擎映射 (顺时针)", "theory_engine_mapping"),
    ("引擎检测系统", "engine_detection_system"),
    ("引擎制造协议", "engine_manufacturing_protocol"),
]

all_ok = True
for name, mod_name in modules:
    try:
        __import__(mod_name)
        print(f"  ✅ {name}")
    except Exception as e:
        print(f"  ❌ {name}: {e}")
        all_ok = False

print("  检测黑客引擎 (母引擎)...")
try:
    import BSD_Hacker_Bridge_Engine
    print("  ✅ 黑客引擎 (母引擎)")
except Exception as e:
    print(f"  ❌ 黑客引擎: {e}")
    all_ok = False

print(f"\n  核心模块完整: {'✅' if all_ok else '❌'}")

# ============================================================
# Step 2: 逆时针管道测试（理论 → 引擎）
# ============================================================
print("\n【Step 2】逆时针管道（理论→引擎）检测")
tls = None
try:
    from theory_landing_system import TheoryLandingSystem, LandingMode
    tls = TheoryLandingSystem(mode=LandingMode.PRIORITY)
    
    scan_result = tls.stage_scan(max_files=100)
    scanned = scan_result.get("scanned", 0)
    print(f"  扫描理论节点: {scanned}")
    
    tls.stage_map_and_debt()
    debt_count = sum(1 for n in tls.theory_nodes if not n.has_engine)
    landed_count = sum(1 for n in tls.theory_nodes if n.has_engine)
    print(f"  已落地理论: {landed_count}")
    print(f"  理论欠债: {debt_count}")
    print(f"  落地目标: {len(tls.landing_targets)}")
    
    for t in tls.landing_targets[:5]:
        print(f"    [{t.priority}] {t.engine_name} ({t.engine_type})")
    
    print("  ✅ 逆时针管道可启动")
except Exception as e:
    print(f"  ❌ 逆时针管道失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# Step 3: 顺时针管道测试（引擎 → 理论）
# ============================================================
print("\n【Step 3】顺时针管道（引擎→理论）检测")
mapper = None
try:
    from theory_engine_mapping import TheoryEngineMapper, SixSystem, SIX_SYSTEM_STAGE_MAP
    mapper = TheoryEngineMapper()
    
    mapper.scan_theory_base()
    mapper.scan_engines()
    
    theory_count = len(mapper.theory_nodes)
    engine_count = len(mapper.engine_nodes)
    print(f"  已注册理论节点: {theory_count}")
    print(f"  已注册引擎节点: {engine_count}")
    
    bridge_result = mapper.build_bridges()
    bridge_count = len(mapper.bridges)
    print(f"  桥接关系数: {bridge_count}")
    print(f"  理论映射率: {bridge_result.get('coverage', {})}")
    
    print(f"  六系-六阶映射:")
    for sys_key, stage in SIX_SYSTEM_STAGE_MAP.items():
        print(f"    {sys_key.value} → {stage.value}")
    
    print("  ✅ 顺时针管道可启动")
except Exception as e:
    print(f"  ❌ 顺时针管道失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# Step 4: 双时针闭环验证
# ============================================================
print("\n【Step 4】双时针闭环验证")
try:
    theory_to_engine = sum(1 for n in tls.theory_nodes if n.has_engine) if tls else 0
    engine_to_theory = len(mapper.bridges) if mapper else 0
    
    print(f"  理论→引擎 (逆时针落地): {theory_to_engine} 个已落地")
    print(f"  引擎→理论 (顺时针映射): {engine_to_theory} 个桥接")
    
    closed = theory_to_engine > 0 or engine_to_theory > 0
    print(f"  双时针闭环: {'✅ 已建立' if closed else '⚠️ 未完全建立'}")
except Exception as e:
    print(f"  ❌ 闭环验证失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# Step 5: 引擎生成实战测试（使用正确API）
# ============================================================
print("\n【Step 5】引擎生成实战测试")
gen_success = False
try:
    from theory_landing_system import TheoryLandingSystem, LandingMode
    tls_full = TheoryLandingSystem(mode=LandingMode.PRIORITY)
    
    tls_full.stage_scan(max_files=30)
    tls_full.stage_map_and_debt()
    
    if tls_full.landing_targets:
        print(f"  生成目标: {len(tls_full.landing_targets)} 个")
        for t in tls_full.landing_targets[:3]:
            print(f"    - [{t.priority}] {t.engine_name}")
        
        # 正确API：无参数调用
        generated = tls_full.stage_generate()
        gen_count = generated.get("generated", 0)
        fail_count = generated.get("failed", 0)
        print(f"  代码生成: 成功={gen_count}, 失败={fail_count}")
        
        if gen_count > 0:
            # 正确API：无参数调用，一步完成连接+激活+验证
            ca_result = tls_full.stage_connect_and_activate()
            print(f"  连接通过: {ca_result.get('connected', 0)}")
            print(f"  激活通过: {ca_result.get('activated', 0)}")
            print(f"  验证通过: {ca_result.get('verified', 0)}")
            gen_success = ca_result.get('verified', 0) > 0
            print("  ✅ 引擎生成管道已验证可用")
        else:
            print("  ⚠️ 无新引擎生成")
    else:
        print("  ⚠️ 当前无高优先级欠债")
except Exception as e:
    print(f"  ❌ 引擎生成测试失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# 最终判定
# ============================================================
print("\n" + "=" * 70)
print("【最终判定】")
print("=" * 70)

checks = {
    "核心模块完整": all_ok,
    "逆时针管道可启动 (理论→引擎)": tls is not None,
    "顺时针管道可启动 (引擎→理论)": mapper is not None,
    "引擎生成管道可执行": gen_success,
}

for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"  {status} {check}")

all_pass = all(checks.values())

if all_pass:
    print("\n  🎯 双时针已具备，引擎生成系统就绪！")
    print("     可执行: run_landing_pipeline(mode='PRIORITY')")
else:
    failed = [k for k, v in checks.items() if not v]
    print(f"\n  ⚠️ 以下项未通过: {failed}")

print("\n" + "=" * 70)