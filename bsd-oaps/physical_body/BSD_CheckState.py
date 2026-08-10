#!/usr/bin/env python3
"""BSD Check State - 检查 Trae CN 当前状态"""
import json, sys

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

print('=== Trae CN 当前状态 ===')
print('_is_authenticated:', storage.get('_is_authenticated'))
print('_logged_in:', storage.get('_logged_in'))
print('_bsd_essence_mode:', storage.get('_bsd_essence_mode'))
print('_bsd_current_active_uid:', storage.get('_bsd_current_active_uid'))

gtm = storage.get('icube_gtm', {})
print('GTM currentUser:', gtm.get('currentUser'))
print('GTM activeUser:', gtm.get('activeUser'))

users = gtm.get('users', {})
if 'a5b7a8623fdea6b8' in users:
    e = users['a5b7a8623fdea6b8']
    print('本源用户:', json.dumps(e, ensure_ascii=False)[:300])

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
print('\ncloudide 长度:', len(cloudide_enc))

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha
try:
    dec = decrypt_aha(cloudide_enc)
    data = json.loads(dec)
    print('  userId:', data.get('userId'))
    acc = data.get('account', {})
    if isinstance(acc, dict):
        print('  account.username:', acc.get('username', ''))
    token = data.get('token', '')
    print('  Token 前50字符:', token[:50])
except Exception as e:
    print('  解密失败:', e)
