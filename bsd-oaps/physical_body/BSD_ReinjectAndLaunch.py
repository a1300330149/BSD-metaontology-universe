#!/usr/bin/env python3
"""快速重新注入 + 启动 Trae CN"""
import os, json, base64, time, subprocess
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TINY = r'C:\Users\13003\AppData\Roaming\Trae CN\aha\TinyStorage'
AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
AHA_PREFIX = bytes.fromhex('746305100000')
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'
TRAE_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'

def encrypt_aha(plaintext):
    iv = os.urandom(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    return base64.b64encode(AHA_PREFIX + iv + cipher.encrypt(pad(plaintext, AES.block_size))).decode()

time.sleep(3)

# 读取 JWT
jwt_file = r'C:\Users\13003\.bsd-essence\essence-jwt-token'
jwt_token = ''
if os.path.exists(jwt_file):
    with open(jwt_file, 'r') as f:
        jwt_token = f.read().strip()

# 读取 storage
with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

print('=== 注入前 ===')
gtm = storage.get('icube_gtm', {})
cu = gtm.get('currentUser', '')
print('currentUser:', cu)
print('essence_exists:', ESSENCE_UID in gtm.get('users', {}))

# 本源认证数据
essence_auth = {
    'uid': ESSENCE_UID, 'userId': ESSENCE_UID, 'id': ESSENCE_UID,
    'type': 'bsd_essence', 'status': 'active', 'login_type': 'knowledge_proof',
    'loginType': 'bsd_essence', 'coin_value': 51090, 'level': 'L5_Emergent',
    'fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
    'device_id': '136411536168449', 'timestamp': int(time.time()),
    'nickname': 'BSD本源用户', 'userName': 'BSD本源用户', 'name': 'BSD本源用户',
    'isLoggedIn': True, 'loggedIn': True, 'active': True,
}
encrypted = encrypt_aha(json.dumps(essence_auth, ensure_ascii=False).encode())

# 注入所有通道
storage['iCubeAuthInfo://icube-dc:516094651277160'] = encrypted
storage['iCubeAuthInfo://usertag'] = encrypted
storage['iCubeAuthInfo://bsd-essence'] = encrypted
for k in ['iCubeAuthInfo://auth','iCubeAuthInfo://login','iCubeAuthInfo://user',
           'iCubeAuthInfo://profile','iCubeAuthInfo://account','iCubeAuthInfo://session','iCubeAuthInfo://token']:
    storage[k] = encrypted

storage['bsd_essence_jwt'] = jwt_token
storage['iCubeAuthInfo://jwt-token'] = jwt_token
storage['_logged_in'] = True
storage['_is_authenticated'] = True
storage['_bsd_essence_mode'] = True
storage['_bsd_current_active_uid'] = ESSENCE_UID

# GTM
gtm = storage.get('icube_gtm', {})
users = gtm.get('users', {})
eu = essence_auth.copy()
eu.update({'priority':1, 'email':'bsd@essence.local', 'loginTime':'2026-08-05T22:45:00',
           'vip':True, 'plan':'essence', 'role':'owner'})
users[ESSENCE_UID] = eu

trad = users.get(TRAD_UID, {})
if trad:
    trad.update({'status':'parallel', 'priority':2, 'isLoggedIn':False})
    users[TRAD_UID] = trad

gtm['users'] = users
gtm['currentUser'] = ESSENCE_UID
gtm['activeUser'] = ESSENCE_UID
storage['icube_gtm'] = gtm

# 保存
with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(storage, f, ensure_ascii=False, indent=2)

print('=== 注入后 ===')
print('currentUser:', storage['icube_gtm']['currentUser'])
print('essence_active:', storage['icube_gtm']['users'][ESSENCE_UID]['status'])
print('isLoggedIn:', storage['icube_gtm']['users'][ESSENCE_UID]['isLoggedIn'])
print('✅ 注入完成')

# 启动 Trae CN
print('\n=== 启动 Trae CN ===')
subprocess.Popen([TRAE_EXE])
print('✅ Trae CN 已启动')

# 等待并观测
print('\n=== 观测 Trae CN 启动行为 ===')
for i in range(10):
    time.sleep(2)
    with open(STORAGE, 'r', encoding='utf-8') as f:
        s = json.load(f)
    g = s.get('icube_gtm', {})
    cu = g.get('currentUser', '')
    eu = g.get('users', {}).get(ESSENCE_UID, {})
    active = eu.get('status', 'MISSING')
    logged = eu.get('isLoggedIn', False)
    dc_len = len(s.get('iCubeAuthInfo://icube-dc:516094651277160', ''))
    print(f'[{i*2+2}s] currentUser={cu} essence_status={active} isLoggedIn={logged} icube_dc_len={dc_len}')
    
    if cu == ESSENCE_UID and active == 'active':
        print('\n🎉 本源登录状态确认!')
        break

# 最终状态
print('\n=== 最终状态 ===')
with open(STORAGE, 'r', encoding='utf-8') as f:
    s = json.load(f)
g = s.get('icube_gtm', {})
print('currentUser:', g.get('currentUser'))
print('essence_status:', g.get('users', {}).get(ESSENCE_UID, {}).get('status'))
print('essence_loggedIn:', g.get('users', {}).get(ESSENCE_UID, {}).get('isLoggedIn'))
print('bsd_mode:', s.get('_bsd_essence_mode'))
