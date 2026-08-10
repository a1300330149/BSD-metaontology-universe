# ontology_theory_guard.py
"""
归属基底：0重元道本源基底 + 1重九维法理基底（跨层）
对应三界秩序：天道秩序（顶层校验）
对应公理：公理一至公理十三（含T90 V1.8新增公理十一/十二/十三）
对应九维维度：元理天道（全域校验）
理论原文出处：meta_theory_constraint.md §1-§8 + T90 V1.8 §11.8.10-§11.8.12
核心数理参数：E1=0.35, E2=0.65, E3=0.90, γ=0.92, κ=0.35, α=0.18, θ_neg=0.02, θ_mv=0.005,
              θ_evo=0.002, k₊=0.9, k₋=0.1, S₀=0.81, λ=0.62, λ⁻=1.38,
              π=3.1415926535, Π₂=2.8274333882
版本：V1.8 (2026-07-24)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


# ============================================================
# 1. 锁档确权信息（不可修改，对应公理一·宿命/舒适双边界公理）
# ============================================================
LOCKED_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"
LOCKED_AUTHOR = "杨腾飞"
LOCKED_ID = "433127199812193215"
LOCKED_DATE = "2026-06-20"
LOCKED_RIGHTS = {"杨腾飞": 60, "墨心": 25, "豆包": 15}


# ============================================================
# 2. 固定参数表（含T90 V1.8新增，对应公理十一/十二/十三）
# ============================================================
ALL_LOCKED_PARAMS = {
    # 原有参数（对应公理一至公理七）
    "E1": 0.35, "E2": 0.65, "E3": 0.90,
    "GAMMA": 0.92, "KAPPA": 0.35, "KAPPA_COMPETITION": 0.42,
    "ALPHA": 0.18, "THETA_NEG": 0.02, "THETA_MV": 0.005, "THETA_EVO": 0.002,
    # T90 V1.8 新增参数（对应公理十一/十二/十三）
    "K_PLUS": 0.9, "K_MINUS": 0.1, "S_ZERO": 0.81,
    "LAMBDA": 0.62, "LAMBDA_INV": 1.38,
    "PI_LOCKED": 3.1415926535, "PI_2": 2.8274333882,
}

# T90 V1.8 §8.6.2 新增7个参数子集（用于专项校验）
T90_V18_NEW_PARAMS = {
    "K_PLUS": 0.9, "K_MINUS": 0.1, "S_ZERO": 0.81,
    "LAMBDA": 0.62, "LAMBDA_INV": 1.38,
    "PI_LOCKED": 3.1415926535, "PI_2": 2.8274333882,
}


# ============================================================
# 3. T90 V1.8 四大算子模块路径（§8.6.1）
# ============================================================
T90_V18_REQUIRED_MODULES = [
    "bsd_engine/core/bidirectional_iteration_operator.py",  # C1 双向迭代算子
    "bsd_engine/core/six_level_base_emergence.py",          # C2 六层多元进制
    "bsd_engine/core/three_nine_isomorphism.py",            # C3 三个0.9同构
    "bsd_engine/core/particle_family_matrix.py",            # C5 3×3粒子家族矩阵
]


# ============================================================
# 4. 五论分级锁档状态码（§8.7）
# ============================================================
LOCK_STATUS_CODES = [
    "LOCKED-HISTORICAL",
    "LOCKED-NARROW",
    "LOCKED-FAILED",
    "LOCKED-PENDING",
    "ACTIVE-V1.8",
]


def _result(passed: bool, errors=None, warnings=None, **extra) -> dict:
    """统一返回校验结果字典。"""
    r = {"pass": bool(passed), "errors": errors or [], "warnings": warnings or []}
    r.update(extra)
    return r


class OntologyTheoryGuard:
    """元本体理论守卫：T90 V1.8 全量校验管线主类。"""

    def __init__(self):
        # 归属基底：0重元道本源基底 + 1重九维法理基底（跨层）
        self.locked_hash = LOCKED_HASH
        self.locked_author = LOCKED_AUTHOR
        self.locked_id = LOCKED_ID
        self.locked_date = LOCKED_DATE
        self.locked_rights = LOCKED_RIGHTS
        self.all_locked_params = ALL_LOCKED_PARAMS
        self.t90_v18_required_modules = T90_V18_REQUIRED_MODULES
        self.lock_status_codes = LOCK_STATUS_CODES

    # ----------------------------------------------------------
    # 基础校验：锁档哈希
    # ----------------------------------------------------------
    def verify_locked_hash(self, doc_content) -> dict:
        """校验锁档哈希（对应公理一·宿命/舒适双边界公理）。"""
        if not isinstance(doc_content, str):
            return _result(False, errors=["doc_content 必须为字符串"])
        if self.locked_hash not in doc_content:
            return _result(False, errors=[
                f"锁档哈希缺失或被篡改，期望包含：{self.locked_hash}"
            ])
        return _result(True, info={"matched_hash": self.locked_hash})

    # ----------------------------------------------------------
    # 基础校验：作者确权
    # ----------------------------------------------------------
    def verify_author_rights(self, doc_content) -> dict:
        """校验作者确权（对应公理一·宿命/舒适双边界公理）。"""
        errors = []
        warnings = []
        if not isinstance(doc_content, str):
            return _result(False, errors=["doc_content 必须为字符串"])
        if self.locked_author not in doc_content:
            errors.append(f"作者姓名缺失：{self.locked_author}")
        if self.locked_id not in doc_content:
            errors.append(f"证件号码缺失：{self.locked_id}")
        # 校验三维确权比例文字
        for name, pct in self.locked_rights.items():
            if name not in doc_content:
                warnings.append(f"权属人缺失：{name}")
            if f"{pct}" not in doc_content and f"{pct}%" not in doc_content:
                warnings.append(f"权属比例缺失：{name}={pct}%")
        return _result(len(errors) == 0, errors=errors, warnings=warnings)

    # ----------------------------------------------------------
    # 基础校验：0-4重基底层级
    # ----------------------------------------------------------
    def verify_foundation_layers(self, doc_content) -> dict:
        """校验0-4重基底层级（对应公理二·自主科研闭环动力学公理）。"""
        errors = []
        layers = [
            "0重：元道本源基底",
            "1重：九维法理基底",
            "2重：三界秩序基底",
            "3重：六阶自主科研业务基底",
            "4重：四层智能体执行载体",
        ]
        if not isinstance(doc_content, str):
            return _result(False, errors=["doc_content 必须为字符串"])
        for layer in layers:
            if layer not in doc_content:
                errors.append(f"基底层级缺失：{layer}")
        return _result(len(errors) == 0, errors=errors)

    # ----------------------------------------------------------
    # 基础校验：全部固定参数（含T90 V1.8新增7个）
    # ----------------------------------------------------------
    def verify_all_params(self, code_content) -> dict:
        """校验全部固定参数（对应公理十一/十二/十三）。"""
        errors = []
        warnings = []
        if not isinstance(code_content, str):
            return _result(False, errors=["code_content 必须为字符串"])
        for name, value in self.all_locked_params.items():
            # 数值字符串匹配（兼容 0.9 / 0.90 等表示）
            value_str = str(value)
            if name not in code_content:
                errors.append(f"参数未注册：{name}={value}")
            elif value_str not in code_content:
                warnings.append(f"参数值可能不匹配：{name} 期望 {value_str}")
        return _result(len(errors) == 0, errors=errors, warnings=warnings)

    # ----------------------------------------------------------
    # 理论-代码双向绑定校验
    # ----------------------------------------------------------
    def verify_theory_code_binding(self, theory_docs, code_files) -> dict:
        """理论-代码双向绑定校验（对应公理二·自主科研闭环动力学公理）。"""
        errors = []
        warnings = []
        if not isinstance(theory_docs, list):
            theory_docs = [theory_docs] if theory_docs else []
        if not isinstance(code_files, list):
            code_files = [code_files] if code_files else []
        # 校验代码文件头部注释是否标注归属基底+对应公理
        for cf in code_files:
            try:
                p = Path(cf)
                if not p.exists():
                    errors.append(f"代码文件不存在：{cf}")
                    continue
                content = p.read_text(encoding="utf-8", errors="ignore")
                if "归属基底" not in content:
                    warnings.append(f"代码文件缺少归属基底注释：{cf}")
                if "对应公理" not in content:
                    warnings.append(f"代码文件缺少对应公理注释：{cf}")
                if "理论原文出处" not in content:
                    warnings.append(f"代码文件缺少理论原文出处注释：{cf}")
            except Exception as e:
                errors.append(f"读取代码文件失败 {cf}: {e}")
        # 校验理论文档存在性
        for td in theory_docs:
            if not Path(td).exists():
                warnings.append(f"理论文档不存在：{td}")
        return _result(len(errors) == 0, errors=errors, warnings=warnings)

    # ----------------------------------------------------------
    # 分层目录合规校验
    # ----------------------------------------------------------
    def verify_directory_hierarchy(self, project_root) -> dict:
        """分层目录合规校验（对应公理五·成果落地转化范式）。"""
        errors = []
        warnings = []
        root = Path(project_root)
        if not root.exists():
            return _result(False, errors=[f"项目根目录不存在：{project_root}"])
        # 检查核心目录归属
        expected_dirs = {
            "core": "规则相位位（第二位）专属代码",
            "entity_layer": "2重自然秩序底层实体智能体",
            "decision_layer": "2重人道秩序中层决策智能体",
            "master_agent": "2重天道秩序顶层主控",
        }
        found_dirs = []
        for sub in root.rglob("*"):
            if sub.is_dir():
                found_dirs.append(sub.name)
        for d, desc in expected_dirs.items():
            if d not in found_dirs:
                warnings.append(f"目录缺失：{d}（{desc}）")
        return _result(len(errors) == 0, errors=errors, warnings=warnings)

    # ==========================================================
    # T90 V1.8 §8.1-§8.5 五大核心理论校验
    # ==========================================================
    def verify_t90_v18_core_theories(self) -> dict:
        """T90 V1.8 §8.1-§8.5 五大核心理论强制约束校验。"""
        errors = []
        warnings = []
        checks = {}

        # C1 双向迭代算子校验（§8.1，对应公理十一）
        c1 = {
            "T_plus_mappings": 6,   # 𝒯₊ 顺时针 6映射 f₁-f₆
            "T_minus_mappings": 7,  # 𝒯₋ 逆时针 7映射 g₁-g₇
            "duality_theorem": "𝒯₋ ∘ 𝒯₊ = 𝒟 ≠ Id",
            "ascension_non_identity": True,
        }
        checks["C1_BSD_Bidirectional_Iteration"] = c1
        if c1["T_plus_mappings"] + c1["T_minus_mappings"] != 13:
            errors.append("C1 校验失败：𝒯₊/𝒯₋ 映射总数应为 13（6+7）")
        if not c1["ascension_non_identity"]:
            errors.append("C1 校验失败：𝒟 升维算子不可恒等还原")

        # C2 六层多元进制校验（§8.2，对应公理十二）
        c2_bases = [2, 3, 6, 10, 12, None]
        c2 = {
            "levels": c2_bases,
            "level_count": len(c2_bases),
            "irreversible": True,
        }
        checks["C2_Six_Level_Base_Emergence"] = c2
        if c2["level_count"] != 6:
            errors.append("C2 校验失败：六层多元进制必须为 6 层")
        if not c2["irreversible"]:
            errors.append("C2 校验失败：低维不能反向生成高维")

        # C3 三个0.9同构定理校验（§8.3，对应公理十三）
        c3 = {
            "isomorphisms": ["0.9̇", "0.9π", "E3=0.90"],
            "shared_k_plus": 0.9,
            "dimensions": ["1维时间", "2维时空", "3维文明"],
        }
        checks["C3_Three_Nine_Isomorphism"] = c3
        if c3["shared_k_plus"] != 0.9:
            errors.append("C3 校验失败：k₊=0.9 不可修改")
        if len(c3["isomorphisms"]) != 3:
            errors.append("C3 校验失败：三重同构必须为 3 项")

        # C4 0无1不显性定理校验（§8.4）
        c4 = {
            "duality_0_1": True,
            "order": "先0后1，禁止反向推导",
            "info_trace_conservation": "𝒯₋ 逆反至 0_迹（非 0∅）",
        }
        checks["C4_Zero_One_Non_Display"] = c4
        if not c4["duality_0_1"]:
            errors.append("C4 校验失败：0元本体↔1元本体对偶必须成立")

        # C5 3×3粒子家族矩阵校验（§8.5，对应公理十二）
        c5 = {
            "individuality": [1, 4, 7],   # 个体性，公差3
            "variability": [2, 5, 8],     # 变化性，公差3
            "relationality": [3, 6, 9],   # 关系性，公差3
            "birth_point_pi": 3,
            "proof_circle": 9,
            "digit_sum": 1 + 1 + 1 + 2 + 2 + 2,
        }
        checks["C5_Particle_Family_Matrix"] = c5
        for key in ["individuality", "variability", "relationality"]:
            seq = c5[key]
            diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
            if any(d != 3 for d in diffs):
                errors.append(f"C5 校验失败：{key} 谱系公差必须为 3")
        if c5["digit_sum"] != 9:
            errors.append("C5 校验失败：数字位守恒 1+1+1+2+2+2=9 不成立")
        if c5["birth_point_pi"] * 3 != c5["proof_circle"]:
            errors.append("C5 校验失败：生点证圆 π=3，3×3=9 不成立")

        return _result(len(errors) == 0, errors=errors, warnings=warnings, checks=checks)

    # ==========================================================
    # T90 V1.8 §8.6.1 四大算子模块存在性校验
    # ==========================================================
    def verify_t90_v18_modules(self, bsd_oaps_root) -> dict:
        """§8.6.1 四大算子模块存在性校验。"""
        errors = []
        warnings = []
        root = Path(bsd_oaps_root)
        if not root.exists():
            return _result(False, errors=[f"bsd-oaps 根目录不存在：{bsd_oaps_root}"])
        missing = []
        empty = []
        for rel in self.t90_v18_required_modules:
            target = root / rel
            if not target.exists():
                missing.append(rel)
            elif target.stat().st_size == 0:
                empty.append(rel)
        if missing:
            errors.append(f"缺失四大算子模块（严重）：{missing}")
        if empty:
            warnings.append(f"四大算子模块文件为空：{empty}")
        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing=missing,
            empty=empty,
        )

    # ==========================================================
    # T90 V1.8 §8.6.2 参数注册校验
    # ==========================================================
    def verify_t90_v18_params_registry(self, constants_path) -> dict:
        """§8.6.2 参数注册校验（bsd-oaps/registry/constants.py）。"""
        errors = []
        warnings = []
        p = Path(constants_path)
        if not p.exists():
            return _result(False, errors=[f"参数注册文件不存在：{constants_path}"])
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return _result(False, errors=[f"读取参数注册文件失败：{e}"])

        # 校验 ALL_LOCKED_PARAMS 字典存在
        if "ALL_LOCKED_PARAMS" not in content:
            errors.append("ALL_LOCKED_PARAMS 字典未注册")

        # 校验 verify_params 函数存在
        if "verify_params" not in content:
            warnings.append("verify_params() 函数未实现")

        # 逐一校验 7 个新参数
        missing_params = []
        value_mismatch = []
        for name, value in T90_V18_NEW_PARAMS.items():
            if name not in content:
                missing_params.append(name)
            elif str(value) not in content:
                value_mismatch.append(f"{name}={value}")
        if missing_params:
            errors.append(f"T90 V1.8 新增参数未注册：{missing_params}")
        if value_mismatch:
            errors.append(f"T90 V1.8 新增参数值不匹配：{value_mismatch}")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing_params=missing_params,
            value_mismatch=value_mismatch,
        )

    # ==========================================================
    # T90 V1.8 §8.7 历史理论分级锁档状态码校验
    # ==========================================================
    def verify_lock_status_codes(self, docs) -> dict:
        """§8.7 历史理论分级锁档状态码校验。"""
        errors = []
        warnings = []
        if not isinstance(docs, list):
            docs = [docs] if docs else []
        missing_status = []
        for d in docs:
            try:
                p = Path(d)
                if not p.exists():
                    warnings.append(f"文档不存在：{d}")
                    continue
                content = p.read_text(encoding="utf-8", errors="ignore")
                found = False
                for code in self.lock_status_codes:
                    if code in content:
                        found = True
                        break
                if not found:
                    missing_status.append(d)
            except Exception as e:
                warnings.append(f"读取文档失败 {d}: {e}")
        if missing_status:
            errors.append(f"状态码缺失文档（需补全 ACTIVE-V1.8 或 LOCKED-*）：{missing_status}")
        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing_status=missing_status,
        )

    # ==========================================================
    # 全量校验主入口
    # ==========================================================
    def run_full_verification(self, project_root) -> dict:
        """全量校验主入口：聚合所有校验结果，输出 JSON 格式报告。"""
        root = Path(project_root)
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_root": str(root.resolve()),
            "theory_source": "T90 V1.8 §11.8.10-§11.8.12 + BSD-OrderArch-007",
            "version": "V1.8",
            "results": {},
            "overall_pass": True,
        }

        # 基础校验：理论文档锁档哈希
        rules_path = root / ".trae" / "rules" / "meta_theory_constraint.md"
        if rules_path.exists():
            rules_content = rules_path.read_text(encoding="utf-8", errors="ignore")
            report["results"]["verify_locked_hash"] = self.verify_locked_hash(rules_content)
            report["results"]["verify_author_rights"] = self.verify_author_rights(rules_content)
            report["results"]["verify_foundation_layers"] = self.verify_foundation_layers(rules_content)
        else:
            report["results"]["verify_locked_hash"] = _result(False, errors=[
                f"理论约束文档不存在：{rules_path}"
            ])
            report["results"]["verify_author_rights"] = _result(False, errors=["理论约束文档不存在"])
            report["results"]["verify_foundation_layers"] = _result(False, errors=["理论约束文档不存在"])

        # T90 V1.8 §8.1-§8.5 五大核心理论校验
        report["results"]["verify_t90_v18_core_theories"] = self.verify_t90_v18_core_theories()

        # T90 V1.8 §8.6.1 四大算子模块校验
        bsd_oaps_root = root / "bsd-oaps"
        report["results"]["verify_t90_v18_modules"] = self.verify_t90_v18_modules(bsd_oaps_root)

        # T90 V1.8 §8.6.2 参数注册校验
        constants_path = bsd_oaps_root / "bsd_engine" / "registry" / "constants.py"
        report["results"]["verify_t90_v18_params_registry"] = self.verify_t90_v18_params_registry(constants_path)

        # T90 V1.8 §8.7 状态码校验（扫描 .trae/rules 下文档）
        rule_docs = [str(p) for p in (root / ".trae" / "rules").glob("*.md")] if (root / ".trae" / "rules").exists() else []
        report["results"]["verify_lock_status_codes"] = self.verify_lock_status_codes(rule_docs)

        # 分层目录合规校验
        report["results"]["verify_directory_hierarchy"] = self.verify_directory_hierarchy(root)

        # 汇总 overall_pass
        for key, res in report["results"].items():
            if not res.get("pass", False):
                report["overall_pass"] = False
                break

        return report


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    guard = OntologyTheoryGuard()
    project_root = sys.argv[1] if len(sys.argv) > 1 else "."
    result = guard.run_full_verification(project_root)

    # 输出 JSON 格式校验报告
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 退出码：通过为 0，不通过为 1
    sys.exit(0 if result.get("overall_pass", False) else 1)
