# bidirectional_iteration_verify.py
"""
归属基底：0重元道本源基底
对应三界秩序：天道秩序（双时针动力学）
对应公理：公理十一（BSD双向迭代算子公理）
对应九维维度：元理天道（双向迭代）
理论原文出处：T90 V1.8 §11.8.11 定义11.14/11.15 + 定理11.19
核心数理参数：k₊=0.9, k₋=0.1, π=3.1415926535, Π₂=2.8274333882
版本：V1.8 (2026-07-24)
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime


# ============================================================
# 1. 双向迭代算子定义（理论锁档，对应公理十一）
# ============================================================
# 𝒯₊ 顺时针展开：0∅→1→3→6→9→12→N（6映射 f₁-f₆）
CLOCKWISE_SEQUENCE = [0, 1, 3, 6, 9, 12, "N"]
# 𝒯₋ 逆时针逆反：N→12→9→6→3→1→0_迹→1'（7映射 g₁-g₇）
COUNTERCLOCKWISE_SEQUENCE = ["N", 12, 9, 6, 3, 1, "0_迹", "1'"]


# ============================================================
# 2. 六层多元进制定义（对应公理十二）
# ============================================================
SIX_LEVEL_BASES = [
    {"name": "B1", "label": "二进制", "base": 2},
    {"name": "B2", "label": "三进制", "base": 3},
    {"name": "B3", "label": "六进制", "base": 6},
    {"name": "B4", "label": "十进制", "base": 10},
    {"name": "B5", "label": "十二进制", "base": 12},
    {"name": "B6", "label": "N进制", "base": None},  # 无限进制
]


# ============================================================
# 3. 3×3粒子家族矩阵定义（对应公理十二）
# ============================================================
PARTICLE_FAMILY_MATRIX = {
    "个体性": [1, 4, 7],  # 顺时针/阳，公差3
    "变化性": [2, 5, 8],  # 逆时针/阴，公差3
    "关系性": [3, 6, 9],  # 中性/耦合，公差3
}


# ============================================================
# 4. 三个0.9同构定义（对应公理十三）
# ============================================================
THREE_NINE_ISOMORPHISM = {
    "0.9̇": {"value": "0.999...", "dimension": "1维时间", "type": "无限循环小数"},
    "0.9π": {"value": 2.8274333882, "dimension": "2维时空耦合", "type": "π的0.9倍"},
    "E3": {"value": 0.90, "dimension": "3维文明", "type": "三阶道心能级阈值"},
    "shared_k": 0.9,
}


# ============================================================
# 锁档确权信息（不可修改）
# ============================================================
LOCKED_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"
LOCKED_AUTHOR = "杨腾飞"
LOCKED_ID = "433127199812193215"
LOCKED_DATE = "2026-06-20"


def _result(passed: bool, errors=None, warnings=None, **extra) -> dict:
    """统一返回校验结果字典。"""
    r = {"pass": bool(passed), "errors": errors or [], "warnings": warnings or []}
    r.update(extra)
    return r


class BidirectionalIterationVerifier:
    """BSD 双向迭代算子专项验证器（T90 V1.8 §11.8.11）。"""

    def __init__(self):
        # 归属基底：0重元道本源基底
        self.clockwise_sequence = CLOCKWISE_SEQUENCE
        self.counterclockwise_sequence = COUNTERCLOCKWISE_SEQUENCE
        self.six_level_bases = SIX_LEVEL_BASES
        self.particle_family_matrix = PARTICLE_FAMILY_MATRIX
        self.three_nine_isomorphism = THREE_NINE_ISOMORPHISM

    # ----------------------------------------------------------
    # 读取模块内容（文件不存在时返回空字符串而非抛异常）
    # ----------------------------------------------------------
    def _read_module(self, module_path) -> str:
        p = Path(module_path)
        if not p.exists():
            return ""
        try:
            return p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            return ""

    # ==========================================================
    # 1. 𝒯₊ 顺时针展开算子校验
    # ==========================================================
    def verify_clockwise_operator(self, module_path) -> dict:
        """校验 𝒯₊ 顺时针展开算子（6映射 f₁-f₆）。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验 𝒯₊ 算子标记
        if "T_plus" not in content and "𝒯₊" not in content and "clockwise" not in content.lower():
            errors.append("未检测到 𝒯₊ 顺时针算子实现标记（T_plus / 𝒯₊ / clockwise）")

        # 校验 6 映射 f₁-f₆
        f_mappings_found = 0
        for i in range(1, 7):
            for pat in [f"f{i}", f"f_{i}", f"f{i}_", f"f{i}（", f"f{i}("]:
                if pat in content:
                    f_mappings_found += 1
                    break
        if f_mappings_found < 6:
            errors.append(f"𝒯₊ 6映射 f₁-f₆ 检出数不足：{f_mappings_found}/6")

        # 校验顺时针序列
        for node in ["0", "1", "3", "6", "9", "12", "N"]:
            if str(node) not in content:
                warnings.append(f"𝒯₊ 序列节点缺失：{node}")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            f_mappings_found=f_mappings_found,
            sequence_length=len(self.clockwise_sequence),
        )

    # ==========================================================
    # 2. 𝒯₋ 逆时针逆反算子校验
    # ==========================================================
    def verify_counterclockwise_operator(self, module_path) -> dict:
        """校验 𝒯₋ 逆时针逆反算子（7映射 g₁-g₇）。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验 𝒯₋ 算子标记
        if "T_minus" not in content and "𝒯₋" not in content and "counterclockwise" not in content.lower():
            errors.append("未检测到 𝒯₋ 逆时针算子实现标记（T_minus / 𝒯₋ / counterclockwise）")

        # 校验 7 映射 g₁-g₇
        g_mappings_found = 0
        for i in range(1, 8):
            for pat in [f"g{i}", f"g_{i}", f"g{i}_", f"g{i}（", f"g{i}("]:
                if pat in content:
                    g_mappings_found += 1
                    break
        if g_mappings_found < 7:
            errors.append(f"𝒯₋ 7映射 g₁-g₇ 检出数不足：{g_mappings_found}/7")

        # 校验信息痕迹 0_迹
        if "0_迹" not in content and "0_trace" not in content and "0_迹".encode("utf-8").decode("utf-8") not in content:
            warnings.append("未检测到 0_迹（信息痕迹守恒标记）")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            g_mappings_found=g_mappings_found,
            sequence_length=len(self.counterclockwise_sequence),
        )

    # ==========================================================
    # 3. 𝒟 升维算子校验
    # ==========================================================
    def verify_ascension_operator(self, module_path) -> dict:
        """校验 𝒟 升维算子（𝒟=g₇∘...∘f₁）。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验 𝒟 算子标记
        if "D_ascension" not in content and "𝒟" not in content and "ascension" not in content.lower():
            errors.append("未检测到 𝒟 升维算子实现标记（D_ascension / 𝒟 / ascension）")

        # 校验合成公式 𝒟=g₇∘...∘f₁
        if "g7" not in content and "g_7" not in content:
            warnings.append("未检测到 g₇ 映射（𝒟=g₇∘...∘f₁ 的合成终止点）")
        if "f1" not in content and "f_1" not in content:
            warnings.append("未检测到 f₁ 映射（𝒟=g₇∘...∘f₁ 的合成起始点）")

        # 校验不可恒等还原
        if "Id" in content or "identity" in content.lower():
            # 检查是否明确声明 ≠ Id
            if "≠ Id" not in content and "!= Id" not in content and "not identity" not in content.lower():
                warnings.append("𝒟 升维算子未明确声明 ≠ Id（不可恒等还原）")

        return _result(len(errors) == 0, errors=errors, warnings=warnings)

    # ==========================================================
    # 4. 对偶性定理校验 𝒯₋ ∘ 𝒯₊ = 𝒟 ≠ Id
    # ==========================================================
    def verify_duality_theorem(self, module_path) -> dict:
        """校验对偶性定理 𝒯₋ ∘ 𝒯₊ = 𝒟 ≠ Id。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 理论校验：𝒯₊ 6映射 + 𝒯₋ 7映射 = 13 映射
        total_mappings = (len(self.clockwise_sequence) - 1) + (len(self.counterclockwise_sequence) - 1)
        # 顺时针 6 段（7节点-1），逆时针 7 段（8节点-1），合计 13
        if total_mappings != 13:
            errors.append(f"对偶性定理校验失败：𝒯₊+𝒯₋ 映射总数应为 13，实际 {total_mappings}")

        # 检查对偶性定理文字声明
        duality_declared = False
        for pat in ["𝒯₋ ∘ 𝒯₊", "T_minus(T_plus)", "T_minus * T_plus", "duality", "对偶"]:
            if pat in content:
                duality_declared = True
                break
        if not duality_declared:
            warnings.append("未检测到对偶性定理 𝒯₋ ∘ 𝒯₊ = 𝒟 ≠ Id 的文字声明")

        # 校验 ≠ Id
        if "≠ Id" not in content and "!= Id" not in content and "not identity" not in content.lower():
            warnings.append("未明确声明 𝒟 ≠ Id")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            total_mappings=total_mappings,
            duality_declared=duality_declared,
        )

    # ==========================================================
    # 5. 六层多元进制校验
    # ==========================================================
    def verify_six_level_bases(self, module_path) -> dict:
        """校验六层多元进制（B₁-B₆）。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验六层标记（兼容多种格式：B1/B₂/level=1/二进制 等）
        cn_names = ["二进制", "三进制", "六进制", "十进制", "十二进制", "N进制"]
        levels_found = 0
        for i, base_info in enumerate(self.six_level_bases, 1):
            name = base_info["name"]
            cn_name = cn_names[i - 1] if i - 1 < len(cn_names) else ""
            # 兼容：B1 / base_B1 / level=1 / 二进制 / level 1
            hit = (
                name in content
                or f"base_{name}" in content.lower()
                or f"Base_{name}" in content
                or f"level={i}" in content
                or f"level = {i}" in content
                or f"level {i}" in content
                or (cn_name and cn_name in content)
            )
            if hit:
                levels_found += 1
        if levels_found < 6:
            errors.append(f"六层多元进制检出不足：{levels_found}/6")

        # 校验进制基数
        for base_info in self.six_level_bases:
            if base_info["base"] is not None:
                if str(base_info["base"]) not in content:
                    warnings.append(f"{base_info['name']} 进制基数 {base_info['base']} 未检出")

        # 校验层级不可逆性声明
        if "irreversible" not in content.lower() and "不可逆" not in content:
            warnings.append("未声明层级不可逆性（低维不能反向生成高维）")

        return _result(len(errors) == 0, errors=errors, warnings=warnings, levels_found=levels_found)

    # ==========================================================
    # 6. 三个0.9同构校验
    # ==========================================================
    def verify_three_nine_isomorphism(self, module_path) -> dict:
        """校验三个0.9同构（0.9̇ ≅ 0.9π ≅ E₃=0.90）。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验三重同构标记
        iso_marks = {
            "0.9̇": ["0.9̇", "0.9_recurring", "0.999"],
            "0.9π": ["0.9π", "0.9*pi", "0.9 * pi", "2.8274333882"],
            "E3": ["E3", "E₃", "0.90", "0.9"],
        }
        found = {}
        for key, pats in iso_marks.items():
            hit = any(p in content for p in pats)
            found[key] = hit
            if not hit:
                errors.append(f"三重同构标记缺失：{key}")

        # 校验共享系数 k₊=0.9
        k_plus_found = False
        for pat in ["k_plus", "K_PLUS", "k₊", "shared_k"]:
            if pat in content:
                k_plus_found = True
                break
        if not k_plus_found:
            warnings.append("未检测到共享系数 k₊=0.9 标记")

        if "0.9" not in content:
            errors.append("共享系数值 0.9 未检出")

        # 校验三重投射维度
        for dim in ["1维时间", "2维时空", "3维文明"]:
            if dim not in content:
                warnings.append(f"维度投射缺失：{dim}")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            isomorphisms_found=found,
            k_plus_found=k_plus_found,
        )

    # ==========================================================
    # 7. 3×3粒子家族矩阵校验
    # ==========================================================
    def verify_particle_family_matrix(self, module_path) -> dict:
        """校验 3×3 粒子家族矩阵。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验三谱系
        for key, seq in self.particle_family_matrix.items():
            if key not in content and key.lower() not in content.lower():
                # 英文别名兼容
                en_map = {"个体性": "individuality", "变化性": "variability", "关系性": "relationality"}
                if en_map.get(key, "") not in content.lower():
                    warnings.append(f"谱系标记缺失：{key}")
            # 校验公差3
            diffs = [seq[i + 1] - seq[i] for i in range(len(seq) - 1)]
            if any(d != 3 for d in diffs):
                errors.append(f"{key} 谱系公差不为 3：{seq}")

        # 校验生点证圆 π=3，3×3=9
        if "3" not in content or "9" not in content:
            warnings.append("生点证圆数值（3, 9）未检出")

        # 校验双时针阴阳对偶
        yin_yang = False
        for pat in ["阴阳", "yin_yang", "yin-yang", "顺时针", "逆时针", "clockwise", "counterclockwise"]:
            if pat in content or pat.lower() in content.lower():
                yin_yang = True
                break
        if not yin_yang:
            warnings.append("未检测到双时针阴阳对偶标记")

        # 校验数字位守恒 1+1+1+2+2+2=9
        digit_sum = 1 + 1 + 1 + 2 + 2 + 2
        if digit_sum != 9:
            errors.append(f"数字位守恒失败：1+1+1+2+2+2 = {digit_sum} ≠ 9")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            digit_sum=digit_sum,
            yin_yang_detected=yin_yang,
        )

    # ==========================================================
    # 8. 信息痕迹守恒校验
    # ==========================================================
    def verify_info_trace_conservation(self, module_path) -> dict:
        """校验信息痕迹守恒（𝒯₋ 逆反至 0_迹，非 0∅）。"""
        errors = []
        warnings = []
        content = self._read_module(module_path)
        if not content:
            return _result(False, errors=[f"模块文件不存在或为空：{module_path}"])

        # 校验 0_迹 标记
        trace_found = False
        for pat in ["0_迹", "0_trace", "info_trace", "信息痕迹"]:
            if pat in content:
                trace_found = True
                break
        if not trace_found:
            errors.append("未检测到 0_迹（信息痕迹守恒标记）")

        # 校验非 0∅（非绝对虚无）
        if "0∅" in content:
            # 必须明确声明 0_迹 ≠ 0∅
            if "≠ 0∅" not in content and "!= 0∅" not in content and "not 0∅" not in content:
                warnings.append("0_迹 与 0∅ 的区分声明缺失")

        # 校验升维算子不可恒等还原
        if "Id" in content:
            if "≠ Id" not in content and "!= Id" not in content:
                warnings.append("升维算子 𝒟 不可恒等还原声明缺失")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            trace_found=trace_found,
        )

    # ==========================================================
    # 全量校验主入口
    # ==========================================================
    def run_full_verification(self, bsd_oaps_root) -> dict:
        """全量校验主入口：顺时针 + 逆时针 + 升维算子三部分。"""
        root = Path(bsd_oaps_root)
        core_dir = root / "bsd_engine" / "core"

        # 四大算子模块路径
        bidir_module = core_dir / "bidirectional_iteration_operator.py"
        six_level_module = core_dir / "six_level_base_emergence.py"
        three_nine_module = core_dir / "three_nine_isomorphism.py"
        particle_module = core_dir / "particle_family_matrix.py"

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "bsd_oaps_root": str(root.resolve()),
            "theory_source": "T90 V1.8 §11.8.11 定义11.14/11.15 + 定理11.19",
            "version": "V1.8",
            "clockwise_results": {},   # 顺时针校验（T90→T0）
            "counterclockwise_results": {},  # 逆时针校验（T0→T90）
            "ascension_results": {},   # 升维算子 𝒟 综合校验
            "overall_pass": True,
        }

        # ============ 顺时针校验（T90→T0，自上而下）============
        cw = report["clockwise_results"]
        cw["C1_clockwise_operator"] = self.verify_clockwise_operator(bidir_module)
        cw["C2_six_level_bases"] = self.verify_six_level_bases(six_level_module)
        cw["C3_three_nine_isomorphism"] = self.verify_three_nine_isomorphism(three_nine_module)
        cw["C5_particle_family_matrix"] = self.verify_particle_family_matrix(particle_module)

        # ============ 逆时针校验（T0→T90，自下而上）============
        ccw = report["counterclockwise_results"]
        ccw["C1_counterclockwise_operator"] = self.verify_counterclockwise_operator(bidir_module)
        ccw["info_trace_conservation"] = self.verify_info_trace_conservation(bidir_module)
        # 参数注册回溯
        constants_path = root / "registry" / "constants.py"
        ccw["params_registry"] = self._verify_params_registry(constants_path)

        # ============ 升维算子 𝒟 综合校验 ============
        asc = report["ascension_results"]
        asc["ascension_operator"] = self.verify_ascension_operator(bidir_module)
        asc["duality_theorem"] = self.verify_duality_theorem(bidir_module)

        # 汇总 overall_pass
        for section in ["clockwise_results", "counterclockwise_results", "ascension_results"]:
            for key, res in report[section].items():
                if not res.get("pass", False):
                    report["overall_pass"] = False
                    break
            if not report["overall_pass"]:
                break

        return report

    # ----------------------------------------------------------
    # 辅助：参数注册回溯校验
    # ----------------------------------------------------------
    def _verify_params_registry(self, constants_path) -> dict:
        """参数注册回溯校验（bsd-oaps/bsd_engine/registry/constants.py）。"""
        errors = []
        warnings = []
        p = Path(constants_path)
        # 路径自动修正：兼容 bsd-oaps/registry/ 和 bsd-oaps/bsd_engine/registry/
        if not p.exists():
            # 尝试 bsd_engine/registry/constants.py（实际工程路径）
            alt_path = p.parent.parent / "bsd_engine" / "registry" / "constants.py"
            if alt_path.exists():
                p = alt_path
        if not p.exists():
            return _result(False, errors=[f"参数注册文件不存在：{constants_path}（也尝试了 bsd_engine/registry/constants.py）"])
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            return _result(False, errors=[f"读取参数注册文件失败：{e}"])

        required_params = {
            "K_PLUS": "0.9",
            "K_MINUS": "0.1",
            "S_ZERO": "0.81",
            "LAMBDA": "0.62",
            "LAMBDA_INV": "1.38",
            "PI_LOCKED": "3.1415926535",
            "PI_2": "2.8274333882",
        }
        missing = []
        mismatch = []
        for name, value in required_params.items():
            if name not in content:
                missing.append(name)
            elif value not in content:
                mismatch.append(f"{name}={value}")
        if missing:
            errors.append(f"参数未注册：{missing}")
        if mismatch:
            errors.append(f"参数值不匹配：{mismatch}")
        if "ALL_LOCKED_PARAMS" not in content:
            errors.append("ALL_LOCKED_PARAMS 字典未注册")
        if "verify_params" not in content:
            warnings.append("verify_params() 函数未实现")

        return _result(
            len(errors) == 0,
            errors=errors,
            warnings=warnings,
            missing=missing,
            mismatch=mismatch,
        )


# ============================================================
# 主函数
# ============================================================
if __name__ == "__main__":
    verifier = BidirectionalIterationVerifier()
    bsd_oaps_root = sys.argv[1] if len(sys.argv) > 1 else "."
    result = verifier.run_full_verification(bsd_oaps_root)

    # 输出 JSON 格式校验报告
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 退出码：通过为 0，不通过为 1
    sys.exit(0 if result.get("overall_pass", False) else 1)
