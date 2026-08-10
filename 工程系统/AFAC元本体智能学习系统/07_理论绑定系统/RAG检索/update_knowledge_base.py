"""
归属基底：3重六阶自主科研业务基底
对应三界秩序：人道
对应公理：第7条系统自进化迭代公理
对应九维维度：创化社会
理论原文出处：theory_base/四位一体驻波动力学框架本源知识库：0-4重基底完整理论文档合集.md
核心数理参数：无
"""
import os
import json
import hashlib
from pathlib import Path

KB_CONFIG_PATH = Path(__file__).parent.parent / ".trae" / "docs.json"
THEORY_BASE_PATH = Path(__file__).parent.parent / "theory_base"

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def scan_theory_files(base_path):
    md_files = []
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'node_modules']]
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                rel_path = file_path.relative_to(base_path)
                file_hash = calculate_file_hash(file_path)
                file_size = os.path.getsize(file_path)
                md_files.append({
                    "path": str(rel_path),
                    "fullPath": str(file_path),
                    "hash": file_hash,
                    "size": file_size,
                    "lastModified": os.path.getmtime(file_path)
                })
    return md_files

def update_knowledge_base():
    print("=" * 60)
    print("四位一体驻波动力学框架本源知识库更新工具")
    print("=" * 60)
    
    if not THEORY_BASE_PATH.exists():
        print(f"错误：理论基底目录不存在: {THEORY_BASE_PATH}")
        return
    
    print(f"\n扫描理论文件目录: {THEORY_BASE_PATH}")
    md_files = scan_theory_files(THEORY_BASE_PATH)
    print(f"找到 {len(md_files)} 个 Markdown 文件")
    
    if KB_CONFIG_PATH.exists():
        with open(KB_CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"\n现有知识库配置版本: {config.get('version', '未知')}")
        print(f"现有知识库描述: {config.get('description', '未知')}")
    else:
        config = {
            "name": "四位一体驻波动力学框架本源知识库",
            "description": "V3.0 Rev.04 四位一体驻波动力学框架理论文档集",
            "version": "3.0.04",
            "hash": "e62f918340dc2975108294736ac8927d90584136972485931027958740925713",
            "author": "杨腾飞",
            "lockDate": "2026-06-20",
            "basePath": "./theory_base",
            "indexConfig": {
                "chunkSize": 500,
                "chunkOverlap": 50,
                "maxDepth": 3,
                "includePatterns": ["*.md"],
                "excludePatterns": ["__pycache__", ".git", "node_modules"]
            },
            "metadata": {
                "ontologyVersion": "3.0",
                "foundationLayers": ["0重元道本源", "1重九维法理", "2重三界秩序", "3重六阶科研", "4重智能体执行"],
                "axioms": 7,
                "dimensions": 9,
                "threeRealms": ["天道", "自然", "人道"]
            }
        }
    
    config["files"] = md_files
    config["totalFiles"] = len(md_files)
    config["lastUpdated"] = str(os.path.getmtime(__file__))
    
    with open(KB_CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 知识库配置已更新到: {KB_CONFIG_PATH}")
    print(f"📁 索引文件数量: {len(md_files)}")
    print(f"🔒 锁档哈希: {config['hash']}")
    print(f"📅 锁档日期: {config['lockDate']}")
    
    print("\n" + "=" * 60)
    print("知识库更新完成！请在 Trae IDE 中重新加载文档集")
    print("=" * 60)

if __name__ == "__main__":
    update_knowledge_base()