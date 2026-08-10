"""
归属基底：第1重九维法理基底
对应三界秩序：自然
对应公理：公理二（自主科研闭环动力学公理）
对应九维维度：载体实体
理论原文出处：theory_base/L0_总本源层/全域大一统理论/
固定数理常量：γ=0.92、κ=0.35
"""
"""
【归属基底：L0_总本源层·全域双界域隔离壁垒本源】
【对应公理：双界域隔离终极公理·跨界侵染检测】

CrossRealmContaminationDetector —— 跨界侵染检测器
界域侵染、跨界畸变、边界模糊检测
"""

import math
from typing import Dict, List, Tuple
from ..core.base_theory_module import BaseTheoryModule


class ContaminationLevel:
    NONE = "无污染"
    LOW = "轻度污染"
    MEDIUM = "中度污染"
    HIGH = "重度污染"
    CRITICAL = "临界崩溃"


class CrossRealmContaminationDetector(BaseTheoryModule):
    """跨界侵染检测器"""

    module_id = "T30_C04"
    module_name = "跨界侵染检测器"
    version = "V1.0"
    cosmic_level = 0
    base_belong = "L0_总本源层·全域双界域隔离壁垒本源"
    corresponding_axiom = "双界域隔离终极公理·跨界侵染检测"
    is_origin_locked = True
    dependencies = ["T30", "T30_C01", "T30_C02", "T30_C03"]

    def __init__(self):
        super().__init__()
        self._contamination_matrix = {}
        self._thresholds = {
            "low": 0.01,
            "medium": 0.1,
            "high": 0.3,
            "critical": 0.7
        }

    def add_contamination(self, from_realm: str, to_realm: str, amount: float):
        """添加侵染记录"""
        key = f"{from_realm}->{to_realm}"
        self._contamination_matrix[key] = self._contamination_matrix.get(key, 0.0) + amount

    def get_contamination_level(self, realm: str) -> Dict[str, any]:
        """获取指定界域的污染水平"""
        total = 0.0
        sources = []
        for key, val in self._contamination_matrix.items():
            if key.endswith(f"->{realm}"):
                total += val
                sources.append(key)
        level = self._classify(total)
        return {
            "realm": realm,
            "total_contamination": total,
            "level": level,
            "sources": sources
        }

    def _classify(self, value: float) -> str:
        if value < self._thresholds["low"]:
            return ContaminationLevel.NONE
        elif value < self._thresholds["medium"]:
            return ContaminationLevel.LOW
        elif value < self._thresholds["high"]:
            return ContaminationLevel.MEDIUM
        elif value < self._thresholds["critical"]:
            return ContaminationLevel.HIGH
        else:
            return ContaminationLevel.CRITICAL

    def global_contamination_report(self, realms: List[str]) -> Dict[str, any]:
        """全域污染报告"""
        report = {}
        total_global = 0.0
        critical_realms = []
        for realm in realms:
            info = self.get_contamination_level(realm)
            report[realm] = info
            total_global += info["total_contamination"]
            if info["level"] in (ContaminationLevel.HIGH, ContaminationLevel.CRITICAL):
                critical_realms.append(realm)
        return {
            "per_realm": report,
            "total_global_contamination": total_global,
            "critical_realms": critical_realms,
            "global_status": self._classify(total_global / max(len(realms), 1))
        }

    def reset_all(self):
        """重置所有污染"""
        self._contamination_matrix.clear()

    def validate(self) -> Tuple[bool, List[str]]:
        ok, errors = super().validate()
        if not ok:
            return ok, errors
        return (len(errors) == 0, errors)
