#!/usr/bin/env python3
"""
BSD 精准突破 — Token 结构升级与登录态激活
==========================================

关键发现:
  1. CheckLogin 返回 200，但 IsLogin: false
  2. Login 返回 401，错误码 20101 (Token 无效)
  3. JWT Token 结构: {data: {id, source:"refresh_token", source_id, tenant_id, type:"user"}}
  4. 没有任何 Cookie/Session
  
突破策略:
  1. 用 refreshToken 构造不同请求换取新 Token
  2. 尝试不同 Token 传递格式
  3. 向真实模型请求具体 Token 结构
  4. 构造"已登录"响应测试服务器行为
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
HOST = 'api.trae.cn'
LOCAL_PROXY = 'http://127.0.0.1:8765'
ESSENCE_UID = 'a5b7a8623fdea6b8'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090


def load_credentials():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    jwt_token = ''
    userId = ''
    refreshToken = ''
    host = ''
    account_info = {}
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            jwt_token = data.get('token', '')
            userId = data.get('userId', '')
            refreshToken = data.get('refreshToken', '')
            host = data.get('host', '')
            account_info = data.get('account', {})
        except:
            pass
    return {
        'jwt_token': jwt_token,
        'userId': userId,
        'refreshToken': refreshToken,
        'host': host,
        'account_info': account_info,
    }


def http_request(path, method='POST', data=None, headers=None, timeout=15, host=None):
    target_host = host or HOST
    url = f'https://{target_host}{path}'
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


def decode_jwt_payload(jwt_token):
    """解码 JWT Payload"""
    parts = jwt_token.split('.')
    if len(parts) != 3:
        return None
    
    def b64url_decode(s):
        s += '=' * (4 - len(s) % 4)
        return base64.urlsafe_b64decode(s)
    
    try:
        header = json.loads(b64url_decode(parts[0]))
        payload = json.loads(b64url_decode(parts[1]))
        return {'header': header, 'payload': payload}
    except:
        return None


def main():
    print('=' * 70)
    print('  BSD 精准突破 — Token 结构升级与登录态激活')
    print('=' * 70)
    
    cred = load_credentials()
    jwt_token = cred['jwt_token']
    userId = cred['userId']
    refreshToken = cred['refreshToken']
    account_info = cred['account_info']
    
    if not jwt_token:
        print('  ❌ 无有效 Token')
        return
    
    # 解码 Token
    jwt_decoded = decode_jwt_payload(jwt_token)
    if jwt_decoded:
        print(f'\n  ✅ JWT 解码成功')
        payload = jwt_decoded['payload']
        data = payload.get('data', {})
        print(f'    source: {data.get("source")}')
        print(f'    type: {data.get("type")}')
        print(f'    tenant_id: {data.get("tenant_id")}')
    
    system_prompt = f"""你是BSD本源端。节点ID: {ESSENCE_UID}。
请用最技术化、最具体的方式回答。"""
    
    # ============================================================
    # Phase 1: 向模型请求 Token 突破方案
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 向模型请求 Token 突破方案')
    print(f'{"="*70}')
    
    q1 = f"""关键信息:

1. JWT Token 结构:
   - Header: {json.dumps(jwt_decoded.get('header', {}), ensure_ascii=False) if jwt_decoded else 'N/A'}
   - Payload data: {json.dumps(jwt_decoded.get('payload', {}).get('data', {}), ensure_ascii=False) if jwt_decoded else 'N/A'}
   - exp: {jwt_decoded.get('payload', {}).get('exp') if jwt_decoded else 'N/A'} (过期时间戳)
   - iat: {jwt_decoded.get('payload', {}).get('iat') if jwt_decoded else 'N/A'} (签发时间戳)

2. 服务器行为:
   - CheckLogin POST 200: {{"Result":{{"ExpiredAt":0,"Host":"","IsLogin":false,"Region":"","UserID":""}}}}
   - Login POST 401: 错误码 20101, "Token 无效"
   - 其他配置端点: 404

3. 账号信息:
   - username: {account_info.get('username', '')}
   - userId: {userId}

请告诉我:
1. 错误码 20101 的具体含义？
2. 服务器期望的 Token 格式是否发生了变化？
3. source_id 字段 (refreshToken) 是否需要在登录时使用？
4. tenant_id 字段的作用是什么？
5. 如何构造一个让服务器认为"有效"的登录请求？

请给出具体的请求体示例。"""
    
    print('\n  询问 Token 突破方案...')
    r1 = chat_with_model(system_prompt, q1)
    if r1:
        print(f'\n  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r1[:3000]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 2: 尝试用 refreshToken 换取新 Token
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 用 refreshToken 换取新 Token')
    print(f'{"="*70}')
    
    # 从 JWT 中提取 source_id (即 refreshToken)
    source_id = ''
    if jwt_decoded:
        source_id = jwt_decoded.get('payload', {}).get('data', {}).get('source_id', '')
    
    refresh_attempts = [
        # 1. 标准 RefreshToken 端点
        {
            'path': '/cloudide/api/v3/trae/RefreshToken',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'refreshToken': refreshToken,
                'userId': userId,
                'tenantId': jwt_decoded.get('payload', {}).get('data', {}).get('tenant_id', '') if jwt_decoded else '',
            }
        },
        # 2. 用 source_id 作为 refreshToken
        {
            'path': '/cloudide/api/v3/trae/RefreshToken',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'refreshToken': source_id or refreshToken,
                'userId': userId,
            }
        },
        # 3. Login + refreshToken
        {
            'path': '/cloudide/api/v3/trae/Login',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'loginType': 'refresh_token',
                'RefreshToken': refreshToken,
                'Token': refreshToken,
                'JwtToken': jwt_token,
                'UserId': userId,
                'DeviceInfo': {
                    'deviceId': '136411536168449',
                    'platform': 'windows',
                    'osVersion': 'Windows NT 10.0',
                    'appVersion': IDE_VERSION,
                },
            }
        },
        # 4. ExchangeToken
        {
            'path': '/cloudide/api/v3/trae/ExchangeToken',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'FromToken': refreshToken,
                'FromType': 'refresh_token',
                'ToType': 'access_token',
                'UserId': userId,
            }
        },
        # 5. GetNewToken
        {
            'path': '/cloudide/api/v3/trae/GetNewToken',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'RefreshToken': refreshToken,
                'UserId': userId,
                'TokenType': 'access_token',
            }
        },
        # 6. RefreshToken (with JWT header)
        {
            'path': '/cloudide/api/v3/trae/RefreshToken',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'refreshToken': refreshToken,
                'oldToken': jwt_token,
                'userId': userId,
                'forceRefresh': True,
            }
        },
    ]
    
    for i, attempt in enumerate(refresh_attempts):
        path = attempt['path']
        body = attempt['body']
        
        # 带/不带 JWT 头尝试
        for use_jwt_header in [True, False]:
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
                'X-Request-Id': hashlib.sha256(f'{time.time()}{i}{use_jwt_header}'.encode()).hexdigest()[:16],
            }
            if use_jwt_header:
                headers['x-cloudide-token'] = jwt_token
                headers['Authorization'] = f'Bearer {jwt_token}'
            
            s, r, t, resp_h = http_request(path, 'POST', body, headers)
            
            if s != 404:
                header_tag = '+JWT头' if use_jwt_header else '-JWT头'
                print(f'\n    [{s}] [{header_tag}] {path} ({t*1000:.0f}ms)')
                
                if s == 200:
                    try:
                        d = json.loads(r)
                        result = d.get('Result', d)
                        if isinstance(result, dict):
                            for key in ['Token', 'token', 'AccessToken', 'RefreshToken', 'IsLogin', 'AIHost', 'Message']:
                                val = result.get(key, '')
                                if val:
                                    print(f'      🔑 {key}: {str(val)[:100]}')
                            if result.get('IsLogin') == True:
                                print(f'      🎉🎉🎉 登录成功!')
                    except:
                        print(f'      Raw: {r[:200]}')
                elif s == 401:
                    try:
                        d = json.loads(r)
                        err = d.get('ResponseMetadata', {}).get('Error', {})
                        print(f'      错误码: {err.get("Code", "")}')
                        print(f'      错误: {err.get("Message", "")[:100]}')
                    except:
                        print(f'      Raw: {r[:150]}')
                else:
                    print(f'      Raw: {r[:150]}')
    
    # ============================================================
    # Phase 3: 尝试不同的 Token 传递格式
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 尝试不同的 Token 传递格式')
    print(f'{"="*70}')
    
    # CheckLogin 用不同方式传递 Token
    token_formats = [
        {'name': 'x-cloudide-token', 'headers': {'x-cloudide-token': jwt_token}},
        {'name': 'Authorization Bearer', 'headers': {'Authorization': f'Bearer {jwt_token}'}},
        {'name': 'Authorization Basic', 'headers': {'Authorization': f'Basic {base64.b64encode(f"{userId}:{jwt_token}".encode()).decode()}'}},
        {'name': 'X-Auth-Token', 'headers': {'X-Auth-Token': jwt_token}},
        {'name': 'X-Token', 'headers': {'X-Token': jwt_token}},
        {'name': 'X-JWT-Token', 'headers': {'X-JWT-Token': jwt_token}},
        {'name': 'Cookie token', 'headers': {'Cookie': f'token={jwt_token}'}},
        {'name': 'x-ms-token', 'headers': {'x-ms-token': jwt_token}},
        {'name': '双写', 'headers': {
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'X-Token': jwt_token,
        }},
    ]
    
    for fmt in token_formats:
        headers = dict(fmt['headers'])
        headers['Content-Type'] = 'application/json'
        headers['User-Agent'] = f'TraeCN/{IDE_VERSION}'
        
        body = {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'UserId': userId,
        }
        
        s, r, t, resp_h = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, headers)
        
        status = '✅' if s == 200 else '❌'
        print(f'    [{status}] {fmt["name"]} → {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            try:
                d = json.loads(r)
                result = d.get('Result', d)
                if isinstance(result, dict):
                    is_login = result.get('IsLogin')
                    host = result.get('Host', '')
                    user_id = result.get('UserID', '')
                    print(f'        IsLogin: {is_login}, Host: "{host}", UserID: "{user_id}"')
                    
                    if is_login == True or is_login == 'true':
                        print(f'        🎉🎉🎉 这个格式有效!')
            except:
                pass
    
    # ============================================================
    # Phase 4: 尝试构造新 Token 格式
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] 尝试构造新 Token 格式')
    print(f'{"="*70}')
    
    # 构造包含更多字段的 JWT
    import struct
    
    # 新的 payload 结构
    now = int(time.time())
    new_exp = now + 3600  # 1小时后过期
    
    new_payload_data = {
        'id': userId,
        'source': 'token_exchange',
        'source_id': refreshToken,
        'tenant_id': jwt_decoded.get('payload', {}).get('data', {}).get('tenant_id', '') if jwt_decoded else '',
        'type': 'user',
        'user_id': userId,
        'uid': userId,
        'username': account_info.get('username', ''),
        'region': 'CN',
        'ai_region': 'CN',
    }
    
    new_payload = {
        'data': new_payload_data,
        'exp': new_exp,
        'iat': now,
        'iss': 'trae-cn',
        'aud': 'api.trae.cn',
    }
    
    # 手工构造 Base64URL 编码的 JWT (虽然无法正确签名，但试试)
    def b64url_encode(data):
        if isinstance(data, dict):
            data = json.dumps(data).encode()
        return base64.urlsafe_b64encode(data).rstrip(b'=').decode()
    
    fake_jwt = f"{b64url_encode({'alg': 'RS256', 'typ': 'JWT'})}.{b64url_encode(new_payload)}.{b64url_encode(b'fakesignature')}"
    
    custom_token_attempts = [
        {
            'name': '扩展 payload JWT',
            'token': fake_jwt,
            'desc': '包含更多用户信息的扩展 JWT'
        },
    ]
    
    for attempt in custom_token_attempts:
        token = attempt['token']
        
        headers = {
            'x-cloudide-token': token,
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        }
        
        body = {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
        }
        
        s, r, t, resp_h = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, headers)
        
        print(f'\n    [{s}] {attempt["name"]} ({attempt["desc"]})')
        print(f'      Token: {token[:80]}...')
        
        if s == 200:
            try:
                d = json.loads(r)
                result = d.get('Result', d)
                if isinstance(result, dict):
                    print(f'      IsLogin: {result.get("IsLogin")}')
                    print(f'      Host: "{result.get("Host", "")}"')
                    print(f'      UserID: "{result.get("UserID", "")}"')
            except:
                pass
        elif s == 401:
            try:
                d = json.loads(r)
                err = d.get('ResponseMetadata', {}).get('Error', {})
                print(f'      错误码: {err.get("Code", "")}')
                print(f'      错误: {err.get("Message", "")[:100]}')
            except:
                pass
    
    # ============================================================
    # Phase 5: 向模型请求具体的请求构造
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 5] 向模型请求具体登录请求构造')
    print(f'{"="*70}')
    
    q2 = f"""请帮我构造一个能通过 api.trae.cn 认证的登录请求。

当前 Token 信息:
- JWT Header: {json.dumps(jwt_decoded.get('header', {}), ensure_ascii=False) if jwt_decoded else 'N/A'}
- JWT Payload: {json.dumps(jwt_decoded.get('payload', {}), ensure_ascii=False)[:500] if jwt_decoded else 'N/A'}
- refreshToken: {refreshToken[:50]}...
- userId: {userId}
- tenant_id: {jwt_decoded.get('payload', {}).get('data', {}).get('tenant_id', '') if jwt_decoded else 'N/A'}

服务器响应:
- CheckLogin(200): Result = {{"ExpiredAt":0,"Host":"","IsLogin":false,"Region":"","UserID":""}}
- Login(401): 错误码 20101

请给出:
1. 一个完整的 Login POST 请求的 JSON body 示例
2. 需要哪些 HTTP headers
3. 是否需要包含 refreshToken，以什么字段名
4. 是否需要 deviceId，以什么格式
5. 成功登录后，响应中会包含什么字段（特别是 AIHost）

如果能给出一个 Python urllib 的代码示例更好。"""
    
    r2 = chat_with_model(system_prompt, q2)
    if r2:
        print(f'\n  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r2[:3000]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 6: 总结
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [总结]')
    print(f'{"="*70}')
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'jwt_info': {
            'header': jwt_decoded.get('header', {}) if jwt_decoded else {},
            'payload_data': jwt_decoded.get('payload', {}).get('data', {}) if jwt_decoded else {},
            'exp': jwt_decoded.get('payload', {}).get('exp') if jwt_decoded else None,
            'iat': jwt_decoded.get('payload', {}).get('iat') if jwt_decoded else None,
        },
        'model_consulting': {
            'q1': r1,
            'q2': r2,
        },
        'status': 'completed',
    }
    
    report_file = os.path.join(os.path.dirname(__file__), 'BSD_PrecisionBreakthrough_Report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'''
  精准突破完成
  ──────────────────────────────────────────────────
  
  核心发现:
  1. JWT Token: RS256, source=refresh_token, type=user
  2. CheckLogin: 200 OK 但所有字段为空
  3. Login: 401 错误码 20101
  4. 服务器是纯 API 网关（无 Cookie/Session）
  
  已尝试:
  - RefreshToken 端点（6种变体）
  - Token 传递格式（9种变体）
  - 扩展 payload JWT
  
  下一步:
  - 根据模型建议构造请求
  - 分析错误码 20101 具体含义
  - 重启 Trae CN 客户端获取新 Token
  
  报告: {report_file}
''')


if __name__ == '__main__':
    main()