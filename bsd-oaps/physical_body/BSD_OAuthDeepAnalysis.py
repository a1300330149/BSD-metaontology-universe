"""
深入分析main.js中的OAuth配置和API端点
找到正确的URL格式和请求参数
"""
import os
import re
import json

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=' * 70)
print('  深入分析OAuth配置和API端点')
print('=' * 70)

# 1. 搜索所有URL模式
print('\n=== 1. 搜索API URL ===')

# 搜索trae和cloudide相关路径
url_patterns = [
    r'"(/trae/[^"]+)"',
    r'"(/cloudide/[^"]+)"',
    r'"(https?://[^"]*trae[^"]*)"',
    r'"(https?://[^"]*cloudide[^"]*)"',
    r'baseURL\s*:\s*"([^"]+)"',
    r'BASE_URL\s*=\s*"([^"]+)"',
    r'apiHost\s*[:=]\s*"([^"]+)"',
    r'serverUrl\s*[:=]\s*"([^"]+)"',
]

found_urls = set()
for pat in url_patterns:
    matches = re.findall(pat, content, re.IGNORECASE)
    if matches:
        for m in matches:
            if len(m) < 200:
                found_urls.add(m)

print(f'\n  找到 {len(found_urls)} 个URL:')
for url in sorted(found_urls)[:50]:
    print(f'    {url}')

# 2. 分析OAuth授权URL
print('\n=== 2. OAuth授权URL ===')

# 搜索authorize相关
auth_patterns = [
    r'authorize.*?["\']([^"\']+)["\']',
    r'oauth.*?url.*?["\']([^"\']+)["\']',
    r'login.*?url.*?["\']([^"\']+)["\']',
    r'authorizeUrl["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    r'loginUrl["\']?\s*[:=]\s*["\']([^"\']+)["\']',
]

for pat in auth_patterns:
    matches = re.findall(pat, content, re.IGNORECASE)
    if matches:
        print(f'\n  [{pat[:30]}...]')
        for m in set(matches):
            if len(m) < 200:
                print(f'    {m}')

# 3. 分析完整的OAuth配置对象
print('\n=== 3. OAuth配置对象 ===')

# 搜索包含client_id, authorize, token_url等的配置
config_patterns = [
    r'client_id["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    r'authorize_url["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    r'token_url["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    r'redirect_uri["\']?\s*[:=]\s*["\']([^"\']+)["\']',
    r'scope["\']?\s*[:=]\s*["\']([^"\']+)["\']',
]

for pat in config_patterns:
    matches = re.findall(pat, content, re.IGNORECASE)
    if matches:
        print(f'\n  [{pat[:30]}...]')
        for m in set(matches):
            if len(m) < 200:
                print(f'    {m}')

# 4. 搜索完整的OAuth类定义
print('\n=== 4. OAuth类和方法 ===')

# 找OAuthenticator类
oauth_class = re.finditer(r'class\s+\w*OAuthenticator\w*', content)
for m in oauth_class:
    print(f'\n  OAuth类 @{m.start()}')
    
    # 提取整个类
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 5000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 200:
                end = i + 1
                break
    
    ctx = content[start:end]
    
    # 找方法
    methods = re.findall(r'(?:async\s+)?(\w+)\s*\(([^)]*)\)\s*\{', ctx)
    print(f'    方法:')
    for name, args in methods[:20]:
        print(f'      - {name}({args})')

# 5. 分析ExchangeToken完整调用
print('\n=== 5. ExchangeToken调用分析 ===')

# 找所有ExchangeToken相关代码
exchange_calls = [(m.start(), content[max(0,m.start()-200):m.end()+300]) 
                   for m in re.finditer(r'ExchangeToken', content)]
if exchange_calls:
    print(f'\n  找到 {len(exchange_calls)} 处ExchangeToken引用:')
    for pos, ctx in exchange_calls[:5]:
        ctx_clean = ctx.replace('\n', ' ')[:500]
        print(f'\n    @{pos}:')
        print(f'    {ctx_clean}')

# 6. 分析CheckLogin和LoginByJwt
print('\n=== 6. 登录API分析 ===')

login_apis = [(m.start(), content[max(0,m.start()-100):m.end()+400]) 
              for m in re.finditer(r'CheckLogin|LoginByJwt|ClearRefreshToken', content)]
if login_apis:
    print(f'\n  找到 {len(login_apis)} 处登录API引用:')
    for pos, ctx in login_apis[:10]:
        ctx_clean = ctx.replace('\n', ' ')[:600]
        print(f'\n    @{pos}:')
        print(f'    {ctx_clean}')

# 7. 分析baseURL和配置
print('\n=== 7. 服务端配置 ===')

# 搜索配置文件路径或配置对象
config_paths = [
    r'iCubeApp.*?config',
    r'authConfig',
    r'TRAE.*?config',
    r'SOLO.*?config',
]

for pat in config_paths:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+200]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'    @{pos}: {ctx_clean}')

# 8. 提取authConfig完整对象
print('\n=== 8. authConfig完整配置 ===')

# 尝试找到authConfig对象的完整定义
config_start = re.search(r'authConfig["\']?\s*[:=]\s*\{', content)
if config_start:
    start = config_start.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 3000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 200:
                end = i + 1
                break
    
    config_ctx = content[start:end]
    print(f'\n  authConfig @{start}:')
    print(config_ctx[:2500])

print('\n' + '=' * 70)
print('  分析完成')
print('=' * 70)