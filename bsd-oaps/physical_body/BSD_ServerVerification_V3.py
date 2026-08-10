#!/usr/bin/env python3
"""
BSD × Trae CN — 服务器端本源验证 V3
==================================

基于 main.js 逆向的真实协议:
  URL: {apiHost}/cloudide/api/v3/trae/CheckLogin
  Method: POST
  Headers: { "x-cloudide-token": <token>, "Content-Type": "application/json" }
  Body: { IDEVersion: "2.3.62837", ReqSource: "IDE"|"Lite", GetAIPayHost: true }

关键突破:
  1. API 主机地址从 bootConfig.account.trae 配置获取
  2. 认证通过 x-cloudide-token Header 传递
  3. 请求体不需要 UID — 服务器根据 token 解析身份
  4. 本源 JWT 需要通过 LoginByJwt 或 ExchangeToken 换取有效 token

版本: V3.0 · 基于逆向协议
"""

import os, json, base64, hashlib, time, struct
from datetime import datetime
import urllib.request
import urllib.error
import ssl

# ==================== 配置 ====================
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
TINY = os.path.join(TRAE_DATA, 'aha', 'TinyStorage')
PRODUCT = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app\product.json'

# 从 product.json 获取 API 主机
def get_api_hosts():
    with open(PRODUCT, 'r', encoding='utf-8') as f:
        product = json.load(f)
    
    boot = product.get('bootConfig', {})
    account = boot.get('account', {})
    trae_config = account.get('trae', {})
    
    hosts = {
        'normal': trae_config.get('normal', ''),
        'CN': trae_config.get('CN', ''),
        'SG': trae_config.get('SG', ''),
        'USTTP': trae_config.get('USTTP', ''),
    }
    
    # 清理空值
    hosts = {k: v for k, v in hosts.items() if v}
    return hosts

# SSL 上下文
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}

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
    """解析响应"""
    if resp['body']:
        try:
            return json.loads(resp['body'])
        except:
            return {'raw': resp['body'][:500]}
    return {}


def normalize_host(host):
    """移除主机前缀的 https:// 或 http://"""
    if host.startswith('https://'):
        return host[8:]
    if host.startswith('http://'):
        return host[7:]
    return host


def check_login_directive(api_host, token, req_source='IDE'):
    """
    按 main.js 逆向协议调用 CheckLogin
    
    协议 (来自 main.js):
    URL: {apiHost}/cloudide/api/v3/trae/CheckLogin
    Method: POST
    Headers: { "x-cloudide-token": token, "Content-Type": "application/json" }
    Body: { IDEVersion, ReqSource, GetAIPayHost: true }
    """
    host = normalize_host(api_host)
    url = f'https://{host}/cloudide/api/v3/trae/CheckLogin'
    
    headers = {
        'x-cloudide-token': token,
        'Content-Type': 'application/json',
    }
    
    data = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': req_source,
        'GetAIPayHost': True,
    }
    
    print(f'  URL: {url}')
    print(f'  Headers: x-cloudide-token={token[:50]}...')
    print(f'  Body: {json.dumps(data)}')
    
    resp = http_request(url, 'POST', data, headers)
    return resp, parse_response(resp)


def login_by_jwt(api_host, jwt_token):
    """
    LoginByJwt 协议
    URL: {apiHost}/cloudide/api/v3/trae/LoginByJwt
    """
    host = normalize_host(api_host)
    url = f'https://{host}/cloudide/api/v3/trae/LoginByJwt'
    
    headers = {'Content-Type': 'application/json'}
    data = {
        'jwtToken': jwt_token,
        'provider': 'icube.cloudide',
        'deviceId': AUTHOR['device_id'],
        'IDEVersion': IDE_VERSION,
    }
    
    print(f'  URL: {url}')
    print(f'  JWT: {jwt_token[:80]}...')
    
    resp = http_request(url, 'POST', data, headers)
    return resp, parse_response(resp)


def exchange_token(api_host, refresh_token, client_id='ono9krqynydwx5'):
    """
    ExchangeToken 协议
    URL: {apiHost}/trae/api/v3/oauth/ExchangeToken
    """
    host = normalize_host(api_host)
    url = f'https://{host}/trae/api/v3/oauth/ExchangeToken'
    
    # 简化版请求 (实际需要签名)
    data = {
        'ClientID': client_id,
        'ClientSecret': '',
        'RefreshToken': refresh_token,
        'DeviceInfo': '',
        'IDEVersion': IDE_VERSION,
    }
    
    resp = http_request(url, 'POST', data, {'Content-Type': 'application/json'})
    return resp, parse_response(resp)


def main():
    print('='*70)
    print('  BSD × Trae CN — 服务器端本源验证 V3')
    print('  基于 main.js 逆向的真实 API 协议')
    print('='*70)
    
    # 1. 获取 API 主机
    hosts = get_api_hosts()
    print(f'\n📡 API 主机地址:')
    for k, v in hosts.items():
        print(f'  {k}: {v}')
    
    api_host = hosts.get('normal', '')
    if not api_host:
        print('❌ 无可用 API 主机')
        return
    print(f'\n🎯 使用主机: {api_host}')
    
    # 2. 加载 storage.json 获取凭证
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 传统 token (从 usertag 解密结果提取)
    trad_token = storage.get('iCubeAuthInfo://usertag', '')
    # 本源 JWT
    essence_jwt = storage.get('bsd_essence_jwt', '')
    # 本源 token
    essence_token = storage.get('iCubeAuthInfo://jwt-token', essence_jwt)
    
    print(f'\n🔑 凭证:')
    print(f'  传统 usertag: {trad_token[:60]}...' if trad_token else '  传统: ❌')
    print(f'  本源 JWT: {essence_jwt[:80]}...' if essence_jwt else '  本源: ❌')
    
    # 3. 用传统 token 调用 CheckLogin (验证链路)
    print(f'\n{"="*60}')
    print('  [测试1] 传统凭证 CheckLogin')
    print('='*60)
    
    if trad_token:
        resp, parsed = check_login_directive(api_host, trad_token)
        print(f'\n  响应: {json.dumps(parsed, ensure_ascii=False)[:500]}')
        
        code = parsed.get('code', parsed.get('ResponseMetadata', {}).get('Error', {}).get('Code', 'N/A'))
        result = parsed.get('Result', {})
        is_login = result.get('IsLogin', 'N/A')
        
        print(f'  状态码: {resp["status"]}')
        print(f'  业务码: {code}')
        print(f'  IsLogin: {is_login}')
    else:
        print('  ⚠️ 无传统 token')
    
    # 4. 用本源 JWT 调用 LoginByJwt
    print(f'\n{"="*60}')
    print('  [测试2] 本源 JWT LoginByJwt')
    print('='*60)
    
    if essence_jwt:
        resp, parsed = login_by_jwt(api_host, essence_jwt)
        print(f'\n  响应: {json.dumps(parsed, ensure_ascii=False)[:500]}')
        
        code = parsed.get('code', 'N/A')
        print(f'  HTTP 状态: {resp["status"]}')
        print(f'  业务码: {code}')
        
        # 检查是否返回了新的 token
        token_data = parsed.get('data', {})
        if isinstance(token_data, dict):
            new_token = token_data.get('Token', token_data.get('token', ''))
            new_uid = token_data.get('uid', token_data.get('userId', ''))
            print(f'  返回 Token: {new_token[:60]}...' if new_token else '  无返回 Token')
            print(f'  返回 UID: {new_uid}')
    else:
        print('  ⚠️ 无本源 JWT')
    
    # 5. 用本源 token 调用 CheckLogin
    print(f'\n{"="*60}')
    print('  [测试3] 本源 Token CheckLogin')
    print('='*60)
    
    if essence_token:
        resp, parsed = check_login_directive(api_host, essence_token)
        print(f'\n  响应: {json.dumps(parsed, ensure_ascii=False)[:500]}')
        
        code = parsed.get('code', parsed.get('ResponseMetadata', {}).get('Error', {}).get('Code', 'N/A'))
        result = parsed.get('Result', {})
        is_login = result.get('IsLogin', 'N/A')
        uid_data = result.get('UserId', result.get('uid', ''))
        
        print(f'  HTTP 状态: {resp["status"]}')
        print(f'  业务码: {code}')
        print(f'  IsLogin: {is_login}')
        print(f'  服务器返回 UID: {uid_data}')
        
        if is_login == True or (is_login != 'N/A' and is_login is not False):
            print('\n  🎉 本源身份已被服务器承认!')
        elif uid_data and AUTHOR['essence_uid'] in str(uid_data):
            print('\n  🎉 服务器返回了本源 UID!')
        else:
            print('\n  ⚠️ 服务器未承认本源身份')
    else:
        print('  ⚠️ 无本源 token')
    
    # 6. 尝试 ExchangeToken 路径
    print(f'\n{"="*60}')
    print('  [测试4] ExchangeToken 路径')
    print('='*60)
    
    # 尝试用传统 refresh token 换取
    cloudide_auth = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_auth:
        print(f'  使用 icube.cloudide 凭证')
        print(f'  长度: {len(cloudide_auth)}')
        print(f'  前60字符: {cloudide_auth[:60]}...')
        
        # 直接用 cloudide_auth 作为 token 调用 CheckLogin
        resp, parsed = check_login_directive(api_host, cloudide_auth)
        print(f'\n  响应: {json.dumps(parsed, ensure_ascii=False)[:500]}')
    else:
        print('  ⚠️ 无 cloudide 凭证')
    
    # 7. 尝试多个 API 主机
    print(f'\n{"="*60}')
    print('  [测试5] 多主机轮询')
    print('='*60)
    
    for region, host in hosts.items():
        print(f'\n  --- {region}: {host} ---')
        try:
            resp, parsed = check_login_directive(host, trad_token or essence_token)
            code = parsed.get('code', 'N/A')
            is_login = parsed.get('Result', {}).get('IsLogin', 'N/A')
            print(f'  HTTP: {resp["status"]}, 业务码: {code}, IsLogin: {is_login}')
            if is_login == True:
                print(f'  ✅ {region} 验证通过!')
                break
        except Exception as e:
            print(f'  ❌ {region} 失败: {e}')
    
    print(f'\n{"="*70}')
    print('  验证完成')
    print('='*70)


if __name__ == '__main__':
    main()
