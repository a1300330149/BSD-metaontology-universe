"""
Phase 0 迁移验证测试
验证所有迁移文件的完整性和可导入性
"""
import os
import ast
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_constants_locked():
    """验证锁档参数未被篡改"""
    from bsd_engine.registry.constants import verify_params, ALL_LOCKED_PARAMS
    assert verify_params() is True
    assert ALL_LOCKED_PARAMS["E1"] == 0.35
    assert ALL_LOCKED_PARAMS["E2"] == 0.65
    assert ALL_LOCKED_PARAMS["E3"] == 0.90
    assert ALL_LOCKED_PARAMS["GAMMA"] == 0.92
    assert ALL_LOCKED_PARAMS["KAPPA"] == 0.35
    assert ALL_LOCKED_PARAMS["KAPPA_COMPETITION"] == 0.42
    assert ALL_LOCKED_PARAMS["ALPHA"] == 0.18
    assert ALL_LOCKED_PARAMS["THETA_NEG"] == 0.02
    assert ALL_LOCKED_PARAMS["THETA_MV"] == 0.005
    assert ALL_LOCKED_PARAMS["THETA_EVO"] == 0.002

def test_hash_integrity():
    """验证确权哈希"""
    from bsd_engine.registry.constants import HASH_SHA256, AUTHOR, AUTHOR_ID
    assert HASH_SHA256 == "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"
    assert AUTHOR == "杨腾飞"
    assert AUTHOR_ID == "433127199812193215"

def test_core_modules_count():
    """验证core模块迁移完整性"""
    core_dir = os.path.join(PROJECT_ROOT, "bsd_engine", "core")
    py_files = [f for f in os.listdir(core_dir) if f.endswith('.py') and f != '__init__.py']
    assert len(py_files) == 26, f"期望26个core模块，实际{len(py_files)}个"

def test_theories_modules_count():
    """验证theories模块迁移完整性"""
    th_dir = os.path.join(PROJECT_ROOT, "bsd_engine", "theories")
    py_files = [f for f in os.listdir(th_dir) if f.endswith('.py') and f != '__init__.py']
    assert len(py_files) >= 80, f"期望至少80个theory模块，实际{len(py_files)}个"

def test_validators_modules_count():
    """验证validators模块迁移完整性"""
    v_dir = os.path.join(PROJECT_ROOT, "bsd_engine", "validators")
    py_files = [f for f in os.listdir(v_dir) if f.endswith('.py') and f != '__init__.py']
    assert len(py_files) >= 4, f"期望至少4个validator模块，实际{len(py_files)}个"

def test_all_syntax_ok():
    """验证所有.py文件语法正确"""
    errors = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        dirs[:] = [d for d in dirs if d != '__pycache__' and d != '.git']
        for f in files:
            if f.endswith('.py'):
                path = os.path.join(root, f)
                try:
                    with open(path, 'r', encoding='utf-8-sig') as fh:
                        ast.parse(fh.read(), filename=path)
                except SyntaxError as e:
                    errors.append(f'{path}: {e}')
    assert len(errors) == 0, f"语法错误: {errors}"

def test_core_bsd_annotations():
    """验证core模块的BSD标注注释存在"""
    core_dir = os.path.join(PROJECT_ROOT, "bsd_engine", "core")
    missing = []
    for f in os.listdir(core_dir):
        if f.endswith('.py') and f != '__init__.py':
            path = os.path.join(core_dir, f)
            with open(path, 'r', encoding='utf-8-sig') as fh:
                content = fh.read(500)  # 只读前500字符
            if '归属基底' not in content:
                missing.append(f)
    assert len(missing) == 0, f"缺少BSD标注的文件: {missing}"

def test_validators_bsd_annotations():
    """验证validators模块的BSD标注注释存在"""
    v_dir = os.path.join(PROJECT_ROOT, "bsd_engine", "validators")
    missing = []
    for f in os.listdir(v_dir):
        if f.endswith('.py') and f != '__init__.py':
            path = os.path.join(v_dir, f)
            with open(path, 'r', encoding='utf-8-sig') as fh:
                content = fh.read(500)
            if '归属基底' not in content:
                missing.append(f)
    assert len(missing) == 0, f"缺少BSD标注的文件: {missing}"

def test_directory_structure():
    """验证目录结构完整性"""
    required_dirs = [
        "bsd_engine",
        "bsd_engine/core",
        "bsd_engine/theories",
        "bsd_engine/axioms",
        "bsd_engine/equations",
        "bsd_engine/registry",
        "bsd_engine/validators",
        "bsd_sim",
        "bsd_agents",
        "bsd_mcp",
        "bsd_verify",
        "bsd_verify/millennium",
        "tests",
        "tests/unit",
    ]
    for d in required_dirs:
        path = os.path.join(PROJECT_ROOT, d)
        assert os.path.isdir(path), f"目录不存在: {d}"

def test_pyproject_exists():
    """验证pyproject.toml存在"""
    assert os.path.isfile(os.path.join(PROJECT_ROOT, "pyproject.toml"))

def test_license_exists():
    """验证LICENSE存在"""
    assert os.path.isfile(os.path.join(PROJECT_ROOT, "LICENSE"))
