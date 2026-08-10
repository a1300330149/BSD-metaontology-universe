"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道秩序
对应公理：第6条（全局宿命边界统摄理论）、第1条（宿命/舒适双边界公理）
对应九维维度：天道原理/天道动力学
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：SHA256全局总哈希

场3-6：归档全局总SHA256计算工具
实现项目全局哈希计算、写入归档说明书、交付唯一校验指纹
对应盲区整改：优先级4-盲区12（归档无全局哈希）
"""

import os
import hashlib
import json
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent
ARCHIVE_DIR = PROJECT_ROOT / "archive"
INCLUDE_DIRS = ["src", "scripts", "theory_base", ".trae/rules"]
IGNORE_PATTERNS = [
    "__pycache__",
    ".git",
    "node_modules",
    ".trae/cache",
    ".trae/sessions",
    ".egg-info",
    "dist",
    "build",
    "*.pyc",
    "*.egg",
    "*.log",
    "*.tmp",
    "*.bak",
    "output",
    "results",
    "experiments",
    "archive",
]

FILE_TYPES_TO_HASH = [".py", ".md", ".yaml", ".yml", ".json", ".txt"]


class ArchiveHashCalculator:
    """
    功能：归档全局哈希计算器
    理论映射：规则相位位（第二位）·全局宿命边界统摄理论
    约束来源：优先级4-盲区12整改方案
    核心能力：全局哈希计算、文件指纹收集、校验报告生成
    """

    def __init__(self):
        self.file_hashes = {}
        self.global_hash = ""
        self.total_files = 0
        self.hash_timestamp = ""

    def _should_ignore(self, path: Path) -> bool:
        """判断是否应该忽略该路径"""
        for pattern in IGNORE_PATTERNS:
            if pattern.startswith("*."):
                suffix = pattern[1:]
                if path.suffix == suffix:
                    return True
            else:
                if pattern in str(path):
                    return True
        return False

    def _calculate_file_hash(self, file_path: Path) -> str:
        """计算单个文件的SHA256哈希"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(chunk)
            return sha256_hash.hexdigest()
        except Exception:
            return ""

    def scan_and_hash(self, root_dir: Path = None) -> Dict[str, str]:
        """
        扫描指定目录并计算所有文件的哈希
        参数：root_dir - 根目录，默认为PROJECT_ROOT
        返回：文件路径到哈希的映射
        """
        if root_dir is None:
            root_dir = PROJECT_ROOT

        file_hashes = {}

        for include_dir in INCLUDE_DIRS:
            include_path = root_dir / include_dir
            if not include_path.exists():
                continue

            for current_dir, dirs, files in os.walk(include_path):
                dirs[:] = [d for d in dirs if not self._should_ignore(Path(current_dir) / d)]

                for file in files:
                    file_path = Path(current_dir) / file

                    if self._should_ignore(file_path):
                        continue

                    if file_path.suffix in FILE_TYPES_TO_HASH:
                        file_hash = self._calculate_file_hash(file_path)
                        if file_hash:
                            rel_path = file_path.relative_to(root_dir)
                            file_hashes[str(rel_path)] = file_hash

        self.file_hashes = file_hashes
        self.total_files = len(file_hashes)
        return file_hashes

    def calculate_global_hash(self) -> str:
        """
        计算项目全局总SHA256哈希
        将所有文件哈希按路径排序后连接，再计算总哈希
        """
        if not self.file_hashes:
            self.scan_and_hash()

        sorted_paths = sorted(self.file_hashes.keys())
        combined_hash = "".join(self.file_hashes[path] for path in sorted_paths)

        global_sha256 = hashlib.sha256(combined_hash.encode('utf-8'))
        self.global_hash = global_sha256.hexdigest()
        self.hash_timestamp = datetime.datetime.now().isoformat()

        return self.global_hash

    def generate_archive_report(self) -> str:
        """生成归档哈希报告"""
        report_path = ARCHIVE_DIR / "成果归档清单.md"
        ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

        content = f"""# 成果归档清单

## 归档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | 四位一体驻波动力学框架体系 |
| 版本 | V3.0 |
| 归档时间 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 全局总哈希 | `{self.global_hash}` |
| 文件总数 | {self.total_files} |

## 全局哈希计算说明

### 计算规则
1. 遍历项目根目录下所有文件
2. 忽略临时文件、缓存目录、日志文件等
3. 仅计算 `.py`, `.md`, `.yaml`, `.yml`, `.json`, `.txt` 类型文件
4. 按文件路径字典序排序所有文件哈希
5. 将排序后的哈希值拼接为字符串
6. 对拼接字符串计算SHA256得到全局总哈希

### 全局哈希指纹
```
{self.global_hash}
```

### 哈希时间戳
```
{self.hash_timestamp}
```

## 文件哈希清单

### 统计信息

| 类型 | 文件数 |
|------|--------|
| Python文件 (.py) | {sum(1 for p in self.file_hashes.keys() if p.endswith('.py'))} |
| Markdown文件 (.md) | {sum(1 for p in self.file_hashes.keys() if p.endswith('.md'))} |
| JSON文件 (.json) | {sum(1 for p in self.file_hashes.keys() if p.endswith('.json'))} |
| YAML文件 (.yaml/.yml) | {sum(1 for p in self.file_hashes.keys() if p.endswith('.yaml') or p.endswith('.yml'))} |
| 其他文本文件 (.txt) | {sum(1 for p in self.file_hashes.keys() if p.endswith('.txt'))} |

### 文件哈希详细列表

| 文件路径 | SHA256哈希 |
|----------|------------|
"""

        for path in sorted(self.file_hashes.keys()):
            content += f"| `{path}` | `{self.file_hashes[path]}` |\n"

        content += "\n---\n\n"
        content += "## 版权声明\n\n"
        content += "本归档清单由归档全局哈希计算器自动生成\n"
        content += "全局哈希作为交付唯一校验指纹，可用于验证归档包完整性\n"
        content += "理论基准：四位一体驻波动力学框架\n"
        content += "锁档哈希：e62f918340dc2975108294736ac8927d90584136972485931027958740925713\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[INFO] 归档清单已生成: {report_path}")
        return str(report_path)

    def export_hash_manifest(self) -> str:
        """导出哈希清单为JSON格式"""
        manifest = {
            "global_hash": self.global_hash,
            "timestamp": self.hash_timestamp,
            "total_files": self.total_files,
            "file_hashes": self.file_hashes,
            "project": "四位一体驻波动力学框架体系",
            "version": "V3.0"
        }

        manifest_path = ARCHIVE_DIR / "hash_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        print(f"[INFO] 哈希清单JSON已导出: {manifest_path}")
        return str(manifest_path)

    def verify_archive(self, archive_dir: Path) -> Tuple[bool, Dict]:
        """
        验证归档包完整性
        参数：archive_dir - 归档目录路径
        返回：(是否完整, 验证详情)
        """
        original_hash = self.global_hash
        calculator = ArchiveHashCalculator()
        calculator.scan_and_hash(archive_dir)
        archive_hash = calculator.calculate_global_hash()

        is_valid = original_hash == archive_hash
        result = {
            "original_hash": original_hash,
            "archive_hash": archive_hash,
            "is_valid": is_valid,
            "original_file_count": self.total_files,
            "archive_file_count": calculator.total_files,
            "timestamp": datetime.datetime.now().isoformat()
        }

        if is_valid:
            print("[SUCCESS] ✅ 归档包完整性校验通过")
        else:
            print("[ERROR] ❌ 归档包完整性校验失败 - 哈希不匹配")

        return is_valid, result

    def run_full_archive(self) -> Dict:
        """执行完整归档流程"""
        print("=" * 60)
        print("场3-6：归档全局总SHA256计算工具")
        print(f"归属基底：第规则相位位（第二位）")
        print(f"对应公理：公理六（全局宿命边界统摄理论）")
        print("=" * 60)

        print("\n[STEP 1] 扫描文件并计算哈希...")
        file_hashes = self.scan_and_hash()
        print(f"[INFO] 扫描到 {self.total_files} 个文件")

        print("\n[STEP 2] 计算全局总哈希...")
        global_hash = self.calculate_global_hash()
        print(f"[INFO] 全局总哈希: {global_hash}")

        print("\n[STEP 3] 生成归档清单...")
        report_path = self.generate_archive_report()

        print("\n[STEP 4] 导出哈希清单JSON...")
        manifest_path = self.export_hash_manifest()

        print("\n" + "=" * 60)
        print("归档全局哈希计算完成！")
        print(f"全局总哈希: {global_hash}")
        print("=" * 60)

        return {
            "global_hash": global_hash,
            "total_files": self.total_files,
            "hash_timestamp": self.hash_timestamp,
            "report_path": report_path,
            "manifest_path": manifest_path
        }


def main():
    """主程序入口"""
    calculator = ArchiveHashCalculator()
    result = calculator.run_full_archive()

    print(f"\n[RESULT] 归档完成：")
    print(f"  全局总哈希: {result['global_hash']}")
    print(f"  文件总数: {result['total_files']}")
    print(f"  归档清单: {result['report_path']}")
    print(f"  哈希清单: {result['manifest_path']}")


if __name__ == "__main__":
    main()
