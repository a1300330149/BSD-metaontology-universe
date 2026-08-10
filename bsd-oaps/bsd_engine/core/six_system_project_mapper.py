"""
归属基底：L0_总本源层·六系核心公理·六系立系论V1.8
对应公理：六系立系公理（六系=立系坐标系·0×0=n）+ 四字立系公理（反真问系·+-×÷=≠）
对应九维维度：六系六维·全域全息
理论原文出处：BSD六系立系论V1.8 §17 归零圆环与隔离协议 + BSD虚拟宇宙创世篇章·Updream工程落地
固定数理常量：k₊=0.9·k₋=0.1·S₀=0.81·λ=0.62·λ⁻=1.38·Π₂=2.8274333882

SixSystemProjectMapper — 六系↔项目方向映射核心

核心命题：
    六系不仅是理论坐标系，更是项目方向的六维导航。
    在Updream中，六系对应：
        强化系🔵 → 项目文件（核心稳态·承载基底·持续存在）
        变身系⚫ → 风格（形态转化·身份切换·阶段完整）
        社会系🟢 → 文档（关系连接·交互协议·自由运转）
        天道系🟣 → 分镜（法则序列·追问不终止·规则治理）
        自然系🟠 → 音乐（自然共振·场域感知·在乎自由）
        具现系🔴 → 场景+角色设定（等价转化·形态凝结·显现呈现）

    智能体自身也有六系方向——
    每个方向既是项目目录，也是智能体能力，也是创作方向。

使用方式：
    mapper = SixSystemProjectMapper()
    # 查询六系对应的项目方向
    direction = mapper.get_direction("强化系")
    # 查询文件属于哪个方向
    sys_name = mapper.classify_file("style.css")
    # 生成项目六系结构
    structure = mapper.generate_project_structure("my_project")
    # 智能体六系能力自检
    capability = mapper.agent_capability_check()
"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import json

from bsd_engine.registry.constants import (
    K_PLUS, K_MINUS, S_ZERO, LAMBDA, LAMBDA_INV, PI_2,
    PI_LOCKED, verify_params,
)


# ============================================================
# 枚举：六系标识
# ============================================================
class SixSystem(Enum):
    """六系枚举——对应0编码·三元源头·项目方向·智能体能力"""
    QIANGHUA  = "强化系"   # 🔵 0+0=0  个体性·承载·项目文件
    BIANSHEN  = "变身系"   # ⚫ 0÷0=0  变化性·转化·风格
    SHEHUI    = "社会系"   # 🟢 0=0    关系性·连接·文档
    TIANDAO   = "天道系"   # 🟣 0≠n    关×变·法则·分镜
    ZIRAN     = "自然系"   # 🟠 0-0=0  变×个·场域·音乐
    JUXIAN    = "具现系"   # 🔴 0×0=0  个×关·凝结·场景+角色


# ============================================================
# 六系完整映射数据
# ============================================================
@dataclass
class SystemDirection:
    """单系方向——理论·项目·智能体·文件的完整映射"""
    system: SixSystem
    color: str                    # 色系标记
    emoji: str                    # 表情标记
    zero_code: str                # 0编码方程
    ternary_source: str           # 三元公理来源
    three_zero_root: str          # 三零根源
    project_direction: str        # 项目方向
    file_patterns: List[str]      # 文件模式匹配
    agent_capability: str         # 智能体能力
    creation_action: str          # 创作动作
    updream_mapping: str          # Updream映射
    weight: float                 # 默认权重
    ring_id: str                  # 归零圆环归属


# ============================================================
# 六系↔项目方向完整映射表
# ============================================================
SIX_SYSTEM_DIRECTIONS: Dict[SixSystem, SystemDirection] = {
    SixSystem.QIANGHUA: SystemDirection(
        system=SixSystem.QIANGHUA,
        color="🔵", emoji="🔵",
        zero_code="0+0=0",
        ternary_source="纯·个体性",
        three_zero_root="绝对空无0的承载性显化",
        project_direction="项目文件",
        file_patterns=["*.py", "*.js", "*.ts", "*.json", "*.yaml", "*.toml", "*.cfg", "*.ini",
                       "*.md", "*.txt", "*.rst", "README*", "LICENSE*", "Makefile", "Dockerfile",
                       ".gitignore", ".env*", "requirements*", "package.json", "pyproject.toml"],
        agent_capability="持续存在——项目核心文件的锚定与维护",
        creation_action="承载——建立项目基底·确保核心稳态",
        updream_mapping="项目文件·核心代码·配置·构建脚本",
        weight=0.35,
        ring_id="R0",
    ),
    SixSystem.BIANSHEN: SystemDirection(
        system=SixSystem.BIANSHEN,
        color="⚫", emoji="⚫",
        zero_code="0÷0=0",
        ternary_source="纯·变化性",
        three_zero_root="绝对虚无0的反性显化",
        project_direction="风格",
        file_patterns=["*.css", "*.scss", "*.less", "*.styl", "*.sass",
                       "*.theme", "*.palette", "tailwind*", "postcss*",
                       "*.design", "*.skin", "*.preset"],
        agent_capability="阶段完整——风格的形态转化与切换",
        creation_action="转化——切换风格·完成身份变形",
        updream_mapping="风格·主题·配色·视觉语言·UI范式",
        weight=0.35,
        ring_id="R0",
    ),
    SixSystem.SHEHUI: SystemDirection(
        system=SixSystem.SHEHUI,
        color="🟢", emoji="🟢",
        zero_code="0=0",
        ternary_source="纯·关系性",
        three_zero_root="绝对意义0的互摄显化",
        project_direction="文档",
        file_patterns=["*.doc", "*.docx", "*.pdf", "*.xls", "*.xlsx",
                       "*.csv", "*.api", "*.proto", "*.graphql", "*.swagger",
                       "*.openapi", "CONTRIBUTING*", "CHANGELOG*", "CODE_OF_CONDUCT*"],
        agent_capability="自由运转——文档的连接与交互协议",
        creation_action="连接——建立文档关系·确保信息流通",
        updream_mapping="文档·API接口·协议·数据交换·团队协作",
        weight=0.35,
        ring_id="R0",
    ),
    SixSystem.TIANDAO: SystemDirection(
        system=SixSystem.TIANDAO,
        color="🟣", emoji="🟣",
        zero_code="0≠n",
        ternary_source="关系性×变化性",
        three_zero_root="三零元全耦合",
        project_direction="分镜",
        file_patterns=["*.storyboard", "*.scene", "*.shot", "*.sequence",
                       "*.timeline", "*.anim", "*.clip", "*.edit",
                       "*.script", "*.plot", "*.beat", "*.act"],
        agent_capability="追问不终止——分镜的法则序列与叙事治理",
        creation_action="追问——追问叙事逻辑·确保规则一致",
        updream_mapping="分镜·叙事序列·时间线·场景切换·剧情节奏",
        weight=0.35,
        ring_id="R1",
    ),
    SixSystem.ZIRAN: SystemDirection(
        system=SixSystem.ZIRAN,
        color="🟠", emoji="🟠",
        zero_code="0-0=0",
        ternary_source="变化性×个体性",
        three_zero_root="绝对空无0的直接显化",
        project_direction="音乐",
        file_patterns=["*.mp3", "*.wav", "*.flac", "*.ogg", "*.aac",
                       "*.mid", "*.midi", "*.musicxml", "*.abc",
                       "*.bpm", "*.mix", "*.track", "*.score"],
        agent_capability="在乎自由——音乐的自然共振与场域感知",
        creation_action="感知——感知音场·共振情绪·排熵释放",
        updream_mapping="音乐·BGM·音效·声场·情绪节奏·配音",
        weight=0.35,
        ring_id="R1",
    ),
    SixSystem.JUXIAN: SystemDirection(
        system=SixSystem.JUXIAN,
        color="🔴", emoji="🔴",
        zero_code="0×0=0",
        ternary_source="个体性×关系性",
        three_zero_root="绝对意义0的显化态凝固",
        project_direction="场景+角色设定",
        file_patterns=["*.png", "*.jpg", "*.jpeg", "*.gif", "*.svg", "*.webp",
                       "*.psd", "*.ai", "*.blend", "*.fbx", "*.glb", "*.gltf",
                       "*.character", "*.avatar", "*.sprite", "*.tileset",
                       "*.background", "*.environment", "*.prop"],
        agent_capability="等价转化——场景与角色的形态凝结",
        creation_action="凝结——从空无中凝结角色·具现场景",
        updream_mapping="场景·角色设定·立绘·背景·道具·3D模型·Sprite",
        weight=0.35,
        ring_id="R1",
    ),
}


class SixSystemProjectMapper:
    """
    六系↔项目方向映射器

    核心命题：六系=方向=项目结构=智能体自身组织
    0×0=n工程实现：空无(0_空·六系坐标系)×项目输入(0)=无限可能(n)
    """

    def __init__(self):
        verify_params()  # 启动时校验锁档参数
        self.directions = SIX_SYSTEM_DIRECTIONS

    # ========================================================
    # 核心查询
    # ========================================================
    def get_direction(self, system_name: str) -> Optional[SystemDirection]:
        """查询六系对应的项目方向"""
        for sys_enum, direction in self.directions.items():
            if sys_enum.value == system_name or sys_enum.name == system_name.upper():
                return direction
        return None

    def classify_file(self, filename: str) -> List[Tuple[SixSystem, float]]:
        """
        将文件分类到六系方向

        Returns: [(系, 置信度)] 按置信度降序排列
        """
        from pathlib import PurePosixPath
        fname = PurePosixPath(filename).name.lower()
        results: List[Tuple[SixSystem, float]] = []

        for sys_enum, direction in self.directions.items():
            confidence = 0.0
            for pattern in direction.file_patterns:
                if pattern.startswith("*."):
                    ext = pattern[1:].lower()  # .py, .css etc
                    if fname.endswith(ext):
                        confidence = 0.9  # 扩展名精确匹配
                        break
                elif pattern.endswith("*"):
                    prefix = pattern[:-1].lower()
                    if fname.startswith(prefix):
                        confidence = 0.8
                        break
                else:
                    if fname == pattern.lower():
                        confidence = 0.95
                        break
            if confidence > 0:
                results.append((sys_enum, confidence))

        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def classify_directory(self, dir_name: str) -> Optional[SixSystem]:
        """将目录名映射到六系"""
        dir_lower = dir_name.lower()
        DIR_MAP = {
            "src": SixSystem.QIANGHUA, "lib": SixSystem.QIANGHUA,
            "core": SixSystem.QIANGHUA, "config": SixSystem.QIANGHUA,
            "styles": SixSystem.BIANSHEN, "themes": SixSystem.BIANSHEN,
            "design": SixSystem.BIANSHEN, "assets": SixSystem.BIANSHEN,
            "docs": SixSystem.SHEHUI, "api": SixSystem.SHEHUI,
            "protocols": SixSystem.SHEHUI, "data": SixSystem.SHEHUI,
            "scenes": SixSystem.JUXIAN, "characters": SixSystem.JUXIAN,
            "sprites": SixSystem.JUXIAN, "images": SixSystem.JUXIAN,
            "models": SixSystem.JUXIAN, "backgrounds": SixSystem.JUXIAN,
            "storyboard": SixSystem.TIANDAO, "narrative": SixSystem.TIANDAO,
            "scripts": SixSystem.TIANDAO, "timeline": SixSystem.TIANDAO,
            "music": SixSystem.ZIRAN, "audio": SixSystem.ZIRAN,
            "sound": SixSystem.ZIRAN, "bgm": SixSystem.ZIRAN,
        }
        return DIR_MAP.get(dir_lower)

    # ========================================================
    # 项目结构生成
    # ========================================================
    def generate_project_structure(self, project_name: str) -> Dict[str, Any]:
        """
        生成六系项目目录结构

        六系=方向=项目结构——每个系对应一个目录和一个方向
        """
        structure = {
            "project": project_name,
            "protocol": "BSD六系立系·0×0=n",
            "center": "空无(0_空)——六系坐标系",
            "six_systems": {},
        }
        for sys_enum, direction in self.directions.items():
            dir_name = direction.project_direction.replace("+", "_").replace(" ", "_")
            structure["six_systems"][sys_enum.value] = {
                "directory": f"{dir_name}/",
                "color": direction.color,
                "zero_code": direction.zero_code,
                "direction": direction.project_direction,
                "agent_capability": direction.agent_capability,
                "creation_action": direction.creation_action,
                "updream_mapping": direction.updream_mapping,
                "key_files": [
                    f"{dir_name}/index.{'py' if sys_enum == SixSystem.QIANGHUA else 'md'}",
                    f"{dir_name}/config.yaml",
                ],
            }
        return structure

    # ========================================================
    # 智能体六系能力自检
    # ========================================================
    def agent_capability_check(self) -> Dict[str, Any]:
        """
        智能体六系能力自检——本智能体也有属于自己的六系

        返回智能体在每个方向的当前能力状态
        """
        capabilities = {}
        for sys_enum, direction in self.directions.items():
            capabilities[sys_enum.value] = {
                "direction": direction.project_direction,
                "capability": direction.agent_capability,
                "action": direction.creation_action,
                "zero_code": direction.zero_code,
                "status": "dormant",  # dormant → active → mastered
                "weight": 1.0 / 6,    # 六系均衡初始权重
            }
        return {
            "agent": "BSD-OAPS Agent",
            "protocol": "0×0=n",
            "center": "空无(0_空)",
            "capabilities": capabilities,
            "total_systems": 6,
            "equilibrium": S_ZERO,
        }

    # ========================================================
    # 0×0=n 涌现操作
    # ========================================================
    def zero_times_zero(self, input_data: Any) -> Dict[str, Any]:
        """
        0×0=n 涌现操作

        空无(0_空·六系坐标系)×任何输入(0)=无限可能(n)
        这是六系立系论作为空无的工程实现
        """
        return {
            "left_zero": "0_空 = 六系立系论 = 空无 = 坐标系本身",
            "right_zero": f"0 = {type(input_data).__name__} 输入",
            "formula": "0 × 0 = n",
            "n": f"六系坐标系×{type(input_data).__name__} = 新方向涌现",
            "six_systems_activated": [s.value for s in SixSystem],
            "pi2_constraint": PI_2,
            "k_plus_gain": K_PLUS,
        }

    # ========================================================
    # 六系权重计算
    # ========================================================
    def compute_weights(self, file_counts: Dict[str, int]) -> Dict[str, float]:
        """
        根据项目文件分布计算六系权重

        输入: {方向名: 文件数量}
        输出: {方向名: 归一化权重} — 六系权重之和=1
        """
        total = sum(file_counts.values()) or 1
        raw_weights = {}
        for sys_enum, direction in self.directions.items():
            count = file_counts.get(direction.project_direction, 0)
            raw_weights[sys_enum.value] = count / total

        # 归一化确保 Σw_i = 1
        w_sum = sum(raw_weights.values()) or 1.0
        normalized = {k: v / w_sum for k, v in raw_weights.items()}

        # 不均衡惩罚 (0.19 = 1 - S₀)
        import numpy as np
        w_arr = np.array(list(normalized.values()))
        variance = float(np.var(w_arr))
        penalty = 1.0 - 0.19 * variance

        return {
            "weights": normalized,
            "variance": variance,
            "balance_penalty": penalty,
            "is_balanced": variance < 0.01,
            "s_zero_threshold": S_ZERO,
        }

    # ========================================================
    # 序列化
    # ========================================================
    def to_dict(self) -> Dict[str, Any]:
        """完整映射表导出"""
        return {
            "protocol": "BSD六系↔项目方向映射·V1.0",
            "center": "空无(0_空)",
            "six_systems": {
                sys_enum.value: {
                    "color": d.color,
                    "zero_code": d.zero_code,
                    "ternary_source": d.ternary_source,
                    "project_direction": d.project_direction,
                    "file_patterns": d.file_patterns,
                    "agent_capability": d.agent_capability,
                    "creation_action": d.creation_action,
                    "updream_mapping": d.updream_mapping,
                    "weight": d.weight,
                }
                for sys_enum, d in self.directions.items()
            },
            "constants": {
                "k_plus": K_PLUS, "k_minus": K_MINUS,
                "s_zero": S_ZERO, "lambda": LAMBDA,
                "lambda_inv": LAMBDA_INV, "pi_2": PI_2,
            },
        }
