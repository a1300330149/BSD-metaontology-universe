"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道秩序
对应公理：第6条（全局宿命边界统摄理论）、第1条（宿命/舒适双边界公理）
对应九维维度：天道原理/天道动力学
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：SHA256锁档哈希、版本标签过滤权重

场3-2：RAG全局检索哈希过滤机制
实现检索时自动过滤过期向量、版本标签权重控制、0/1重基底优先召回
对应盲区整改：优先级0-盲区1（RAG知识库静态缺陷）、优先级0-盲区3（长上下文衰减）
"""

import os
import json
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"
CURRENT_VERSION = "V3.0"
VALID_VERSIONS = ["V3.0"]
DEPRECATED_VERSIONS = ["V2.0", "V1.0", "草稿", "废弃"]

BASE_PRIORITY_DOCS = [
    "本体拓扑位（第一位）.md",
    "规则相位位（第二位）.md",
    "元本体理论分册.md",
    "四位一体驻波动力学框架本源知识库.md",
    "宇宙基底层级定义.md"
]

PROJECT_ROOT = Path(__file__).parent.parent
KB_CONFIG_PATH = PROJECT_ROOT / ".trae" / "docs.json"
THEORY_BASE_PATH = PROJECT_ROOT / "theory_base"


class RAGHashFilter:
    """
    功能：RAG检索哈希过滤器
    理论映射：规则相位位（第二位）·全局宿命边界统摄理论
    约束来源：优先级0-盲区1、优先级0-盲区3整改方案
    核心能力：版本过滤、哈希匹配、基底优先召回
    """

    def __init__(self):
        self.valid_file_hashes = set()
        self.valid_file_paths = set()
        self.base_priority_files = set()
        self.deprecated_files = set()
        self.load_config()

    def load_config(self) -> None:
        """加载知识库配置，构建有效文件哈希集合"""
        if not KB_CONFIG_PATH.exists():
            print(f"[WARNING] 知识库配置文件不存在: {KB_CONFIG_PATH}")
            return

        with open(KB_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)

        for file_entry in config.get("files", []):
            file_hash = file_entry.get("hash", "")
            file_path = file_entry.get("path", "")
            full_path = file_entry.get("fullPath", "")

            if self._is_valid_version(file_path, full_path):
                self.valid_file_hashes.add(file_hash)
                self.valid_file_paths.add(file_path)

                if self._is_base_priority(file_path):
                    self.base_priority_files.add(file_path)
            else:
                self.deprecated_files.add(file_path)

        print(f"[INFO] 加载有效文件: {len(self.valid_file_paths)} 个")
        print(f"[INFO] 加载有效哈希: {len(self.valid_file_hashes)} 个")
        print(f"[INFO] 基底优先级文件: {len(self.base_priority_files)} 个")
        print(f"[INFO] 已废弃文件: {len(self.deprecated_files)} 个")

    def _is_valid_version(self, file_path: str, full_path: str) -> bool:
        """判断文件是否为有效版本"""
        file_name = os.path.basename(file_path)

        if any(v in file_name for v in VALID_VERSIONS):
            return True

        if any(v in file_name for v in DEPRECATED_VERSIONS):
            return False

        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read(500)
                if any(v in content for v in DEPRECATED_VERSIONS):
                    return False
                if any(v in content for v in VALID_VERSIONS):
                    return True
        except Exception:
            pass

        return True

    def _is_base_priority(self, file_path: str) -> bool:
        """判断文件是否为基底优先级文档"""
        file_name = os.path.basename(file_path)
        return any(base_name.lower() in file_name.lower() for base_name in BASE_PRIORITY_DOCS)

    def filter_by_hash(self, retrieved_docs: List[Dict]) -> List[Dict]:
        """
        根据哈希过滤检索结果
        参数：retrieved_docs - 原始检索结果列表，每个文档包含file_path和content字段
        返回：过滤后的文档列表，只保留有效版本的文档
        """
        filtered = []
        rejected = []

        for doc in retrieved_docs:
            file_path = doc.get("file_path", "")
            content = doc.get("content", "")

            if file_path in self.valid_file_paths:
                filtered.append(doc)
            else:
                rejected.append({
                    "file_path": file_path,
                    "reason": "hash_not_in_valid_set"
                })

        if rejected:
            print(f"[INFO] RAG哈希过滤：保留 {len(filtered)} 篇，过滤 {len(rejected)} 篇过期文档")

        return filtered

    def apply_version_weight(self, retrieved_docs: List[Dict]) -> List[Dict]:
        """
        应用版本权重
        废弃版本文档权重置0，V3.0版本权重为1.0
        """
        for doc in retrieved_docs:
            file_path = doc.get("file_path", "")

            if file_path in self.deprecated_files:
                doc["version_weight"] = 0.0
                doc["version_status"] = "deprecated"
            elif file_path in self.valid_file_paths:
                doc["version_weight"] = 1.0
                doc["version_status"] = "valid"
            else:
                doc["version_weight"] = 0.5
                doc["version_status"] = "unknown"

        return retrieved_docs

    def prioritize_base_docs(self, retrieved_docs: List[Dict]) -> List[Dict]:
        """
        确保基底优先级文档优先召回
        将0/1重基底文档置顶，权重提升
        对应整改：优先级0-盲区3（长上下文衰减）
        """
        base_docs = []
        other_docs = []

        for doc in retrieved_docs:
            file_path = doc.get("file_path", "")
            if file_path in self.base_priority_files:
                doc["priority_weight"] = 2.0
                doc["is_base_priority"] = True
                base_docs.append(doc)
            else:
                doc["priority_weight"] = 1.0
                doc["is_base_priority"] = False
                other_docs.append(doc)

        return base_docs + other_docs

    def filter_and_prioritize(self, retrieved_docs: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        完整过滤流程：哈希过滤 → 版本权重 → 基底优先
        返回：(过滤后的文档列表, 过滤统计信息)
        """
        initial_count = len(retrieved_docs)

        docs = self.filter_by_hash(retrieved_docs)
        hash_filtered_count = len(docs)

        docs = self.apply_version_weight(docs)
        docs = self.prioritize_base_docs(docs)

        stats = {
            "initial_count": initial_count,
            "hash_filtered_count": hash_filtered_count,
            "final_count": len(docs),
            "base_priority_count": sum(1 for d in docs if d.get("is_base_priority", False)),
            "deprecated_count": initial_count - hash_filtered_count
        }

        return docs, stats

    def validate_retrieval_context(self, retrieved_docs: List[Dict]) -> Dict:
        """
        验证检索上下文是否满足理论约束
        检查：1. 是否包含0/1重基底文档 2. 是否包含锁档哈希
        """
        has_base_0 = False
        has_base_1 = False
        has_lock_hash = False

        for doc in retrieved_docs:
            content = doc.get("content", "")
            file_path = doc.get("file_path", "")

            if "0重" in file_path or "道本源" in file_path:
                has_base_0 = True
            if "1重" in file_path or "九维法理" in file_path:
                has_base_1 = True
            if LOCK_HASH in content:
                has_lock_hash = True

        return {
            "has_base_0": has_base_0,
            "has_base_1": has_base_1,
            "has_lock_hash": has_lock_hash,
            "is_valid": has_base_0 and has_base_1 and has_lock_hash,
            "missing": [
                "0重本源基底" if not has_base_0 else "",
                "规则相位位（第二位）" if not has_base_1 else "",
                "锁档哈希" if not has_lock_hash else ""
            ]
        }

    def generate_filter_report(self, retrieved_docs: List[Dict]) -> str:
        """生成过滤报告"""
        docs, stats = self.filter_and_prioritize(retrieved_docs)
        validation = self.validate_retrieval_context(docs)

        report = f"""# RAG检索哈希过滤报告

## 过滤统计

| 指标 | 数值 |
|------|------|
| 原始检索数量 | {stats['initial_count']} |
| 哈希过滤后数量 | {stats['hash_filtered_count']} |
| 最终保留数量 | {stats['final_count']} |
| 基底优先级文档 | {stats['base_priority_count']} |
| 过滤废弃文档 | {stats['deprecated_count']} |

## 理论约束验证

| 约束项 | 状态 |
|--------|------|
| 包含0重本源基底 | {'✅ 是' if validation['has_base_0'] else '❌ 否'} |
| 包含规则相位位（第二位） | {'✅ 是' if validation['has_base_1'] else '❌ 否'} |
| 包含锁档哈希 | {'✅ 是' if validation['has_lock_hash'] else '❌ 否'} |

"""

        if validation['missing']:
            report += "\n## 缺失项\n\n"
            for item in validation['missing']:
                if item:
                    report += f"- ⚠️ 缺少：{item}\n"
        else:
            report += "\n## 缺失项\n\n- ✅ 所有理论约束均满足\n"

        report += "\n## 文档列表\n\n"
        report += "| 优先级 | 文件路径 | 版本状态 |\n"
        report += "|--------|----------|----------|\n"

        for doc in docs:
            priority = "基底优先" if doc.get("is_base_priority", False) else "普通"
            version = doc.get("version_status", "unknown")
            report += f"| {priority} | `{doc.get('file_path', '')}` | {version} |\n"

        report += "\n---\n"
        report += "本报告由RAG哈希过滤机制自动生成\n"
        report += f"锁档哈希：{LOCK_HASH}\n"

        return report


def simulate_retrieval(test_docs: int = 10) -> List[Dict]:
    """模拟RAG检索结果"""
    docs = []

    if THEORY_BASE_PATH.exists():
        md_files = list(THEORY_BASE_PATH.glob("**/*.md"))
        sample_files = md_files[:test_docs]

        for i, file_path in enumerate(sample_files):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read(200)

            docs.append({
                "file_path": str(file_path.relative_to(THEORY_BASE_PATH)),
                "full_path": str(file_path),
                "content": content,
                "score": 1.0 - i * 0.05
            })

    return docs


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-2：RAG全局检索哈希过滤机制")
    print(f"归属基底：第规则相位位（第二位）")
    print(f"对应公理：公理六（全局宿命边界统摄理论）")
    print(f"锁档哈希：{LOCK_HASH}")
    print("=" * 60)

    filter = RAGHashFilter()

    print("\n[STEP 1] 模拟RAG检索...")
    retrieved_docs = simulate_retrieval()
    print(f"[INFO] 模拟检索到 {len(retrieved_docs)} 篇文档")

    print("\n[STEP 2] 执行哈希过滤与优先级排序...")
    filtered_docs, stats = filter.filter_and_prioritize(retrieved_docs)

    print(f"\n[RESULT] 过滤统计：")
    print(f"  原始: {stats['initial_count']} | 过滤后: {stats['final_count']}")
    print(f"  基底优先级: {stats['base_priority_count']}")

    print("\n[STEP 3] 验证理论约束...")
    validation = filter.validate_retrieval_context(filtered_docs)

    print(f"  包含0重本源基底: {'✅' if validation['has_base_0'] else '❌'}")
    print(f"  包含规则相位位（第二位）: {'✅' if validation['has_base_1'] else '❌'}")
    print(f"  包含锁档哈希: {'✅' if validation['has_lock_hash'] else '❌'}")

    if validation['is_valid']:
        print("\n[SUCCESS] ✅ 理论约束验证通过")
    else:
        print("\n[WARNING] ⚠️ 理论约束验证失败，缺少以下项：")
        for item in validation['missing']:
            if item:
                print(f"  - {item}")

    print("\n[STEP 4] 生成过滤报告...")
    report = filter.generate_filter_report(retrieved_docs)
    report_path = PROJECT_ROOT / "RAG检索过滤报告.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"[SUCCESS] 过滤报告已生成: {report_path}")

    print("\n" + "=" * 60)
    print("RAG哈希过滤机制测试完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
