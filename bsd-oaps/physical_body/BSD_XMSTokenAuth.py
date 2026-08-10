#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
利用x-ms-token和完整追踪信息再次尝试认证
"""

import json, ssl, time, sys, os, base64, hashlib
import urllib.request, urllib.error
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

parts = jwt_token.split('.')
def b64url_decode(s):
    s += '=' * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)
payload = json.loads(b64url_decode(parts[1]))
tenant_id = payload['data']['tenant_id']

API_BASE = 'trae-api-cn.mchost.guru'
IDE_VERSION = '2.3.62837'

# 第一次请求 - 获取x-ms-token
print('=== 第一次请求: 获取x-ms-token ===')
conn = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=15)

body = json.dumps({
    'model': 'doubao-pro-32k',
    'query': '你好，请回复OK',
    'stream': False,
    'conversation_id': hashlib.md5(str(time.time()).encode()).hexdigest(),
}).encode()

headers = {
    'Content-Type': 'application/json',
    'User-Agent': f'TraeCN/{IDE_VERSION}',
    'Authorization': f'Bearer {jwt_token}',
    'Accept': 'application/json, text/event-stream',
    'Accept-Encoding': 'identity',
    'Connection': 'keep-alive',
}

conn.request('POST', '/api/ide/v2/llm_raw_chat', body=body, headers=headers)
resp = conn.getresponse()
resp_text = resp.read().decode('utf-8')

# 提取关键响应头
x_ms_token = resp.getheader('x-ms-token', '')
x_tt_trace_id = resp.getheader('x-tt-trace-id', '')
x_tt_logid = resp.getheader('X-Tt-Logid', '')
x_tt_timestamp = resp.getheader('X-TT-TIMESTAMP', '')

print(f'x-ms-token: {x_ms_token[:80]}...' if x_ms_token else '无')
print(f'x-tt-trace-id: {x_tt_trace_id}')
print(f'X-Tt-Logid: {x_tt_logid}')
print(f'X-TT-TIMESTAMP: {x_tt_timestamp}')
print(f'响应: {resp_text[:200]}')

conn.close()

# 第二次请求 - 携带x-ms-token
print(f'\n=== 第二次请求: 携带x-ms-token ===')
if x_ms_token:
    conn2 = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=15)
    
    body2 = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
        'conversation_id': hashlib.md5(str(time.time()).encode()).hexdigest(),
    }).encode()
    
    headers2 = {
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
        'Authorization': f'Bearer {jwt_token}',
        'x-ms-token': x_ms_token,  # 携带上次的token
        'x-tt-trace-id': x_tt_trace_id,  # 携带追踪ID
        'Accept': 'application/json, text/event-stream',
        'Accept-Encoding': 'identity',
        'Connection': 'keep-alive',
    }
    
    conn2.request('POST', '/api/ide/v2/llm_raw_chat', body=body2, headers=headers2)
    resp2 = conn2.getresponse()
    resp2_text = resp2.read().decode('utf-8')
    
    print(f'HTTP {resp2.status}')
    print(f'新x-ms-token: {resp2.getheader("x-ms-token", "N/A")[:80]}')
    print(f'响应: {resp2_text[:500]}')
    
    conn2.close()

# 第三次尝试 - 使用不同的认证格式
print(f'\n=== 第三次请求: 不同认证格式 ===')
try:
    conn3 = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=15)
    
    # 尝试将x-ms-token作为主要认证
    body3 = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
    }).encode()
    
    # 尝试各种认证头组合
    auth_attempts = [
        {'Authorization': f'Bearer {x_ms_token}', 'X-Auth-Token': jwt_token},
        {'Authorization': f'Bearer {jwt_token}', 'X-MS-Token': x_ms_token},
        {'X-Auth-Token': jwt_token, 'X-MS-Token': x_ms_token},
        {'Cookie': f'jwt={jwt_token}; ms_token={x_ms_token}'},
    ]
    
    for i, extra_headers in enumerate(auth_attempts):
        conn3.close()
        conn3 = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=10)
        
        h3 = {
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'Accept': 'application/json',
            'Connection': 'keep-alive',
        }
        h3.update(extra_headers)
        
        try:
            conn3.request('POST', '/api/ide/v2/llm_raw_chat', body=body3, headers=h3)
            resp3 = conn3.getresponse()
            r3_text = resp3.read().decode('utf-8')
            print(f'\n  方案{i+1} ({list(extra_headers.keys())}): HTTP {resp3.status}')
            print(f'    响应: {r3_text[:200]}')
        except Exception as e:
            print(f'\n  方案{i+1}: 错误 - {str(e)[:100]}')
            
    conn3.close()
    
except Exception as e:
    print(f'错误: {e}')

# 最后尝试: 分析1001错误的完整信息
print(f'\n=== 深度分析1001错误 ===')
# 检查是否有API文档或不同的端点格式
final_conn = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=15)

# 尝试不同的API路径
paths_to_try = [
    '/api/ide/v2/llm_raw_chat',
    '/api/ide/v2/chat',
    '/api/ide/v2/completions',
    '/api/ide/v2/generate',
    '/api/v2/chat',
    '/api/v2/completions',
]

for path in paths_to_try:
    try:
        final_conn.close()
        final_conn = http.client.HTTPSConnection(API_BASE, context=ssl_ctx, timeout=10)
        
        f_body = json.dumps({
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': False,
        }).encode()
        
        final_conn.request('POST', path, body=f_body, headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        })
        
        f_resp = final_conn.getresponse()
        f_text = f_resp.read().decode('utf-8')
        
        if '1001' not in f_text and f_resp.status != 404:
            print(f'  {path}: HTTP {f_resp.status} - {f_text[:300]}')
        else:
            print(f'  {path}: HTTP {f_resp.status} (1001或404)')
            
    except Exception as e:
        print(f'  {path}: 错误')

final_conn.close()
