"""
BSD引擎→Updream对接桥·集成测试
[V1.0·2026-08-01]
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bsd_universe_engine import BSDUniverseEngine
from bsd_entity import EntityType
from bsd_updream_bridge import (
    BSDUpdreamBridge,
    UpdreamTaskType,
    UpdreamWorkflow,
    create_updream_workflow_from_engine,
)

print("=" * 80)
print("BSD引擎→Updream智能体对接桥·集成测试")
print("=" * 80)

# ============================================================
# 测试1：初始化引擎并运行SAGA循环
# ============================================================
print("\n[1/4] 初始化BSD宇宙引擎·运行20次SAGA循环")
engine = BSDUniverseEngine()
engine.initialize_standard_universe()

# 添加一些实体以丰富宇宙状态
engine.create_custom_entity(
    entity_id="test_character_01",
    name="测试角色-01",
    entity_type=EntityType.MATERIAL,
)
engine.create_custom_entity(
    entity_id="test_scene_01",
    name="测试场景-01",
    entity_type=EntityType.NATURAL,
)

# 运行SAGA循环
engine.simulate_universe(total_cycles=20, delta_time=1.5)
print(f"  SAGA循环: {engine.saga_cycle_count}次")
print(f"  实体数: {len(engine.entity_registry.list_entities())}个")
print(f"  场景数: {len(engine.scene_generator.list_scenes())}个")
print(f"  规则数: {len(engine.rule_engine.list_rules())}条")
print("✅ 宇宙初始化完成")

# ============================================================
# 测试2：创建对接桥·生成Updream工作流
# ============================================================
print("\n[2/4] 创建对接桥·生成Updream工作流")

bridge, workflow = create_updream_workflow_from_engine(
    engine,
    workflow_name="Updream标准工作流",
    cycles_to_analyze=10,
)

print(f"  工作流ID: {workflow.workflow_id}")
print(f"  工作流名称: {workflow.name}")
print(f"  任务数: {len(workflow.tasks)}个")
print(f"  初始阶段: {workflow.current_phase}")

# 验证任务生成
task_types_count = {}
for task in workflow.tasks:
    tt = task.task_type.value
    task_types_count[tt] = task_types_count.get(tt, 0) + 1

print("\n  【任务类型分布】")
for tt, cnt in sorted(task_types_count.items(), key=lambda x: -x[1]):
    print(f"    {tt}: {cnt}个")

# 验证任务属性
for task in workflow.tasks:
    assert task.task_id, f"任务{task.task_id}缺少ID"
    assert task.title, f"任务{task.task_id}缺少标题"
    assert 1 <= task.priority <= 10, f"任务{task.task_id}优先级越界: {task.priority}"
    assert task.estimated_duration >= 0, f"任务{task.task_id}时长为负"
print("✅ 工作流任务验证通过")

# ============================================================
# 测试3：推进工作流阶段
# ============================================================
print("\n[3/4] 推进工作流阶段·模拟SAGA循环")

# 设置回调
completed_tasks = []
def on_task_completed(task):
    completed_tasks.append(task.task_id)

bridge.set_callbacks(on_workflow_completed=lambda wf: print(f"  🎉 工作流{wf.workflow_id}完成！"))

# 推进5个阶段
phases = ["sensing", "analyzing", "generating", "acting", "completed"]
for phase in phases:
    wf = bridge.advance_workflow_phase(workflow.workflow_id)
    if wf:
        print(f"  → {phase}·进度={wf.progress:.0f}%")

# 验证完成
assert workflow.current_phase == "completed", f"工作流未完成: {workflow.current_phase}"
print("✅ 工作流阶段推进验证通过")

# ============================================================
# 测试4：完整对接桥报告
# ============================================================
print("\n[4/4] 生成完整对接桥报告")
report = bridge.get_bridge_report()
print(report)

# 验证报告内容
assert "对接工作流" in report
assert "对接日志" in report
assert "引擎状态" in report
print("✅ 对接桥报告验证通过")

print("\n" + "=" * 80)
print("✅ BSD引擎→Updream智能体对接桥·集成测试通过！")
print("=" * 80)
print(f"""
【对接成果总览】

  ① 对接桥核心能力
     · SAGA循环 → Updream工作流映射
     · 实体化 → 角色/道具对象池
     · 场景化 → 场景/环境配置
     · 时间化 → 剧情时间线/节奏控制
     · 规则化 → 创作规则/约束条件
     · 双时针 → 创作节奏控制

  ② 六系→Updream创作域映射
     · 强化系 → 角色塑造（Character）
     · 自然系 → 环境氛围（Environment）
     · 具现系 → 道具造物（Prop）
     · 变身系 → 形态变化（Transform）
     · 社会系 → 社交互动（Social）
     · 天道系 → 美学风格（Aesthetic）

  ③ 任务类型映射（9种）
     · 角色设计/场景设计/道具设计
     · 分镜/动画/对话/音效/调色/后期

  ④ 工作流阶段（5阶段）
     · Sensing（感知）→ 需求分析/素材收集
     · Analyzing（分析）→ 创意构思/结构规划
     · Generating（生成）→ 内容创作/产品产出
     · Acting（行动）→ 部署发布/迭代优化
     · Completed（完成）→ 归档总结

  宇宙→创作完整链路：
     BSD宇宙引擎（实体/场景/规则/时间）
         ↓ SAGA循环
     BSDUpdreamBridge（映射/生成/调度）
         ↓ 任务列表
     Updream智能体（创作执行）
""")
