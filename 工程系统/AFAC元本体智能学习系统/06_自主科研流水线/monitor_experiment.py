"""
监控AFAC2026实验进度
"""
import os
import time
import json
from datetime import datetime

reports_dir = "./output/reports"
print("开始监控AFAC2026实验进度...")
print(f"报告目录: {reports_dir}")
print("按Ctrl+C停止监控\n")

last_count = 0
try:
    while True:
        # 获取最新的报告目录
        if not os.path.exists(reports_dir):
            print("等待报告目录创建...")
            time.sleep(5)
            continue

        dirs = [d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d))]
        if not dirs:
            print("等待实验开始...")
            time.sleep(5)
            continue

        # 按时间排序，获取最新的
        dirs.sort(reverse=True)
        latest_dir = dirs[0]
        latest_path = os.path.join(reports_dir, latest_dir)

        metrics_file = os.path.join(latest_path, "metrics.json")
        report_file = os.path.join(latest_path, "report.txt")

        if len(dirs) != last_count:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 新报告目录: {latest_dir}")
            last_count = len(dirs)

        # 检查是否有metrics.json
        if os.path.exists(metrics_file):
            try:
                with open(metrics_file, 'r', encoding='utf-8') as f:
                    metrics = json.load(f)

                best_score = metrics.get('best_score', 0)
                final_level = metrics.get('final_level', 'N/A')
                total_steps = metrics.get('total_step', 0)

                print(f"\r[{datetime.now().strftime('%H:%M:%S')}] 最优分数: {best_score:.4f} | 步数: {total_steps} | 等级: {final_level}", end='', flush=True)
            except Exception as e:
                print(f"\n读取metrics失败: {e}")

        # 检查是否有report.txt
        if os.path.exists(report_file):
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "最优分数" in content:
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 实验完成!")
                        print(content)
                        break
            except Exception as e:
                pass

        time.sleep(2)

except KeyboardInterrupt:
    print("\n\n监控已停止")