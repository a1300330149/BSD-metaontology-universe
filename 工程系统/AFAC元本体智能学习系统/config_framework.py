"""
================================================================================
V3.0 Rev.04 新四位一体框架 - 配置文件
================================================================================
配置参数定义，与框架核心公理保持一致

理论来源：V3.0 Rev.04 四位一体驻波动力学框架
================================================================================
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class FrameworkConfig:
    """框架核心配置"""
    
    # ========================================================================
    # 版本信息
    # ========================================================================
    VERSION: str = "V3.0 Rev.04"
    BUILD_DATE: str = "2026-06-24"
    AUTHOR: str = "杨腾飞"
    AUTHOR_ID: str = "433127199812193215"
    
    # ========================================================================
    # 0元空无基底常量
    # ========================================================================
    ORIGIN_BASE: float = 0.0           # 空无零点基准
    MAX_EMERGENCE_VALUE: float = 100.0  # 全域最高涌现价值
    
    # ========================================================================
    # 五界域定义
    # ========================================================================
    FIVE_DOMAINS: List[str] = None
    
    def __post_init__(self):
        if self.FIVE_DOMAINS is None:
            self.FIVE_DOMAINS = [
                "material_entity",      # 物质实体界
                "virtual_modal",        # 虚拟模态界
                "mental_conscious",     # 精神意识界
                "social_order",         # 社会秩序界
                "global_unify"          # 全域统合界
            ]
    
    # ========================================================================
    # 腾飞四论定义
    # ========================================================================
    FOUR_THEORY: Dict[str, str] = None
    
    def __post_init__(self):
        if self.FOUR_THEORY is None:
            self.FOUR_THEORY = {
                "positive": "稳态建构(可证可证伪)",
                "reverse": "范式解构(可证可证伪)",
                "truth": "全域定型(可证不可证伪)",
                "fallacy": "失效隔离(可证伪不可证)"
            }
    
    # ========================================================================
    # 价值光谱维度
    # ========================================================================
    VALUE_SPECTRUM: List[str] = None
    
    def __post_init__(self):
        if self.VALUE_SPECTRUM is None:
            self.VALUE_SPECTRUM = ["complexity", "diversity", "symbiosis"]
    
    # ========================================================================
    # 权重参数（四论判定）
    # ========================================================================
    WEIGHT_DOMAIN: float = 1.0     # 界域数量权重
    WEIGHT_LAYER: float = 0.6       # 嵌套层级权重
    WEIGHT_SPECTRUM: float = 0.4    # 光谱偏移权重
    
    # ========================================================================
    # 阈值参数（理论分型）
    # ========================================================================
    TRUTH_STEADY_THRESHOLD: float = 0.8   # 真论稳态阈值
    TRUTH_CONFLICT_THRESHOLD: float = 0.2  # 真论冲突阈值
    POSITIVE_STEADY_THRESHOLD: float = 0.5 # 正论稳态阈值
    POSITIVE_CONFLICT_THRESHOLD: float = 0.5 # 正论冲突阈值
    REVERSE_STEADY_THRESHOLD: float = 0.4   # 逆论稳态阈值
    REVERSE_CONFLICT_THRESHOLD: float = 0.4 # 逆论冲突阈值
    
    # ========================================================================
    # 等级划分阈值
    # ========================================================================
    LEVEL_S_THRESHOLD: float = 80.0  # S级阈值
    LEVEL_A_THRESHOLD: float = 60.0  # A级阈值
    LEVEL_B_THRESHOLD: float = 40.0  # B级阈值
    LEVEL_C_THRESHOLD: float = 20.0  # C级阈值
    
    # ========================================================================
    # 四位一体层级
    # ========================================================================
    ENTITY_LAYER: bool = True       # 实体原本体层
    NON_ENTITY_LAYER: bool = True   # 非本体层
    MODAL_LAYER: bool = True        # 模态分划层
    META_MODAL_LAYER: bool = True   # 元模态终局层
    
    # ========================================================================
    # 过滤维度
    # ========================================================================
    FILTER_DIMENSIONS: List[str] = None
    
    def __post_init__(self):
        if self.FILTER_DIMENSIONS is None:
            self.FILTER_DIMENSIONS = [
                "ontology_bound",    # 本体边界
                "steady_screen",     # 稳态筛选
                "paradigm_iter",     # 范式迭代
                "core_lock"          # 核心锁档
            ]
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            'version': self.VERSION,
            'author': self.AUTHOR,
            'origin_base': self.ORIGIN_BASE,
            'max_emergence_value': self.MAX_EMERGENCE_VALUE,
            'five_domains': self.FIVE_DOMAINS,
            'four_theory': self.FOUR_THEORY,
            'value_spectrum': self.VALUE_SPECTRUM,
            'weight_params': {
                'domain': self.WEIGHT_DOMAIN,
                'layer': self.WEIGHT_LAYER,
                'spectrum': self.WEIGHT_SPECTRUM
            },
            'threshold_params': {
                'truth_steady': self.TRUTH_STEADY_THRESHOLD,
                'truth_conflict': self.TRUTH_CONFLICT_THRESHOLD,
                'positive_steady': self.POSITIVE_STEADY_THRESHOLD,
                'positive_conflict': self.POSITIVE_CONFLICT_THRESHOLD,
                'reverse_steady': self.REVERSE_STEADY_THRESHOLD,
                'reverse_conflict': self.REVERSE_CONFLICT_THRESHOLD
            },
            'level_thresholds': {
                'S': self.LEVEL_S_THRESHOLD,
                'A': self.LEVEL_A_THRESHOLD,
                'B': self.LEVEL_B_THRESHOLD,
                'C': self.LEVEL_C_THRESHOLD
            },
            'four_dimension': {
                'entity_layer': self.ENTITY_LAYER,
                'non_entity_layer': self.NON_ENTITY_LAYER,
                'modal_layer': self.MODAL_LAYER,
                'meta_modal_layer': self.META_MODAL_LAYER
            },
            'filter_dimensions': self.FILTER_DIMENSIONS
        }


# 全局配置实例
GLOBAL_CONFIG = FrameworkConfig()
