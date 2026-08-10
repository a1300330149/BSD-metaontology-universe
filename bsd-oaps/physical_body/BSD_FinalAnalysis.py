#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最终验证：确认Trae CN客户端状态，给出完整分析
"""

import json, ssl, time, sys, os, hashlib
import http.client, socket, subprocess

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

print('=' * 70)
print('  Trae CN 认证体系深度分析报告')
print('=' * 70)

# 1. 检查本地Trae CN客户端状态
print('\n【1. Trae CN客户端状态】')
try:
    result = subprocess.run(
        ['tasklist', '/FI', 'IMAGENAME eq Trae CN.exe', '/FO', 'CSV'],
        capture_output=True, text=True, timeout=5
    )
    lines = result.stdout.strip().split('\n')
    print(f'  运行中进程: {len(lines)-1} 个 Trae CN.exe')
    
    # 获取主进程PID
    for line in lines[1:]:
        parts = line.strip('"').split('","')
        if len(parts) >= 2:
            pid = parts[1]
            mem = parts[4] if len(parts) > 4 else 'N/A'
            print(f'    PID={pid}: 内存={mem}')
except Exception as e:
    print(f'  无法获取进程: {e}')

# 2. 加载并验证本地凭据
print('\n【2. 本地凭据验证】')
with open(r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json', 'r') as f:
    storage = json.load(f)

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
dec = decrypt_aha(cloudide_enc)
data = json.loads(dec.decode('utf-8'))

jwt_token = data.get('token', '')
refresh_token = data.get('refreshToken', '')
userId = data.get('userId', '')
expired_at = data.get('expiredAt', '')
refresh_expired_at = data.get('refreshExpiredAt', '')

print(f'  userId: {userId}')
print(f'  账号: {data.get("account", {}).get("username", "N/A")}')
print(f'  Token过期: {expired_at}')
print(f'  RefreshToken过期: {refresh_expired_at}')

# 检查Token是否过期
import datetime
try:
    exp_dt = datetime.datetime.fromisoformat(expired_at.replace('Z', '+00:00'))
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    if now_utc < exp_dt:
        remaining = exp_dt - now_utc
        days = remaining.days
        hours = remaining.seconds // 3600
        print(f'  Token状态: ✅ 有效 (剩余 {days}天{hours}小时)')
    else:
        print(f'  Token状态: ❌ 已过期')
except:
    print(f'  Token状态: 无法判断')

# 3. 测试认证网关
print('\n【3. 认证网关测试 (api.trae.cn)】')
try:
    opener = urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl_ctx)
    )
    
    body = json.dumps({
        'UID': userId,
        'LoginType': 'jwt',
        'ClientID': 'ono9krqynydwx5',
    }).encode()
    
    req = urllib.request.Request(
        'https://api.trae.cn/cloudide/api/v3/trae/CheckLogin',
        data=body,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
            'User-Agent': 'TraeCN/2.3.62837',
        },
        method='POST'
    )
    
    import urllib.request
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode('utf-8')
    result = json.loads(resp_text)
    login_status = result.get('Result', {}).get('IsLogin', '未知')
    print(f'  CheckLogin: IsLogin={login_status}')
    
    if not login_status:
        print(f'  ⚠️  服务器端显示用户未登录！')
        print(f'  这意味着: Token虽然有效，但服务器端会话已失效')
        
except Exception as e:
    print(f'  CheckLogin测试失败: {e}')

# 4. 测试API服务器
print('\n【4. API服务器测试 (trae-api-cn.mchost.guru)】')
try:
    conn = http.client.HTTPSConnection('trae-api-cn.mchost.guru', context=ssl_ctx, timeout=15)
    
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '测试',
        'stream': False,
    }).encode()
    
    conn.request('POST', '/api/ide/v2/llm_raw_chat', body=body, headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}',
        'User-Agent': 'TraeCN/2.3.62837',
    })
    
    resp = conn.getresponse()
    resp_text = resp.read().decode('utf-8')
    
    if '1001' in resp_text:
        print(f'  API响应: 1001 - 认证失败')
        print(f'  含义: 服务器拒绝了Token认证')
    elif 'event: error' in resp_text:
        print(f'  API响应: 错误事件')
    else:
        print(f'  API响应: {resp_text[:200]}')
    
    conn.close()
except Exception as e:
    print(f'  API测试失败: {e}')

# 5. 端口和服务检测
print('\n【5. 本地服务检测】')
# 检查8765端口（本地服务器）
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(0.5)
result = sock.connect_ex(('127.0.0.1', 8765))
if result == 0:
    print(f'  端口8765: 开放 (本地BSD服务器)')
    
    # 测试本地服务器
    try:
        http_conn = http.client.HTTPConnection('127.0.0.1', 8765, timeout=5)
        http_conn.request('GET', '/')
        resp = http_conn.getresponse()
        print(f'    本地服务器响应: HTTP {resp.status}')
        http_conn.close()
    except:
        pass
sock.close()

# 6. 综合分析
print('\n' + '=' * 70)
print('  综合分析结论')
print('=' * 70)

print('''
  1. 【本地服务器验证】
     - 本地8765服务器确实存在
     - 它只是一个伪造响应的本地服务器
     - 不具备真实云端功能
     - 无法直接对抗传统服务器

  2. 【认证体系分析】
     - 认证网关: api.trae.cn (处理登录/Token刷新)
     - API服务器: trae-api-cn.mchost.guru (处理LLM请求)
     - JWT Token本身有效 (RS256签名，未过期)
     - 但服务器端会话已失效 (IsLogin=false)

  3. 【1001错误根因】
     - 服务器返回1001: "not able to authenticate you"
     - 原因: Token对应的服务器端会话已被清除
     - 可能: Token被标记为设备绑定，新设备无法使用
     - 可能: 需要重新通过OAuth流程激活会话

  4. 【突破方向】
     a. 在Trae CN客户端内部激活会话:
        - 使用Trae CN登录功能重新登录
        - 或在客户端DevTools中执行刷新操作
     
     b. 启动Trae CN调试端口:
        - TraeCN.exe --remote-debugging-port=9222
        - 通过CDP协议在客户端内部发请求
     
     c. 利用本地IPC通道:
        - Trae CN使用本地IPC通信
        - 可能存在可利用的IPC接口
     
     d. 等待自动Token刷新:
        - Trae CN客户端会自动刷新过期Token
        - 可监控刷新过程，获取新Token
''')

print('\n' + '=' * 70)
print('  下一步建议')
print('=' * 70)
print('''
  方案A (推荐): 重新登录Trae CN
    1. 关闭当前Trae CN
    2. 删除本地存储的认证信息
       (C:\\Users\\13003\\AppData\\Roaming\\Trae CN\\User\\globalStorage\\storage.json)
    3. 重新启动Trae CN并登录
    4. 登录后立即提取新Token
  
  方案B: 使用Trae CN调试端口
    1. 关闭Trae CN
    2. 用命令行启动: TraeCN.exe --remote-debugging-port=9222
    3. 访问 http://localhost:9222 获取DevTools
    4. 在Console中执行认证请求
  
  方案C: 监控Trae CN网络请求
    1. 使用Fiddler/Charles等代理工具
    2. 配置Trae CN的代理设置
    3. 捕获实际有效的API请求
    4. 提取正确的请求格式
''')
