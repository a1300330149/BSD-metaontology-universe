"""
Trae CN OAuth登录流程深度分析
找到loginCredentialCallback的完整实现
"""
import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 1. loginCredentialCallback完整实现 ===')
# 找到loginCredentialCallback的完整代码块
start_pattern = r'async loginCredentialCallback'
matches = list(re.finditer(start_pattern, content))
for m in matches[:2]:
    # 从匹配位置开始，找到函数结束（通过大括号计数）
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 3000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 100:
                end = i + 1
                break
    
    ctx = content[start:end]
    print(f'\n--- 位置 @{m.start()} ---')
    print(ctx[:2000])

print('\n\n=== 2. checkLogin完整实现 ===')
start_pattern2 = r'async checkLogin'
matches2 = list(re.finditer(start_pattern2, content))
for m in matches2[:2]:
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 1000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 100:
                end = i + 1
                break
    
    ctx = content[start:end]
    print(f'\n--- 位置 @{m.start()} ---')
    print(ctx[:1000])

print('\n\n=== 3. ExchangeToken流程 ===')
# 搜索ExchangeToken相关
exchange_matches = [(m.start(), content[max(0,m.start()-100):m.end()+300]) 
                    for m in re.finditer(r'ExchangeToken', content)]
for pos, ctx in exchange_matches[:3]:
    ctx_clean = ctx.replace('\n', ' ')[:500]
    print(f'\n  @{pos}: {ctx_clean}')

print('\n\n=== 4. 本地凭证存储路径 ===')
# 搜索ide_credential相关
cred_matches = [(m.start(), content[max(0,m.start()-100):m.end()+300]) 
                for m in re.finditer(r'ide_credential|credential.*path|credential.*file', content, re.IGNORECASE)]
for pos, ctx in cred_matches[:5]:
    ctx_clean = ctx.replace('\n', ' ')[:400]
    print(f'\n  @{pos}: {ctx_clean}')

print('\n\n=== 5. 搜索认证状态存储 ===')
# 搜索readAccessToken|readRefreshToken|writeAccessToken等
token_patterns = [
    r'readAccessToken',
    r'writeAccessToken',
    r'readRefreshToken', 
    r'writeRefreshToken',
    r'writeToken',
    r'saveToken',
]

for pat in token_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+200]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f'    @{pos}: {ctx_clean}')

print('\n\n=== 6. 查找API Host配置 ===')
# 搜索normal|USTTP|SG等区域配置
api_host_matches = [(m.start(), content[max(0,m.start()-100):m.end()+200]) 
                    for m in re.finditer(r'apiHost.*normal|apiHost.*USTTP|apiHost.*SG', content, re.IGNORECASE)]
for pos, ctx in api_host_matches[:3]:
    ctx_clean = ctx.replace('\n', ' ')[:400]
    print(f'\n  @{pos}: {ctx_clean}')
