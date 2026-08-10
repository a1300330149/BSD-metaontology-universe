#!/usr/bin/env python3
"""
BSD × Trae CN — 服务器端本源验证 V4
==================================

核心突破:
  1. AHA 解密 icube.cloudide 得到了真正的服务器凭证
  2. Token 有效 (RS256 JWT, exp: 2026-08-18)
  3. RefreshToken 有效 (exp: 2027-01-31)
  4. API 主机: https://api.trae.cn

目标:
  1. 用有效 token 验证 CheckLogin 链路
  2. 尝试用 RefreshToken 换取本源身份的 token
  3. 通过服务器端真实验证实现本源登录

版本: V4.0 · 基于真实服务器凭证
"""

import os, json, base64, hashlib, time, struct
from datetime import datetime
import urllib.request
import urllib.error
import ssl
import sys

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

# ==================== 配置 ====================
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

IDE_VERSION = '2.3.62837'


def http_request(url, method='GET', data=None, headers=None, timeout=15):
    """通用 HTTP 请求"""
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION} (BSD-Essence)')
    hdrs.setdefault('Content-Type', 'application/json')
    
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            resp_body = resp.read().decode('utf-8', errors='replace')
            return {'status': resp.status, 'body': resp_body, 'ok': True}
    except urllib.error.HTTPError as e:
        resp_body = e.read().decode('utf-8', errors='replace')
        return {'status': e.code, 'body': resp_body, 'ok': False, 'error': str(e)}
    except Exception as e:
        return {'status': 0, 'body': '', 'ok': False, 'error': str(e)}


def parse_response(resp):
    if resp['body']:
        try:
            return json.loads(resp['body'])
        except:
            return {'raw': resp['body'][:500]}
    return {}


def load_credentials():
    """从 storage.json 解密获取真实凭证"""
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 解密 cloudide 数据 - 包含真实 token
    cloudide_key = 'iCubeAuthInfo://icube.cloudide'
    cloudide_enc = storage.get(cloudide_key, '')
    
    # 同时解密 icube-dc 获取密钥对
    dc_key = 'iCubeAuthInfo://icube-dc:516094651277160'
    dc_enc = storage.get(dc_key, '')
    
    credentials = {}
    
    if cloudide_enc:
        try:
            cloudide_dec = decrypt_aha(cloudide_enc)
            cloudide_data = json.loads(cloudide_dec)
            credentials['token'] = cloudide_data.get('token', '')
            credentials['refreshToken'] = cloudide_data.get('refreshToken', '')
            credentials['expiredAt'] = cloudide_data.get('expiredAt', '')
            credentials['refreshExpiredAt'] = cloudide_data.get('refreshExpiredAt', '')
            credentials['userId'] = cloudide_data.get('userId', '')
            credentials['host'] = cloudide_data.get('host', '')
            credentials['account'] = cloudide_data.get('account', {})
            print(f'  ✅ 解密成功: userId={credentials["userId"]}, exp={credentials["expiredAt"]}')
        except Exception as e:
            print(f'  ❌ cloudide 解密失败: {e}')
    
    if dc_enc:
        try:
            dc_dec = decrypt_aha(dc_enc)
            dc_data = json.loads(dc_dec)
            credentials['privateKeyPEM'] = dc_data.get('privateKeyPEM', '')
            credentials['publicKeyPEM'] = dc_data.get('publicKeyPEM', '')
            print(f'  ✅ 密钥对解密成功')
        except Exception as e:
            print(f'  ❌ dc 解密失败: {e}')
    
    return credentials


def check_login(host, token, req_source='IDE'):
    """
    CheckLogin 协议 (来自 main.js):
    URL: {host}/cloudide/api/v3/trae/CheckLogin
    Headers: { "x-cloudide-token": token }
    Body: { IDEVersion, ReqSource, GetAIPayHost: true }
    """
    host_clean = host.replace('https://', '').replace('http://', '')
    url = f'https://{host_clean}/cloudide/api/v3/trae/CheckLogin'
    
    headers = {'x-cloudide-token': token}
    data = {'IDEVersion': IDE_VERSION, 'ReqSource': req_source, 'GetAIPayHost': True}
    
    print(f'  POST {url}')
    print(f'  x-cloudide-token: {token[:60]}...')
    
    resp = http_request(url, 'POST', data, headers)
    parsed = parse_response(resp)
    
    result = parsed.get('Result', {})
    is_login = result.get('IsLogin', 'N/A')
    user_id = result.get('UserID', '')
    expired_at = result.get('ExpiredAt', 0)
    
    print(f'  HTTP: {resp["status"]}')
    print(f'  IsLogin: {is_login}')
    print(f'  UserID: {user_id}')
    print(f'  ExpiredAt: {expired_at}')
    
    if resp['body'] and len(resp['body']) < 500:
        print(f'  Full Response: {resp["body"]}')
    
    return resp, parsed


def exchange_refresh_token(host, refresh_token, private_key_pem, public_key_pem):
    """
    ExchangeToken 协议 (来自 main.js):
    URL: {host}/trae/api/v3/oauth/ExchangeToken
    需要: ClientID, RefreshToken, DeviceInfo(RSA加密), DeviceProof(签名)
    """
    import hashlib
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.backends import default_backend
    
    host_clean = host.replace('https://', '').replace('http://', '')
    url = f'https://{host_clean}/trae/api/v3/oauth/ExchangeToken'
    
    # ClientID (从 main.js Vv 函数获取)
    client_id = 'ono9krqynydwx5'
    
    # 加载密钥
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode('utf-8'), password=None, backend=default_backend()
    )
    
    # DeviceInfo: 用公钥加密随机设备ID
    device_id = os.urandom(16).hex()
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'), backend=default_backend()
    )
    encrypted_device = public_key.encrypt(
        device_id.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    device_info = base64.b64encode(encrypted_device).decode('utf-8')
    
    # DeviceProof: 签名 (简化版)
    timestamp = str(int(time.time()))
    nonce = os.urandom(8).hex()
    sign_str = f'POST\\n/trae/api/v3/oauth/ExchangeToken\\n{client_id}\\n{refresh_token}\\n{timestamp}\\n{nonce}'
    
    signature = private_key.sign(
        sign_str.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
    data = {
        'ClientID': client_id,
        'ClientSecret': '',
        'RefreshToken': refresh_token,
        'DeviceInfo': device_info,
        'DeviceProof': {
            'Signature': signature_b64,
            'Timestamp': timestamp,
            'Nonce': nonce
        },
        'IDEVersion': IDE_VERSION
    }
    
    print(f'  POST {url}')
    print(f'  ClientID: {client_id}')
    print(f'  RefreshToken: {refresh_token[:40]}...')
    print(f'  DeviceInfo: {device_info[:40]}...')
    
    resp = http_request(url, 'POST', data, {'Content-Type': 'application/json'})
    return resp, parse_response(resp)


def try_login_paths(host, token, refresh_token, private_key, public_key):
    """尝试多种登录路径"""
    host_clean = host.replace('https://', '').replace('http://', '')
    
    paths = [
        ('/cloudide/api/v3/trae/CheckLogin', {'x-cloudide-token': token}),
        ('/cloudide/api/v3/trae/LoginByJwt', {'Content-Type': 'application/json'}),
        ('/cloudide/api/v3/trae/LoginByCode', {'Content-Type': 'application/json'}),
        ('/trae/api/v3/oauth/ExchangeToken', {'Content-Type': 'application/json'}),
        ('/cloudide/api/v3/trae/GetUserInfo', {'x-cloudide-token': token}),
        ('/cloudide/api/v3/trae/GetAIPayHost', {'x-cloudide-token': token}),
    ]
    
    for path, headers in paths:
        url = f'https://{host_clean}{path}'
        
        if 'ExchangeToken' in path:
            # ExchangeToken 需要不同的 body
            print(f'\\n  --- POST {path} ---')
            print(f'  状态: 跳过 (需要完整签名实现)')
            continue
        
        if 'LoginByJwt' in path:
            body = {'jwtToken': token, 'provider': 'icube.cloudide', 'IDEVersion': IDE_VERSION}
        elif 'LoginByCode' in path:
            body = {'code': token[:50], 'provider': 'icube.cloudide', 'IDEVersion': IDE_VERSION}
        elif 'GetUserInfo' in path:
            body = {'IDEVersion': IDE_VERSION}
        elif 'GetAIPayHost' in path:
            body = {'IDEVersion': IDE_VERSION}
        else:
            body = {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}
        
        resp = http_request(url, 'POST', body, headers)
        parsed = parse_response(resp)
        
        status = resp['status']
        result_code = parsed.get('code', parsed.get('ResponseMetadata', {}).get('Error', {}).get('Code', ''))
        short_body = resp['body'][:200] if resp['body'] else ''
        
        print(f'\\n  POST {path}')
        print(f'  Status: {status}, Code: {result_code}')
        print(f'  Response: {short_body}')
        
        if status == 200 and 'IsLogin' in str(parsed.get('Result', {})):
            is_login = parsed['Result'].get('IsLogin', 'N/A')
            user_id = parsed['Result'].get('UserID', '')
            print(f'  ⭐ IsLogin: {is_login}, UserID: {user_id}')


def main():
    print('='*70)
    print('  BSD × Trae CN — 服务器端本源验证 V4')
    print('  基于 AHA 解密的真实服务器凭证')
    print('='*70)
    
    # 1. 加载并解密凭证
    print('\\n📡 [Step 1] 加载凭证')
    creds = load_credentials()
    
    if not creds.get('token'):
        print('❌ 无有效 token，终止')
        return
    
    host = creds.get('host', 'https://api.trae.cn')
    token = creds['token']
    refresh_token = creds.get('refreshToken', '')
    user_id = creds.get('userId', '')
    
    # 2. 用真实 token 验证 CheckLogin
    print(f'\\n{"="*60}')
    print(f'  [Step 2] CheckLogin 验证 (真实 token)')
    print(f'{"="*60}')
    
    resp, parsed = check_login(host, token)
    
    result = parsed.get('Result', {})
    is_login = result.get('IsLogin', False)
    
    if is_login:
        print(f'\\n  🎉🎉🎉 服务器承认传统身份登录!')
        print(f'     UserID: {result.get("UserID")}')
        print(f'     ExpiredAt: {result.get("ExpiredAt")}')
    else:
        print(f'\\n  ⚠️ 服务器返回 IsLogin=false')
        print(f'     这说明 token 可能已过期或被吊销')
    
    # 3. 检查 token 过期时间
    print(f'\\n{"="*60}')
    print(f'  [Step 3] Token 有效期检查')
    print(f'{"="*60}')
    
    exp = creds.get('expiredAt', '')
    refresh_exp = creds.get('refreshExpiredAt', '')
    
    print(f'  Access Token 过期: {exp}')
    print(f'  Refresh Token 过期: {refresh_exp}')
    
    if exp:
        try:
            exp_dt = datetime.fromisoformat(exp.replace('Z', '+00:00'))
            now = datetime.now(exp_dt.tzinfo)
            remaining = exp_dt - now
            print(f'  剩余有效时间: {remaining}')
            if remaining.total_seconds() < 0:
                print(f'  ⚠️ Token 已过期! 需要用 RefreshToken 换取新 token')
        except:
            pass
    
    # 4. 尝试用 RefreshToken 换取新 Access Token
    print(f'\\n{"="*60}')
    print(f'  [Step 4] ExchangeToken (用 RefreshToken 换新 token)')
    print(f'{"="*60}')
    
    if refresh_token and creds.get('privateKeyPEM') and creds.get('publicKeyPEM'):
        print(f'  尝试用 RefreshToken 换取新 Access Token...')
        try:
            resp, parsed = exchange_refresh_token(
                host, refresh_token, 
                creds['privateKeyPEM'], creds['publicKeyPEM']
            )
            print(f'  HTTP: {resp["status"]}')
            print(f'  Response: {resp["body"][:500]}')
            
            if resp['status'] == 200:
                # 检查是否返回了新 token
                if isinstance(parsed, dict):
                    new_token = parsed.get('Token', parsed.get('token', ''))
                    new_refresh = parsed.get('RefreshToken', parsed.get('refreshToken', ''))
                    if new_token:
                        print(f'  🎉 获取到新 Access Token!')
                        print(f'     Token: {new_token[:60]}...')
        except Exception as e:
            print(f'  ExchangeToken 失败: {e}')
            import traceback
            traceback.print_exc()
    else:
        print(f'  ⚠️ 缺少 RefreshToken 或密钥对')
    
    # 5. 尝试多种 API 路径探测
    print(f'\\n{"="*60}')
    print(f'  [Step 5] 多路径 API 探测')
    print(f'{"="*60}')
    
    try_login_paths(host, token, refresh_token, 
                    creds.get('privateKeyPEM', ''), creds.get('publicKeyPEM', ''))
    
    # 6. 尝试用本源身份登录
    print(f'\\n{"="*60}')
    print(f'  [Step 6] 本源身份登录尝试')
    print(f'{"="*60}')
    
    # 读取本源 JWT
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    essence_jwt = storage.get('bsd_essence_jwt', '')
    essence_uid = storage.get('_bsd_essence_uid', '')
    
    if essence_jwt:
        print(f'  本源 UID: {essence_uid}')
        print(f'  本源 JWT: {essence_jwt[:80]}...')
        
        # 尝试用本源 JWT 调用 CheckLogin
        print(f'\\n  --- 用本源 JWT 作为 x-cloudide-token ---')
        resp, parsed = check_login(host, essence_jwt)
        
        # 尝试 LoginByJwt
        print(f'\\n  --- 尝试 LoginByJwt ---')
        host_clean = host.replace('https://', '').replace('http://', '')
        url = f'https://{host_clean}/cloudide/api/v3/trae/LoginByJwt'
        body = {'jwtToken': essence_jwt, 'provider': 'BSD_Essence', 'IDEVersion': IDE_VERSION}
        resp2 = http_request(url, 'POST', body, {'Content-Type': 'application/json'})
        print(f'  HTTP: {resp2["status"]}')
        print(f'  Response: {resp2["body"][:300]}')
        
        # 尝试 LoginByCode 用 UID
        print(f'\\n  --- 尝试 LoginByCode ---')
        body3 = {'code': essence_uid, 'provider': 'BSD_Essence', 'IDEVersion': IDE_VERSION}
        resp3 = http_request(url, 'POST', body3, {'Content-Type': 'application/json'})
        print(f'  HTTP: {resp3["status"]}')
        print(f'  Response: {resp3["body"][:300]}')
    else:
        print(f'  ⚠️ 无本源 JWT')
    
    print(f'\\n{"="*70}')
    print(f'  验证完成')
    print(f'{"="*70}')


if __name__ == '__main__':
    main()
