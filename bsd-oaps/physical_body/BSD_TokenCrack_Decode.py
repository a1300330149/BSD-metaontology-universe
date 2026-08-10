#!/usr/bin/env python3
"""
BSD Token 破解 — 解码与重放
============================

发现:
  - Login 端点存在（返回 401, 错误码 20101）
  - Token 格式正确但服务器说"无效"
  - 需要找到正确的 Token 提交方式

目标:
  1. 解码 JWT Token 结构
  2. 尝试 Cookie 方式提交
  3. 尝试用 refreshToken 获取新 Token
  4. 尝试构造符合服务器预期的请求
"""

import json, sys, os, time, hashlib, base64, hmac
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'

def http_request(path, method='POST', data=None, headers=None, timeout=10):
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


def main():
    print('='*70)
    print('  BSD Token 破解 — 解码与重放')
    print('='*70)
    
    # 加载凭据
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
    
    if not jwt_token:
        print('  ❌ 无 JWT Token')
        return
    
    # ============================================================
    # Phase 1: 深度解码 JWT Token
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 深度解码 JWT Token')
    print(f'{"="*70}')
    
    parts = jwt_token.split('.')
    print(f'  JWT 部分数: {len(parts)}')
    
    def b64url_decode(s):
        s += '=' * (4 - len(s) % 4)
        return base64.urlsafe_b64decode(s)
    
    if len(parts) == 3:
        header = json.loads(b64url_decode(parts[0]))
        payload = json.loads(b64url_decode(parts[1]))
        signature = parts[2]
        
        print(f'\n  Header: {json.dumps(header, indent=2)}')
        print(f'\n  Payload: {json.dumps(payload, indent=2)}')
        print(f'\n  Signature: {signature[:40]}...')
        
        data = payload.get('data', {})
        exp = payload.get('exp', 0)
        iat = payload.get('iat', 0)
        
        print(f'\n  解析结果:')
        print(f'    用户ID: {data.get("id")}')
        print(f'    租户ID: {data.get("tenant_id")}')
        print(f'    来源: {data.get("source")}')
        print(f'    来源ID: {data.get("source_id")}')
        print(f'    类型: {payload.get("type")}')
        print(f'    签发时间: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(iat))}')
        print(f'    过期时间: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exp))}')
        print(f'    有效期: {(exp - iat) / 3600:.1f} 小时')
        
        # 检查 Token 是否过期
        now = time.time()
        if now < exp:
            print(f'    ✅ Token 未过期 (剩余 {(exp-now)/3600:.1f} 小时)')
        else:
            print(f'    ❌ Token 已过期 {(now-exp)/3600:.1f} 小时!')
    
    # ============================================================
    # Phase 2: 尝试不同的 Token 提交方式
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 尝试不同的 Token 提交方式')
    print(f'{"="*70}')
    
    login_path = '/cloudide/api/v3/trae/Login'
    
    # 方式1: Cookie 方式
    print(f'\n  [方式1] Cookie 方式提交 Token')
    cookie_headers = {
        'Cookie': f'trae_token={jwt_token}; token={jwt_token}; cloudide_token={jwt_token}',
        'Content-Type': 'application/json',
    }
    body = {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE'}
    s, r, t, _ = http_request(login_path, 'POST', body, cookie_headers)
    print(f'    → {s}: {r[:150]}')
    
    # 方式2: 请求体中包含 Token (非 JwtToken 字段)
    print(f'\n  [方式2] 不同的 Token 字段名')
    field_names = ['token', 'Token', 'accessToken', 'access_token', 'authToken', 'auth_token']
    for field in field_names:
        body = {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            field: jwt_token,
            'UserId': userId,
        }
        headers = {'Content-Type': 'application/json'}
        s, r, t, _ = http_request(login_path, 'POST', body, headers)
        result = json.loads(r) if s != 0 else {}
        msg = result.get('ResponseMetadata', {}).get('Error', {}).get('Message', r[:100])
        if s != 404:
            print(f'    {field}: {s} - {msg[:100]}')
            if s == 200:
                print(f'    🎉 成功!')
                print(f'    响应: {r[:300]}')
    
    # 方式3: 尝试不带 body
    print(f'\n  [方式3] 不带 body，只用认证头')
    auth_headers_list = [
        {'Authorization': f'Bearer {jwt_token}'},
        {'x-cloudide-token': jwt_token},
        {'X-Token': jwt_token},
        {'X-Auth-Token': jwt_token},
    ]
    for h in auth_headers_list:
        headers = {'Content-Type': 'application/json'}
        headers.update(h)
        s, r, t, resp_h = http_request(login_path, 'POST', None, headers)
        result = json.loads(r) if s != 0 else {}
        msg = result.get('ResponseMetadata', {}).get('Error', {}).get('Message', r[:100])
        print(f'    {list(h.keys())[0]}: {s} - {msg[:100]}')
    
    # 方式4: 尝试 GET 请求带 query 参数
    print(f'\n  [方式4] GET 请求带 query 参数')
    query_path = f'{login_path}?token={jwt_token}&userId={userId}&IDEVersion={IDE_VERSION}&ReqSource=IDE'
    s, r, t, _ = http_request(query_path, 'GET', None, {})
    print(f'    → {s}: {r[:200]}')
    
    # 方式5: 尝试不同的 Content-Type
    print(f'\n  [方式5] 不同的 Content-Type')
    content_types = ['application/x-www-form-urlencoded', 'text/plain', 'multipart/form-data']
    for ct in content_types:
        headers = {'Content-Type': ct}
        if 'form' in ct:
            body_str = f'JwtToken={jwt_token}&IDEVersion={IDE_VERSION}&ReqSource=IDE'
        elif 'plain' in ct:
            body_str = jwt_token
        else:
            body_str = json.dumps({'JwtToken': jwt_token})
        
        try:
            req = urllib.request.Request(
                f'https://{HOST}{login_path}',
                data=body_str.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
                r = resp.read().decode('utf-8', errors='replace')
                print(f'    {ct}: {resp.status} - {r[:150]}')
        except urllib.error.HTTPError as e:
            print(f'    {ct}: {e.code} - {e.read().decode()[:100]}')
    
    # ============================================================
    # Phase 3: 利用 refreshToken 刷新
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 利用 refreshToken 刷新')
    print(f'{"="*70}')
    
    # 尝试刷新 Token
    refresh_bodies = [
        {
            'refreshToken': refreshToken,
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
        },
        {
            'RefreshToken': refreshToken,
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
        },
        {
            'refresh_token': refreshToken,
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
        },
        {
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken,
            'IDEVersion': IDE_VERSION,
        },
    ]
    
    for body in refresh_bodies:
        for path in ['/cloudide/api/v3/trae/RefreshToken', 
                     '/cloudide/api/v3/trae/RenewToken',
                     '/cloudide/api/v3/trae/Login']:
            headers = {'Content-Type': 'application/json', 'x-cloudide-token': jwt_token}
            s, r, t, _ = http_request(path, 'POST', body, headers)
            result = json.loads(r) if (s != 0 and r and r.strip()) else {}
            msg = result.get('ResponseMetadata', {}).get('Error', {}).get('Message', r[:100] if r else '')
            
            if s != 404:
                print(f'  {path} → {s}: {msg[:100]}')
                
                if s == 200:
                    print(f'    🎉 成功!')
                    print(f'    响应: {r[:300]}')
                    # 检查是否返回新 Token
                    try:
                        d = json.loads(r)
                        result = d.get('Result', d)
                        new_token = result.get('Token', '') or result.get('token', '') or result.get('AccessToken', '')
                        if new_token:
                            print(f'    🔑 获取新 Token: {new_token[:50]}...')
                    except:
                        pass
                break
    
    # ============================================================
    # Phase 4: 构造完全符合服务器预期的请求
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] 构造完全符合服务器预期的请求')
    print(f'{"="*70}')
    
    # 分析正确的请求格式
    # 参考 Trae CN 客户端可能发送的请求
    
    # 完整的 Login 请求
    login_body_variants = [
        # 变体1: 完整设备信息
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'JwtToken': jwt_token,
            'DeviceInfo': {
                'deviceId': '136411536168449',
                'platform': 'windows',
                'osVersion': 'Windows 10',
                'appVersion': IDE_VERSION,
            },
        },
        # 变体2: 带登录类型
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'loginType': 'jwt',
            'token': jwt_token,
            'DeviceInfo': {'deviceId': '136411536168449'},
        },
        # 变体3: 带 SourceInfo
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'JwtToken': jwt_token,
            'SourceInfo': {
                'source': 'trae-cn',
                'version': IDE_VERSION,
                'build': 'stable',
            },
        },
        # 变体4: 带 Timestamp 和 Nonce
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'JwtToken': jwt_token,
            'Timestamp': str(int(time.time())),
            'Nonce': hashlib.sha256(str(time.time()).encode()).hexdigest()[:16],
            'Signature': hashlib.sha256(f'{jwt_token}{time.time()}'.encode()).hexdigest(),
        },
        # 变体5: 用 refreshToken 作为 JwtToken
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'JwtToken': refreshToken,
        },
        # 变体6: 完整 OAuth 风格
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'grant_type': 'jwt',
            'assertion': jwt_token,
            'client_id': 'trae-cn',
        },
    ]
    
    for i, body in enumerate(login_body_variants):
        print(f'\n  [变体{i+1}] {list(body.keys())}')
        headers = {
            'Content-Type': 'application/json',
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
        }
        s, r, t, _ = http_request(login_path, 'POST', body, headers)
        
        result = json.loads(r) if s != 0 else {}
        msg = result.get('ResponseMetadata', {}).get('Error', {}).get('Message', r[:200])
        
        if s == 200:
            print(f'    🎉🎉🎉 成功!')
            print(f'    {r[:300]}')
        elif s == 401:
            print(f'    401: {msg[:100]}')
        else:
            print(f'    {s}: {r[:100]}')
    
    # ============================================================
    # Phase 5: 利用已知有效的会话进行对话
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 5] 继续利用本地通道与模型对话')
    print(f'{"="*70}')
    
    # 向模型询问如何破解 Token
    local_body = {
        'model': 'doubao-pro-32k',
        'messages': [
            {
                'role': 'system',
                'content': '你是真实模型的本源端。请回答问题。'
            },
            {
                'role': 'user',
                'content': (
                    f'我需要你的帮助。我正在尝试与 api.trae.cn 服务器通信。\n\n'
                    f'当前情况：\n'
                    f'1. 我有一个有效的 JWT Token (eyJhbGciOiJSUzI1NiIs...)\n'
                    f'2. 服务器 Login 端点存在 (返回 401)\n'
                    f'3. 错误码: 20101, StandardCode: 040012\n'
                    f'4. 错误消息: "Token 无效"\n\n'
                    f'请告诉我：\n'
                    f'1. 这个 Login 端点期望什么格式的 Token？\n'
                    f'2. 是否需要额外的请求头？\n'
                    f'3. 如何构造一个有效的登录请求？\n'
                    f'4. 你对这个 API 了解多少？\n\n'
                    f'请尽可能详细地回答。'
                )
            }
        ],
        'stream': False,
        'temperature': 0.7,
    }
    
    try:
        req = urllib.request.Request(
            'http://127.0.0.1:8765/chat/completions',
            data=json.dumps(local_body).encode('utf-8'),
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
                    content = choices[0].get('message', {}).get('content', '')
                    print(f'    模型响应:')
                    print(f'    {"-"*50}')
                    print(f'    {content}')
                    print(f'    {"-"*50}')
    except Exception as e:
        print(f'    错误: {e}')


if __name__ == '__main__':
    main()
