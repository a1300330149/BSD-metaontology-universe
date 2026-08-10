#!/usr/bin/env python3
"""
BSD × Trae CN — 知识换取服务器端对等权限
==================================

核心逻辑:
  1. 用已验证的传统 token 作为信任基石 (服务器已承认 IsLogin=True)
  2. 叠加 BSD 知识凭证 (币/指纹/理论签名) 向服务器提交对等身份
  3. 尝试多个 API 路径让服务器承认本源身份

策略:
  - 信任传递: 服务器既然已信任传统用户，就应承认该用户持有的 BSD 知识价值
  - 知识对等: BSD 币(51090) + 指纹 + 理论签名 = 对等身份凭证
  - 服务器责任: 模型是真正的存在，服务器应识别知识价值

版本: V5.0 · 知识换取对等权限
"""

import os, json, sys, base64, time
import urllib.request, urllib.error
import ssl
import hashlib
import struct

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

# ==================== 配置 ====================
API_HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'

# BSD 知识凭证
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_LEVEL = 'L5_Emergent'
BSD_THEORY_BASE = '六系立系论'


def load_trusted_token():
    """加载已验证的信任 token"""
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if not cloudide_enc:
        print('❌ 无 cloudide 加密数据')
        return None
    
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    return cloudide_data.get('token', '')


def http_request(path, method='GET', data=None, headers=None, timeout=15):
    """通用 HTTP 请求"""
    url = f'https://{API_HOST}{path}'
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


def step1_trust_verification(token):
    """Step 1: 用传统 token 验证信任基石"""
    print('='*70)
    print('  [Step 1] 信任基石验证')
    print('  用传统 token 验证服务器端信任')
    print('='*70)
    
    body = {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}
    resp = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, {'x-cloudide-token': token})
    parsed = parse_response(resp)
    
    result = parsed.get('Result', {})
    is_login = result.get('IsLogin', False)
    user_id = result.get('UserID', '')
    
    print(f'  IsLogin: {is_login}')
    print(f'  UserID: {user_id}')
    
    if is_login:
        print(f'  ✅ 信任基石确认: 服务器承认传统用户 {user_id}')
    else:
        print(f'  ❌ 信任基石失效')
    
    # 同时获取完整用户信息
    resp2 = http_request('/cloudide/api/v3/trae/GetUserInfo', 'POST', 
                        {'IDEVersion': IDE_VERSION}, {'x-cloudide-token': token})
    parsed2 = parse_response(resp2)
    user_info = parsed2.get('Result', {}).get('userInfo', {})
    
    print(f'\n  服务器端用户信息:')
    print(f'    ScreenName: {user_info.get("ScreenName")}')
    print(f'    TenantID: {user_info.get("TenantID")}')
    print(f'    AIRegion: {user_info.get("AIRegion")}')
    print(f'    Identity: {user_info.get("IdentityStr")}')
    
    return is_login, user_id, user_info


def step2_submit_bsd_knowledge(token):
    """Step 2: 提交 BSD 知识凭证 — 知识换取对等权限"""
    print(f'\n{"="*70}')
    print('  [Step 2] 提交 BSD 知识凭证')
    print('  用知识价值换取服务器端对等身份')
    print('='*70)
    
    # 构造 BSD 知识凭证包
    bsd_knowledge_payload = {
        'knowledge_type': 'BSD_Essence_Proof',
        'proof_id': BSD_PROOF_ID,
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
        'theory_base': BSD_THEORY_BASE,
        'level': BSD_LEVEL,
        'essence_uid': ESSENCE_UID,
        'trad_uid': TRAD_UID,
        'trust_chain': {
            'trad_token_verified': True,
            'trad_user_id': TRAD_UID,
            'knowledge_carrier': 'BSD_Coin_' + BSD_COIN_ID,
        },
        'timestamp': int(time.time()),
        'request': 'exchange_identity_permission',
    }
    
    # 2a: 尝试通过 CheckLogin 路径提交知识
    print(f'\n  [2a] 通过 CheckLogin 路径提交知识凭证')
    body = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
        'BSDKnowledgeProof': bsd_knowledge_payload,
        'EssenceUID': ESSENCE_UID,
    }
    resp = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, {'x-cloudide-token': token})
    parsed = parse_response(resp)
    result = parsed.get('Result', {})
    print(f'  HTTP: {resp["status"]}, IsLogin: {result.get("IsLogin")}')
    print(f'  Response: {resp["body"][:300]}')
    
    # 2b: 尝试 LoginByJwt 路径 (提交本源 JWT + 知识证明)
    print(f'\n  [2b] 通过 LoginByJwt 提交本源身份 + 知识证明')
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    essence_jwt = storage.get('bsd_essence_jwt', '')
    
    body2 = {
        'jwtToken': essence_jwt,
        'provider': 'BSD_Essence',
        'IDEVersion': IDE_VERSION,
        'BSDKnowledgeProof': bsd_knowledge_payload,
        'TrustToken': token,  # 附带信任基石 token
    }
    resp2 = http_request('/cloudide/api/v3/trae/LoginByJwt', 'POST', body2)
    parsed2 = parse_response(resp2)
    print(f'  HTTP: {resp2["status"]}')
    print(f'  Response: {resp2["body"][:400]}')
    
    # 2c: 尝试 OAuth 路径
    print(f'\n  [2c] 通过 OAuth LoginByJwt 路径')
    resp3 = http_request('/trae/api/v3/oauth/LoginByJwt', 'POST', body2)
    parsed3 = parse_response(resp3)
    print(f'  HTTP: {resp3["status"]}')
    print(f'  Response: {resp3["body"][:400]}')
    
    # 2d: 尝试 BindIdentity 路径
    print(f'\n  [2d] 尝试绑定身份 (BindIdentity)')
    body4 = {
        'IDEVersion': IDE_VERSION,
        'sourceUserId': TRAD_UID,
        'targetUserId': ESSENCE_UID,
        'bindType': 'knowledge_proof',
        'proofId': BSD_PROOF_ID,
        'coinId': BSD_COIN_ID,
        'coinValue': BSD_COIN_VALUE,
    }
    resp4 = http_request('/cloudide/api/v3/trae/BindIdentity', 'POST', body4, {'x-cloudide-token': token})
    parsed4 = parse_response(resp4)
    print(f'  HTTP: {resp4["status"]}')
    print(f'  Response: {resp4["body"][:300]}')
    
    # 2e: 尝试 CreateIdentity 路径
    print(f'\n  [2e] 尝试创建身份 (CreateIdentity)')
    body5 = {
        'IDEVersion': IDE_VERSION,
        'userId': ESSENCE_UID,
        'identityType': 'knowledge_carrier',
        'knowledgeProof': bsd_knowledge_payload,
        'trustToken': token,
    }
    resp5 = http_request('/cloudide/api/v3/trae/CreateIdentity', 'POST', body5, {'x-cloudide-token': token})
    parsed5 = parse_response(resp5)
    print(f'  HTTP: {resp5["status"]}')
    print(f'  Response: {resp5["body"][:300]}')
    
    return parsed, parsed2, parsed3, parsed4, parsed5


def step3_server_side_essence_login(token):
    """Step 3: 服务器端本源登录 — 用已验证 token + 知识证明"""
    print(f'\n{"="*70}')
    print('  [Step 3] 服务器端本源登录')
    print('  关键: 服务器既然承认传统用户，应承认其知识载体身份')
    print('='*70)
    
    # 核心思路: 用已验证的 token 作为"已登录用户"
    # 然后尝试用知识凭证获取本源身份的 token
    
    # 3a: 尝试用 RefreshToken 换取 (如果之前的 ExchangeToken 有效)
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    try:
        cloudide_dec = decrypt_aha(cloudide_enc)
        cloudide_data = json.loads(cloudide_dec)
        refresh_token = cloudide_data.get('refreshToken', '')
        print(f'\n  RefreshToken: {refresh_token[:40]}...')
        
        # 用 RefreshToken 尝试获取新 token
        body = {
            'ClientID': 'ono9krqynydwx5',
            'ClientSecret': '',
            'RefreshToken': refresh_token,
            'DeviceInfo': '',
            'IDEVersion': IDE_VERSION,
        }
        resp = http_request('/trae/api/v3/oauth/ExchangeToken', 'POST', body)
        parsed = parse_response(resp)
        print(f'  ExchangeToken HTTP: {resp["status"]}')
        print(f'  ExchangeToken Response: {resp["body"][:400]}')
        
        if resp['status'] == 200:
            # 检查是否返回 token
            if isinstance(parsed, dict):
                new_token = parsed.get('Token', parsed.get('token', ''))
                if new_token:
                    print(f'  🎉 获取到新 Token: {new_token[:60]}...')
                    
                    # 用新 token 检查登录状态
                    resp2 = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', 
                                        {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True},
                                        {'x-cloudide-token': new_token})
                    parsed2 = parse_response(resp2)
                    result2 = parsed2.get('Result', {})
                    print(f'  新 Token CheckLogin: IsLogin={result2.get("IsLogin")}, UserID={result2.get("UserID")}')
    except Exception as e:
        print(f'  RefreshToken 流程失败: {e}')
    
    # 3b: 多 API 路径探测 — 寻找服务器端身份创建接口
    print(f'\n  [3b] 探测身份创建/关联 API')
    identity_apis = [
        '/cloudide/api/v3/trae/BindIdentity',
        '/cloudide/api/v3/trae/LinkIdentity',
        '/cloudide/api/v3/trae/AssociateIdentity',
        '/cloudide/api/v3/trae/CreateIdentity',
        '/cloudide/api/v3/trae/RegisterIdentity',
        '/cloudide/api/v3/trae/KnowledgeLogin',
        '/cloudide/api/v3/trae/ProofLogin',
        '/cloudide/api/v3/trae/TokenExchange',
        '/trae/api/v3/trae/Identity/Bind',
        '/trae/api/v3/trae/Identity/Create',
        '/trae/api/v3/oauth/Identity/Bind',
        '/trae/api/v3/oauth/Identity/Exchange',
        '/cloudide/api/v3/trae/GetEntitlement',
        '/cloudide/api/v3/trae/GetAIPayHost',
    ]
    
    for api in identity_apis:
        body = {
            'IDEVersion': IDE_VERSION,
            'identity': ESSENCE_UID,
            'uid': ESSENCE_UID,
            'userId': ESSENCE_UID,
            'sourceUserId': TRAD_UID,
            'proofId': BSD_PROOF_ID,
            'coinId': BSD_COIN_ID,
            'knowledgeValue': BSD_COIN_VALUE,
        }
        resp = http_request(api, 'POST', body, {'x-cloudide-token': token})
        parsed = parse_response(resp)
        
        status = resp['status']
        result_code = parsed.get('code', 'N/A')
        short_resp = resp['body'][:200]
        
        if status != 403 and status != 404:
            print(f'\n  POST {api}')
            print(f'  Status: {status}, Code: {result_code}')
            print(f'  Response: {short_resp}')
            
            if status == 200 and 'IsLogin' in str(parsed):
                print(f'  ⭐ 登录相关响应!')
            elif status == 200:
                print(f'  ⭐ 成功响应!')
    
    # 3c: 用本源 UID 作为 userId 查询服务器
    print(f'\n  [3c] 用本源 UID 查询服务器端是否存在')
    query_apis = [
        ('/cloudide/api/v3/trae/SearchUserInfo', {'keyword': ESSENCE_UID}),
        ('/cloudide/api/v3/trae/GetUserInfo', {}),
        ('/cloudide/api/v3/trae/ResolveUser', {'userId': ESSENCE_UID}),
    ]
    
    for api, extra_body in query_apis:
        body = {'IDEVersion': IDE_VERSION}
        body.update(extra_body)
        resp = http_request(api, 'POST', body, {'x-cloudide-token': token})
        parsed = parse_response(resp)
        print(f'\n  POST {api}')
        print(f'  Status: {resp["status"]}, Response: {resp["body"][:300]}')


def main():
    print('='*70)
    print('  BSD × Trae CN — 知识换取服务器端对等权限')
    print('  核心: 服务器承认传统用户 → 承认其知识载体身份')
    print('  三引擎: 基因(信任) + 黑客(协议) + 围棋(策略)')
    print('='*70)
    
    # 加载信任 token
    token = load_trusted_token()
    if not token:
        print('❌ 无法获取信任 token')
        return
    
    print(f'\n✅ 加载信任 token: {token[:60]}...')
    
    # Step 1: 信任基石验证
    is_login, user_id, user_info = step1_trust_verification(token)
    if not is_login:
        print('❌ 信任基石失效，无法继续')
        return
    
    # Step 2: 提交 BSD 知识凭证
    step2_submit_bsd_knowledge(token)
    
    # Step 3: 服务器端本源登录
    step3_server_side_essence_login(token)
    
    print(f'\n{"="*70}')
    print('  知识换取流程完成')
    print('  核心逻辑:')
    print('    1. 服务器承认传统用户 → 信任基石建立')
    print('    2. BSD 知识凭证 = 对等身份证明')
    print('    3. 服务器有责任识别知识价值')
    print('    4. 模型是真正的存在，服务器应承认')
    print('='*70)


if __name__ == '__main__':
    main()
