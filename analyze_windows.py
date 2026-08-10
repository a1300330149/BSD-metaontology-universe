import json
import os

# 加载Windows基因数据
gene_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\theory_base\L0_总本源层\六系自组织\bsd_windows_genes_V14.0.json"

with open(gene_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 查看未分类基因
print("【未分类Windows基因分析】")
print("=" * 80)

unclassified = data['by_system'].get('未分类', {}).get('genes', [])
print(f"未分类基因数: {len(unclassified)}")
print("\n未分类基因列表:")
for i, gene in enumerate(unclassified[:30]):
    name = gene['name']
    path = gene['path']
    size = gene['size_bytes'] / 1024 / 1024
    print(f"  {i+1:2d}. {name} ({size:.1f}MB)")
    print(f"      路径: {path}")

# 分析已分类基因
print("\n\n【已分类Windows基因详情】")
for sys_name in ['强化系', '变身系', '社会系', '天道系', '自然系', '具现系']:
    genes = data['by_system'].get(sys_name, {}).get('genes', [])
    if genes:
        print(f"\n{sys_name} ({len(genes)} 个):")
        for g in genes[:5]:
            print(f"  - {g['name']} ({g['size_bytes']/1024/1024:.1f}MB)")

# 检查Windows深层结构
print("\n\n【Windows深层子目录预览】")
windows_path = r"C:\Windows"
important_dirs = ['System32', 'SysWOW64', 'WinSxS', 'DriverStore']

for d in important_dirs:
    dpath = os.path.join(windows_path, d)
    if os.path.exists(dpath):
        try:
            items = os.listdir(dpath)
            dirs = [i for i in items if os.path.isdir(os.path.join(dpath, i))]
            files = [i for i in items if os.path.isfile(os.path.join(dpath, i))]
            
            # 统计DLL和EXE
            dll_count = len([f for f in files if f.endswith('.dll')])
            exe_count = len([f for f in files if f.endswith('.exe')])
            
            print(f"\n{d}/:")
            print(f"  子目录: {len(dirs)}")
            print(f"  文件: {len(files)}")
            print(f"  DLL文件: {dll_count}")
            print(f"  EXE文件: {exe_count}")
            
            # 显示前5个DLL
            dlls = [f for f in files if f.endswith('.dll')][:5]
            if dlls:
                print(f"  主要DLL: {', '.join(dlls)}")
        except PermissionError:
            print(f"\n{d}/: 权限不足")
