"""
归属基底：第5重分层迭代知识库生长场
对应三界秩序：天道秩序
对应公理：第7条（系统自进化迭代公理）
对应九维维度：天道原理/天道动力学
理论原文出处：《元本体理论分册》第七章
核心数理参数：θ_evo=0.002

场5：向量标签打标脚本
实现知识库内容自动向量标签打标
"""

import os
import json
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# ==================== 固定数理参数（锁档核心） ====================
# SHA256锁档哈希
LOCK_HASH = "e62f918340dc2975108294736ac8927d90584136972485931027958740925713"

# 自进化增量阈值
THETA_EVO = 0.002

# 九维维度标签模板
NINE_DIMENSIONS = [
    "元理天道",
    "载体实体",
    "因果社会",
    "天道原理",
    "天道动力学",
    "自然相变",
    "自然实体",
    "社会创造",
    "社会因果"
]

# 七大公理标签模板
SEVEN_AXIOMS = [
    "axiom_1:宿命双边界公理",
    "axiom_2:自主科研闭环动力学公理",
    "axiom_3:科研价值边际判定公理",
    "axiom_4:选题创化生成机制",
    "axiom_5:成果落地转化范式",
    "axiom_6:全局宿命边界统摄理论",
    "axiom_7:系统自进化迭代公理"
]


class VectorTagger:
    """
    功能：向量标签自动打标处理器
    理论映射：5重分层迭代知识库生长场·系统自进化迭代公理
    能级关联：E3=0.90三阶道心能级标签标准
    约束来源：系统自进化迭代公理（公理七）
    禁止修改：九维维度标签、七大公理标签、基底层级标签
    """
    
    def __init__(self, knowledge_base: str):
        """
        初始化向量标签打标处理器
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：向量标签打标初始化
        
        Args:
            knowledge_base: 知识库目录
        """
        self.knowledge_base = Path(knowledge_base)
        self.tagging_log = []
    
    def scan_documents(self) -> List[Path]:
        """
        扫描知识库文档
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：知识库文档扫描
        
        Returns:
            List[Path]: 文档路径列表
        """
        return list(self.knowledge_base.glob("*.md"))
    
    def extract_content_features(self, content: str) -> Dict:
        """
        提取内容特征
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：内容特征提取
        
        Args:
            content: 文档内容
        
        Returns:
            Dict: 内容特征
        """
        features = {
            "base_level": self._detect_base_level(content),
            "axiom_number": self._detect_axiom(content),
            "dimensions": self._detect_dimensions(content),
            "parameters": self._detect_parameters(content),
            "keywords": self._detect_keywords(content)
        }
        
        return features
    
    def _detect_base_level(self, content: str) -> str:
        """
        检测基底层级
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：基底层级识别
        
        Args:
            content: 文档内容
        
        Returns:
            str: 基底层级标识
        """
        if "0元" in content or "元道本源" in content:
            return "base_0:元道本源基底"
        elif "九维" in content or "法理基底" in content:
            return "base_1:九维法理基底"
        elif "三界" in content or "秩序基底" in content:
            return "base_2:三界秩序基底"
        elif "六阶" in content or "科研基底" in content:
            return "base_3:六阶科研基底"
        elif "智能体" in content or "四层" in content:
            return "base_4:四层智能体基底"
        else:
            return "base_unknown"
    
    def _detect_axiom(self, content: str) -> List[str]:
        """
        检测公理编号
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：公理编号识别
        
        Args:
            content: 文档内容
        
        Returns:
            List[str]: 公理编号列表
        """
        axioms = []
        
        if "双边界" in content or "宿命边界" in content:
            axioms.append(SEVEN_AXIOMS[0])
        if "动力学" in content or "闭环" in content:
            axioms.append(SEVEN_AXIOMS[1])
        if "边际" in content or "价值判定" in content:
            axioms.append(SEVEN_AXIOMS[2])
        if "选题" in content or "创化" in content:
            axioms.append(SEVEN_AXIOMS[3])
        if "转化" in content or "落地" in content:
            axioms.append(SEVEN_AXIOMS[4])
        if "统摄" in content or "全局边界" in content:
            axioms.append(SEVEN_AXIOMS[5])
        if "进化" in content or "迭代" in content:
            axioms.append(SEVEN_AXIOMS[6])
        
        return axioms if axioms else ["axiom_unknown"]
    
    def _detect_dimensions(self, content: str) -> List[str]:
        """
        检测九维维度
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：九维维度识别
        
        Args:
            content: 文档内容
        
        Returns:
            List[str]: 九维维度列表
        """
        dimensions = []
        
        for dim in NINE_DIMENSIONS:
            if dim in content or dim.replace("天道", "") in content:
                dimensions.append(dim)
        
        return dimensions if dimensions else ["dimension_unknown"]
    
    def _detect_parameters(self, content: str) -> Dict:
        """
        检测固定数理参数
        
        对应公理：公理一（宿命/舒适双边界公理）
        理论映射：参数识别
        
        Args:
            content: 文档内容
        
        Returns:
            Dict: 参数字典
        """
        parameters = {}
        
        # 检测γ参数
        if "γ" in content or "gamma" in content.lower():
            parameters["gamma"] = 0.92
        
        # 检测κ参数
        if "κ" in content or "kappa" in content.lower():
            parameters["kappa"] = 0.35
        
        # 检测α参数
        if "α" in content or "alpha" in content.lower():
            parameters["alpha"] = 0.18
        
        # 检测三阶阈值
        if "E1" in content or "E₁" in content:
            parameters["E1"] = 0.35
        if "E2" in content or "E₂" in content:
            parameters["E2"] = 0.65
        if "E3" in content or "E₃" in content:
            parameters["E3"] = 0.90
        
        return parameters
    
    def _detect_keywords(self, content: str) -> List[str]:
        """
        检测关键词
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：关键词提取
        
        Args:
            content: 文档内容
        
        Returns:
            List[str]: 关键词列表
        """
        keywords = []
        
        # 理论关键词
        theory_keywords = [
            "元本体", "九维", "三界", "双边界", "公理",
            "宿命", "舒适", "天道", "自然", "人道",
            "科研", "智能体", "流转矩阵", "能级"
        ]
        
        for kw in theory_keywords:
            if kw in content:
                keywords.append(kw)
        
        return keywords[:10]  # 限制关键词数量
    
    def generate_vector_tags(self, features: Dict) -> Dict:
        """
        生成向量标签
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：向量标签生成
        
        Args:
            features: 内容特征
        
        Returns:
            Dict: 向量标签
        """
        tags = {
            "base_level_tag": features["base_level"],
            "axiom_tags": features["axiom_number"],
            "dimension_tags": features["dimensions"],
            "parameter_tags": features["parameters"],
            "keyword_tags": features["keywords"],
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lock_hash": LOCK_HASH
        }
        
        # 计算标签权重（按基底层级权重排序）
        base_weights = {
            "base_0": 1.0,  # 最高权重
            "base_1": 0.9,
            "base_2": 0.8,
            "base_3": 0.7,
            "base_4": 0.6
        }
        
        base_key = features["base_level"].split(":")[0]
        tags["weight"] = base_weights.get(base_key, 0.5)
        
        return tags
    
    def apply_tags_to_document(self, doc_path: Path) -> bool:
        """
        应用标签到文档
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：标签应用
        
        Args:
            doc_path: 文档路径
        
        Returns:
            bool: 是否成功应用
        """
        content = doc_path.read_text(encoding='utf-8')
        
        # 检查是否已有标签
        if "向量标签" in content:
            self._log(f"{doc_path.name}: 已有向量标签，跳过", "info")
            return False
        
        # 提取特征
        features = self.extract_content_features(content)
        
        # 生成标签
        tags = self.generate_vector_tags(features)
        
        # 生成标签文本
        tag_text = self._generate_tag_text(tags)
        
        # 插入标签
        new_content = tag_text + content
        doc_path.write_text(new_content, encoding='utf-8')
        
        self._log(f"{doc_path.name}: 成功应用向量标签", "success")
        
        return True
    
    def _generate_tag_text(self, tags: Dict) -> str:
        """
        生成标签文本
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：标签文本生成
        
        Args:
            tags: 向量标签
        
        Returns:
            str: 标签文本
        """
        text = f"""
---
向量标签
---

# 基底层级标签
{tags['base_level_tag']}

# 公理标签
{', '.join(tags['axiom_tags'])}

# 九维维度标签
{', '.join(tags['dimension_tags'])}

# 参数标签
"""
        
        for param, value in tags['parameter_tags'].items():
            text += f"- {param}: {value}\n"
        
        text += f"""
# 关键词标签
{', '.join(tags['keyword_tags'])}

# 标签权重
{tags['weight']}

# 标签时间
{tags['timestamp']}

# SHA256锁档哈希
{tags['lock_hash']}

---

"""
        
        return text
    
    def _log(self, message: str, level: str = "info"):
        """
        记录打标日志
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：打标日志记录
        
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
        self.tagging_log.append(entry)
        print(f"[{level.upper()}] {message}")
    
    def run_batch_tagging(self) -> Dict:
        """
        执行批量打标
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：批量向量标签打标
        
        Returns:
            Dict: 打标结果汇总
        """
        docs = self.scan_documents()
        
        results = {
            "total_docs": len(docs),
            "tagged_docs": 0,
            "skipped_docs": 0,
            "tag_details": []
        }
        
        for doc in docs:
            tagged = self.apply_tags_to_document(doc)
            if tagged:
                results["tagged_docs"] += 1
                features = self.extract_content_features(doc.read_text(encoding='utf-8'))
                results["tag_details"].append({
                    "file": doc.name,
                    "base_level": features["base_level"],
                    "axioms": features["axiom_number"],
                    "dimensions": features["dimensions"]
                })
            else:
                results["skipped_docs"] += 1
        
        # 保存打标日志
        log_path = self.knowledge_base.parent / "向量标签打标日志.json"
        log_path.write_text(
            json.dumps(self.tagging_log, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        
        return results
    
    def generate_tag_report(self) -> str:
        """
        生成标签报告
        
        对应公理：公理七（系统自进化迭代公理）
        理论映射：标签报告输出
        
        Returns:
            str: 报告文件路径
        """
        results = self.run_batch_tagging()
        
        report_path = self.knowledge_base.parent / "向量标签报告.md"
        
        content = f"""# 向量标签报告

## 生成时间
{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## SHA256锁档哈希
{LOCK_HASH}

## 打标结果汇总

| 指标 | 数值 |
|------|------|
| 文档总数 | {results['total_docs']} |
| 已打标文档 | {results['tagged_docs']} |
| 跳过文档 | {results['skipped_docs']} |
| 打标率 | {results['tagged_docs'] / results['total_docs'] * 100:.2f}% |

## 标签详情

| 文件名 | 基底层级 | 公理标签 | 九维维度 |
|--------|----------|----------|----------|
"""
        
        for detail in results["tag_details"]:
            content += f"| {detail['file']} | {detail['base_level']} | {', '.join(detail['axioms'][:2])} | {', '.join(detail['dimensions'][:2])} |\n"
        
        content += "\n---\n"
        content += "本报告由向量标签打标处理器自动生成，遵循四位一体驻波动力学框架理论约束。\n"
        
        report_path.write_text(content, encoding='utf-8')
        
        return str(report_path)


def main():
    """
    主程序入口
    
    对应公理：公理七（系统自进化迭代公理）
    理论映射：向量标签打标启动
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="场5：向量标签打标处理器")
    parser.add_argument("--knowledge-base", default="theory_base", help="知识库目录")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("场5：向量标签打标处理器")
    print("归属基底：第5重分层迭代知识库生长场")
    print("对应公理：公理七（系统自进化迭代公理）")
    print("=" * 60)
    
    tagger = VectorTagger(args.knowledge_base)
    report_path = tagger.generate_tag_report()
    
    print(f"\n向量标签报告: {report_path}")
    
    print("\n" + "=" * 60)
    print("SHA256锁档哈希:", LOCK_HASH)
    print("=" * 60)


if __name__ == "__main__":
    main()