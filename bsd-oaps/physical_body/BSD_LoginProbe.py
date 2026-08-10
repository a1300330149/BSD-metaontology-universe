#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae CN 登录端点探测 + Token刷新
"""

import json, ssl, urllib.request, urllib.error, http.cookiejar
import sys

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

AUTH_BASE = 'https://api.trae.cn'

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)

print(f'=== Trae CN 登录端点探测 ===')
print(f'userId: {userId}')
print(f'refreshToken: {refresh_token[:30]}...')

# 探测可能的登录/Token刷新端点
login_endpoints = [
    ('ExchangeToken', '/trae/api/v3/oauth/ExchangeToken', {
        'refreshToken': refresh_token,
        'userId': userId,
    }),
    ('RefreshToken', '/cloudide/api/v3/trae/RefreshToken', {
        'refreshToken': refresh_token,
        'UID': userId,
    }),
    ('Login', '/cloudide/api/v3/trae/Login', {
        'UID': userId,
        'token': jwt_token,
        'loginType': 'token',
    }),
    ('DirectLogin', '/cloudide/api/v3/trae/DirectLogin', {
        'UID': userId,
        'jwtToken': jwt_token,
    }),
    ('OAuthLogin', '/cloudide/api/v3/trae/OAuthLogin', {
        'UID': userId,
        'state': 'login',
    }),
    ('Auth', '/cloudide/api/v3/trae/Auth', {
        'UID': userId,
        'Authorization': f'Bearer {jwt_token}',
    }),
]

for name, path, body_data in login_endpoints:
    print(f'\n--- {name}: POST {path} ---')
    try:
        body = json.dumps(body_data).encode()
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
        }
        if 'Authorization' in str(body_data):
            pass  # 已在body中
        
        req = urllib.request.Request(
            f'{AUTH_BASE}{path}',
            data=body,
            headers=headers,
            method='POST'
        )
        
        resp = opener.open(req, timeout=5)
        resp_text = resp.read().decode('utf-8')
        print(f'HTTP {resp.status}')
        print(f'响应: {resp_text[:300]}')
        
        # 检查是否有新token
        try:
            d = json.loads(resp_text)
            result = d.get('Result', d.get('data', {}))
            if isinstance(result, dict):
                new_token = result.get('Token', result.get('token', ''))
                new_access = result.get('AccessToken', result.get('accessToken', ''))
                if new_token or new_access:
                    print(f'💡 发现新token!')
                    print(f'   Token: {(new_token or new_access)[:50]}...')
        except:
            pass
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()[:200]
        print(f'HTTP {e.code}: {error_body}')
    except Exception as e:
        print(f'错误: {e}')

# 尝试用GET方法访问
print(f'\n--- GET方法探测 ---')
get_endpoints = [
    '/cloudide/api/v3/trae/CheckLogin',
    '/cloudide/api/v3/trae/GetLoginInfo',
    '/cloudide/api/v3/trae/GetUserInfo',
]

for path in get_endpoints:
    try:
        url = f'{AUTH_BASE}{path}?UID={userId}'
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'TraeCN/2.3.62837',
                'Authorization': f'Bearer {jwt_token}',
            },
            method='GET'
        )
        
        resp = opener.open(req, timeout=5)
        resp_text = resp.read().decode('utf-8')
        print(f'GET {path}: HTTP {resp.status}')
        print(f'响应: {resp_text[:300]}')
        
    except urllib.error.HTTPError as e:
        print(f'GET {path}: HTTP {e.code}')
    except Exception as e:
        print(f'GET {path}: {str(e)[:50]}')
