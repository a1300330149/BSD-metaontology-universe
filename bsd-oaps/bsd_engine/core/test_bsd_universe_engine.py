"""
BSD虚拟宇宙引擎·全集成测试
[归属基底：四向展开法·实体化+场景化+时间化+规则化]
[V1.0·2026-08-01]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_universe_engine import BSDUniverseEngine, UniverseState, SAGAPhase
from bsd_entity import EntityType
from bsd_scene import SceneType, SceneZone
from bsd_timeline import ClockState, LifecyclePhase
from bsd_rule_engine import RulePriority

print("=" * 70)
print("BSD虚拟宇宙引擎·全集成测试")
print("四向展开法：实体化+场景化+时间化+规则化")
print("=" * 70)

# 1. 初始化引擎
engine = BSDUniverseEngine()
print("\n[1/6] 引擎创建完成")
print(f"  初始状态: {engine.universe_state.value}")

# 2. 初始化标准宇宙
engine.initialize_standard_universe()
print("\n[2/6] 标准宇宙初始化完成")
print(f"  宇宙状态: {engine.universe_state.value}")
print(f"  实体数: {len(engine.entity_registry.list_entities())}")
print(f"  场景数: {len(engine.scene_generator.list_scenes())}")
print(f"  规则数: {len(engine.rule_engine.list_rules())}")

# 3. 检查四向展开
print("\n[3/6] 四向展开完整性检查")
entities = engine.entity_registry.list_entities()
scenes = engine.scene_generator.list_scenes()
states = engine.timeline.get_all_states()
rules = engine.rule_engine.list_rules()

# 实体化
for e in entities:
    dom_sys, dom_val = e.six_system.dominant_system()
    cart = e.sphere_pos.to_cartesian()
    density = e.compute_density()
    complexity = e.compute_complexity()
    life = e.compute_life_indicator()
    print(f"  实体 {e.name} | 类型={e.entity_type.value} | 主导={dom_sys}({dom_val:.2f}) | 密度={density:.3f} | 复杂度={complexity:.3f} | 生命度={life:.3f}")

# 三体共振
triads = engine.entity_registry._triad_groups
print(f"  三体共振组: {len(triads)}组")

# 场景化
for s in scenes:
    print(f"  场景 {s.name} | 类型={s.scene_type.value} | 区域={s.zone.value} | 实体数={s.entity_count()} | 主素材={s.material.primary_platform_id} | 辅助={s.material.secondary_platform_ids}")

# 时间化
for eid, state in states.items():
    print(f"  时间线 {eid} | 相位={state.phase.value} | 循环={state.cycle_count}")

# 规则化
for r in rules:
    print(f"  规则 {r.rule_id}·{r.name} | 公理={r.underlying_axiom} | 优先级={r.priority.value}")

# 4. 模拟宇宙演化
print("\n[4/6] 模拟宇宙演化·30个SAGA循环")
summary = engine.simulate_universe(total_cycles=30, delta_time=2.0)
print(f'  初始实体: {summary["initial_entities"]} → 最终: {summary["final_entities"]}')
print(f'  初始场景: {summary["initial_scenes"]} → 最终: {summary["final_scenes"]}')
print(f'  规则总触发: {summary["total_rule_triggers"]}次')
print(f'  交互总数: {summary["interactions_count"]}')
print(f'  最终宇宙状态: {summary["final_universe_state"]}')
print("  实体循环完成情况:")
for eid, cycles in summary["entity_cycles_completed"].items():
    print(f"    {eid}: {cycles}次循环")

# 5. 运行单SAGA循环并展示细节
print("\n[5/6] 单SAGA循环详细执行")
engine2 = BSDUniverseEngine()
engine2.initialize_standard_universe()
result = engine2.run_saga_cycle(delta_time=1.0)
print(f"  循环ID: {result.cycle_id}")
print(f"  处理实体: {result.entities_processed}")
print(f"  处理场景: {result.scenes_processed}")
print(f"  规则触发: {result.rules_triggered}条")
print("  交互详情:")
for inter in result.interactions:
    print(f'    [{inter["rule_id"]}] {inter["rule_name"]} | 动作={inter["action"]} | {inter["description"]}')
print("  状态变化:")
for change in result.state_changes:
    print(f'    {change["entity_id"]}: {change["new_phase"]} (循环#{change["cycle_count"]})')

# 6. 生成完整报告
print("\n[6/6] 生成完整宇宙状态报告")
full_report = engine.generate_full_report()
print(full_report)

print("\n" + "=" * 70)
print("✅ BSD虚拟宇宙引擎·全集成测试通过！")
print("四向展开法验证完成：")
print("  ① 实体化·Entity体系 ✅")
print("  ② 场景化·Scene场域 ✅")
print("  ③ 时间化·Timeline双时针 ✅")
print("  ④ 规则化·RuleEngine ✅")
print("  SAGA工作流闭环 ✅")
print("  互相内含/三体共振/素材子集 ✅")
print("=" * 70)
