"""
找到Trae CN凭证存储路径 + 注入本源端凭证
"""
import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 1. 搜索凭证存储路径 ===')

# 搜索ide_credential相关的路径
cred_patterns = [
    r'ide_credential',
    r'credential.*path',
    r'write.*credential',
    r'read.*credential',
    r'credential.*json',
    r'credential.*file',
]

for pat in cred_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+200]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:5]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f'    @{pos}: {ctx_clean}')

print('\n\n=== 2. 搜索workspaceStorage和globalStorage ===')
# 搜索storage路径模式
storage_patterns = [
    r'workspaceStorage',
    r'globalStorage',
    r'storage\.json',
    r'state\.vscdb',
]

for pat in storage_patterns:
    matches = [(m.start(), content[max(0,m.start()-30):m.end()+100]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f'    @{pos}: {ctx_clean}')

print('\n\n=== 3. 搜索完整的凭证读写流程 ===')
# 找OAuth认证的完整类
oauth_class = list(re.finditer(r'class\s+\w*OAuthenticator\w*\{', content))
for m in oauth_class[:2]:
    start = m.start()
    brace_count = 0
    end = start
    for i in range(start, min(start + 5000, len(content))):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0 and i > start + 500:
                end = i + 1
                break
    
    ctx = content[start:end]
    print(f'\n--- OAuth类 @{m.start()} ---')
    
    # 提取关键方法
    methods = re.findall(r'(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{', ctx)
    print(f'  方法列表: {methods[:20]}')

print('\n\n=== 4. 搜索Token存储相关 ===')
# 找update/serverKey
token_store = [(m.start(), content[max(0,m.start()-100):m.end()+300]) 
               for m in re.finditer(r'update.*serverKey|serverKey.*update|readAccessToken|readRefreshToken', content)]
for pos, ctx in token_store[:5]:
    ctx_clean = ctx.replace('\n', ' ')[:500]
    print(f'\n  @{pos}: {ctx_clean}')

print('\n\n=== 5. 检查当前本地存储的所有JSON文件 ===')
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        if f.endswith('.json'):
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, TRAE_CN_DATA)
            size = os.path.getsize(fp)
            
            # 检查是否包含认证相关内容
            try:
                with open(fp, 'r', encoding='utf-8') as fh:
                    data = json.load(fh)
                text = json.dumps(data, ensure_ascii=False)
                if any(kw in text.lower() for kw in ['token', 'auth', 'login', 'user', 'credential', 'session']):
                    print(f'  {rel}: {size:,} bytes (含认证数据)')
            except:
                pass
