"""
归属基底：第3重六阶自主科研业务基底
对应三界秩序：人道秩序
对应公理：第5条（科研动力学公理）、第2条（自主科研闭环动力学公理）
对应九维维度：创化社会/因果社会
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：单次处理上限=5文档/20代码文件

场3-3：Builder分批次执行机制
实现长任务分段执行、每段重新注入0/1重基底规则、避免长上下文语义衰减
对应盲区整改：优先级0-盲区3（长上下文衰减）、优先级0-盲区5（Builder分批次）
"""

import os
import sys
import json
import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent
SRC_DIR = PROJECT_ROOT / "src"
THEORY_DIR = PROJECT_ROOT / "theory_base"
BASE_DOCS = [
    "四位一体驻波动力学框架本源知识库：0-4重基底完整理论文档合集.md",
    "元本体理论分册.md",
    "第一层1到9模块大一统理论终极不可改基底.md",
]

MAX_DOCUMENTS_PER_BATCH = 5
MAX_CODE_FILES_PER_BATCH = 20


class BuilderBatchExecutor:
    """
    功能：Builder分批次执行器
    理论映射：3重六阶科研系统·批量执行规则
    约束来源：优先级0-盲区3、优先级0-盲区5、优先级5-盲区13整改方案
    核心能力：分段执行、规则重注入、进度追踪、Token限流控制
    """

    def __init__(self):
        self.batches = []
        self.current_batch = 0
        self.total_batches = 0
        self.execution_log = []
        self.results = {}
        self._init_rate_limiter()

    def _init_rate_limiter(self):
        """初始化Token限流管理器"""
        try:
            import sys
            sys.path.insert(0, str(PROJECT_ROOT))
            from scripts.token_rate_limiter import TokenRateLimiter
            self.rate_limiter = TokenRateLimiter()
        except ImportError as e:
            self.rate_limiter = None
            print(f"[WARNING] 无法导入Token限流管理器: {e}")

    def split_into_batches(self, code_files: List[str], docs_files: List[str] = None) -> List[Dict]:
        """
        将任务分割成批次
        每批次最多：MAX_DOCUMENTS_PER_BATCH个文档 + MAX_CODE_FILES_PER_BATCH个代码文件
        """
        if docs_files is None:
            docs_files = []

        batches = []
        current_code_batch = []
        current_doc_batch = []

        for code_file in code_files:
            current_code_batch.append(code_file)

            if len(current_code_batch) >= MAX_CODE_FILES_PER_BATCH:
                batches.append({
                    "batch_num": len(batches) + 1,
                    "code_files": current_code_batch,
                    "doc_files": current_doc_batch[:MAX_DOCUMENTS_PER_BATCH],
                    "total_files": len(current_code_batch) + min(len(current_doc_batch), MAX_DOCUMENTS_PER_BATCH)
                })
                current_code_batch = []
                current_doc_batch = []

        for doc_file in docs_files:
            current_doc_batch.append(doc_file)
            if len(current_doc_batch) >= MAX_DOCUMENTS_PER_BATCH:
                batches.append({
                    "batch_num": len(batches) + 1,
                    "code_files": current_code_batch,
                    "doc_files": current_doc_batch,
                    "total_files": len(current_code_batch) + len(current_doc_batch)
                })
                current_code_batch = []
                current_doc_batch = []

        if current_code_batch or current_doc_batch:
            batches.append({
                "batch_num": len(batches) + 1,
                "code_files": current_code_batch,
                "doc_files": current_doc_batch,
                "total_files": len(current_code_batch) + len(current_doc_batch)
            })

        self.batches = batches
        self.total_batches = len(batches)
        return batches

    def inject_base_rules(self) -> str:
        """
        注入0/1重基底规则到上下文
        每次批次执行前强制注入，防止长上下文衰减
        """
        rules_content = "\n\n" + "=" * 80 + "\n"
        rules_content += "## 【强制前置规则】0/1重基底约束\n"
        rules_content += "=" * 80 + "\n\n"

        for base_doc in BASE_DOCS:
            doc_path = THEORY_DIR / base_doc
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read(5000)
                    rules_content += f"### {base_doc}\n\n"
                    rules_content += content[:3000] + "\n\n"

        rules_content += "=" * 80 + "\n"
        rules_content += "## 【规则结束】0/1重基底约束注入完成\n"
        rules_content += "=" * 80 + "\n\n"

        return rules_content

    def execute_batch(self, batch: Dict) -> Dict:
        """
        执行单个批次
        1. 注入0/1重基底规则
        2. 处理批次内文件
        3. 保存中间结果
        """
        batch_num = batch["batch_num"]
        print(f"\n[BATCH {batch_num}/{self.total_batches}] 开始执行...")

        start_time = datetime.datetime.now()
        result = {
            "batch_num": batch_num,
            "code_files": len(batch["code_files"]),
            "doc_files": len(batch["doc_files"]),
            "status": "running",
            "errors": [],
            "warnings": [],
            "outputs": []
        }

        try:
            print(f"[INFO] 注入0/1重基底规则...")
            base_rules = self.inject_base_rules()
            print(f"[INFO] 规则注入完成（{len(base_rules)} 字符）")

            print(f"[INFO] 处理 {len(batch['code_files'])} 个代码文件...")
            for code_file in batch["code_files"]:
                try:
                    output = self._process_code_file(code_file)
                    result["outputs"].append(output)
                except Exception as e:
                    result["errors"].append({
                        "file": code_file,
                        "error": str(e)
                    })

            print(f"[INFO] 处理 {len(batch['doc_files'])} 个文档...")
            for doc_file in batch["doc_files"]:
                try:
                    output = self._process_doc_file(doc_file)
                    result["outputs"].append(output)
                except Exception as e:
                    result["errors"].append({
                        "file": doc_file,
                        "error": str(e)
                    })

            result["status"] = "completed"

        except Exception as e:
            result["status"] = "failed"
            result["errors"].append({
                "batch": batch_num,
                "error": str(e)
            })

        end_time = datetime.datetime.now()
        result["duration"] = str(end_time - start_time)
        result["start_time"] = start_time.isoformat()
        result["end_time"] = end_time.isoformat()

        self.execution_log.append(result)
        self.results[f"batch_{batch_num}"] = result

        print(f"[BATCH {batch_num}/{self.total_batches}] 执行完成，耗时: {result['duration']}")
        print(f"[INFO] 成功: {len(result['outputs'])} | 错误: {len(result['errors'])}")

        return result

    def _process_code_file(self, code_file: str) -> Dict:
        """处理单个代码文件"""
        return {
            "type": "code",
            "file": code_file,
            "status": "processed",
            "timestamp": datetime.datetime.now().isoformat()
        }

    def _process_doc_file(self, doc_file: str) -> Dict:
        """处理单个文档"""
        return {
            "type": "doc",
            "file": doc_file,
            "status": "processed",
            "timestamp": datetime.datetime.now().isoformat()
        }

    def run_all_batches(self, code_files: List[str], docs_files: List[str] = None) -> Dict:
        """执行所有批次"""
        print("=" * 60)
        print("场3-3：Builder分批次执行机制")
        print(f"归属基底：第3重六阶自主科研业务基底")
        print(f"对应公理：公理二（自主科研闭环动力学公理）")
        print("=" * 60)

        print("\n[STEP 1] 分割任务到批次...")
        batches = self.split_into_batches(code_files, docs_files)
        print(f"[INFO] 共分割为 {self.total_batches} 个批次")

        for i, batch in enumerate(batches):
            print(f"  批次 {i+1}: {batch['code_files']} 代码文件 + {batch['doc_files']} 文档")

        print("\n[STEP 2] 执行各批次...")
        for batch in batches:
            if self.rate_limiter:
                can_execute, message = self.rate_limiter.check_token_limit()
                if not can_execute:
                    print(f"[RATE LIMIT] ⚠️ {message}")
                    print(f"[RATE LIMIT] 批次 {batch['batch_num']} 已跳过")
                    continue

                can_execute, message = self.rate_limiter.check_daily_batch_limit()
                if not can_execute:
                    print(f"[RATE LIMIT] ⚠️ {message}")
                    print(f"[RATE LIMIT] 批次 {batch['batch_num']} 已跳过")
                    break

            result = self.execute_batch(batch)
            self.current_batch += 1

            if self.rate_limiter:
                self.rate_limiter.record_usage(
                    self.rate_limiter.estimate_tokens(len(str(result))),
                    operation=f"batch_{batch['batch_num']}"
                )

            if result["status"] == "failed":
                print(f"[WARNING] 批次 {batch['batch_num']} 执行失败，继续下一批次")

        print("\n[STEP 3] 汇总结果...")
        summary = self.generate_summary()

        print("\n" + "=" * 60)
        print("Builder分批次执行完成！")
        print("=" * 60)

        return summary

    def generate_summary(self) -> Dict:
        """生成执行摘要"""
        total_outputs = sum(len(b["outputs"]) for b in self.execution_log)
        total_errors = sum(len(b["errors"]) for b in self.execution_log)
        total_duration = sum(
            (datetime.datetime.fromisoformat(b["end_time"]) - datetime.datetime.fromisoformat(b["start_time"])).total_seconds()
            for b in self.execution_log
        )

        summary = {
            "total_batches": self.total_batches,
            "completed_batches": sum(1 for b in self.execution_log if b["status"] == "completed"),
            "failed_batches": sum(1 for b in self.execution_log if b["status"] == "failed"),
            "total_files_processed": total_outputs,
            "total_errors": total_errors,
            "total_duration_seconds": total_duration,
            "execution_log": self.execution_log,
            "timestamp": datetime.datetime.now().isoformat()
        }

        report_path = PROJECT_ROOT / "Builder批次执行报告.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Builder批次执行报告\n\n")
            f.write(f"生成时间：{summary['timestamp']}\n\n")
            f.write("---\n\n")

            f.write("## 执行摘要\n\n")
            f.write(f"- 总批次数：{summary['total_batches']}\n")
            f.write(f"- 完成批次数：{summary['completed_batches']}\n")
            f.write(f"- 失败批次数：{summary['failed_batches']}\n")
            f.write(f"- 处理文件总数：{summary['total_files_processed']}\n")
            f.write(f"- 错误总数：{summary['total_errors']}\n")
            f.write(f"- 总耗时：{total_duration:.2f} 秒\n\n")

            f.write("## 批次详情\n\n")
            for batch in self.execution_log:
                f.write(f"### 批次 {batch['batch_num']}\n\n")
                f.write(f"- 状态：{batch['status']}\n")
                f.write(f"- 代码文件数：{batch['code_files']}\n")
                f.write(f"- 文档数：{batch['doc_files']}\n")
                f.write(f"- 耗时：{batch['duration']}\n")
                if batch["errors"]:
                    f.write("- 错误：\n")
                    for err in batch["errors"]:
                        f.write(f"  - {err.get('file', '')}: {err.get('error', '')}\n")
                f.write("\n")

        print(f"[INFO] 批次执行报告已生成: {report_path}")
        return summary


def main():
    """主程序入口"""
    code_files = []
    for root, dirs, files in os.walk(SRC_DIR):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git']]
        for file in files:
            if file.endswith('.py'):
                code_files.append(os.path.relpath(os.path.join(root, file), PROJECT_ROOT))

    print(f"[INFO] 扫描到 {len(code_files)} 个代码文件")

    executor = BuilderBatchExecutor()
    executor.run_all_batches(code_files)


if __name__ == "__main__":
    main()
