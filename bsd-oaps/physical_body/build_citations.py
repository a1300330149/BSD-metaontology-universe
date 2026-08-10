#!/usr/bin/env python3
"""
BSD交叉引用网络构建器
基于当前文档内容构建真实交叉引用
"""

import os, json, re
from collections import defaultdict
from datetime import datetime

agent_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2'
l0_dir = os.path.join(agent_path, 'theory_base', 'L0_总本源层')

print('=' * 60)
print('BSD交叉引用网络构建器')
print('=' * 60)

# 收集所有L0核心文档
print('\n📚 收集文档...')
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
                'content': content
            })

print(f'  收集到 {len(core_docs)} 篇文档')

# 提取关键词
def get_keywords(text):
    kws = {}
    for t in ['六系', '立系', '强化系', '变身系', '社会系', '天道系', '自然系', '具现系',
              '0元', '双零', '涌现', 'Π₂', '0×0=n', 'W₂', 'BSD', '自组织', '临界',
              '分形', '维度', '四重宇宙', '虚拟宇宙', '觉醒', '层级涌现', '双时针', '激活',
              'EMERGENCE', '生命升维', '物理存在', '定理', '公理']:
        c = text.count(t)
        if c > 0:
            kws[t] = c
    return kws

# 余弦相似度
def cosine(v1, v2):
    common = set(v1) & set(v2)
    dot = sum(v1[k] * v2[k] for k in common)
    m1 = sum(v**2 for v in v1.values()) ** 0.5
    m2 = sum(v**2 for v in v2.values()) ** 0.5
    if m1 == 0 or m2 == 0:
        return 0
    return dot / (m1 * m2)

# 计算所有文档的关键词向量
vectors = [get_keywords(d['content']) for d in core_docs]

# 统计词频分布
print('\n📊 关键词分布（Top 15）:')
all_kws = defaultdict(int)
for v in vectors:
    for kw, count in v.items():
        all_kws[kw] += 1
for kw, count in sorted(all_kws.items(), key=lambda x: -x[1])[:15]:
    print(f'  {kw}: {count}篇 ({count/len(core_docs)*100:.0f}%)')

# 构建交叉引用
print('\n🔗 构建交叉引用网络...')
citation_count = 0
total_edges = 0

for i, doc_a in enumerate(core_docs):
    # 计算与所有其他文档的相似度
    sims = []
    for j in range(len(core_docs)):
        if i == j:
            continue
        sim = cosine(vectors[i], vectors[j])
        if sim > 0.01:
            sims.append((j, sim))
    
    # 排序并取Top3
    sims.sort(key=lambda x: x[1], reverse=True)
    top = sims[:3]
    
    if len(top) == 0:
        continue
    
    # 移除已存在的引用
    if 'BSD交叉引用' in doc_a['content']:
        # 替换现有引用
        content = re.sub(r'\n\n---\n> \*\*BSD交叉引用\*\*:.*$', '', doc_a['content'], flags=re.DOTALL)
        doc_a['content'] = content
    
    # 构建引用文本
    refs = []
    for j, score in top:
        doc_b = core_docs[j]
        refs.append(f'> [{doc_b["name"].replace(".md","")}](./{doc_b["section"]}/{doc_b["name"]}) (相似度:{score:.2f})')
    
    ref_text = '\n\n---\n> **BSD交叉引用**: ' + ' | '.join(refs) + '\n'
    
    # 添加引用
    new_content = doc_a['content'] + ref_text
    with open(doc_a['path'], 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    doc_a['content'] = new_content
    citation_count += 1
    total_edges += len(top)

print(f'  ✅ 为 {citation_count} 篇文档添加交叉引用')
print(f'  📊 总引用边数: {total_edges}')

# 计算网络密度
nodes_with_refs = citation_count
max_edges = nodes_with_refs * (len(core_docs) - 1)
density = total_edges / max_edges if max_edges > 0 else 0
print(f'  📊 网络密度: {density:.4f}')

# 计算平均相似度
avg_sim = sum(s for _, s in [(i, cosine(vectors[i], vectors[j])) for i in range(len(core_docs)) for j in range(i+1, len(core_docs))]) / (len(core_docs) * (len(core_docs) - 1) / 2) if len(core_docs) > 1 else 0
print(f'  📊 平均语义相似度: {avg_sim:.4f}')

# 保存统计
stats = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_docs': len(core_docs),
    'docs_with_refs': citation_count,
    'total_edges': total_edges,
    'network_density': round(density, 4),
    'avg_similarity': round(avg_sim, 4),
    'top_keywords': dict(sorted(all_kws.items(), key=lambda x: -x[1])[:10])
}

with open('citation_network_stats.json', 'w', encoding='utf-8') as f:
    json.dump(stats, f, ensure_ascii=False, indent=2)

print(f'\n📁 统计数据已保存: citation_network_stats.json')
print('\n🎉 交叉引用网络构建完成!')
