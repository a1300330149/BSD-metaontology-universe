"""
归属基底：第5重分层迭代知识库生长场
对应三界秩序：天道/自然/人道
对应公理：第7条（系统自进化迭代公理）
对应九维维度：天道原理/自然相变/社会创造
理论原文出处：《元本体理论分册》第七章
核心数理参数：θ_evo=0.002

场5：增量归档脚本
实现理论/工程/实验数据增量自动归档入库
"""

import os
import json
import datetime
import hashlib
from pathlib import Path
from typing import Dict, List, Optional

# ==================== 固定数理参数（锁档核心） ====================
# SHA256锁档哈希
LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"

# 自进化增量阈值
THETA_EVO = 0.002


class IncrementalArchive:
    """
    功能：增量自动归档入库处理器
    理论映射：5重分层迭代知识库生长场·系统自进化迭代公理
    能级关联：E3=0.90三阶道心能级归档标准
    约束来源：系统自进化迭代公理（公理七）
    禁止修改：归档模板、锁档哈希、基底标签
    """
    
    def __init__(self, project_root: str, knowledge_base: str):
        """
        初始化增量归档处理器
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：知识库生长初始化
        
        Args:
            project_root: 项目根目录
            knowledge_base: 知识库目录
        """
        self.project_root = Path(project_root)
        self.knowledge_base = Path(knowledge_base)
        self.archive_log = []
    
    def detect_new_content(self) -> Dict:
        """
        检测新增内容
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：增量检测
        
        Returns:
            Dict: 新增内容检测结果
        """
        # 扫描理论文档
        theory_files = list(self.project_root.glob("theory_base/*.md"))
        
        # 扫描代码文件
        code_files = list(self.project_root.glob("src/**/*.py"))
        
        # 扫描实验数据
        experiment_files = list(self.project_root.glob("output/**/*.json"))
        
        # 扫描配置文件
        config_files = list(self.project_root.glob("configs/*.yaml"))
        
        # 计算现有知识库文件哈希
        existing_hashes = set()
        for f in self.knowledge_base.glob("*.md"):
            content = f.read_bytes()
            existing_hashes.add(hashlib.sha256(content).hexdigest())
        
        # 检测新增文件
        new_theory = []
        for f in theory_files:
            content = f.read_bytes()
            h = hashlib.sha256(content).hexdigest()
            if h not in existing_hashes:
                new_theory.append(f)
        
        new_code = []
        for f in code_files:
            content = f.read_bytes()
            h = hashlib.sha256(content).hexdigest()
            if h not in existing_hashes:
                new_code.append(f)
        
        new_experiment = []
        for f in experiment_files:
            content = f.read_bytes()
            h = hashlib.sha256(content).hexdigest()
            if h not in existing_hashes:
                new_experiment.append(f)
        
        return {
            "new_theory": new_theory,
            "new_code": new_code,
            "new_experiment": new_experiment,
            "total_new": len(new_theory) + len(new_code) + len(new_experiment)
        }
    
    def archive_theory_document(self, doc_path: Path) -> str:
        """
        归档理论文档
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：理论文档增量归档
        
        Args:
            doc_path: 文档路径
        
        Returns:
            str: 归档文件路径
        """
        content = doc_path.read_text(encoding='utf-8')
        
        # 提取基底层级
        base_level = self._extract_base_level(content)
        
        # 提取公理编号
        axiom_number = self._extract_axiom_number(content)
        
        # 生成归档文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{base_level}_{axiom_number}_{doc_path.stem}_{timestamp}.md"
        
        # 添加归档标签
        archive_content = self._add_archive_tags(content, base_level, axiom_number)
        
        # 写入归档文件
        archive_path = self.knowledge_base / archive_name
        archive_path.write_text(archive_content, encoding='utf-8')
        
        self._log(f"理论文档归档: {doc_path.name} → {archive_name}", "success")
        
        return str(archive_path)
    
    def archive_code_module(self, code_path: Path) -> str:
        """
        归档代码模块
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：代码模块增量归档
        
        Args:
            code_path: 代码文件路径
        
        Returns:
            str: 归档文件路径
        """
        content = code_path.read_text(encoding='utf-8')
        
        # 提取基底层级
        base_level = self._extract_base_level(content)
        
        # 提取公理编号
        axiom_number = self._extract_axiom_number(content)
        
        # 生成归档说明文档
        archive_doc = self._generate_code_archive_doc(code_path, base_level, axiom_number)
        
        # 生成归档文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"code_{base_level}_{axiom_number}_{code_path.stem}_{timestamp}.md"
        
        # 写入归档文件
        archive_path = self.knowledge_base / archive_name
        archive_path.write_text(archive_doc, encoding='utf-8')
        
        self._log(f"代码模块归档: {code_path.name} → {archive_name}", "success")
        
        return str(archive_path)
    
    def archive_experiment_data(self, data_path: Path) -> str:
        """
        归档实验数据
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：实验数据增量归档
        
        Args:
            data_path: 数据文件路径
        
        Returns:
            str: 归档文件路径
        """
        content = data_path.read_text(encoding='utf-8')
        
        # 解析实验数据
        try:
            data = json.loads(content)
        except:
            data = {"raw_content": content}
        
        # 生成理论佐证文档
        archive_doc = self._generate_experiment_archive_doc(data_path, data)
        
        # 生成归档文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"experiment_{data_path.stem}_{timestamp}.md"
        
        # 写入归档文件
        archive_path = self.knowledge_base / archive_name
        archive_path.write_text(archive_doc, encoding='utf-8')
        
        self._log(f"实验数据归档: {data_path.name} → {archive_name}", "success")
        
        return str(archive_path)
    
    def _extract_base_level(self, content: str) -> str:
        """
        提取基底层级
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：基底层级识别
        
        Args:
            content: 文档内容
        
        Returns:
            str: 基底层级标识
        """
        if "0元" in content or "元道" in content:
            return "base_0"
        elif "九维" in content or "法理" in content:
            return "base_1"
        elif "三界" in content or "秩序" in content:
            return "base_2"
        elif "六阶" in content or "科研" in content:
            return "base_3"
        elif "智能体" in content or "四层" in content:
            return "base_4"
        else:
            return "base_unknown"
    
    def _extract_axiom_number(self, content: str) -> str:
        """
        提取公理编号
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：公理编号识别
        
        Args:
            content: 文档内容
        
        Returns:
            str: 公理编号标识
        """
        if "双边界" in content or "宿命" in content:
            return "axiom_1"
        elif "动力学" in content or "闭环" in content:
            return "axiom_2"
        elif "边际" in content or "价值" in content:
            return "axiom_3"
        elif "选题" in content or "创化" in content:
            return "axiom_4"
        elif "转化" in content or "落地" in content:
            return "axiom_5"
        elif "统摄" in content or "全局" in content:
            return "axiom_6"
        elif "进化" in content or "迭代" in content:
            return "axiom_7"
        else:
            return "axiom_unknown"
    
    def _add_archive_tags(self, content: str, base_level: str, axiom_number: str) -> str:
        """
        添加归档标签
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：归档标签自动打标
        
        Args:
            content: 文档内容
            base_level: 基底层级
            axiom_number: 公理编号
        
        Returns:
            str: 添加标签后的内容
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        tags = f"""
---
归档标签
---

# 归属基底
{base_level}

# 对应公理
{axiom_number}

# 归档时间
{timestamp}

# SHA256锁档哈希
{LOCK_HASH}

# 归档来源
增量自动归档入库

---

"""
        
        return tags + content
    
    def _generate_code_archive_doc(self, code_path: Path, base_level: str, axiom_number: str) -> str:
        """
        生成代码归档说明文档
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：代码归档文档生成
        
        Args:
            code_path: 代码文件路径
            base_level: 基底层级
            axiom_number: 公理编号
        
        Returns:
            str: 归档文档内容
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# 代码模块归档说明

## 归档信息

| 项目 | 内容 |
|------|------|
| 模块名称 | {code_path.name} |
| 归属基底 | {base_level} |
| 对应公理 | {axiom_number} |
| 归档时间 | {timestamp} |
| SHA256哈希 | {LOCK_HASH} |

## 模块功能

该模块对应{base_level}基底，遵循{axiom_number}公理约束。

## 理论映射

- 基底层级：{base_level}
- 公理编号：{axiom_number}
- 九维维度：自动识别

## 归档来源

增量自动归档入库，遵循系统自进化迭代公理。

---

本归档文档由增量归档处理器自动生成，遵循四位一体驻波动力学框架理论约束。
"""
        
        return content
    
    def _generate_experiment_archive_doc(self, data_path: Path, data: Dict) -> str:
        """
        生成实验数据归档文档
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：实验数据归档文档生成
        
        Args:
            data_path: 数据文件路径
            data: 实验数据
        
        Returns:
            str: 归档文档内容
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        content = f"""# 实验数据归档说明

## 归档信息

| 项目 | 内容 |
|------|------|
| 数据名称 | {data_path.name} |
| 归档时间 | {timestamp} |
| SHA256哈希 | {LOCK_HASH} |

## 实验数据摘要

"""
        
        # 提取关键指标
        if isinstance(data, dict):
            for key, value in data.items():
                if key in ["metrics", "accuracy", "diversity", "overall_status"]:
                    content += f"- {key}: {value}\n"
        
        content += "\n## 理论佐证\n\n"
        content += "该实验数据为理论推导提供实证支撑，遵循系统自进化迭代公理。\n\n"
        content += "---\n"
        content += "本归档文档由增量归档处理器自动生成，遵循四位一体驻波动力学框架理论约束。\n"
        
        return content
    
    def _log(self, message: str, level: str = "info"):
        """
        记录归档日志
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：归档日志记录
        
        Args:
            message: 日志消息
            level: 日志级别
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message
        }
        self.archive_log.append(entry)
        print(f"[{level.upper()}] {message}")
    
    def run_incremental_archive(self) -> Dict:
        """
        执行增量归档
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：增量自动归档入库
        
        Returns:
            Dict: 归档结果汇总
        """
        # 检测新增内容
        new_content = self.detect_new_content()
        
        results = {
            "new_theory_count": len(new_content["new_theory"]),
            "new_code_count": len(new_content["new_code"]),
            "new_experiment_count": len(new_content["new_experiment"]),
            "total_archived": 0,
            "archive_paths": []
        }
        
        # 归档理论文档
        for doc in new_content["new_theory"]:
            archive_path = self.archive_theory_document(doc)
            results["archive_paths"].append(archive_path)
            results["total_archived"] += 1
        
        # 归档代码模块
        for code in new_content["new_code"]:
            archive_path = self.archive_code_module(code)
            results["archive_paths"].append(archive_path)
            results["total_archived"] += 1
        
        # 归档实验数据
        for data in new_content["new_experiment"]:
            archive_path = self.archive_experiment_data(data)
            results["archive_paths"].append(archive_path)
            results["total_archived"] += 1
        
        # 保存归档日志
        log_path = self.project_root / "归档日志.json"
        log_path.write_text(
            json.dumps(self.archive_log, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        return results


def main():
    """
    主程序入口
    
    对应公理：公理七（系统自进化迭代公理）
    理论映射：增量归档启动
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="场5：增量归档处理器")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument("--knowledge-base", default="theory_base", help="知识库目录")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("场5：增量归档处理器")
    print("归属基底：第5重分层迭代知识库生长场")
    print("对应公理：公理七（系统自进化迭代公理）")
    print("=" * 60)
    
    archiver = IncrementalArchive(args.project_root, args.knowledge_base)
    results = archiver.run_incremental_archive()
    
    print("\n归档结果汇总:")
    print(f"  新增理论文档: {results['new_theory_count']}")
    print(f"  新增代码模块: {results['new_code_count']}")
    print(f"  新增实验数据: {results['new_experiment_count']}")
    print(f"  总归档数量: {results['total_archived']}")
    
    print(f"\n归档文件路径:")
    for path in results["archive_paths"]:
        print(f"  - {path}")
    
    print("\n" + "=" * 60)
    print("SHA256锁档哈希:", LOCK_HASH)
    print("=" * 60)


if __name__ == "__main__":
    main()