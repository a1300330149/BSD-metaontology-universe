"""
深度分析JWT Token共享机制
找到Trae CN独立认证路径
"""
import os, json

TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'

print('=== 1. 分析共享Token来源 ===')

# 检查当前Token
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path):
    with open(jwt_path, 'r') as f:
        jwt = f.read().strip()
    print(f'  当前Token长度: {len(jwt)} chars')
    print(f'  Token前100字: {jwt[:100]}...')

# 解析JWT Header和Payload
import base64

def parse_jwt(token):
    try:
        parts = token.split('.')
        if len(parts) >= 2:
            header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            return header, payload
    except:
        pass
    return None, None

if jwt:
    header, payload = parse_jwt(jwt)
    if header:
        print(f'\n  JWT Header: {json.dumps(header, indent=2)}')
    if payload:
        # 只显示关键字段
        keys = ['sub', 'uid', 'userId', 'account_id', 'exp', 'iat', 'iss', 'aud', 
                'scope', 'type', 'role', 'username', 'nickname']
        print(f'  JWT Payload (关键字段):')
        for k in keys:
            if k in payload:
                val = payload[k]
                if isinstance(val, str) and len(val) > 50:
                    val = val[:50] + '...'
                print(f'    {k}: {val}')

print('\n=== 2. 检查TRAE SOLO CN的认证存储 ===')

# 检查SOLO的数据目录
for root, dirs, files in os.walk(TRAE_SOLO_DATA):
    for f in files:
        fp = os.path.join(root, f)
        fl = f.lower()
        if any(kw in fl for kw in ['token', 'auth', 'login', 'cookie', 'session', 'jwt']):
            size = os.path.getsize(fp)
            print(f'  {os.path.relpath(fp, TRAE_SOLO_DATA)}: {size:,} bytes')

# 检查SOLO的Local State
solo_ls = os.path.join(TRAE_SOLO_DATA, 'Local State')
if os.path.exists(solo_ls):
    with open(solo_ls, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    def find_auth(obj, path=''):
        results = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                kl = k.lower()
                if any(kw in kl for kw in ['token', 'session', 'user', 'login', 'auth', 'cookie']):
                    sv = str(v)[:100] if not isinstance(v, (dict, list)) else type(v).__name__
                    results.append((path + '.' + k, sv))
                results.extend(find_auth(v, path + '.' + k))
        return results
    
    auth_found = find_auth(ls)
    print(f'\n  TRAE SOLO CN Local State 认证字段 ({len(auth_found)}):')
    for p, v in auth_found[:15]:
        print(f'    {p}: {v}')

print('\n=== 3. 检查.trae-cn下所有认证相关文件 ===')
for item in sorted(os.listdir(TRAE_CONFIG)):
    ip = os.path.join(TRAE_CONFIG, item)
    if os.path.isfile(ip):
        fl = item.lower()
        if any(kw in fl for kw in ['token', 'auth', 'login', 'cookie', 'session', 'jwt', 'credential']):
            size = os.path.getsize(ip)
            print(f'  {item}: {size:,} bytes')
    elif os.path.isdir(ip):
        fl = item.lower()
        if any(kw in fl for kw in ['token', 'auth', 'login', 'credential']):
            print(f'  📁 {item}/')

print('\n=== 4. 对比Trae CN与TRAE SOLO CN的认证文件 ===')
cn_auth = []
solo_auth = []

for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        fl = f.lower()
        if any(kw in fl for kw in ['token', 'auth', 'cookie', 'session', 'jwt']):
            cn_auth.append(os.path.relpath(os.path.join(root, f), TRAE_CN_DATA))

for root, dirs, files in os.walk(TRAE_SOLO_DATA):
    for f in files:
        fl = f.lower()
        if any(kw in fl for kw in ['token', 'auth', 'cookie', 'session', 'jwt']):
            solo_auth.append(os.path.relpath(os.path.join(root, f), TRAE_SOLO_DATA))

print(f'  Trae CN认证文件: {len(cn_auth)} 个')
for a in cn_auth:
    print(f'    {a}')

print(f'\n  TRAE SOLO CN认证文件: {len(solo_auth)} 个')
for a in solo_auth:
    print(f'    {a}')

print('\n=== 5. 查找独立Token存储路径 ===')
# 检查Trae CN的state.vscdb（SQLite数据库，存储状态）
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        if f.endswith('.vscdb'):
            fp = os.path.join(root, f)
            size = os.path.getsize(fp)
            print(f'  {os.path.relpath(fp, TRAE_CN_DATA)}: {size:,} bytes')
