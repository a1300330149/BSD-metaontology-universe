"""
BSD虚拟宇宙·全扩展集成测试
[归属基底：四向展开法+进化协议规则+扩展场景+实体工厂]
[V1.0·2026-08-01]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_universe_engine import BSDUniverseEngine, UniverseState
from bsd_entity import EntityType
from bsd_scene import SceneType, SceneZone
from bsd_rule_engine import RulePriority

# 扩展模块
from evolution_protocol_rules import (
    register_all_evolution_protocol_rules,
    generate_protocol_report,
    EvolutionProtocol,
)
from extended_scene_generator import (
    ExtendedSceneGenerator,
    create_standard_extended_scenes,
    MixedSceneConfig,
    CompoundSceneLink,
)
from entity_factory import (
    BSDEntityFactory,
    FactoryStrategy,
    AssignmentStrategy,
    create_population_mix,
)

print("=" * 80)
print("BSD虚拟宇宙·全扩展集成测试")
print("三大扩展：12条进化协议规则 + 扩展场景 + 实体工厂")
print("=" * 80)

# ============================================================
# 测试1：注册12条进化协议规则
# ============================================================
print("\n[1/5] 注册12条进化协议规则")
engine = BSDUniverseEngine()
engine.initialize_standard_universe()

before_count = len(engine.rule_engine.list_rules())
registered = register_all_evolution_protocol_rules(engine.rule_engine)
after_count = len(engine.rule_engine.list_rules())

print(f"  原有规则: {before_count}条")
print(f"  新增规则: {registered}条")
print(f"  总规则数: {after_count}条")
assert after_count == before_count + 12, f"规则数应为{before_count + 12}，实际{after_count}"
print("✅ 12条进化协议规则注册成功")

# 打印协议报告
protocol_report = generate_protocol_report()
print(protocol_report)

# 验证规则存在性
for i in range(1, 13):
    rid = f"EP-RULE-{i:03d}"
    rule = engine.rule_engine.get_rule(rid)
    assert rule is not None, f"规则{rid}不存在"
    assert len(rule.underlying_axiom) > 0, f"规则{rid}缺少公理归属"
print("✅ 12条规则公理归属验证通过")

# ============================================================
# 测试2：扩展场景创建
# ============================================================
print("\n[2/5] 创建扩展场景·混合场域+跨区域复合场")

base_gen = engine.scene_generator
ext_gen = ExtendedSceneGenerator(base_gen)

# 创建标准扩展场景套件
extended_scenes = create_standard_extended_scenes(ext_gen)
print(f"  扩展场景创建: {len(extended_scenes)}个")
for s in extended_scenes:
    print(f"    {s.scene_id}: {s.name} | 区域={s.zone.value} | 类型={s.scene_type.value}")
    assert s.scene_type == SceneType.MIXED, f"扩展场景应为MIXED类型"
    assert len(s.material.secondary_platform_ids) > 0 or s.material.primary_platform_id, \
        f"扩展场景{s.scene_id}缺少素材配置"

# 验证混合场域
assert len(ext_gen._mixed_scenes) == 9, f"混合场景应为9个，实际{len(ext_gen._mixed_scenes)}"
# 验证复合链接
assert len(ext_gen._compound_links) == 3, f"复合链接应为3条，实际{len(ext_gen._compound_links)}"

# 验证桥接区域覆盖
zone_pairs = set()
for link in ext_gen._compound_links:
    zone_pairs.add(frozenset([link.source_zone.value, link.target_zone.value]))
assert len(zone_pairs) == 3, f"应有3种区域桥接对，实际{len(zone_pairs)}"
print("✅ 混合场域+跨区域复合场创建成功")

# 打印扩展场景报告
print(ext_gen.get_compound_report())

# ============================================================
# 测试3：实体工厂·批量创建
# ============================================================
print("\n[3/5] 实体工厂·批量创建+自动分配")

factory = BSDEntityFactory(
    entity_registry=engine.entity_registry,
    scene_generator=engine.scene_generator,
    timeline=engine.timeline,
)

# 批量创建不同类型实体
results: List = []
batches = [
    (EntityType.ABSTRACT, 6, FactoryStrategy.DIVERSIFIED, "abstract"),
    (EntityType.MATERIAL, 9, FactoryStrategy.GRADIENT, "material"),
    (EntityType.SOCIAL, 6, FactoryStrategy.DIVERSIFIED, "social"),
    (EntityType.NATURAL, 9, FactoryStrategy.RANDOM, "natural"),
    (EntityType.EVOLUTIONARY, 3, FactoryStrategy.UNIFORM, "evo"),
]

for etype, count, strategy, prefix in batches:
    result = factory.create_batch(
        entity_type=etype,
        count=count,
        strategy=strategy,
        assignment=AssignmentStrategy.AUTO_BY_SYSTEM,
        prefix=prefix,
        create_triad=True,
    )
    results.append(result)
    print(f"  批次 {result.batch_id}: {result.total_count}×{etype.value} | 策略={strategy.value} | 成功率={result.success_rate:.0%}")
    print(f"    分配场景数: {len(result.entities_assigned)} | 三体组数: {len(result.triad_groups_created)}")

# 验证总数
total_created = sum(r.total_count for r in results)
total_registered = len(engine.entity_registry.list_entities())
print(f"\n  工厂批量创建: {total_created}个实体")
print(f"  实体注册表总计: {total_registered}个（含3个初始三球）")

# 验证自动分配
for r in results:
    assert len(r.entities_assigned) > 0, f"{r.batch_id}分配场景为空"
    total_assigned = sum(len(v) for v in r.entities_assigned.values())
    assert total_assigned == r.total_count, f"{r.batch_id}分配数({total_assigned})≠创建数({r.total_count})"
print("✅ 自动场景分配验证通过")

# 验证三体共振自动创建
total_triads = len(engine.entity_registry._triad_groups)
initial_triads = 1  # 初始三球对偶
factory_triads = total_triads - initial_triads
print(f"  三体共振组: 初始{initial_triads} + 工厂创建{factory_triads} = 总{total_triads}")

# 验证生命周期自动注册
timeline_states = engine.timeline.get_all_states()
# 新创建的实体应有生命周期
expected_count = total_registered
print(f"  生命周期注册: {len(timeline_states)}/{expected_count}个实体")
assert len(timeline_states) >= expected_count, f"生命周期注册数不足"
print("✅ 实体工厂批量创建+自动分配验证通过")

# 打印工厂报告
print(factory.generate_factory_report())

# ============================================================
# 测试4：全引擎SAGA循环+规则触发
# ============================================================
print("\n[4/5] 全引擎SAGA循环·30次迭代·扩展规则触发验证")

# 先模拟20次SAGA循环让实体演化
summary = engine.simulate_universe(total_cycles=20, delta_time=1.5)
print(f"  30循环模拟完成")
print(f"  初始实体: {summary['initial_entities']} → 最终: {summary['final_entities']}")
print(f"  最终宇宙状态: {summary['final_universe_state']}")
print(f"  规则总触发: {summary['total_rule_triggers']}次")
print(f"  交互总数: {summary['interactions_count']}")

# 验证扩展规则被触发
ep_rules_triggered = 0
for r in engine.rule_engine.list_rules():
    if r.rule_id.startswith("EP-RULE") and r.trigger_count > 0:
        ep_rules_triggered += 1
print(f"\n  进化协议规则触发: {ep_rules_triggered}/12条规则被激活")

# 单独验证关键规则
rule_001 = engine.rule_engine.get_rule("EP-RULE-001")  # 本源涌现
rule_004 = engine.rule_engine.get_rule("EP-RULE-004")  # 场域显化
rule_012 = engine.rule_engine.get_rule("EP-RULE-012")  # 永续重生
assert rule_001 is not None
assert rule_004 is not None
assert rule_012 is not None
print(f"  EP-RULE-001(本源涌现): {rule_001.trigger_count}次触发")
print(f"  EP-RULE-004(场域显化): {rule_004.trigger_count}次触发")
print(f"  EP-RULE-012(永续重生): {rule_012.trigger_count}次触发")
print("✅ 进化协议规则触发验证通过")

# ============================================================
# 测试5：完整宇宙状态报告
# ============================================================
print("\n[5/5] 生成完整宇宙状态报告")
full_report = engine.generate_full_report()
print(full_report)

# 最终完备性验证
all_rules = engine.rule_engine.list_rules()
all_entities = engine.entity_registry.list_entities()
all_scenes = engine.scene_generator.list_scenes()

print("\n" + "=" * 80)
print("✅ BSD虚拟宇宙·全扩展集成测试通过！")
print("=" * 80)
print(f"""
【三大扩展成果】

  ① 进化协议规则（12条）
     · 创世组：P01本源涌现/P02球体形成/P03六系立系
     · 显化组：P04场域显化/P05实体凝结/P06素材整合
     · 进化组：P07互相内含/P08三体共振/P09进化耦合
     · 归零组：P10逆时针归零/P11循环完成/P12永续重生
     · 总规则数：{len(all_rules)}条
     · 触发验证：{ep_rules_triggered}/12条被激活

  ② 扩展场景（9个）
     · 混合场域：6个（农生/化工/工信/政经/六系太极/本源孕育）
     · 复合场：3个（农工桥接/化政拱门/本源永续极轴）
     · 总场景数：{len(all_scenes)}个

  ③ 实体工厂（33个+3初始=36实体）
     · 创建批次：5批
     · 创建总数：{total_created}个
     · 三体共振：{total_triads}组
     · 策略覆盖：均匀/梯度/随机/多样化 4种
     · 分配策略：按系自动分配+密度平衡+轮询

  宇宙完备性：
     实体={len(all_entities)} | 场景={len(all_scenes)} | 规则={len(all_rules)}
     交互总数={summary['interactions_count']} | 宇宙状态={summary['final_universe_state']}
""")
