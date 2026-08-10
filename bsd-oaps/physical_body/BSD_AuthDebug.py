#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae CN 认证流程调试脚本
"""

import json, ssl, urllib.request, urllib.error, http.cookiejar
import sys

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# 加载凭据
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

TRUE_API_BASE = 'https://trae-api-cn.mchost.guru'

# 创建cookie jar和opener
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)

print(f'=== Trae CN 认证流程调试 ===')
print(f'userId: {userId}')
print(f'token前30: {jwt_token[:30]}...')

# Step 1: 访问根路径
print(f'\n--- Step 1: GET / ---')
try:
    req = urllib.request.Request(
        f'{TRUE_API_BASE}/',
        headers={'User-Agent': 'TraeCN/2.3.62837'},
        method='GET'
    )
    resp = opener.open(req, timeout=10)
    print(f'HTTP {resp.status}')
    print(f'Cookies: {len(list(cookie_jar))}')
    for c in cookie_jar:
        print(f'  {c.name}: {c.value[:30]}...')
except Exception as e:
    print(f'错误: {e}')

# Step 2: CheckLogin
print(f'\n--- Step 2: POST /cloudide/api/v3/trae/CheckLogin ---')
try:
    body = json.dumps({
        'UID': userId,
        'LoginType': 'jwt',
        'ClientID': '7o2d89p7dr1bo4',
    }).encode()
    
    req = urllib.request.Request(
        f'{TRUE_API_BASE}/cloudide/api/v3/trae/CheckLogin',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'Authorization': f'Bearer {jwt_token}',
        },
        method='POST'
    )
    
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode('utf-8')
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
    
    try:
        d = json.loads(resp_text)
        print(f'isLogin: {d.get("data", {}).get("isLogin", "N/A")}')
        print(f'aiHost: {d.get("data", {}).get("aiHost", "N/A")}')
        print(f'code: {d.get("code", "N/A")}')
    except:
        print('JSON解析失败')
        
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(f'错误响应: {e.read().decode()[:500]}')
except Exception as e:
    print(f'错误: {e}')

# Step 3: LoginByJwt
print(f'\n--- Step 3: POST /cloudide/api/v3/trae/LoginByJwt ---')
try:
    body = json.dumps({
        'UID': userId,
        'LoginType': 'jwt',
        'ClientID': '7o2d89p7dr1bo4',
        'jwtToken': jwt_token,
        'refreshToken': refresh_token,
    }).encode()
    
    req = urllib.request.Request(
        f'{TRUE_API_BASE}/cloudide/api/v3/trae/LoginByJwt',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
        },
        method='POST'
    )
    
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode('utf-8')
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
    
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(f'错误响应: {e.read().decode()[:500]}')
except Exception as e:
    print(f'错误: {e}')

# Step 4: 直接请求llm_raw_chat
print(f'\n--- Step 4: POST /api/ide/v2/llm_raw_chat ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
        'origin_uid': 'a5b7a8623fdea6b8',
    }).encode()
    
    req = urllib.request.Request(
        f'{TRUE_API_BASE}/api/ide/v2/llm_raw_chat',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'Accept': 'text/event-stream',
            'Authorization': f'Bearer {jwt_token}',
        },
        method='POST'
    )
    
    resp = opener.open(req, timeout=15)
    resp_text = resp.read().decode('utf-8')
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
    
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(f'错误响应: {e.read().decode()[:500]}')
except Exception as e:
    print(f'错误: {e}')
