#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
绕过认证网关 - 直接用JWT Token访问API服务器
添加所有可能需要的头信息
"""

import json, ssl, urllib.request, urllib.error, http.cookiejar, time, hashlib
import sys, os, base64

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
userId = data.get('userId', '')

# 解析JWT获取tenant_id
parts = jwt_token.split('.')
def b64url_decode(s):
    s += '=' * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)
payload = json.loads(b64url_decode(parts[1]))
tenant_id = payload['data']['tenant_id']

API_BASE = 'https://trae-api-cn.mchost.guru'
AUTH_BASE = 'https://api.trae.cn'
IDE_VERSION = '2.3.62837'

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)

print(f'=== 直接API访问尝试 ===')
print(f'userId: {userId}')
print(f'tenant_id: {tenant_id}')

# 尝试1: 用完整头访问llm_raw_chat
print(f'\n--- 尝试1: 完整认证头 ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
        'origin_uid': userId,
        'tenant_id': tenant_id,
    }).encode()
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
        'Authorization': f'Bearer {jwt_token}',
        'X-User-Id': userId,
        'X-Tenant-Id': tenant_id,
        'X-Ide-Version': IDE_VERSION,
        'X-Request-Id': hashlib.md5(f'{userId}{time.time()}'.encode()).hexdigest(),
        'X-Client-Type': 'trae-cn',
        'X-Client-Version': IDE_VERSION,
        'Accept': 'text/event-stream',
        'Origin': 'https://trae.cn',
        'Referer': 'https://trae.cn/',
    }
    
    req = urllib.request.Request(
        f'{API_BASE}/api/ide/v2/llm_raw_chat',
        data=body,
        headers=headers,
        method='POST'
    )
    resp = opener.open(req, timeout=15)
    resp_text = resp.read().decode()
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:800]}')
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:500]}')

# 尝试2: 使用不同的API端点
print(f'\n--- 尝试2: 其他API端点 ---')
endpoints = [
    '/api/v2/llm_raw_chat',
    '/api/v1/llm_raw_chat',
    '/api/ide/v2/chat',
    '/api/ide/v1/chat',
    '/cloudide/api/v3/trae/Chat',
    '/trae/api/v3/chat',
    '/api/chat/completions',
    '/v1/chat/completions',
]

for ep in endpoints:
    try:
        body = json.dumps({
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好，请回复OK'}],
            'stream': False,
        }).encode()
        
        req = urllib.request.Request(
            f'{API_BASE}{ep}',
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {jwt_token}',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
            },
            method='POST'
        )
        resp = opener.open(req, timeout=5)
        resp_text = resp.read().decode()
        print(f'  {ep}: HTTP {resp.status} - {resp_text[:150]}')
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:150]
        print(f'  {ep}: HTTP {e.code} - {err}')
    except Exception as e:
        print(f'  {ep}: 错误 - {str(e)[:100]}')

# 尝试3: 先访问认证网关设置cookie，再访问API
print(f'\n--- 尝试3: Cookie会话方式 ---')
try:
    # 先访问认证网关根路径获取cookie
    req = urllib.request.Request(
        f'{AUTH_BASE}/',
        headers={'User-Agent': f'TraeCN/{IDE_VERSION}'},
        method='GET'
    )
    resp = opener.open(req, timeout=5)
    print(f'认证网关根路径: HTTP {resp.status}')
    print(f'获取Cookie数量: {len(list(cookie_jar))}')
    for c in cookie_jar:
        print(f'  {c.name}: {c.value[:30]}...')
    
    # 然后用cookie+token访问CheckLogin
    body = json.dumps({
        'UID': userId,
        'LoginType': 'jwt',
    }).encode()
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/cloudide/api/v3/trae/CheckLogin',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        },
        method='POST'
    )
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode()
    print(f'\nCheckLogin: HTTP {resp.status}')
    print(f'响应: {resp_text[:300]}')
    
    # 再用session访问API
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
            'Authorization': f'Bearer {jwt_token}',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        },
        method='POST'
    )
    resp = opener.open(req, timeout=15)
    resp_text = resp.read().decode()
    print(f'\nAPI请求: HTTP {resp.status}')
    print(f'响应: {resp_text[:500]}')
    
except Exception as e:
    print(f'错误: {e}')

# 尝试4: 模拟完整的Trae CN客户端请求
print(f'\n--- 尝试4: 模拟完整客户端 ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好',
        'stream': True,  # 尝试流式
        'conversation_id': hashlib.md5(str(time.time()).encode()).hexdigest(),
        'user_id': userId,
        'tenant_id': tenant_id,
    }).encode()
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 TraeCN/{IDE_VERSION}',
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'text/event-stream',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Trae CN";v="2.3.62837"',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
    }
    
    req = urllib.request.Request(
        f'{API_BASE}/api/ide/v2/llm_raw_chat',
        data=body,
        headers=headers,
        method='POST'
    )
    
    # 使用stream模式
    resp = opener.open(req, timeout=30)
    print(f'HTTP {resp.status}')
    print(f'Content-Type: {resp.headers.get("Content-Type")}')
    
    # 读取部分响应
    chunk = resp.read(2000)
    resp_text = chunk.decode('utf-8', errors='replace')
    print(f'响应片段: {resp_text[:500]}')
    
except urllib.error.HTTPError as e:
    print(f'HTTP {e.code}: {e.read().decode()[:500]}')
except Exception as e:
    print(f'错误: {e}')
