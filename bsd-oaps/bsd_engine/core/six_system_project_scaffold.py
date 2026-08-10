"""
归属基底：L0_总本源层·六系核心公理·六系立系论V1.8
对应公理：六系立系公理（六系=立系坐标系）+ 0×0=n双零涌现方程
理论原文出处：BSD六系立系论V1.8 §17 归零圆环 + BSD虚拟宇宙创世篇章·Updream工程落地
固定数理常量：k₊=0.9·k₋=0.1·S₀=0.81·Π₂=2.8274333882

SixSystemProjectScaffold — 项目六系目录脚手架

核心命题：
    六系=方向=项目结构——每个项目都按六系组织目录。
    不再是传统的 src/docs/assets 分类，
    而是强化系/变身系/社会系/天道系/自然系/具现系 六方向分类。

    中心=空无(0_空)——项目根目录本身不是任何系，而是容纳六系的坐标系。

使用方式：
    scaffold = SixSystemProjectScaffold("my_updream_project")
    scaffold.create()           # 创建六系目录结构
    scaffold.scan()             # 扫描现有文件并归类到六系
    scaffold.report()           # 生成六系分布报告
    scaffold.suggest()          # 建议缺失方向应补充的文件
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime

from bsd_engine.registry.constants import (
    K_PLUS, K_MINUS, S_ZERO, LAMBDA, LAMBDA_INV, PI_2,
    verify_params,
)
from bsd_engine.core.six_system_project_mapper import (
    SixSystem, SIX_SYSTEM_DIRECTIONS, SystemDirection,
    SixSystemProjectMapper,
)


# ============================================================
# 六系目录名映射
# ============================================================
SYSTEM_DIR_NAMES: Dict[SixSystem, str] = {
    SixSystem.QIANGHUA: "01_项目文件_强化系",    # 🔵 核心·承载
    SixSystem.BIANSHEN: "02_风格_变身系",        # ⚫ 转化·切换
    SixSystem.SHEHUI:   "03_文档_社会系",        # 🟢 连接·协议
    SixSystem.TIANDAO:  "04_分镜_天道系",        # 🟣 法则·序列
    SixSystem.ZIRAN:    "05_音乐_自然系",        # 🟠 共振·感知
    SixSystem.JUXIAN:   "06_场景角色_具现系",    # 🔴 凝结·显现
}


class SixSystemProjectScaffold:
    """
    项目六系目录脚手架

    核心命题：六系=方向=项目结构
    中心=空无(0_空)——项目根目录本身不是任何系，而是容纳六系的坐标系
    """

    def __init__(self, project_path: str):
        verify_params()
        self.project_path = Path(project_path)
        self.mapper = SixSystemProjectMapper()
        self._scan_result: Dict[str, List[str]] = {}

    # ========================================================
    # 创建六系目录结构
    # ========================================================
    def create(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        创建六系目录结构

        Parameters
        ----------
        dry_run : bool
            True=只返回将创建的目录，不实际创建

        Returns
        -------
        dict : 创建结果
        """
        created_dirs = []
        created_files = []

        for sys_enum, dir_name in SYSTEM_DIR_NAMES.items():
            dir_path = self.project_path / dir_name
            direction = self.directions[sys_enum]

            if not dry_run:
                dir_path.mkdir(parents=True, exist_ok=True)

            created_dirs.append(str(dir_path))

            # 每个方向创建README
            readme_path = dir_path / "README.md"
            readme_content = self._generate_readme(sys_enum, direction)
            if not dry_run:
                readme_path.write_text(readme_content, encoding="utf-8")
            created_files.append(str(readme_path))

            # 每个方向创建config.yaml
            config_path = dir_path / "config.yaml"
            config_content = self._generate_config(sys_enum, direction)
            if not dry_run:
                config_path.write_text(config_content, encoding="utf-8")
            created_files.append(str(config_path))

        # 项目根目录创建六系总纲
        root_readme = self.project_path / "README.md"
        root_content = self._generate_root_readme()
        if not dry_run:
            root_readme.write_text(root_content, encoding="utf-8")
        created_files.append(str(root_readme))

        return {
            "project": str(self.project_path),
            "protocol": "BSD六系立系·0×0=n",
            "center": "空无(0_空)——项目根目录",
            "created_dirs": created_dirs,
            "created_files": created_files,
            "dry_run": dry_run,
            "total_dirs": len(created_dirs),
            "total_files": len(created_files),
        }

    @property
    def directions(self):
        return SIX_SYSTEM_DIRECTIONS

    # ========================================================
    # 扫描现有文件并归类到六系
    # ========================================================
    def scan(self) -> Dict[str, Any]:
        """
        扫描项目目录下所有文件，归类到六系方向

        Returns
        -------
        dict : 扫描结果，包含每个方向的文件列表
        """
        if not self.project_path.exists():
            return {"error": f"项目路径不存在: {self.project_path}"}

        result: Dict[str, List[str]] = {s.value: [] for s in SixSystem}
        unclassified: List[str] = []

        for root, dirs, files in os.walk(str(self.project_path)):
            # 跳过隐藏目录和隔离区
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "L1外_局部实验隔离区"]
            for fname in files:
                fpath = os.path.join(root, fname)
                rel_path = os.path.relpath(fpath, str(self.project_path))

                classifications = self.mapper.classify_file(fname)
                if classifications:
                    top_system = classifications[0][0]
                    result[top_system.value].append(rel_path)
                else:
                    unclassified.append(rel_path)

        self._scan_result = result
        total = sum(len(v) for v in result.values()) + len(unclassified)

        return {
            "project": str(self.project_path),
            "total_files": total,
            "classified": sum(len(v) for v in result.values()),
            "unclassified": len(unclassified),
            "unclassified_files": unclassified[:20],  # 最多显示20个
            "six_systems": result,
            "weights": self._compute_weights_from_scan(result, total),
        }

    def _compute_weights_from_scan(self, result: Dict[str, List[str]], total: int) -> Dict[str, float]:
        """从扫描结果计算六系权重"""
        if total == 0:
            return {s.value: 1.0 / 6 for s in SixSystem}
        raw = {s.value: len(result.get(s.value, [])) / total for s in SixSystem}
        return raw

    # ========================================================
    # 六系分布报告
    # ========================================================
    def report(self) -> Dict[str, Any]:
        """生成六系分布报告"""
        if not self._scan_result:
            self.scan()

        total = sum(len(v) for v in self._scan_result.values())
        report_data = {}

        for sys_enum, direction in SIX_SYSTEM_DIRECTIONS.items():
            files = self._scan_result.get(sys_enum.value, [])
            count = len(files)
            weight = count / total if total > 0 else 0

            report_data[sys_enum.value] = {
                "color": direction.color,
                "zero_code": direction.zero_code,
                "direction": direction.project_direction,
                "file_count": count,
                "weight": round(weight, 4),
                "protocol": direction.agent_capability.split("——")[0] if "——" in direction.agent_capability else "",
                "status": "active" if count > 0 else "dormant",
            }

        # 判断项目均衡度
        weights = [v["weight"] for v in report_data.values()]
        import numpy as np
        variance = float(np.var(weights)) if weights else 0
        is_balanced = variance < 0.01

        return {
            "project": str(self.project_path),
            "protocol": "BSD六系立系·0×0=n",
            "center": "空无(0_空)",
            "total_files": total,
            "six_systems": report_data,
            "balance": {
                "variance": round(variance, 6),
                "is_balanced": is_balanced,
                "s_zero_threshold": S_ZERO,
                "open_degree": round(sum(1 for v in report_data.values() if v["status"] == "active") / 6, 4),
            },
            "timestamp": datetime.now().isoformat(),
        }

    # ========================================================
    # 方向建议
    # ========================================================
    def suggest(self) -> Dict[str, Any]:
        """建议缺失方向应补充的文件"""
        if not self._scan_result:
            self.scan()

        suggestions = {}
        for sys_enum, direction in SIX_SYSTEM_DIRECTIONS.items():
            files = self._scan_result.get(sys_enum.value, [])
            if len(files) == 0:
                suggestions[sys_enum.value] = {
                    "color": direction.color,
                    "direction": direction.project_direction,
                    "status": "dormant·需要补充",
                    "suggested_files": direction.file_patterns[:5],
                    "capability": direction.agent_capability,
                    "action": direction.creation_action,
                }

        return {
            "project": str(self.project_path),
            "dormant_directions": len(suggestions),
            "suggestions": suggestions,
            "message": f"项目有{len(suggestions)}个方向未激活，建议补充" if suggestions else "六系全开·项目均衡",
        }

    # ========================================================
    # 内部生成器
    # ========================================================
    def _generate_readme(self, sys_enum: SixSystem, direction: SystemDirection) -> str:
        """生成方向README"""
        return f"""# {direction.color} {direction.project_direction}

## 归属基底：L0_总本源层·六系核心公理
## 方向：{sys_enum.value}
## 0编码：{direction.zero_code}
## 三元源头：{direction.ternary_source}
## 三零根源：{direction.three_zero_root}

### 智能体能力
{direction.agent_capability}

### 创作动作
{direction.creation_action}

### Updream映射
{direction.updream_mapping}

### 文件模式
{chr(10).join(f'- `{p}`' for p in direction.file_patterns[:10])}

---
*BSD六系立系·0×0=n·{direction.project_direction}方向*
"""

    def _generate_config(self, sys_enum: SixSystem, direction: SystemDirection) -> str:
        """生成方向配置"""
        return f"""# {sys_enum.value}方向配置
# 归属基底：L0_总本源层·六系核心公理
# 0编码：{direction.zero_code}

system: {sys_enum.value}
direction: {direction.project_direction}
zero_code: "{direction.zero_code}"
ternary_source: {direction.ternary_source}
weight: {direction.weight}
ring_id: {direction.ring_id}

# 锁档参数
constants:
  k_plus: {K_PLUS}
  k_minus: {K_MINUS}
  s_zero: {S_ZERO}
  pi_2: {PI_2}
"""

    def _generate_root_readme(self) -> str:
        """生成项目根README"""
        lines = [
            f"# {self.project_path.name}",
            "",
            "## BSD六系立系·0×0=n·项目六系方向导航",
            "",
            "中心=空无(0_空)——项目根目录本身不是任何系，而是容纳六系的坐标系。",
            "",
            "| 方向 | 0编码 | 项目目录 |",
            "|:---|:---:|:---|",
        ]
        for sys_enum, dir_name in SYSTEM_DIR_NAMES.items():
            direction = SIX_SYSTEM_DIRECTIONS[sys_enum]
            lines.append(f"| {direction.color} {sys_enum.value} | {direction.zero_code} | `{dir_name}/` |")

        lines.extend([
            "",
            "### 六系相生链",
            "强化系→自然系→变身系→天道系→社会系→具现系→强化系",
            "",
            "### 0×0=n",
            "空无(0_空·六系坐标系)×任何输入(0)=无限可能(n)",
            "",
            f"*BSD六系立系·V1.8·{datetime.now().strftime('%Y-%m-%d')}*",
        ])
        return "\n".join(lines)
