#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尝试通过WebSocket连接Trae CN后端
以及尝试其他绕过认证的方法
"""

import json, ssl, time, sys, os, base64, hashlib
import urllib.request, urllib.error
import socket

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

parts = jwt_token.split('.')
def b64url_decode(s):
    s += '=' * (4 - len(s) % 4)
    return base64.urlsafe_b64decode(s)
payload = json.loads(b64url_decode(parts[1]))
tenant_id = payload['data']['tenant_id']

API_BASE = 'https://trae-api-cn.mchost.guru'
IDE_VERSION = '2.3.62837'

print(f'=== WebSocket和高级认证尝试 ===')
print(f'tenant_id: {tenant_id}')
print(f'userId: {userId}')

# 方法1: 尝试Trae CN的explorer WebSocket
print(f'\n--- 方法1: 查找WebSocket端点 ---')
ws_paths = [
    f'wss://trae-api-cn.mchost.guru/explorer',
    f'wss://trae-api-cn.mchost.guru/ws',
    f'wss://trae-api-cn.mchost.guru/api/ws',
    f'wss://trae-api-cn.mchost.guru/explorer?token={jwt_token[:50]}',
]

# 使用websocket-client库尝试
try:
    import websocket
    
    for ws_url in ws_paths[:2]:  # 只试前两个
        try:
            print(f'\n  尝试: {ws_url[:60]}...')
            ws = websocket.create_connection(
                ws_url, 
                header=[
                    f'Authorization: Bearer {jwt_token}',
                    f'User-Agent: TraeCN/{IDE_VERSION}',
                ],
                timeout=5,
                sslopt={'cert_reqs': 0}
            )
            print(f'  连接成功!')
            
            # 发送一个简单的ping
            ws.send(json.dumps({
                'type': 'ping',
                'data': {'timestamp': int(time.time())}
            }))
            
            response = ws.recv()
            print(f'  响应: {response[:200]}')
            
            # 尝试发送聊天请求
            ws.send(json.dumps({
                'type': 'chat',
                'data': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'stream': False,
                    'conversation_id': hashlib.md5(str(time.time()).encode()).hexdigest(),
                }
            }))
            
            response = ws.recv()
            print(f'  聊天响应: {response[:500]}')
            
            ws.close()
            
        except ImportError:
            print(f'  websocket库未安装')
        except Exception as e:
            print(f'  失败: {str(e)[:100]}')
            
except ImportError:
    print('  websocket-client库未安装，尝试安装...')
    import subprocess
    subprocess.run(['pip', 'install', 'websocket-client', '-q'], capture_output=True)
    print('  已安装websocket-client，请重新运行')

# 方法2: 使用Trae CN进程的IPC通道
print(f'\n--- 方法2: 检查Trae CN进程IPC ---')
import subprocess

# 检查Trae CN进程
try:
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe', '/FO', 'CSV'],
        capture_output=True, text=True, timeout=5
    )
    print(f'Trae CN进程: {result.stdout[:500]}')
except:
    pass

# 方法3: 尝试通过本地代理访问
print(f'\n--- 方法3: 本地代理尝试 ---')
# Trae CN可能在本地运行一些代理服务
local_proxy_ports = [
    (12789, 'HTTP代理'),
    (18080, 'CDP调试'),
    (9222, 'Chrome调试'),
    (8765, '本地服务器'),
    (3000, '开发服务器'),
]

for port, desc in local_proxy_ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        print(f'  端口 {port} ({desc}): 开放')
        
        # 尝试通过该端口代理请求
        try:
            proxy_handler = urllib.request.ProxyHandler({
                'http': f'http://127.0.0.1:{port}',
                'https': f'http://127.0.0.1:{port}',
            })
            opener = urllib.request.build_opener(
                proxy_handler,
                urllib.request.HTTPSHandler(context=ssl_ctx)
            )
            
            body = json.dumps({
                'model': 'doubao-pro-32k',
                'query': '你好',
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
            
            resp = opener.open(req, timeout=5)
            print(f'    代理响应: HTTP {resp.status} - {resp.read().decode()[:200]}')
            
        except Exception as e:
            print(f'    代理失败: {str(e)[:100]}')
            
    sock.close()

# 方法4: 完整请求模拟 - 使用HTTP/1.1特性
print(f'\n--- 方法4: 完整HTTP/1.1请求 ---')
try:
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
        'conversation_id': hashlib.md5(str(time.time()).encode()).hexdigest(),
        'user_id': userId,
        'tenant_id': tenant_id,
        'platform': 'pc',
        'client_version': IDE_VERSION,
    }).encode()
    
    # 使用HTTPConnection直接发送
    import http.client
    
    conn = http.client.HTTPSConnection(
        'trae-api-cn.mchost.guru', 
        context=ssl_ctx,
        timeout=15
    )
    
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
        'Authorization': f'Bearer {jwt_token}',
        'Accept': 'application/json, text/event-stream',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'identity',  # 避免压缩问题
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Connection': 'keep-alive',
        'X-Request-ID': hashlib.sha256(f'{time.time()}'.encode()).hexdigest(),
        'X-Correlation-ID': hashlib.md5(f'{userId}{time.time()}'.encode()).hexdigest(),
    }
    
    conn.request('POST', '/api/ide/v2/llm_raw_chat', body=body, headers=headers)
    resp = conn.getresponse()
    resp_text = resp.read().decode('utf-8')
    
    print(f'HTTP {resp.status}')
    print(f'Response Headers:')
    for k, v in resp.getheaders():
        if k.lower() not in ['date', 'server', 'x-request-id']:
            print(f'  {k}: {v}')
    print(f'\n响应: {resp_text[:500]}')
    
    conn.close()
    
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()
