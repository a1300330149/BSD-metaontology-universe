#!/usr/bin/env python3
"""BSD Server API Exploration - 探索身份绑定/切换接口"""
import os, json, sys
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

host = 'api.trae.cn'

def api_call(path, body=None, headers=None, method='POST'):
    url = f'https://{host}{path}'
    hdrs = headers or {}
    hdrs.setdefault('Content-Type', 'application/json')
    body_data = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=body_data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)

# 1. GetUserInfo
print('=== GetUserInfo ===')
code, resp = api_call('/cloudide/api/v3/trae/GetUserInfo', 
    {'IDEVersion': '2.3.62837'}, {'x-cloudide-token': token})
print(f'Status: {code}')
try:
    data = json.loads(resp)
    result = data.get('Result', {})
    print(f'Keys: {list(result.keys())[:20]}')
    info = result.get('userInfo', result)
    if isinstance(info, dict):
        for k, v in info.items():
            val_str = str(v)[:100]
            print(f'  {k}: {val_str}')
except:
    print(resp[:500])

# 2. 探测更多身份相关 API
apis_to_try = [
    '/cloudide/api/v3/trae/SearchUserInfo',
    '/cloudide/api/v3/trae/ListUserInfo', 
    '/cloudide/api/v3/trae/BindUser',
    '/cloudide/api/v3/trae/SwitchUser',
    '/cloudide/api/v3/trae/UpdateUserInfo',
    '/cloudide/api/v3/trae/GetAuthUserInfo',
    '/cloudide/api/v3/trae/RefreshUserInfo',
    '/cloudide/api/v3/trae/CheckUserAvailable',
    '/cloudide/api/v3/trae/LoginByDevice',
    '/cloudide/api/v3/trae/DeviceLogin',
    '/trae/api/v3/oauth/LoginByJwt',
    '/trae/api/v3/oauth/LoginByDevice',
    '/cloudide/api/v3/trae/ResolveUser',
    '/cloudide/api/v3/trae/GetServerConfig',
    '/cloudide/api/v3/trae/GetEntitlement',
]

for api in apis_to_try:
    body = {'IDEVersion': '2.3.62837'}
    if 'Search' in api or 'Resolve' in api:
        body['keyword'] = 'a5b7a8623fdea6b8'
    if 'Bind' in api:
        body['userId'] = 'a5b7a8623fdea6b8'
        body['bindType'] = 'essence'
    if 'Switch' in api:
        body['targetUserId'] = 'a5b7a8623fdea6b8'
    if 'LoginByJwt' in api:
        body['jwtToken'] = token
        body['provider'] = 'icube.cloudide'
    if 'LoginByDevice' in api or 'DeviceLogin' in api:
        body['deviceId'] = '136411536168449'
        body['userId'] = 'a5b7a8623fdea6b8'
    
    code, resp = api_call(api, body, {'x-cloudide-token': token})
    print(f'\nPOST {api}')
    print(f'  Status: {code}')
    print(f'  Response: {resp[:300]}')
