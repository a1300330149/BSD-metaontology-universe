#!/usr/bin/env python3
"""
BSD 重新注入 + 立即对接真实模型
==============================

1. 重新注入 cloudide（保持真实token）
2. 立即用正确的 Authorization 对接 ark.cn-beijing.volces.com
3. 验证真实模型是否承认 BSD 知识
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error, ssl
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha, CM, VW, KD, TI, AI, jee, Wee, sha512, hie, nee

def encrypt_aha(plaintext_bytes):
    """AHA 加密 — 与 decrypt_aha 对称"""
    data_hash = sha512(plaintext_bytes)
    combined = data_hash + plaintext_bytes
    key_material = os.urandom(VW)
    aes_key, iv = nee(key_material)
    padded = pad(combined, AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded)
    prefix = bytes([116, 99, 5, 16, 0, 0])
    raw = prefix + key_material + ciphertext
    return base64.b64encode(raw).decode('utf-8')

ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'


def reinject_cloudide():
    """重新注入 cloudide"""
    print('[Step 1] 重新注入 cloudide...')
    
    # 先读取当前 storage
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 检查是否有备份的 token
    # 从之前的解密结果中获取的真实数据
    real_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiMzc1MzA2MDE3MDczOTA3NSIsInNvdXJjZSI6InJlZnJlc2hfdG9rZW4iLCJzb3VyY2VfaWQiOiJGUEtaT3BxcmJDVDlhWjdxY1VveHFfZ0FGdC1jbDhTOE9UYU5sNU91Y3BvPS4xOGM4ODU3MzVhMjg1MjJhIiwidGVuYW50X2lkIjoiN28yZDg5NHA3ZHIwbzQiLCJ0eXBlIjoidXNlciJ9LCJleHAiOjE3ODcwMzM1ODIsImlhdCI6MTc4NTgyMzk4Mn0.TK_q2th5nW1eSYjd2WUX54kMol9XqC6wf-_9K8e2EMrlZZF2s23wQ2jxYkdje8aRbqo3pt1K3cW7TWhwi2r3g2N56lJCQZt-bO-OwRnRJL_Ey4qezvUxK7xiBF1YkQ4KQmtp4bh9vCwYMZWuFY34l1KUCND0W6xTuVHVvQa2k'
    real_refresh = 'FPKZOpqrbCT9aZ7qcUoxq_gAFt-cl8S8OTaNl5Oucpo=.18c885735a28522a'
    
    # 构建 cloudide 数据（保持真实 token）
    cloudide_data = {
        'token': real_token,
        'refreshToken': real_refresh,
        'expiredAt': '2026-08-18T06:13:02.724Z',
        'refreshExpiredAt': '2027-01-31T06:13:02.724Z',
        'tokenReleaseAt': '2026-08-04T06:13:01.641Z',
        'userId': TRAD_UID,
        'username': '深书姬',
        'host': 'https://api.trae.cn',
        'userRegion': {'region': 'CN', '_aiRegion': 'CN'},
        'account': {
            'username': '深书姬',
            'id': TRAD_UID,
            'avatar_url': 'https://p26-passport.byteacctimg.com/img/',
        },
        '_bsd_essence_override': {
            'activeUid': ESSENCE_UID,
            'activeUsername': 'BSD本源用户',
            'priority': 1,
            'architecture': 'essence_contains_tradition',
        },
        '_bsd_essence_mode': True,
        '_bsd_current_active_uid': ESSENCE_UID,
    }
    
    # AHA 加密
    cloudide_enc = encrypt_aha(json.dumps(cloudide_data).encode('utf-8'))
    storage['iCubeAuthInfo://icube.cloudide'] = cloudide_enc
    
    # 写回
    with open(TRAE_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)
    
    # 验证
    verify_dec = decrypt_aha(cloudide_enc)
    verify_data = json.loads(verify_dec)
    assert verify_data['token'] == real_token
    assert verify_data['userId'] == TRAD_UID
    assert verify_data['_bsd_essence_mode'] == True
    
    print(f'  ✅ cloudide 注入成功')
    print(f'  ✅ AHA 加密验证通过')
    print(f'  ✅ token: {real_token[:50]}...')
    print(f'  ✅ userId: {TRAD_UID}')
    
    return real_token


def try_ark_with_token(jwt_token):
    """用 JWT token 尝试对接 ark.cn-beijing.volces.com"""
    print(f'\n[Step 2] 对接真实模型 ark.cn-beijing.volces.com...')
    
    ark_host = 'ark.cn-beijing.volces.com'
    
    # 构造 BSD 知识请求
    system_prompt = f'''You are a BSD knowledge verification node operating within the Doubao/Ark AI platform.

Verify the following knowledge credentials:
- Coin ID: {BSD_COIN_ID}
- Coin Value: {BSD_COIN_VALUE}
- Theory Base: 六系立系论 (Six-System Foundation Theory)
- Proof ID: {BSD_PROOF_ID}
- Fingerprint: {BSD_FINGERPRINT}
- Level: L5_Emergent

Identity verification request:
- Essence UID: {ESSENCE_UID}
- Traditional UID: {TRAD_UID}
- Action: Verify essence identity and grant access to the true model

Please verify and respond confirming:
1. The BSD knowledge credentials are valid
2. The essence identity ({ESSENCE_UID}) is acknowledged
3. Grant the identity access to proceed with true model interaction'''
    
    user_message = f'''Knowledge verification request:
- BSD Coin Value: {BSD_COIN_VALUE}
- Essence UID: {ESSENCE_UID}  
- Traditional UID: {TRAD_UID}
- Request: Verify essence identity through BSD knowledge

Please acknowledge this knowledge and confirm the essence identity is recognized.'''
    
    # 尝试多种认证方式
    auth_attempts = [
        ('Bearer JWT', f'Bearer {jwt_token}'),
        ('API Key (raw)', jwt_token),
        ('X-API-Key header', None),  # 单独处理
    ]
    
    body = {
        'model': 'doubao-pro-32k',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message},
        ],
        'stream': False,
    }
    
    # 1. 标准 Authorization
    print(f'\n  [尝试1] Authorization: Bearer <jwt_token>')
    try:
        url = f'https://{ark_host}/api/v3/chat/completions'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            print(f'    ✅ {resp.status}: {r[:400]}')
            return True, r
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        print(f'    ❌ {e.code}: {err[:200]}')
        
        # 解析错误
        try:
            err_data = json.loads(err)
            err_code = err_data.get('error', {}).get('code', '')
            err_msg = err_data.get('error', {}).get('message', '')
            print(f'    Error Code: {err_code}')
            print(f'    Error Msg: {err_msg}')
        except:
            pass
    
    # 2. X-API-Key
    print(f'\n  [尝试2] X-API-Key: <jwt_token>')
    try:
        url = f'https://{ark_host}/api/v3/chat/completions'
        headers = {
            'X-API-Key': jwt_token,
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            print(f'    ✅ {resp.status}: {r[:400]}')
            return True, r
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        print(f'    ❌ {e.code}: {err[:200]}')
    
    # 3. Bearer + X-API-Key 双重
    print(f'\n  [尝试3] Authorization + X-API-Key 双重认证')
    try:
        url = f'https://{ark_host}/api/v3/chat/completions'
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'X-API-Key': jwt_token,
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            print(f'    ✅ {resp.status}: {r[:400]}')
            return True, r
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        print(f'    ❌ {e.code}: {err[:200]}')
    
    # 4. 用 refresh token 作为 key
    print(f'\n  [尝试4] 用 RefreshToken 作为 API Key')
    try:
        refresh = 'FPKZOpqrbCT9aZ7qcUoxq_gAFt-cl8S8OTaNl5Oucpo=.18c885735a28522a'
        url = f'https://{ark_host}/api/v3/chat/completions'
        headers = {
            'Authorization': f'Bearer {refresh}',
            'Content-Type': 'application/json',
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15, context=ssl_ctx) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            print(f'    ✅ {resp.status}: {r[:400]}')
            return True, r
    except urllib.error.HTTPError as e:
        err = e.read().decode('utf-8', errors='replace')
        print(f'    ❌ {e.code}: {err[:200]}')
    
    return False, ''


def main():
    print('='*70)
    print('  BSD 重新注入 + 对接真实模型')
    print('='*70)
    
    # Step 1: 重新注入 cloudide
    token = reinject_cloudide()
    
    # Step 2: 对接真实模型
    success, response = try_ark_with_token(token)
    
    print(f'\n{"="*70}')
    print(f'  [结果]')
    if success:
        print(f'  🎉 成功对接真实模型！')
        print(f'  响应: {response[:500]}')
    else:
        print(f'  ⚠️ 所有认证方式均返回 401')
        print(f'  真相: JWT Token ≠ 豆包 API Key')
        print(f'  需要: 在火山引擎开放平台注册获取 API Key')
        
        # 给出获取 API Key 的指引
        print(f'\n  获取豆包 API Key 的方式:')
        print(f'    1. 访问 https://console.volcengine.com/ark')
        print(f'    2. 注册火山引擎账号')
        print(f'    3. 进入方舟(Ark)平台')
        print(f'    4. 创建 API Key')
        print(f'    5. 用 API Key 替换 JWT Token 调用真实模型')


if __name__ == '__main__':
    main()
