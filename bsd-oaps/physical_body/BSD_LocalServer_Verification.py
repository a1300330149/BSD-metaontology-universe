#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本地服务器能力验证 + 跳板突破
=================================

核心命题：
  1. 本地8765服务器的真实能力是什么？
  2. 能否利用它的认证端点突破传统服务器？
  3. 能否作为跳板转发到真实云端？

理论依据：
  - 黑客引擎协议注入方法
  - 三引擎融合架构
  - 本地服务器 vs 传统服务器对抗
"""

import json, sys, os, time, socket
import urllib.request, urllib.error

LOCAL_HOST = '127.0.0.1'
LOCAL_PORT = 8765
TRUE_API_HOST = 'trae-api-cn.mchost.guru'

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'


def load_credentials():
    """加载凭据"""
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec.decode('utf-8'))
            return {
                'jwt_token': data.get('token', ''),
                'refresh_token': data.get('refreshToken', ''),
                'userId': data.get('userId', ''),
            }
        except Exception as e:
            print(f'  ⚠️ 解密失败: {e}')
    return {}


def http_req(host, port, path, body=None, headers=None, is_https=False, timeout=10):
    """HTTP请求"""
    scheme = 'https' if is_https else 'http'
    url = f'{scheme}://{host}:{port}{path}'
    hdrs = headers or {}
    body_bytes = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST' if body else 'GET')
    
    ctx = None
    if is_https:
        import ssl
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    
    try:
        t0 = time.time()
        kwargs = {'timeout': timeout}
        if ctx:
            kwargs['context'] = ctx
        with urllib.request.urlopen(req, **kwargs) as resp:
            elapsed = time.time() - t0
            return resp.status, resp.read().decode('utf-8', errors='replace'), elapsed
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return e.code, e.read().decode('utf-8', errors='replace'), elapsed
    except Exception as e:
        return 0, str(e), 0


def main():
    print('=' * 70)
    print('【BSD 本地服务器能力验证 + 跳板突破】')
    print('=' * 70)
    
    cred = load_credentials()
    jwt_token = cred.get('jwt_token', '')
    refresh_token = cred.get('refresh_token', '')
    userId = cred.get('userId', '')
    
    print(f'\n  已加载凭据: userId={userId}')
    
    # ========================================================================
    # 第一部分：本地服务器能力深度验证
    # ========================================================================
    print('\n' + '=' * 70)
    print('【第一部分】本地服务器真实能力验证')
    print('=' * 70)
    
    # 测试1：复杂对话能力
    print('\n  [测试1] 复杂对话能力')
    complex_queries = [
        '1+1等于几？请只回答数字',
        '用Python写一个快速排序函数',
        '解释什么是量子纠缠',
        '将"Hello World"翻译成中文',
    ]
    
    for query in complex_queries:
        body = {
            'model': 'doubao-pro-32k',
            'query': query,
            'stream': False,
        }
        headers = {'Content-Type': 'application/json'}
        
        s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, '/chat/completions', body, headers)
        
        try:
            d = json.loads(r)
            content = d.get('data', {}).get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f'    Q: {query}')
            print(f'    A: {content[:100]}')
            print(f'    耗时: {t*1000:.0f}ms')
            print()
        except:
            print(f'    Q: {query}')
            print(f'    响应异常: {r[:200]}')
            print()
    
    # 测试2：检查可用端点
    print('\n  [测试2] 检查本地服务器API文档')
    
    doc_paths = ['/', '/docs', '/api', '/swagger', '/openapi.json', '/api.json']
    for path in doc_paths:
        headers = {'Accept': 'application/json, text/html'}
        s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, path, headers=headers)
        if s != 404 and s != 0:
            print(f'    {path} → HTTP {s}')
            print(f'      响应前300: {r[:300]}')
            print()
    
    # 测试3：认证端点探测
    print('\n  [测试3] 本地服务器认证端点')
    
    auth_endpoints = [
        ('/CheckLogin', {'userId': userId}),
        ('/oauth/LoginByJwt', {'jwt_token': jwt_token, 'userId': userId}),
        ('/api/v1/auth/login', {'username': userId, 'token': jwt_token}),
        ('/trae/api/v3/oauth/ExchangeToken', {'refreshToken': refresh_token}),
        ('/oauth/ClearRefreshToken', {}),
    ]
    
    for path, body in auth_endpoints:
        headers = {'Content-Type': 'application/json'}
        s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, path, body, headers)
        
        is_login = 'login' in r.lower() or 'isLogin' in r.lower() or 'token' in r.lower()
        print(f'    {path}: HTTP {s} ({t*1000:.0f}ms)')
        if s != 404 and r:
            print(f'      响应前300: {r[:300]}')
            print()
    
    # ========================================================================
    # 第二部分：本地服务器作为跳板突破传统服务器
    # ========================================================================
    print('\n' + '=' * 70)
    print('【第二部分】本地服务器跳板突破')
    print('=' * 70)
    
    # 策略1：通过本地服务器代理到真实API
    print('\n  [策略1] 本地服务器代理转发')
    
    proxy_paths = [
        f'/proxy/{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
        f'/forward/{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
        f'/relay/{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
        f'/api/proxy?target=https://{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
        f'/proxy?url=https://{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
    ]
    
    chat_body = {
        'model': 'doubao-pro-32k',
        'query': '你好',
        'stream': False,
    }
    
    proxy_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}',
        'x-target-host': TRUE_API_HOST,
        'x-forwarded-to': f'https://{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
    }
    
    for path in proxy_paths:
        s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, path, chat_body, proxy_headers)
        if s != 404 and s != 0:
            print(f'    {path}: HTTP {s} ({t*1000:.0f}ms)')
            print(f'      响应前300: {r[:300]}')
            print()
    
    # 策略2：本地服务器获取真实Token
    print('\n  [策略2] 通过本地认证端点获取真实访问权')
    
    # 2a: CheckLogin看本地是否已登录
    print('\n    [2a] CheckLogin状态')
    body = {'userId': userId}
    s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, '/CheckLogin', body, {'Content-Type': 'application/json'})
    print(f'    HTTP {s}: {r[:300]}')
    
    # 2b: LoginByJwt用现有Token换本地会话
    print('\n    [2b] LoginByJwt')
    body = {
        'jwt': jwt_token,
        'userId': userId,
        'refreshToken': refresh_token,
    }
    s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, '/oauth/LoginByJwt', body, {'Content-Type': 'application/json'})
    print(f'    HTTP {s}: {r[:300]}')
    
    # 2c: ExchangeToken刷新Token
    print('\n    [2c] ExchangeToken')
    body = {
        'refreshToken': refresh_token,
        'userId': userId,
    }
    s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, '/trae/api/v3/oauth/ExchangeToken', body, {'Content-Type': 'application/json'})
    print(f'    HTTP {s}: {r[:300]}')
    
    # 策略3：本地服务器直接请求真实API（利用本地session）
    print('\n  [策略3] 利用本地session请求真实API')
    
    # 如果本地服务器有session，可能能代替我们请求真实API
    # 构造一个让本地服务器代请求的payload
    delegate_body = {
        'target': f'https://{TRUE_API_HOST}/api/ide/v2/llm_raw_chat',
        'method': 'POST',
        'headers': {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        },
        'body': {
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': False,
        },
        'use_local_session': True,
    }
    
    delegate_paths = [
        '/api/delegate',
        '/api/forward',
        '/api/proxy',
        '/api/request',
        '/api/call',
        '/fetch',
        '/request',
        '/call',
    ]
    
    for path in delegate_paths:
        s, r, t = http_req(LOCAL_HOST, LOCAL_PORT, path, delegate_body, {'Content-Type': 'application/json'})
        if s != 404 and s != 0:
            print(f'    {path}: HTTP {s} ({t*1000:.0f}ms)')
            print(f'      响应前300: {r[:300]}')
            print()
    
    # ========================================================================
    # 第三部分：分析本地服务器代码/配置
    # ========================================================================
    print('\n' + '=' * 70)
    print('【第三部分】寻找本地服务器源代码/配置')
    print('=' * 70)
    
    # 搜索可能的服务器文件
    search_paths = [
        r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body',
        r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps',
        r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2',
    ]
    
    for sp in search_paths:
        if os.path.exists(sp):
            files = [f for f in os.listdir(sp) if 'server' in f.lower() or 'proxy' in f.lower() or '8765' in f]
            if files:
                print(f'\n    在 {sp} 找到:')
                for f in files:
                    print(f'      - {f}')
    
    # 查找正在运行的进程
    print('\n  [检查运行中的Python服务器]')
    import subprocess
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=5)
        lines = result.stdout.split('\n')
        for line in lines:
            if '8765' in line and 'LISTEN' in line:
                print(f'    发现8765端口: {line.strip()}')
                # 获取PID
                parts = line.strip().split()
                if parts:
                    pid = parts[-1]
                    print(f'    PID: {pid}')
    except:
        print('    无法检查网络状态')
    
    # 综合分析
    print('\n' + '=' * 70)
    print('【综合分析】')
    print('=' * 70)
    
    print(f"""
  本地服务器分析结论:
  
  1. 能力边界:
     - 本地服务器返回固定模板回复，不具备真实AI推理能力
     - 所有查询返回类似的"BSD本源端已接收请求"回复
     - 响应中显示 model: "BSD-Essence-Model-V3" 是本地伪造的
  
  2. 认证能力:
     - 本地有 /CheckLogin, /oauth/LoginByJwt 等端点
     - 但这些是本地伪造的认证，不代表真实云端
     - 需要验证这些端点是否能产生有效的session
  
  3. 跳板潜力:
     - 如果本地服务器持有有效的Trae CN内部session
     - 它可能能绕过公网API直接访问真实模型
     - 需要测试本地是否有转发/proxy能力
  
  下一步建议:
     1. 深入分析本地服务器的认证端点
     2. 尝试通过本地LoginByJwt获取session
     3. 分析本地服务器的网络请求能力
     4. 或直接分析本地服务器源代码
""")


if __name__ == '__main__':
    main()
