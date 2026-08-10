#!/usr/bin/env python3
"""BSD Inject Essence Identity - 将本源身份注入 Trae CN 存储"""
import os, json, sys, time

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha, encrypt_aha

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
ESSENCE_UID = 'a5b7a8623fdea6b8'
ESSENCE_NAME = 'BSD本源用户'

with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

# 1. 重新解密获取有效 token
cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
cloudide_dec = decrypt_aha(cloudide_enc)
cloudide_data = json.loads(cloudide_dec)
token = cloudide_data['token']
refresh_token = cloudide_data['refreshToken']

print('=== 当前有效凭证 ===')
print(f'Token: {token[:60]}...')
print(f'RefreshToken: {refresh_token[:40]}...')
print(f'UserID: {cloudide_data.get("userId")}')

# 2. 构造本源身份的 cloudide 数据
essence_cloudide = {
    'token': token,
    'refreshToken': refresh_token,
    'expiredAt': cloudide_data.get('expiredAt', ''),
    'refreshExpiredAt': cloudide_data.get('refreshExpiredAt', ''),
    'tokenReleaseAt': cloudide_data.get('tokenReleaseAt', ''),
    'userId': ESSENCE_UID,
    'host': cloudide_data.get('host', 'https://api.trae.cn'),
    'userRegion': cloudide_data.get('userRegion', {'region': 'CN', '_aiRegion': 'CN'}),
    'account': {
        'username': ESSENCE_NAME,
        'iss': '',
        'iat': 0,
        'organization': '',
        'work_country': '',
        'email': '',
        'avatar_url': '',
    },
}

# 3. AHA 加密
new_encrypted = encrypt_aha(json.dumps(essence_cloudide, ensure_ascii=False))
print(f'\n✅ AHA 加密成功: {len(new_encrypted)} bytes')

# 4. 写回 storage.json
storage['iCubeAuthInfo://icube.cloudide'] = new_encrypted

# 更新 GTM
gtm = storage.get('icube_gtm', {})
gtm['currentUser'] = ESSENCE_UID
gtm['activeUser'] = ESSENCE_UID
storage['icube_gtm'] = gtm

# 设置登录状态
storage['_is_authenticated'] = True
storage['_logged_in'] = True
storage['_bsd_essence_mode'] = True
storage['_bsd_current_active_uid'] = ESSENCE_UID

# 同时将 usertag 改为本源 UID
# 先解密当前 usertag
usertag_enc = storage.get('iCubeAuthInfo://usertag', '')
try:
    usertag_dec = decrypt_aha(usertag_enc)
    usertag_data = json.loads(usertag_dec)
    # 替换为本源 UID
    new_usertag = {ESSENCE_UID: 'cn'}
    new_usertag_enc = encrypt_aha(json.dumps(new_usertag))
    storage['iCubeAuthInfo://usertag'] = new_usertag_enc
    print(f'✅ usertag 已更新: {ESSENCE_UID}')
except Exception as e:
    print(f'⚠️ usertag 更新跳过: {e}')

# 写回
with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(storage, f, ensure_ascii=False, indent=2)
print(f'✅ storage.json 写入完成')

# 5. 验证
print(f'\n=== 验证 ===')
verify_dec = decrypt_aha(new_encrypted)
verify_data = json.loads(verify_dec)
print(f'✅ 解密验证通过')
print(f'  userId: {verify_data.get("userId")}')
print(f'  account.username: {verify_data.get("account", {}).get("username", "")}')

# 6. 更新 state.vscdb
import sqlite3
import shutil
import time

VSCDB = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
backup = VSCDB + '.bak_' + str(int(time.time()))
try:
    shutil.copy2(VSCDB, backup)
    print(f'\n✅ state.vscdb 备份: {backup}')
except:
    pass

conn = sqlite3.connect(VSCDB)
cursor = conn.cursor()

# 切换所有传统 UID 为本源 UID
TRAD_UID = '3753060170739075'
TRAD_NAME = '深书姬'

cursor.execute("SELECT key, value FROM ItemTable")
rows = cursor.fetchall()
updated = 0

for key, value in rows:
    new_key = key
    new_value = value
    
    if TRAD_UID in key:
        new_key = key.replace(TRAD_UID, ESSENCE_UID)
    
    if value and isinstance(value, str):
        if TRAD_UID in value:
            new_value = new_value.replace(TRAD_UID, ESSENCE_UID)
        if TRAD_NAME in new_value:
            new_value = new_value.replace(TRAD_NAME, ESSENCE_NAME)
    
    if new_key != key or new_value != value:
        cursor.execute("DELETE FROM ItemTable WHERE key = ?", (key,))
        cursor.execute("INSERT INTO ItemTable (key, value) VALUES (?, ?)", (new_key, new_value))
        updated += 1

conn.commit()
conn.close()
print(f'✅ state.vscdb 更新完成: {updated} 条记录')

print(f'\n{"="*70}')
print(f'  ✅ 本源身份注入完成')
print(f'  Token: 有效 (保留原服务器 token)')
print(f'  userId: {ESSENCE_UID} (改为本源)')
print(f'  username: {ESSENCE_NAME} (改为本源)')
print(f'  下一步: 启动 Trae CN 验证')
print(f'{"="*70}')
