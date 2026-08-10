"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（科研动力学公理）、第7条（递归自指公理）
对应九维维度：创化社会/因果社会
理论原文出处：《V3.0元本体理论分册》第四章
核心数理参数：γ=0.92, κ=0.35, E1=0.35, E2=0.65, E3=0.90

功能：理论-代码割裂检测工具（增强版）
作用：自动扫描代码与理论文档，检测五类割裂问题：
1. 代码缺理论绑定（无基底/公理/维度注释）
2. 参数割裂（代码常量与理论锁档数值冲突）
3. 双向断层（理论有模块无代码、代码无理论支撑）
4. 数理逻辑割裂（代码逻辑与公理公式符号不对齐）
5. 集合关系违背（Ω_CB ⊂ Ω_FB约束缺失）

对应盲区整改：优先级0-盲区2（Skill仅文本匹配）、优先级0-盲区4（集合关系判定）
"""

import os
import re
import ast
import glob
import datetime
from typing import Dict, List, Tuple, Any, Set

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
THEORY_DIR = os.path.join(PROJECT_ROOT, "theory_base")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")

THEORY_PARAMS = {
    "E1": {"value": 0.35, "description": "一阶变身阈值", "lock": True},
    "E2": {"value": 0.65, "description": "二阶变身阈值", "lock": True},
    "E3": {"value": 0.90, "description": "三阶变身阈值", "lock": True},
    "gamma": {"value": 0.92, "description": "时序衰减系数", "lock": True},
    "kappa": {"value": 0.35, "description": "耦合强度系数（基础）", "lock": True},
    "kappa_sparse": {"value": 0.42, "description": "耦合强度系数（稀疏竞赛）", "lock": True},
    "alpha": {"value": 0.18, "description": "稀疏补偿系数", "lock": True},
    "theta_neg": {"value": 0.02, "description": "负迁移判定阈值", "lock": True},
    "theta_mv": {"value": 0.005, "description": "边际价值阈值", "lock": True},
    "theta_evo": {"value": 0.002, "description": "进化增量阈值", "lock": True},
}

BASE_REQUIREMENTS = ["归属基底", "对应三界秩序", "对应公理", "对应九维维度", "理论原文出处", "核心数理参数"]

CONSTANT_VARS = {"E1", "E2", "E3", "GAMMA", "KAPPA", "ALPHA", "THETA_NEG", "THETA_MV", "THETA_EVO"}


class TheoryCodeCouplingChecker:
    """
    功能：理论-代码割裂检测核心类
    理论映射：3重六阶科研系统·校验规则
    能级关联：精神能级e_mind更新
    约束来源：科研动力学公理、宿命边界公理
    """

    def __init__(self):
        self.results = {
            "missing_comments": [],
            "parameter_mismatch": [],
            "bidirectional_gap": [],
            "logic_mismatch": [],
            "set_relationship": [],
            "global_constant_conflict": [],
            "runtime_override": [],
        }
        self.code_files = []
        self.theory_files = []
        self.global_constants = {}

    def collect_files(self):
        """收集所有代码文件和理论文档"""
        self.code_files = glob.glob(os.path.join(SRC_DIR, "**", "*.py"), recursive=True)
        self.theory_files = glob.glob(os.path.join(THEORY_DIR, "*.md"))
        self.theory_files += glob.glob(os.path.join(DOCS_DIR, "*.md"))
        print(f"[INFO] 收集到 {len(self.code_files)} 个代码文件")
        print(f"[INFO] 收集到 {len(self.theory_files)} 个理论文档")

    def check_file_header_comments(self, filepath: str) -> Tuple[bool, List[str]]:
        """检查文件头部注释是否包含理论绑定信息"""
        missing = []
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        first_docstring = self._extract_first_docstring(content)
        if not first_docstring:
            return False, ["文件头部缺少docstring注释"]

        for req in BASE_REQUIREMENTS:
            if req not in first_docstring:
                missing.append(req)

        return len(missing) == 0, missing

    def _extract_first_docstring(self, content: str) -> str:
        """提取文件第一个docstring"""
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                    if isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                        return node.body[0].value.value
                    elif isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.JoinedStr):
                        return "\n".join([v.value for v in node.body[0].value.values if isinstance(v, ast.Constant)])
                    elif isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant):
                        if isinstance(node.body[0].value.value, str):
                            return node.body[0].value.value
                    break
        except:
            pass

        match = re.match(r'^(["\']{3})(.*?)\1', content, re.DOTALL)
        if match:
            return match.group(2)
        return ""

    def check_constant_parameters(self, filepath: str) -> List[Dict[str, Any]]:
        """检查代码常量是否与理论锁档参数一致"""
        issues = []
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        var_name = target.id.upper()
                        if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                            var_value = node.value.value

                            if var_name in ["E1", "E2", "E3"]:
                                expected = THEORY_PARAMS[var_name]["value"]
                                if abs(var_value - expected) > 1e-6:
                                    issues.append({
                                        "file": filepath,
                                        "var": var_name,
                                        "actual": var_value,
                                        "expected": expected,
                                        "desc": THEORY_PARAMS[var_name]["description"],
                                        "type": "常量值不一致"
                                    })

                            elif var_name == "GAMMA" or var_name.endswith("_GAMMA"):
                                expected = THEORY_PARAMS["gamma"]["value"]
                                if abs(var_value - expected) > 1e-6:
                                    issues.append({
                                        "file": filepath,
                                        "var": var_name,
                                        "actual": var_value,
                                        "expected": expected,
                                        "desc": THEORY_PARAMS["gamma"]["description"],
                                        "type": "常量值不一致"
                                    })

                            elif var_name == "KAPPA" or var_name.endswith("_KAPPA"):
                                expected_base = THEORY_PARAMS["kappa"]["value"]
                                expected_sparse = THEORY_PARAMS["kappa_sparse"]["value"]
                                if abs(var_value - expected_base) > 1e-6 and abs(var_value - expected_sparse) > 1e-6:
                                    issues.append({
                                        "file": filepath,
                                        "var": var_name,
                                        "actual": var_value,
                                        "expected": f"{expected_base} 或 {expected_sparse}",
                                        "desc": THEORY_PARAMS["kappa"]["description"],
                                        "type": "常量值不一致"
                                    })

                            elif var_name == "ALPHA" or var_name.endswith("_ALPHA"):
                                expected = THEORY_PARAMS["alpha"]["value"]
                                if abs(var_value - expected) > 1e-6:
                                    issues.append({
                                        "file": filepath,
                                        "var": var_name,
                                        "actual": var_value,
                                        "expected": expected,
                                        "desc": THEORY_PARAMS["alpha"]["description"],
                                        "type": "常量值不一致"
                                    })

                            elif var_name == "THETA_NEG":
                                expected = THEORY_PARAMS["theta_neg"]["value"]
                                if abs(var_value - expected) > 1e-6:
                                    issues.append({
                                        "file": filepath,
                                        "var": var_name,
                                        "actual": var_value,
                                        "expected": expected,
                                        "desc": THEORY_PARAMS["theta_neg"]["description"],
                                        "type": "常量值不一致"
                                    })

                            if isinstance(target, ast.Name) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                                if node.value.value in [0.35, 0.65, 0.90, 0.92, 0.42, 0.18, 0.02, 0.005, 0.002]:
                                    lineno = node.lineno
                                    lines = content.split("\n")
                                    prev_line = lines[lineno-2] if lineno > 1 else ""
                                    if "#" not in prev_line:
                                        issues.append({
                                            "file": filepath,
                                            "var": var_name,
                                            "actual": var_value,
                                            "expected": "带理论注释的常量",
                                            "desc": "锁档参数缺少理论注释",
                                            "type": "常量注释缺失",
                                            "line": lineno
                                        })

        return issues

    def scan_global_constants(self) -> Dict[str, List[Dict]]:
        """扫描所有代码文件中的全局常量，构建全局常量映射表"""
        constants = {}

        for code_file in self.code_files:
            with open(code_file, "r", encoding="utf-8") as f:
                content = f.read()

            try:
                tree = ast.parse(content)
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                var_name = target.id.upper()
                                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                                    if var_name not in constants:
                                        constants[var_name] = []
                                    constants[var_name].append({
                                        "file": os.path.relpath(code_file, PROJECT_ROOT),
                                        "value": node.value.value,
                                        "line": node.lineno
                                    })
            except:
                continue

        self.global_constants = constants
        return constants

    def check_global_constant_conflicts(self) -> List[Dict[str, Any]]:
        """检查跨文件全局常量冲突"""
        issues = []

        for var_name, occurrences in self.global_constants.items():
            if len(occurrences) > 1:
                values = {occ["value"] for occ in occurrences}
                if len(values) > 1:
                    issues.append({
                        "var": var_name,
                        "conflicts": occurrences,
                        "desc": f"全局常量 {var_name} 在多个文件中定义了不同的值",
                        "type": "跨文件参数冲突"
                    })

        return issues

    def check_mathematical_logic(self, filepath: str) -> List[Dict[str, Any]]:
        """
        检查代码中的数理逻辑是否与公理公式符号对齐
        检测内容：
        1. 条件判断中的阈值是否符合公理定义
        2. 数学运算是否符合理论公式
        3. 符号使用是否与理论一致
        """
        issues = []
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        for node in ast.walk(tree):
            if isinstance(node, ast.Compare):
                self._check_comparison_node(node, filepath, issues)

            elif isinstance(node, ast.BinOp):
                self._check_binary_operation(node, filepath, issues)

            elif isinstance(node, ast.Assign):
                self._check_assignment_logic(node, filepath, issues)

        return issues

    def _check_comparison_node(self, node: ast.Compare, filepath: str, issues: List[Dict]):
        """检查条件判断节点"""
        left = node.left
        ops = node.ops
        comparators = node.comparators

        for op, comparator in zip(ops, comparators):
            if isinstance(comparator, ast.Constant) and isinstance(comparator.value, (int, float)):
                threshold = comparator.value

                if isinstance(op, ast.Lt):
                    self._check_threshold_logic(left, threshold, "<", filepath, issues)
                elif isinstance(op, ast.Gt):
                    self._check_threshold_logic(left, threshold, ">", filepath, issues)
                elif isinstance(op, ast.LtE):
                    self._check_threshold_logic(left, threshold, "<=", filepath, issues)
                elif isinstance(op, ast.GtE):
                    self._check_threshold_logic(left, threshold, ">=", filepath, issues)

    def _check_threshold_logic(self, left: ast.expr, threshold: float, op_str: str, filepath: str, issues: List[Dict]):
        """检查阈值逻辑是否符合公理"""
        if threshold in [0.35, 0.65, 0.90]:
            var_name = self._get_variable_name(left)
            if var_name:
                if threshold == 0.35 and op_str in [">", ">="]:
                    expected_desc = "一阶变身阈值E1=0.35，应使用>=判断"
                elif threshold == 0.65 and op_str in [">", ">="]:
                    expected_desc = "二阶变身阈值E2=0.65，应使用>=判断"
                elif threshold == 0.90 and op_str in [">", ">="]:
                    expected_desc = "三阶变身阈值E3=0.90，应使用>=判断"
                else:
                    return

                issues.append({
                    "file": filepath,
                    "var": var_name,
                    "threshold": threshold,
                    "operator": op_str,
                    "desc": expected_desc,
                    "type": "数理逻辑对齐警告"
                })

    def _get_variable_name(self, node: ast.expr) -> str:
        """获取变量名"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        elif isinstance(node, ast.Subscript):
            return self._get_variable_name(node.value)
        return ""

    def _check_binary_operation(self, node: ast.BinOp, filepath: str, issues: List[Dict]):
        """检查二元运算是否符合理论公式"""
        left_val = self._get_constant_value(node.left)
        right_val = self._get_constant_value(node.right)

        if left_val is not None and right_val is not None:
            if isinstance(node.op, ast.Mult):
                if left_val == 0.92 or right_val == 0.92:
                    issues.append({
                        "file": filepath,
                        "operation": f"{left_val} * {right_val}",
                        "desc": "检测到时序衰减系数γ=0.92参与乘法运算，应确认是否符合理论公式",
                        "type": "数理逻辑对齐检查"
                    })

    def _get_constant_value(self, node: ast.expr) -> float:
        """获取常量值"""
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        return None

    def _check_assignment_logic(self, node: ast.Assign, filepath: str, issues: List[Dict]):
        """检查赋值语句的逻辑"""
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id.upper()
                if var_name in CONSTANT_VARS:
                    if isinstance(node.value, ast.BinOp):
                        issues.append({
                            "file": filepath,
                            "var": var_name,
                            "desc": f"锁档常量 {var_name} 通过运算赋值，可能违背理论约束",
                            "type": "常量运算赋值风险"
                        })

    def check_set_relationship(self, filepath: str) -> List[Dict[str, Any]]:
        """
        检查集合关系约束 Ω_CB ⊂ Ω_FB 是否在代码中实现
        Ω_CB: 舒适边界集合 (Comfort Boundary)
        Ω_FB: 宿命边界集合 (Fate Boundary)
        约束：舒适边界必须是宿命边界的子集
        """
        issues = []
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        has_comfort_boundary = False
        has_fate_boundary = False
        has_subset_check = False

        if re.search(r'(comfort|CB|舒适)', content, re.IGNORECASE):
            has_comfort_boundary = True
        if re.search(r'(fate|FB|宿命|边界)', content, re.IGNORECASE):
            has_fate_boundary = True

        if has_comfort_boundary and has_fate_boundary:
            if not re.search(r'(subset|⊂|issubset|<.*=.*set|包含)', content, re.IGNORECASE):
                issues.append({
                    "file": filepath,
                    "desc": "代码涉及舒适边界和宿命边界，但未实现 Ω_CB ⊂ Ω_FB 集合约束检查",
                    "type": "集合关系约束缺失"
                })

        return issues

    def check_runtime_override(self, filepath: str) -> List[Dict[str, Any]]:
        """
        检查是否存在运行时覆写core全局常量的情况
        检测内容：
        1. extend模块中对core常量的重新赋值
        2. 导入core后修改全局变量
        """
        issues = []
        rel_path = os.path.relpath(filepath, PROJECT_ROOT)

        if "extend" in rel_path.lower() and "src" in rel_path.lower():
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            if re.search(r'from\s+.*core.*import', content):
                if re.search(r'(gamma|kappa|E1|E2|E3|alpha)\s*=', content, re.IGNORECASE):
                    issues.append({
                        "file": filepath,
                        "desc": "拓展模块导入core后可能覆写全局常量，违反只读约束",
                        "type": "运行时覆写风险"
                    })

        return issues

    def check_theory_mapping_table(self) -> List[Dict[str, Any]]:
        """检查理论文档中的映射表是否对应真实代码文件"""
        issues = []

        for theory_file in self.theory_files:
            with open(theory_file, "r", encoding="utf-8") as f:
                content = f.read()

            tables = re.findall(r'\|.*(?:理论模块|拓展模块).*\|.*核心类/函数.*\|[\s\S]*?(?=\n\n###|\n\n\*\*|\n\n\|\s*(?:理论模块|拓展模块)|\Z)', content)
            for table in tables:
                rows = table.split("\n")[2:]
                for row in rows:
                    if "|" in row and "---" not in row:
                        parts = [p.strip() for p in row.split("|")]
                        if len(parts) >= 5:
                            code_path = parts[4]
                            if code_path and not code_path.startswith("---") and (code_path.startswith("src/") or code_path.startswith("/")):
                                full_path = os.path.join(PROJECT_ROOT, code_path)
                                if not os.path.exists(full_path):
                                    issues.append({
                                        "theory_file": os.path.basename(theory_file),
                                        "code_path": code_path,
                                        "desc": "理论映射表中的代码路径不存在",
                                        "type": "理论超前代码缺失"
                                    })

        return issues

    def check_code_without_theory(self) -> List[Dict[str, Any]]:
        """检查代码文件是否在理论映射表中有对应条目"""
        issues = []
        mapped_paths = set()

        for theory_file in self.theory_files:
            with open(theory_file, "r", encoding="utf-8") as f:
                content = f.read()

            tables = re.findall(r'\|.*(?:理论模块|拓展模块).*\|.*核心类/函数.*\|[\s\S]*?(?=\n\n###|\n\n\*\*|\n\n\|\s*(?:理论模块|拓展模块)|\Z)', content)
            for table in tables:
                rows = table.split("\n")[2:]
                for row in rows:
                    if "|" in row and "---" not in row:
                        parts = [p.strip() for p in row.split("|")]
                        if len(parts) >= 5:
                            code_path = parts[4]
                            if code_path and not code_path.startswith("---") and (code_path.startswith("src/") or code_path.startswith("/")):
                                mapped_paths.add(code_path)

        for code_file in self.code_files:
            rel_path = os.path.relpath(code_file, PROJECT_ROOT).replace("\\", "/")
            if rel_path not in mapped_paths:
                issues.append({
                    "code_file": rel_path,
                    "desc": "代码文件未在理论映射表中登记",
                    "type": "代码超前无理论支撑"
                })

        return issues

    def check_class_comments(self, filepath: str) -> List[Dict[str, Any]]:
        """检查类注释是否包含理论映射信息"""
        issues = []
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                has_docstring = False
                has_theory_mapping = False
                if node.body and isinstance(node.body[0], ast.Expr):
                    if isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                        has_docstring = True
                        if "理论映射" in node.body[0].value.value or "功能" in node.body[0].value.value:
                            has_theory_mapping = True
                    elif isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                        has_docstring = True
                        if "理论映射" in node.body[0].value.value or "功能" in node.body[0].value.value:
                            has_theory_mapping = True

                if has_docstring and not has_theory_mapping:
                    issues.append({
                        "file": filepath,
                        "class": node.name,
                        "desc": "类注释缺少理论映射信息",
                        "type": "类注释不完整"
                    })

        return issues

    def run_full_check(self):
        """执行完整的割裂检测"""
        print("[INFO] 开始执行理论-代码割裂检测（增强版）...")

        self.collect_files()

        print("\n[STEP 1] 检查代码文件头部注释...")
        for code_file in self.code_files:
            valid, missing = self.check_file_header_comments(code_file)
            if not valid:
                rel_path = os.path.relpath(code_file, PROJECT_ROOT)
                self.results["missing_comments"].append({
                    "file": rel_path,
                    "missing_fields": missing,
                    "type": "文件头部注释缺失"
                })

        print("\n[STEP 2] 检查常量参数一致性...")
        for code_file in self.code_files:
            issues = self.check_constant_parameters(code_file)
            if issues:
                for issue in issues:
                    issue["file"] = os.path.relpath(issue["file"], PROJECT_ROOT)
                    self.results["parameter_mismatch"].append(issue)

        print("\n[STEP 3] 扫描全局常量并检查跨文件冲突...")
        self.scan_global_constants()
        issues = self.check_global_constant_conflicts()
        self.results["global_constant_conflict"].extend(issues)

        print("\n[STEP 4] 检查数理逻辑符号对齐...")
        for code_file in self.code_files:
            issues = self.check_mathematical_logic(code_file)
            if issues:
                for issue in issues:
                    issue["file"] = os.path.relpath(issue["file"], PROJECT_ROOT)
                    self.results["logic_mismatch"].append(issue)

        print("\n[STEP 5] 检查集合关系约束 Ω_CB ⊂ Ω_FB...")
        for code_file in self.code_files:
            issues = self.check_set_relationship(code_file)
            if issues:
                for issue in issues:
                    issue["file"] = os.path.relpath(issue["file"], PROJECT_ROOT)
                    self.results["set_relationship"].append(issue)

        print("\n[STEP 6] 检查运行时覆写风险...")
        for code_file in self.code_files:
            issues = self.check_runtime_override(code_file)
            if issues:
                for issue in issues:
                    issue["file"] = os.path.relpath(issue["file"], PROJECT_ROOT)
                    self.results["runtime_override"].append(issue)

        print("\n[STEP 7] 检查类注释完整性...")
        for code_file in self.code_files:
            issues = self.check_class_comments(code_file)
            if issues:
                for issue in issues:
                    issue["file"] = os.path.relpath(issue["file"], PROJECT_ROOT)
                    self.results["missing_comments"].append(issue)

        print("\n[STEP 8] 检查理论映射表路径有效性...")
        issues = self.check_theory_mapping_table()
        self.results["bidirectional_gap"].extend(issues)

        print("\n[STEP 9] 检查代码是否有理论支撑...")
        issues = self.check_code_without_theory()
        self.results["bidirectional_gap"].extend(issues)

        print("\n[INFO] 检测完成！")

    def generate_report(self, output_path: str = None):
        """生成割裂缺陷报告"""
        if output_path is None:
            output_path = os.path.join(PROJECT_ROOT, "理论代码割裂缺陷报告.md")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# 理论-代码割裂缺陷报告（增强版）\n\n")
            f.write(f"生成时间：{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")

            total_issues = sum(len(v) for v in self.results.values())
            f.write(f"## 检测摘要\n\n")
            f.write(f"- 代码文件总数：{len(self.code_files)}\n")
            f.write(f"- 理论文档总数：{len(self.theory_files)}\n")
            f.write(f"- 发现割裂问题总数：{total_issues}\n")
            f.write(f"- 代码缺理论绑定：{len(self.results['missing_comments'])}\n")
            f.write(f"- 参数割裂：{len(self.results['parameter_mismatch'])}\n")
            f.write(f"- 双向断层：{len(self.results['bidirectional_gap'])}\n")
            f.write(f"- 数理逻辑割裂：{len(self.results['logic_mismatch'])}\n")
            f.write(f"- 集合关系违背：{len(self.results['set_relationship'])}\n")
            f.write(f"- 跨文件常量冲突：{len(self.results['global_constant_conflict'])}\n")
            f.write(f"- 运行时覆写风险：{len(self.results['runtime_override'])}\n")
            f.write("\n")

            if total_issues == 0:
                f.write("### ✅ 检测通过\n\n")
                f.write("所有代码文件均已正确绑定理论，参数与理论锁档数值一致，双向映射完整。\n")
                f.write("数理逻辑与公理公式符号对齐，集合关系约束满足 Ω_CB ⊂ Ω_FB。\n")
                f.write("\n")
                f.write("---\n\n")
                f.write("## 版权声明\n\n")
                f.write("本报告由理论-代码割裂检测工具自动生成，所有内容受著作权保护。\n")
                f.write("检测工具版本：V2.0（增强版）\n")
                f.write("理论基准：V3.0 Rev.04 四位一体驻波动力学框架\n")
                return

            if self.results["missing_comments"]:
                f.write("## 一、代码缺理论绑定\n\n")
                f.write("| 文件路径 | 问题类型 | 缺失字段 |\n")
                f.write("|----------|----------|----------|\n")
                for issue in self.results["missing_comments"]:
                    missing = issue.get("missing_fields", [])
                    if missing:
                        f.write(f"| {issue['file']} | {issue['type']} | {', '.join(missing)} |\n")
                    else:
                        class_name = issue.get("class", "")
                        f.write(f"| {issue['file']} ({class_name}) | {issue['type']} | - |\n")
                f.write("\n")

            if self.results["parameter_mismatch"]:
                f.write("## 二、参数割裂\n\n")
                f.write("| 文件路径 | 变量名 | 实际值 | 期望值 | 问题描述 |\n")
                f.write("|----------|--------|--------|--------|----------|\n")
                for issue in self.results["parameter_mismatch"]:
                    f.write(f"| {issue['file']} | {issue['var']} | {issue['actual']} | {issue['expected']} | {issue['desc']} |\n")
                f.write("\n")

            if self.results["global_constant_conflict"]:
                f.write("## 三、跨文件常量冲突\n\n")
                for issue in self.results["global_constant_conflict"]:
                    f.write(f"### {issue['var']}\n\n")
                    f.write(f"- 问题描述：{issue['desc']}\n")
                    f.write("| 文件路径 | 值 | 行号 |\n")
                    f.write("|----------|-----|------|\n")
                    for conflict in issue["conflicts"]:
                        f.write(f"| {conflict['file']} | {conflict['value']} | {conflict['line']} |\n")
                    f.write("\n")

            if self.results["logic_mismatch"]:
                f.write("## 四、数理逻辑割裂\n\n")
                f.write("| 文件路径 | 变量/运算 | 问题描述 |\n")
                f.write("|----------|-----------|----------|\n")
                for issue in self.results["logic_mismatch"]:
                    var_or_op = issue.get("var", "") or issue.get("operation", "")
                    f.write(f"| {issue['file']} | {var_or_op} | {issue['desc']} |\n")
                f.write("\n")

            if self.results["set_relationship"]:
                f.write("## 五、集合关系违背\n\n")
                f.write("⚠️ 以下文件涉及舒适边界(Ω_CB)和宿命边界(Ω_FB)，但未实现子集约束检查\n\n")
                f.write("| 文件路径 | 问题描述 |\n")
                f.write("|----------|----------|\n")
                for issue in self.results["set_relationship"]:
                    f.write(f"| {issue['file']} | {issue['desc']} |\n")
                f.write("\n")

            if self.results["runtime_override"]:
                f.write("## 六、运行时覆写风险\n\n")
                f.write("⚠️ 以下拓展模块可能覆写core全局常量，违反只读约束\n\n")
                f.write("| 文件路径 | 问题描述 |\n")
                f.write("|----------|----------|\n")
                for issue in self.results["runtime_override"]:
                    f.write(f"| {issue['file']} | {issue['desc']} |\n")
                f.write("\n")

            if self.results["bidirectional_gap"]:
                f.write("## 七、双向断层\n\n")
                f.write("| 问题类型 | 涉及文件 | 描述 |\n")
                f.write("|----------|----------|------|\n")
                for issue in self.results["bidirectional_gap"]:
                    if "theory_file" in issue:
                        f.write(f"| {issue['type']} | {issue['theory_file']} → {issue['code_path']} | {issue['desc']} |\n")
                    else:
                        f.write(f"| {issue['type']} | {issue['code_file']} | {issue['desc']} |\n")
                f.write("\n")

            f.write("---\n\n")
            f.write("## 修复建议\n\n")
            f.write("1. **代码缺理论绑定**：为文件头部添加标准化注释模板，包含归属基底、对应公理、九维维度等信息；\n")
            f.write("2. **参数割裂**：将代码中的常量值修正为理论锁档数值，并添加理论注释；\n")
            f.write("3. **跨文件常量冲突**：统一使用configs配置文件管理常量，禁止在代码中硬编码；\n")
            f.write("4. **数理逻辑割裂**：检查条件判断阈值、数学运算是否与公理公式一致；\n")
            f.write("5. **集合关系违背**：为涉及边界的代码添加 Ω_CB ⊂ Ω_FB 子集约束检查；\n")
            f.write("6. **运行时覆写风险**：禁止extend模块修改core导出的全局常量；\n")
            f.write("7. **双向断层**：理论有内容无代码时需补充实现，代码无理论支撑时需在理论文档中添加映射条目；\n")
            f.write("8. 所有割裂缺陷修复后，重新运行本检测工具，确保报告显示\"检测通过\"后方可归档。\n")
            f.write("\n")
            f.write("---\n\n")
            f.write("## 版权声明\n\n")
            f.write("本报告由理论-代码割裂检测工具自动生成，所有内容受著作权保护。\n")
            f.write("检测工具版本：V2.0（增强版）\n")
            f.write("理论基准：V3.0 Rev.04 四位一体驻波动力学框架\n")

        print(f"[INFO] 割裂缺陷报告已生成：{output_path}")


if __name__ == "__main__":
    checker = TheoryCodeCouplingChecker()
    checker.run_full_check()
    checker.generate_report()

    total = sum(len(v) for v in checker.results.values())
    if total == 0:
        print("\n✅ 检测通过：所有代码文件均已正确绑定理论！")
    else:
        print(f"\n❌ 发现 {total} 个割裂问题，请查看报告进行修复。")
