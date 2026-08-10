# emergence_dual_judge.py
# 人机双重判定涌现分析引擎：智能体量化 + 作者人工终审
import json
from typing import List, Dict


class EmergenceDualJudge:
    def __init__(self):
        self.bottom_layer_cache = []
        self.emergence_record = {}
        self.author_conclusion = None

    def decompose_emergence_basis(self, emergence_text: str, all_sub_sys: List[Dict]) -> List[Dict]:
        """智能体自动：拆解涌现秩序底层低阶构成"""
        basis_list = []
        for sys in all_sub_sys:
            if sys["name"] in emergence_text or any(kw in emergence_text for kw in sys["theory_category"]["sub_type"].split()):
                basis_list.append({
                    "base_subsystem": sys["name"],
                    "base_logic_type": sys["theory_category"]["logic_type"],
                    "base_spectrum": sys["theory_category"]["spectrum_value"]
                })
        self.bottom_layer_cache = basis_list
        return basis_list

    def simulate_three_destiny(self, spectrum_list: List[float]) -> Dict:
        """自动化模拟三大终极秩序归宿量化趋势"""
        avg_spec = sum(spectrum_list) / len(spectrum_list) if spectrum_list else 0.5
        return {
            "永恒稳态拟合值": round(avg_spec * 1.08, 2),
            "循环生灭波动区间": [round(avg_spec - 0.2, 2), round(avg_spec + 0.2, 2)],
            "复归空无衰减速率": round(1 - avg_spec, 2),
            "avg_all_spectrum": round(avg_spec, 2)
        }

    def submit_author_judge(self, conclusion: str):
        """录入作者顶层元思辨判定，完成双重闭环"""
        self.author_conclusion = conclusion

    def export_final_audit_report(self, emergence_name: str) -> str:
        """输出人机协同完整报告，区分自动数据/人工缺失项"""
        report = [
            f"# 高阶涌现秩序双重判定报告：{emergence_name}",
            f"## 1. 智能体自动拆解底层构成",
            json.dumps(self.bottom_layer_cache, ensure_ascii=False, indent=2),
            f"\n## 2. 三大秩序归宿全域模拟数据",
            json.dumps(self.simulate_three_destiny([b["base_spectrum"] for b in self.bottom_layer_cache]), ensure_ascii=False, indent=2),
            "\n## 3. 待作者人工破解项（代码无法自主完成）",
            "- 提炼涌现专属底层公理",
            "- 定位该秩序在空无-所有光谱元层级",
            "- 判定是否纳入全域成熟体系/永久隔离",
            "- 三大演化归宿元价值取舍",
            "\n## 4. 作者思辨结论录入",
            self.author_conclusion if self.author_conclusion else "【待作者输入，当前存在单方判定盲区】"
        ]
        report_path = f"./theory_community/buffer_community_center/emergence_audit_reports/emergence_audit_{emergence_name}.md"
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(report))
        return report_path


import os
