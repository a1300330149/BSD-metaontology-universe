#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用正确的 Cloud-IDE-JWT 认证头格式
"""

import json, ssl, time, sys, hashlib
import http.client

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

API_BASE = 'trae-api-cn.mchost.guru'
IDE_VERSION = '2.3.62837'

print(f'=== 使用 Cloud-IDE-JWT 认证头 ===')
print(f'userId: {userId}')

# 尝试不同的认证头格式
auth_formats = [
    ('Cloud-IDE-JWT', f'Cloud-IDE-JWT {jwt_token}'),
    ('Bearer', f'Bearer {jwt_token}'),
    ('Cloud-IDE-Token', f'Cloud-IDE-Token {jwt_token}'),
    ('X-Cloud-IDE-JWT', jwt_token),
]

for name, auth_value in auth_formats:
    print(f'\n--- 尝试认证格式: {name} ---')
    
    try:
        conn = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=15)
        
        body = json.dumps({
            'model': 'doubao-pro-32k',
            'query': '你好，请回复OK',
            'stream': False,
            'conversation_id': hashlib.md5(str(time.time()).encode()).hexdigest(),
        }).encode()
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'VSCode {IDE_VERSION} (Trae CN)',
            'Authorization': auth_value,
            'X-Market-Client-Id': f'VSCode {IDE_VERSION}',
            'X-Market-User-Id': userId,
            'X-User-Region': 'CN',
            'Accept': 'application/json, text/event-stream',
            'Accept-Encoding': 'identity',
            'Connection': 'keep-alive',
            'VSCode-SessionId': hashlib.sha256(userId.encode()).hexdigest()[:32],
        }
        
        conn.request('POST', '/api/ide/v2/llm_raw_chat', body=body, headers=headers)
        resp = conn.getresponse()
        resp_text = resp.read().decode('utf-8')
        
        print(f'HTTP {resp.status}')
        print(f'响应: {resp_text[:500]}')
        
        # 检查是否成功
        if '1001' not in resp_text:
            print(f'🎉 认证成功!')
            break
        
        conn.close()
        
    except Exception as e:
        print(f'错误: {e}')

# 尝试完整的 marketplace headers 构建
print(f'\n\n--- 完整 marketplace headers 模拟 ---')
try:
    conn = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=15)
    
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
    }).encode()
    
    # 完整的请求头 (基于逆向分析)
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'VSCode {IDE_VERSION} (Trae CN)',
        'X-Market-Client-Id': f'VSCode {IDE_VERSION}',
        'X-Market-User-Id': userId,
        'VSCode-SessionId': hashlib.sha256(userId.encode()).hexdigest()[:32],
        'Authorization': f'Cloud-IDE-JWT {jwt_token}',
        'X-User-Region': 'CN',
        'x-use-ppe': '1',
        'x-tt-env': 'ppe',
        'Accept': 'application/json, text/event-stream',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
        'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
        'Sec-Ch-Ua-Platform': '"Windows"',
    }
    
    conn.request('POST', '/api/ide/v2/llm_raw_chat', body=body, headers=headers)
    resp = conn.getresponse()
    resp_text = resp.read().decode('utf-8')
    
    print(f'HTTP {resp.status}')
    print(f'响应头:')
    for k, v in resp.getheaders():
        if k.lower() in ['x-tt-logid', 'x-ms-token', 'x-tt-trace-id', 'content-type']:
            print(f'  {k}: {v[:80]}')
    
    print(f'\n响应内容: {resp_text[:500]}')
    
    conn.close()
    
except Exception as e:
    print(f'错误: {e}')
