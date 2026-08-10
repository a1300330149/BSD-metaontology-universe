"""
理论注册验证脚本 —— 注册29个核心模块并执行完整守卫校验
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from theory_code.core.base_theory_module import BaseTheoryModule
from theory_code.core.theory_hub import TheoryHub

hub = TheoryHub()
hub.clear()

from theory_code.theories.t29_self_excited_phase_transition import SelfExcitedPhaseTransition
from theory_code.core.void_potential_accumulator import VoidPotentialAccumulator
from theory_code.core.dual_polarity_spawner import DualPolaritySpawner
from theory_code.core.nine_realms_emergence import NineRealmsEmergence
from theory_code.core.entropy_zero_point_regression import EntropyZeroPointRegression
from theory_code.core.closure_judgment import ClosureJudgment

from theory_code.theories.t30_dual_boundary_isolation import DualBoundaryIsolation
from theory_code.core.vbb_topology_operator import VBBTopologyOperator
from theory_code.core.cpfb_outer_container import CPFBOuterContainer
from theory_code.core.dual_asymmetry_verifier import DualAsymmetryVerifier
from theory_code.core.cross_realm_contamination_detector import CrossRealmContaminationDetector
from theory_code.core.dual_origin_closure_judge import DualOriginClosureJudge

from theory_code.theories.t31_ni_tengfei_five_theories import NiTengfeiFiveTheories
from theory_code.core.dual_weight_normalizer import DualWeightNormalizer
from theory_code.core.dual_mapping_matrix import DualMappingMatrix
from theory_code.core.reverse_entropy_calculator import ReverseEntropyCalculator
from theory_code.core.global_entropy_conservation_judge import GlobalEntropyConservationJudge
from theory_code.core.new_realm_birth_detector import NewRealmBirthDetector

from theory_code.theories.t32_duality_system_grand_theory import DualitySystemGrandTheory
from theory_code.core.dual_six_systems_mapper import DualSixSystemsMapper
from theory_code.core.bidirectional_phase_transition import BidirectionalPhaseTransition
from theory_code.core.reverse_three_stage_transformer import ReverseThreeStageTransformer
from theory_code.core.eighteen_realm_duality_judge import EighteenRealmDualityJudge
from theory_code.core.duality_completeness_auditor import DualityCompletenessAuditor

from theory_code.theories.t33_parallel_origin_systems import ParallelOriginSystems
from theory_code.core.material_replacement_operator import MaterialReplacementOperator
from theory_code.core.multi_origin_coupler import MultiOriginCoupler
from theory_code.core.cross_origin_weight_mapper import CrossOriginWeightMapper
from theory_code.core.meta_axiom_implementer import MetaAxiomImplementer
from theory_code.theories.t34_zero_ontology_six_systems import (
    SixSystemsOntologyZero,
    ThreeAxiomsOfExistence,
    ThreeAxiomsOrthogonalityProof,
    ShengKeDualClosure,
    ZeroPresetUltimateClosure,
    AbsoluteVoidCore,
    ThreeFoldDifferentiation,
    FourYuanOntology,
)

modules = [
    SelfExcitedPhaseTransition(),
    VoidPotentialAccumulator(),
    DualPolaritySpawner(),
    NineRealmsEmergence(),
    EntropyZeroPointRegression(),
    ClosureJudgment(),
    DualBoundaryIsolation(),
    VBBTopologyOperator(),
    CPFBOuterContainer(),
    DualAsymmetryVerifier(),
    CrossRealmContaminationDetector(),
    DualOriginClosureJudge(),
    NiTengfeiFiveTheories(),
    DualWeightNormalizer(),
    DualMappingMatrix(),
    ReverseEntropyCalculator(),
    GlobalEntropyConservationJudge(),
    NewRealmBirthDetector(),
    DualitySystemGrandTheory(),
    DualSixSystemsMapper(),
    BidirectionalPhaseTransition(),
    ReverseThreeStageTransformer(),
    EighteenRealmDualityJudge(),
    DualityCompletenessAuditor(),
    ParallelOriginSystems(),
    MaterialReplacementOperator(),
    MultiOriginCoupler(),
    CrossOriginWeightMapper(),
    MetaAxiomImplementer(),
    # T34 新增模块
    AbsoluteVoidCore(),
    ThreeFoldDifferentiation(),
    FourYuanOntology(),
    ThreeAxiomsOfExistence(),
    ThreeAxiomsOrthogonalityProof(),
    SixSystemsOntologyZero(),
    ShengKeDualClosure(),
    ZeroPresetUltimateClosure(),
]

print("=" * 70)
print("  理论注册中心 · 29模块批量注册与守卫校验")
print("=" * 70)
print()

for m in modules:
    ok = hub.register(m)
    status = "✓" if ok else "✗"
    print(f"  {status} [{m.module_id}] {m.module_name} (L{m.cosmic_level})")

print()
print("-" * 70)
print(f"  注册完成：共 {len(modules)} 个模块，成功 {len(hub.get_all())} 个")
print("-" * 70)
print()

dep_result = hub.validate_dependencies()
val_result = hub.validate_all()
origin_locked = hub.get_origin_locked()

print(hub.integrity_report())
print()

print("  本源锁定模块清单：")
for m in origin_locked:
    print(f"    • [{m.module_id}] {m.module_name} — SHA256: {m.sha256[:16]}...")
print()

print("  校验结果统计：")
print(f"    依赖校验通过率: {dep_result['passed']}/{dep_result['total_modules']}")
print(f"    完整自检通过率: {val_result['passed']}/{val_result['total_modules']}")
print()

failed_deps = [k for k, v in dep_result['details'].items() if v['status'] == 'FAIL']
failed_val = [k for k, v in val_result['details'].items() if v['status'] == 'FAIL']

if failed_deps:
    print("  ⚠ 依赖缺失模块：")
    for mid in failed_deps:
        print(f"    • {mid}: 缺失 {dep_result['details'][mid]['missing_deps']}")
    print()

if failed_val:
    print("  ⚠ 自检失败模块：")
    for mid in failed_val:
        print(f"    • {mid}: {val_result['details'][mid]['errors']}")
    print()

all_pass = dep_result['failed'] == 0 and val_result['failed'] == 0
print("=" * 70)
if all_pass:
    print("  ✅ 全部通过！29个模块守卫校验 100% 通过")
else:
    print(f"  ❌ 存在未通过项：依赖{dep_result['failed']}个，自检{val_result['failed']}个")
print("=" * 70)
