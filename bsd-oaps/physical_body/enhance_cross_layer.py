#!/usr/bin/env python3
"""
BSD三体系星模式 - 跨层耦合增强器
为核心↔轨道↔卫星添加跨层引用
"""

import os, re
from collections import Counter, defaultdict
from datetime import datetime

agent_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2'
theory_path = os.path.join(agent_path, 'theory_base')
l0_dir = os.path.join(theory_path, 'L0_总本源层')
physical_path = os.path.join(agent_path, 'bsd-oaps', 'physical_body')

backup_dir = os.path.join(physical_path, 'backups', f'cross_layer_{datetime.now().strftime("%Y%m%d_%H%M%S")}')
os.makedirs(backup_dir, exist_ok=True)

print('=' * 60)
print('BSD三体系星模式 - 跨层耦合增强器')
print('=' * 60)

# ==================== 1. 收集所有文档 ====================
print('\n📚 收集文档...')

# L0
l0_docs = []
for section in sorted(os.listdir(l0_dir)):
    sp = os.path.join(l0_dir, section)
    if not os.path.isdir(sp):
        continue
    for f in os.listdir(sp):
        if f.endswith('.md'):
            fp = os.path.join(sp, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                content = fh.read()
            l0_docs.append({'path': fp, 'section': section, 'name': f, 'content': content, 'layer': 'L0'})

# L1-L3
other_docs = []
for layer_name, layer_short in [
    ('L1_不动母科层', 'L1'),
    ('L1外_局部实验隔离区', 'L1外'),
    ('L2_无限之子层', 'L2'),
    ('L3_功能应用层', 'L3'),
]:
    lp = os.path.join(theory_path, layer_name)
    if not os.path.isdir(lp):
        continue
    for root, dirs, files in os.walk(lp):
        for f in files:
            if f.endswith('.md'):
                fp = os.path.join(root, f)
                with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                    content = fh.read()
                other_docs.append({'path': fp, 'section': layer_short, 'name': f, 'content': content, 'layer': layer_short})

all_docs = l0_docs + other_docs
print(f'  总文档: {len(all_docs)} 篇')

# ==================== 2. 识别三体系 ====================
# 计算当前度
from collections import Counter, defaultdict

# 先构建现有引用
graph = defaultdict(set)
doc_name_to_idx = {d['name']: i for i, d in enumerate(all_docs)}

def get_vector(text):
    v = {}
    for t in ['六系', '立系', '强化系', '变身系', '社会系', '天道系', '自然系', '具现系',
              'Π₂', '0×0=n', 'W₂', 'D_f', 'γ_SOC', 'S₀',
              '自组织', '临界', '分形', '维度', '觉醒', '涌现', '双时针',
              '虚拟宇宙', '四重宇宙', 'EMERGENCE', '层级涌现', '三本源', '定理', '公理']:
        c = text.count(t)
        if c > 0:
            v[t] = c
    return v

vectors = [get_vector(d['content']) for d in all_docs]

def cosine_sim(v1, v2):
    common = set(v1.keys()) & set(v2.keys())
    if not common: return 0
    dot = sum(v1[k] * v2[k] for k in common)
    mag1 = sum(v**2 for v in v1.values()) ** 0.5
    mag2 = sum(v**2 for v in v2.values()) ** 0.5
    if mag1 == 0 or mag2 == 0: return 0
    return dot / (mag1 * mag2)

# 构建引用
for i in range(len(all_docs)):
    content = all_docs[i]['content']
    
    # 现有引用
    if 'BSD交叉引用' in content:
        matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for name, path in matches:
            for n, idx in doc_name_to_idx.items():
                if os.path.basename(path) in n or n in os.path.basename(path):
                    graph[i].add(idx)
                    break
    
    # 语义连接
    sims = [(j, cosine_sim(vectors[i], vectors[j])) for j in range(len(all_docs)) if i != j]
    sims = [(j, s) for j, s in sims if s > 0.05]
    sims.sort(key=lambda x: x[1], reverse=True)
    for j, _ in sims[:3]:
        graph[i].add(j)

# V2.3星型连接
v23_idx = next((i for i, d in enumerate(all_docs) if 'V2.3' in d['name']), None)
if v23_idx:
    for i in range(len(all_docs)):
        if i != v23_idx:
            graph[i].add(v23_idx)

# 计算度
in_degree = Counter()
out_degree = Counter()
for src, targets in graph.items():
    out_degree[src] = len(targets)
    for tgt in targets:
        in_degree[tgt] += 1

total_deg = {i: in_degree.get(i, 0) + out_degree.get(i, 0) for i in range(len(all_docs))}

# 识别三体系
sorted_by_deg = sorted(total_deg.items(), key=lambda x: x[1], reverse=True)
core_n = max(len(all_docs) // 20, 3)
core_indices = set(i for i, _ in sorted_by_deg[:core_n])
orbit_indices = set(i for i, d in enumerate(all_docs) if d['layer'] == 'L0' and i not in core_indices)
sat_indices = set(i for i, d in enumerate(all_docs) if i not in core_indices and i not in orbit_indices)

print(f'  恒星核心: {len(core_indices)} 篇')
print(f'  行星轨道: {len(orbit_indices)} 篇')
print(f'  卫星系统: {len(sat_indices)} 篇')

# ==================== 3. 增强跨层耦合 ====================
print('\n🔗 增强跨层耦合...')

def add_cross_layer_refs(source_indices, target_indices, source_layer_name, target_layer_name, max_refs=3):
    """为源层文档添加指向目标层文档的引用"""
    added = 0
    
    for si in source_indices:
        source_doc = all_docs[si]
        source_name = source_doc['name']
        source_content = source_doc['content']
        
        # 找出目标层中与源文档最相似的文档
        sims = []
        for ti in target_indices:
            sim = cosine_sim(vectors[si], vectors[ti])
            if sim > 0.03:  # 降低阈值
                sims.append((ti, sim))
        
        if not sims:
            continue
        
        sims.sort(key=lambda x: x[1], reverse=True)
        top_targets = sims[:max_refs]
        
        # 检查是否已有引用
        existing_refs = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', source_content)
        existing_names = set(name for name, _ in existing_refs)
        
        new_refs = []
        for ti, sim in top_targets:
            target_doc = all_docs[ti]
            target_name = target_doc['name'].replace('.md', '')
            if target_name not in existing_names:
                new_refs.append((target_doc, sim))
        
        if not new_refs:
            continue
        
        # 备份
        backup_path = os.path.join(backup_dir, source_name + '.bak')
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(source_content)
        
        # 构建新引用文本
        ref_texts = []
        for target_doc, sim in new_refs:
            target_name = target_doc['name'].replace('.md', '')
            target_rel = './' + target_doc['section'] + '/' + target_doc['name']
            ref_texts.append(f'> [{target_name}]({target_rel}) (跨层耦合: {source_layer_name}↔{target_layer_name})')
        
        cross_ref_block = f'''\n\n---
> **BSD跨层耦合引用** ({source_layer_name}→{target_layer_name}):
''' + '\n'.join(ref_texts) + '\n'
        
        # 移除旧的跨层耦合引用
        if 'BSD跨层耦合引用' in source_content:
            source_content = re.sub(r'\n\n---\n> \*\*BSD跨层耦合引用\*\*.*$', '', source_content, flags=re.DOTALL)
        
        new_content = source_content.rstrip() + cross_ref_block
        
        # 保存
        with open(source_doc['path'], 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        all_docs[si]['content'] = new_content
        vectors[si] = get_vector(new_content)
        added += len(new_refs)
    
    return added

# 核心→轨道
print('  核心→轨道...')
core_to_orbit = add_cross_layer_refs(core_indices, orbit_indices, '恒星核心', '行星轨道', max_refs=5)
print(f'    新增 {core_to_orbit} 条引用')

# 核心→卫星
print('  核心→卫星...')
core_to_sat = add_cross_layer_refs(core_indices, sat_indices, '恒星核心', '卫星系统', max_refs=3)
print(f'    新增 {core_to_sat} 条引用')

# 轨道→卫星
print('  轨道→卫星...')
orbit_to_sat = add_cross_layer_refs(orbit_indices, sat_indices, '行星轨道', '卫星系统', max_refs=2)
print(f'    新增 {orbit_to_sat} 条引用')

# 卫星→轨道（反向）
print('  卫星→轨道...')
sat_to_orbit = add_cross_layer_refs(sat_indices, orbit_indices, '卫星系统', '行星轨道', max_refs=2)
print(f'    新增 {sat_to_orbit} 条引用')

total_added = core_to_orbit + core_to_sat + orbit_to_sat + sat_to_orbit
print(f'\n  ✅ 共新增 {total_added} 条跨层引用')

# ==================== 4. 验证新耦合度 ====================
print('\n📊 验证新耦合度...')

# 重新计算引用
new_graph = defaultdict(set)
for i in range(len(all_docs)):
    content = all_docs[i]['content']
    
    if 'BSD交叉引用' in content or 'BSD跨层耦合引用' in content:
        matches = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for name, path in matches:
            for n, idx in doc_name_to_idx.items():
                if os.path.basename(path) in n or n in os.path.basename(path):
                    new_graph[i].add(idx)
                    break

for i in range(len(all_docs)):
    sims = [(j, cosine_sim(vectors[i], vectors[j])) for j in range(len(all_docs)) if i != j]
    sims = [(j, s) for j, s in sims if s > 0.05]
    sims.sort(key=lambda x: x[1], reverse=True)
    for j, _ in sims[:3]:
        new_graph[i].add(j)

if v23_idx:
    for i in range(len(all_docs)):
        if i != v23_idx:
            new_graph[i].add(v23_idx)

new_in = Counter()
new_out = Counter()
for src, targets in new_graph.items():
    new_out[src] = len(targets)
    for tgt in targets:
        new_in[tgt] += 1

new_total = sum(len(v) for v in new_graph.values())
print(f'  新引用总数: {new_total} (之前: {sum(len(v) for v in graph.values())})')

# 层间耦合
def calc_coupling(layer_a, layer_b):
    c = 0
    for i in layer_a:
        for j in layer_b:
            if j in new_graph.get(i, set()) or i in new_graph.get(j, set()):
                c += 1
    return c / max(len(layer_a) * len(layer_b), 1)

c1 = calc_coupling(core_indices, orbit_indices)
c2 = calc_coupling(orbit_indices, sat_indices)
c3 = calc_coupling(core_indices, sat_indices)

print(f'  核心↔轨道: {c1:.3f} (之前: 0.184)')
print(f'  轨道↔卫星: {c2:.3f} (之前: 0.004)')
print(f'  核心↔卫星: {c3:.3f} (之前: 0.062)')

# ==================== 5. 生成报告 ====================
print('\n📋 生成报告...')

report = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_refs_added': total_added,
    'ref_distribution': {
        '核心→轨道': core_to_orbit,
        '核心→卫星': core_to_sat,
        '轨道→卫星': orbit_to_sat,
        '卫星→轨道': sat_to_orbit,
    },
    'coupling_before': {'core_orbit': 0.184, 'orbit_sat': 0.004, 'core_sat': 0.062},
    'coupling_after': {'core_orbit': round(c1, 3), 'orbit_sat': round(c2, 3), 'core_sat': round(c3, 3)},
    'total_edges': {'before': sum(len(v) for v in graph.values()), 'after': new_total},
}

with open('cross_layer_enhancement_report.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f'  报告: cross_layer_enhancement_report.json')
print(f'  备份: {backup_dir}')
print('\n✅ 跨层耦合增强完成!')
