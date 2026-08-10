"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（成果落地转化范式）
对应九维维度：社会因果/社会创造
理论原文出处：《六阶自主科研架构论文》第五章
核心数理参数：θ_mv=0.005

场3：文档批量标准化脚本
实现理论文档批量标准化处理
"""

import os
import re
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ==================== 固定数理参数（锁档核心） ====================
# SHA256锁档哈希
LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"

# 确权扉页模板（锁档核心，禁止修改）
STANDARD_HEADER = """---
确权扉页
---

# 作品全称
V3.0 Rev.04 新四位一体框架3.0元本体论（专属理论分册）

# SHA256唯一锁档哈希
e62f918340dc2975108294736ac8927d90584136972485931027958740925713

# 作者/著作权人
杨腾飞（证件号码：433127199812193215）

# 锁档定稿日期
2026-06-20

# 三维协同确权
创世作者：杨腾飞（60%）
墨心推演：AI辅助（25%）
豆包运维：AI辅助（15%）

---

"""


class DocumentStandardizer:
    """
    功能：文档批量标准化处理器
    理论映射：3重六阶自主科研业务基底·成果落地转化范式
    能级关联：E3=0.90三阶道心能级验收标准
    约束来源：成果落地转化范式（公理五）
    禁止修改：确权扉页模板、锁档哈希、权属文字
    """
    
    def __init__(self, project_root: str):
        """
        初始化文档标准化处理器
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档标准化初始化
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root)
        self.docs_path = self.project_root / "docs"
        self.theory_path = self.project_root / "theory_base"
        self.standardization_log = []
    
    def scan_documents(self) -> List[Path]:
        """
        扫描所有md文档
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档扫描
        
        Returns:
            List[Path]: 文档路径列表
        """
        all_docs = []
        
        # 扫描docs目录
        if self.docs_path.exists():
            all_docs.extend(self.docs_path.glob("*.md"))
        
        # 扫描theory_base目录
        if self.theory_path.exists():
            all_docs.extend(self.theory_path.glob("*.md"))
        
        # 扫描根目录md文件
        all_docs.extend(self.project_root.glob("*.md"))
        
        return all_docs
    
    def check_header_integrity(self, doc_path: Path) -> Dict:
        """
        检查文档扉页完整性
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：确权扉页校验
        
        Args:
            doc_path: 文档路径
        
        Returns:
            Dict: 校验结果
        """
        content = doc_path.read_text(encoding='utf-8')
        
        checks = {
            "has_hash": LOCK_HASH in content,
            "has_author": "杨腾飞" in content,
            "has_id": "433127199812193215" in content,
            "has_date": "2026-06-20" in content,
            "has_rights": "创世作者" in content and "墨心推演" in content and "豆包运维" in content
        }
        
        integrity_score = sum(1 for v in checks.values() if v) / len(checks)
        
        return {
            "file": doc_path.name,
            "checks": checks,
            "integrity_score": integrity_score,
            "needs_header": integrity_score < 0.8
        }
    
    def insert_standard_header(self, doc_path: Path) -> bool:
        """
        插入标准确权扉页
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：确权扉页插入
        
        Args:
            doc_path: 文档路径
        
        Returns:
            bool: 是否成功插入
        """
        content = doc_path.read_text(encoding='utf-8')
        
        # 检查是否已有扉页
        if LOCK_HASH in content and "杨腾飞" in content:
            self._log(f"{doc_path.name}: 已有完整扉页，跳过插入", "info")
            return False
        
        # 插入扉页
        new_content = STANDARD_HEADER + content
        doc_path.write_text(new_content, encoding='utf-8')
        
        self._log(f"{doc_path.name}: 成功插入标准扉页", "success")
        return True
    
    def remove_ai_remarks(self, doc_path: Path) -> int:
        """
        清除AI冗余备注
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档格式规整
        
        Args:
            doc_path: 文档路径
        
        Returns:
            int: 清除的备注数量
        """
        content = doc_path.read_text(encoding='utf-8')
        
        # AI冗余备注模式
        ai_patterns = [
            r"注：部分内容可能由AI生成",
            r"AI辅助创作",
            r"自动生成内容",
            r"AI生成",
            r"机器生成"
        ]
        
        removed_count = 0
        for pattern in ai_patterns:
            matches = re.findall(pattern, content)
            removed_count += len(matches)
            content = re.sub(pattern, "", content)
        
        if removed_count > 0:
            doc_path.write_text(content, encoding='utf-8')
            self._log(f"{doc_path.name}: 清除{removed_count}个AI冗余备注", "success")
        
        return removed_count
    
    def normalize_title_levels(self, doc_path: Path) -> int:
        """
        统一标题层级
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档格式规整
        
        Args:
            doc_path: 文档路径
        
        Returns:
            int: 修正的标题数量
        """
        content = doc_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        fixed_count = 0
        for i, line in enumerate(lines):
            # 检查标题层级
            if line.startswith('#'):
                # 计算当前层级
                level = len(line) - len(line.lstrip('#'))
                
                # 修正层级（确保1-3级）
                if level > 3:
                    # 降级到3级
                    new_line = '###' + line.lstrip('#')
                    lines[i] = new_line
                    fixed_count += 1
        
        if fixed_count > 0:
            new_content = '\n'.join(lines)
            doc_path.write_text(new_content, encoding='utf-8')
            self._log(f"{doc_path.name}: 修正{fixed_count}个标题层级", "success")
        
        return fixed_count
    
    def remove_duplicates(self, doc_path: Path) -> int:
        """
        删除重复段落
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档冗余消除
        
        Args:
            doc_path: 文档路径
        
        Returns:
            int: 删除的重复段落数量
        """
        content = doc_path.read_text(encoding='utf-8')
        
        # 按段落分割
        paragraphs = content.split('\n\n')
        
        # 检测重复段落
        seen = set()
        unique_paragraphs = []
        removed_count = 0
        
        for para in paragraphs:
            # 标准化段落（去除空白差异）
            normalized = para.strip()
            
            if normalized not in seen and len(normalized) > 10:
                seen.add(normalized)
                unique_paragraphs.append(para)
            elif normalized in seen:
                removed_count += 1
        
        if removed_count > 0:
            new_content = '\n\n'.join(unique_paragraphs)
            doc_path.write_text(new_content, encoding='utf-8')
            self._log(f"{doc_path.name}: 删除{removed_count}个重复段落", "success")
        
        return removed_count
    
    def add_appendix(self, doc_path: Path) -> bool:
        """
        补充附录符号表
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档附录补充
        
        Args:
            doc_path: 文档路径
        
        Returns:
            bool: 是否成功添加
        """
        content = doc_path.read_text(encoding='utf-8')
        
        # 检查是否已有附录
        if "核心符号对照表" in content or "附录" in content:
            self._log(f"{doc_path.name}: 已有附录，跳过添加", "info")
            return False
        
        # 添加附录模板
        appendix = """

---

## 附录：核心符号对照表

| 符号 | 含义 | 锁档值 |
|------|------|------|
| γ | 时序衰减系数 | 0.92 |
| κ | 虚实阻尼系数 | 0.35 |
| α | 稀疏补偿系数 | 0.18 |
| E₁ | 一阶肉身能级阈值 | 0.35 |
| E₂ | 二阶精神能级阈值 | 0.65 |
| E₃ | 三阶道心能级阈值 | 0.90 |
| θ_mv | 科研边际价值判定阈值 | 0.005 |
| θ_evo | 自进化增量阈值 | 0.002 |
| θ_neg | 负迁移判定阈值 | 0.02 |

---

"""
        
        new_content = content + appendix
        doc_path.write_text(new_content, encoding='utf-8')
        
        self._log(f"{doc_path.name}: 成功添加附录符号表", "success")
        return True
    
    def _log(self, message: str, level: str = "info"):
        """
        记录标准化日志
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：自校验日志
        
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
        self.standardization_log.append(entry)
        print(f"[{level.upper()}] {message}")
    
    def run_batch_standardization(self) -> Dict:
        """
        执行批量标准化
        
        对应公理：公理五（成果落地转化范式）
        理论映射：文档批量标准化处理
        
        Returns:
            Dict: 标准化结果汇总
        """
        docs = self.scan_documents()
        
        results = {
            "total_docs": len(docs),
            "headers_inserted": 0,
            "ai_remarks_removed": 0,
            "titles_fixed": 0,
            "duplicates_removed": 0,
            "appendix_added": 0,
            "defect_docs": []
        }
        
        for doc in docs:
            # 检查扉页完整性
            check = self.check_header_integrity(doc)
            if check["needs_header"]:
                self.insert_standard_header(doc)
                results["headers_inserted"] += 1
            
            # 清除AI冗余备注
            removed = self.remove_ai_remarks(doc)
            results["ai_remarks_removed"] += removed
            
            # 统一标题层级
            fixed = self.normalize_title_levels(doc)
            results["titles_fixed"] += fixed
            
            # 删除重复段落
            duplicates = self.remove_duplicates(doc)
            results["duplicates_removed"] += duplicates
            
            # 补充附录
            added = self.add_appendix(doc)
            results["appendix_added"] += added
        
        # 保存日志
        log_path = self.project_root / "文档标准化日志.json"
        log_path.write_text(
            str(self.standardization_log).replace("'", '"'),
            encoding='utf-8'
        )
        
        return results
    
    def generate_defect_report(self) -> str:
        """
        生成版权校验缺陷报告
        
        对应公理：公理五（成果落地转化范式）
        理论映射：版权缺陷报告输出
        
        Returns:
            str: 报告文件路径
        """
        docs = self.scan_documents()
        
        defect_docs = []
        for doc in docs:
            check = self.check_header_integrity(doc)
            if check["needs_header"]:
                defect_docs.append({
                    "file": doc.name,
                    "defect_type": "扉页缺失",
                    "integrity_score": check["integrity_score"]
                })
        
        report_path = self.project_root / "版权校验缺陷报告.md"
        
        content = f"""# 版权校验缺陷报告

## 生成时间
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## SHA256锁档哈希
{LOCK_HASH}

## 缺陷文档清单

| 文件名 | 缺陷类型 | 完整性评分 |
|--------|----------|------------|
"""
        
        for defect in defect_docs:
            content += f"| {defect['file']} | {defect['defect_type']} | {defect['integrity_score']:.2%} |\n"
        
        if not defect_docs:
            content += "| 无缺陷文档 | - | 100% |\n"
        
        content += "\n---\n"
        content += "本报告由文档标准化处理器自动生成，遵循四位一体驻波动力学框架理论约束。\n"
        
        report_path.write_text(content, encoding='utf-8')
        
        return str(report_path)


def main():
    """
    主程序入口
    
    对应公理：公理五（成果落地转化范式）
    理论映射：文档批量标准化处理
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="场3：文档批量标准化处理器")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("场3：文档批量标准化处理器")
    print("归属基底：第3重六阶自主科研业务基底")
    print("对应公理：公理五（成果落地转化范式）")
    print("=" * 60)
    
    standardizer = DocumentStandardizer(args.project_root)
    results = standardizer.run_batch_standardization()
    
    print("\n标准化结果汇总:")
    print(f"  文档总数: {results['total_docs']}")
    print(f"  扉页插入: {results['headers_inserted']}")
    print(f"  AI备注清除: {results['ai_remarks_removed']}")
    print(f"  标题修正: {results['titles_fixed']}")
    print(f"  重复删除: {results['duplicates_removed']}")
    print(f"  附录添加: {results['appendix_added']}")
    
    defect_report = standardizer.generate_defect_report()
    print(f"\n版权校验缺陷报告: {defect_report}")
    
    print("\n" + "=" * 60)
    print("SHA256锁档哈希:", LOCK_HASH)
    print("=" * 60)


if __name__ == "__main__":
    main()