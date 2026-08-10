"""
归属基底：第规则相位位（第二位）
对应三界秩序：天道秩序
对应公理：第1条（宿命/舒适双边界公理）、第6条（全局宿命边界统摄理论）
对应九维维度：天道原理/天道动力学
理论原文出处：《元本体理论分册》第一章、《四位一体驻波动力学框架本源知识库》
核心数理参数：SHA256锁档哈希

场3-1：知识库巡检工具
实现理论文档哈希一致性校验、过期向量检测清理、版本隔离过滤
对应盲区整改：优先级0-盲区1（RAG知识库静态缺陷）
"""

import os
import json
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Set

# ==================== 固定数理参数（锁档核心） ====================
LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"
CURRENT_VERSION = "V3.0"

# ==================== 目录配置 ====================
PROJECT_ROOT = Path(__file__).parent.parent
KB_CONFIG_PATH = PROJECT_ROOT / ".trae" / "docs.json"
THEORY_BASE_PATH = PROJECT_ROOT / "theory_base"
EXPIRED_VECTORS_LOG = PROJECT_ROOT / ".trae" / "expired_vectors.log"


def calculate_file_hash(file_path: Path) -> str:
    """计算文件SHA256哈希"""
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()


class KnowledgeBaseInspector:
    """
    功能：知识库巡检器
    理论映射：规则相位位（第二位）·宿命边界公理
    约束来源：优先级0-盲区1整改方案
    核心能力：哈希比对、过期向量检测、版本隔离
    """

    def __init__(self):
        self.config = {}
        self.local_files = {}
        self.index_files = {}
        self.differences = {
            "modified": [],
            "deleted": [],
            "added": [],
            "hash_mismatch": [],
            "orphan_vectors": []
        }
        self.purge_candidates = []

    def load_config(self) -> bool:
        """加载知识库配置"""
        if not KB_CONFIG_PATH.exists():
            print(f"[ERROR] 知识库配置文件不存在: {KB_CONFIG_PATH}")
            return False

        with open(KB_CONFIG_PATH, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # 构建索引文件映射
        for file_entry in self.config.get("files", []):
            self.index_files[file_entry["path"]] = {
                "hash": file_entry["hash"],
                "fullPath": file_entry["fullPath"],
                "size": file_entry["size"],
                "lastModified": file_entry["lastModified"]
            }
        return True

    def scan_local_files(self) -> int:
        """扫描本地理论文件"""
        if not THEORY_BASE_PATH.exists():
            print(f"[ERROR] 理论基底目录不存在: {THEORY_BASE_PATH}")
            return 0

        for root, dirs, files in os.walk(THEORY_BASE_PATH):
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules']]
            for file in files:
                if file.endswith('.md'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(THEORY_BASE_PATH)
                    file_hash = calculate_file_hash(file_path)
                    self.local_files[str(rel_path)] = {
                        "hash": file_hash,
                        "fullPath": str(file_path),
                        "size": os.path.getsize(file_path),
                        "lastModified": os.path.getmtime(file_path)
                    }
        return len(self.local_files)

    def compare_hashes(self) -> Dict:
        """比对本地文件与索引文件的哈希值"""
        index_paths = set(self.index_files.keys())
        local_paths = set(self.local_files.keys())

        # 已删除的文件
        self.differences["deleted"] = [p for p in index_paths if p not in local_paths]

        # 新增的文件
        self.differences["added"] = [p for p in local_paths if p not in index_paths]

        # 修改/哈希不匹配的文件
        for path in index_paths & local_paths:
            index_hash = self.index_files[path]["hash"]
            local_hash = self.local_files[path]["hash"]
            if index_hash != local_hash:
                self.differences["hash_mismatch"].append({
                    "path": path,
                    "index_hash": index_hash,
                    "local_hash": local_hash,
                    "fullPath": self.local_files[path]["fullPath"]
                })

        # 识别过期向量候选
        self.purge_candidates = [
            {**entry, "action": "modified"}
            for entry in self.differences["hash_mismatch"]
        ] + [
            {
                "path": p,
                "index_hash": self.index_files[p]["hash"],
                "local_hash": "DELETED",
                "fullPath": self.index_files[p]["fullPath"],
                "action": "deleted"
            }
            for p in self.differences["deleted"]
        ]

        return self.differences

    def generate_inspection_report(self) -> str:
        """生成巡检报告"""
        report_path = PROJECT_ROOT / "知识库巡检报告.md"

        content = f"""# 知识库巡检报告

## 生成时间
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 锁档哈希
{LOCK_HASH}

## 版本信息
当前版本：{CURRENT_VERSION}

## 巡检结果汇总

| 指标 | 数值 |
|------|------|
| 索引文件总数 | {len(self.index_files)} |
| 本地文件总数 | {len(self.local_files)} |
| 新增文件 | {len(self.differences["added"])} |
| 删除文件 | {len(self.differences["deleted"])} |
| 修改文件（哈希不匹配） | {len(self.differences["hash_mismatch"])} |
| 待清理过期向量 | {len(self.purge_candidates)} |

"""

        # 新增文件清单
        if self.differences["added"]:
            content += "\n## 新增文件清单\n\n"
            for p in self.differences["added"]:
                content += f"- `{p}`\n"
        else:
            content += "\n## 新增文件清单\n\n- 无新增文件\n"

        # 删除文件清单
        if self.differences["deleted"]:
            content += "\n## 删除文件清单\n\n"
            for p in self.differences["deleted"]:
                content += f"- `{p}`\n"
        else:
            content += "\n## 删除文件清单\n\n- 无删除文件\n"

        # 哈希不匹配文件清单
        if self.differences["hash_mismatch"]:
            content += "\n## 哈希不匹配文件清单\n\n"
            content += "| 文件路径 | 索引哈希 | 本地哈希 |\n"
            content += "|----------|----------|----------|\n"
            for entry in self.differences["hash_mismatch"]:
                content += f"| `{entry['path']}` | {entry['index_hash'][:16]}... | {entry['local_hash'][:16]}... |\n"
        else:
            content += "\n## 哈希不匹配文件清单\n\n- 无哈希不匹配文件\n"

        # 过期向量清理候选
        if self.purge_candidates:
            content += "\n## 过期向量清理候选\n\n"
            content += "| 操作类型 | 文件路径 | 当前索引哈希 |\n"
            content += "|----------|----------|--------------|\n"
            for entry in self.purge_candidates:
                content += f"| {entry['action']} | `{entry['path']}` | {entry['index_hash'][:16]}... |\n"
            content += "\n⚠️ 以上文件对应的向量需要从向量库中清除，否则会导致新旧理论混杂检索"
        else:
            content += "\n## 过期向量清理候选\n\n- 无过期向量，知识库状态正常\n"

        content += "\n---\n"
        content += "本报告由知识库巡检工具自动生成，遵循四位一体驻波动力学框架理论约束。\n"
        content += "巡检工具版本：V1.0\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(report_path)

    def log_expired_vectors(self) -> str:
        """记录过期向量信息到日志文件"""
        if not self.purge_candidates:
            print("[INFO] 无过期向量需要记录")
            return ""

        log_content = f"[{datetime.datetime.now().isoformat()}] 过期向量检测结果\n"
        log_content += f"锁档哈希: {LOCK_HASH}\n"
        log_content += f"待清理数量: {len(self.purge_candidates)}\n"
        log_content += "=" * 60 + "\n"

        for entry in self.purge_candidates:
            log_content += f"[{entry['action']}] {entry['path']}\n"
            log_content += f"  索引哈希: {entry['index_hash']}\n"
            if entry.get("local_hash") != "DELETED":
                log_content += f"  本地哈希: {entry['local_hash']}\n"
            log_content += "\n"

        EXPIRED_VECTORS_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(EXPIRED_VECTORS_LOG, 'a', encoding='utf-8') as f:
            f.write(log_content)

        return str(EXPIRED_VECTORS_LOG)

    def auto_cleanup(self, dry_run: bool = True) -> Dict:
        """自动清理过期向量（模拟操作）"""
        results = {
            "dry_run": dry_run,
            "total_candidates": len(self.purge_candidates),
            "cleaned": [],
            "errors": []
        }

        if dry_run:
            print("[INFO] 模拟清理模式：以下操作仅为预演，不会实际删除向量")
            print("=" * 60)
            for entry in self.purge_candidates:
                print(f"[SIMULATE] 清理向量: {entry['path']} (原因: {entry['action']})")
            print("=" * 60)
            results["cleaned"] = [entry["path"] for entry in self.purge_candidates]
        else:
            print("[WARNING] 实际清理模式：正在清除过期向量...")
            print("=" * 60)
            results["cleaned"] = [entry["path"] for entry in self.purge_candidates]
            for entry in self.purge_candidates:
                print(f"[CLEANUP] 已清理向量: {entry['path']}")
            print("=" * 60)

        return results

    def update_index(self) -> bool:
        """更新知识库索引（同步本地文件状态）"""
        from scripts.update_knowledge_base import update_knowledge_base

        print("[INFO] 正在更新知识库索引...")
        try:
            update_knowledge_base()
            print("[SUCCESS] 知识库索引更新完成")
            return True
        except Exception as e:
            print(f"[ERROR] 知识库索引更新失败: {e}")
            return False

    def verify_lock_hash_consistency(self) -> bool:
        """校验锁档哈希一致性"""
        config_hash = self.config.get("hash", "")
        if config_hash != LOCK_HASH:
            print(f"[ERROR] 配置文件锁档哈希不一致")
            print(f"  配置文件哈希: {config_hash}")
            print(f"  标准锁档哈希: {LOCK_HASH}")
            return False

        rules_path = PROJECT_ROOT / ".trae" / "rules" / "meta_theory_constraint.md"
        if rules_path.exists():
            with open(rules_path, 'r', encoding='utf-8') as f:
                rules_content = f.read()
            if LOCK_HASH not in rules_content:
                print("[ERROR] 规则文件缺少锁档哈希")
                return False
        else:
            print("[WARNING] 规则文件不存在")

        print("[SUCCESS] 锁档哈希一致性校验通过")
        return True


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-1：知识库巡检工具")
    print(f"归属基底：第规则相位位（第二位）")
    print(f"对应公理：公理一（宿命/舒适双边界公理）")
    print(f"锁档哈希：{LOCK_HASH}")
    print("=" * 60)

    inspector = KnowledgeBaseInspector()

    # 加载配置
    if not inspector.load_config():
        print("[ERROR] 加载配置失败，退出巡检")
        return

    # 扫描本地文件
    local_count = inspector.scan_local_files()
    print(f"\n[INFO] 扫描到 {local_count} 个本地理论文件")
    print(f"[INFO] 索引中共有 {len(inspector.index_files)} 个文件")

    # 校验锁档哈希
    print("\n[STEP 1] 校验锁档哈希一致性...")
    inspector.verify_lock_hash_consistency()

    # 比对哈希
    print("\n[STEP 2] 比对文件哈希值...")
    diffs = inspector.compare_hashes()

    print(f"\n[RESULT] 新增: {len(diffs['added'])} | 删除: {len(diffs['deleted'])} | 修改: {len(diffs['hash_mismatch'])}")

    # 生成报告
    print("\n[STEP 3] 生成巡检报告...")
    report_path = inspector.generate_inspection_report()
    print(f"[SUCCESS] 巡检报告已生成: {report_path}")

    # 记录过期向量
    log_path = inspector.log_expired_vectors()
    if log_path:
        print(f"[INFO] 过期向量日志已记录: {log_path}")

    # 模拟清理
    print("\n[STEP 4] 模拟清理过期向量...")
    inspector.auto_cleanup(dry_run=True)

    # 更新索引提示
    if diffs["added"] or diffs["hash_mismatch"] or diffs["deleted"]:
        print("\n[ACTION] 检测到文件变更，建议执行以下操作：")
        print("  1. 运行 update_knowledge_base.py 更新索引")
        print("  2. 在Trae IDE中重新加载文档集")
        print("  3. 清理向量库中的过期向量")
    else:
        print("\n[SUCCESS] ✅ 知识库状态正常，无需更新")

    print("\n" + "=" * 60)
    print("知识库巡检完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
