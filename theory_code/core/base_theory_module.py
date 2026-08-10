"""
【归属基底：L0_总本源层·0元本体论大一统】
【对应公理：公理0·元道存在】

BaseTheoryModule —— 所有理论模块的统一基类
遵循「四位一体驻波动力学框架本源知识库」顶层约束
继承自 V3.0 Rev.04 终版确权稿，SHA256 主锁保持一致
"""

import hashlib
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Tuple


@dataclass
class TheoryLockInfo:
    """理论锁档信息 —— 继承自主锁，不可修改"""
    work_full_name: str = "V3.0 Rev.04 新四位一体框架 3.0 元本体论（专属理论分册）"
    main_sha256: str = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"
    author: str = "杨腾飞"
    author_id: str = "433127199812193215"
    three_dim_rights: Dict[str, float] = field(default_factory=lambda: {
        "creation_author": 0.60,
        "moxin_deduction": 0.25,
        "doubao_operation": 0.15
    })
    lock_date: str = "2026-06-20"


@dataclass
class CoreConstants:
    """全域核心常量 —— 铁律不可修改"""
    E1: float = 0.35
    E2: float = 0.65
    E3: float = 0.90
    kappa: float = 0.35
    gamma: float = 0.92
    alpha: float = 0.18
    theta_neg: float = 0.02
    theta_mv: float = 0.005
    theta_evo: float = 0.002
    DIM_MATRIX: int = 54
    NUM_REALMS: int = 9
    NUM_SIX_SYS: int = 6


class BaseTheoryModule:
    """
    所有理论模块的统一基类
    
    设计原则：
    1. 所有理论模块必须继承本基类
    2. 层级 ≤ 1 的本源理论必须计算 SHA256 并锁定
    3. 必须声明归属基底和对应公理
    4. 必须实现 validate() 自检方法
    """

    # 子类必须覆盖的属性
    module_id: str = "BASE"
    module_name: str = "基类理论模块"
    version: str = "V1.0"
    cosmic_level: int = 4  # 0=L0本源, 1=L1母科, 2=L2无限之子, 3=L3应用, 4=待确认
    base_belong: str = "待确认"  # 归属基底
    corresponding_axiom: str = "待确认"  # 对应公理
    is_origin_locked: bool = False  # 是否本源锁定（level≤1必须为True）
    dependencies: List[str] = field(default_factory=list)  # 依赖的理论模块ID
    _sha256_lock: Optional[str] = None  # 锁档哈希

    def __init__(self):
        self.lock_info = TheoryLockInfo()
        self.constants = CoreConstants()
        self._registered = False
        if self.is_origin_locked:
            self._compute_lock_hash()

    def _compute_lock_hash(self) -> str:
        """计算理论模块的锁档SHA256哈希（仅本源层级使用）"""
        content = f"{self.module_id}|{self.module_name}|{self.version}|{self.cosmic_level}"
        content += f"|{self.base_belong}|{self.corresponding_axiom}"
        content += f"|{self.lock_info.main_sha256}"
        h = hashlib.sha256(content.encode('utf-8')).hexdigest()
        self._sha256_lock = h
        return h

    @property
    def sha256(self) -> Optional[str]:
        """获取锁档哈希"""
        return self._sha256_lock

    def validate(self) -> Tuple[bool, List[str]]:
        """
        理论自检验证 —— 子类必须实现
        返回 (是否通过, 错误信息列表)
        """
        errors = []
        if not self.module_id or self.module_id == "BASE":
            errors.append("module_id 未设置")
        if not self.module_name:
            errors.append("module_name 未设置")
        if self.base_belong == "待确认":
            errors.append("base_belong 未设置")
        if self.corresponding_axiom == "待确认":
            errors.append("corresponding_axiom 未设置")
        if self.cosmic_level <= 1 and not self.is_origin_locked:
            errors.append(f"L{self.cosmic_level} 本源理论必须锁定（is_origin_locked=True）")
        if self.is_origin_locked and not self._sha256_lock:
            errors.append("本源理论缺少锁档哈希")
        return (len(errors) == 0, errors)

    def get_info(self) -> Dict[str, Any]:
        """获取理论模块信息"""
        return {
            "module_id": self.module_id,
            "module_name": self.module_name,
            "version": self.version,
            "cosmic_level": f"L{self.cosmic_level}",
            "base_belong": self.base_belong,
            "corresponding_axiom": self.corresponding_axiom,
            "is_origin_locked": self.is_origin_locked,
            "sha256": self._sha256_lock,
            "dependencies": self.dependencies,
            "author": self.lock_info.author,
            "three_dim_rights": self.lock_info.three_dim_rights
        }

    def to_json(self) -> str:
        """序列化为JSON"""
        return json.dumps(self.get_info(), ensure_ascii=False, indent=2)

    def __repr__(self) -> str:
        return f"[{self.module_id}] {self.module_name} (L{self.cosmic_level})"
