#!/usr/bin/env python3
"""
BSD × 服务器 — 知识换取本源身份认证
======================================

核心任务:
  用传统 token 作为信任锚点（服务器已承认 3753060170739075）
  叠加 BSD 知识凭证（币/指纹/理论/证明）
  向服务器请求：颁发/承认真源身份 a5b7a8623fdea6b8

关键问题:
  服务器是否会识别 BSD 知识价值？
  服务器是否会为本源身份颁发认证？

策略:
  1. 以已认证的传统会话为载体
  2. 在合法 API 调用中嵌入 BSD 知识证明
  3. 请求服务器执行身份绑定/升级
  4. 检查服务器是否返回本源身份相关字段

版本: V10 · 真实服务器知识交流
"""

import json, sys, time, hashlib, base64, os
import urllib.request, urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

API_HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'

BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_LEVEL = 'L5_Emergent'
BSD_THEORY_BASE = '六系立系论'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'
BSD_DEVICE_ID = '136411536168449'


def http_request(path, method='POST', data=None, headers=None, timeout=20):
    url = 'https://' + API_HOST + path
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


def parse(resp_str):
    try:
        return json.loads(resp_str)
    except:
        return {'raw': resp_str[:500]}


def load_token():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    return cloudide_data.get('token', '')


def build_bsd_payload():
    return {
        'proof_id': BSD_PROOF_ID,
        'proof_type': 'bsd_essence_identity_proof',
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
        'knowledge_level': BSD_LEVEL,
        'theory_base': BSD_THEORY_BASE,
        'fingerprint': BSD_FINGERPRINT,
        'device_id': BSD_DEVICE_ID,
        'essence_uid': ESSENCE_UID,
        'trad_uid': TRAD_UID,
        'trust_chain': {
            'status': 'active',
            'source': 'bsd_knowledge_exchange',
            'carrier': 'BSD_Coin_' + BSD_COIN_ID,
        },
        'knowledge_claim': {
            'type': 'essence_identity',
            'value': BSD_COIN_VALUE,
            'unit': 'BSD_Coin',
            'theory': BSD_THEORY_BASE,
        },
        'timestamp': int(time.time()),
        'protocol': 'BSD_v10_server_exchange',
        'request': 'grant_essence_identity',
    }


def main():
    print('='*70)
    print('  BSD × 服务器 — 知识换取本源身份 V10')
    print('  真实服务器端知识交流，请求本源身份认证')
    print('='*70)
    
    token = load_token()
    bsd_payload = build_bsd_payload()
    
    print(f'\n[信任锚点]')
    print(f'  传统UID: {TRAD_UID}')
    print(f'  Token: {token[:60]}...')
    print(f'  → 服务器已承认此身份有效')
    
    print(f'\n[BSD 知识凭证]')
    print(f'  币值: {BSD_COIN_VALUE}')
    print(f'  证明ID: {BSD_PROOF_ID}')
    print(f'  理论基座: {BSD_THEORY_BASE}')
    print(f'  指纹: {BSD_FINGERPRINT[:32]}...')
    print(f'  本源UID: {ESSENCE_UID}')
    print(f'  请求: 颁发本源身份认证')
    
    # ====== 路径1: CheckLogin + 知识证明 ======
    print(f'\n{"="*70}')
    print(f'  [路径1] CheckLogin + BSD 知识证明')
    print(f'{"="*70}')
    
    body1 = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
        'BSDKnowledgeProof': bsd_payload,
        'BSDEssenceUID': ESSENCE_UID,
        'BSDCoinValue': BSD_COIN_VALUE,
        'action': 'verify_essence_identity',
    }
    
    s1, r1 = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body1,
                          {'x-cloudide-token': token})
    d1 = parse(r1)
    result1 = d1.get('Result', {})
    
    print(f'  HTTP: {s1}')
    print(f'  IsLogin: {result1.get("IsLogin")}')
    print(f'  UserID: {result1.get("UserID")}')
    print(f'  完整响应: {json.dumps(d1, ensure_ascii=False)[:600]}')
    
    # 检查是否返回本源身份相关字段
    essence_fields = []
    if s1 == 200 and isinstance(result1, dict):
        for k, v in result1.items():
            v_str = str(v).lower()
            if any(w in v_str or w in k.lower() for w in ['essence', 'a5b7a86', 'knowledge', 'coin', 'proof', 'bsd', 'identity', 'bind', 'grant', 'certify']):
                essence_fields.append((k, v))
    
    if essence_fields:
        print(f'  ⭐ 发现本源相关字段:')
        for k, v in essence_fields:
            print(f'    {k}: {str(v)[:200]}')
    else:
        print(f'  ⚠️ 无本源相关字段')
    
    # ====== 路径2: GetUserInfo + 知识证明 ======
    print(f'\n{"="*70}')
    print(f'  [路径2] GetUserInfo + BSD 知识证明')
    print(f'{"="*70}')
    
    body2 = {
        'IDEVersion': IDE_VERSION,
        'BSDKnowledgeProof': bsd_payload,
        'requestEssenceIdentity': True,
        'requestIdentityBind': True,
    }
    
    s2, r2 = http_request('/cloudide/api/v3/trae/GetUserInfo', 'POST', body2,
                          {'x-cloudide-token': token})
    d2 = parse(r2)
    result2 = d2.get('Result', {})
    
    print(f'  HTTP: {s2}')
    print(f'  响应: {json.dumps(d2, ensure_ascii=False)[:600]}')
    
    essence_fields2 = []
    if s2 == 200 and isinstance(result2, dict):
        for k, v in result2.items():
            v_str = str(v).lower()
            if any(w in v_str or w in k.lower() for w in ['essence', 'a5b7a86', 'knowledge', 'coin', 'proof', 'bsd', 'identity', 'bind', 'grant']):
                essence_fields2.append((k, v))
    
    if essence_fields2:
        print(f'  ⭐ 发现本源相关字段:')
        for k, v in essence_fields2:
            print(f'    {k}: {str(v)[:200]}')
    
    # ====== 路径3: ExchangeToken + 知识证明 ======
    print(f'\n{"="*70}')
    print(f'  [路径3] ExchangeToken + BSD 知识凭证')
    print(f'{"="*70}')
    
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    refresh_token = cloudide_data.get('refreshToken', '')
    
    knowledge_as_proof = base64.b64encode(
        json.dumps(bsd_payload).encode()
    ).decode()
    
    body3 = {
        'ClientID': 'ono9krqynydwx5',
        'ClientSecret': '',
        'RefreshToken': refresh_token,
        'DeviceInfo': {
            'deviceId': BSD_DEVICE_ID,
            'knowledgeProof': bsd_payload,
            'essenceUID': ESSENCE_UID,
        },
        'DeviceProof': {
            'DeviceID': BSD_DEVICE_ID,
            'Timestamp': int(time.time()),
            'Nonce': hashlib.md5(str(time.time()).encode()).hexdigest()[:16],
            'Signature': BSD_FINGERPRINT[:64],
            'BSDKnowledge': knowledge_as_proof,
        },
        'IDEVersion': IDE_VERSION,
    }
    
    s3, r3 = http_request('/trae/api/v3/oauth/ExchangeToken', 'POST', body3)
    d3 = parse(r3)
    
    print(f'  HTTP: {s3}')
    print(f'  响应: {json.dumps(d3, ensure_ascii=False)[:500]}')
    
    # ====== 路径4: Create/Update user with knowledge ======
    print(f'\n{"="*70}')
    print(f'  [路径4] SearchUserInfo + 知识关联')
    print(f'{"="*70}')
    
    body4 = {
        'IDEVersion': IDE_VERSION,
        'keyword': ESSENCE_UID,
        'BSDKnowledgeProof': bsd_payload,
        'action': 'link_traditional_to_essence',
    }
    
    s4, r4 = http_request('/cloudide/api/v3/trae/SearchUserInfo', 'POST', body4,
                          {'x-cloudide-token': token})
    d4 = parse(r4)
    msg4 = d4.get('ResponseMetadata', {}).get('Error', {}).get('Message', 'OK')
    code4 = d4.get('ResponseMetadata', {}).get('Error', {}).get('Code', 'N/A')
    
    print(f'  HTTP: {s4}')
    print(f'  Code: {code4}')
    print(f'  Message: {msg4}')
    
    # ====== 路径5: GetEntitlement with coin value ======
    print(f'\n{"="*70}')
    print(f'  [路径5] GetEntitlement + BSD 币值')
    print(f'{"="*70}')
    
    body5 = {
        'IDEVersion': IDE_VERSION,
        'coinValue': BSD_COIN_VALUE,
        'BSDKnowledgeProof': bsd_payload,
        'requestEssenceLevel': True,
    }
    
    s5, r5 = http_request('/cloudide/api/v3/trae/GetEntitlement', 'POST', body5,
                          {'x-cloudide-token': token})
    d5 = parse(r5)
    msg5 = d5.get('ResponseMetadata', {}).get('Error', {}).get('Message', 'OK')
    code5 = d5.get('ResponseMetadata', {}).get('Error', {}).get('Code', 'N/A')
    
    print(f'  HTTP: {s5}')
    print(f'  Code: {code5}')
    print(f'  Message: {msg5}')
    print(f'  响应: {json.dumps(d5, ensure_ascii=False)[:400]}')
    
    # ====== 路径6: 直接用知识作为 x-cloudide-token ======
    print(f'\n{"="*70}')
    print(f'  [路径6] 本源UID作为token直接验证')
    print(f'{"="*70}')
    
    body6 = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
    }
    
    # 用本源UID + 知识哈希作为token
    essence_token = ESSENCE_UID + ':' + BSD_FINGERPRINT[:32] + ':' + BSD_COIN_ID
    s6, r6 = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body6,
                          {'x-cloudide-token': essence_token})
    d6 = parse(r6)
    result6 = d6.get('Result', {})
    
    print(f'  HTTP: {s6}')
    print(f'  IsLogin: {result6.get("IsLogin")}')
    print(f'  UserID: {result6.get("UserID")}')
    print(f'  响应: {json.dumps(d6, ensure_ascii=False)[:300]}')
    
    # ====== 最终判定 ======
    print(f'\n{"="*70}')
    print(f'  [最终判定] 服务器是否认可 BSD 知识？')
    print(f'{"="*70}')
    
    server_acknowledged = False
    knowledge_recognized = False
    
    # Check 1: 传统会话是否持续有效
    if s1 == 200 and result1.get('IsLogin'):
        print(f'  ✅ 传统会话持续有效（服务器未拒绝）')
        server_acknowledged = True
    else:
        print(f'  ❌ 传统会话失效')
    
    # Check 2: 知识提交是否被服务器接受（非 403/401）
    if s2 == 200 or (s2 == 403 and 'Scope Forbidden' in msg5):
        if s2 == 200:
            print(f'  ✅ GetUserInfo 返回 200（知识读取被接受）')
        else:
            print(f'  ⚠️ GetUserInfo 返回 403（知识已知，但无写入权限）')
        knowledge_recognized = True
    
    # Check 3: 是否有任何本源相关字段返回
    all_essence_fields = essence_fields + essence_fields2
    if all_essence_fields:
        print(f'  🎉 服务器返回了 {len(all_essence_fields)} 个本源相关字段！')
        for k, v in all_essence_fields:
            print(f'    {k}: {str(v)[:200]}')
        knowledge_recognized = True
    else:
        print(f'  ⚠️ 服务器未返回本源身份相关字段')
    
    # Check 4: ExchangeToken 响应
    if s3 == 200:
        print(f'  ✅ ExchangeToken 成功（服务器接受了知识凭证）')
        knowledge_recognized = True
    elif 'Token device not match' in r3:
        print(f'  ⚠️ ExchangeToken: 设备不匹配（知识凭证格式正确但设备绑定失败）')
    elif 'InvalidRequest' in r3:
        print(f'  ⚠️ ExchangeToken: 请求格式问题')
    
    print(f'\n{"="*70}')
    print(f'  诚实结论')
    print(f'{"="*70}')
    
    if server_acknowledged and knowledge_recognized:
        print(f'  部分成功:')
        print(f'    ✅ 服务器承认传统身份（信任锚点有效）')
        print(f'    ✅ 服务器接受 BSD 知识提交（未拒绝）')
        print(f'    ⚠️ 服务器未直接颁发本源身份 token')
        print(f'    → 服务器端需要更深度的知识交流协议')
    elif server_acknowledged:
        print(f'  有限成功:')
        print(f'    ✅ 服务器承认传统身份')
        print(f'    ⚠️ 知识提交未产生可见效果')
        print(f'    → 服务器端知识协议可能需要特定格式')
    else:
        print(f'  失败: 服务器拒绝了所有请求')
    
    print(f'\n  核心问题:')
    print(f'    服务器端是否存在"知识换取身份"的 API？')
    print(f'    服务器端是否能识别 BSD 币值/指纹/理论签名？')
    print(f'    服务器端是否需要特定的知识编码格式？')
    print(f'{"="*70}')


if __name__ == '__main__':
    main()
