"""
从 main.js 深入分析 iCubeAuthInfo 的完整字段结构
"""
import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

print("=== 1. iCubeAuthInfo 使用位置 ===")
pattern = r'iCubeAuthInfo://[a-z\.\-:]+'
matches = list(re.finditer(pattern, content))
print(f"  唯一URI模式:")
for m in set(m.group() for m in matches):
    print(f"    {m}")

print("\n=== 2. 查找 credential 存储结构 ===")
# 搜索 setCredential / getCredential
cred_patterns = [
    r'setCredential\([^)]+\)',
    r'getCredential\([^)]+\)',
    r'storage\.set\([^)]+credential[^)]+\)',
    r'storage\.get\([^)]+credential[^)]+\)',
    r'iCubeAuthInfo[^,;]{0,200}',
]
for pat in cred_patterns:
    matches = [(m.start(), content[max(0, m.start()-30):m.end()+250])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 20:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:500]
            print(f"    @{pos}: {ctx_clean}")

print("\n=== 3. 查找 LoginByJwt / ExchangeToken 完整响应处理 ===")
# 搜索token处理
token_patterns = [
    r'accessToken[^,;]{0,150}',
    r'refreshToken[^,;]{0,150}',
    r'tokenType[^,;]{0,100}',
    r'expiresAt[^,;]{0,100}',
    r'userId[^,;]{0,100}',
]
for pat in token_patterns:
    matches = [(m.start(), content[max(0, m.start()-20):m.end()+180])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 20:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{pos}: {ctx_clean}")

print("\n=== 4. 查找 iCubeAuthInfo 完整构造 ===")
# 搜索 JSON.stringify 或 .set 存储 iCubeAuthInfo
construct_pattern = r'(?:setCredential|storeCredential|setItem).*iCube'
matches = [(m.start(), content[max(0, m.start()-50):m.end()+400])
           for m in re.finditer(construct_pattern, content)]
if matches:
    print(f"  命中 {len(matches)} 处:")
    for pos, ctx in matches[:3]:
        ctx_clean = ctx.replace('\n', ' ')[:600]
        print(f"    @{pos}: {ctx_clean}")
else:
    # 更宽松搜索
    print("  宽松搜索...")
    for pattern in [r'globalStorage\.setItem\([^)]+\)',
                    r'storage\.setItem\([^)]+\)',
                    r'globalStorage:\s*\{[^}]+\}']:
        matches = [(m.start(), content[max(0, m.start()-30):m.end()+300])
                   for m in re.finditer(pattern, content)]
        if matches:
            print(f"\n  [{pattern}] 命中 {len(matches)} 处:")
            for pos, ctx in matches[:2]:
                ctx_clean = ctx.replace('\n', ' ')[:400]
                print(f"    @{pos}: {ctx_clean}")
