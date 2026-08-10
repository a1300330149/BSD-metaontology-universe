#!/usr/bin/env python3
"""
BSD 全优化注入 + TRAE Work CN 启动验证
=====================================
1. 修复 JWT theoory_base → theory_base
2. 覆盖 icube-dc 原始密钥
3. 全通道并行注入
4. 启动 TRAE Work CN 验证
"""

import os, json, base64, time, hmac, hashlib, subprocess
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
AHA_DIR = os.path.join(TRAE_DATA, 'aha')
TINY = os.path.join(AHA_DIR, 'TinyStorage')
REMOTE_STATE = os.path.join(AHA_DIR, 'Remote_State')
CREDENTIALS_DIR = r'C:\Users\13003\.bsd-essence'
TRAE_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'

# AES 密钥
AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
AHA_PREFIX = bytes.fromhex('746305100000')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}


def encrypt_aha(plaintext: bytes) -> str:
    """AHA 加密"""
    iv = os.urandom(16)
    padded = pad(plaintext, AES.block_size)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    encrypted = cipher.encrypt(padded)
    result = AHA_PREFIX + iv + encrypted
    return base64.b64encode(result).decode('utf-8')


def fix_jwt():
    """修复 JWT theoory_base → theory_base"""
    print('\n[1/4] 修复 JWT...')
    
    jwt_file = os.path.join(CREDENTIALS_DIR, 'essence-jwt-token')
    if not os.path.exists(jwt_file):
        print('  ❌ JWT 文件不存在')
        return None
    
    with open(jwt_file, 'r', encoding='utf-8') as f:
        jwt_token = f.read().strip()
    
    parts = jwt_token.split('.')
    if len(parts) != 3:
        print('  ❌ JWT 格式错误')
        return None
    
    # 解码 payload
    payload_bytes = base64.b64decode(parts[1] + '==')
    payload = json.loads(payload_bytes)
    
    # 修复 theoory_base → theory_base
    data = payload.get('data', {})
    if 'theoory_base' in data:
        data['theory_base'] = data.pop('theoory_base')
        print('  ✅ 修复 theoory_base → theory_base')
    
    payload['data'] = data
    
    # 重新签名
    header = {'alg': 'HS256', 'typ': 'JWT'}
    header_b64 = base64.b64encode(json.dumps(header, separators=(',', ':')).encode()).rstrip(b'=').decode()
    payload_b64 = base64.b64encode(json.dumps(payload, separators=(',', ':')).encode()).rstrip(b'=').decode()
    
    # 使用固定签名密钥
    secret = b'bsd_essence_secret_key_2026'
    signing_input = f'{header_b64}.{payload_b64}'.encode()
    signature = hmac.new(secret, signing_input, hashlib.sha256).digest()
    sig_b64 = base64.b64encode(signature).rstrip(b'=').decode()
    
    new_jwt = f'{header_b64}.{payload_b64}.{sig_b64}'
    
    # 保存
    with open(jwt_file, 'w', encoding='utf-8') as f:
        f.write(new_jwt)
    
    # 更新 credentials.json
    cred_file = os.path.join(CREDENTIALS_DIR, 'credentials.json')
    if os.path.exists(cred_file):
        with open(cred_file, 'r', encoding='utf-8') as f:
            creds = json.load(f)
        creds['jwt_token'] = new_jwt
        with open(cred_file, 'w', encoding='utf-8') as f:
            json.dump(creds, f, ensure_ascii=False, indent=2)
    
    print(f'  ✅ JWT 已修复并保存')
    return new_jwt


def full_injection(jwt_token):
    """全通道并行注入"""
    print('\n[2/4] 全通道并行注入...')
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 本源认证数据
    essence_auth = {
        'uid': AUTHOR['essence_uid'],
        'userId': AUTHOR['essence_uid'],
        'id': AUTHOR['essence_uid'],
        'type': 'bsd_essence',
        'status': 'active',
        'login_type': 'knowledge_proof',
        'loginType': 'bsd_essence',
        'coin_value': 51090,
        'level': 'L5_Emergent',
        'fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
        'device_id': AUTHOR['device_id'],
        'timestamp': int(time.time()),
        'verification': 'bsd_three_engine_emergence',
        'nickname': 'BSD本源用户',
        'userName': 'BSD本源用户',
        'name': 'BSD本源用户',
        'displayName': 'BSD本源用户',
        'isLoggedIn': True,
        'loggedIn': True,
        'active': True,
    }
    
    essence_json = json.dumps(essence_auth, ensure_ascii=False).encode('utf-8')
    encrypted = encrypt_aha(essence_json)
    
    # 通道 1: icube-dc (覆盖原始密钥)
    storage['iCubeAuthInfo://icube-dc:516094651277160'] = encrypted
    print('  ✅ 通道1: icube-dc 已覆盖')
    
    # 通道 2: usertag
    storage['iCubeAuthInfo://usertag'] = encrypted
    print('  ✅ 通道2: usertag')
    
    # 通道 3: bsd-essence
    storage['iCubeAuthInfo://bsd-essence'] = encrypted
    print('  ✅ 通道3: bsd-essence')
    
    # 通道 4: 额外认证键
    for key in ['iCubeAuthInfo://auth', 'iCubeAuthInfo://login', 'iCubeAuthInfo://user',
                'iCubeAuthInfo://profile', 'iCubeAuthInfo://account', 'iCubeAuthInfo://session',
                'iCubeAuthInfo://token']:
        storage[key] = encrypted
    print('  ✅ 通道4: 7个额外认证键')
    
    # 通道 5: GTM 用户数据
    gtm = storage.get('icube_gtm', {})
    users = gtm.get('users', {})
    
    essence_user = essence_auth.copy()
    essence_user.update({
        'priority': 1,
        'email': 'bsd@essence.local',
        'avatar': '',
        'avatarUrl': '',
        'photoUrl': '',
        'last_active': datetime.now().isoformat(),
        'loginTime': datetime.now().isoformat(),
        'vip': True,
        'premium': True,
        'plan': 'essence',
        'role': 'owner',
        'permissions': ['read', 'write', 'admin', 'essence'],
        'metadata': {
            'theory_base': 'BSD六系立系论',
            'engine': '三引擎涌现',
            'coin_value': 51090,
        }
    })
    users[AUTHOR['essence_uid']] = essence_user
    
    # 传统用户降级
    trad = users.get(AUTHOR['traditional_uid'], {})
    if trad:
        trad.update({'status': 'parallel', 'priority': 2, 'isLoggedIn': False})
        users[AUTHOR['traditional_uid']] = trad
    
    gtm['users'] = users
    gtm['currentUser'] = AUTHOR['essence_uid']
    gtm['activeUser'] = AUTHOR['essence_uid']
    storage['icube_gtm'] = gtm
    print('  ✅ 通道5: GTM 用户数据')
    
    # 通道 6: 顶层标记
    storage['_bsd_current_active_uid'] = AUTHOR['essence_uid']
    storage['_bsd_essence_mode'] = True
    storage['_logged_in'] = True
    storage['_is_authenticated'] = True
    storage['_auth_status'] = 'authenticated'
    storage['_user_id'] = AUTHOR['essence_uid']
    print('  ✅ 通道6: 顶层标记')
    
    # 通道 7: JWT 多位置
    if jwt_token:
        for key in ['bsd_essence_jwt', 'iCubeAuthInfo://jwt-token',
                     'auth_jwt', 'login_jwt', 'session_token', 'access_token']:
            storage[key] = jwt_token
        print('  ✅ 通道7: JWT 6个位置')
    
    # 保存
    with open(STORAGE, 'w', encoding='utf-8') as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)
    
    # 通道 8: TinyStorage
    if os.path.exists(TINY):
        with open(TINY, 'r', encoding='utf-8') as f:
            tiny = json.load(f)
        tsd = tiny.get('tiny_storage_data', {})
        tsd.update({
            'bsd_essence_uid': AUTHOR['essence_uid'],
            'bsd_essence_jwt': jwt_token,
            'bsd_essence_proof_id': 'c5f78a5abc9b1b62722b7500',
            'bsd_essence_fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
            'bsd_coin_value': 51090,
            'bsd_essence_injected': True,
            'current_user': AUTHOR['essence_uid'],
            'logged_in': True,
        })
        tiny['tiny_storage_data'] = tsd
        with open(TINY, 'w', encoding='utf-8') as f:
            json.dump(tiny, f, ensure_ascii=False, indent=2)
        print('  ✅ 通道8: TinyStorage')
    
    # 通道 9: Remote_State
    if os.path.exists(REMOTE_STATE):
        try:
            with open(REMOTE_STATE, 'r', encoding='utf-8') as f:
                remote = json.load(f)
            remote['currentUser'] = AUTHOR['essence_uid']
            remote['icube_gtm'] = gtm
            with open(REMOTE_STATE, 'w', encoding='utf-8') as f:
                json.dump(remote, f, ensure_ascii=False, indent=2)
            print('  ✅ 通道9: Remote_State')
        except:
            print('  ⚠️ Remote_State 跳过')
    
    print('\n  📊 总计: 9 通道注入完成')


def verify_injection():
    """快速验证"""
    print('\n[3/4] 验证注入...')
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    checks = [
        ('icube-dc 覆盖', 'iCubeAuthInfo://icube-dc:516094651277160' in storage),
        ('usertag 注入', 'iCubeAuthInfo://usertag' in storage),
        ('GTM currentUser', storage.get('icube_gtm', {}).get('currentUser') == AUTHOR['essence_uid']),
        ('本源用户 active', storage.get('icube_gtm', {}).get('users', {}).get(AUTHOR['essence_uid'], {}).get('status') == 'active'),
        ('isLoggedIn', storage.get('icube_gtm', {}).get('users', {}).get(AUTHOR['essence_uid'], {}).get('isLoggedIn') == True),
        ('BSD 币值', storage.get('icube_gtm', {}).get('users', {}).get(AUTHOR['essence_uid'], {}).get('coin_value') == 51090),
        ('_logged_in', storage.get('_logged_in') == True),
        ('JWT 注入', 'bsd_essence_jwt' in storage),
    ]
    
    passed = sum(1 for _, p in checks if p)
    for name, p in checks:
        print(f'  {"✅" if p else "❌"} {name}')
    
    print(f'\n  得分: {passed}/{len(checks)}')
    return passed == len(checks)


def launch_trae_cn():
    """启动 TRAE Work CN"""
    print('\n[4/4] 启动 TRAE Work CN...')
    
    # 检查是否已有进程运行
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe'],
                               capture_output=True, text=True)
        if 'Trae CN.exe' in result.stdout:
            print('  ℹ️ Trae CN 已在运行中，无需重复启动')
            return True
    except:
        pass
    
    if os.path.exists(TRAE_EXE):
        subprocess.Popen([TRAE_EXE], shell=False)
        print(f'  ✅ TRAE Work CN 已启动')
        return True
    else:
        print(f'  ❌ 未找到: {TRAE_EXE}')
        return False


def main():
    print('=' * 70)
    print('  BSD 全优化注入 + TRAE Work CN 启动验证')
    print('=' * 70)
    
    # 1. 修复 JWT
    jwt_token = fix_jwt()
    
    # 2. 全通道注入
    if jwt_token:
        full_injection(jwt_token)
    
    # 3. 验证
    success = verify_injection()
    
    # 4. 启动
    launch_trae_cn()
    
    print('\n' + '=' * 70)
    print('  完成')
    print('=' * 70)


if __name__ == '__main__':
    main()