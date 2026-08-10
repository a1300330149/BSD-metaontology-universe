import json
import os

v10_path = r"C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd_full_gene_report_V10.0.json"

with open(v10_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 检查是否包含C:\Windows基因
print("【检查C:\\Windows基因覆盖情况】")
print("=" * 60)

has_windows = False
windows_genes = []

for sys_name, sys_info in data.get('by_system', {}).items():
    genes = sys_info.get('genes', [])
    for gene in genes:
        path = gene.get('path', '')
        if 'C:\\Windows' in path:
            has_windows = True
            windows_genes.append({
                'system': sys_name,
                'path': path[:80],
                'name': gene.get('name', '')
            })

if has_windows:
    print(f"✅ 已包含C:\\Windows基因: {len(windows_genes)} 个")
    for g in windows_genes[:10]:
        print(f"   [{g['system']}] {g['path']}")
else:
    print("❌ 未包含C:\\Windows基因！")
    print("   原因：扫描配置中主动跳过了C:\\Windows目录")
    print("   需要专门提取C:\\Windows的核心基因")

# 检查Windows目录结构
print("\n【C:\\Windows目录结构预览】")
windows_path = r"C:\Windows"
if os.path.exists(windows_path):
    try:
        items = os.listdir(windows_path)
        dirs = [i for i in items if os.path.isdir(os.path.join(windows_path, i))]
        files = [i for i in items if os.path.isfile(os.path.join(windows_path, i))]
        print(f"   子目录数: {len(dirs)}")
        print(f"   文件数: {len(files)}")
        print(f"\n   核心子目录（前20个）：")
        for d in sorted(dirs)[:20]:
            dpath = os.path.join(windows_path, d)
            try:
                size = sum(os.path.getsize(os.path.join(dpath, f)) for f in os.listdir(dpath) if os.path.isfile(os.path.join(dpath, f)))
                print(f"     {d}/ ({len(os.listdir(dpath))} items, {size/1024/1024:.1f}MB)")
            except:
                print(f"     {d}/")
    except PermissionError:
        print("   权限不足，无法完全列举")
else:
    print("   C:\\Windows 不存在！")
