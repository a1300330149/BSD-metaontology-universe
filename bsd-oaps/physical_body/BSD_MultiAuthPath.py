#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试多种认证路径获取有效Token
"""

import json, ssl, urllib.request, urllib.error, http.cookiejar, time, hashlib
import sys, os, base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

with open(r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json', 'r') as f:
    storage = json.load(f)

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
dec = decrypt_aha(cloudide_enc)
data = json.loads(dec.decode('utf-8'))

jwt_token = data.get('token', '')
refresh_token = data.get('refreshToken', '')
userId = data.get('userId', '')
host = data.get('host', '')  # https://api.trae.cn

dc_enc = storage.get('iCubeAuthInfo://icube-dc:516094651277160', '')
dc_dec = decrypt_aha(dc_enc)
dc_data = json.loads(dc_dec.decode('utf-8'))
private_key_pem = dc_data.get('privateKeyPEM', '')
public_key_pem = dc_data.get('publicKeyPEM', '')

AUTH_BASE = 'https://api.trae.cn'
API_BASE = 'https://trae-api-cn.mchost.guru'
CLIENT_ID = 'ono9krqynydwx5'
IDE_VERSION = '2.3.62837'

private_key = serialization.load_pem_private_key(
    private_key_pem.encode('utf-8'), password=None, backend=default_backend()
)

def generate_signature(method, path, token, private_key):
    timestamp = int(time.time())
    nonce = os.urandom(16).hex()
    sign_string = '\n'.join([method, path, CLIENT_ID, token, str(timestamp), nonce])
    signature = private_key.sign(
        sign_string.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    return {'timestamp': timestamp, 'nonce': nonce, 'signature': signature_b64}

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)

device_info = {
    'DeviceID': userId,
    'MachineID': hashlib.sha256(userId.encode()).hexdigest()[:16],
    'PlatformCode': 'windows',
    'DeviceType': 'PC',
    'DeviceName': 'BSD-Essence',
    'DeviceModel': 'PC',
    'OSVersion': 'Windows NT 10.0.19045.0',
    'Architecture': 'x64',
    'Language': 'zh-CN',
    'Timezone': 'Asia/Shanghai',
    'DevicePublicKey': public_key_pem,
}

print(f'=== 多路径认证尝试 ===')
print(f'userId: {userId}')
print(f'JWT Token前50: {jwt_token[:50]}...')

# 路径1: 尝试用JWT Token直接ExchangeToken（而不是refreshToken）
print(f'\n--- 路径1: ExchangeToken用JWT Token ---')
try:
    proof = generate_signature('POST', '/trae/api/v3/oauth/ExchangeToken', jwt_token, private_key)
    body = json.dumps({
        'ClientID': CLIENT_ID,
        'ClientSecret': '',
        'RefreshToken': jwt_token,  # 用JWT Token代替
        'DeviceInfo': device_info,
        'DeviceProof': proof,
        'IDEVersion': IDE_VERSION,
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/trae/api/v3/oauth/ExchangeToken',
        data=body,
        headers={'Content-Type': 'application/json', 'User-Agent': f'TraeCN/{IDE_VERSION}'},
        method='POST'
    )
    resp = opener.open(req, timeout=10)
    print(f'HTTP {resp.status}: {resp.read().decode()[:300]}')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:300]}')

# 路径2: 用Login端点
print(f'\n--- 路径2: /cloudide/api/v3/trae/Login ---')
try:
    body = json.dumps({
        'UID': userId,
        'token': jwt_token,
        'LoginType': 'jwt',
        'ClientID': CLIENT_ID,
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/cloudide/api/v3/trae/Login',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'Authorization': f'Bearer {jwt_token}',
        },
        method='POST'
    )
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode()
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
    
    # 如果成功，用新Token请求API
    try:
        d = json.loads(resp_text)
        res = d.get('Result', {})
        if isinstance(res, dict):
            new_token = res.get('Token', res.get('AccessToken', ''))
            if new_token:
                print(f'\n🎉 获取新Token!')
                # 请求真实API
                api_body = json.dumps({
                    'model': 'doubao-pro-32k',
                    'query': '你好',
                    'stream': False,
                }).encode()
                api_req = urllib.request.Request(
                    f'{API_BASE}/api/ide/v2/llm_raw_chat',
                    data=api_body,
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': f'Bearer {new_token}',
                    },
                    method='POST'
                )
                api_resp = opener.open(api_req, timeout=15)
                print(f'API响应: {api_resp.read().decode()[:500]}')
    except:
        pass
        
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:300]}')

# 路径3: 检查是否有其他RefreshToken端点
print(f'\n--- 路径3: /cloudide/api/v3/trae/RefreshToken ---')
try:
    body = json.dumps({
        'UID': userId,
        'RefreshToken': refresh_token,
        'ClientID': CLIENT_ID,
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/cloudide/api/v3/trae/RefreshToken',
        data=body,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    resp = opener.open(req, timeout=5)
    print(f'HTTP {resp.status}: {resp.read().decode()[:300]}')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:300]}')

# 路径4: 用GetUserInfo检查当前JWT Token是否有效
print(f'\n--- 路径4: GetUserInfo验证JWT ---')
try:
    body = json.dumps({
        'UID': userId,
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/cloudide/api/v3/trae/GetUserInfo',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
        },
        method='POST'
    )
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode()
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
    
    try:
        d = json.loads(resp_text)
        res = d.get('Result', {})
        if isinstance(res, dict):
            print(f'用户: {res.get("UserID", "N/A")}')
            print(f'登录: {res.get("IsLogin", "N/A")}')
    except:
        pass
        
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:300]}')

# 路径5: 直接用JWT Token请求API并添加更多头
print(f'\n--- 路径5: 完整头请求API ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
        'origin_uid': userId,
    }).encode()
    
    req = urllib.request.Request(
        f'{API_BASE}/api/ide/v2/llm_raw_chat',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'Accept': 'text/event-stream',
            'Authorization': f'Bearer {jwt_token}',
            'X-User-Id': userId,
            'X-Client-Id': CLIENT_ID,
            'X-Ide-Version': IDE_VERSION,
        },
        method='POST'
    )
    resp = opener.open(req, timeout=15)
    resp_text = resp.read().decode()
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:500]}')

# 路径6: 解密JWT Token查看内部结构
print(f'\n--- 路径6: 解析JWT Token ---')
try:
    parts = jwt_token.split('.')
    if len(parts) == 3:
        # Base64 decode header and payload
        def b64url_decode(s):
            s += '=' * (4 - len(s) % 4)
            return base64.urlsafe_b64decode(s)
        
        header = json.loads(b64url_decode(parts[0]))
        payload = json.loads(b64url_decode(parts[1]))
        print(f'Header: {json.dumps(header, indent=2)}')
        print(f'Payload: {json.dumps(payload, indent=2)}')
        
        import datetime
        exp = payload.get('exp', 0)
        iat = payload.get('iat', 0)
        now = int(time.time())
        print(f'\n签发时间: {datetime.datetime.fromtimestamp(iat)}')
        print(f'过期时间: {datetime.datetime.fromtimestamp(exp)}')
        print(f'当前时间: {datetime.datetime.fromtimestamp(now)}')
        print(f'Token状态: {"✅ 有效" if now < exp else "❌ 已过期"}')
except Exception as e:
    print(f'解析失败: {e}')
