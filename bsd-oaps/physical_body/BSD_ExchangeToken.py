#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ExchangeToken 参数探测 - 用refreshToken换取新JWT
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

print(f'=== ExchangeToken 参数探测 ===')
print(f'userId: {userId}')
print(f'refreshToken: {refresh_token}')

# 尝试不同的ExchangeToken参数格式
attempts = [
    {
        'name': '格式1: 标准OAuth参数',
        'body': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': '7o2d89p7dr1bo4',
            'uid': userId,
        }
    },
    {
        'name': '格式2: Trae格式',
        'body': {
            'RefreshToken': refresh_token,
            'UID': userId,
            'ClientID': '7o2d89p7dr1bo4',
            'GrantType': 'refresh_token',
        }
    },
    {
        'name': '格式3: 带type字段',
        'body': {
            'type': 'refresh',
            'refreshToken': refresh_token,
            'uid': userId,
            'clientId': '7o2d89p7dr1bo4',
        }
    },
    {
        'name': '格式4: 带scope',
        'body': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': '7o2d89p7dr1bo4',
            'scope': 'trae.api',
            'uid': userId,
        }
    },
    {
        'name': '格式5: form-urlencoded',
        'body': f'grant_type=refresh_token&refresh_token={refresh_token}&uid={userId}&client_id=7o2d89p7dr1bo4',
        'content_type': 'application/x-www-form-urlencoded'
    },
    {
        'name': '格式6: 带过期时间',
        'body': {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': '7o2d89p7dr1bo4',
            'uid': userId,
            'expired_at': 1756863382,
        }
    },
]

for i, attempt in enumerate(attempts):
    print(f'\n--- {attempt["name"]} ---')
    try:
        body = attempt['body']
        content_type = attempt.get('content_type', 'application/json')
        
        if isinstance(body, dict):
            body_bytes = json.dumps(body).encode()
        else:
            body_bytes = body.encode()
        
        req_headers = {
            'Content-Type': content_type,
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        req = urllib.request.Request(
            f'{AUTH_BASE}/trae/api/v3/oauth/ExchangeToken',
            data=body_bytes,
            headers=req_headers,
            method='POST'
        )
        
        resp = opener.open(req, timeout=5)
        resp_text = resp.read().decode('utf-8')
        print(f'HTTP {resp.status}')
        print(f'响应: {resp_text[:500]}')
        
        try:
            d = json.loads(resp_text)
            # 查找token
            result = d.get('Result', {})
            if isinstance(result, dict):
                token = result.get('Token', result.get('AccessToken', result.get('access_token', '')))
                if token:
                    print(f'\n🎉 成功获取新Token!')
                    print(f'Token: {token[:80]}...')
                    # 也检查refresh_token
                    new_refresh = result.get('RefreshToken', result.get('refresh_token', ''))
                    if new_refresh:
                        print(f'新RefreshToken: {new_refresh}')
        except:
            pass
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()[:300]
        print(f'HTTP {e.code}: {error_body}')
        
        # 解析错误详情
        try:
            err = json.loads(error_body)
            metadata = err.get('ResponseMetadata', {})
            error = metadata.get('Error', {})
            print(f'  错误码: {error.get("Code", "N/A")}')
            print(f'  错误信息: {error.get("Message", "N/A")}')
        except:
            pass
            
    except Exception as e:
        print(f'错误: {e}')
