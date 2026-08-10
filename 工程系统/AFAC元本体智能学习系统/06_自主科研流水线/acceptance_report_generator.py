"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（成果落地转化范式）
对应九维维度：社会因果/人道能级
理论原文出处：《六阶自主科研架构论文》第五章
核心数理参数：θ_mv=0.005, θ_evo=0.002

场2：验收报表生成脚本
实现科研成果验收报表自动生成
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ==================== 固定数理参数（锁档核心） ====================
# 对应规则相位位（第二位）·科研价值边际判定规则
THETA_MV = 0.005  # 科研边际价值判定阈值
THETA_EVO = 0.002  # 自进化增量阈值

# SHA256锁档哈希
LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"


class AcceptanceReportGenerator:
    """
    功能：科研成果验收报表生成器
    理论映射：3重六阶自主科研业务基底·成果落地转化范式
    能级关联：E3=0.90三阶道心能级验收标准
    约束来源：成果落地转化范式（公理五）
    禁止修改：验收阈值θ_mv/θ_evo，修改会破坏理论闭环
    """
    
    def __init__(self, project_root: str):
        """
        初始化验收报表生成器
        
        对应公理：公理五（成果落地转化范式）
        理论映射：科研成果验收初始化
        
        Args:
            project_root: 项目根目录
        """
        self.project_root = Path(project_root)
        self.output_path = self.project_root / "output"
        self.report_data = {}
    
    def collect_metrics(self) -> Dict:
        """
        收集验收指标
        
        对应公理：公理五（成果落地转化范式）
        理论映射：科研成果指标收集
        
        Returns:
            Dict: 收集的指标数据
        """
        metrics = {
            "timestamp": datetime.datetime.now().isoformat(),
            "lock_hash": LOCK_HASH,
            "project_info": self._collect_project_info(),
            "code_metrics": self._collect_code_metrics(),
            "theory_metrics": self._collect_theory_metrics(),
            "output_metrics": self._collect_output_metrics(),
            "acceptance_criteria": self._check_acceptance_criteria()
        }
        
        self.report_data = metrics
        return metrics
    
    def _collect_project_info(self) -> Dict:
        """
        收集项目基本信息
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：锁档确权信息
        
        Returns:
            Dict: 项目基本信息
        """
        return {
            "name": "V3.0 Rev.04 四位一体驻波动力学框架",
            "author": "杨腾飞",
            "id_number": "433127199812193215",
            "lock_date": "2026-06-20",
            "hash": LOCK_HASH,
            "three_dim_rights": {
                "creator": 0.60,
                "moxin": 0.25,
                "doubao": 0.15
            }
        }
    
    def _collect_code_metrics(self) -> Dict:
        """
        收集代码指标
        
        对应公理：公理二（自主科研闭环动力学公理）
        理论映射：代码工程指标
        
        Returns:
            Dict: 代码指标
        """
        src_path = self.project_root / "src"
        code_files = list(src_path.glob("**/*.py"))
        
        # 统计各层代码文件数量
        core_files = list(src_path.glob("core/*.py"))
        entity_files = list(src_path.glob("entity_layer/*.py"))
        decision_files = list(src_path.glob("decision_layer/*.py"))
        master_files = list(src_path.glob("master_agent/*.py"))
        support_files = list(src_path.glob("support/*.py"))
        extend_files = list(src_path.glob("support/extend/*.py"))
        
        # 统计理论绑定率
        bound_files = 0
        for f in code_files:
            content = f.read_text(encoding='utf-8')
            if "归属基底" in content and "对应公理" in content:
                bound_files += 1
        
        binding_rate = bound_files / len(code_files) if code_files else 0
        
        return {
            "total_files": len(code_files),
            "bound_files": bound_files,
            "binding_rate": binding_rate,
            "layer_distribution": {
                "core": len(core_files),
                "entity": len(entity_files),
                "decision": len(decision_files),
                "master": len(master_files),
                "support": len(support_files),
                "extend": len(extend_files)
            }
        }
    
    def _collect_theory_metrics(self) -> Dict:
        """
        收集理论文档指标
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：理论文档完整性
        
        Returns:
            Dict: 理论文档指标
        """
        theory_path = self.project_root / "theory_base"
        theory_files = list(theory_path.glob("*.md"))
        
        # 统计各基底文档数量
        base_0_files = [f for f in theory_files if "0元" in f.name or "元道" in f.name]
        base_1_files = [f for f in theory_files if "九维" in f.name or "法理" in f.name]
        base_2_files = [f for f in theory_files if "三界" in f.name or "秩序" in f.name]
        axiom_files = [f for f in theory_files if "公理" in f.name]
        
        return {
            "total_files": len(theory_files),
            "base_distribution": {
                "base_0": len(base_0_files),
                "base_1": len(base_1_files),
                "base_2": len(base_2_files),
                "axiom": len(axiom_files)
            }
        }
    
    def _collect_output_metrics(self) -> Dict:
        """
        收集输出文件指标
        
        对应公理：公理五（成果落地转化范式）
        理论映射：科研成果输出
        
        Returns:
            Dict: 输出文件指标
        """
        submission_path = self.output_path / "submission"
        task1_path = self.output_path / "task1"
        task2_path = self.output_path / "task2"
        
        submission_files = list(submission_path.glob("*.csv")) if submission_path.exists() else []
        task1_files = list(task1_path.glob("*")) if task1_path.exists() else []
        task2_files = list(task2_path.glob("*")) if task2_path.exists() else []
        
        return {
            "submission_files": len(submission_files),
            "task1_files": len(task1_files),
            "task2_files": len(task2_files),
            "total_outputs": len(submission_files) + len(task1_files) + len(task2_files)
        }
    
    def _check_acceptance_criteria(self) -> Dict:
        """
        检查验收标准
        
        对应公理：公理五（成果落地转化范式）
        理论映射：科研成果验收判定
        
        Returns:
            Dict: 验收标准检查结果
        """
        criteria = {
            "code_binding_rate": {
                "threshold": 0.35,  # E1阈值
                "actual": self.report_data.get("code_metrics", {}).get("binding_rate", 0),
                "pass": False
            },
            "theory_files_min": {
                "threshold": 7,
                "actual": self.report_data.get("theory_metrics", {}).get("total_files", 0),
                "pass": False
            },
            "output_files_min": {
                "threshold": 4,
                "actual": self.report_data.get("output_metrics", {}).get("total_outputs", 0),
                "pass": False
            },
            "extend_modules_min": {
                "threshold": 3,
                "actual": self.report_data.get("code_metrics", {}).get("layer_distribution", {}).get("extend", 0),
                "pass": False
            }
        }
        
        # 更新实际值并判定
        code_metrics = self._collect_code_metrics()
        theory_metrics = self._collect_theory_metrics()
        output_metrics = self._collect_output_metrics()
        
        criteria["code_binding_rate"]["actual"] = code_metrics["binding_rate"]
        criteria["code_binding_rate"]["pass"] = code_metrics["binding_rate"] >= criteria["code_binding_rate"]["threshold"]
        
        criteria["theory_files_min"]["actual"] = theory_metrics["total_files"]
        criteria["theory_files_min"]["pass"] = theory_metrics["total_files"] >= criteria["theory_files_min"]["threshold"]
        
        criteria["output_files_min"]["actual"] = output_metrics["total_outputs"]
        criteria["output_files_min"]["pass"] = output_metrics["total_outputs"] >= criteria["output_files_min"]["threshold"]
        
        criteria["extend_modules_min"]["actual"] = code_metrics["layer_distribution"]["extend"]
        criteria["extend_modules_min"]["pass"] = code_metrics["layer_distribution"]["extend"] >= criteria["extend_modules_min"]["threshold"]
        
        # 计算总体验收状态
        pass_count = sum(1 for c in criteria.values() if c["pass"])
        overall_pass = pass_count >= 3
        
        criteria["overall_pass"] = overall_pass
        criteria["pass_count"] = pass_count
        
        return criteria
    
    def generate_report(self) -> str:
        """
        生成验收报表
        
        对应公理：公理五（成果落地转化范式）
        理论映射：科研成果验收报表输出
        
        Returns:
            str: 报表文件路径
        """
        # 收集指标
        self.collect_metrics()
        
        # 生成JSON报表
        json_path = self.output_path / "acceptance_report.json"
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(self.report_data, indent=2, ensure_ascii=False), encoding='utf-8')
        
        # 生成Markdown报表
        md_path = self.output_path / "验收报表.md"
        md_content = self._generate_md_report()
        md_path.write_text(md_content, encoding='utf-8')
        
        return str(json_path), str(md_path)
    
    def _generate_md_report(self) -> str:
        """
        生成Markdown格式验收报表
        
        对应公理：公理五（成果落地转化范式）
        理论映射：科研成果验收报表格式
        
        Returns:
            str: Markdown内容
        """
        criteria = self.report_data.get("acceptance_criteria", {})
        
        content = f"""# 科研成果验收报表

## 生成时间
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## SHA256锁档哈希
{LOCK_HASH}

## 项目基本信息

| 项目 | 内容 |
|------|------|
| 作品全称 | V3.0 Rev.04 四位一体驻波动力学框架 |
| 作者 | 杨腾飞 |
| 证件号码 | 433127199812193215 |
| 锁档日期 | 2026-06-20 |

## 验收标准检查

| 标准项 | 阈值 | 实际值 | 状态 |
|------|------|------|------|
| 代码理论绑定率 | ≥{criteria.get('code_binding_rate', {}).get('threshold', 0):.2%} | {criteria.get('code_binding_rate', {}).get('actual', 0):.2%} | {'✅ PASS' if criteria.get('code_binding_rate', {}).get('pass', False) else '❌ FAIL'} |
| 理论文档数量 | ≥{criteria.get('theory_files_min', {}).get('threshold', 0)} | {criteria.get('theory_files_min', {}).get('actual', 0)} | {'✅ PASS' if criteria.get('theory_files_min', {}).get('pass', False) else '❌ FAIL'} |
| 输出文件数量 | ≥{criteria.get('output_files_min', {}).get('threshold', 0)} | {criteria.get('output_files_min', {}).get('actual', 0)} | {'✅ PASS' if criteria.get('output_files_min', {}).get('pass', False) else '❌ FAIL'} |
| 拓展模块数量 | ≥{criteria.get('extend_modules_min', {}).get('threshold', 0)} | {criteria.get('extend_modules_min', {}).get('actual', 0)} | {'✅ PASS' if criteria.get('extend_modules_min', {}).get('pass', False) else '❌ FAIL'} |

## 总体验收状态

**{criteria.get('pass_count', 0)}/4 标准通过**

{'✅ **验收通过**' if criteria.get('overall_pass', False) else '❌ **验收未通过**'}

## 固定数理参数

| 参数 | 锁档值 | 说明 |
|------|------|------|
| θ_mv | {THETA_MV} | 科研边际价值判定阈值 |
| θ_evo | {THETA_EVO} | 自进化增量阈值 |

---

本报表由验收报表生成器自动生成，遵循四位一体驻波动力学框架理论约束。
"""
        
        return content


def main():
    """
    主程序入口
    
    对应公理：公理五（成果落地转化范式）
    理论映射：科研成果验收报表生成
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="场2：验收报表生成器")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("场2：验收报表生成器")
    print("归属基底：第3重六阶自主科研业务基底")
    print("对应公理：公理五（成果落地转化范式）")
    print("=" * 60)
    
    generator = AcceptanceReportGenerator(args.project_root)
    json_path, md_path = generator.generate_report()
    
    print(f"\nJSON报表: {json_path}")
    print(f"Markdown报表: {md_path}")
    
    criteria = generator.report_data.get("acceptance_criteria", {})
    print(f"\n验收状态: {criteria.get('pass_count', 0)}/4 标准通过")
    print(f"总体状态: {'✅ 验收通过' if criteria.get('overall_pass', False) else '❌ 验收未通过'}")
    
    print("\n" + "=" * 60)
    print("SHA256锁档哈希:", LOCK_HASH)
    print("=" * 60)


if __name__ == "__main__":
    main()