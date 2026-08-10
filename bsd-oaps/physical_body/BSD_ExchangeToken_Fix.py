#!/usr/bin/env python3
"""BSD ExchangeToken - 尝试正确的设备 ID"""
import os, json, sys, time, hashlib
import urllib.request, urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

API_HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'
MACHINE_ID = '7df8ec0fa686402a409be1e0670678c87a0114ccc1e085e40ce5f7f4c464d679'

with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)
cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
cloudide_dec = decrypt_aha(cloudide_enc)
cloudide_data = json.loads(cloudide_dec)
token = cloudide_data['token']
refresh_token = cloudide_data['refreshToken']

def http_request(path, method='POST', data=None, headers=None, timeout=15):
    url = 'https://' + API_HOST + path
    hdrs = headers or {}
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)

timestamp = int(time.time())
nonce = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]

# 尝试不同的设备 ID
device_ids_to_try = [
    '3lq9jknd97kxqo',      # BoundDeviceID from CheckLogin
    MACHINE_ID,             # machineId from telemetry
    '136411536168449',      # 设备 ID
    '',                     # 空
]

print('=== ExchangeToken 设备匹配测试 ===')
for did in device_ids_to_try:
    body = {
        'ClientID': 'ono9krqynydwx5',
        'ClientSecret': '',
        'RefreshToken': refresh_token,
        'DeviceInfo': {
            'deviceId': did,
            'os': 'windows',
            'clientVersion': IDE_VERSION,
            'machineId': MACHINE_ID,
        },
        'DeviceProof': {
            'DeviceID': did,
            'Timestamp': timestamp,
            'Nonce': nonce,
            'Signature': '',
        },
        'IDEVersion': IDE_VERSION,
    }
    
    status, resp = http_request('/trae/api/v3/oauth/ExchangeToken', 'POST', body)
    try:
        data = json.loads(resp)
        err = data.get('ResponseMetadata', {}).get('Error', {})
        msg = err.get('Message', 'OK')
        code = err.get('Code', 'N/A')
        short_did = did[:20] if did else '(empty)'
        print(f'  deviceId={short_did} => HTTP:{status}, Code:{code}, Msg:{msg}')
        
        if status == 200:
            token_data = data.get('Token', data.get('token', ''))
            print(f'  🎉 成功! Token: {str(token_data)[:80]}...')
            # 用新 token 检查登录
            status2, resp2 = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST',
                {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True},
                {'x-cloudide-token': str(token_data)})
            print(f'  CheckLogin with new token: HTTP:{status2}')
            print(f'  Response: {resp2[:300]}')
    except:
        print(f'  deviceId={did[:20] if did else "empty"} => HTTP:{status}, Raw:{resp[:200]}')

# 尝试用 Access Token 直接调用 ExchangeToken (可能需要不同的认证)
print()
print('=== 尝试用 Access Token 作为认证 ===')
body = {
    'ClientID': 'ono9krqynydwx5',
    'ClientSecret': '',
    'RefreshToken': refresh_token,
    'DeviceInfo': {
        'deviceId': '3lq9jknd97kxqo',
        'os': 'windows',
        'clientVersion': IDE_VERSION,
        'machineId': MACHINE_ID,
    },
    'DeviceProof': {
        'DeviceID': '3lq9jknd97kxqo',
        'Timestamp': timestamp,
        'Nonce': nonce,
        'Signature': '',
    },
    'IDEVersion': IDE_VERSION,
}

status, resp = http_request('/trae/api/v3/oauth/ExchangeToken', 'POST', body,
    {'x-cloudide-token': token, 'Content-Type': 'application/json'})
print(f'  With token header => HTTP:{status}')
try:
    data = json.loads(resp)
    print(f'  Response: {json.dumps(data, ensure_ascii=False)[:400]}')
except:
    print(f'  Raw: {resp[:300]}')
