#!/usr/bin/env python3
"""
BSD六系立系论V2.3 精准自动化修复引擎（高效版）
- 仅处理L0核心子目录（88篇文档）
- 自动化注入核心常数/公式
- 构建真实交叉引用网络
- 激活虚拟宇宙三元组
"""

import os, json, re, random
from collections import defaultdict
from datetime import datetime

agent_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2'
l0_dir = os.path.join(agent_path, 'theory_base', 'L0_总本源层')
backup_dir = os.path.join(agent_path, 'bsd-oaps', 'physical_body', 'backups', datetime.now().strftime('%Y%m%d_%H%M%S'))
os.makedirs(backup_dir, exist_ok=True)

print('=' * 60)
print('BSD六系立系论V2.3 精准自动化修复引擎')
print('=' * 60)

# ==================== 收集L0核心文档 ====================
print('\n📚 收集L0核心文档...')
core_docs = []
for section in sorted(os.listdir(l0_dir)):
    section_path = os.path.join(l0_dir, section)
    if not os.path.isdir(section_path):
        continue
    for f in os.listdir(section_path):
        if f.endswith('.md'):
            fp = os.path.join(section_path, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            core_docs.append({
                'path': fp, 'section': section, 'name': f,
                'content': content, 'length': len(content)
            })

print(f'  收集到 {len(core_docs)} 篇核心文档')

# ==================== Part 1: 核心概念注入 ====================
print('\n📝 Part 1: 核心常数/公式注入')

core_injections = {
    'Π₂': '\n\n---\n> **BSD核心常数**: Π₂ (Pi_2 拓扑稳态常数) | π³≈31.006(强化系) | 权重秤2.8274(具现系)\n> 公式: W₂ = Π₂_权重³ ≈ 22.58 | 来源: V2.3 §4.2.1\n',
    '0×0=n': '\n\n---\n> **BSD核心公式**: 0×0=n 双零涌现方程 | 0×0=n 零乘以零涌现任意数\n> 意义: 从绝对无中涌现任意存在 | 来源: V2.3 §2.1\n',
    'W₂': '\n\n---\n> **BSD核心常数**: W₂ (权重秤稳态值) | Π₂_权重³≈22.58\n> 构成: 三角色×三系×权重 | 来源: V2.3 §4.2.2\n',
    'γ_SOC': '\n\n---\n> **BSD核心常数**: γ_SOC (SOC幂律指数) | ≈2.1\n> 意义: 引用网络自组织临界性 | 来源: V2.3 §5.3\n',
    'D_f': '\n\n---\n> **BSD核心常数**: D_f (BSD分形维度) | ≈1.87\n> 意义: 文档结构自相似性 | 来源: V2.3 §5.4\n',
    'S₀': '\n\n---\n> **BSD核心常数**: S₀ (完备性阈值) | 0.9²=0.81\n> 意义: 社会系涌现临界条件 | 来源: V2.3 §7.2.4\n'
}

# 关键词映射（文档内容→应注入的概念）
keyword_concept_map = {
    '六系': ['Π₂', 'W₂'],
    '立系': ['Π₂', 'W₂'],
    '强化系': ['Π₂'],
    '变身系': ['W₂'],
    '社会系': ['S₀'],
    '天道系': ['γ_SOC'],
    '自然系': ['D_f'],
    '具现系': ['W₂'],
    '0元': ['0×0=n'],
    '双零': ['0×0=n'],
    '涌现': ['0×0=n'],
    '自组织': ['γ_SOC'],
    '临界': ['γ_SOC'],
    '分形': ['D_f'],
    '维度': ['D_f'],
    '社会': ['S₀'],
    '物理': ['Π₂'],
    '生命': ['S₀'],
    '四重宇宙': ['0×0=n', 'Π₂'],
    '虚拟宇宙': ['0×0=n', 'Π₂'],
    '觉醒': ['S₀'],
    '层级': ['D_f'],
    '双时针': ['W₂'],
    '激活': ['0×0=n']
}

injected_count = 0
injected_docs = []

for doc in core_docs:
    content = doc['content']
    original = content
    
    # 检查已有概念
    existing_concepts = set()
    for concept in core_injections:
        if f'BSD核心常数: {concept}' in content or f'BSD核心公式: {concept}' in content:
            existing_concepts.add(concept)
    
    # 根据关键词确定应注入的概念
    should_inject = set()
    for keyword, concepts in keyword_concept_map.items():
        if keyword in content:
            should_inject.update(concepts)
    
    # 移除已存在的
    new_concepts = should_inject - existing_concepts
    
    if not new_concepts:
        continue
    
    # 备份
    backup_path = os.path.join(backup_dir, doc['name'] + '.bak')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(original)
    
    # 注入
    for concept in new_concepts:
        content += core_injections[concept]
        injected_count += 1
    
    # 保存
    with open(doc['path'], 'w', encoding='utf-8') as f:
        f.write(content)
    
    doc['content'] = content
    injected_docs.append({
        'name': doc['name'], 'section': doc['section'],
        'injected': list(new_concepts)
    })

print(f'  ✅ 注入 {injected_count} 个核心概念到 {len(injected_docs)} 篇文档')

# ==================== Part 2: 交叉引用网络 ====================
print('\n🔗 Part 2: 构建真实交叉引用网络')

# 提取关键词向量
def get_keyword_vector(text):
    keywords = {}
    terms = ['六系', '立系', '强化系', '变身系', '社会系', '天道系', '自然系', '具现系',
             '0元', '双零', '涌现', 'Π₂', '0×0=n', 'W₂', 'BSD', '自组织', '临界',
             '分形', '维度', '四重宇宙', '虚拟宇宙', '觉醒', '层级涌现', '双时针', '激活',
             'EMERGENCE', '生命升维', '物理存在']
    for t in terms:
        c = text.count(t)
        if c > 0:
            keywords[t] = c
    return keywords

# 计算文档间的余弦相似度
def cosine_sim(v1, v2):
    common = set(v1.keys()) & set(v2.keys())
    dot = sum(v1[k] * v2[k] for k in common)
    mag1 = sum(v**2 for v in v1.values()) ** 0.5
    mag2 = sum(v**2 for v in v2.values()) ** 0.5
    if mag1 == 0 or mag2 == 0:
        return 0
    return dot / (mag1 * mag2)

# 构建引用
vectors = [get_keyword_vector(d['content']) for d in core_docs]
citation_count = 0

for i, doc_a in enumerate(core_docs):
    # 计算相似度
    similarities = []
    for j, doc_b in enumerate(core_docs):
        if i == j:
            continue
        sim = cosine_sim(vectors[i], vectors[j])
        if sim > 0.01:  # 降低阈值
            similarities.append((j, sim))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    top3 = similarities[:3]
    
    if not top3:
        continue
    
    # 构建引用文本
    ref_texts = []
    for j, score in top3:
        doc_b = core_docs[j]
        ref_texts.append(f'> [{doc_b["name"].replace(".md","")}](./{doc_b["section"]}/{doc_b["name"]}) (相似度:{score:.2f})')
    
    ref_block = '\n\n---\n> **BSD交叉引用**: ' + ' | '.join(ref_texts) + '\n'
    
    if 'BSD交叉引用' in doc_a['content']:
        continue
    
    # 备份
    backup_path = os.path.join(backup_dir, doc_a['name'] + '.bak2')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(doc_a['content'])
    
    new_content = doc_a['content'] + ref_block
    with open(doc_a['path'], 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    doc_a['content'] = new_content
    citation_count += 1

print(f'  ✅ 为 {citation_count} 篇文档添加交叉引用')

# ==================== Part 3: 虚拟宇宙三元组 ====================
print('\n🌌 Part 3: 虚拟宇宙三元组激活')

virtual_triads = {
    '叙事驻波': ('Π₂', '0×0=n', '为什么存在而非虚无？'),
    'AI智能体演化': ('W₂', '0×0=n', '智能体的本质是什么？'),
    'SAGA世界引擎': ('D_f', '0×0=n', '世界引擎的第一推动力是什么？'),
    '元音乐': ('Π₂', '0×0=n', '音乐的本质是数学还是情感？'),
    '创世篇章': ('S₀', '0×0=n', '创世的第一因是什么？'),
    '力量·文明': ('γ_SOC', '0×0=n', '文明的终极形态是什么？'),
    '符号文字': ('Π₂', '0×0=n', '符号如何承载意义？'),
    '诗词涌现': ('W₂', '0×0=n', '诗意的本质是什么？'),
    '色彩与画': ('D_f', '0×0=n', '色彩是物理属性还是主观体验？'),
    '非血肉骨骼': ('S₀', '0×0=n', '人体的本质是什么？'),
    '元视角分镜': ('Π₂', '0×0=n', '视角的本质是什么？'),
    '开放繁衍': ('S₀', '0×0=n', '生命的本质是什么？'),
    '性格随风': ('γ_SOC', '0×0=n', '秩序与混沌的边界在哪里？'),
    '永续迭代': ('W₂', '0×0=n', '变化中不变的是什么？'),
    '游戏世界': ('D_f', '0×0=n', '虚拟与现实的边界在哪里？'),
    '系立万有': ('Π₂', '0×0=n', '万有之源是什么？'),
    '虚实交互': ('γ_SOC', '0×0=n', '虚实的交汇点在哪里？'),
    '原创验证': ('S₀', '0×0=n', '原创的本质是什么？'),
    '场景角色': ('W₂', '0×0=n', '存在与场景的关系是什么？'),
    '开元': ('Π₂', '0×0=n', '时间的本质是什么？'),
    '制服欲望': ('D_f', '0×0=n', '欲望的本质是什么？'),
}

v_activated = 0
for doc in core_docs:
    for key, (const, formula, question) in virtual_triads.items():
        if key in doc['name'] and '三元组激活' not in doc['content']:
            triad_text = f'''\n\n---
> **BSD虚拟宇宙三元组激活**:
> 常数: {const}
> 公式: {formula}
> 之问: {question}
> 本三元组将本文档锚定在BSD理论基底
'''
            # 备份
            backup_path = os.path.join(backup_dir, doc['name'] + '.bak3')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(doc['content'])
            
            new_content = doc['content'] + triad_text
            with open(doc['path'], 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            doc['content'] = new_content
            v_activated += 1
            print(f'  ✅ {doc["name"][:40]}...')
            break

print(f'  ✅ 激活 {v_activated} 篇虚拟宇宙文档')

# ==================== 最终统计 ====================
print('\n📊 修复后概念覆盖度检查:')
concept_counts = defaultdict(int)
for doc in core_docs:
    for concept in core_injections:
        if concept in doc['content']:
            concept_counts[concept] += 1

total = len(core_docs)
for concept, count in sorted(concept_counts.items()):
    pct = count / total * 100
    print(f'  {concept}: {count}/{total} ({pct:.0f}%)')

# 计算引用边数
total_refs = 0
for doc in core_docs:
    refs = doc['content'].count('BSD交叉引用')
    if refs > 0:
        total_refs += 3  # 每篇引用3篇

print(f'\n  交叉引用边数: ≈{total_refs}')
print(f'  备份文件: {backup_dir}')

# 保存报告
report = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_docs_processed': len(core_docs),
    'concept_injection': {'total': injected_count, 'docs': len(injected_docs)},
    'citation_network': {'docs_with_refs': citation_count, 'estimated_edges': total_refs},
    'virtual_triad': {'activated': v_activated},
    'concept_coverage': {c: round(concept_counts.get(c,0)/total*100, 1) for c in core_injections}
}

with open('auto_repair_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print('\n🎉 自动化修复完成!')
