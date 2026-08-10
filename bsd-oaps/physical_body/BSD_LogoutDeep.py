"""
Trae CN 退出登录入口深度分析
"""

import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

if not os.path.exists(main_js):
    print('main.js not found')
    exit()

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 搜索IPC事件发射器
print('=== 1. 搜索IPC事件 (login/logout相关) ===')

# 查找事件发射器模式
patterns = [
    ('out/login', 'out/login'),
    ('out/logout', 'out/logout'),
    ('out/signin', 'out/signin'),
    ('out/signout', 'out/signout'),
    ('out/auth', 'out/auth'),
    ('out/authentication', 'out/authentication'),
    ('out/account', 'out/account'),
    ('out/user', 'out/user'),
    ('out/identity', 'out/identity'),
    ('onDidChangeAuthentication', 'onDidChangeAuthentication'),
    ('onDidChangeUser', 'onDidChangeUser'),
    ('onAuthentication', 'onAuthentication'),
    ('out/chat', 'out/chat'),
    ('out/chat.completion', 'out/chat.completion'),
    ('out/ai', 'out/ai'),
    ('out/copilot', 'out/copilot'),
    ('out/chat.send', 'out/chat.send'),
    ('out/chat.message', 'out/chat.message'),
]

for pat, label in patterns:
    pattern = re.escape(pat)
    matches = [(m.start(), content[max(0,m.start()-20):m.end()+80]) 
               for m in re.finditer(pattern, content, re.IGNORECASE)]
    if matches:
        for pos, ctx in matches[:5]:
            ctx_clean = ctx.replace('\n', ' ').replace('\r', '')
            print(f'  [{label}] @{pos}: {ctx_clean[:120]}')

# 2. 搜索菜单相关
print('\n=== 2. 搜索菜单/命令(退出登录) ===')
menu_patterns = [
    'logout',
    'signOut',
    'sign_out',
    'logOut',
    'clearSession',
    'clearToken',
    'revokeToken',
    'invalidateSession',
    'endSession',
    'closeSession',
]

for kw in menu_patterns:
    pattern = re.escape(kw)
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+100]) 
               for m in re.finditer(pattern, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{kw}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ').replace('\r', '')
            print(f'    @{pos}: {ctx_clean[:150]}')

# 3. 搜索deeplink/url协议
print('\n=== 3. 搜索url协议/deeplink ===')
proto_patterns = [
    'trae://',
    'trae-cn://',
    'vscode://',
    'command:',
    'trae.login',
    'trae.logout',
    'trae.account',
    'trae.auth',
]

for proto in proto_patterns:
    pattern = re.escape(proto)
    matches = [(m.start(), content[max(0,m.start()-20):m.end()+80]) 
               for m in re.finditer(pattern, content, re.IGNORECASE)]
    if matches:
        print(f'  [{proto}] 找到 {len(matches)} 处')
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ').replace('\r', '')
            print(f'    @{pos}: {ctx_clean[:120]}')

# 4. 检查product.json
print('\n=== 4. product.json ===')
prod_path = os.path.join(TRAE_CN_APP, 'product.json')
if os.path.exists(prod_path):
    with open(prod_path, 'r', encoding='utf-8') as f:
        prod = json.load(f)
    
    for k in ['deeplinkHost', 'urlProtocol', 'webviewContentExternalBaseUrlTemplate',
              'serverLicense', 'enableMarketplace', 'chat.ai', 'trae.ai']:
        if k in prod:
            val = prod[k]
            if isinstance(val, str) and len(val) > 100:
                val = val[:100] + '...'
            print(f'  {k}: {val}')

# 5. 搜索webview URL
print('\n=== 5. 搜索webview/登录URL ===')
url_patterns = [
    'trae.cn',
    'account.trae',
    'auth.trae',
    'login.trae',
    'api.trae',
    'copilot.trae',
    'license.vscode',
    'accounts.vscode',
]

for up in url_patterns:
    pattern = re.escape(up)
    matches = [(m.start(), content[max(0,m.start()-30):m.end()+80]) 
               for m in re.finditer(pattern, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{up}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ').replace('\r', '')
            print(f'    @{pos}: {ctx_clean[:150]}')
