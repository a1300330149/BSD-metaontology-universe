"""
归属基底：第0重元道本源基底
对应公理：宿命双边界公理（理论-代码-实验三向绑定）
对应九维维度：元理天道
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92, κ=0.35

交叉验证 Agent（理论-代码-实验三层闭环验证）
—— 调用 bsd_engine.validators.* 既有模块
   完成理论-代码-实验三向闭环校验，确保三界秩序天道锚定
"""
from typing import Any, Dict, List, Optional

from bsd_agents.base import BSDAgentBase, AgentMessage
from bsd_engine.validators.binding_checker import (
    scan_all_source_files,
    check_bsd_annotation_coverage,
)
from bsd_engine.validators.compliance_checker import (
    check_axiom_completeness,
    check_equation_completeness,
)
from bsd_engine.validators.hash_checker import verify_core_params
from bsd_engine.registry.constants import GAMMA, KAPPA


class CrossValidationAgent(BSDAgentBase):
    """
    交叉验证 Agent（理论-代码-实验三层闭环）

    职责：
    - validate_theory_code：验证理论-代码双向绑定（BSD标注 + 公理引用）
    - validate_code_experiment：验证代码-实验一致性（哈希 + 方程求解器）
    - validate_theory_experiment：验证理论-实验一致性（参数锁档 + 公理完备性）
    - run_full_validation：执行全套三层交叉验证
    - generate_report：生成 Markdown 验证报告
    """

    def __init__(self):
        super().__init__(
            name="CrossValidationAgent",
            description="交叉验证Agent：理论-代码-实验三层闭环校验",
        )
        self._last_report: Optional[Dict[str, Any]] = None

    # ------------------------------------------------------------------
    # 理论-代码双向绑定验证
    # ------------------------------------------------------------------
    def validate_theory_code(self, theory_id: str, code_path: str) -> Dict[str, Any]:
        """
        验证理论-代码双向绑定。

        参数
        ----
        theory_id : str
            理论模块标识（如 "T1"/"T25"）。空字符串视为扫描全部。
        code_path : str
            代码路径（可为目录或文件）。空字符串则使用默认引擎路径。

        返回
        ----
        dict
            {
                "theory_id": str,
                "code_path": str,
                "annotated_files": int,
                "coverage": float,
                "binding_pass": bool,
                "headers_sample": {...},
            }
        """
        try:
            headers = scan_all_source_files(code_path if code_path else None)
        except Exception as exc:  # noqa: BLE001 - 容错保护
            return {
                "theory_id": theory_id,
                "code_path": code_path,
                "error": f"扫描源文件失败: {exc}",
                "binding_pass": False,
            }

        try:
            coverage, annotated, total = check_bsd_annotation_coverage()
        except Exception as exc:  # noqa: BLE001 - 容错保护
            coverage, annotated, total = 0.0, 0, 0

        # 过滤命中指定 theory_id 的文件（若提供）
        matched: Dict[str, Any] = {}
        if theory_id:
            for rel, header in headers.items():
                ref = str(header.get("理论原文出处", ""))
                if theory_id.lower() in rel.lower() or theory_id.lower() in ref.lower():
                    matched[rel] = header
        else:
            # 取前 5 条作为样本
            for idx, (rel, header) in enumerate(headers.items()):
                if idx >= 5:
                    break
                matched[rel] = header

        binding_pass = coverage >= 0.8 and len(headers) > 0
        return {
            "theory_id": theory_id,
            "code_path": code_path,
            "annotated_files": len(headers),
            "coverage": coverage,
            "coverage_detail": {"annotated": annotated, "total": total},
            "binding_pass": binding_pass,
            "headers_sample": matched,
        }

    # ------------------------------------------------------------------
    # 代码-实验一致性验证
    # ------------------------------------------------------------------
    def validate_code_experiment(self, code_module: str, experiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证代码-实验一致性。

        参数
        ----
        code_module : str
            代码模块名（用于追溯，可为空）
        experiment_data : dict
            实验数据，可包含 expected_params（期望锁档参数）

        返回
        ----
        dict
            {
                "code_module": str,
                "hash_passed": bool,
                "hash_errors": List[str],
                "equation_complete": bool,
                "equation_stats": dict,
                "consistency_pass": bool,
            }
        """
        try:
            hash_passed, hash_errors = verify_core_params()
        except Exception as exc:  # noqa: BLE001
            hash_passed, hash_errors = False, [f"哈希校验异常: {exc}"]

        try:
            eq_complete, eq_stats = check_equation_completeness()
        except Exception as exc:  # noqa: BLE001
            eq_complete, eq_stats = False, {"error": str(exc)}

        consistency_pass = hash_passed and eq_complete
        return {
            "code_module": code_module,
            "hash_passed": hash_passed,
            "hash_errors": list(hash_errors),
            "equation_complete": eq_complete,
            "equation_stats": eq_stats,
            "experiment_data_keys": list(experiment_data.keys()) if isinstance(experiment_data, dict) else [],
            "consistency_pass": consistency_pass,
        }

    # ------------------------------------------------------------------
    # 理论-实验一致性验证
    # ------------------------------------------------------------------
    def validate_theory_experiment(self, theory_id: str, experiment_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        验证理论-实验一致性（公理完备性 + 锁档参数）。

        参数
        ----
        theory_id : str
            理论模块标识
        experiment_data : dict
            实验数据，可包含 expected_axiom_count

        返回
        ----
        dict
            {
                "theory_id": str,
                "axiom_complete": bool,
                "axiom_stats": dict,
                "hash_passed": bool,
                "consistency_pass": bool,
            }
        """
        try:
            axiom_complete, axiom_stats = check_axiom_completeness()
        except Exception as exc:  # noqa: BLE001
            axiom_complete, axiom_stats = False, {"error": str(exc)}

        try:
            hash_passed, _ = verify_core_params()
        except Exception:  # noqa: BLE001
            hash_passed = False

        expected = 0
        if isinstance(experiment_data, dict):
            try:
                expected = int(experiment_data.get("expected_axiom_count", 0))
            except Exception:  # noqa: BLE001
                expected = 0

        actual_total = int(axiom_stats.get("total_axioms", 0)) if isinstance(axiom_stats, dict) else 0
        count_match = (expected == 0) or (expected == actual_total)

        consistency_pass = axiom_complete and hash_passed and count_match
        return {
            "theory_id": theory_id,
            "axiom_complete": axiom_complete,
            "axiom_stats": axiom_stats,
            "hash_passed": hash_passed,
            "expected_axiom_count": expected,
            "actual_axiom_count": actual_total,
            "count_match": count_match,
            "consistency_pass": consistency_pass,
        }

    # ------------------------------------------------------------------
    # 执行全套交叉验证
    # ------------------------------------------------------------------
    def run_full_validation(self) -> Dict[str, Any]:
        """
        执行全套三层交叉验证。

        返回
        ----
        dict
            {
                "theory_code": {...},
                "code_experiment": {...},
                "theory_experiment": {...},
                "overall_pass": bool,
                "constants": {...},
            }
        """
        tc = self.validate_theory_code("", "")
        ce = self.validate_code_experiment("", {})
        te = self.validate_theory_experiment("", {})

        overall = bool(
            tc.get("binding_pass", False)
            and ce.get("consistency_pass", False)
            and te.get("consistency_pass", False)
        )

        report = {
            "theory_code": tc,
            "code_experiment": ce,
            "theory_experiment": te,
            "overall_pass": overall,
            "constants": {"GAMMA": GAMMA, "KAPPA": KAPPA},
        }
        self._last_report = report
        return report

    # ------------------------------------------------------------------
    # 生成验证报告
    # ------------------------------------------------------------------
    def generate_report(self) -> Dict[str, Any]:
        """
        生成 Markdown 验证报告（若未运行全套验证则自动触发）。
        """
        if self._last_report is None:
            self.run_full_validation()

        r = self._last_report or {}
        tc = r.get("theory_code", {})
        ce = r.get("code_experiment", {})
        te = r.get("theory_experiment", {})

        lines: List[str] = []
        lines.append("# BSD 交叉验证报告")
        lines.append("")
        lines.append(f"**综合结果**: {'✓ 通过' if r.get('overall_pass') else '✗ 存在缺陷'}")
        lines.append("")
        lines.append("## 1. 理论-代码双向绑定")
        lines.append(f"- 已标注文件数: {tc.get('annotated_files', 0)}")
        lines.append(f"- BSD标注覆盖率: {tc.get('coverage', 0.0) * 100:.1f}%")
        lines.append(f"- 绑定状态: {'✓ 有效' if tc.get('binding_pass') else '✗ 缺陷'}")
        lines.append("")
        lines.append("## 2. 代码-实验一致性")
        lines.append(f"- 哈希锁档校验: {'✓ 通过' if ce.get('hash_passed') else '✗ 失败'}")
        lines.append(f"- 方程求解器完整性: {'✓ 完整' if ce.get('equation_complete') else '✗ 缺失'}")
        lines.append(f"- 一致性: {'✓ 一致' if ce.get('consistency_pass') else '✗ 不一致'}")
        lines.append("")
        lines.append("## 3. 理论-实验一致性")
        lines.append(f"- 公理完备性: {'✓ 完整' if te.get('axiom_complete') else '✗ 不完整'}")
        lines.append(f"- 公理总数: {te.get('actual_axiom_count', 0)}")
        lines.append(f"- 锁档参数校验: {'✓ 通过' if te.get('hash_passed') else '✗ 失败'}")
        lines.append("")
        lines.append("## 固定常量")
        lines.append(f"- γ (GAMMA) = {GAMMA}")
        lines.append(f"- κ (KAPPA) = {KAPPA}")

        return {
            "markdown": "\n".join(lines),
            "overall_pass": r.get("overall_pass", False),
            "raw": r,
        }

    # ------------------------------------------------------------------
    # 消息处理
    # ------------------------------------------------------------------
    def process(self) -> List[Dict[str, Any]]:
        """
        处理消息队列中的验证请求。

        支持的 content.action：
        - "validate_theory_code"      content.theory_id / content.code_path
        - "validate_code_experiment"  content.code_module / content.experiment_data
        - "validate_theory_experiment" content.theory_id / content.experiment_data
        - "run_full_validation"
        - "generate_report"
        """
        results: List[Dict[str, Any]] = []
        while self.message_queue:
            msg: AgentMessage = self.message_queue.pop(0)
            content = msg.content if isinstance(msg.content, dict) else {}
            action = content.get("action", "")
            try:
                if action == "validate_theory_code":
                    res = self.validate_theory_code(
                        content.get("theory_id", ""),
                        content.get("code_path", ""),
                    )
                elif action == "validate_code_experiment":
                    res = self.validate_code_experiment(
                        content.get("code_module", ""),
                        content.get("experiment_data", {}) or {},
                    )
                elif action == "validate_theory_experiment":
                    res = self.validate_theory_experiment(
                        content.get("theory_id", ""),
                        content.get("experiment_data", {}) or {},
                    )
                elif action == "run_full_validation":
                    res = self.run_full_validation()
                elif action == "generate_report":
                    res = self.generate_report()
                else:
                    res = {"error": f"未知 action: {action}"}
            except Exception as exc:  # noqa: BLE001 - 容错保护
                res = {"error": str(exc), "action": action}
            results.append({
                "message_id": msg.message_id,
                "action": action,
                "result": res,
            })
        return results
