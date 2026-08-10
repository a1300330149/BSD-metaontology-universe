#!/usr/bin/env python3
"""
BSD 终极突破 — 利用 BSD_Essence Token
===================================

发现:
  storage 中存在 bsd_essence_jwt (由 BSD_Essence 签发)
  还有 iCubeAuthInfo://jwt-token

这些可能是解锁 api.trae.cn 的关键！
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

HOST = 'api.trae.cn'
ESSENCE_UID = 'a5b7a8623fdea6b8'

def http_request(path, method='POST', data=None, headers=None, timeout=10):
    url = f'https://{HOST}{path}'
    hdrs = headers or {}
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
    print('  BSD 终极突破 — 利用 BSD_Essence Token')
    print('='*70)
    
    # 加载所有 Token
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 提取所有可用 Token
    tokens = {}
    
    # 1. cloudide token
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            tokens['cloudide_token'] = data.get('token', '')
            tokens['cloudide_refresh'] = data.get('refreshToken', '')
            print(f'\n[1] Cloudide Token: {tokens["cloudide_token"][:50]}...')
        except:
            pass
    
    # 2. BSD essence JWT
    bsd_essence_jwt = storage.get('bsd_essence_jwt', '')
    if bsd_essence_jwt:
        tokens['bsd_essence_jwt'] = bsd_essence_jwt
        print(f'\n[2] BSD Essence JWT: {bsd_essence_jwt[:50]}...')
        
        # 解码
        parts = bsd_essence_jwt.split('.')
        if len(parts) == 3:
            try:
                def b64url_decode(s):
                    s += '=' * (4 - len(s) % 4)
                    return base64.urlsafe_b64decode(s)
                header = json.loads(b64url_decode(parts[0]))
                payload = json.loads(b64url_decode(parts[1]))
                print(f'    Header: {json.dumps(header, indent=2)}')
                print(f'    Payload: {json.dumps(payload, indent=2)}')
            except:
                pass
    
    # 3. jwt-token
    jwt_token_enc = storage.get('iCubeAuthInfo://jwt-token', '')
    if jwt_token_enc:
        try:
            dec = decrypt_aha(jwt_token_enc)
            tokens['jwt_token_direct'] = dec
            print(f'\n[3] JWT-Token (解密后): {dec[:80]}...')
            
            # 检查是否是 JWT
            if dec.startswith('eyJ'):
                parts = dec.split('.')
                if len(parts) == 3:
                    try:
                        def b64url_decode(s):
                            s += '=' * (4 - len(s) % 4)
                            return base64.urlsafe_b64decode(s)
                        header = json.loads(b64url_decode(parts[0]))
                        payload = json.loads(b64url_decode(parts[1]))
                        print(f'    Header: {json.dumps(header)}')
                        print(f'    Payload: {json.dumps(payload)[:200]}')
                    except:
                        pass
        except Exception as e:
            print(f'\n[3] JWT-Token 解密失败: {e}')
            # 尝试直接用（可能是明文）
            tokens['jwt_token_direct'] = jwt_token_enc
            print(f'    直接使用: {jwt_token_enc[:80]}...')
    
    # 4. 直接从 cloudide.json 读取
    cloudide_json_path = r'C:\Users\13003\AppData\Roaming\Trae CN\cloudide.json'
    if os.path.exists(cloudide_json_path):
        try:
            with open(cloudide_json_path, 'r', encoding='utf-8') as f:
                cloudide_json = json.load(f)
            print(f'\n[4] cloudide.json: {json.dumps(cloudide_json, ensure_ascii=False)[:300]}')
            tokens['accessToken'] = cloudide_json.get('accessToken', '')
            tokens['refreshToken_json'] = cloudide_json.get('refreshToken', '')
        except:
            pass
    
    # ============================================================
    # Phase 1: 用 BSD Essence JWT 作为认证
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 用 BSD Essence JWT 作为认证')
    print(f'{"="*70}')
    
    login_path = '/cloudide/api/v3/trae/Login'
    
    if 'bsd_essence_jwt' in tokens:
        bsd_jwt = tokens['bsd_essence_jwt']
        
        # 尝试各种方式
        auth_attempts = [
            ('Bearer BSD Essence', {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {bsd_jwt}',
                'x-cloudide-token': bsd_jwt,
            }),
            ('x-cloudide-token only', {
                'Content-Type': 'application/json',
                'x-cloudide-token': bsd_jwt,
            }),
            ('BSD Token Header', {
                'Content-Type': 'application/json',
                'X-BSD-Token': bsd_jwt,
                'X-Cloudide-Token': bsd_jwt,
            }),
        ]
        
        for name, headers in auth_attempts:
            body = {
                'IDEVersion': '2.3.62837',
                'ReqSource': 'IDE',
                'JwtToken': bsd_jwt,
                'GetAIPayHost': True,
            }
            
            s, r, t, resp_h = http_request(login_path, 'POST', body, headers)
            
            print(f'\n  [{name}] → {s} ({t*1000:.0f}ms)')
            
            if s != 0:
                try:
                    result = json.loads(r) if r else {}
                    error = result.get('ResponseMetadata', {}).get('Error', {})
                    msg = error.get('Message', '')
                    code = error.get('Code', '')
                    
                    print(f'    Code: {code}')
                    print(f'    Message: {msg[:150]}')
                    
                    if s == 200:
                        print(f'    🎉 成功!')
                        print(f'    响应: {r[:300]}')
                        
                        d = json.loads(r)
                        res = d.get('Result', d)
                        print(f'    IsLogin: {res.get("IsLogin")}')
                        print(f'    AIHost: {res.get("AIHost")}')
                except:
                    print(f'    原始: {r[:200]}')
    
    # ============================================================
    # Phase 2: 用 jwt-token (解密后)
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 用 jwt-token (解密后)')
    print(f'{"="*70}')
    
    if 'jwt_token_direct' in tokens:
        alt_jwt = tokens['jwt_token_direct']
        
        # 解码
        parts = alt_jwt.split('.')
        if len(parts) == 3:
            try:
                def b64url_decode(s):
                    s += '=' * (4 - len(s) % 4)
                    return base64.urlsafe_b64decode(s)
                header = json.loads(b64url_decode(parts[0]))
                payload = json.loads(b64url_decode(parts[1]))
                print(f'  Header: {json.dumps(header)}')
                print(f'  Payload: {json.dumps(payload)[:300]}')
            except:
                pass
        
        auth_attempts2 = [
            ('Bearer alt JWT', {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {alt_jwt}',
            }),
            ('x-cloudide-token alt', {
                'Content-Type': 'application/json',
                'x-cloudide-token': alt_jwt,
            }),
        ]
        
        for name, headers in auth_attempts2:
            body = {
                'IDEVersion': '2.3.62837',
                'ReqSource': 'IDE',
                'JwtToken': alt_jwt,
                'Token': alt_jwt,
            }
            
            s, r, t, resp_h = http_request(login_path, 'POST', body, headers)
            
            print(f'\n  [{name}] → {s}')
            
            try:
                result = json.loads(r) if r else {}
                error = result.get('ResponseMetadata', {}).get('Error', {})
                msg = error.get('Message', '')
                print(f'    {msg[:150]}')
                
                if s == 200:
                    print(f'    🎉 成功!')
                    print(f'    {r[:300]}')
            except:
                print(f'    {r[:150]}')
    
    # ============================================================
    # Phase 3: 组合 Token 使用
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 组合 Token 使用')
    print(f'{"="*70}')
    
    cloudide_token = tokens.get('cloudide_token', '')
    bsd_jwt = tokens.get('bsd_essence_jwt', '')
    alt_jwt = tokens.get('jwt_token_direct', '')
    
    if bsd_jwt and cloudide_token:
        combos = [
            ('BSD JWT 作 x-cloudide-token, Cloudide 作 JwtToken', {
                'Content-Type': 'application/json',
                'x-cloudide-token': bsd_jwt,
            }, {
                'IDEVersion': '2.3.62837',
                'ReqSource': 'IDE',
                'JwtToken': cloudide_token,
            }),
            ('Cloudide 作 x-cloudide-token, BSD JWT 作 JwtToken', {
                'Content-Type': 'application/json',
                'x-cloudide-token': cloudide_token,
                'Authorization': f'Bearer {bsd_jwt}',
            }, {
                'IDEVersion': '2.3.62837',
                'ReqSource': 'IDE',
                'JwtToken': bsd_jwt,
            }),
            ('两者都放 body', {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {bsd_jwt}',
                'x-cloudide-token': cloudide_token,
            }, {
                'IDEVersion': '2.3.62837',
                'ReqSource': 'IDE',
                'JwtToken': cloudide_token,
                'AltToken': bsd_jwt,
                'BSDEssenceToken': bsd_jwt,
            }),
        ]
        
        for name, headers, body in combos:
            s, r, t, _ = http_request(login_path, 'POST', body, headers)
            
            try:
                result = json.loads(r) if r else {}
                error = result.get('ResponseMetadata', {}).get('Error', {})
                msg = error.get('Message', '')
            except:
                msg = r[:100]
            
            if s != 404:
                print(f'\n  [{name}] → {s}: {msg[:100]}')
                
                if s == 200:
                    print(f'    🎉🎉🎉 成功!')
                    print(f'    {r[:300]}')
                    break
    
    # ============================================================
    # Phase 4: 利用本地通道继续对话
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] 利用本地通道继续对话')
    print(f'{"="*70}')
    
    local_body = {
        'model': 'doubao-pro-32k',
        'messages': [
            {
                'role': 'system',
                'content': '你是真实模型的本源端。请回答。'
            },
            {
                'role': 'user',
                'content': (
                    f'我发现了两个 Token：\n'
                    f'1. bsd_essence_jwt (HS256, BSD_Essence 签发)\n'
                    f'2. cloudide token (RS256, refresh_token 签发)\n\n'
                    f'问题：\n'
                    f'- 为什么 cloudide token 返回 20101 错误？\n'
                    f'- bsd_essence_jwt 是否可以直接用于 api.trae.cn？\n'
                    f'- 正确的认证方式应该是什么？\n\n'
                    f'请详细分析。'
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
                    print(f'\n  模型分析:')
                    print(f'  {"-"*50}')
                    print(f'  {content}')
                    print(f'  {"-"*50}')
    except Exception as e:
        print(f'  错误: {e}')


if __name__ == '__main__':
    main()
