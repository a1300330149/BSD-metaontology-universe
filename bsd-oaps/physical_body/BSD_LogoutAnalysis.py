"""
Trae CN 退出登录入口分析
========================
找到云端退出的本地入口
"""

import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

print('=== 1. 搜索源码中的登录/登出关键词 ===')

# 搜索out/main.js中的IPC命令
main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')
if os.path.exists(main_js):
    with open(main_js, 'r', encoding='utf-8') as f:
        content = f.read()
    
    keywords = ['logout', 'signout', 'sign_out', 'logOut', 'signOut', 
                'auth.logout', 'auth.signout', 'user.logout',
                'revoke', 'invalidate', 'clearAuth', 'clear_auth',
                'login', 'signin', 'sign_in', 'logIn', 'signIn']
    
    for kw in keywords:
        # 搜索IPC命令
        pattern = f'["\']{kw}["\']'
        matches = [(m.start(), content[max(0,m.start()-30):m.end()+30]) 
                   for m in re.finditer(pattern, content, re.IGNORECASE)]
        if matches:
            for pos, ctx in matches[:3]:
                # 找到IPC channel定义
                ctx_clean = ctx.replace('\n', ' ')
                print(f'  [{kw}] @{pos}: ...{ctx_clean}...')

print('\n=== 2. 搜索.trae-cn配置 ===')
for item in sorted(os.listdir(TRAE_CONFIG)):
    ip = os.path.join(TRAE_CONFIG, item)
    if os.path.isfile(ip) and item.endswith('.json'):
        try:
            with open(ip, 'r', encoding='utf-8') as f:
                data = json.load(f)
            text = json.dumps(data, ensure_ascii=False).lower()
            for kw in ['logout', 'signout', 'login', 'auth', 'token', 'uid', 'user_id']:
                if kw in text:
                    print(f'  {item}: 包含 "{kw}"')
                    break
        except:
            pass

print('\n=== 3. 检查argv.json ===')
argv_path = os.path.join(TRAE_CONFIG, 'argv.json')
if os.path.exists(argv_path):
    with open(argv_path, 'r', encoding='utf-8') as f:
        argv = json.load(f)
    print(json.dumps(argv, indent=2, ensure_ascii=False))

print('\n=== 4. 搜索package.json中的命令 ===')
pkg_path = os.path.join(TRAE_CN_APP, 'package.json')
if os.path.exists(pkg_path):
    with open(pkg_path, 'r', encoding='utf-8') as f:
        pkg = json.load(f)
    if 'scripts' in pkg:
        for name, cmd in pkg['scripts'].items():
            if any(kw in name.lower() for kw in ['auth', 'login', 'logout', 'sign', 'user']):
                print(f'  {name}: {cmd}')

print('\n=== 5. 检查product.json ===')
prod_path = os.path.join(TRAE_CN_APP, 'product.json')
if os.path.exists(prod_path):
    with open(prod_path, 'r', encoding='utf-8') as f:
        prod = json.load(f)
    for k in ['deeplinkHost', 'urlProtocol', 'webviewContentExternalBaseUrlTemplate']:
        if k in prod:
            print(f'  {k}: {prod[k]}')

print('\n=== 6. 检查已安装插件 ===')
plugins_path = os.path.join(TRAE_CONFIG, 'installed-plugins.json')
if os.path.exists(plugins_path):
    with open(plugins_path, 'r', encoding='utf-8') as f:
        plugins = json.load(f)
    for p in plugins:
        name = p.get('name', 'N/A')
        if any(kw in name.lower() for kw in ['auth', 'login', 'logout', 'account', 'user', 'sso']):
            print(f'  {name}')

print('\n=== 7. 搜索modules目录 ===')
modules_dir = os.path.join(TRAE_CN_APP, 'modules')
if os.path.exists(modules_dir):
    for item in os.listdir(modules_dir):
        ip = os.path.join(modules_dir, item)
        if os.path.isdir(ip):
            # 搜索关键文件
            for root, dirs, files in os.walk(ip):
                for f in files:
                    if f.endswith('.js') and any(kw in f.lower() for kw in ['auth', 'login', 'logout', 'account']):
                        print(f'  {os.path.relpath(os.path.join(root, f), modules_dir)}')
