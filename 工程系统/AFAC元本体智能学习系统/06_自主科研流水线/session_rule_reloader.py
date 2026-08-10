"""
归属基底：第本体拓扑位（第一位）
对应三界秩序：天道秩序
对应公理：第1条（宿命/舒适双边界公理）、第2条（自主科研闭环动力学公理）
对应九维维度：道心本源/道心演化
理论原文出处：《四位一体驻波动力学框架本源知识库》
核心数理参数：RELOAD_INTERVAL_ROUNDS=10, RULES_CACHE_TTL=3600

场3-10：会话规则重加载器
实现长会话规则定期重加载、SOLO子任务提示词重置、上下文稀释防护
对应盲区整改：优先级5-盲区14（Skill无持久状态，长会话规则被上下文稀释）
"""

import os
import json
import time
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

PROJECT_ROOT = Path(__file__).parent.parent
RULES_DIR = PROJECT_ROOT / ".trae" / "rules"
THEORY_DIR = PROJECT_ROOT / "theory_base"

RELOAD_INTERVAL_ROUNDS = 10
RULES_CACHE_TTL = 3600


class SessionRuleReloader:
    """
    功能：会话规则重加载器
    理论映射：本体拓扑位（第一位）·规则持久化机制
    约束来源：优先级5-盲区14整改方案
    核心能力：规则定期重加载、提示词重置、上下文稀释防护
    """

    def __init__(self):
        self.conversation_round = 0
        self.rules_cache = {}
        self.last_reload_time = None
        self.system_prompt_stack = []
        self.base_rules_injected = False

    def load_top_rules(self) -> str:
        """
        加载顶层.rules完整约束
        从.rules目录加载所有规则文件
        """
        rules_content = ""

        if RULES_DIR.exists():
            for rule_file in RULES_DIR.glob("*.md"):
                with open(rule_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    rules_content += f"## {rule_file.name}\n\n"
                    rules_content += content + "\n\n"

        return rules_content

    def load_base_theory(self) -> str:
        """
        加载0/1重基底理论
        用于在长会话中重新注入理论基础
        """
        base_docs = [
            "四位一体驻波动力学框架本源知识库：0-4重基底完整理论文档合集.md",
            "元本体理论分册.md",
            "第一层1到9模块大一统理论终极不可改基底.md",
        ]

        theory_content = ""
        for doc_name in base_docs:
            doc_path = THEORY_DIR / doc_name
            if doc_path.exists():
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read(5000)
                    theory_content += f"## {doc_name}\n\n"
                    theory_content += content[:3000] + "\n\n"

        return theory_content

    def build_system_prompt(self, stage: str = "") -> str:
        """
        构建系统提示词
        参数：stage - 当前阶段（用于SOLO子任务重置）
        返回：完整的系统提示词
        """
        prompt = "\n" + "=" * 80 + "\n"
        prompt += "## 【强制前置规则】四位一体驻波动力学框架约束\n"
        prompt += "=" * 80 + "\n\n"

        prompt += self.load_top_rules()

        prompt += "## 【基底理论注入】\n\n"
        prompt += self.load_base_theory()

        if stage:
            prompt += f"## 【当前阶段】{stage}\n\n"
            prompt += "本阶段结束后将重置系统提示词，确保规则不被遗忘。\n\n"

        prompt += "=" * 80 + "\n"
        prompt += "## 【规则结束】约束注入完成\n"
        prompt += "=" * 80 + "\n\n"

        self.system_prompt_stack.append({
            "stage": stage,
            "timestamp": datetime.datetime.now().isoformat(),
            "length": len(prompt),
        })

        if len(self.system_prompt_stack) > 5:
            self.system_prompt_stack = self.system_prompt_stack[-3:]

        return prompt

    def check_need_reload(self) -> Tuple[bool, str]:
        """
        检查是否需要重新加载规则
        返回：(是否需要, 原因)
        """
        self.conversation_round += 1

        if self.conversation_round % RELOAD_INTERVAL_ROUNDS == 0:
            return True, f"达到{RELOAD_INTERVAL_ROUNDS}轮对话，需要重新加载规则"

        if self.last_reload_time:
            elapsed = (datetime.datetime.now() - self.last_reload_time).total_seconds()
            if elapsed > RULES_CACHE_TTL:
                return True, f"规则缓存已过期（{elapsed:.0f}秒 > {RULES_CACHE_TTL}秒）"

        return False, "无需重新加载"

    def reload_rules(self) -> Dict:
        """
        重新加载规则
        返回：重加载结果
        """
        print("\n[RULE RELOAD] 🔄 重新加载规则...")

        start_time = datetime.datetime.now()

        try:
            rules_content = self.load_top_rules()
            theory_content = self.load_base_theory()

            self.rules_cache = {
                "top_rules": rules_content,
                "base_theory": theory_content,
                "reload_time": start_time.isoformat(),
                "rules_length": len(rules_content),
                "theory_length": len(theory_content),
            }

            self.last_reload_time = start_time
            self.base_rules_injected = True

            result = {
                "status": "success",
                "message": "规则重新加载成功",
                "rules_length": len(rules_content),
                "theory_length": len(theory_content),
                "reload_time": start_time.isoformat(),
                "round": self.conversation_round,
            }

            print(f"[RULE RELOAD] ✅ 规则重新加载成功")
            print(f"  顶层规则: {len(rules_content)} 字符")
            print(f"  基底理论: {len(theory_content)} 字符")
            print(f"  当前对话轮次: {self.conversation_round}")

        except Exception as e:
            result = {
                "status": "failed",
                "message": f"规则重新加载失败: {str(e)}",
                "reload_time": start_time.isoformat(),
            }
            print(f"[RULE RELOAD] ❌ 规则重新加载失败: {e}")

        return result

    def reset_system_prompt(self, stage: str = "") -> str:
        """
        重置系统提示词（SOLO子任务专用）
        参数：stage - 当前阶段
        返回：新的系统提示词
        """
        print(f"\n[PROMPT RESET] 🚀 重置系统提示词（阶段：{stage}）")
        new_prompt = self.build_system_prompt(stage)
        print(f"[PROMPT RESET] ✅ 提示词已重置，长度: {len(new_prompt)} 字符")
        return new_prompt

    def get_dilution_warning(self) -> Optional[str]:
        """
        获取上下文稀释警告
        如果规则注入时间过长，返回警告信息
        """
        if not self.last_reload_time:
            return "警告：规则从未加载，可能存在上下文稀释风险"

        elapsed_minutes = (datetime.datetime.now() - self.last_reload_time).total_seconds() / 60

        if elapsed_minutes > 30:
            return f"警告：规则已{elapsed_minutes:.0f}分钟未加载，建议重新注入"

        if self.conversation_round > RELOAD_INTERVAL_ROUNDS * 2:
            return f"警告：已进行{self.conversation_round}轮对话，建议重新加载规则"

        return None

    def generate_session_report(self) -> str:
        """生成会话规则状态报告"""
        report_path = PROJECT_ROOT / "会话规则状态报告.md"

        dilution_warning = self.get_dilution_warning()

        content = f"""# 会话规则状态报告

## 报告信息

| 项目 | 内容 |
|------|------|
| 生成时间 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| 当前对话轮次 | {self.conversation_round} |
| 规则重加载间隔 | {RELOAD_INTERVAL_ROUNDS} 轮 |
| 规则缓存有效期 | {RULES_CACHE_TTL} 秒 |
| 上一次重加载时间 | {self.last_reload_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_reload_time else '从未'} |
| 基底规则已注入 | {'是' if self.base_rules_injected else '否'} |

## 上下文稀释警告

"""

        if dilution_warning:
            content += f"> ⚠️ {dilution_warning}\n\n"
        else:
            content += "> ✅ 正常 - 无上下文稀释风险\n\n"

        content += "## 系统提示词历史\n\n"
        if self.system_prompt_stack:
            for i, entry in enumerate(reversed(self.system_prompt_stack)):
                content += f"- **第{i+1}次**（{entry['stage']}）: {entry['length']} 字符 - {entry['timestamp']}\n"
        else:
            content += "- 无提示词重置记录\n\n"

        content += "## 规则重加载策略\n\n"
        content += "### 自动重加载条件\n\n"
        content += "1. **对话轮次触发**：每{RELOAD_INTERVAL_ROUNDS}轮对话自动重新加载\n"
        content += "2. **时间过期触发**：规则缓存超过{RULES_CACHE_TTL}秒自动重新加载\n"
        content += "3. **SOLO子任务触发**：每个SOLO阶段开始时重置系统提示词\n\n"
        content += "### 防护措施\n\n"
        content += "1. 拆分常驻轻量校验Skill和单次Builder专用Skill\n"
        content += "2. 超长会话每10轮重新加载顶层.rules完整约束\n"
        content += "3. SOLO每一步子任务重置系统提示词\n"
        content += "4. 定期检查上下文稀释风险并发出警告\n\n"
        content += "---\n"
        content += "本报告由会话规则重加载器自动生成\n"
        content += "理论基准：四位一体驻波动力学框架\n"

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[INFO] 会话规则状态报告已生成: {report_path}")
        return str(report_path)


def test_reloader():
    """测试会话规则重加载器"""
    reloader = SessionRuleReloader()

    print("\n[TEST 1] 加载顶层规则...")
    rules = reloader.load_top_rules()
    print(f"  规则长度: {len(rules)} 字符")

    print("\n[TEST 2] 构建系统提示词...")
    prompt = reloader.build_system_prompt("代码生成阶段")
    print(f"  提示词长度: {len(prompt)} 字符")

    print("\n[TEST 3] 模拟多轮对话...")
    for i in range(12):
        need_reload, reason = reloader.check_need_reload()
        print(f"  轮次 {i+1}: {'🔄 需要重加载' if need_reload else '✓ 正常'} - {reason}")
        if need_reload:
            reloader.reload_rules()

    print("\n[TEST 4] 重置系统提示词...")
    new_prompt = reloader.reset_system_prompt("实验验证阶段")
    print(f"  新提示词长度: {len(new_prompt)} 字符")

    print("\n[TEST 5] 检查稀释警告...")
    warning = reloader.get_dilution_warning()
    print(f"  警告: {warning or '无'}")

    reloader.generate_session_report()


def main():
    """主程序入口"""
    print("=" * 60)
    print("场3-10：会话规则重加载器")
    print(f"归属基底：第本体拓扑位（第一位）")
    print(f"对应公理：公理二（自主科研闭环动力学公理）")
    print("=" * 60)

    test_reloader()


if __name__ == "__main__":
    main()
