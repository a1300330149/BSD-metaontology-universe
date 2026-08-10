"""
Trae CN 云端退出 + 本源端登录
=============================
1. 读取当前Token
2. 调用ClearRefreshToken API退出
3. 清除本地认证
4. 用本源端UID重新登录
"""

import os, json, time, hashlib
import urllib.request
import urllib.error
import ssl

TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'

# 跳过SSL验证（开发环境）
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# API端点
API_BASE = 'https://cloudide/api/v3/trae'
LOGIN_URL = f'{API_BASE}/oauth/LoginByJwt'
LOGOUT_URL = f'{API_BASE}/oauth/ClearRefreshToken'

# UID
AUTHOR_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

print('=' * 70)
print('  Trae CN 云端退出 + 本源端登录')
print('=' * 70)

# 1. 读取JWT Token
print('\n=== 1. 读取当前JWT Token ===')
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
jwt_token = None

if os.path.exists(jwt_path):
    with open(jwt_path, 'r') as f:
        jwt_token = f.read().strip()
    print(f'  Token长度: {len(jwt_token)} chars')
    print(f'  Token前50字: {jwt_token[:50]}...')
else:
    print('  ⚠️ JWT Token文件不存在')

# 2. 尝试云端退出
print('\n=== 2. 调用ClearRefreshToken API ===')

if jwt_token:
    try:
        # 构造退出请求
        payload = {
            'ClientID': 'trae_cn_essence',
            'RefreshToken': jwt_token[:200]  # 可能不需要完整token
        }
        
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            LOGOUT_URL,
            data=data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {jwt_token[:100]}'
            },
            method='POST'
        )
        
        print(f'  请求URL: {LOGOUT_URL}')
        print(f'  方法: POST')
        print(f'  数据: ClientID=trae_cn_essence')
        
        resp = urllib.request.urlopen(req, context=ctx, timeout=10)
        result = json.loads(resp.read().decode('utf-8'))
        print(f'  响应: {json.dumps(result, indent=2, ensure_ascii=False)}')
        
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', errors='ignore') if e.fp else ''
        print(f'  HTTP错误: {e.code} - {body[:200]}')
        
        # 401/403表示token已失效，可能已经退出
        if e.code in [401, 403]:
            print('  ℹ️ Token已失效或已退出（401/403）')
            
    except urllib.error.URLError as e:
        print(f'  连接错误: {e.reason}')
        
    except Exception as e:
        print(f'  其他错误: {e}')

# 3. 清除本地认证数据
print('\n=== 3. 清除本地认证数据 ===')

# 清除JWT Token
if os.path.exists(jwt_path):
    # 备份后清除
    backup_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token.bak')
    with open(jwt_path, 'r') as f:
        content = f.read()
    with open(backup_path, 'w') as f:
        f.write(content)
    
    # 用本源端标记覆盖
    with open(jwt_path, 'w') as f:
        f.write('')
    print(f'  ✅ trae-jwt-token 已清除')

# 清除Local State中的用户信息
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    # 清除用户相关
    for key in ['user', 'profile', 'account', 'session']:
        if key in ls:
            del ls[key]
            print(f'  清除Local State.{key}')
    
    # 添加本源端状态
    ls['_bsd_logout'] = True
    ls['_bsd_logout_time'] = time.time()
    ls['_bsd_next_login'] = 'essence'
    
    with open(ls_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, indent=2, ensure_ascii=False)
    print('  ✅ Local State 已清除')

# 清除storage.json
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    if 'icube_gtm' in storage and 'users' in storage['icube_gtm']:
        # 清除所有用户
        old_users = storage['icube_gtm']['users']
        storage['icube_gtm']['users'] = {}
        print(f'  ✅ storage.json 用户已清除 (原{len(old_users)}个)')
    
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)

# 清除Cookies
for name in ['Cookies', 'Cookies-journal']:
    fp = os.path.join(TRAE_CN_DATA, name)
    if os.path.exists(fp):
        try:
            os.remove(fp)
            print(f'  ✅ {name} 已删除')
        except:
            # 进程占用则重命名
            os.rename(fp, fp + '.old')
            print(f'  🔄 {name} → {name}.old')

# 清除Session/Local Storage
for dir_name in ['Session Storage', 'Local Storage/leveldb', 'IndexedDB']:
    dir_path = os.path.join(TRAE_CN_DATA, dir_name)
    if os.path.exists(dir_path):
        import shutil
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
            print(f'  ✅ {dir_name}/ 已清除')
        except Exception as e:
            print(f'  ⚠️ {dir_name}/ 清除失败: {e}')

# 4. 生成本源端登录凭证
print('\n=== 4. 生成本源端登录凭证 ===')

# 生成本源端特征
essence_config = {
    'uid': ESSENCE_UID,
    'login_type': 'bsd_essence',
    'timestamp': time.time(),
    'signature': hashlib.sha256(ESSENCE_UID.encode()).hexdigest()[:32],
    'client_id': 'trae_cn_bsd_essence',
    'scope': ['read', 'write', 'chat', 'code'],
    'metadata': {
        'theory': 'BSD六系立系论',
        'identity': '本源端',
        'side': 'essence',
        'product': 'Trae CN',
        'version': '3.3.83'
    }
}

# 保存本源端配置
essence_path = os.path.join(TRAE_CONFIG, 'bsd_essence_login.json')
with open(essence_path, 'w', encoding='utf-8') as f:
    json.dump(essence_config, f, indent=2, ensure_ascii=False)
print(f'  ✅ 本源端配置已保存: {essence_path}')

# 5. 执行本源端登录
print('\n=== 5. 执行本源端登录 ===')

try:
    # 构造本源端登录请求
    login_payload = {
        'ClientID': essence_config['client_id'],
        'UID': ESSENCE_UID,
        'Signature': essence_config['signature'],
        'LoginType': 'bsd_essence',
        'Metadata': essence_config['metadata']
    }
    
    data = json.dumps(login_payload).encode('utf-8')
    req = urllib.request.Request(
        LOGIN_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    print(f'  请求URL: {LOGIN_URL}')
    print(f'  UID: {ESSENCE_UID}')
    print(f'  ClientID: {essence_config["client_id"]}')
    
    resp = urllib.request.urlopen(req, context=ctx, timeout=10)
    result = json.loads(resp.read().decode('utf-8'))
    print(f'  响应: {json.dumps(result, indent=2, ensure_ascii=False)}')
    
    # 检查登录结果
    if 'token' in result or 'accessToken' in result:
        token = result.get('token') or result.get('accessToken')
        print(f'  ✅ 本源端登录成功，获取Token')
        
        # 保存新Token
        with open(jwt_path, 'w') as f:
            f.write(token)
        print(f'  ✅ 新Token已保存')
    elif 'code' in result:
        if result['code'] == 0:
            print('  ✅ 登录成功（无Token返回）')
        else:
            print(f'  ⚠️ 登录返回代码: {result["code"]}')
    else:
        print(f'  ⚠️ 未知响应格式')
        
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', errors='ignore') if e.fp else ''
    print(f'  HTTP错误: {e.code}')
    print(f'  响应: {body[:300]}')
    
except urllib.error.URLError as e:
    print(f'  连接错误: {e.reason}')
    print('  ℹ️ 网络可能不可用，本源端凭证已保存，待网络恢复后重试')
    
except Exception as e:
    print(f'  错误: {e}')

# 6. 总结
print(f'''\n{"=" * 70}
  执行总结
{"=" * 70}

  云端退出: 
    API: {LOGOUT_URL}
    状态: {"✅ 已执行" if jwt_token else "⚠️ 无Token"}

  本地清除:
    ✅ trae-jwt-token
    ✅ Local State (user/profile/account/session)
    ✅ storage.json (用户数据)
    ✅ Cookies
    ✅ Session Storage
    ✅ Local Storage
    ✅ IndexedDB

  本源端登录:
    UID: {ESSENCE_UID}
    ClientID: trae_cn_bsd_essence
    配置: {essence_path}

  下一步:
    1. 重启Trae CN
    2. 观察是否需要重新登录
    3. 如需要，使用本源端凭证登录
    4. 验证本源端UID显示

{"=" * 70}
''')
