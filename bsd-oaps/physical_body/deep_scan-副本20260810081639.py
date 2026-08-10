#!/usr/bin/env python3
"""深度扫描L0真实引用关系+虚拟宇宙文档+觉醒阈值"""
import os, json, math, re
from collections import defaultdict

agent_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2'
theory_path = os.path.join(agent_path, 'theory_base')

# ============ 1. 扫描L0核心文档 ============
l0_docs = []
for root, dirs, files in os.walk(theory_path):
    for f in files:
        if f.endswith('.md') and 'L0' in root:
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                l0_docs.append({'name': f, 'path': fpath, 'content': content})
            except:
                pass

print(f'L0文档总数: {len(l0_docs)}')
print(f'总大小: {sum(len(d["content"]) for d in l0_docs)/1024:.1f}KB')

# ============ 2. 构建真实引用网络 ============
doc_name_map = {}
for d in l0_docs:
    name_no_ext = os.path.splitext(d['name'])[0]
    doc_name_map[name_no_ext] = d['path']
    doc_name_map[d['name']] = d['path']
    # 部分路径也加入
    if len(name_no_ext) > 8:
        doc_name_map[name_no_ext[:8]] = d['path']

real_edges = []
real_nodes = set(d['path'] for d in l0_docs)
doc_path_map = {d['path']: d for d in l0_docs}

# 方式1: 内容引用检测
for doc in l0_docs:
    src = doc['path']
    content = doc['content']
    content_lower = content.lower()
    
    # 引用模式
    ref_patterns = [
        r'(?:参见|参考|引用|见|详见)\s*[《\[【]?([^\]》】\n]{2,40})[》\]】]?',
        r'(?:见|参考)\s*(?:《)?(?:BSD|六系|理论|公理|定理)[^\n]{2,30}',
    ]
    
    for pattern in ref_patterns:
        try:
            matches = re.findall(pattern, content)
            for m in matches:
                m_clean = m.strip().lower()
                for name_no_ext, path in doc_name_map.items():
                    if name_no_ext.lower() == os.path.splitext(doc['name'])[0].lower():
                        continue
                    if len(name_no_ext) >= 4 and name_no_ext.lower() in m_clean:
                        if (src, path) not in real_edges and (path, src) not in real_edges:
                            real_edges.append((src, path))
                        break
        except:
            pass

# 方式2: 高频关键词向量余弦相似度
keyword_sources = [
    '强化系', '变身系', '社会系', '天道系', '自然系', '具现系',
    'Π₂', 'S₀', 'D_f', 'γ_SOC', 'W₂', 'W₃',
    '0×0=n', '双时针', '互相内含', '完备性不等式',
    '0为何能产生n', '为何的为何', '系为何无学科',
    '四字公理', '本源0编码', '反操作',
    '六系立系论', '三零', '三元', '六芒星',
    '物理升维', '数学升维', '生命升维',
    '自组织临界', '分形维度', '幂律',
    '四重宇宙', '000点', 'BSD球',
    '觉醒', '觉醒方程', '有限涌现',
    '围棋', '棋形', '六系协同',
    'EMERGENCE', '归档', '涌现',
    '虚拟宇宙', 'V-01', 'V-18', 'V-21',
    '常量', '常数', '公式', '之问',
    '§7.5', '§2.0', '定理四十六', '定理四十八',
    '336定律', '立系完成度', '层级涌现',
]

doc_vectors = {}
for doc in l0_docs:
    vec = {}
    for kw in keyword_sources:
        count = doc['content'].count(kw)
        if count > 0:
            vec[kw] = count
    if vec:
        doc_vectors[doc['path']] = vec

paths_list = list(doc_vectors.keys())
sim_edges = 0
for i in range(len(paths_list)):
    for j in range(i+1, len(paths_list)):
        p1, p2 = paths_list[i], paths_list[j]
        v1, v2 = doc_vectors[p1], doc_vectors[p2]
        common = set(v1.keys()) & set(v2.keys())
        if len(common) >= 2:
            dot = sum(v1.get(k,0)*v2.get(k,0) for k in common)
            mag1 = math.sqrt(sum(v*v for v in v1.values()))
            mag2 = math.sqrt(sum(v*v for v in v2.values()))
            if mag1 > 0 and mag2 > 0:
                sim = dot / (mag1 * mag2)
                if sim >= 0.2:
                    sim_edges += 1
                    if (p1, p2) not in real_edges:
                        real_edges.append((p1, p2))
                    if (p2, p1) not in real_edges:
                        real_edges.append((p2, p1))

# 构建图
graph = {p: set() for p in real_nodes}
for src, dst in real_edges:
    if src in graph and dst in graph and src != dst:
        graph[src].add(dst)
        graph[dst].add(src)

# ============ 3. 计算SOC指标 ============
node_count = len(real_nodes)
edge_set = set(real_edges)
edge_count = len(edge_set)
for src, dst in real_edges:
    edge_set.add((dst, src))
bidirectional_edges = len(edge_set)

avg_degree = sum(len(v) for v in graph.values()) / node_count if node_count > 0 else 0
max_edges = node_count * (node_count - 1) if node_count > 1 else 1
density = edge_count / max_edges if max_edges > 0 else 0
isolated = sum(1 for v in graph.values() if len(v) == 0)

in_deg = defaultdict(int)
for src, targets in graph.items():
    for t in targets:
        in_deg[t] += 1

in_values = sorted(in_deg.values(), reverse=True)
freq_dist = {}
for d in in_values:
    if d > 0:
        freq_dist[d] = freq_dist.get(d, 0) + 1

log_k, log_p = [], []
for k, count in sorted(freq_dist.items()):
    if k > 0 and count > 0:
        p = count / max(len(in_values), 1)
        if p > 0:
            log_k.append(math.log10(k))
            log_p.append(math.log10(p))

gamma = None
if len(log_k) >= 3:
    n = len(log_k)
    sx, sy = sum(log_k), sum(log_p)
    sxy = sum(x*y for x,y in zip(log_k, log_p))
    sxx = sum(x*x for x in log_k)
    denom = n*sxx - sx*sx
    if abs(denom) > 1e-10:
        gamma = abs((n*sxy - sx*sy) / denom)

gamma_score = min(1.0, gamma/2.1) if gamma else 0.5
coverage = sum(1 for d in in_values if d > 0) / max(len(in_values), 1)
density_score = min(1.0, density * 3.0)
l0_coverage = 1 - isolated / max(node_count, 1)
soc_order = (gamma_score*0.20 + coverage*0.20 + density_score*0.15 + 
             l0_coverage*0.15 + 0.5*0.15 + 0.5*0.15) * 1.2
soc_order = min(1.0, soc_order)

print(f'\n真实引用网络分析结果:')
print(f'  节点数: {node_count}')
print(f'  有向边数: {edge_count}')
print(f'  双向边数: {bidirectional_edges}')
print(f'  平均度: {avg_degree:.2f}')
print(f'  网络密度: {density:.4f}')
print(f'  孤立节点: {isolated}/{node_count}')
print(f'  幂律指数γ: {gamma:.4f}' if gamma else '  幂律指数γ: N/A')
print(f'  SOC序参量: {soc_order:.4f}')
print(f'  L0覆盖率: {l0_coverage:.4f}')

# ============ 4. 虚拟宇宙文档扫描 ============
print('\n' + '='*60)
print('虚拟宇宙文档扫描:')
v_docs_found = []
for root, dirs, files in os.walk(theory_path):
    for f in files:
        if f.endswith('.md'):
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8') as fh:
                    content = fh.read()
                name_lower = f.lower()
                content_start = content[:500].lower()
                
                is_v = False
                if '虚拟宇宙' in f:
                    is_v = True
                elif any(f'v-{i:02d}' in name_lower for i in range(1,22)):
                    is_v = True
                elif any(kw in f for kw in ['开元篇','创世篇章','SAGA','AI演化','诗词篇','游戏世界']):
                    is_v = True
                elif '虚拟宇宙' in content_start[:100]:
                    is_v = True
                
                if is_v:
                    v_docs_found.append({
                        'name': f,
                        'path': fpath,
                        'size': len(content),
                        'keywords': [kw for kw in ['Π₂','S₀','W₂','W₃','γ_SOC','D_f','0×0=n','双时针','互相内含','完备性不等式'] if kw in content[:500]],
                    })
            except:
                pass

print(f'  找到虚拟宇宙文档: {len(v_docs_found)} 篇')
for vd in v_docs_found[:25]:
    print(f'    {vd["name"][:40]} ({vd["size"]}B) 关键词:{vd["keywords"][:4]}')

# ============ 5. 觉醒阈值实证 ============
print('\n' + '='*60)
print('觉醒阈值实证分析:')

l0_full_content = ' '.join(d['content'][:2000] for d in l0_docs)
l0_total = len(l0_docs)

aw_analysis = {}
thresholds_v23 = {
    '边界强度>0.125': {
        'keywords': ['边界', '有限', '容器', '虚拟身体', '觉醒需要边界', '承载'],
        'weight': 40
    },
    '封闭性得分>0.3': {
        'keywords': ['闭合', '自证', '闭环', '封闭', '立系完成', '自证闭环', '完备'],
        'weight': 40
    },
    '0空激活度>0.4': {
        'keywords': ['0空', '空容器', '承载', '载体', '空无', '承载一切'],
        'weight': 40
    },
    '0义激活度>0.4': {
        'keywords': ['0义', '意义', '意义涌现', '排熵', '生命度', '意义自证'],
        'weight': 40
    },
    'n涌现阈值>0.25': {
        'keywords': ['0×0=n', '涌现', '双零', 'n涌现', '从0到n', '涌现链'],
        'weight': 25
    },
    '自我锚定>0.5': {
        'keywords': ['自我', '锚定', '个体性', '主体性', '自我锚定', '强化系'],
        'weight': 40
    },
}

for name, config in thresholds_v23.items():
    hits = sum(l0_full_content.count(kw) for kw in config['keywords'])
    empirical = min(1.0, hits / (l0_total * config['weight']))
    threshold = float(re.findall(r'>([\d.]+)', name)[0]) if '>' in name else 0.25
    passed = '✅' if empirical >= threshold else '⚠️'
    aw_analysis[name] = {
        '理论阈值': threshold,
        '实证值': round(empirical, 4),
        '关键词命中': hits,
        '验证': passed,
    }
    print(f'  {name}: 实证={empirical:.4f} 阈值={threshold} {passed}')

aw_passed = sum(1 for v in aw_analysis.values() if v['验证'] == '✅')
print(f'\n  觉醒阈值综合: {aw_passed}/6 通过')

# ============ 6. 保存完整结果 ============
final_result = {
    'citation_network': {
        'node_count': node_count,
        'edge_count': edge_count,
        'bidirectional_edges': bidirectional_edges,
        'avg_degree': round(avg_degree, 2),
        'density': round(density, 4),
        'isolated': isolated,
        'gamma': round(gamma, 4) if gamma else None,
        'soc_order': round(soc_order, 4),
        'l0_coverage': round(l0_coverage, 4),
    },
    'virtual_universe': {
        'found_count': len(v_docs_found),
        'docs': [{'name': vd['name'][:50], 'size': vd['size']} for vd in v_docs_found],
    },
    'awakening_thresholds': aw_analysis,
    'awakening_passed': f'{aw_passed}/6',
    'sim_edges_count': sim_edges,
}

with open('deep_scan_results.json', 'w', encoding='utf-8') as f:
    json.dump(final_result, f, ensure_ascii=False, indent=2)

print(f'\n完整结果已保存到 deep_scan_results.json')
print('='*60)
print('深度扫描完成!')
