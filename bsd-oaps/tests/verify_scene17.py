"""
scene#17 "Agent 应用" 成立性验证脚本
—— 验证 ApplicationAgent T90 V1.8 升级后端到端可用、理论自洽、合规全通过
"""
import sys
import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from bsd_agents.application_agent import ApplicationAgent


def section(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def check(name, passed, detail=""):
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {name}" + (f" — {detail}" if detail else ""))
    return passed

results = {}

# ==================================================================
# 1. T90 V1.8 合规状态
# ==================================================================
section("1. T90 V1.8 合规状态检查")
agent = ApplicationAgent()
status = agent.get_t90_v18_status()

results["theory_version"] = check(
    "理论版本状态码", status["theory_version"] == "ACTIVE-V1.8",
    status["theory_version"]
)
results["params_verified"] = check(
    "锁档参数校验", status["params_verified"] is True,
    f"error={status.get('params_error')}" if status.get('params_error') else "7参数+对偶约束全通过"
)
results["all_operators_valid"] = check(
    "四大算子全部自检", status["all_operators_valid"] is True
)
for op_key, op_val in status["operators"].items():
    check(f"  {op_key}", op_val["validated"], f"模块ID={op_val['module_id']}")
results["copyright"] = check(
    "版权确权信息", (
        status["copyright"]["author"] == "杨腾飞" and
        status["copyright"]["hash_sha256"] is not None and
        "杨腾飞" in status["copyright"]["equity_split"]
    ),
    f"作者={status['copyright']['author']}, 锁档={status['copyright']['lock_date']}"
)

# ==================================================================
# 2. 双时针迭代动力学
# ==================================================================
section("2. C1 双时针迭代动力学验证")
iter_result = agent.run_dual_clockwise_iteration()
ir = iter_result["iteration_result"]

results["dual_clockwise"] = check(
    "双时针迭代可执行", iter_result["scene"] == "dual_clockwise_iteration"
)
results["duality_11_19"] = check(
    "定理11.19 对偶性 (𝒯₋∘𝒯₊=𝒟≠Id)",
    ir["duality_theorem_11_19"]["passed"],
    f"not_identity={ir['duality_theorem_11_19']['not_identity']}, "
    f"info_increased={ir['duality_theorem_11_19']['info_strictly_increased']}, "
    f"dim_increased={ir['duality_theorem_11_19']['dimension_increased']}"
)
results["trace_11_9"] = check(
    "推论11.9 信息痕迹守恒律 (ΣTrace > ΣLoss)",
    ir["info_trace_corollary_11_9"]["passed"],
    f"trace={ir['info_trace']}, loss={ir['info_loss']}, "
    f"trace_gt_loss={ir['info_trace_corollary_11_9']['trace_gt_loss']}"
)
results["ascension"] = check(
    "升维验证 (Info(1') > Info(1))",
    ir["ascension_verified"],
    f"info_content={ir['info_content']}, final_state={ir['final_state']}, dim={ir['final_dimension']}"
)

# ==================================================================
# 3. 三场景仿真端到端
# ==================================================================
section("3. 三场景仿真端到端验证")

# 3a. 医学
med = agent.apply_to_medicine({
    "qi": 0.8, "blood": 0.8, "body": 0.8, "mind": 0.8, "dao": 0.8,
    "time_steps": 100, "dt": 0.01,
})
results["medicine"] = check(
    "医学场景仿真", "error" not in med,
    f"health={med.get('health_level')}, coherence={med.get('global_coherence')}, "
    f"S0_assessment={med.get('s_zero_assessment')}"
)
check("  T90 V1.8 参数注入", "t90_v18_params" in med)
check("  theory_version 标注", med.get("theory_version") == "ACTIVE-V1.8")

# 3b. 物理
phys = agent.apply_to_physics({
    "Lambda": 1.1e-52, "Omega_m": 0.3111, "Omega_r": 9.0e-5,
    "time_steps": 50,
})
results["physics"] = check(
    "物理场景仿真", "error" not in phys,
    f"lambda_verify={phys.get('lambda_verification') is not None}"
)
check("  Π₂ 拓扑常数对照", "pi2_topological_constant" in phys)

# 3c. 文明
civ = agent.apply_to_civilization({
    "six_systems_params": [0.5, 0.6, 0.7, 0.4, 0.5, 0.6],
    "time_steps": 100, "dt": 0.1,
})
results["civilization"] = check(
    "文明场景仿真", "error" not in civ,
    f"catastrophe={civ.get('catastrophe') is not None}"
)
check("  C2 文明跃迁映射", "civilization_mapping" in civ)

# ==================================================================
# 4. 消息队列处理
# ==================================================================
section("4. 消息队列处理验证")
from bsd_agents.base import AgentMessage

agent2 = ApplicationAgent()
agent2.receive(AgentMessage(source="test", target="ApplicationAgent", content={
    "action": "run_dual_clockwise_iteration"
}))
agent2.receive(AgentMessage(source="test", target="ApplicationAgent", content={
    "action": "get_t90_v18_status"
}))
agent2.receive(AgentMessage(source="test", target="ApplicationAgent", content={
    "action": "run_simulation", "sim_type": "medicine",
    "params": {"qi": 0.8, "blood": 0.8, "body": 0.8, "mind": 0.8, "dao": 0.8, "time_steps": 50}
}))
msg_results = agent2.process()
results["message_queue"] = check(
    "消息队列处理 (3条消息)", len(msg_results) == 3,
    f"actions={[r['action'] for r in msg_results]}"
)
for r in msg_results:
    has_error = isinstance(r.get("result"), dict) and "error" in r.get("result", {})
    check(f"  {r['action']}", not has_error)

# ==================================================================
# 汇总
# ==================================================================
section("汇总")
total = len(results)
passed = sum(1 for v in results.values() if v)
print(f"\n  通过: {passed}/{total}")
all_pass = all(results.values())
print(f"  scene#17 \"Agent 应用\" 成立: {'YES' if all_pass else 'NO'}")

sys.exit(0 if all_pass else 1)
