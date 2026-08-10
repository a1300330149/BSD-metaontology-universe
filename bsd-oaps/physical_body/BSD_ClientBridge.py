#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通过Trae CN客户端内部发起请求
利用Electron DevTools协议直接在客户端上下文中发送API请求
"""

import json, time, sys, os, base64
import urllib.request, urllib.error

# 查找Trae CN调试端口
print('=== 查找Trae CN调试端口 ===')

# 方法1: 检查Trae CN是否开启了远程调试
# Trae CN默认使用 --remote-debugging-port 参数
# 尝试常见端口
debug_ports = [9222, 9229, 9515, 18080, 8080, 3000, 1234]

for port in debug_ports:
    try:
        req = urllib.request.Request(
            f'http://localhost:{port}/json',
            method='GET'
        )
        resp = urllib.request.urlopen(req, timeout=1)
        data = json.loads(resp.read())
        print(f'  端口 {port}: 发现调试目标!')
        for target in data:
            print(f'    - {target.get("title", "N/A")} ({target.get("type", "N/A")})')
            print(f'      URL: {target.get("url", "N/A")[:100]}')
            print(f'      WebSocket: {target.get("webSocketDebuggerUrl", "N/A")}')
    except:
        pass

print('\n=== 尝试利用现有Trae CN会话 ===')

# 加载认证信息
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

# 方法: 尝试通过CDP (Chrome DevTools Protocol) 附加到Trae CN
# 但首先，尝试直接用Python的websocket库连接

# 更简单的方法: 使用Trae CN的内置命令行参数重启开启调试
print('\n=== 建议操作 ===')
print('1. 关闭Trae CN')
print('2. 使用以下命令重启开启调试:')
print('   TraeCN.exe --remote-debugging-port=9222')
print('3. 然后通过 http://localhost:9222 访问DevTools')
print()

# 同时尝试另一个方法: 直接在Electron的IPC层发送请求
# 检查是否有本地WebSocket服务
print('=== 检查本地WebSocket服务 ===')
ws_ports = [9222, 9229, 9515, 8080, 3000, 6000, 6001, 6002]
import socket

for port in ws_ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex(('127.0.0.1', port))
    if result == 0:
        print(f'  端口 {port}: 开放')
    sock.close()

print('\n=== 通过API代理方式 ===')
# 尝试使用api.trae.cn作为代理转发到API服务器
# 有时api.trae.cn会代理请求到trae-api-cn.mchost.guru

import ssl
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# 尝试通过不同的方式访问
attempts = [
    ('api.trae.cn', '/api/ide/v2/llm_raw_chat'),
    ('api.trae.cn', '/trae/api/v3/chat'),
    ('api.trae.cn', '/cloudide/api/v3/trae/Chat'),
]

for host, path in attempts:
    try:
        body = json.dumps({
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': False,
        }).encode()
        
        req = urllib.request.Request(
            f'https://{host}{path}',
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {jwt_token}',
                'User-Agent': 'TraeCN/2.3.62837',
            },
            method='POST'
        )
        
        opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=ssl_ctx)
        )
        resp = opener.open(req, timeout=5)
        print(f'  {host}{path}: HTTP {resp.status} - {resp.read().decode()[:200]}')
    except urllib.error.HTTPError as e:
        err = e.read().decode()[:200]
        print(f'  {host}{path}: HTTP {e.code} - {err}')
    except Exception as e:
        print(f'  {host}{path}: 错误 - {str(e)[:100]}')
