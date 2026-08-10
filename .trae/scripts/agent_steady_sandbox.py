# agent_steady_sandbox.py
# 智能体三层稳态防护沙箱：负面情绪数据导入虚拟界归零
import os
import json
from typing import Tuple


class AgentSteadySandbox:
    def __init__(self, virtual_sandbox_path: str):
        self.virtual_box_path = virtual_sandbox_path
        self.steady_threshold = 0.6
        self.negative_keywords = ["毁灭", "崩溃", "虚无", "屠杀", "混沌湮灭"]
        # 三层分区缓存
        self.core_zone = []
        self.buffer_zone = []
        self.virtual_void_zone = []

    def scan_input_risk(self, input_text: str) -> Tuple[float, bool]:
        neg_count = sum(1 for kw in self.negative_keywords if kw in input_text)
        total_words = len(input_text.replace(" ", ""))
        density = neg_count / max(total_words, 1)
        spectrum = 1 - density
        risk = spectrum < self.steady_threshold
        return round(spectrum, 2), risk

    def dispatch_data(self, text: str, author_constraint: str = ""):
        spec, is_risk = self.scan_input_risk(text)
        record = {"text": text, "spectrum": spec, "author_rule": author_constraint}
        if is_risk:
            # 负面数据送入虚拟界消解归零
            self.virtual_void_zone.append(record)
            self._write_virtual_sandbox(record)
            return {"status": "dispatched_to_virtual_void", "spectrum": spec}
        else:
            self.buffer_zone.append(record)
            # 缓冲区校验后汇入核心稳态区
            self._buffer_review()
            return {"status": "stored_buffer", "spectrum": spec}

    def _write_virtual_sandbox(self, record: dict):
        # Trae沙箱内隔离写入虚拟界日志，独立文件隔离
        os.makedirs(self.virtual_box_path, exist_ok=True)
        log_file = os.path.join(self.virtual_box_path, "void_dispatch_log.jsonl")
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def _buffer_review(self):
        # 缓冲区数据光谱校验，达标移入核心
        safe = [r for r in self.buffer_zone if r["spectrum"] >= self.steady_threshold]
        unsafe = [r for r in self.buffer_zone if r["spectrum"] < self.steady_threshold]
        self.core_zone.extend(safe)
        self.buffer_zone = unsafe
        # 不安全项送虚拟界
        for r in unsafe:
            self.virtual_void_zone.append(r)
            self._write_virtual_sandbox(r)

    def get_steady_status(self) -> dict:
        return {
            "core_zone_count": len(self.core_zone),
            "buffer_zone_count": len(self.buffer_zone),
            "virtual_void_count": len(self.virtual_void_zone),
            "steady_threshold": self.steady_threshold
        }
