#!/usr/bin/env python3
"""BSD Inject Essence Identity V2 - 含 AHA 加密实现"""
import os, json, sys, base64, hashlib, time, sqlite3, shutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha, CM, VW, KD, TI, AI, jee, Wee, sha512, hie, nee

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
VSCDB = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
ESSENCE_UID = 'a5b7a8623fdea6b8'
ESSENCE_NAME = 'BSD本源用户'
TRAD_UID = '3753060170739075'
TRAD_NAME = '深书姬'


def encrypt_aha(plaintext_bytes):
    """AHA 加密 — 与 decrypt_aha 对称"""
    import struct
    
    # 1. 计算数据哈希
    data_hash = sha512(plaintext_bytes)  # 64 bytes
    
    # 2. 组合: [64字节哈希][实际数据]
    combined = data_hash + plaintext_bytes
    
    # 3. 生成 32 字节随机密钥材料
    key_material = os.urandom(VW)
    
    # 4. 派生 AES 密钥和 IV
    aes_key, iv = nee(key_material)
    
    # 5. AES-128-CBC 加密
    padded = pad(combined, AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded)
    
    # 6. 组合: [6字节前缀][32字节密钥材料][密文]
    prefix = bytes([116, 99, 5, 16, 0, 0])  # 746305100000
    raw = prefix + key_material + ciphertext
    
    # 7. Base64 编码
    return base64.b64encode(raw).decode('utf-8')


# ============ 主流程 ============
print('='*70)
print('  BSD Inject Essence Identity V2')
print('='*70)

# 1. 加载并解密当前凭证
with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
cloudide_dec = decrypt_aha(cloudide_enc)
cloudide_data = json.loads(cloudide_dec)
token = cloudide_data['token']
refresh_token = cloudide_data['refreshToken']

print(f'\n✅ 解密凭证: userId={cloudide_data.get("userId")}')
print(f'   Token: {token[:50]}...')

# 2. 构造本源身份数据
essence_data = {
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

essence_json = json.dumps(essence_data, ensure_ascii=False)
print(f'\n本源数据: {essence_json[:300]}...')

# 3. AHA 加密
new_encrypted = encrypt_aha(essence_json.encode('utf-8'))
print(f'\n✅ AHA 加密: {len(new_encrypted)} chars')

# 4. 验证加密-解密一致性
verify = decrypt_aha(new_encrypted)
verify_data = json.loads(verify)
print(f'✅ 解密验证: userId={verify_data.get("userId")}, username={verify_data.get("account", {}).get("username")}')

# 5. 更新 storage.json
storage['iCubeAuthInfo://icube.cloudide'] = new_encrypted

# 更新 GTM
gtm = storage.get('icube_gtm', {})
gtm['currentUser'] = ESSENCE_UID
gtm['activeUser'] = ESSENCE_UID
storage['icube_gtm'] = gtm

# 设置本源登录状态
storage['_is_authenticated'] = True
storage['_logged_in'] = True
storage['_bsd_essence_mode'] = True
storage['_bsd_current_active_uid'] = ESSENCE_UID

# 更新 usertag
usertag_data = {ESSENCE_UID: 'cn'}
usertag_json = json.dumps(usertag_data)
new_usertag = encrypt_aha(usertag_json.encode('utf-8'))
storage['iCubeAuthInfo://usertag'] = new_usertag
print(f'✅ usertag 已更新: {ESSENCE_UID}')

with open(STORAGE, 'w', encoding='utf-8') as f:
    json.dump(storage, f, ensure_ascii=False, indent=2)
print(f'✅ storage.json 写入完成')

# 6. 更新 state.vscdb
backup = VSCDB + '.bak_' + str(int(time.time()))
try:
    shutil.copy2(VSCDB, backup)
    print(f'\n✅ state.vscdb 备份: {backup}')
except Exception as e:
    print(f'\n⚠️ 备份失败: {e}')

conn = sqlite3.connect(VSCDB)
cursor = conn.cursor()

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
print(f'✅ state.vscdb 更新: {updated} 条记录')

# 7. 验证
print(f'\n{"="*70}')
print(f'  ✅ 完成')
print(f'  cloudide.userId: {ESSENCE_UID}')
print(f'  cloudide.username: {ESSENCE_NAME}')
print(f'  Token: {token[:50]}...（有效服务器 token 保留）')
print(f'  下一步: 启动 Trae CN')
print(f'{"="*70}')
