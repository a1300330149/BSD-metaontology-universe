#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trae CN 认证流程调试 V2 — 正确分离认证网关和API服务器
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

# 正确分离：认证网关 vs API服务器
AUTH_BASE = 'https://api.trae.cn'  # 认证网关
API_BASE = 'https://trae-api-cn.mchost.guru'  # API服务器

# 创建cookie jar和opener
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)

print(f'=== Trae CN 认证流程调试 V2 ===')
print(f'userId: {userId}')
print(f'认证网关: {AUTH_BASE}')
print(f'API服务器: {API_BASE}')

# Step 1: 向认证网关发送CheckLogin
print(f'\n--- Step 1: POST {AUTH_BASE}/cloudide/api/v3/trae/CheckLogin ---')
try:
    body = json.dumps({
        'UID': userId,
        'LoginType': 'jwt',
        'ClientID': '7o2d89p7dr1bo4',
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/cloudide/api/v3/trae/CheckLogin',
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
        
        # 保存aiHost用于后续请求
        ai_host = d.get('data', {}).get('aiHost', '')
        if ai_host:
            print(f'\n💡 发现aiHost: {ai_host}')
    except:
        print('JSON解析失败')
        
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(f'错误响应: {e.read().decode()[:500]}')
except Exception as e:
    print(f'错误: {e}')

# Step 2: 如果未登录，尝试LoginByJwt
print(f'\n--- Step 2: POST {AUTH_BASE}/cloudide/api/v3/trae/LoginByJwt ---')
try:
    body = json.dumps({
        'UID': userId,
        'LoginType': 'jwt',
        'ClientID': '7o2d89p7dr1bo4',
        'jwtToken': jwt_token,
        'refreshToken': refresh_token,
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/cloudide/api/v3/trae/LoginByJwt',
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
    
    try:
        d = json.loads(resp_text)
        print(f'登录状态: {d.get("data", {}).get("isLogin", "N/A")}')
        print(f'code: {d.get("code", "N/A")}')
        # 检查是否有token返回
        if 'data' in d and isinstance(d['data'], dict):
            new_token = d['data'].get('token', '')
            if new_token:
                print(f'新token: {new_token[:50]}...')
    except:
        print('JSON解析失败')
        
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}')
    print(f'错误响应: {e.read().decode()[:500]}')
except Exception as e:
    print(f'错误: {e}')

# Step 3: 尝试其他可能的认证路径
print(f'\n--- Step 3: 尝试其他认证路径 ---')
alt_paths = [
    f'{AUTH_BASE}/api/v3/trae/CheckLogin',
    f'{AUTH_BASE}/trae/api/v3/trae/CheckLogin',
    f'{AUTH_BASE}/cloudide/api/v1/auth/login',
]

for path in alt_paths:
    try:
        body = json.dumps({
            'UID': userId,
        }).encode()
        
        req = urllib.request.Request(
            path,
            data=body,
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'TraeCN/2.3.62837',
                'Authorization': f'Bearer {jwt_token}',
            },
            method='POST'
        )
        
        resp = opener.open(req, timeout=5)
        resp_text = resp.read().decode('utf-8')
        print(f'  {path.split("trae.cn")[1]}: HTTP {resp.status}')
        print(f'    响应: {resp_text[:200]}')
        
    except urllib.error.HTTPError as e:
        print(f'  {path.split("trae.cn")[1]}: HTTP {e.code}')
    except Exception as e:
        print(f'  {path.split("trae.cn")[1]}: {str(e)[:50]}')

# Step 4: 用api.trae.cn的session请求真实API
print(f'\n--- Step 4: 用认证后的session请求API服务器 ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
    }).encode()
    
    req = urllib.request.Request(
        f'{API_BASE}/api/ide/v2/llm_raw_chat',
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

# Step 5: 尝试从api.trae.cn直接请求llm_raw_chat（可能api.trae.cn会转发）
print(f'\n--- Step 5: 直接通过认证网关请求llm_raw_chat ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/api/ide/v2/llm_raw_chat',
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
