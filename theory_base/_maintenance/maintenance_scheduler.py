#!/usr/bin/env python3
"""
运维脚本调度器 - 全域知识库定时自动化运维

功能：
1. 分层定时执行哈希巡检、冲突检测、索引更新
2. 三级异常自动处置
3. 每日0点全索引重构
4. 每周版本链完整归档备份
5. 异常告警与锁定机制

使用方式：
    python maintenance_scheduler.py [--daemon] [--run-task TASK_ID] [--status]
"""

import os
import sys
import json
import time
import subprocess
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# 配置路径
SETTINGS_FILE = "./.trae/settings.json"
MAINTENANCE_DIR = "./theory_base/_maintenance"
LOCK_FILE = "./theory_base/_maintenance/.lockdown"
LOG_FILE = "./theory_base/_maintenance/maintenance_log.json"

class MaintenanceScheduler:
    """运维调度器"""

    def __init__(self):
        self.config = self.load_config()
        self.tasks = self.config.get("scheduled_maintenance_config", {}).get("tasks", [])
        self.exception_config = self.config.get("exception_handling_config", {})
        self.last_run = {}
        self.is_locked = False
        self.load_last_run()

    def load_config(self) -> Dict:
        """加载配置"""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def load_last_run(self):
        """加载上次运行记录"""
        if os.path.exists(LOG_FILE):
            try:
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.last_run = data.get("last_run", {})
            except:
                self.last_run = {}

    def save_last_run(self):
        """保存运行记录"""
        data = {
            "last_run": self.last_run,
            "last_updated": datetime.now().isoformat()
        }
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def is_locked(self) -> bool:
        """检查是否锁定"""
        return os.path.exists(LOCK_FILE)

    def lock_system(self, reason: str):
        """锁定系统"""
        os.makedirs(os.path.dirname(LOCK_FILE), exist_ok=True)
        with open(LOCK_FILE, 'w', encoding='utf-8') as f:
            f.write(f"LOCKED: {reason}\n")
            f.write(f"TIME: {datetime.now().isoformat()}\n")
        self.is_locked = True
        print("=" * 60)
        print("【系统锁定】一级异常：基底篡改检测")
        print(f"原因：{reason}")
        print("所有推演功能已被锁定，等待人工修复")
        print("=" * 60)

    def unlock_system(self):
        """解锁系统"""
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        self.is_locked = False
        print("系统已解锁")

    def run_script(self, script: str, args: str = "") -> tuple:
        """执行脚本"""
        script_path = os.path.join(MAINTENANCE_DIR, script)
        if not os.path.exists(script_path):
            return False, f"脚本不存在: {script_path}"

        cmd = f'python "{script_path}" {args}'
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )
            return result.returncode == 0, result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            return False, "执行超时"
        except Exception as e:
            return False, str(e)

    def handle_exception(self, task_id: str, exception_level: str, error: str):
        """处理异常"""
        if exception_level not in self.exception_config:
            return

        config = self.exception_config[exception_level]

        # 记录日志
        print(f"[ERROR] 任务 {task_id} 执行失败: {error}")
        print(f"[ACTION] 执行异常处置: {config.get('action')}")

        # 一级异常：锁定系统
        if config.get("action") == "lockdown_all":
            self.lock_system(f"任务 {task_id} 失败: {error}")

        # 记录异常
        self.save_exception_log(task_id, exception_level, error)

    def save_exception_log(self, task_id: str, level: str, error: str):
        """保存异常日志"""
        log_path = os.path.join(MAINTENANCE_DIR, "exception_log.json")
        logs = []
        if os.path.exists(log_path):
            try:
                with open(log_path, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append({
            "task_id": task_id,
            "level": level,
            "error": error,
            "time": datetime.now().isoformat()
        })

        # 保留最近100条
        logs = logs[-100:]

        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

    def should_run(self, task: Dict) -> bool:
        """检查任务是否应该运行"""
        task_id = task.get("task_id")
        interval_hours = task.get("interval_hours", 24)

        if task_id not in self.last_run:
            return True

        last_time = datetime.fromisoformat(self.last_run[task_id])
        next_time = last_time + timedelta(hours=interval_hours)

        return datetime.now() >= next_time

    def run_task(self, task: Dict) -> bool:
        """执行单个任务"""
        task_id = task.get("task_id")
        script = task.get("script")
        args = task.get("args", "")
        description = task.get("description", "")
        on_failure = task.get("on_failure", "alert")

        print(f"\n{'=' * 60}")
        print(f"[任务] {task_id}: {description}")
        print(f"时间：{datetime.now().isoformat()}")
        print("=" * 60)

        # 检查系统锁定
        if self.is_locked() and task_id != "core_hash_check":
            print(f"[跳过] 系统已锁定，跳过任务 {task_id}")
            return True

        # 执行脚本
        success, output = self.run_script(script, args)

        if success:
            print(f"[成功] 任务 {task_id} 执行完成")
            self.last_run[task_id] = datetime.now().isoformat()
            self.save_last_run()

            # 检查是否有告警
            if "FAIL" in output or "ERROR" in output:
                print(f"[警告] 任务执行完成但存在异常: {output[:200]}")

            return True
        else:
            print(f"[失败] 任务 {task_id} 执行失败: {output}")

            # 确定异常级别
            if task_id == "core_hash_check":
                self.handle_exception(task_id, "level1_baseline_tamper", output)
            elif task_id == "agent_compliance_check":
                self.handle_exception(task_id, "level2_agent_conflict", output)
            else:
                self.handle_exception(task_id, "level3_theory_deviation", output)

            return False

    def run_all_due_tasks(self):
        """执行所有到期的任务"""
        if self.is_locked():
            print("【系统已锁定】跳过后台任务执行")
            return

        for task in self.tasks:
            if self.should_run(task):
                self.run_task(task)

    def daemon_mode(self):
        """守护进程模式"""
        print("=" * 60)
        print("【运维调度器】守护进程模式启动")
        print(f"监控任务数：{len(self.tasks)}")
        print("=" * 60)

        check_interval = 60  # 每分钟检查一次

        while True:
            try:
                self.run_all_due_tasks()
                time.sleep(check_interval)
            except KeyboardInterrupt:
                print("\n运维调度器已停止")
                break
            except Exception as e:
                print(f"[ERROR] 调度器异常: {e}")
                time.sleep(check_interval)

    def status(self):
        """显示状态"""
        print("=" * 60)
        print("【运维调度器状态】")
        print("=" * 60)

        # 锁定状态
        if self.is_locked():
            print("状态：🔴 已锁定")
            if os.path.exists(LOCK_FILE):
                with open(LOCK_FILE, 'r') as f:
                    print(f.read())
        else:
            print("状态：🟢 正常运行")

        print()

        # 任务状态
        print("任务状态：")
        for task in self.tasks:
            task_id = task.get("task_id")
            description = task.get("description", "")
            interval = task.get("interval_hours", 24)

            if task_id in self.last_run:
                last = datetime.fromisoformat(self.last_run[task_id])
                next_run = last + timedelta(hours=interval)
                status_icon = "✅" if datetime.now() < next_run else "⏰"
                print(f"  {status_icon} {task_id}")
                print(f"      {description}")
                print(f"      上次运行：{last.strftime('%Y-%m-%d %H:%M')}")
                print(f"      下次运行：{next_run.strftime('%Y-%m-%d %H:%M')}")
            else:
                print(f"  ⚪ {task_id}")
                print(f"      {description}")
                print(f"      状态：从未运行")

            print()

        # 异常日志
        log_path = os.path.join(MAINTENANCE_DIR, "exception_log.json")
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            if logs:
                print(f"最近异常 ({len(logs)} 条)：")
                for log in logs[-5:]:
                    print(f"  [{log['level']}] {log['task_id']} - {log['time']}")
                    print(f"    {log['error'][:100]}")

        print("=" * 60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="运维脚本调度器")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--run-task", help="执行指定任务")
    parser.add_argument("--status", action="store_true", help="显示状态")
    parser.add_argument("--unlock", action="store_true", help="解锁系统")
    args = parser.parse_args()

    scheduler = MaintenanceScheduler()

    if args.status:
        scheduler.status()
    elif args.unlock:
        scheduler.unlock_system()
    elif args.run_task:
        for task in scheduler.tasks:
            if task.get("task_id") == args.run_task:
                scheduler.run_task(task)
                break
        else:
            print(f"未找到任务: {args.run_task}")
    elif args.daemon:
        scheduler.daemon_mode()
    else:
        # 单次运行所有到期任务
        scheduler.run_all_due_tasks()

if __name__ == "__main__":
    main()