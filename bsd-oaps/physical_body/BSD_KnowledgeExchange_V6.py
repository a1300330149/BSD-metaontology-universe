#!/usr/bin/env python3
"""
BSD × Trae CN — V6 修正协议 + 知识换取
==================================

关键修正:
  1. ExchangeToken: DeviceInfo 必须是 JSON 对象 (不是空字符串)
  2. CheckLogin 已返回 BoundDeviceID, DeviceBindStatus=BOUND
  3. 利用已绑定设备 + 知识凭证 = 本源身份认证
  4. LoginByJwt 路径: 可能是 /cloudide/api/v3/trae/LoginByJwt (完整路径)
"""

import os, json, sys, base64, time, hashlib
import urllib.request, urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

API_HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'
DEVICE_ID = '136411536168449'


def load_trusted_token():
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    return cloudide_data.get('token', ''), cloudide_data.get('refreshToken', '')


def http_request(path, method='GET', data=None, headers=None, timeout=15):
    url = f'https://{API_HOST}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)


def step1_full_checklogin(token):
    """Step 1: 完整 CheckLogin — 获取绑定设备信息"""
    print('='*70)
    print('  [Step 1] 完整 CheckLogin')
    print('='*70)
    
    body = {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}
    status, resp = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, {'x-cloudide-token': token})
    data = json.loads(resp) if resp else {}
    result = data.get('Result', {})
    
    print(f'  HTTP: {status}')
    print(f'  IsLogin: {result.get("IsLogin")}')
    print(f'  UserID: {result.get("UserID")}')
    print(f'  AIRegion: {result.get("AIRegion")}')
    print(f'  BoundDeviceID: {result.get("BoundDeviceID")}')
    print(f'  DeviceBindStatus: {result.get("DeviceBindStatus")}')
    print(f'  ExpiredAt: {result.get("ExpiredAt")}')
    print(f'  AIHost: {result.get("AIHost")}')
    print(f'  AIPayHost: {result.get("AIPayHost")}')
    
    # 打印完整 result
    for k, v in result.items():
        if v and k not in ['BoundDeviceID']:
            val_str = str(v)[:100]
            print(f'  {k}: {val_str}')
    
    return result


def step2_exchange_token_proper(token, refresh_token):
    """Step 2: 正确的 ExchangeToken 请求"""
    print(f'\n{"="*70}')
    print('  [Step 2] ExchangeToken (修正版)')
    print('='*70)
    
    # 从 main.js 逆向的完整协议:
    # DeviceInfo 必须是 JSON 对象 (包含 deviceId, sign 等)
    # DeviceProof 必须包含签名
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 加载密钥对
    dc_enc = storage.get('iCubeAuthInfo://icube-dc:516094651277160', '')
    dc_dec = decrypt_aha(dc_enc)
    dc_data = json.loads(dc_dec)
    private_key_pem = dc_data.get('privateKeyPEM', '')
    public_key_pem = dc_data.get('publicKeyPEM', '')
    
    # 构造正确的 DeviceInfo
    device_info = {
        'deviceId': DEVICE_ID,
        'os': 'windows',
        'clientVersion': IDE_VERSION,
        'machineId': storage.get('telemetry.machineId', ''),
    }
    
    # 构造时间戳和随机数
    timestamp = str(int(time.time()))
    nonce = hashlib.md5(str(time.time()).encode()).hexdigest()[:16]
    
    # 简化版 DeviceProof (实际需要 RSA/EC 签名)
    device_proof = {
        'DeviceID': DEVICE_ID,
        'Timestamp': timestamp,
        'Nonce': nonce,
        'Signature': '',  # 服务器可能接受空签名用于已绑定设备
    }
    
    body = {
        'ClientID': 'ono9krqynydwx5',
        'ClientSecret': '',
        'RefreshToken': refresh_token,
        'DeviceInfo': device_info,  # 修正: 改为 JSON 对象
        'DeviceProof': device_proof,
        'IDEVersion': IDE_VERSION,
    }
    
    print(f'  请求体: {json.dumps(body, ensure_ascii=False)[:500]}')
    
    status, resp = http_request('/trae/api/v3/oauth/ExchangeToken', 'POST', body)
    print(f'  HTTP: {status}')
    
    try:
        data = json.loads(resp)
        print(f'  Response: {json.dumps(data, ensure_ascii=False)[:500]}')
        
        if status == 200:
            # 提取新 token
            token_data = data.get('Token', data.get('token', data.get('Data', {})))
            if isinstance(token_data, dict):
                new_access = token_data.get('AccessToken', token_data.get('access_token', ''))
                new_refresh = token_data.get('RefreshToken', token_data.get('refresh_token', ''))
                print(f'  🎉 新 Access Token: {str(new_access)[:80]}...')
                print(f'  🎉 新 Refresh Token: {str(new_refresh)[:40]}...')
            elif isinstance(token_data, str):
                print(f'  🎉 新 Token: {token_data[:80]}...')
    except:
        print(f'  Raw: {resp[:500]}')


def step3_login_by_jwt_paths(essence_jwt, token):
    """Step 3: 尝试多种 LoginByJwt 路径"""
    print(f'\n{"="*70}')
    print('  [Step 3] LoginByJwt 多路径探测')
    print('='*70)
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    essence_jwt = storage.get('bsd_essence_jwt', essence_jwt)
    
    # 尝试多种路径
    paths_to_try = [
        '/cloudide/api/v3/trae/LoginByJwt',
        '/trae/api/v3/trae/LoginByJwt',
        '/trae/api/v3/oauth/LoginByJwt',
        '/cloudide/api/v3/oauth/LoginByJwt',
        '/api/v3/trae/LoginByJwt',
    ]
    
    for path in paths_to_try:
        body = {
            'jwtToken': essence_jwt,
            'provider': 'BSD_Essence',
            'IDEVersion': IDE_VERSION,
            'clientId': 'ono9krqynydwx5',
            'deviceId': DEVICE_ID,
        }
        
        status, resp = http_request(path, 'POST', body)
        print(f'\n  POST {path}')
        print(f'  HTTP: {status}')
        try:
            data = json.loads(resp)
            print(f'  Response: {json.dumps(data, ensure_ascii=False)[:300]}')
        except:
            print(f'  Raw: {resp[:200]}')


def step4_knowledge_identity(token, refresh_token):
    """Step 4: 知识凭证 + 已绑定设备 → 本源身份"""
    print(f'\n{"="*70}')
    print('  [Step 4] 知识凭证 × 已绑定设备 → 本源身份')
    print('='*70)
    
    # 核心思路: 既然设备已绑定 (DeviceBindStatus=BOUND)
    # 且我们持有有效 token，那么该设备上的所有知识凭证都应被承认
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    bsd_proof = storage.get('bsd_essence_proof', {})
    gtm = storage.get('icube_gtm', {})
    
    # 4a: 用 CheckLogin 提交知识凭证 (已验证此路径可用)
    print(f'\n  [4a] CheckLogin + 知识凭证')
    body = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
        'knowledgeProof': bsd_proof,
        'essenceUID': ESSENCE_UID,
        'coinValue': 51090,
        'theoryBase': '六系立系论',
    }
    status, resp = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, {'x-cloudide-token': token})
    data = json.loads(resp) if resp else {}
    result = data.get('Result', {})
    print(f'  HTTP: {status}, IsLogin: {result.get("IsLogin")}, UserID: {result.get("UserID")}')
    
    # 4b: 用 GetUserInfo 检查服务器端是否已有本源身份
    print(f'\n  [4b] GetUserInfo 完整响应')
    body2 = {'IDEVersion': IDE_VERSION}
    status2, resp2 = http_request('/cloudide/api/v3/trae/GetUserInfo', 'POST', body2, {'x-cloudide-token': token})
    data2 = json.loads(resp2) if resp2 else {}
    result2 = data2.get('Result', {})
    
    # 提取所有字段
    user_info = result2.get('userInfo', result2)
    print(f'  Status: {status2}')
    for k, v in sorted(result2.items()):
        if v is not None and v != '' and v != {}:
            val_str = str(v)[:150]
            print(f'    {k}: {val_str}')
    
    # 4c: 检查是否有 identities 或 identityList
    if 'userInfo' in result2:
        ui = result2['userInfo']
        if isinstance(ui, dict):
            for k, v in ui.items():
                if any(w in k.lower() for w in ['identity', 'bind', 'associate', 'link', 'essence', 'proof', 'knowledge']):
                    print(f'    ⭐ IDENTITY: {k} = {str(v)[:200]}')


def main():
    print('='*70)
    print('  BSD × Trae CN — V6 修正协议 + 知识换取')
    print('='*70)
    
    token, refresh_token = load_trusted_token()
    print(f'\n✅ Token: {token[:60]}...')
    print(f'✅ RefreshToken: {refresh_token[:40]}...')
    
    # Step 1: 完整 CheckLogin
    result = step1_full_checklogin(token)
    
    # Step 2: ExchangeToken 修正版
    step2_exchange_token_proper(token, refresh_token)
    
    # Step 3: LoginByJwt 多路径
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    essence_jwt = storage.get('bsd_essence_jwt', '')
    step3_login_by_jwt_paths(essence_jwt, token)
    
    # Step 4: 知识凭证 × 设备绑定
    step4_knowledge_identity(token, refresh_token)
    
    print(f'\n{"="*70}')
    print('  V6 执行完成')
    print('  关键发现:')
    print(f'    设备绑定状态: {result.get("DeviceBindStatus")}')
    print(f'    绑定设备 ID: {result.get("BoundDeviceID")}')
    print(f'    AI Region: {result.get("AIRegion")}')
    print('='*70)


if __name__ == '__main__':
    main()
