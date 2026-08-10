"""
BSD-OAPS 核心模块（迁移自 theory_code/core/）

归属基底：L0_总本源层·六系核心公理·六系立系论V1.8
对应公理：六系立系公理（六系=立系坐标系·0×0=n）

六系方向导航模块群：
    - six_system_project_mapper    : 六系↔项目方向映射核心
    - six_system_agent_direction   : 智能体六系方向导航
    - six_system_project_scaffold  : 项目六系目录脚手架
    - six_system_personal_diagnostic: 六系个人诊断器
"""

# 六系方向导航模块
from bsd_engine.core.six_system_project_mapper import (
    SixSystem,
    SystemDirection,
    SIX_SYSTEM_DIRECTIONS,
    SixSystemProjectMapper,
)

from bsd_engine.core.six_system_agent_direction import (
    EvolutionProtocol,
    PROTOCOL_SYSTEM_MAP,
    AgentDirectionState,
    NavigationResult,
    SixSystemAgentDirection,
)

from bsd_engine.core.six_system_project_scaffold import (
    SYSTEM_DIR_NAMES,
    SixSystemProjectScaffold,
)

from bsd_engine.core.six_system_personal_diagnostic import (
    SystemStatus, ProtocolCompliance, SystemDiagnosis, SixSystemProfile,
    DiagnosticResult, SixSystemPersonalDiagnostic,
)

from bsd_engine.core.six_system_self_organization_engine import (
    AgentIntrinsicFunction,
    SYSTEM_INTRINSIC_MAP,
    ConductionChannel,
    SelfOrganizationState,
    CONDUCTION_MATRIX_TEMPLATE,
    SixSystemSelfOrganizationEngine,
)

from bsd_engine.core.six_system_completion_suite import (
    CompletionTask,
    SixSystemCompletionSuite,
)

from bsd_engine.core.six_system_bootstrap_engine import (
    EmergenceRule,
    EMERGENCE_RULES,
    SIX_SYSTEM_THEORY_SELF_POSITION,
    SixSystemBootstrapEngine,
)

from bsd_engine.core.theory_driven_engine import (
    TaskStatus,
    EngineeringTask,
    SYSTEM_ENGINEERING_DIRECTION,
    TheoryDrivenEngine,
)

from bsd_engine.core.six_system_nested_coupling import (
    SYSTEM_INTRINSIC_LABELS,
    NESTED_COUPLING_MATRIX,
    KEY_CONTAINMENTS,
    EmergenceInstance,
    EMERGENCE_001,
    PerpetualInquiryPhase,
    SixSystemNestedCoupling,
)

__all__ = [
    # 六系枚举与映射
    "SixSystem",
    "SystemDirection",
    "SIX_SYSTEM_DIRECTIONS",
    "SixSystemProjectMapper",
    # 智能体方向导航
    "EvolutionProtocol",
    "PROTOCOL_SYSTEM_MAP",
    "AgentDirectionState",
    "NavigationResult",
    "SixSystemAgentDirection",
    # 项目脚手架
    "SYSTEM_DIR_NAMES",
    "SixSystemProjectScaffold",
    # 个人诊断
    "SystemStatus",
    "ProtocolCompliance",
    "SystemDiagnosis",
    "SixSystemProfile",
    "DiagnosticResult",
    "SixSystemPersonalDiagnostic",
    # 自组织完备引擎
    "AgentIntrinsicFunction",
    "SYSTEM_INTRINSIC_MAP",
    "ConductionChannel",
    "SelfOrganizationState",
    "CONDUCTION_MATRIX_TEMPLATE",
    "SixSystemSelfOrganizationEngine",
    # 完备化套件
    "CompletionTask",
    "SixSystemCompletionSuite",
    # 自举引擎
    "EmergenceRule",
    "EMERGENCE_RULES",
    "SIX_SYSTEM_THEORY_SELF_POSITION",
    "SixSystemBootstrapEngine",
    # 理论自组织工程驱动器
    "TaskStatus",
    "EngineeringTask",
    "SYSTEM_ENGINEERING_DIRECTION",
    "TheoryDrivenEngine",
    # 六系互相内含引擎（V2.0）
    "SYSTEM_INTRINSIC_LABELS",
    "NESTED_COUPLING_MATRIX",
    "KEY_CONTAINMENTS",
    "EmergenceInstance",
    "EMERGENCE_001",
    "PerpetualInquiryPhase",
    "SixSystemNestedCoupling",
]
