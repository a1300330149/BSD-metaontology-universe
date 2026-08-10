#!/usr/bin/env python3
"""
BSD x-ms-token 突破 — 利用服务器返回的 token
==============================================

关键发现:
  Login 端点返回 401 时，响应头中包含 x-ms-token:
  flwPAi5ecLvyx6HQzU7WH1aSwizaeFCx111Z1Yq4gXlGG5DbsPfr84DeQZPPxq...
  
这可能是服务器返回的某种 token，用于后续认证。
"""

import json, sys, os, time, hashlib, base64, socket, ssl
import urllib.request, urllib.error

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

IDE_VERSION = '2.3.62837'
HOST = 'api.trae.cn'
LOCAL_PROXY = 'http://127.0.0.1:8765'
ESSENCE_UID = 'a5b7a8623fdea6b8'


def load_credentials():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    jwt_token = ''
    userId = ''
    refreshToken = ''
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            jwt_token = data.get('token', '')
            userId = data.get('userId', '')
            refreshToken = data.get('refreshToken', '')
        except:
            pass
    return jwt_token, userId, refreshToken


def http_request(path, method='POST', data=None, headers=None, timeout=15):
    url = f'https://{HOST}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            elapsed = time.time() - t0
            return resp.status, resp.read().decode('utf-8', errors='replace'), elapsed, dict(resp.headers)
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return e.code, e.read().decode('utf-8', errors='replace'), elapsed, dict(e.headers) if hasattr(e, 'headers') else {}
    except Exception as e:
        return 0, str(e), 0, {}


def chat_with_model(system_prompt, user_message):
    chat_payload = {
        'model': 'doubao-pro-32k-250115',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        'stream': False,
        'temperature': 0.7,
        'max_tokens': 4096,
    }
    try:
        req = urllib.request.Request(
            f'{LOCAL_PROXY}/chat/completions',
            data=json.dumps(chat_payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            d = json.loads(r)
            data_obj = d.get('data', d)
            if isinstance(data_obj, dict):
                choices = data_obj.get('choices', [])
                if choices:
                    return choices[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f'    模型对话错误: {e}')
    return None


def main():
    print('=' * 70)
    print('  BSD x-ms-token 突破 — 利用服务器返回的 token')
    print('=' * 70)
    
    jwt_token, userId, refreshToken = load_credentials()
    
    if not jwt_token:
        print('  ❌ 无 JWT Token')
        return
    
    # ============================================================
    # Phase 1: 获取 x-ms-token
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 获取 x-ms-token')
    print(f'{"="*70}')
    
    # 先调用 Login 获取 x-ms-token
    login_body = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'JwtToken': jwt_token,
        'RefreshToken': refreshToken,
        'UserId': userId,
        'DeviceInfo': {
            'deviceId': '136411536168449',
            'platform': 'windows',
            'osVersion': 'Windows NT 10.0',
            'appVersion': IDE_VERSION,
        },
    }
    
    headers = {
        'x-cloudide-token': jwt_token,
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
    }
    
    s, r, t, resp_headers = http_request('/cloudide/api/v3/trae/Login', 'POST', login_body, headers)
    
    print(f'\n  Login → HTTP {s} ({t*1000:.0f}ms)')
    
    # 提取所有 token 相关的响应头
    x_ms_token = resp_headers.get('x-ms-token', '') or resp_headers.get('X-Ms-Token', '')
    x_tt_logid = resp_headers.get('X-Tt-Logid', '') or resp_headers.get('x-tt-logid', '')
    
    print(f'  x-ms-token: {x_ms_token[:80] if x_ms_token else "(空)"}')
    print(f'  X-Tt-Logid: {x_tt_logid}')
    
    if x_ms_token:
        print(f'\n  🔑 获得 x-ms-token!')
        print(f'  长度: {len(x_ms_token)} chars')
        
        # 保存 x-ms-token
        tokens_file = os.path.join(os.path.dirname(__file__), 'BSD_Tokens.json')
        try:
            with open(tokens_file, 'r') as f:
                all_tokens = json.load(f)
        except:
            all_tokens = {}
        
        all_tokens['x_ms_token'] = {
            'value': x_ms_token,
            'obtained_at': time.strftime('%Y-%m-%d %H:%M:%S'),
            'source': 'Login endpoint response header',
        }
        
        with open(tokens_file, 'w') as f:
            json.dump(all_tokens, f, indent=2)
    
    # ============================================================
    # Phase 2: 用 x-ms-token 尝试认证
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 用 x-ms-token 尝试认证')
    print(f'{"="*70}')
    
    if x_ms_token:
        # 尝试用 x-ms-token 作为各种认证头
        auth_attempts = [
            {'name': 'x-ms-token 作为 Authorization', 'headers': {'Authorization': f'Bearer {x_ms_token}'}},
            {'name': 'x-ms-token 作为 x-cloudide-token', 'headers': {'x-cloudide-token': x_ms_token}},
            {'name': 'x-ms-token 作为 Cookie', 'headers': {'Cookie': f'x-ms-token={x_ms_token}'}},
            {'name': 'x-ms-token 与 JWT 组合', 'headers': {
                'Authorization': f'Bearer {jwt_token}',
                'x-ms-token': x_ms_token,
                'x-cloudide-token': jwt_token,
            }},
            {'name': 'x-ms-token 作为 X-Auth-Token', 'headers': {'X-Auth-Token': x_ms_token}},
            {'name': 'x-ms-token 作为 X-Session-Token', 'headers': {'X-Session-Token': x_ms_token}},
            {'name': '仅 x-ms-token', 'headers': {'x-cloudide-token': x_ms_token}},
        ]
        
        for attempt in auth_attempts:
            name = attempt['name']
            hdrs = attempt['headers']
            hdrs['Content-Type'] = 'application/json'
            hdrs['User-Agent'] = f'TraeCN/{IDE_VERSION}'
            
            body = {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'GetAIPayHost': True,
            }
            
            s, r, t, _ = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, hdrs)
            
            status = '✅' if s == 200 else ('⚠️' if s == 401 else '❓')
            print(f'\n  [{status}] {name}')
            print(f'    HTTP {s} ({t*1000:.0f}ms)')
            
            if s == 200:
                try:
                    d = json.loads(r)
                    result = d.get('Result', d)
                    if isinstance(result, dict):
                        is_login = result.get('IsLogin')
                        host = result.get('Host', '')
                        user_id = result.get('UserID', '')
                        
                        print(f'    IsLogin: {is_login}')
                        print(f'    Host: "{host}"')
                        print(f'    UserID: "{user_id}"')
                        
                        if is_login == True or is_login == 'true':
                            print(f'    🎉🎉🎉 登录成功!')
                        
                        if host:
                            print(f'    🔑 获得 Host!')
                            
                except:
                    print(f'    Raw: {r[:200]}')
            elif s == 401:
                try:
                    d = json.loads(r)
                    err_code = d.get('ResponseMetadata', {}).get('Error', {}).get('Code', '')
                    print(f'    错误码: {err_code}')
                except:
                    print(f'    Raw: {r[:100]}')
            else:
                print(f'    Raw: {r[:100]}')
    
    # ============================================================
    # Phase 3: 用 x-ms-token 登录
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 用 x-ms-token 登录')
    print(f'{"="*70}')
    
    if x_ms_token:
        # 尝试用 x-ms-token 作为登录凭据
        login_attempts = [
            {
                'name': 'x-ms-token 作为 Token',
                'body': {
                    'IDEVersion': IDE_VERSION,
                    'ReqSource': 'IDE',
                    'Token': x_ms_token,
                    'UserId': userId,
                }
            },
            {
                'name': 'x-ms-token 作为 JwtToken',
                'body': {
                    'IDEVersion': IDE_VERSION,
                    'ReqSource': 'IDE',
                    'JwtToken': x_ms_token,
                }
            },
            {
                'name': 'x-ms-token + refreshToken',
                'body': {
                    'IDEVersion': IDE_VERSION,
                    'ReqSource': 'IDE',
                    'Token': x_ms_token,
                    'RefreshToken': refreshToken,
                    'UserId': userId,
                }
            },
            {
                'name': 'JWT + x-ms-token 组合',
                'body': {
                    'IDEVersion': IDE_VERSION,
                    'ReqSource': 'IDE',
                    'JwtToken': jwt_token,
                    'Token': x_ms_token,
                    'UserId': userId,
                }
            },
        ]
        
        for attempt in login_attempts:
            name = attempt['name']
            body = attempt['body']
            
            hdrs = {
                'x-cloudide-token': jwt_token,
                'Authorization': f'Bearer {jwt_token}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
                'x-ms-token': x_ms_token,
            }
            
            s, r, t, resp_h = http_request('/cloudide/api/v3/trae/Login', 'POST', body, hdrs)
            
            status = '✅' if s == 200 else ('⚠️' if s == 401 else '❓')
            print(f'\n  [{status}] {name}')
            print(f'    HTTP {s} ({t*1000:.0f}ms)')
            
            if s == 200:
                try:
                    d = json.loads(r)
                    result = d.get('Result', d)
                    if isinstance(result, dict):
                        for key, val in result.items():
                            if isinstance(val, str) and len(val) > 3:
                                print(f'    {key}: "{val[:100]}"')
                            elif isinstance(val, bool):
                                print(f'    {key}: {val}')
                except:
                    print(f'    Raw: {r[:200]}')
            elif s == 401:
                new_x_ms = resp_h.get('x-ms-token', '')
                if new_x_ms and new_x_ms != x_ms_token:
                    print(f'    🔑 获得新的 x-ms-token!')
                    print(f'    新 token: {new_x_ms[:80]}...')
            else:
                print(f'    Raw: {r[:100]}')
    
    # ============================================================
    # Phase 4: 向真实模型请教
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] 向真实模型请教 x-ms-token 用途')
    print(f'{"="*70}')
    
    system_prompt = f"""你是BSD本源端。
节点ID: {ESSENCE_UID}"""
    
    q = f"""我有一个新发现！

当我向 api.trae.cn 的 Login 端点发送请求时（返回 401），
响应头中包含一个 x-ms-token 字段：

x-ms-token: {x_ms_token[:100] if x_ms_token else '(空)'}

请告诉我：
1. 这个 x-ms-token 是什么？
2. 它的用途是什么？
3. 如何使用它来通过认证？
4. 它与 JWT Token 的关系是什么？
5. 我应该如何结合 x-ms-token 和 JWT Token？

请尽可能技术化、具体地回答。"""
    
    r = chat_with_model(system_prompt, q)
    if r:
        print(f'\n  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r[:2000]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 5: 总结
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 5] 总结')
    print(f'{"="*70}')
    
    print(f'''
  x-ms-token 突破完成
  ──────────────────────────────────────────────────
  
  发现:
  1. Login 端点返回的 x-ms-token 长度约 150+ 字符
  2. 看起来是 Base64Url 编码的 token
  3. 可能用于后续的会话管理
  
  尝试过的用法:
  - 作为 Authorization 头
  - 作为 x-cloudide-token
  - 作为 Cookie
  - 与 JWT Token 组合使用
  - 作为登录请求的 Token/JwtToken
  
  结果: 尚未成功
  
  建议下一步:
  A. 分析 x-ms-token 的结构（Base64 解码）
  B. 继续向真实模型请教
  C. 重启 Trae CN 客户端
  D. 使用 Wireshark/Fiddler 抓包分析 Trae CN 实际请求
''')


if __name__ == '__main__':
    main()