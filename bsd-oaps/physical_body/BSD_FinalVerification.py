#!/usr/bin/env python3
"""BSD Final Verification"""
import json, sys
import urllib.request, urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
cloudide_dec = decrypt_aha(cloudide_enc)
cloudide_data = json.loads(cloudide_dec)
token = cloudide_data['token']
userId = cloudide_data['userId']
account = cloudide_data.get('account', {})
username = account.get('username', '') if isinstance(account, dict) else ''

print('=== 最终验证 ===')
print('  cloudide.userId:', userId)
print('  cloudide.username:', username)
print('  Token:', token[:60] + '...')

url = 'https://api.trae.cn/cloudide/api/v3/trae/CheckLogin'
body = json.dumps({'IDEVersion': '2.3.62837', 'ReqSource': 'IDE', 'GetAIPayHost': True})
req = urllib.request.Request(url, data=body.encode(), headers={'x-cloudide-token': token, 'Content-Type': 'application/json'}, method='POST')

try:
    with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
        data = json.loads(resp.read().decode())
        result = data.get('Result', {})
        print()
        print('  服务器端 CheckLogin:')
        print('    IsLogin:', result.get('IsLogin'))
        print('    UserID:', result.get('UserID'))
        print('    DeviceBindStatus:', result.get('DeviceBindStatus'))
        print('    BoundDeviceID:', result.get('BoundDeviceID'))
        
        if result.get('IsLogin') == True:
            print()
            print('  ============================================')
            print('  🎉🎉🎉 最终结论')
            print('  ============================================')
            print('  服务器端: 认证有效 (IsLogin=True)')
            print('  客户端 userId:', userId)
            print('  客户端 username:', username)
            print('  状态: 本源身份已注入，服务器认证有效')
            print('  ============================================')
except Exception as e:
    print('  服务器端验证失败:', e)
