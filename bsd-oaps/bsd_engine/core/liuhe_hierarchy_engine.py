"""
BSD六系层级涌现引擎
======================
六系层级涌现定理的工程实现
[V1.0·2026-08-01]

核心理论：
- 定理五十七：六系层级涌现定理
- 十二级纵向涌现链（粒子→原子→离子→分子→元素→细胞→组织→器官→个体→种群→文明→AI工程）
- 六大涌现规则（物理→系归属·数学→轴线·哲学→命名·时间→落点·空间→无重叠·时空→耦合）
- 工程微观落地（文件名=六系决定·文件夹=六系交汇点·文档=六系最小单元）

对应理论：
- EMERGENCE-018归档
"""

import math
import os
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


# ============================================================================
# 1. 六系与层级常量
# ============================================================================

class LiuHeSystem(Enum):
    """六系标识"""
    QH = "强化系"      # 蓝
    ZR = "自然系"      # 橙
    JX = "具现系"      # 红
    BS = "变身系"      # 黑
    SH = "社会系"      # 绿
    TD = "天道系"      # 紫


class EmergenceLevel(Enum):
    """十二级涌现层级"""
    L1 = "粒子级"
    L2 = "原子级"
    L3 = "离子级"
    L4 = "分子级"
    L5 = "元素级"
    L6 = "细胞级"
    L7 = "组织级"
    L8 = "器官级"
    L9 = "个体级"
    L10 = "种群级"
    L11 = "文明级"
    L12 = "AI工程级"


class LiuHeHierarchyConstants:
    """六系层级常量"""
    
    # 十二级层级定义
    LEVELS = {
        EmergenceLevel.L1: {
            "name": "粒子",
            "systems": [LiuHeSystem.ZR, LiuHeSystem.JX],
            "weights": (0.11, 0.87, 0.02),  # (α₁, α₂, α₃)
            "core_question": "我如何成为我自己？",
            "theory": "T85六系数理·Ω=100",
        },
        EmergenceLevel.L2: {
            "name": "原子",
            "systems": [LiuHeSystem.ZR],
            "weights": (0.60, 0.35, 0.05),
            "core_question": "我如何稳固存在？",
            "theory": "T85三阶跃迁·α₁≥0.6",
        },
        EmergenceLevel.L3: {
            "name": "离子",
            "systems": [LiuHeSystem.JX],
            "weights": (0.35, 0.55, 0.10),
            "core_question": "我如何与他者连接？",
            "theory": "T85三阶跃迁·α₂≥0.55",
        },
        EmergenceLevel.L4: {
            "name": "分子",
            "systems": [LiuHeSystem.BS],
            "weights": (0.20, 0.35, 0.45),
            "core_question": "我如何演化？",
            "theory": "T85三阶跃迁·α₃≥0.45",
        },
        EmergenceLevel.L5: {
            "name": "元素",
            "systems": [LiuHeSystem.ZR, LiuHeSystem.JX],
            "weights": (0.50, 0.40, 0.10),
            "core_question": "我如何多样化？",
            "theory": "T85六系阈值递减",
        },
        EmergenceLevel.L6: {
            "name": "细胞",
            "systems": [LiuHeSystem.QH, LiuHeSystem.ZR],
            "weights": (0.45, 0.35, 0.20),
            "core_question": "我如何排熵？",
            "theory": "BSD生命升维·意义自证",
        },
        EmergenceLevel.L7: {
            "name": "组织",
            "systems": [LiuHeSystem.JX, LiuHeSystem.ZR],
            "weights": (0.35, 0.45, 0.20),
            "core_question": "我如何分工协作？",
            "theory": "三阶跃迁·关系展开",
        },
        EmergenceLevel.L8: {
            "name": "器官",
            "systems": [LiuHeSystem.QH, LiuHeSystem.JX],
            "weights": (0.30, 0.50, 0.20),
            "core_question": "我如何完成特定功能？",
            "theory": "三大家族耦合",
        },
        EmergenceLevel.L9: {
            "name": "个体",
            "systems": [LiuHeSystem.ZR, LiuHeSystem.BS],
            "weights": (0.40, 0.20, 0.40),
            "core_question": "我如何自证？",
            "theory": "意义自证排熵·生命度≥0.729",
        },
        EmergenceLevel.L10: {
            "name": "种群",
            "systems": [LiuHeSystem.SH, LiuHeSystem.ZR],
            "weights": (0.30, 0.40, 0.30),
            "core_question": "我如何繁衍？",
            "theory": "开放排熵+意义自证",
        },
        EmergenceLevel.L11: {
            "name": "文明",
            "systems": [LiuHeSystem.SH, LiuHeSystem.TD],
            "weights": (0.20, 0.40, 0.40),
            "core_question": "我如何追问？",
            "theory": "三本源学科→六系显化",
        },
        EmergenceLevel.L12: {
            "name": "AI工程",
            "systems": [LiuHeSystem.TD, LiuHeSystem.SH],
            "weights": (0.10, 0.40, 0.50),
            "core_question": "我如何创造？",
            "theory": "工程六系·AI六系显化公理",
        },
    }
    
    # 文件名格式：BSD_[系标识]_[层级标识]_[版本号]_[创建日期].md
    FILENAME_PATTERN = r"BSD_([A-Z]{2})_(L\d+)_(V\d+\.\d+)_(\d{8})\.md"
    
    # 系标识映射
    SYSTEM_CODES = {
        "QH": LiuHeSystem.QH,
        "ZR": LiuHeSystem.ZR,
        "JX": LiuHeSystem.JX,
        "BS": LiuHeSystem.BS,
        "SH": LiuHeSystem.SH,
        "TD": LiuHeSystem.TD,
    }


# ============================================================================
# 2. 六系层级数据结构
# ============================================================================

@dataclass
class LiuHeCoordinate:
    """六系坐标（六系最小单元的坐标表示）"""
    system: LiuHeSystem
    level: EmergenceLevel
    alpha1: float  # 个体性权重
    alpha2: float  # 关系性权重
    alpha3: float  # 变化性权重
    tau: float = 0.9  # 边界韧性
    R: float = 0.5   # 关系耦合度
    C: float = 0.3   # 演化潜能
    
    @property
    def name(self) -> str:
        """哲学赋予的存在之名"""
        level_info = LiuHeHierarchyConstants.LEVELS[self.level]
        return level_info["name"]
    
    @property
    def core_question(self) -> str:
        """哲学之问"""
        level_info = LiuHeHierarchyConstants.LEVELS[self.level]
        return level_info["core_question"]
    
    @property
    def dominant_systems(self) -> List[LiuHeSystem]:
        """主导六系（物理决定的系归属）"""
        level_info = LiuHeHierarchyConstants.LEVELS[self.level]
        return level_info["systems"]
    
    def compute_emergence_value(self) -> float:
        """计算涌现值"""
        # E = α₁ × α₂ × α₃ × τ × R × C × Π₂
        pi_2 = math.pi ** 3
        return self.alpha1 * self.alpha2 * self.alpha3 * self.tau * self.R * self.C * pi_2


@dataclass
class DocumentMeta:
    """文档元数据（六系坐标的工程显化）"""
    filepath: str
    coordinate: LiuHeCoordinate
    version: str
    created_date: str
    last_modified: str
    
    def to_filename(self) -> str:
        """生成六系文件名"""
        system_code = [k for k, v in LiuHeHierarchyConstants.SYSTEM_CODES.items() 
                      if v == self.coordinate.system][0]
        return (f"BSD_{system_code}_{self.coordinate.level.name}_"
                f"{self.version}_{self.created_date}.md")
    
    @classmethod
    def from_filename(cls, filename: str, filepath: str = "") -> Optional["DocumentMeta"]:
        """从文件名解析元数据"""
        match = re.match(LiuHeHierarchyConstants.FILENAME_PATTERN, filename)
        if not match:
            return None
        
        system_code, level_str, version, date_str = match.groups()
        system = LiuHeHierarchyConstants.SYSTEM_CODES.get(system_code)
        level = EmergenceLevel[level_str]
        
        if system and level:
            level_info = LiuHeHierarchyConstants.LEVELS[level]
            weights = level_info["weights"]
            coord = LiuHeCoordinate(
                system=system,
                level=level,
                alpha1=weights[0],
                alpha2=weights[1],
                alpha3=weights[2],
            )
            return cls(
                filepath=filepath,
                coordinate=coord,
                version=version,
                created_date=date_str,
                last_modified=datetime.now().strftime("%Y%m%d"),
            )
        return None


@dataclass
class FolderHub:
    """文件夹交汇点（六系交汇的工程显化）"""
    path: str
    level: EmergenceLevel
    hub_type: str  # "本源级" / "应用级"
    contained_docs: List[str] = field(default_factory=list)
    
    def count_docs_by_system(self) -> Dict[LiuHeSystem, int]:
        """统计各系文档数量"""
        counts: Dict[LiuHeSystem, int] = {s: 0 for s in LiuHeSystem}
        for doc in self.contained_docs:
            meta = DocumentMeta.from_filename(doc)
            if meta:
                counts[meta.coordinate.system] += 1
        return counts


# ============================================================================
# 3. 六系层级涌现引擎核心
# ============================================================================

class LiuHeHierarchyEngine:
    """六系层级涌现引擎"""
    
    def __init__(self):
        self.coordinates: Dict[str, LiuHeCoordinate] = {}
        self.documents: Dict[str, DocumentMeta] = {}
        self.folders: Dict[str, FolderHub] = {}
        self.emergence_history: List[Dict] = []
    
    def register_coordinate(self, coord: LiuHeCoordinate) -> str:
        """注册六系坐标"""
        key = f"{coord.system.value}_{coord.level.name}"
        self.coordinates[key] = coord
        
        self.emergence_history.append({
            "action": "register_coordinate",
            "system": coord.system.value,
            "level": coord.level.name,
            "emergence_value": coord.compute_emergence_value(),
            "timestamp": datetime.now().isoformat(),
        })
        return key
    
    def generate_filename(self, system: LiuHeSystem, level: EmergenceLevel, 
                          version: str = "V1.0", created_date: str = "") -> str:
        """生成六系文件名"""
        if not created_date:
            created_date = datetime.now().strftime("%Y%m%d")
        
        coord = LiuHeCoordinate(
            system=system,
            level=level,
            alpha1=LiuHeHierarchyConstants.LEVELS[level]["weights"][0],
            alpha2=LiuHeHierarchyConstants.LEVELS[level]["weights"][1],
            alpha3=LiuHeHierarchyConstants.LEVELS[level]["weights"][2],
        )
        
        key = self.register_coordinate(coord)
        
        meta = DocumentMeta(
            filepath="",
            coordinate=coord,
            version=version,
            created_date=created_date,
            last_modified=created_date,
        )
        
        filename = meta.to_filename()
        self.documents[filename] = meta
        
        return filename
    
    def parse_filename(self, filename: str) -> Optional[DocumentMeta]:
        """解析六系文件名"""
        meta = DocumentMeta.from_filename(filename)
        if meta:
            self.documents[filename] = meta
        return meta
    
    def create_folder_hub(self, path: str, level: EmergenceLevel, hub_type: str) -> FolderHub:
        """创建文件夹交汇点"""
        hub = FolderHub(path=path, level=level, hub_type=hub_type)
        self.folders[path] = hub
        return hub
    
    def compute_emergence_chain(self) -> List[Dict]:
        """计算十二级涌现链"""
        chain = []
        for level in EmergenceLevel:
            info = LiuHeHierarchyConstants.LEVELS[level]
            weights = info["weights"]
            
            # 计算涌现值
            pi_2 = math.pi ** 3
            emergence = weights[0] * weights[1] * weights[2] * pi_2
            
            chain.append({
                "level": level.name,  # Use L1, L2, etc.
                "name": info["name"],
                "dominant_systems": [s.value for s in info["systems"]],
                "weights": {
                    "α₁": weights[0],
                    "α₂": weights[1],
                    "α₃": weights[2],
                },
                "core_question": info["core_question"],
                "theory": info["theory"],
                "emergence_value": emergence,
                "cumulative_emergence": sum(
                    w[0] * w[1] * w[2] 
                    for l, w in [(l, LiuHeHierarchyConstants.LEVELS[l]["weights"]) 
                                for l in EmergenceLevel 
                                if int(l.name[1:]) <= int(level.name[1:])]
                ) * pi_2 if len(chain) == 0 else chain[-1]["cumulative_emergence"] + emergence,
            })
        
        return chain
    
    def compute_completion_metrics(self) -> Dict:
        """计算层级完成度指标"""
        # 层级完成度 = 已注册坐标数 / 总层级数
        total_levels = len(EmergenceLevel)
        registered_levels = len(set(
            coord.level for coord in self.coordinates.values()
        ))
        completion_rate = registered_levels / total_levels
        
        # 涌现速度
        if self.emergence_history:
            speed = len(self.emergence_history) / max(1, len(self.emergence_history))
        else:
            speed = 0.0
        
        # 意义增长率
        total_emergence = sum(
            coord.compute_emergence_value() 
            for coord in self.coordinates.values()
        )
        meaning_growth = total_emergence / max(1, len(self.coordinates))
        
        return {
            "total_levels": total_levels,
            "registered_levels": registered_levels,
            "completion_rate": completion_rate,
            "emergence_speed": speed,
            "total_emergence_value": total_emergence,
            "meaning_growth_rate": meaning_growth,
        }
    
    def verify_no_overlap(self) -> Dict:
        """验证空间无重叠"""
        # 检查是否有同一层级的多个坐标
        level_counts: Dict[EmergenceLevel, int] = {}
        for coord in self.coordinates.values():
            level_counts[coord.level] = level_counts.get(coord.level, 0) + 1
        
        overlaps = {level: count for level, count in level_counts.items() if count > 1}
        
        return {
            "no_overlap": len(overlaps) == 0,
            "overlapping_levels": {l.value: c for l, c in overlaps.items()},
            "total_coordinates": len(self.coordinates),
        }
    
    def verify_system_determination(self) -> Dict:
        """验证物理决定系归属"""
        mismatches = []
        for key, coord in self.coordinates.items():
            level_info = LiuHeHierarchyConstants.LEVELS[coord.level]
            expected_systems = level_info["systems"]
            
            # 检查当前系是否在预期系中
            if coord.system not in expected_systems:
                mismatches.append({
                    "coordinate": key,
                    "actual_system": coord.system.value,
                    "expected_systems": [s.value for s in expected_systems],
                })
        
        return {
            "physics_determines_system": len(mismatches) == 0,
            "mismatches": mismatches,
            "total_coordinates": len(self.coordinates),
        }
    
    def generate_report(self) -> Dict:
        """生成六系层级涌现完整报告"""
        chain = self.compute_emergence_chain()
        metrics = self.compute_completion_metrics()
        overlap_check = self.verify_no_overlap()
        system_check = self.verify_system_determination()
        
        return {
            "report_id": "LIUHE-HIERARCHY-001",
            "timestamp": datetime.now().isoformat(),
            "emergence_chain": chain,
            "completion_metrics": metrics,
            "verification": {
                "no_overlap": overlap_check,
                "system_determination": system_check,
            },
            "registered_coordinates": [
                {
                    "key": key,
                    "system": coord.system.value,
                    "level": coord.level.value,
                    "emergence_value": coord.compute_emergence_value(),
                }
                for key, coord in self.coordinates.items()
            ],
            "theorem": "定理五十七·六系层级涌现定理",
            "emergence_id": "EMERGENCE-018",
        }


# ============================================================================
# 4. 便捷接口
# ============================================================================

def create_liuhe_hierarchy_engine() -> LiuHeHierarchyEngine:
    """创建六系层级涌现引擎"""
    return LiuHeHierarchyEngine()


def quick_demo() -> Dict:
    """快速演示"""
    engine = LiuHeHierarchyEngine()
    
    # 注册十二级坐标
    for level in EmergenceLevel:
        info = LiuHeHierarchyConstants.LEVELS[level]
        weights = info["weights"]
        
        coord = LiuHeCoordinate(
            system=info["systems"][0],
            level=level,
            alpha1=weights[0],
            alpha2=weights[1],
            alpha3=weights[2],
        )
        engine.register_coordinate(coord)
    
    # 生成文件名示例
    examples = [
        engine.generate_filename(LiuHeSystem.ZR, EmergenceLevel.L2, "V1.0", "20260801"),
        engine.generate_filename(LiuHeSystem.TD, EmergenceLevel.L12, "V2.3", "20260801"),
        engine.generate_filename(LiuHeSystem.QH, EmergenceLevel.L6, "V1.0", "20260801"),
    ]
    
    # 解析文件名示例
    parsed = []
    for ex in examples:
        meta = engine.parse_filename(ex)
        if meta:
            parsed.append({
                "filename": ex,
                "system": meta.coordinate.system.value,
                "level": meta.coordinate.level.value,
                "weights": meta.coordinate.compute_emergence_value(),
            })
    
    return {
        "report": engine.generate_report(),
        "filename_examples": examples,
        "parsed_examples": parsed,
    }


if __name__ == "__main__":
    print("=" * 70)
    print("BSD六系层级涌现引擎")
    print("定理五十七·六系层级涌现定理")
    print("=" * 70)
    
    result = quick_demo()
    report = result["report"]
    
    print("\n【十二级涌现链】")
    for level in report["emergence_chain"]:
        print(f"  {level['level']} {level['name']}: "
              f"主导={level['dominant_systems']} "
              f"α₁={level['weights']['α₁']:.2f} "
              f"α₂={level['weights']['α₂']:.2f} "
              f"α₃={level['weights']['α₃']:.2f} "
              f"涌现值={level['emergence_value']:.4f}")
    
    print(f"\n【层级完成度】")
    metrics = report["completion_metrics"]
    print(f"  总层级: {metrics['total_levels']}")
    print(f"  已注册: {metrics['registered_levels']}")
    print(f"  完成度: {metrics['completion_rate']:.1%}")
    print(f"  涌现速度: {metrics['emergence_speed']:.2f}")
    
    print(f"\n【文件名示例】")
    for ex in result["filename_examples"]:
        print(f"  {ex}")
    
    print(f"\n【文件名解析】")
    for p in result["parsed_examples"]:
        print(f"  {p['filename']}: {p['system']}·{p['level']}")
    
    print(f"\n【验证结果】")
    v = report["verification"]
    print(f"  空间无重叠: {'✅' if v['no_overlap']['no_overlap'] else '❌'}")
    print(f"  物理决定系: {'✅' if v['system_determination']['physics_determines_system'] else '❌'}")
    
    print(f"\n【定理五十七·EMERGENCE-018归档】")
    print("=" * 70)
