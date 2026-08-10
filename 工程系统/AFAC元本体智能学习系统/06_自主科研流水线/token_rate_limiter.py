"""
归属基底：第4重智能体执行基底
对应三界秩序：自然秩序
对应公理：第1条（宿命/舒适双边界公理）、第7条（三界秩序层级仲裁公理）
对应九维维度：自然实体/自然相变
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：TOKEN_LIMIT_PER_HOUR=100000, BATCH_INTERVAL_SECONDS=30

场3-9：Token限流与分批策略管理器
实现免费版token限流规避、大批量处理精度保护、AFAC交付包分批处理
对应盲区整改：优先级5-盲区13（免费版token限流、重度批量处理精度下跌）
"""

import os
import json
import time
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent

TOKEN_LIMIT_PER_HOUR = 100000
BATCH_INTERVAL_SECONDS = 30
MAX_FILES_PER_BATCH = 15
MAX_ROUNDS_PER_DAY = 10
AFAC_DAYS_TO_PREPARE = 3


class TokenRateLimiter:
    """
    功能：Token限流管理器
    理论映射：4重智能体执行基底·资源约束规则
    约束来源：优先级5-盲区13整改方案
    核心能力：token消耗追踪、限流规避、分批策略
    """

    def __init__(self):
        self.token_usage = 0
        self.token_usage_log = []
        self.current_hour_start = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        self.pause_until = None
        self.batch_count_today = 0
        self.last_batch_time = None

    def check_token_limit(self, estimated_tokens: int = 0) -> Tuple[bool, str]:
        """
        检查是否允许执行
        参数：estimated_tokens - 预估token消耗
        返回：(是否允许, 状态信息)
        """
        now = datetime.datetime.now()

        if self.pause_until and now < self.pause_until:
            remaining = (self.pause_until - now).total_seconds()
            return False, f"暂停中，剩余 {remaining:.0f} 秒"

        hour_start = now.replace(minute=0, second=0, microsecond=0)
        if hour_start != self.current_hour_start:
            self.current_hour_start = hour_start
            self.token_usage = 0

        if self.token_usage + estimated_tokens > TOKEN_LIMIT_PER_HOUR:
            pause_until = hour_start + datetime.timedelta(hours=1)
            self.pause_until = pause_until
            remaining = (pause_until - now).total_seconds()
            return False, f"Token即将耗尽，暂停至下一小时（剩余 {remaining:.0f} 秒）"

        return True, "允许执行"

    def record_usage(self, tokens_used: int, operation: str = "") -> None:
        """
        记录token消耗
        参数：
            tokens_used - 实际消耗的token数
            operation - 操作描述
        """
        now = datetime.datetime.now()
        self.token_usage += tokens_used

        self.token_usage_log.append({
            "timestamp": now.isoformat(),
            "tokens_used": tokens_used,
            "total_usage": self.token_usage,
            "operation": operation,
            "hour_remaining": max(0, TOKEN_LIMIT_PER_HOUR - self.token_usage),
        })

        if len(self.token_usage_log) > 100:
            self.token_usage_log = self.token_usage_log[-50:]

    def estimate_tokens(self, text_length: int) -> int:
        """
        估算token数量（粗略估算：1token≈4字符）
        参数：text_length - 文本长度
        返回：预估token数
        """
        return max(1, text_length // 4)

    def wait_for_rate_limit(self, min_wait_seconds: int = 10) -> None:
        """
        等待速率限制恢复
        参数：min_wait_seconds - 最小等待秒数
        """
        wait_time = max(min_wait_seconds, BATCH_INTERVAL_SECONDS)
        print(f"[RATE LIMIT] 等待 {wait_time} 秒后继续...")
        time.sleep(wait_time)

    def split_for_afac_delivery(self, total_files: int) -> List[Dict]:
        """
        AFAC交付包分批处理策略
        提前3天分批处理，避免一次性超大任务触发限流
        参数：total_files - 总文件数
        返回：每天的任务分配
        """
        files_per_day = total_files // AFAC_DAYS_TO_PREPARE
        remainder = total_files % AFAC_DAYS_TO_PREPARE

        plan = []
        remaining = total_files

        for day in range(1, AFAC_DAYS_TO_PREPARE + 1):
            day_files = files_per_day + (1 if day <= remainder else 0)
            remaining -= day_files

            batches_per_day = (day_files + MAX_FILES_PER_BATCH - 1) // MAX_FILES_PER_BATCH

            plan.append({
                "day": day,
                "files": day_files,
                "batches": batches_per_day,
                "files_per_batch": MAX_FILES_PER_BATCH,
                "remaining_after_day": remaining,
            })

        return plan

    def check_daily_batch_limit(self) -> Tuple[bool, str]:
        """
        检查每日批次限制
        返回：(是否允许, 状态信息)
        """
        today = datetime.date.today()

        if self.last_batch_time is None or self.last_batch_time.date() != today:
            self.batch_count_today = 0
            self.last_batch_time = datetime.datetime.now()

        if self.batch_count_today >= MAX_ROUNDS_PER_DAY:
            tomorrow = today + datetime.timedelta(days=1)
            return False, f"今日批次已达上限({MAX_ROUNDS_PER_DAY})，请明日继续"

        self.batch_count_today += 1
        self.last_batch_time = datetime.datetime.now()
        return True, f"允许执行（今日第 {self.batch_count_today}/{MAX_ROUNDS_PER_DAY} 批）"

    def run_batch_with_limit(self, task_func, *args, **kwargs) -> Dict:
        """
        带限流控制的批次执行
        参数：
            task_func - 任务函数
            *args, **kwargs - 任务参数
        返回：执行结果
        """
        now = datetime.datetime.now()
        result = {
            "status": "pending",
            "start_time": now.isoformat(),
            "end_time": None,
            "error": None,
            "output": None,
            "token_usage": 0,
        }

        can_execute, message = self.check_token_limit()
        if not can_execute:
            result["status"] = "blocked"
            result["error"] = message
            return result

        can_execute, message = self.check_daily_batch_limit()
        if not can_execute:
            result["status"] = "blocked"
            result["error"] = message
            return result

        print(f"[INFO] {message}")

        try:
            output = task_func(*args, **kwargs)
            result["output"] = output
            result["status"] = "completed"

            text_output = str(output)
            tokens_used = self.estimate_tokens(len(text_output))
            self.record_usage(tokens_used, operation=task_func.__name__)
            result["token_usage"] = tokens_used

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)

        result["end_time"] = datetime.datetime.now().isoformat()

        self.wait_for_rate_limit()

        return result

    def generate_usage_report(self) -> str:
        """生成Token使用报告"""
        report_path = PROJECT_ROOT / "Token使用报告.md"

        content = f"""# Token使用报告

## 报告信息

| 项目 | 内容 |
|------|------|
| 生成时间 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 本次小时已用 | {self.token_usage} |
| 本次小时剩余 | {max(0, TOKEN_LIMIT_PER_HOUR - self.token_usage)} |
| 今日批次执行数 | {self.batch_count_today} |
| 今日批次剩余数 | {max(0, MAX_ROUNDS_PER_DAY - self.batch_count_today)} |

## 限流参数配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 每小时Token上限 | {TOKEN_LIMIT_PER_HOUR} | 免费版限流阈值 |
| 批次间隔 | {BATCH_INTERVAL_SECONDS} 秒 | 批次间最小等待时间 |
| 每批最大文件数 | {MAX_FILES_PER_BATCH} | 防止单次任务过大 |
| 每日最大批次数 | {MAX_ROUNDS_PER_DAY} | 避免全天消耗过快 |
| AFAC提前准备天数 | {AFAC_DAYS_TO_PREPARE} | 交付包分批处理天数 |

## 最近使用记录

| 时间 | 操作 | Token消耗 | 累计使用 |
|------|------|-----------|----------|
"""

        for record in reversed(self.token_usage_log[-10:]):
            content += f"| {record['timestamp']} | {record['operation']} | {record['tokens_used']} | {record['total_usage']} |\n"

        if not self.token_usage_log:
            content += "| - | - | - | - |\n"

        content += "\n---\n"
        content += "## 限流规避策略\n\n"
        content += "1. **分批次执行**：每次批量处理不超过 {MAX_FILES_PER_BATCH} 个文件\n"
        content += "2. **批次间隔**：每批之间等待 {BATCH_INTERVAL_SECONDS} 秒\n"
        content += "3. **每日限制**：单日不超过 {MAX_ROUNDS_PER_DAY} 批次\n"
        content += "4. **AFAC分批**：交付包提前 {AFAC_DAYS_TO_PREPARE} 天分批处理\n"
        content += "5. **自动暂停**：Token即将耗尽时自动暂停至下一小时\n\n"
        content += "---\n"
        content += "本报告由Token限流管理器自动生成\n"
        content += "理论基准：四位一体驻波动力学框架\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[INFO] Token使用报告已生成: {report_path}")
        return str(report_path)


def test_limiter():
    """测试Token限流管理器"""
    limiter = TokenRateLimiter()

    print("\n[TEST 1] 检查Token限制...")
    can_execute, message = limiter.check_token_limit()
    print(f"  结果: {'✅' if can_execute else '❌'} - {message}")

    print("\n[TEST 2] 记录Token消耗...")
    limiter.record_usage(5000, "代码生成")
    limiter.record_usage(3000, "文档处理")
    print(f"  当前使用: {limiter.token_usage} token")

    print("\n[TEST 3] AFAC交付包分批策略...")
    plan = limiter.split_for_afac_delivery(50)
    for day in plan:
        print(f"  第{day['day']}天: {day['files']}个文件, {day['batches']}批")

    print("\n[TEST 4] 带限流的批次执行...")
    def dummy_task():
        return {"result": "success", "data": "test"}

    result = limiter.run_batch_with_limit(dummy_task)
    print(f"  执行结果: {result['status']}")

    limiter.generate_usage_report()


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-9：Token限流与分批策略管理器")
    print(f"归属基底：第4重智能体执行基底")
    print(f"对应公理：公理一（宿命/舒适双边界公理）")
    print("=" * 60)

    test_limiter()


if __name__ == "__main__":
    main()
