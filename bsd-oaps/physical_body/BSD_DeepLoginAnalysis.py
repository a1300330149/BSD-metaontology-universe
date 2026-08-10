"""
深度分析传统UID登录完整链路
定位：存储位置 + 加密机制 + 启动参数
"""
import os, json, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

print("=== 1. 查找 userDataPath 解析 ===")
with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

patterns = [
    r'userDataPath[^,;]+',
    r'user-data-dir[^,;]+',
    r'--user-data-dir[^,;]+',
    r'app\.getPath\(["\']userData["\']\)[^,;]+',
    r'Roaming[^"\']+',
    r'\.trae-cn[^"\']+',
]
for pat in patterns:
    matches = [(m.start(), content[max(0, m.start()-40):m.end()+120])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 50:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f"    @{pos}: {ctx_clean}")

print("\n=== 2. 查找 storage.json 读写 ===")
storage_patterns = [
    r'storage\.json[^,;]+',
    r'globalStorage[^,;]+',
    r'globalStorage/iCubeAuthInfo[^,;]+',
    r'iCubeAuthInfo://icube[^,;]+',
    r'os_crypt[^,;]+',
    r'encrypted_key[^,;]+',
]
for pat in storage_patterns:
    matches = [(m.start(), content[max(0, m.start()-30):m.end()+180])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 30:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{pos}: {ctx_clean}")

print("\n=== 3. 查找 DPAPI / windows 加密 ===")
dpapi_patterns = [
    r'DPAPI|dpapi',
    r'CryptProtectData|cryptprotect',
    r'machine_guid|MachineGuid',
    r'PROTECTED_DATA|protected_data',
    r'os_crypt\.encrypted_key',
    r'encrypted_key[^,;]{0,200}',
]
for pat in dpapi_patterns:
    matches = [(m.start(), content[max(0, m.start()-30):m.end()+200])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 30:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{pos}: {ctx_clean}")

print("\n=== 4. 查找 trae-jwt-token 读写 ===")
jwt_patterns = [
    r'trae-jwt-token[^,;]+',
    r'jwt-token[^,;]+',
    r'jwtToken[^,;]+',
    r'jwt_token[^,;]+',
    r'JWTToken[^,;]+',
]
for pat in jwt_patterns:
    matches = [(m.start(), content[max(0, m.start()-30):m.end()+200])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 30:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{pos}: {ctx_clean}")

print("\n=== 5. 查找 CheckLogin / login 相关端点 ===")
login_patterns = [
    r'CheckLogin[^,;]+',
    r'LoginByJwt[^,;]+',
    r'ExchangeToken[^,;]+',
    r'ClearRefreshToken[^,;]+',
    r'cloudide/api/v3/trae/[^"\']+',
    r'trae/api/v3/oauth/[^"\']+',
]
for pat in login_patterns:
    matches = [(m.start(), content[max(0, m.start()-20):m.end()+150])
               for m in re.finditer(pat, content)]
    if matches and len(matches) < 30:
        print(f"\n  [{pat}] 命中 {len(matches)} 处:")
        for pos, ctx in matches[:2]:
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f"    @{pos}: {ctx_clean}")
