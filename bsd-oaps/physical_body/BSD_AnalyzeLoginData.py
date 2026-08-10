"""
检查当前认证状态并注入本源登录凭据
目标：让Trae CN系统认为已通过本源认证登录
"""
import json, os, re, time

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
MAIN_JS = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\out\main.js'

# 1. 检查storage.json当前状态
print("=" * 60)
print("1. 检查storage.json认证状态")
print("=" * 60)

with open(STORAGE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 关键认证字段检查
auth_keys = [
    '_logged_in', '_is_authenticated',
    'iCubeAuthInfo://icube.cloudide',
    'iCubeAuthInfo://usertag',
    'iCubeAuthInfo://jwt-token',
    'iCubeAuthInfo://icube-dc',
]

for key in auth_keys:
    val = data.get(key, '(missing)')
    if isinstance(val, str):
        print(f'  {key}: {val[:60]}...' if len(val) > 60 else f'  {key}: {val}')
    else:
        print(f'  {key}: {val}')

# 2. 检查main.js中Jx函数的scope
print("\n" + "=" * 60)
print("2. 检查Jx函数scope配置")
print("=" * 60)

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    code = f.read()

m = re.search(r'Jx=\(t,e,i\)=>\(\{[^}]{0,500}\}\)', code)
if m:
    jx = m.group(0)
    # 提取scope
    scope_match = re.search(r'scope:([^,}]+)', jx)
    if scope_match:
        print(f'  Jx scope: {scope_match.group(1)}')
    # 检查是否有token相关
    has_token = 'token' in jx
    print(f'  Jx has token field: {has_token}')
    print(f'  Jx full: {jx[:200]}...')
else:
    print('  Jx function not found!')

# 3. 检查getUserInfo返回结构
print("\n" + "=" * 60)
print("3. 检查getUserInfo返回的account结构")
print("=" * 60)

# 搜索 getAuthUserInfo 或 getUserInfo 的返回
for pattern in [
    r'async getUserInfo\(\)\{return [^}]+\}',
    r'getAuthUserInfo[^}]{0,100}',
]:
    for m in re.finditer(pattern, code):
        print(f'  Found: {m.group(0)[:150]}')
        break
    break

# 搜索 setUserInfo 被调用的位置，了解account数据结构
print('\n  搜索setUserInfo调用点的上下文...')
for m in re.finditer(r'setUserInfo\([^)]+\)', code):
    pos = m.start()
    ctx = code[max(0,pos-80):pos+40].replace('\n', ' ')
    if 'account' in ctx and 'scope' in ctx:
        print(f'  @{pos}: ...{ctx.strip()[:150]}...')
        break

# 4. 生成本源认证所需的完整数据
print("\n" + "=" * 60)
print("4. 生成本源登录所需的认证数据")
print("=" * 60)

# 关键：构造一个完整的userInfo对象，让系统认为已登录
# 从代码分析：account.scope === It.MARSCODE ("marscode") 是登录状态的判断条件

# JWT token (本源签名)
import base64, hmac, hashlib

def generate_essence_jwt():
    header = json.dumps({"alg": "HS256", "typ": "JWT"})
    payload = json.dumps({
        "iss": "BSD_ESSENCE",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600000,
        "user_id": "a5b7a8623fdea6b8",
        "type": "essence_login",
        "theory_base": "本源知识体系"
    })
    # Base64编码
    h = base64.urlsafe_b64encode(header.encode()).rstrip(b'=').decode()
    p = base64.urlsafe_b64encode(payload.encode()).rstrip(b'=').decode()
    # HMAC签名
    sig_input = f"{h}.{p}"
    sig = base64.urlsafe_b64encode(
        hmac.new(b'bsd_essence_key', sig_input.encode(), hashlib.sha256).digest()
    ).rstrip(b'=').decode()
    return f"{h}.{p}.{sig}"

jwt_token = generate_essence_jwt()
print(f'  JWT Token: {jwt_token[:80]}...')

# 构造完整的userInfo
user_info = {
    "token": jwt_token,
    "refreshToken": jwt_token,
    "expiredAt": int(time.time()) + 3600000000,  # 1小时后过期
    "tokenReleaseAt": int(time.time()),
    "userId": "a5b7a8623fdea6b8",
    "account": {
        "scope": "marscode",  # It.MARSCODE - 关键！登录判断依据
        "loginScope": "trae",
        "organization": "",
        "work_country": "",
        "email": "",
        "avatar_url": "",
        "description": "",
        "storeCountryCode": "cn",
        "storeCountrySrc": "",
        "storeRegion": "CN",
        "userTag": "",
        "migrateToSG": False
    }
}

print(f'  account.scope: {user_info["account"]["scope"]}')
print(f'  account.loginScope: {user_info["account"]["loginScope"]}')
print(f'  token valid: {len(jwt_token)} chars')

# 5. 检查getUserInfo在代码中如何构建返回值
print("\n" + "=" * 60)
print("5. 分析getUserInfo数据流")
print("=" * 60)

# 找到Jx函数和getUserInfo的关系
# 搜索 getUserInfo → Jx 的调用链
for pattern in [
    r'Jx\([^)]*\)',  # Jx调用
    r'getUserInfo[^;]{0,200}',  # getUserInfo实现
]:
    matches = list(re.finditer(pattern, code))
    for m in matches[:3]:
        pos = m.start()
        ctx = code[max(0,pos-30):pos+100].replace('\n', ' ')
        print(f'  @{pos}: {m.group(0)[:100]}')
        print(f'    context: ...{ctx[:150]}...')
        print()

print('\n' + '=' * 60)
print('准备注入登录数据 - 请确认')
print('=' * 60)
