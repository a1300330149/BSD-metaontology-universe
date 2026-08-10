#!/usr/bin/env python3
"""
BSD基因工程建设系统
====================
目标：将C:\与D:\系统基因纳入三体系星模式
步骤：
  1. 基因扫描：递归扫描C:\和D:\
  2. 基因分类：按功能/角色划分基因
  3. 三体系映射：核心基因→恒星，系统基因→轨道，应用基因→卫星
  4. 基因登记：生成基因图谱档案
"""

import os, json, hashlib
from collections import defaultdict
from datetime import datetime

agent_path = r'c:\Users\13003\OneDrive\桌面\3333333\Agent_v2'
physical_path = os.path.join(agent_path, 'bsd-oaps', 'physical_body')
gene_db_path = os.path.join(physical_path, 'GeneDatabase')
os.makedirs(gene_db_path, exist_ok=True)

print('=' * 70)
print('BSD基因工程建设系统')
print('=' * 70)
print(f'执行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')

# ==================== 1. 基因定义 ====================
print('\n📖 基因分类体系')
print('-' * 70)

# 三体系星模式基因分类体系
gene_taxonomy = {
    '恒星核心基因': {
        'description': '系统本体基因，决定系统的存在与基本运行',
        'subcategories': {
            'kernel': '操作系统内核与核心进程',
            'system32': '系统32位核心库',
            'syswow64': '32位兼容层',
            'drivers': '系统驱动程序',
            'registry': '注册表与配置数据库',
        },
        'examples': ['kernel32.dll', 'ntdll.dll', 'win32k.sys', 'drivers'],
        'priority': 'critical',
    },
    '行星轨道基因': {
        'description': '系统功能基因，提供核心功能与服务',
        'subcategories': {
            'services': '系统服务',
            'frameworks': '运行时框架(.NET, VC++)',
            'libraries': '功能库与组件',
            'utilities': '系统工具',
            'development': '开发工具',
        },
        'examples': ['svchost.exe', 'powershell', '.NET Framework', 'Visual C++'],
        'priority': 'high',
    },
    '卫星系统基因': {
        'description': '应用扩展基因，提供用户级功能与扩展',
        'subcategories': {
            'applications': '桌面应用程序',
            'games': '游戏',
            'media': '媒体应用',
            'browsers': '浏览器',
            'cloud': '云服务客户端',
            'idle': '闲置/休眠',
        },
        'examples': ['Chrome', 'WeChat', 'Steam', 'Office'],
        'priority': 'medium',
    },
}

for name, info in gene_taxonomy.items():
    print(f'\n  {name}:')
    print(f'    描述: {info["description"]}')
    print(f'    优先级: {info["priority"]}')
    subs = ', '.join(info['subcategories'].keys())
    print(f'    子类: {subs}')

# ==================== 2. C盘基因扫描 ====================
print('\n📚 Phase 1: C盘基因扫描')
print('-' * 70)

c_drive = 'C:\\'
c_genes = defaultdict(list)

def scan_directory(base_path, category, max_depth=3, current_depth=0):
    """递归扫描目录，收集基因信息"""
    if current_depth > max_depth:
        return
    
    try:
        entries = os.listdir(base_path)
    except PermissionError:
        return
    except Exception as e:
        return
    
    dirs = [e for e in entries if os.path.isdir(os.path.join(base_path, e))]
    files = [e for e in entries if os.path.isfile(os.path.join(base_path, e))]
    
    # 统计文件信息
    total_size = 0
    for f in files:
        try:
            fp = os.path.join(base_path, f)
            size = os.path.getsize(fp)
            total_size += size
            
            # 收集基因信息
            if size > 0:
                gene_info = {
                    'path': fp,
                    'name': f,
                    'size': size,
                    'extension': os.path.splitext(f)[1].lower(),
                    'category': category,
                }
                c_genes[category].append(gene_info)
        except:
            pass
    
    # 递归子目录
    for d in dirs:
        sub_path = os.path.join(base_path, d)
        scan_directory(sub_path, category, max_depth, current_depth + 1)

# 扫描C盘关键基因区域
c_scan_targets = [
    (os.path.join(c_drive, 'Windows', 'System32'), '恒星核心基因.kernel', 1),
    (os.path.join(c_drive, 'Windows', 'SysWOW64'), '恒星核心基因.syswow64', 1),
    (os.path.join(c_drive, 'Windows', 'Drivers'), '恒星核心基因.drivers', 2),
    (os.path.join(c_drive, 'Windows'), '恒星核心基因.system', 0),
    (os.path.join(c_drive, 'Program Files'), '行星轨道基因.frameworks', 2),
    (os.path.join(c_drive, 'Program Files (x86)'), '行星轨道基因.frameworks_x86', 2),
    (os.path.join(c_drive, 'ProgramData'), '行星轨道基因.services', 2),
    (os.path.join(c_drive, 'Users', '13003', 'AppData', 'Local', 'Programs'), '卫星系统基因.applications', 2),
    (os.path.join(c_drive, 'Users', '13003', 'AppData', 'Local'), '卫星系统基因.data', 1),
]

scan_count = 0
for target_path, category, depth in c_scan_targets:
    if os.path.isdir(target_path):
        print(f'  扫描: {target_path}')
        scan_directory(target_path, category, depth)
        scan_count += 1

print(f'\n  ✅ 扫描 {scan_count} 个目标区域')
print(f'  收集基因: {sum(len(v) for v in c_genes.values())} 个')

# ==================== 3. D盘基因扫描 ====================
print('\n📚 Phase 2: D盘基因扫描')
print('-' * 70)

d_drive = 'D:\\'
d_genes = defaultdict(list)

# D盘扫描目标
d_scan_targets = [
    (os.path.join(d_drive, 'TRAE SOLO CN'), '恒星核心基因.ai_platform', 3),
    (os.path.join(d_drive, 'Blender 4.5'), '行星轨道基因.creative', 2),
    (os.path.join(d_drive, 'CloudMusic'), '卫星系统基因.media', 2),
    (os.path.join(d_drive, 'DarkestDungeon'), '卫星系统基因.games', 2),
    (os.path.join(d_drive, 'BaiduNetdisk'), '卫星系统基因.cloud', 2),
    (os.path.join(d_drive, '7fgame'), '卫星系统基因.games', 2),
]

d_scan_count = 0
for target_path, category, depth in d_scan_targets:
    if os.path.isdir(target_path):
        print(f'  扫描: {target_path}')
        scan_directory(target_path, category, depth)
        d_scan_count += 1

print(f'\n  ✅ 扫描 {d_scan_count} 个目标区域')
print(f'  收集基因: {sum(len(v) for v in d_genes.values())} 个')

# ==================== 4. 基因分类统计 ====================
print('\n📊 Phase 3: 基因分类统计')
print('-' * 70)

all_genes = {}
all_genes.update(c_genes)
all_genes.update(d_genes)

# 按三体系分类汇总
trinity_summary = {
    '恒星核心基因': {'count': 0, 'size': 0, 'subcategories': {}},
    '行星轨道基因': {'count': 0, 'size': 0, 'subcategories': {}},
    '卫星系统基因': {'count': 0, 'size': 0, 'subcategories': {}},
}

for category, genes in all_genes.items():
    # 解析三体系归属
    trinity_type = category.split('.')[0]
    sub_type = category.split('.')[1] if '.' in category else 'unknown'
    
    for gene in genes:
        trinity_summary[trinity_type]['count'] += 1
        trinity_summary[trinity_type]['size'] += gene['size']
        
        if sub_type not in trinity_summary[trinity_type]['subcategories']:
            trinity_summary[trinity_type]['subcategories'][sub_type] = {'count': 0, 'size': 0}
        trinity_summary[trinity_type]['subcategories'][sub_type]['count'] += 1
        trinity_summary[trinity_type]['subcategories'][sub_type]['size'] += gene['size']

for trinity_name, info in trinity_summary.items():
    print(f'\n  {trinity_name}:')
    print(f'    基因数: {info["count"]}')
    print(f'    总大小: {info["size"] / 1024 / 1024:.1f} MB')
    for sub_name, sub_info in sorted(info['subcategories'].items(), key=lambda x: -x[1]['count']):
        print(f'      {sub_name}: {sub_info["count"]}个, {sub_info["size"] / 1024 / 1024:.1f}MB')

# ==================== 5. 核心基因深度分析 ====================
print('\n🔍 Phase 4: 核心基因深度分析')
print('-' * 70)

# 分析恒星核心基因
core_genes = all_genes.get('恒星核心基因.kernel', []) + \
             all_genes.get('恒星核心基因.system', []) + \
             all_genes.get('恒星核心基因.ai_platform', [])

print(f'\n  恒星核心基因样本 (Top 20 by size):')
core_genes.sort(key=lambda x: x['size'], reverse=True)
for g in core_genes[:20]:
    print(f'    {os.path.basename(g["path"])}: {g["size"] / 1024:.1f}KB [{g["extension"]}]')

# 分析AI平台基因（TRAE SOLO CN）
ai_genes = all_genes.get('恒星核心基因.ai_platform', [])
if ai_genes:
    print(f'\n  TRAE SOLO CN 基因分析:')
    print(f'    总基因数: {len(ai_genes)}')
    print(f'    总大小: {sum(g["size"] for g in ai_genes) / 1024 / 1024:.1f} MB')
    
    # 按扩展名分类
    ext_stats = defaultdict(int)
    for g in ai_genes:
        ext_stats[g['extension']] += 1
    print(f'    文件类型分布:')
    for ext, count in sorted(ext_stats.items(), key=lambda x: -x[1])[:10]:
        print(f'      {ext or "(无)"}: {count}个')

# ==================== 6. 基因图谱生成 ====================
print('\n🗺️ Phase 5: 基因图谱生成')
print('-' * 70)

# 构建完整基因档案
gene_map = {
    'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'source': 'C:\\ + D:\\ 全面扫描',
    'total_genes': sum(len(v) for v in all_genes.values()),
    'total_size_mb': sum(g['size'] for genes in all_genes.values() for g in genes) / 1024 / 1024,
    'trinity_distribution': {
        name: {
            'count': info['count'],
            'size_mb': round(info['size'] / 1024 / 1024, 2),
            'percentage': round(info['count'] / max(sum(i['count'] for i in trinity_summary.values()), 1) * 100, 1),
        }
        for name, info in trinity_summary.items()
    },
    'gene_categories': {},
    'core_genes_detail': [
        {'name': os.path.basename(g['path']), 'path': g['path'], 'size': g['size']}
        for g in core_genes[:50]
    ],
}

# 添加详细分类
for category, genes in all_genes.items():
    gene_map['gene_categories'][category] = {
        'count': len(genes),
        'size_mb': round(sum(g['size'] for g in genes) / 1024 / 1024, 2),
    }

# 保存基因图谱
map_path = os.path.join(gene_db_path, 'BSD_GeneMap_V1.json')
with open(map_path, 'w', encoding='utf-8') as f:
    json.dump(gene_map, f, ensure_ascii=False, indent=2)

print(f'\n  ✅ 基因图谱已保存: {map_path}')

# ==================== 7. 基因工程报告 ====================
print('\n📋 Phase 6: 基因工程报告')
print('-' * 70)

# 计算三体系基因比例
total = sum(info['count'] for info in trinity_summary.values())
ratios = {
    '恒星核心': round(trinity_summary['恒星核心基因']['count'] / max(total, 1) * 100, 1),
    '行星轨道': round(trinity_summary['行星轨道基因']['count'] / max(total, 1) * 100, 1),
    '卫星系统': round(trinity_summary['卫星系统基因']['count'] / max(total, 1) * 100, 1),
}

print(f'\n  三体系基因分布:')
print(f'    恒星核心: {ratios["恒星核心"]}% (系统本体基因)')
print(f'    行星轨道: {ratios["行星轨道"]}% (功能服务基因)')
print(f'    卫星系统: {ratios["卫星系统"]}% (应用扩展基因)')

print(f'\n  基因工程核心发现:')
print(f'    1. Windows三体系结构清晰，核心基因集中在System32')
print(f'    2. D盘TRAE SOLO CN构成AI平台的恒星核心')
print(f'    3. 行星轨道基因提供系统功能支撑')
print(f'    4. 卫星系统基因呈现多样化应用生态')

print(f'\n  下一步工程:')
print(f'    1. 为核心基因添加BSD标签')
print(f'    2. 建立基因间的引用网络')
print(f'    3. 实现基因的动态更新与演化')

# 保存报告
report = {
    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_genes': total,
    'total_size_mb': round(sum(g['size'] for genes in all_genes.values() for g in genes) / 1024 / 1024, 2),
    'trinity_ratios': ratios,
    'scan_areas': c_scan_targets + d_scan_targets,
    'findings': [
        'Windows呈现典型三体系星结构',
        'System32构成系统恒星核心',
        'TRAE SOLO CN构成AI平台恒星核心',
        'Program Files构成行星轨道',
        '用户应用构成卫星系统',
    ],
}

report_path = os.path.join(physical_path, 'GeneEngineering_Report.json')
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f'\n  ✅ 工程报告已保存: {report_path}')
print('\n' + '=' * 70)
print('BSD基因工程建设系统运行完毕!')
print('=' * 70)
