"""
【归属基底：L0_总本源层·0元本体论大一统】
【对应公理：公理0·元道存在】

TheoryHub —— 理论模块单例注册中心
所有理论模块统一注册、统一管理、统一验证
"""

import json
from typing import Dict, List, Optional, Type, Any
from .base_theory_module import BaseTheoryModule


class TheoryHub:
    """
    理论注册中心（单例模式）
    
    功能：
    1. 统一注册所有理论模块
    2. 依赖关系自动校验
    3. 本源锁定状态检查
    4. 层级完整性自检
    """

    _instance = None
    _modules: Dict[str, BaseTheoryModule] = {}
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, module: BaseTheoryModule) -> bool:
        """注册一个理论模块"""
        if module.module_id in self._modules:
            return False
        self._modules[module.module_id] = module
        module._registered = True
        return True

    def unregister(self, module_id: str) -> bool:
        """注销一个理论模块"""
        if module_id in self._modules:
            del self._modules[module_id]
            return True
        return False

    def get(self, module_id: str) -> Optional[BaseTheoryModule]:
        """获取指定理论模块"""
        return self._modules.get(module_id)

    def get_all(self) -> Dict[str, BaseTheoryModule]:
        """获取所有已注册模块"""
        return dict(self._modules)

    def get_by_level(self, level: int) -> List[BaseTheoryModule]:
        """按层级获取模块"""
        return [m for m in self._modules.values() if m.cosmic_level == level]

    def get_origin_locked(self) -> List[BaseTheoryModule]:
        """获取所有本源锁定模块"""
        return [m for m in self._modules.values() if m.is_origin_locked]

    def validate_dependencies(self) -> Dict[str, Any]:
        """校验所有模块的依赖关系"""
        results = {
            "total_modules": len(self._modules),
            "passed": 0,
            "failed": 0,
            "details": {}
        }
        for mid, mod in self._modules.items():
            missing = [dep for dep in mod.dependencies if dep not in self._modules]
            if missing:
                results["failed"] += 1
                results["details"][mid] = {"status": "FAIL", "missing_deps": missing}
            else:
                results["passed"] += 1
                results["details"][mid] = {"status": "PASS"}
        return results

    def validate_all(self) -> Dict[str, Any]:
        """对所有模块执行完整自检验证"""
        results = {
            "total_modules": len(self._modules),
            "passed": 0,
            "failed": 0,
            "details": {}
        }
        for mid, mod in self._modules.items():
            ok, errors = mod.validate()
            if ok:
                results["passed"] += 1
                results["details"][mid] = {"status": "PASS"}
            else:
                results["failed"] += 1
                results["details"][mid] = {"status": "FAIL", "errors": errors}
        return results

    def integrity_report(self) -> str:
        """生成完整性报告"""
        dep_result = self.validate_dependencies()
        val_result = self.validate_all()
        origin_locked = self.get_origin_locked()
        levels = {}
        for m in self._modules.values():
            lvl = f"L{m.cosmic_level}"
            levels[lvl] = levels.get(lvl, 0) + 1

        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           理论注册中心 · 完整性自检报告                       ║
╠══════════════════════════════════════════════════════════════╣
║  总模块数         : {len(self._modules):<47}║
║  本源锁定数       : {len(origin_locked):<47}║
║  依赖校验通过     : {dep_result['passed']:<47}║
║  依赖校验失败     : {dep_result['failed']:<47}║
║  完整自检通过     : {val_result['passed']:<47}║
║  完整自检失败     : {val_result['failed']:<47}║
╠══════════════════════════════════════════════════════════════╣
║  层级分布                                                    ║
"""
        for lvl in sorted(levels.keys()):
            report += f"║    {lvl:<10}     : {levels[lvl]:<43}║\n"
        report += "╚══════════════════════════════════════════════════════════════╝"
        return report

    def to_json(self) -> str:
        """导出所有模块信息为JSON"""
        data = {mid: m.get_info() for mid, m in self._modules.items()}
        return json.dumps(data, ensure_ascii=False, indent=2)

    def clear(self):
        """清空所有模块（测试用）"""
        self._modules.clear()
