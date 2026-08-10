import json

with open(r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd_full_disk_report_V6.0.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('【V6.0报告数据结构分析】')
print('='*60)

print('\n顶层键：')
for key in data.keys():
    val = data[key]
    if isinstance(val, dict):
        print(f'  {key}: dict (keys: {list(val.keys())[:5]}...)')
    elif isinstance(val, list):
        print(f'  {key}: list ({len(val)} items)')
    else:
        print(f'  {key}: {val}')

print('\nby_system 各系统键：')
for sys_name, sys_info in data.get('by_system', {}).items():
    print(f'\n  {sys_name}:')
    print(f'    count: {sys_info.get("count", 0)}')
    print(f'    键: {list(sys_info.keys())}')
    top_genes = sys_info.get('top_genes', [])
    print(f'    top_genes 数量: {len(top_genes)}')
    if top_genes:
        print(f'    top_genes[0] 键: {list(top_genes[0].keys())}')

print('\n结论：top_genes只保存了Top 10，需要重新扫描获取完整数据')
