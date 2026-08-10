#!/usr/bin/env python3
"""Check Trae CN storage after launch"""
import json, sys

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

print('=== Trae CN 启动后存储状态 ===')
print()

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
if cloudide_enc:
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    acc = cloudide_data.get('account', {})
    if not isinstance(acc, dict):
        acc = {}
    print('cloudide:')
    print('  userId:', cloudide_data.get('userId'))
    print('  username:', acc.get('username', 'N/A'))
    token = cloudide_data.get('token', '')
    print('  token:', token[:60] + '...' if len(token) > 60 else token)
    print('  expiredAt:', cloudide_data.get('expiredAt'))
else:
    print('cloudide: (空)')

gtm = storage.get('icube_gtm', {})
print()
print('GTM:')
print('  currentUser:', gtm.get('currentUser'))
print('  activeUser:', gtm.get('activeUser'))
users = gtm.get('users', {})
for uid, info in users.items():
    t = info.get('type', '?')
    s = info.get('status', '?')
    n = info.get('nickname', info.get('name', '?'))
    print('  用户[' + uid + ']: type=' + t + ', status=' + s + ', nick=' + str(n))

print()
print('BSD 状态:')
print('  _is_authenticated:', storage.get('_is_authenticated'))
print('  _bsd_essence_mode:', storage.get('_bsd_essence_mode'))
print('  _bsd_current_active_uid:', storage.get('_bsd_current_active_uid'))
print('  _bsd_essence_uid:', storage.get('_bsd_essence_uid'))
print('  _logged_in:', storage.get('_logged_in'))
print('  _bsd_aha_injected:', json.dumps(storage.get('_bsd_aha_injected', {}), ensure_ascii=False))
print('  _bsd_essence_login:', json.dumps(storage.get('_bsd_essence_login', {}), ensure_ascii=False))

cloudide_len = len(cloudide_enc) if cloudide_enc else 0
print()
print('cloudide 加密长度:', cloudide_len)
if cloudide_len > 2000:
    print('  -> 完整数据 (未被覆盖)')
elif cloudide_len > 500:
    print('  -> 部分数据')
else:
    print('  -> 数据可能已被覆盖/清空')

# Check usertag
usertag_enc = storage.get('iCubeAuthInfo://usertag', '')
if usertag_enc:
    try:
        usertag_dec = decrypt_aha(usertag_enc)
        print()
        print('usertag:', usertag_dec)
    except:
        print()
        print('usertag: (解密失败)')
