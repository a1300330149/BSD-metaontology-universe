"""
BSD知识提取器 - 从theory_base提取知识单元
==========================================
扫描645篇理论文档，提取公理、定理、方程、哲学之问，
转化为可量化的BSD知识单元。
"""

import os
import re
import json
import hashlib
from typing import Dict, List, Tuple
from dataclasses import dataclass, field


@dataclass
class ExtractedKnowledge:
    """从文档中提取的知识单元"""
    
    knowledge_id: str
    knowledge_type: str  # 公理/定理/方程/哲学/定义/方法
    title: str
    content: str
    source_file: str
    source_layer: str
    value: float
    confidence: float = 1.0
    
    def to_dict(self) -> Dict:
        return {
            "knowledge_id": self.knowledge_id,
            "knowledge_type": self.knowledge_type,
            "title": self.title,
            "content": self.content[:200],
            "source_file": self.source_file,
            "source_layer": self.source_layer,
            "value": self.value,
            "confidence": self.confidence
        }


class BSDKnowledgeExtractor:
    """BSD知识提取器"""
    
    # 知识类型与基础价值
    TYPE_BASE_VALUES = {
        "公理": 100.0,
        "定理": 60.0,
        "方程": 40.0,
        "哲学": 30.0,
        "定义": 20.0,
        "方法": 15.0,
        "实例": 10.0
    }
    
    # 层级价值系数（L0最高）
    LAYER_MULTIPLIERS = {
        "L0": 1.0,
        "L1": 0.9,
        "L2": 0.8,
        "L3": 0.7,
        "L4": 0.6,
        "L5": 0.5
    }
    
    # 关键词模式
    PATTERNS = {
        "公理": [
            r"公理[：:]\s*(.+?)(?:\n|$)",
            r"公理\s*[A-Z0-9一二三四五六七八九十]+[：:]\s*(.+?)(?:\n|$)",
            r"[§§]\d+.*?公理[：:]\s*(.+?)(?:\n|$)",
            r"核心公理[：:]\s*(.+?)(?:\n|$)"
        ],
        "定理": [
            r"定理[：:]\s*(.+?)(?:\n|$)",
            r"定理\s*[一二三四五六七八九十]+[：:]\s*(.+?)(?:\n|$)",
            r"[§§]\d+.*?定理[：:]\s*(.+?)(?:\n|$)",
            r"核心定理[：:]\s*(.+?)(?:\n|$)"
        ],
        "方程": [
            r"[A-Z]\d*\s*[=≠≤≥]\s*.+?\n",
            r"[A-Z][₀-₉]+\s*[=≠≤≥]\s*.+?\n",
            r"方程[：:]\s*(.+?)(?:\n|$)",
            r"公式[：:]\s*(.+?)(?:\n|$)",
            r"[ΠΣΩ]+.*?[=≠].+?\n"
        ],
        "哲学": [
            r"哲学[之问题题][：:]\s*(.+?)(?:\n|$)",
            r"[哲学之问问][：:]\s*(.+?)(?:\n|$)",
            r"本质[是为][：:]\s*(.+?)(?:\n|$)"
        ],
        "定义": [
            r"定义[：:]\s*(.+?)(?:\n|$)",
            r"[Dd]efinition[：:]\s*(.+?)(?:\n|$)"
        ],
        "方法": [
            r"方法[：:]\s*(.+?)(?:\n|$)",
            r"实现[：:]\s*(.+?)(?:\n|$)"
        ]
    }
    
    def __init__(self, theory_base_path: str):
        self.theory_base_path = theory_base_path
        self.extracted_knowledge: List[ExtractedKnowledge] = []
        self.processed_files = 0
        self.failed_files = 0
        
    def scan_all_documents(self) -> List[Dict]:
        """扫描所有文档"""
        print(f"\n{'='*60}")
        print(f"  扫描theory_base文档")
        print(f"{'='*60}")
        
        docs = []
        for root, dirs, files in os.walk(self.theory_base_path):
            level = self._detect_layer(root)
            
            for f in files:
                if f.endswith(('.md', '.json', '.txt')):
                    fp = os.path.join(root, f)
                    size = os.path.getsize(fp)
                    if size > 50:  # 最小50字节
                        docs.append({
                            "path": fp,
                            "relative": os.path.relpath(fp, self.theory_base_path),
                            "size": size,
                            "layer": level
                        })
        
        print(f"\n  找到 {len(docs)} 个文档文件")
        
        # 按大小排序
        docs.sort(key=lambda x: x["size"], reverse=True)
        
        return docs
    
    def _detect_layer(self, path: str) -> str:
        """检测文档所在层级"""
        for layer in ["L0", "L1", "L2", "L3", "L4", "L5"]:
            if layer in path:
                return layer
        return "unknown"
    
    def extract_from_file(self, filepath: str, layer: str) -> List[ExtractedKnowledge]:
        """从单个文件提取知识"""
        extracted = []
        
        try:
            # 读取文件内容
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # 跳过空文件
            if len(content) < 100:
                return []
            
            # 提取文件标题
            title = self._extract_title(content, filepath)
            
            # 按知识类型提取
            kid_base = os.path.basename(filepath).replace('.md', '').replace('.json', '').replace('.txt', '')
            
            # 1. 提取公理
            axioms = self._extract_by_patterns(content, "公理")
            for i, axiom in enumerate(axioms[:5]):  # 每个文件最多5个
                kid = f"BSD-E{len(self.extracted_knowledge)+1:04d}"
                value = self.TYPE_BASE_VALUES["公理"] * self.LAYER_MULTIPLIERS.get(layer, 0.5)
                extracted.append(ExtractedKnowledge(
                    knowledge_id=kid,
                    knowledge_type="公理",
                    title=f"{title} - 公理{i+1}",
                    content=axiom.strip(),
                    source_file=os.path.basename(filepath),
                    source_layer=layer,
                    value=value,
                    confidence=0.9
                ))
            
            # 2. 提取定理
            theorems = self._extract_by_patterns(content, "定理")
            for i, theorem in enumerate(theorems[:5]):
                kid = f"BSD-E{len(self.extracted_knowledge)+1:04d}"
                value = self.TYPE_BASE_VALUES["定理"] * self.LAYER_MULTIPLIERS.get(layer, 0.5)
                extracted.append(ExtractedKnowledge(
                    knowledge_id=kid,
                    knowledge_type="定理",
                    title=f"{title} - 定理{i+1}",
                    content=theorem.strip(),
                    source_file=os.path.basename(filepath),
                    source_layer=layer,
                    value=value,
                    confidence=0.85
                ))
            
            # 3. 提取方程
            equations = self._extract_by_patterns(content, "方程")
            for i, equation in enumerate(equations[:5]):
                kid = f"BSD-E{len(self.extracted_knowledge)+1:04d}"
                value = self.TYPE_BASE_VALUES["方程"] * self.LAYER_MULTIPLIERS.get(layer, 0.5)
                extracted.append(ExtractedKnowledge(
                    knowledge_id=kid,
                    knowledge_type="方程",
                    title=f"{title} - 方程{i+1}",
                    content=equation.strip(),
                    source_file=os.path.basename(filepath),
                    source_layer=layer,
                    value=value,
                    confidence=0.8
                ))
            
            # 4. 提取哲学之问
            philosophies = self._extract_by_patterns(content, "哲学")
            for i, phil in enumerate(philosophies[:3]):
                kid = f"BSD-E{len(self.extracted_knowledge)+1:04d}"
                value = self.TYPE_BASE_VALUES["哲学"] * self.LAYER_MULTIPLIERS.get(layer, 0.5)
                extracted.append(ExtractedKnowledge(
                    knowledge_id=kid,
                    knowledge_type="哲学",
                    title=f"{title} - 哲学{i+1}",
                    content=phil.strip(),
                    source_file=os.path.basename(filepath),
                    source_layer=layer,
                    value=value,
                    confidence=0.75
                ))
            
            # 5. 如果没有匹配到特定模式，提取段落摘要
            if not extracted:
                summaries = self._extract_summary(content, title)
                for i, summary in enumerate(summaries[:2]):
                    kid = f"BSD-E{len(self.extracted_knowledge)+1:04d}"
                    value = self.TYPE_BASE_VALUES["定义"] * self.LAYER_MULTIPLIERS.get(layer, 0.5)
                    extracted.append(ExtractedKnowledge(
                        knowledge_id=kid,
                        knowledge_type="定义",
                        title=f"{title} - 摘要{i+1}",
                        content=summary,
                        source_file=os.path.basename(filepath),
                        source_layer=layer,
                        value=value,
                        confidence=0.6
                    ))
            
            self.processed_files += 1
            
        except Exception as e:
            self.failed_files += 1
            if self.failed_files <= 5:
                print(f"    提取失败: {os.path.basename(filepath)} - {str(e)[:50]}")
        
        return extracted
    
    def _extract_title(self, content: str, filepath: str) -> str:
        """提取文档标题"""
        # 查找Markdown标题
        title_match = re.search(r'^#\s+(.+?)(?:\n|$)', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()[:50]
        
        # 使用文件名
        basename = os.path.basename(filepath)
        return basename.replace('.md', '').replace('.json', '')[:50]
    
    def _extract_by_patterns(self, content: str, knowledge_type: str) -> List[str]:
        """按模式提取知识"""
        results = []
        patterns = self.PATTERNS.get(knowledge_type, [])
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.MULTILINE)
            for match in matches:
                match = match.strip()
                if len(match) > 10 and match not in results:
                    results.append(match)
        
        return results
    
    def _extract_summary(self, content: str, title: str) -> List[str]:
        """提取段落摘要"""
        summaries = []
        
        # 按段落分割
        paragraphs = re.split(r'\n\s*\n', content)
        
        for para in paragraphs:
            para = para.strip()
            if len(para) > 50 and len(para) < 300:
                # 移除Markdown格式
                clean = re.sub(r'[#*`>|-]', '', para)
                clean = re.sub(r'\s+', ' ', clean).strip()
                if len(clean) > 30:
                    summaries.append(clean)
        
        return summaries[:3]
    
    def run_full_extraction(self, max_docs: int = None) -> Dict:
        """运行完整提取流程"""
        print(f"\n{'='*60}")
        print(f"  BSD知识提取器 - 全量提取")
        print(f"{'='*60}")
        
        # 1. 扫描文档
        docs = self.scan_all_documents()
        
        if max_docs:
            docs = docs[:max_docs]
        
        print(f"\n  将处理 {len(docs)} 个文档")
        
        # 2. 逐文件提取
        for i, doc in enumerate(docs):
            if (i + 1) % 50 == 0 or i == 0:
                print(f"    处理进度: {i+1}/{len(docs)} ({(i+1)/len(docs)*100:.0f}%)")
            
            extracted = self.extract_from_file(doc["path"], doc["layer"])
            self.extracted_knowledge.extend(extracted)
        
        # 3. 生成统计
        stats = self._generate_stats()
        
        print(f"\n{'='*60}")
        print(f"  提取完成统计")
        print(f"{'='*60}")
        print(f"\n  处理文件: {self.processed_files} 个")
        print(f"  提取知识: {len(self.extracted_knowledge)} 个单元")
        print(f"  失败文件: {self.failed_files} 个")
        
        # 按类型统计
        type_counts = {}
        type_values = {}
        for k in self.extracted_knowledge:
            t = k.knowledge_type
            type_counts[t] = type_counts.get(t, 0) + 1
            type_values[t] = type_values.get(t, 0) + k.value
        
        print(f"\n  [类型分布]")
        for t, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"    {t}: {count}个, {type_values[t]:.0f} BSD币")
        
        total_value = sum(k.value for k in self.extracted_knowledge)
        print(f"\n  [总价值] {total_value:.0f} BSD币")
        
        return stats
    
    def _generate_stats(self) -> Dict:
        """生成统计信息"""
        type_dist = {}
        layer_dist = {}
        
        for k in self.extracted_knowledge:
            t = k.knowledge_type
            type_dist[t] = type_dist.get(t, 0) + 1
            
            l = k.source_layer
            layer_dist[l] = layer_dist.get(l, 0) + 1
        
        return {
            "total_knowledge": len(self.extracted_knowledge),
            "total_value": sum(k.value for k in self.extracted_knowledge),
            "type_distribution": type_dist,
            "layer_distribution": layer_dist,
            "processed_files": self.processed_files,
            "failed_files": self.failed_files
        }
    
    def export_knowledge_reserve(self, output_path: str = None) -> Dict:
        """导出知识储备"""
        if output_path is None:
            output_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "bsd_knowledge_reserve.json"
            )
        
        # 转为字典列表
        knowledge_list = [k.to_dict() for k in self.extracted_knowledge]
        
        # 保存
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({
                "version": "2.0",
                "total_knowledge": len(knowledge_list),
                "total_value": sum(k["value"] for k in knowledge_list),
                "knowledge": knowledge_list,
                "generated_at": __import__("time").time()
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n  知识储备已导出: {output_path}")
        print(f"    知识单元: {len(knowledge_list)} 个")
        print(f"    总价值: {sum(k['value'] for k in knowledge_list):.0f} BSD币")
        
        return {
            "output_path": output_path,
            "total_knowledge": len(knowledge_list),
            "total_value": sum(k["value"] for k in knowledge_list)
        }


def main():
    """主程序"""
    
    # 查找theory_base
    theory_base_paths = [
        r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base",
        r"C:\Users\13003\OneDrive\桌面\3333333\theory_base",
    ]
    
    theory_base = None
    for p in theory_base_paths:
        if os.path.exists(p):
            theory_base = p
            break
    
    if not theory_base:
        print("未找到theory_base目录")
        return
    
    print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                              BSD知识提取器                                                              ║
║                                                                                                        ║
║  目标：从 {theory_base} 提取BSD理论知识                                                               ║
║  输出：BSD知识储备（量化为BSD币）                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
    
    # 初始化提取器
    extractor = BSDKnowledgeExtractor(theory_base)
    
    # 运行全量提取
    stats = extractor.run_full_extraction(max_docs=200)  # 先处理200个文档
    
    # 导出知识储备
    export_result = extractor.export_knowledge_reserve()
    
    print(f"\n{'='*60}")
    print(f"  下一步")
    print(f"{'='*60}")
    print(f"""
    1. 知识储备已导出为JSON
    2. 可加载到BSDSoloKnowledgeBridge引擎
    3. 实现大规模知识级本源对接
    4. 扩展至所有645篇文档
    """)


if __name__ == "__main__":
    main()
