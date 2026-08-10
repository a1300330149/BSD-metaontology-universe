"""
Trae CN 独立认证机制分析
=======================
分析Trae CN自身的登录体系，不依赖TRAE SOLO CN
"""
import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

main_js = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(main_js, 'r', encoding='utf-8') as f:
    content = f.read()

print('=== 1. 搜索Trae CN独立登录机制 ===')

# 搜索login相关的完整代码块
login_patterns = [
    r'(?:async\s+)?login\w*\s*\([^)]*\)\s*\{',
    r'(?:async\s+)?signIn\w*\s*\([^)]*\)\s*\{',
    r'(?:async\s+)?authenticate\w*\s*\([^)]*\)\s*\{',
    r'LoginByJwt|LoginByToken|LoginByCode|LoginByPassword',
    r'class\s+\w*Auth\w*\{',
    r'class\s+\w*Login\w*\{',
]

for pat in login_patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches:
        for m in matches[:3]:
            # 提取上下文
            start = max(0, m.start() - 100)
            end = min(len(content), m.end() + 200)
            ctx = content[start:end].replace('\n', ' ')[:400]
            print(f'  [{pat[:30]}...] @{m.start()}:')
            print(f'    {ctx}...\n')

print('\n=== 2. 搜索Trae CN的bootConfig ===')
# bootConfig包含API配置
boot_patterns = [
    r'bootConfig',
    r'apiHost',
    r'accountUrl',
    r'authUrl',
    r'ssoUrl',
    r'loginUrl',
    r'oauthUrl',
]

for pat in boot_patterns:
    matches = [(m.start(), content[max(0,m.start()-50):m.end()+150]) 
               for m in re.finditer(pat, content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:250]
            print(f'    @{pos}: {ctx_clean}')

print('\n=== 3. 搜索Trae CN的独立API端点 ===')
api_patterns = [
    r'cloudide/api/v3/trae',
    r'api\.trae\.cn',
    r'api\.trae\.com\.cn',
    r'copilot\.trae',
    r'mcp\.trae',
    r'account\.trae',
    r'auth\.trae',
]

for pat in api_patterns:
    matches = [(m.start(), content[max(0,m.start()-30):m.end()+100]) 
               for m in re.finditer(re.escape(pat), content, re.IGNORECASE)]
    if matches:
        print(f'\n  [{pat}] 找到 {len(matches)} 处:')
        for pos, ctx in matches[:5]:
            ctx_clean = ctx.replace('\n', ' ')[:200]
            print(f'    @{pos}: {ctx_clean}')

print('\n=== 4. 搜索LoginByXxx方法 ===')
login_methods = [
    'LoginByJwt',
    'LoginByToken', 
    'LoginByCode',
    'LoginByPassword',
    'LoginBySso',
    'LoginByPhone',
    'LoginByEmail',
    'LoginByDevice',
    'LoginByFingerprint',
]

for m in login_methods:
    matches = list(re.finditer(m, content))
    if matches:
        print(f'\n  [{m}] 找到 {len(matches)} 处:')
        for match in matches[:3]:
            start = max(0, match.start() - 50)
            end = min(len(content), match.end() + 200)
            ctx = content[start:end].replace('\n', ' ')[:300]
            print(f'    {ctx}')

print('\n=== 5. 检查Trae CN的独立配置文件 ===')
# 查找Trae CN特有的配置
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        fl = f.lower()
        if any(kw in fl for kw in ['auth', 'login', 'token', 'config', 'setting']):
            if f.endswith('.json'):
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        data = json.load(fh)
                    text = json.dumps(data, ensure_ascii=False)
                    if any(kw in text.lower() for kw in ['login', 'auth', 'token', 'url', 'api']):
                        print(f'  {os.path.relpath(fp, TRAE_CN_DATA)}: {len(text)} chars')
                except:
                    pass

print('\n=== 6. 搜索trae.ai域名 ===')
ai_matches = [(m.start(), content[max(0,m.start()-30):m.end()+100]) 
              for m in re.finditer(r'trae\.ai', content, re.IGNORECASE)]
if ai_matches:
    print(f'  trae.ai 找到 {len(ai_matches)} 处:')
    for pos, ctx in ai_matches[:5]:
        ctx_clean = ctx.replace('\n', ' ')[:200]
        print(f'    @{pos}: {ctx_clean}')
