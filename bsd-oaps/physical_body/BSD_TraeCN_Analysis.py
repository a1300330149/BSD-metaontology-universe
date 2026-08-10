"""
Trae CN vs TRAE SOLO CN 对比分析
"""
import os, json

trae_cn_user = r'C:\Users\13003\AppData\Roaming\Trae CN'
trae_cn_local = r'C:\Users\13003\AppData\Local\Programs\Trae CN'
trae_solo_user = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'
trae_config = r'C:\Users\13003\.trae-cn'

print('=== 1. Trae CN 用户数据 ===')
if os.path.exists(trae_cn_user):
    items = os.listdir(trae_cn_user)
    print(f'  条目: {len(items)} 个')
    for item in sorted(items)[:25]:
        ip = os.path.join(trae_cn_user, item)
        if os.path.isfile(ip):
            print(f'    FILE: {item} ({os.path.getsize(ip):,} bytes)')
        else:
            total = 0
            for root, dirs, files in os.walk(ip):
                for f in files:
                    try:
                        total += os.path.getsize(os.path.join(root, f))
                    except:
                        pass
            print(f'    DIR:  {item}/ ({total/1024/1024:.1f} MB)')
else:
    print('  目录不存在')

print('\n=== 2. Trae CN Electron结构 ===')
resources = os.path.join(trae_cn_local, 'resources')
if os.path.exists(resources):
    for item in os.listdir(resources):
        ip = os.path.join(resources, item)
        if os.path.isfile(ip):
            print(f'  FILE: resources/{item} ({os.path.getsize(ip)/1024/1024:.1f} MB)')
        else:
            print(f'  DIR:  resources/{item}/')
    
    app_dir = os.path.join(resources, 'app')
    if os.path.exists(app_dir):
        pkg_path = os.path.join(app_dir, 'package.json')
        if os.path.exists(pkg_path):
            with open(pkg_path, 'r', encoding='utf-8') as f:
                p = json.load(f)
            print('\n  package.json:')
            print(f'    name: {p.get("name")}')
            print(f'    version: {p.get("version")}')
            print(f'    main: {p.get("main")}')
        
        prod_path = os.path.join(app_dir, 'product.json')
        if os.path.exists(prod_path):
            with open(prod_path, 'r', encoding='utf-8') as f:
                pr = json.load(f)
            print('\n  product.json 关键字段:')
            for k in ['applicationName', 'dataFolderName', 'packageType', 'providerCode', 
                     'nameShort', 'nameAlias', 'brandName', 'runMode', 'version',
                     'appVersion', 'provider', 'dataFolderName']:
                if k in pr:
                    print(f'    {k}: {pr[k]}')

print('\n=== 3. TRAE SOLO CN product.json ===')
solo_app = os.path.join(r'D:\TRAE SOLO CN', 'resources', 'app')
solo_prod = os.path.join(solo_app, 'product.json')
if os.path.exists(solo_prod):
    with open(solo_prod, 'r', encoding='utf-8') as f:
        sp = json.load(f)
    for k in ['applicationName', 'dataFolderName', 'packageType', 'providerCode',
             'nameShort', 'brandName', 'runMode', 'version', 'appVersion', 'provider']:
        if k in sp:
            print(f'    {k}: {sp[k]}')

print('\n=== 4. .trae-cn 配置 ===')
if os.path.exists(trae_config):
    for item in sorted(os.listdir(trae_config)):
        ip = os.path.join(trae_config, item)
        if os.path.isfile(ip):
            print(f'  FILE: {item} ({os.path.getsize(ip):,} bytes)')

print('\n=== 5. 账号互通分析 ===')
# 检查Trae CN的Local State
trae_ls = os.path.join(trae_cn_user, 'Local State')
solo_ls = os.path.join(trae_solo_user, 'Local State')

for label, path in [('Trae CN', trae_ls), ('TRAE SOLO CN', solo_ls)]:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            ls = json.load(f)
        
        def find_key(obj, target, path=''):
            results = []
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if target.lower() in k.lower():
                        results.append((path + '.' + k, str(v)[:100]))
                    results.extend(find_key(v, target, path + '.' + k))
            return results
        
        for target in ['uid', 'user', 'account', '3753060170739075', 'token', 'session']:
            found = find_key(ls, target)
            if found:
                for p, v in found[:3]:
                    print(f'  {label} {target}: {p} = {v}')
