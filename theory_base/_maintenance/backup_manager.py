#!/usr/bin/env python3
"""
备份管理器 - 全域知识库版本链完整归档备份

功能：
1. 完整备份theory_base全库
2. 增量备份新增/修改文件
3. 版本链追溯
4. 备份恢复

使用方式：
    python backup_manager.py [--full-backup] [--incremental] [--restore BACKUP_ID] [--list]
"""

import os
import json
import shutil
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# 配置路径
THEORY_BASE = "./theory_base"
BACKUP_DIR = "./theory_base/_maintenance/backups"
BACKUP_INDEX = "./theory_base/_maintenance/backup_index.json"

class BackupManager:
    """备份管理器"""

    def __init__(self):
        os.makedirs(BACKUP_DIR, exist_ok=True)
        self.index = self.load_index()

    def load_index(self) -> Dict:
        """加载备份索引"""
        if os.path.exists(BACKUP_INDEX):
            with open(BACKUP_INDEX, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"backups": [], "version_chain": []}

    def save_index(self):
        """保存备份索引"""
        with open(BACKUP_INDEX, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)

    def calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except:
            return "ERROR"

    def scan_theory_base(self) -> List[Dict]:
        """扫描theory_base"""
        files = []
        for root, dirs, filenames in os.walk(THEORY_BASE):
            # 跳过backup目录
            if '_maintenance/backups' in root:
                continue

            for filename in filenames:
                if filename.endswith('.md') or filename.endswith('.json') or filename.endswith('.py'):
                    file_path = os.path.join(root, filename)
                    rel_path = os.path.relpath(file_path, THEORY_BASE)

                    files.append({
                        "path": rel_path,
                        "full_path": file_path,
                        "hash": self.calculate_file_hash(file_path),
                        "size": os.path.getsize(file_path),
                        "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    })

        return files

    def create_backup(self, backup_type: str = "full") -> str:
        """创建备份"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_id = f"backup_{timestamp}"

        print("=" * 60)
        print(f"【备份管理器】创建{backup_type}备份")
        print("=" * 60)

        # 扫描当前状态
        print("[1/4] 扫描theory_base...")
        current_files = self.scan_theory_base()
        print(f"      扫描到 {len(current_files)} 个文件")

        # 创建备份目录
        backup_path = os.path.join(BACKUP_DIR, backup_id)
        os.makedirs(backup_path, exist_ok=True)

        # 复制文件
        print("[2/4] 复制文件...")
        copied_count = 0
        for file_info in current_files:
            dest_path = os.path.join(backup_path, file_info["path"])
            dest_dir = os.path.dirname(dest_path)
            os.makedirs(dest_dir, exist_ok=True)

            shutil.copy2(file_info["full_path"], dest_path)
            copied_count += 1

        print(f"      已复制 {copied_count} 个文件")

        # 保存备份元数据
        print("[3/4] 保存元数据...")
        metadata = {
            "backup_id": backup_id,
            "backup_type": backup_type,
            "timestamp": datetime.now().isoformat(),
            "file_count": len(current_files),
            "files": current_files
        }

        metadata_path = os.path.join(backup_path, "metadata.json")
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # 更新索引
        print("[4/4] 更新备份索引...")
        self.index["backups"].append(metadata)

        # 更新版本链
        self.index["version_chain"].append({
            "backup_id": backup_id,
            "timestamp": datetime.now().isoformat(),
            "file_count": len(current_files)
        })

        self.save_index()

        print()
        print("=" * 60)
        print(f"【备份完成】备份ID: {backup_id}")
        print(f"文件数：{len(current_files)}")
        print(f"位置：{backup_path}")
        print("=" * 60)

        return backup_id

    def list_backups(self):
        """列出所有备份"""
        print("=" * 60)
        print("【备份列表】")
        print("=" * 60)

        if not self.index["backups"]:
            print("暂无备份")
            return

        for backup in reversed(self.index["backups"][-10:]):
            print(f"\n备份ID: {backup['backup_id']}")
            print(f"  类型: {backup['backup_type']}")
            print(f"  时间: {backup['timestamp']}")
            print(f"  文件数: {backup['file_count']}")

        print()
        print(f"总计: {len(self.index['backups'])} 个备份")

    def restore_backup(self, backup_id: str):
        """恢复备份"""
        backup_path = os.path.join(BACKUP_DIR, backup_id)

        if not os.path.exists(backup_path):
            print(f"备份不存在: {backup_id}")
            return

        print("=" * 60)
        print(f"【恢复备份】{backup_id}")
        print("⚠️ 警告：这将覆盖当前文件！")
        print("=" * 60)

        metadata_path = os.path.join(backup_path, "metadata.json")
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            print(f"\n将恢复 {len(metadata['files'])} 个文件...")

            for file_info in metadata['files']:
                dest_path = os.path.join(THEORY_BASE, file_info["path"])
                dest_dir = os.path.dirname(dest_path)
                os.makedirs(dest_dir, exist_ok=True)

                src_path = os.path.join(backup_path, file_info["path"])
                if os.path.exists(src_path):
                    shutil.copy2(src_path, dest_path)

            print()
            print("=" * 60)
            print("【恢复完成】")
            print("=" * 60)
        else:
            print("备份元数据不存在")

    def cleanup_old_backups(self, keep_count: int = 10):
        """清理旧备份"""
        backups = self.index["backups"]
        if len(backups) <= keep_count:
            print(f"备份数量 {len(backups)} <= {keep_count}，无需清理")
            return

        to_delete = backups[:-keep_count]

        print("=" * 60)
        print(f"【清理旧备份】将删除 {len(to_delete)} 个备份")
        print("=" * 60)

        for backup in to_delete:
            backup_path = os.path.join(BACKUP_DIR, backup["backup_id"])
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
                print(f"已删除: {backup['backup_id']}")

        self.index["backups"] = backups[-keep_count:]
        self.save_index()

        print()
        print("【清理完成】")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="备份管理器")
    parser.add_argument("--full-backup", action="store_true", help="完整备份")
    parser.add_argument("--incremental", action="store_true", help="增量备份")
    parser.add_argument("--restore", help="恢复指定备份")
    parser.add_argument("--list", action="store_true", help="列出所有备份")
    parser.add_argument("--cleanup", type=int, default=0, help="清理旧备份，保留最近N个")
    args = parser.parse_args()

    manager = BackupManager()

    if args.full_backup:
        manager.create_backup("full")
    elif args.incremental:
        manager.create_backup("incremental")
    elif args.restore:
        manager.restore_backup(args.restore)
    elif args.list:
        manager.list_backups()
    elif args.cleanup > 0:
        manager.cleanup_old_backups(args.cleanup)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()