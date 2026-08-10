import os
import sys
import json
from datetime import datetime

# 导入社区中控类
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from community_manager import CommunityManager

class DailyInspection:
    def __init__(self):
        self.manager = CommunityManager()
        self.report_dir = os.path.join(self.manager.buffer_path, "inspection_reports/")
        self.today_str = datetime.now().strftime("%Y%m%d")
        self.report_file = os.path.join(self.report_dir, f"全域本体社区每日巡检报告_{self.today_str}.md")
        self._ensure_dir(self.report_dir)

    def _ensure_dir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def _write(self, content):
        with open(self.report_file, "a", encoding="utf-8") as f:
            f.write(content + "\n")

    def generate_report(self):
        """生成完整每日巡检报告"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始生成每日巡检报告...")

        # 报告头部
        self._write(f"# 全域本体社区每日巡检报告")
        self._write(f"**报告日期**：{datetime.now().strftime('%Y年%m月%d日')}")
        self._write(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self._write(f"**报告类型**：全自动日常运维巡检")
        self._write("")
        self._write("---")
        self._write("")

        # 1. 母核庄园安全状态
        self._write("## 一、母核庄园安全状态")
        core_ok = self.manager.core_security_check()
        if core_ok:
            self._write("- ✅ **母核完整性校验通过**，基准哈希匹配，无篡改痕迹，边界稳固")
        else:
            self._write("- 🚨 **母核状态异常**，哈希不匹配，疑似边界被突破，已触发全域应急封控")
        self._write(f"- 基准哈希值：`{self.manager.core_baseline_hash}`")
        self._write("")

        # 2. 全社区子系统总览
        self._write("## 二、子系统社区总览统计")
        subsystems = self.manager.scan_all_subsystems()
        
        level1 = sum(1 for s in subsystems if s["level"] == "一级成熟")
        level2 = sum(1 for s in subsystems if s["level"] == "二级孵化")
        isolate = sum(1 for s in subsystems if s["boundary_mode"] == "full_isolate")
        protocol = sum(1 for s in subsystems if s["boundary_mode"] == "protocol_restricted")
        full_conn = sum(1 for s in subsystems if s["boundary_mode"] == "full_connect")
        pipe_on = sum(1 for s in subsystems if s["pipeline"] == "开通")
        abnormal = sum(1 for s in subsystems if s["status"] == "异常")
        total_power = sum(s["power_used"] for s in subsystems if s["power_used"] > 0)

        self._write(f"- 子系统总数：**{len(subsystems)} 栋**")
        self._write(f"- 一级成熟独栋：{level1} 栋")
        self._write(f"- 二级孵化独栋：{level2} 栋")
        self._write(f"- 完全隔离模式：{isolate} 栋")
        self._write(f"- 协议受限模式：{protocol} 栋")
        self._write(f"- 完全互通模式：{full_conn} 栋")
        self._write(f"- 外部管线开通：{pipe_on} 栋")
        self._write(f"- 配置异常数量：{abnormal} 栋")
        self._write(f"- 全社区累计算力消耗：**{total_power:.1f} 算力点**")
        self._write("")

        # 3. 子系统明细清单
        self._write("## 三、各子系统详细状态")
        self._write("| 子系统名称 | 层级 | 边界模式 | 外部管线 | 累计算力消耗 | 运行状态 |")
        self._write("|------------|------|----------|----------|--------------|----------|")
        for s in subsystems:
            status_mark = "✅ 正常" if s["status"] == "正常" else "⚠️ 异常"
            power_str = f"{s['power_used']:.1f}" if s["power_used"] >= 0 else "读取失败"
            self._write(f"| {s['name']} | {s['level']} | {s['boundary_mode']} | {s['pipeline']} | {power_str} | {status_mark} |")
        self._write("")

        # 4. 异常告警汇总
        self._write("## 四、异常告警与处置建议")
        abnormal_list = [s for s in subsystems if s["status"] == "异常"]
        high_risk = [s for s in subsystems if s["level"] == "二级孵化" and s["boundary_mode"] == "full_connect"]

        if not abnormal_list and not high_risk and core_ok:
            self._write("✅ **今日无异常告警**，全社区运行状态正常，边界稳固，算力消耗平稳。")
        else:
            if not core_ok:
                self._write("🚨 **严重告警：母核哈希异常**，已自动触发全域封控，请立即人工核查母核文件完整性。")
            if abnormal_list:
                self._write("⚠️ **配置异常告警**：以下子系统边界配置读取失败，建议核查 `facade.json` 文件：")
                for s in abnormal_list:
                    self._write(f"  - {s['name']}（路径：{s['path']}）")
            if high_risk:
                self._write("⚠️ **高风险提示**：以下二级孵化独栋处于完全互通模式，存在风险外溢可能，建议核查：")
                for s in high_risk:
                    self._write(f"  - {s['name']}")
        self._write("")

        # 5. 运维结论
        self._write("## 五、今日运维结论")
        if core_ok and abnormal == 0:
            self._write("整体运行状态：**优秀**。母核稳固，边界有序，子系统生长正常，无安全隐患。")
        elif abnormal > 0:
            self._write("整体运行状态：**留意**。存在局部配置异常，需人工排查修复，母核核心安全未受影响。")
        else:
            self._write("整体运行状态：**告警**。存在核心安全风险，需立即处置。")
        self._write("")

        # 6. 报告落款
        self._write("---")
        self._write("*本报告由全域本体社区中控系统自动生成，全程纯读取校验，未修改任何业务配置与核心基底。*")

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 报告生成完成")
        print(f"报告路径：{self.report_file}")
        return self.report_file


if __name__ == "__main__":
    inspector = DailyInspection()
    inspector.generate_report()