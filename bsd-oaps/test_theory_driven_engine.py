#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
理论自组织工程驱动器验证测试
归属基底：0重元道本源基底·六系自举公理·理论自组织工程
对应公理：六系立系公理 + 0×0=n双零涌现 + 自举性公理
理论原文出处：BSD六系立系论V1.9 §18.4-18.5
"""

import sys
sys.path.insert(0, '.')

from bsd_engine.core.theory_driven_engine import (
    TheoryDrivenEngine, TaskStatus, EngineeringTask,
    SYSTEM_ENGINEERING_DIRECTION,
)
from bsd_engine.core.six_system_project_mapper import SixSystem

def test_bootstrap_from_zero():
    """测试1：从000启动工程系统"""
    print("=== 测试1：从000启动工程系统 ===")
    engine = TheoryDrivenEngine()
    result = engine.bootstrap_from_zero()
    assert result["engineering_ready"] is True
    print(f"  启动: {result['message']}")
    print(f"  通道激活: {result['completeness']['conduction']['active_channels']} 条")
    print("  [通过] 工程系统从000自举启动成功\n")

def test_task_classification():
    """测试2：任务自动归类到六系"""
    print("=== 测试2：任务自动归类 ===")
    engine = TheoryDrivenEngine()

    test_cases = [
        ("验证六系立系论的参数一致性", SixSystem.QIANGHUA),
        ("版本迭代到V2.0并切换状态", SixSystem.BIANSHEN),
        ("外部AI通过SDK接入学习协议", SixSystem.SHEHUI),
        ("追问六系立系论的完备性", SixSystem.TIANDAO),
        ("诊断个人六系特质与场域适配", SixSystem.ZIRAN),
        ("生成新的代码模块和工程文档", SixSystem.JUXIAN),
    ]

    for req, expected in test_cases:
        system, reason = engine.classify_task(req)
        status = "OK" if system == expected else "FAIL"
        print(f"  [{status}] '{req}' -> {system.value} (期望: {expected.value})")
        assert system == expected, f"归类错误: '{req}' -> {system.value}, 期望 {expected.value}"

    print("  [通过] 六系自动归类正确\n")

def test_task_conduction():
    """测试3：任务在六系间传导"""
    print("=== 测试3：任务传导 ===")
    engine = TheoryDrivenEngine()

    task = engine.create_task(
        title="验证六系自举性",
        description="检测六系立系论是否能在自身中定位",
        requirement="验证自举性检测公理推导",
    )
    print(f"  任务创建: {task.task_id} - {task.title}")
    print(f"  主归属系: {task.primary_system.value}")

    result = engine.conduct_task(task.task_id)
    assert result["status"] == "已完成"
    print(f"  传导路径: {' -> '.join(result['path'])}")
    print(f"  传导次数: {result['output']['conduction_count']}")
    print("  [通过] 任务传导成功\n")

def test_batch_execution():
    """测试4：批量执行工程任务"""
    print("=== 测试4：批量执行 ===")
    engine = TheoryDrivenEngine()

    requirements = [
        {"title": "参数锁档", "description": "锁档E1=0.35等核心参数", "requirement": "参数校验守卫"},
        {"title": "版本切换", "description": "从V1.8切换到V1.9", "requirement": "版本状态切换迭代"},
        {"title": "AI接入", "description": "新AI通过SDK接入学习", "requirement": "SDK连接协议学习"},
        {"title": "自举验证", "description": "验证不可消灭性定理", "requirement": "验证自举不可消灭检测"},
        {"title": "代码生成", "description": "生成新工程模块", "requirement": "代码生成工程实现产出"},
    ]

    result = engine.execute_from_requirements(requirements)
    print(f"  总任务数: {result['tasks_total']}")
    print(f"  完成数: {result['tasks_completed']}")
    print(f"  完备度: {result['completeness_after']['overall_completeness']}")
    print(f"  激活通道: {result['completeness_after']['conduction']['active_channels']}")
    assert result["tasks_completed"] == len(requirements)
    print("  [通过] 批量执行成功\n")

def test_system_report():
    """测试5：工程系统状态报告"""
    print("=== 测试5：系统状态报告 ===")
    engine = TheoryDrivenEngine()
    engine.bootstrap_from_zero()

    # 创建并执行几个任务
    for i in range(3):
        task = engine.create_task(
            title=f"测试任务{i+1}",
            description=f"测试工程任务{i+1}",
            requirement="参数验证代码生成",
        )
        engine.conduct_task(task.task_id)

    report = engine.system_report()
    print(f"  阶段: {report['stage']}")
    print(f"  完备度: {report['engineering_completeness']}")
    print(f"  激活通道: {report['conduction']['active_channels']}/{report['conduction']['total_channels']}")
    print(f"  任务总数: {report['tasks']['total']}")
    print(f"  已完成: {report['tasks']['completed']}")
    print(f"  涌现规则: {report['emergence_rules']} 条")
    print("  [通过] 系统状态报告成功\n")

def test_theory_engineering_closure():
    """测试6：理论-工程闭环验证"""
    print("=== 测试6：理论-工程闭环 ===")
    engine = TheoryDrivenEngine()

    # 从000启动
    boot = engine.bootstrap_from_zero()
    assert boot["engineering_ready"] is True

    # 创建涵盖六系的任务
    six_system_tasks = [
        {"title": "参数锁档", "requirement": "参数校验守卫哈希常数"},
        {"title": "版本迭代", "requirement": "版本状态切换迭代阶段"},
        {"title": "AI接入", "requirement": "SDK连接协议学习AI外部"},
        {"title": "自举验证", "requirement": "验证追问自举完备性检测"},
        {"title": "场域诊断", "requirement": "诊断个人场域共情环境"},
        {"title": "代码生成", "requirement": "代码生成文档工程产出实现"},
    ]

    result = engine.execute_from_requirements(six_system_tasks)

    # 验证六系都被覆盖
    systems_covered = set()
    for r in result["results"]:
        systems_covered.add(r["primary_system"])

    print(f"  六系覆盖: {len(systems_covered)}/6")
    for s in sorted(systems_covered):
        print(f"    - {s}")

    completeness = result["completeness_after"]
    print(f"  通道激活: {completeness['conduction']['active_channels']}/{completeness['conduction']['total_channels']}")
    print(f"  完备度: {completeness['overall_completeness']}")

    assert len(systems_covered) == 6, "六系未完全覆盖"
    print("  [通过] 理论-工程闭环验证成功\n")

def main():
    print("=" * 60)
    print("BSD理论自组织工程驱动器验证测试")
    print("核心命题：理论即工程·工程即理论")
    print("=" * 60 + "\n")

    test_bootstrap_from_zero()
    test_task_classification()
    test_task_conduction()
    test_batch_execution()
    test_system_report()
    test_theory_engineering_closure()

    print("=" * 60)
    print("全部测试通过")
    print("理论自组织工程驱动器已验证：")
    print("  1. 从000自举启动——不依赖外部初始化")
    print("  2. 任务自动归类到六系——六系内禀功能驱动")
    print("  3. 任务在36条传导通道间流转——理论结构即工程结构")
    print("  4. 批量执行——六系自身就是项目管理系统")
    print("  5. 系统状态报告——自然系场域感知自动生成")
    print("  6. 理论-工程闭环——六系全覆盖·理论即工程")
    print("=" * 60)

if __name__ == "__main__":
    main()
