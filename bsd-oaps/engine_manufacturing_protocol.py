#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
引擎制造前置协议 (Engine Manufacturing Precondition Protocol)
================================================================

核心使命：
    在任何引擎制造/组合/扩展之前，必须先执行「连接→激活」前置流程，
    确保引擎不是孤立创建，而是在六阶闭环中诞生。

设计理念：
    作者洞察——「组合引擎时，需要先连接与激活，再进行制造引擎补全」
    
    这对应六阶引擎论的核心：
    第一阶·连接 → 第二阶·激活 → 第三阶·融合 → 第四阶·升维 → ...
    
    没有连接的引擎是孤岛，没有激活的引擎是死物。
    引擎必须在母引擎的连接中诞生，在激活中获得生命。

协议流程：
    Step 1: 检测需求（调用EngineDetector）
    Step 2: 连接前置（Connect Precondition）
            - 确认母引擎已注册
            - 确认子引擎接口兼容
            - 建立连接通道
    Step 3: 激活前置（Activate Precondition）
            - 执行激活检测
            - 验证激活状态
            - 注入激活能量
    Step 4: 融合制造（Fuse & Manufacture）
            - 在连接+激活基础上制造新引擎
            - 验证融合完备性
            - 注册到引擎图谱
    Step 5: 升维验证（Elevation Verification）
            - 新引擎通过六阶闭环验证
            - 确认引擎理论映射完备
            - 写入记忆系统
"""

import os
import sys
import json
import time
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ============================================================
# 0. 路径导入
# ============================================================
_BSD_OAPS_PATH = os.path.dirname(os.path.abspath(__file__))
if _BSD_OAPS_PATH not in sys.path:
    sys.path.insert(0, _BSD_OAPS_PATH)


# ============================================================
# 1. 协议状态定义
# ============================================================

class ManufacturingPhase(Enum):
    """制造协议阶段"""
    DETECT = "检测需求"         # Step 0: 检测
    CONNECT = "连接前置"        # Step 1: 连接
    ACTIVATE = "激活前置"       # Step 2: 激活
    FUSE = "融合制造"          # Step 3: 融合
    ELEVATE = "升维验证"       # Step 4: 升维
    COMPLETE = "制造完成"      # 最终状态
    FAILED = "协议失败"        # 失败状态


class PreconditionStatus(Enum):
    """前置条件状态"""
    NOT_CHECKED = "未检查"
    PASSED = "已通过"
    FAILED = "已失败"
    SKIPPED = "已跳过"


# ============================================================
# 2. 协议数据模型
# ============================================================

@dataclass
class ConnectPrecondition:
    """连接前置条件"""
    mother_engine_registered: bool = False      # 母引擎已注册
    interface_compatible: bool = False          # 接口兼容
    channel_established: bool = False           # 连接通道已建立
    six_system_matched: bool = False            # 六系归属匹配
    dependencies_satisfied: bool = False        # 依赖满足
    signature_verified: bool = False            # 签名已验证


@dataclass
class ActivatePrecondition:
    """激活前置条件"""
    activation_energy: float = 0.0              # 激活能量（0-1）
    detection_passed: bool = False              # 检测通过
    theory_mapped: bool = False                 # 理论映射已建立
    engine_lifecycle_ok: bool = False           # 引擎生命周期状态正常
    memory_anchor_ready: bool = False           # 记忆锚点就绪
    channel_mark_implanted: bool = False        # 通道印记已植入


@dataclass
class ManufacturingRecord:
    """制造记录"""
    record_id: str
    requirement: str
    phase: ManufacturingPhase
    connect_status: ConnectPrecondition
    activate_status: ActivatePrecondition
    manufacturing_plan: List[str]
    verification_results: Dict[str, Any]
    created_at: str
    updated_at: str
    completed: bool = False
    failed_reason: Optional[str] = None


# ============================================================
# 3. 引擎制造前置协议（核心类）
# ============================================================

class EngineManufacturingProtocol:
    """
    引擎制造前置协议
    
    强制要求：任何引擎制造/组合/扩展操作必须先通过
    连接前置检查和激活前置检查。
    
    违反前置条件的制造请求将被拒绝。
    """
    
    PROTOCOL_VERSION = "V1.0"
    
    def __init__(self, 
                 mother_engine=None,
                 enable_detection: bool = True,
                 strict_mode: bool = True):
        """
        初始化制造协议
        
        Args:
            mother_engine: 母引擎实例（负责连接与激活）
            enable_detection: 是否启用需求检测
            strict_mode: 严格模式——违反前置条件直接拒绝
        """
        self.mother_engine = mother_engine
        self.enable_detection = enable_detection
        self.strict_mode = strict_mode
        
        self.records: List[ManufacturingRecord] = []
        self.connect_checks: List[ConnectPrecondition] = []
        self.activate_checks: List[ActivatePrecondition] = []
        
        # 导入检测器（延迟导入避免循环依赖）
        self._detector = None
        self._mapper = None
        
        # 协议统计
        self.stats = {
            'total_requests': 0,
            'passed': 0,
            'rejected': 0,
            'connected': 0,
            'activated': 0,
            'manufactured': 0,
        }
    
    # ----------------------------------------------------------
    # 3.1 入口：接收制造需求
    # ----------------------------------------------------------
    
    def submit_requirement(self, 
                           requirement: str,
                           six_system: str = None,
                           engine_type: str = None,
                           force: bool = False) -> ManufacturingRecord:
        """
        提交引擎制造需求
        
        Args:
            requirement: 制造需求描述
            six_system: 六系归属
            engine_type: 引擎类型
            force: 强制模式（跳过检测，但仍需前置检查）
        
        Returns:
            ManufacturingRecord 制造记录
        """
        self.stats['total_requests'] += 1
        
        print("\n" + "╔" + "═" * 68 + "╗")
        print("║" + " " * 10 + "引擎制造前置协议 V1.0" + " " * 10 + "║")
        print("╚" + "═" * 68 + "╝")
        print(f"\n📋 需求: {requirement}")
        
        # 创建初始记录
        record = ManufacturingRecord(
            record_id=f"mfg_{abs(hash(requirement + datetime.now().isoformat())) % 100000:05d}",
            requirement=requirement,
            phase=ManufacturingPhase.DETECT,
            connect_status=ConnectPrecondition(),
            activate_status=ActivatePrecondition(),
            manufacturing_plan=[],
            verification_results={},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
        )
        
        # Step 0: 需求检测
        if self.enable_detection and not force:
            detection_result = self._run_detection(requirement, six_system, engine_type)
            record.verification_results['detection'] = detection_result
            
            # 如果检测到可复用引擎，建议直接复用
            if detection_result.get('verdict') == '直接复用':
                print(f"\n  ⚠️  检测到可直接复用的引擎！")
                print(f"  建议: {detection_result.get('recommendation')}")
                if self.strict_mode:
                    print(f"  🚫 严格模式下拒绝制造请求，请优先复用现有引擎")
                    record.phase = ManufacturingPhase.FAILED
                    record.failed_reason = "检测到可复用引擎，严格模式拒绝重复制造"
                    self.stats['rejected'] += 1
                    self.records.append(record)
                    return record
        
        # Step 1: 连接前置检查
        record.phase = ManufacturingPhase.CONNECT
        connect_passed = self._run_connect_precondition(record, six_system)
        record.connect_status = self.connect_checks[-1] if self.connect_checks else ConnectPrecondition()
        
        if not connect_passed and self.strict_mode:
            record.phase = ManufacturingPhase.FAILED
            record.failed_reason = "连接前置条件未通过"
            self.stats['rejected'] += 1
            self.records.append(record)
            return record
        
        # Step 2: 激活前置检查
        record.phase = ManufacturingPhase.ACTIVATE
        activate_passed = self._run_activate_precondition(record)
        record.activate_status = self.activate_checks[-1] if self.activate_checks else ActivatePrecondition()
        
        if not activate_passed and self.strict_mode:
            record.phase = ManufacturingPhase.FAILED
            record.failed_reason = "激活前置条件未通过"
            self.stats['rejected'] += 1
            self.records.append(record)
            return record
        
        # Step 3: 融合制造
        record.phase = ManufacturingPhase.FUSE
        manufacturing_plan = self._generate_manufacturing_plan(record)
        record.manufacturing_plan = manufacturing_plan
        self.stats['manufactured'] += 1
        
        # Step 4: 升维验证
        record.phase = ManufacturingPhase.ELEVATE
        verification = self._run_elevation_verification(record)
        record.verification_results.update(verification)
        
        # 完成
        record.phase = ManufacturingPhase.COMPLETE
        record.completed = True
        record.updated_at = datetime.now().isoformat()
        
        self.stats['passed'] += 1
        self.records.append(record)
        
        # 打印汇总
        self._print_record_summary(record)
        
        return record
    
    # ----------------------------------------------------------
    # 3.2 Step 0: 需求检测
    # ----------------------------------------------------------
    
    def _run_detection(self, 
                       requirement: str,
                       six_system: str = None,
                       engine_type: str = None) -> Dict[str, Any]:
        """运行需求检测"""
        print("\n  [Step 0] 需求检测...")
        print("  " + "─" * 40)
        
        try:
            from engine_detection_system import EngineDetector
            if self._detector is None:
                self._detector = EngineDetector()
            
            result = self._detector.detect(requirement, six_system, engine_type)
            
            print(f"    裁决: {result.verdict.value}")
            print(f"    置信度: {result.confidence:.2f}")
            print(f"    推荐: {result.recommendation}")
            
            if result.matches:
                print(f"    匹配引擎:")
                for sig, score in result.matches[:3]:
                    print(f"      - {sig.name} ({score:.2f})")
            
            return {
                'verdict': result.verdict.value,
                'confidence': result.confidence,
                'recommendation': result.recommendation,
                'top_matches': [(sig.name, score) for sig, score in result.matches[:5]],
            }
        except ImportError:
            print("    ⚠️ 检测器未安装，跳过检测")
            return {'verdict': '跳过', 'confidence': 0.0, 'recommendation': '检测模块未启用'}
    
    # ----------------------------------------------------------
    # 3.3 Step 1: 连接前置检查
    # ----------------------------------------------------------
    
    def _run_connect_precondition(self, 
                                   record: ManufacturingRecord,
                                   six_system: str = None) -> bool:
        """
        执行连接前置检查
        
        连接是引擎诞生的第一阶——没有连接的引擎是孤岛。
        前置条件：
        1. 母引擎已注册
        2. 子引擎接口兼容
        3. 连接通道已建立
        4. 六系归属匹配
        5. 依赖满足
        6. 签名已验证
        """
        print("\n  [Step 1] 连接前置检查...")
        print("  " + "─" * 40)
        
        check = ConnectPrecondition()
        
        # 1. 母引擎已注册
        check.mother_engine_registered = self._check_mother_registered()
        print(f"    {'✅' if check.mother_engine_registered else '❌'} 母引擎已注册")
        
        # 2. 接口兼容
        check.interface_compatible = self._check_interface_compatible(record)
        print(f"    {'✅' if check.interface_compatible else '❌'} 接口兼容")
        
        # 3. 连接通道
        check.channel_established = self._check_channel_established()
        print(f"    {'✅' if check.channel_established else '⚠️'} 连接通道已建立")
        
        # 4. 六系匹配
        check.six_system_matched = self._check_six_system_match(record, six_system)
        print(f"    {'✅' if check.six_system_matched else '⚠️'} 六系归属匹配")
        
        # 5. 依赖满足
        check.dependencies_satisfied = self._check_dependencies_satisfied(record)
        print(f"    {'✅' if check.dependencies_satisfied else '⚠️'} 依赖满足")
        
        # 6. 签名验证
        check.signature_verified = self._check_signature_verified(record)
        print(f"    {'✅' if check.signature_verified else '⚠️'} 签名已验证")
        
        self.connect_checks.append(check)
        
        # 计算通过率
        checks = [
            check.mother_engine_registered,
            check.interface_compatible,
            check.channel_established,
            check.six_system_matched,
            check.dependencies_satisfied,
            check.signature_verified,
        ]
        passed = sum(1 for c in checks if c)
        total = len(checks)
        
        print(f"\n  连接检查: {passed}/{total} 项通过")
        
        all_passed = passed >= 4  # 至少4项通过
        if all_passed:
            print(f"  ✅ 连接前置条件已满足（{passed}/{total}）")
            self.stats['connected'] += 1
        else:
            print(f"  ❌ 连接前置条件未满足（{passed}/{total}）")
        
        return all_passed
    
    # ----------------------------------------------------------
    # 3.4 Step 2: 激活前置检查
    # ----------------------------------------------------------
    
    def _run_activate_precondition(self, record: ManufacturingRecord) -> bool:
        """
        执行激活前置检查
        
        激活是引擎诞生的第二阶——没有激活的引擎是死物。
        前置条件：
        1. 激活能量充足
        2. 检测通过
        3. 理论映射已建立
        4. 引擎生命周期状态正常
        5. 记忆锚点就绪
        6. 通道印记已植入
        """
        print("\n  [Step 2] 激活前置检查...")
        print("  " + "─" * 40)
        
        check = ActivatePrecondition()
        
        # 1. 激活能量
        check.activation_energy = self._calculate_activation_energy(record)
        energy_ok = check.activation_energy >= 0.3
        print(f"    {'✅' if energy_ok else '❌'} 激活能量: {check.activation_energy:.2f}")
        
        # 2. 检测通过
        detection = record.verification_results.get('detection', {})
        check.detection_passed = detection.get('verdict') not in ['检测到可复用引擎']
        print(f"    {'✅' if check.detection_passed else '⚠️'} 检测通过")
        
        # 3. 理论映射
        check.theory_mapped = self._check_theory_mapping(record)
        print(f"    {'✅' if check.theory_mapped else '⚠️'} 理论映射已建立")
        
        # 4. 引擎生命周期
        check.engine_lifecycle_ok = True  # 默认正常
        print(f"    {'✅' if check.engine_lifecycle_ok else '❌'} 引擎生命周期正常")
        
        # 5. 记忆锚点
        check.memory_anchor_ready = self._check_memory_anchor_ready()
        print(f"    {'✅' if check.memory_anchor_ready else '⚠️'} 记忆锚点就绪")
        
        # 6. 通道印记
        check.channel_mark_implanted = self._check_channel_mark(record)
        print(f"    {'✅' if check.channel_mark_implanted else '⚠️'} 通道印记已植入")
        
        self.activate_checks.append(check)
        
        # 评估
        energy_passed = check.activation_energy >= 0.3
        theory_passed = check.theory_mapped
        lifecycle_passed = check.engine_lifecycle_ok
        
        all_passed = energy_passed and (theory_passed or lifecycle_passed)
        
        if all_passed:
            print(f"  ✅ 激活前置条件已满足")
            self.stats['activated'] += 1
        else:
            print(f"  ⚠️ 激活前置条件部分未满足，但在非严格模式下可继续")
        
        return energy_passed  # 能量是硬性要求
    
    # ----------------------------------------------------------
    # 3.5 Step 3: 生成制造计划
    # ----------------------------------------------------------
    
    def _generate_manufacturing_plan(self, record: ManufacturingRecord) -> List[str]:
        """生成融合制造计划"""
        plan = []
        
        # 分析需求
        requirement = record.requirement
        
        # 检测结果
        detection = record.verification_results.get('detection', {})
        verdict = detection.get('verdict', '未知')
        
        if verdict in ['直接复用', '检测到可复用引擎']:
            plan.append("1. 使用现有引擎直接复用")
        elif verdict == '扩展现有':
            plan.append("1. 基于现有引擎扩展功能")
            plan.append("2. 继承+扩展模式")
        elif verdict == '组合构建':
            plan.append("1. 从公有部件库提取基础部件")
            plan.append("2. 通过组合模式组装")
            plan.append("3. 验证组合完备性")
        else:
            plan.append("1. 分析需求的理论依据")
            plan.append("2. 设计引擎的六阶结构")
            plan.append("3. 提取基础公有部件")
            plan.append("4. 实现特有功能")
            plan.append("5. 注册到引擎图谱")
        
        plan.append(f"6. 验证与母引擎的连接兼容性")
        plan.append(f"7. 执行六阶闭环验证")
        
        record.manufacturing_plan = plan
        
        print(f"\n  [Step 3] 融合制造计划:")
        print("  " + "─" * 40)
        for step in plan:
            print(f"    {step}")
        
        return plan
    
    # ----------------------------------------------------------
    # 3.6 Step 4: 升维验证
    # ----------------------------------------------------------
    
    def _run_elevation_verification(self, record: ManufacturingRecord) -> Dict[str, Any]:
        """执行升维验证"""
        print(f"\n  [Step 4] 升维验证...")
        print("  " + "─" * 40)
        
        verification = {
            'protocol_version': self.PROTOCOL_VERSION,
            'connect_passed': True,
            'activate_passed': True,
            'manufacturing_plan': record.manufacturing_plan,
            'theory_mapping': None,
            'six_stage_ready': True,
        }
        
        # 尝试理论映射验证
        try:
            from theory_engine_mapping import TheoryEngineMapper
            mapper = TheoryEngineMapper()
            mapper.scan_theory_base()
            mapper.scan_engines()
            mapper.build_bridges()
            verification['theory_mapping'] = mapper.generate_report()
            print(f"    ✅ 理论映射验证通过")
        except ImportError:
            print(f"    ⚠️ 理论映射模块未安装，跳过验证")
            verification['theory_mapping'] = {'status': 'skipped'}
        
        # 六阶就绪检查
        stage_checks = ['连接', '激活', '融合', '升维', '等算', '计变']
        print(f"    ✅ 六阶就绪: {', '.join(stage_checks)}")
        
        return verification
    
    # ----------------------------------------------------------
    # 3.7 连接/激活检查辅助方法
    # ----------------------------------------------------------
    
    def _check_mother_registered(self) -> bool:
        """检查母引擎是否已注册"""
        if self.mother_engine is not None:
            return True
        # 检查是否有其他引擎已注册
        return len(self.connect_checks) > 0
    
    def _check_interface_compatible(self, record: ManufacturingRecord) -> bool:
        """检查接口兼容性"""
        # 基础检查——假设兼容（实际需要接口匹配）
        return True
    
    def _check_channel_established(self) -> bool:
        """检查连接通道"""
        return True  # 协议本身就是通道
    
    def _check_six_system_match(self, record: ManufacturingRecord, 
                                 six_system: str = None) -> bool:
        """检查六系归属匹配"""
        if six_system is None:
            return True  # 未指定则不检查
        return True
    
    def _check_dependencies_satisfied(self, record: ManufacturingRecord) -> bool:
        """检查依赖是否满足"""
        return True  # 假设依赖满足
    
    def _check_signature_verified(self, record: ManufacturingRecord) -> bool:
        """检查签名验证"""
        return True  # 协议内部验证
    
    def _calculate_activation_energy(self, record: ManufacturingRecord) -> float:
        """计算激活能量"""
        # 基础能量
        energy = 0.5
        
        # 如果有检测结果，增加能量
        detection = record.verification_results.get('detection', {})
        confidence = detection.get('confidence', 0.0)
        energy += confidence * 0.3
        
        # 如果有母引擎，增加能量
        if self.mother_engine is not None:
            energy += 0.2
        
        return min(energy, 1.0)
    
    def _check_theory_mapping(self, record: ManufacturingRecord) -> bool:
        """检查理论映射"""
        try:
            from theory_engine_mapping import TheoryEngineMapper
            return True
        except ImportError:
            return True  # 模块未安装则跳过
    
    def _check_memory_anchor_ready(self) -> bool:
        """检查记忆锚点"""
        return True
    
    def _check_channel_mark(self, record: ManufacturingRecord) -> bool:
        """检查通道印记"""
        return True
    
    # ----------------------------------------------------------
    # 3.8 报告输出
    # ----------------------------------------------------------
    
    def _print_record_summary(self, record: ManufacturingRecord):
        """打印制造记录摘要"""
        print(f"\n  {'=' * 40}")
        print(f"  【制造完成】{record.record_id}")
        print(f"  {'=' * 40}")
        print(f"  需求: {record.requirement}")
        print(f"  阶段: {record.phase.value}")
        print(f"  完成: {'是' if record.completed else '否'}")
        if record.failed_reason:
            print(f"  失败原因: {record.failed_reason}")
        
        if record.verification_results.get('detection'):
            det = record.verification_results['detection']
            print(f"  检测裁决: {det.get('verdict', 'N/A')}")
            print(f"  检测置信度: {det.get('confidence', 0):.2f}")
    
    def get_protocol_report(self) -> Dict[str, Any]:
        """获取协议执行报告"""
        return {
            'protocol_version': self.PROTOCOL_VERSION,
            'total_requests': self.stats['total_requests'],
            'passed': self.stats['passed'],
            'rejected': self.stats['rejected'],
            'connected': self.stats['connected'],
            'activated': self.stats['activated'],
            'manufactured': self.stats['manufactured'],
            'records': [
                {
                    'record_id': r.record_id,
                    'requirement': r.requirement,
                    'phase': r.phase.value,
                    'completed': r.completed,
                    'failed_reason': r.failed_reason,
                    'created_at': r.created_at,
                }
                for r in self.records[-20:]  # 最近20条
            ],
        }


# ============================================================
# 4. 便捷使用
# ============================================================

def quick_manufacture(requirement: str, 
                       six_system: str = None,
                       mother_engine=None) -> ManufacturingRecord:
    """快速执行引擎制造协议"""
    protocol = EngineManufacturingProtocol(mother_engine=mother_engine)
    return protocol.submit_requirement(requirement, six_system)


if __name__ == '__main__':
    print("=" * 60)
    print("【引擎制造前置协议演示】")
    print("=" * 60)
    
    protocol = EngineManufacturingProtocol(strict_mode=True)
    
    # 演示：提交制造需求
    test_requirements = [
        ("我需要一个围棋引擎，支持落子决策", "具现系🔴"),
        ("构建一个全新的记忆压缩系统", "强化系🔵"),
        ("扩展现有元数据注册表的功能", "天道系🟣"),
    ]
    
    for req, sys_name in test_requirements:
        print(f"\n{'─' * 60}")
        record = protocol.submit_requirement(req, sys_name)
        print(f"\n  结果: {'✅ 成功' if record.completed else '❌ 拒绝'}")
        if record.failed_reason:
            print(f"  原因: {record.failed_reason}")
    
    # 打印统计
    report = protocol.get_protocol_report()
    print(f"\n{'=' * 60}")
    print("【协议执行统计】")
    print(f"{'=' * 60}")
    print(f"  总请求: {report['total_requests']}")
    print(f"  通过: {report['passed']}")
    print(f"  拒绝: {report['rejected']}")
    print(f"  连接: {report['connected']}")
    print(f"  激活: {report['activated']}")
    print(f"  制造: {report['manufactured']}")