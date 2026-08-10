"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·元道本体规则·对偶性体系】
【对应公理：T6 九界对偶定理】

EighteenRealmDualityJudge —— 十八界全域对偶判定器
9界实存 + 9界可能 = 全域18界
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


FORWARD_9 = ["虚无寂灭界", "地府魔界", "物质实体界", "虚拟模态界", "精神意识界", "社会秩序界", "全域统合界", "神仙公理界", "克苏鲁混沌污染界"]
DUAL_9 = [f"对偶·{n}" for n in FORWARD_9]


class EighteenRealmDualityJudge(BaseTheoryModule):
    """十八界全域对偶判定器"""

    module_id = "T32_C04"
    module_name = "十八界全域对偶判定器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·元道本体规则·对偶性体系"
    corresponding_axiom = "T6 九界对偶定理（18界全域）"
    is_origin_locked = True
    dependencies = ["T32", "T30"]

    def __init__(self):
        super().__init__()
        self._forward_realms = FORWARD_9
        self._dual_realms = DUAL_9

    def total_realms(self) -> Dict[str, any]:
        """全域界域总数"""
        return {
            "forward_realms": len(self._forward_realms),
            "dual_realms": len(self._dual_realms),
            "total_realms": len(self._forward_realms) + len(self._dual_realms),
            "theorem": "9界 + 9界 = 全域18界"
        }

    def pair_mapping(self) -> Dict[str, str]:
        """配对映射表"""
        return dict(zip(self._forward_realms, self._dual_realms))

    def total_entropy(self, f_entropies: List[float], d_entropies: List[float]) -> Dict[str, any]:
        """总熵计算"""
        s_f = sum(f_entropies)
        s_d = sum(d_entropies)
        total = s_f + s_d
        return {
            "forward_entropy": s_f,
            "dual_entropy": s_d,
            "total_entropy": total,
            "conserved": abs(total) < self.constants.theta_neg
        }

    def symmetry_check(self, f_weights: List[float], d_weights: List[float]) -> Dict[str, any]:
        """对称检查"""
        if len(f_weights) != 9 or len(d_weights) != 9:
            return {"error": "必须各9个权重"}
        pairs = []
        all_sym = True
        for i in range(9):
            sym = abs(f_weights[i] - d_weights[i]) < self.constants.theta_neg
            pairs.append({"index": i, "forward": f_weights[i], "dual": d_weights[i], "symmetric": sym})
            if not sym:
                all_sym = False
        return {
            "pairs": pairs,
            "all_symmetric": all_sym,
            "symmetry_ratio": sum(1 for p in pairs if p["symmetric"]) / 9
        }

    def realm_crossing_energy(self, from_f: str, to_d: str, energy: float) -> Dict[str, any]:
        """跨界能量（实存↔可能）"""
        # 跨对偶壁垒需要 CPFB + ICPFB 双重穿越
        leakage = energy * 0.05
        return {
            "from_realm": from_f,
            "to_realm": to_d,
            "input_energy": energy,
            "leakage": leakage,
            "actual_transfer": energy - leakage,
            "crossed_dual_barrier": True
        }

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        if len(self._forward_realms) != self.constants.NUM_REALMS:
            errors.append("正向九界必须为9个")
        if len(self._dual_realms) != self.constants.NUM_REALMS:
            errors.append("对偶九界必须为9个")
        return (len(errors) == 0, errors)
