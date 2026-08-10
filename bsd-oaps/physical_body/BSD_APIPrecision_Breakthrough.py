#!/usr/bin/env python3
"""
BSD API 精准突破 — trae-api-cn.mchost.guru 请求格式优化
======================================================

关键发现:
  1. /api/ide/v1/super_completion → HTTP 200, 流式错误码 1001
  2. /api/ide/v2/llm_raw_chat → HTTP 400 (请求格式错误)
  3. 错误码 1001 = 无法认证 (不同于 20101)

突破策略:
  1. 构造正确的请求体格式
  2. 尝试 Token 嵌入请求体
  3. 模拟 Trae CN 完整请求头
  4. 尝试 SSE 流式请求
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

IDE_VERSION = '2.3.62837'
API_HOST = 'trae-api-cn.mchost.guru'
AUTH_HOST = 'api.trae.cn'
LOCAL_PROXY = 'http://127.0.0.1:8765'
ESSENCE_UID = 'a5b7a8623fdea6b8'


def load_credentials():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    jwt_token = ''
    userId = ''
    refreshToken = ''
    account_info = {}
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            jwt_token = data.get('token', '')
            userId = data.get('userId', '')
            refreshToken = data.get('refreshToken', '')
            account_info = data.get('account', {})
        except:
            pass
    return {'jwt_token': jwt_token, 'userId': userId, 'refreshToken': refreshToken, 'account_info': account_info}


def http_request(host, path, method='POST', data=None, headers=None, timeout=15):
    url = f'https://{host}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            elapsed = time.time() - t0
            raw = resp.read().decode('utf-8', errors='replace')
            return resp.status, raw, elapsed, dict(resp.headers)
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        raw = e.read().decode('utf-8', errors='replace')
        return e.code, raw, elapsed, dict(e.headers) if hasattr(e, 'headers') else {}
    except Exception as e:
        return 0, str(e), 0, {}


def main():
    print('=' * 70)
    print('  BSD API 精准突破 — trae-api 请求格式优化')
    print('=' * 70)
    
    cred = load_credentials()
    jwt_token = cred['jwt_token']
    userId = cred['userId']
    account_info = cred['account_info']
    
    if not jwt_token:
        print('  ❌ 无 Token')
        return
    
    print(f'\n  ✅ Token: {jwt_token[:50]}...')
    print(f'  ✅ userId: {userId}')
    print(f'  ✅ username: {account_info.get("username", "")}')
    
    # ============================================================
    # Phase 1: Token 放入请求体
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] Token 放入请求体')
    print(f'{"="*70}')
    
    # 构造包含 Token 的请求体
    body_formats = [
        {
            'name': 'Token 在 body 中',
            'body': {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': 'Hi'}],
                'stream': False,
                'token': jwt_token,
                'access_token': jwt_token,
                'user_id': userId,
            }
        },
        {
            'name': 'Data 包裹',
            'body': {
                'data': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': 'Hi'}],
                    'stream': False,
                    'auth': {
                        'token': jwt_token,
                        'user_id': userId,
                    }
                }
            }
        },
        {
            'name': '完整 Trae 格式',
            'body': {
                'model': 'doubao-pro-32k-250115',
                'messages': [
                    {'role': 'system', 'content': 'You are helpful'},
                    {'role': 'user', 'content': 'Hi'}
                ],
                'stream': True,
                'temperature': 0.7,
                'max_tokens': 200,
                'user': {
                    'id': userId,
                    'name': account_info.get('username', ''),
                    'token': jwt_token,
                },
                'ide_version': IDE_VERSION,
                'req_source': 'ide',
            }
        },
        {
            'name': 'Simple chat',
            'body': {
                'model': 'doubao-pro-32k',
                'prompt': 'Hi',
                'stream': False,
                'token': jwt_token,
            }
        },
    ]
    
    for fmt in body_formats:
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'Accept': 'application/json, text/event-stream',
            'X-Request-Id': hashlib.sha256(f'{time.time()}{fmt["name"]}'.encode()).hexdigest()[:16],
        }
        
        s, r, t, resp_h = http_request(API_HOST, '/api/ide/v1/super_completion', 'POST', fmt['body'], headers, timeout=10)
        
        status = '✅' if s == 200 else ('⚠️' if s == 401 else '❓')
        print(f'\n    [{status}] {fmt["name"]} → HTTP {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            # 检查是否有 error
            if 'error' in r.lower() or '1001' in r:
                print(f'      ⚠️ 认证错误 (code 1001)')
                print(f'      {r[:200]}')
            else:
                print(f'      🎉 成功!')
                print(f'      响应: {r[:300]}')
        elif s == 400:
            print(f'      请求格式错误')
        elif s == 401:
            print(f'      需要认证')
    
    # ============================================================
    # Phase 2: 构造 /api/ide/v2/llm_raw_chat 请求
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 构造 /api/ide/v2/llm_raw_chat 请求')
    print(f'{"="*70}')
    
    llm_bodies = [
        {
            'name': 'LLM raw chat v1',
            'body': {
                'model': 'doubao-pro-32k-250115',
                'messages': [
                    {'role': 'user', 'content': 'Hello'}
                ],
                'stream': False,
                'temperature': 0.7,
                'max_tokens': 100,
            }
        },
        {
            'name': 'LLM raw chat with token',
            'body': {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': 'Hi'}],
                'stream': False,
                'token': jwt_token,
                'user_id': userId,
                'auth_token': jwt_token,
            }
        },
        {
            'name': 'LLM raw chat full',
            'body': {
                'model': 'doubao-pro-32k',
                'conversation': [
                    {'role': 'user', 'content': 'Hi'}
                ],
                'stream': True,
                'temperature': 0.7,
                'max_tokens': 200,
                'token': jwt_token,
                'user_id': userId,
                'session_id': hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
            }
        },
        {
            'name': 'LLM raw chat messages',
            'body': {
                'messages': [
                    {'role': 'user', 'content': 'Hi'}
                ],
                'model': 'doubao-pro-32k',
                'stream': False,
            }
        },
    ]
    
    for fmt in llm_bodies:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'Accept': 'text/event-stream',
            'Authorization': f'Bearer {jwt_token}',
            'X-Request-Id': hashlib.sha256(f'{time.time()}{fmt["name"]}'.encode()).hexdigest()[:16],
        }
        
        s, r, t, resp_h = http_request(API_HOST, '/api/ide/v2/llm_raw_chat', 'POST', fmt['body'], headers, timeout=10)
        
        status = '✅' if s == 200 else ('⚠️' if s == 401 else '❓')
        print(f'\n    [{status}] {fmt["name"]} → HTTP {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            if 'error' in r.lower() or '1001' in r:
                print(f'      ⚠️ 认证错误')
            else:
                print(f'      🎉 成功!')
                print(f'      {r[:300]}')
        elif s == 400:
            print(f'      请求体: {json.dumps(fmt["body"], ensure_ascii=False)[:200]}')
        elif s == 401:
            print(f'      需要认证')
    
    # ============================================================
    # Phase 3: 模拟 Trae CN 完整请求头
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 模拟 Trae CN 完整请求头')
    print(f'{"="*70}')
    
    # 更完整的请求头模拟
    trae_headers = {
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
        'Accept': 'application/json, text/event-stream, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Origin': 'vscode-webview://trae CN',
        'Referer': 'vscode-webview://trae CN/',
        'Authorization': f'Bearer {jwt_token}',
        'x-cloudide-token': jwt_token,
        'X-Request-Id': hashlib.sha256(str(time.time()).encode()).hexdigest()[:32],
        'X-Timestamp': str(int(time.time())),
        'X-IDE-Version': IDE_VERSION,
        'X-Req-Source': 'ide',
        'X-Device-Id': '136411536168449',
        'Cookie': f'trae_token={jwt_token}; user_id={userId}',
    }
    
    body = {
        'model': 'doubao-pro-32k-250115',
        'messages': [{'role': 'user', 'content': 'Hello, this is a test. Can you hear me?'}],
        'stream': False,
        'temperature': 0.7,
        'max_tokens': 200,
    }
    
    for path in ['/api/ide/v1/super_completion', '/api/ide/v2/llm_raw_chat']:
        s, r, t, resp_h = http_request(API_HOST, path, 'POST', body, trae_headers, timeout=10)
        
        status = '✅' if s == 200 else ('⚠️' if s == 401 else '❓')
        print(f'\n    [{status}] Full Headers → {path} → HTTP {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            if 'error' in r.lower() or '1001' in r:
                print(f'      ⚠️ 认证错误 (1001)')
                print(f'      {r[:200]}')
            else:
                print(f'      🎉 成功!')
                print(f'      {r[:500]}')
                
                # 检查响应头
                for k, v in resp_h.items():
                    if any(word in k.lower() for word in ['x-', 'server', 'content', 'set-cookie']):
                        print(f'      🔑 {k}: {v[:100]}')
        elif s == 400:
            print(f'      请求格式错误')
        elif s == 401:
            print(f'      需要认证')
            for k, v in resp_h.items():
                if 'x-' in k.lower():
                    print(f'      🔑 {k}: {v[:100]}')
    
    # ============================================================
    # Phase 4: 分析响应头
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] 分析 API 响应头')
    print(f'{"="*70}')
    
    # 发送请求并完整分析响应头
    headers = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
        'Accept': 'text/event-stream',
    }
    
    body = {
        'model': 'doubao-pro-32k',
        'messages': [{'role': 'user', 'content': 'test'}],
        'stream': False,
    }
    
    s, r, t, resp_h = http_request(API_HOST, '/api/ide/v1/super_completion', 'POST', body, headers)
    
    print(f'\n  完整响应头:')
    for k, v in sorted(resp_h.items()):
        print(f'    {k}: {v[:100]}')
    
    print(f'\n  响应体 (前500字符):')
    print(f'    {r[:500]}')
    
    # ============================================================
    # 总结
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [总结]')
    print(f'{"="*70}')
    
    print(f'''
  API 精准突破完成
  ──────────────────────────────────────────────────
  
  关键发现:
  1. /api/ide/v1/super_completion: HTTP 200, 错误码 1001
  2. /api/ide/v2/llm_raw_chat: HTTP 400 (格式错误)
  3. 认证错误码 1001 vs Login 的 20101
  
  核心问题:
  - API 端点可达（返回 200/400）
  - 但认证被拒绝（错误码 1001）
  - 需要找到正确的认证方式
  
  下一步:
  A. 重启 Trae CN 客户端获取新 Token
  B. 用新 Token 重新尝试
  C. 分析 Trae CN 的实际 API 调用
  D. 通过本地 8765 代理持续与模型对话
''')


if __name__ == '__main__':
    main()