#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整实现 ExchangeToken 认证流程
基于逆向分析 Trae CN OAuth 协议
"""

import json, ssl, urllib.request, urllib.error, http.cookiejar, time, hashlib
import sys, os, base64

# ECDSA 签名
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

# 加载凭据
with open(r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json', 'r') as f:
    storage = json.load(f)

cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
dec = decrypt_aha(cloudide_enc)
data = json.loads(dec.decode('utf-8'))

jwt_token = data.get('token', '')
refresh_token = data.get('refreshToken', '')
userId = data.get('userId', '')
private_key_pem = storage.get('iCubeAuthInfo://icube-dc:516094651277160', '')  # 需要解密

# 实际上私钥在icube-dc中
dc_enc = storage.get('iCubeAuthInfo://icube-dc:516094651277160', '')
dc_dec = decrypt_aha(dc_enc)
dc_data = json.loads(dc_dec.decode('utf-8'))
private_key_pem = dc_data.get('privateKeyPEM', '')
public_key_pem = dc_data.get('publicKeyPEM', '')

AUTH_BASE = 'https://api.trae.cn'
API_BASE = 'https://trae-api-cn.mchost.guru'
CLIENT_ID = 'ono9krqynydwx5'  # TRAE CN默认ClientID
IDE_VERSION = '2.3.62837'

# 加载私钥
private_key = serialization.load_pem_private_key(
    private_key_pem.encode('utf-8'),
    password=None,
    backend=default_backend()
)

def generate_signature(method, path, client_id, refresh_token, private_key):
    """
    生成DeviceProof签名
    对应 Trae CN 的 O9e 函数 (ECDSA签名)
    """
    timestamp = int(time.time())
    nonce = os.urandom(16).hex()
    
    # 拼接签名字符串 (与JS端一致: 用换行符连接)
    sign_string = '\n'.join([method, path, client_id, refresh_token, str(timestamp), nonce])
    
    # ECDSA SHA256 签名
    signature = private_key.sign(
        sign_string.encode('utf-8'),
        ec.ECDSA(hashes.SHA256())
    )
    signature_b64 = base64.b64encode(signature).decode('utf-8')
    
    return {
        'timestamp': timestamp,
        'nonce': nonce,
        'signature': signature_b64
    }

# 生成签名
device_proof = generate_signature(
    'POST',
    '/trae/api/v3/oauth/ExchangeToken',
    CLIENT_ID,
    refresh_token,
    private_key
)

print(f'=== ExchangeToken 认证 ===')
print(f'ClientID: {CLIENT_ID}')
print(f'RefreshToken: {refresh_token[:30]}...')
print(f'签名时间戳: {device_proof["timestamp"]}')
print(f'Nonce: {device_proof["nonce"]}')
print(f'签名: {device_proof["signature"][:50]}...')

# 构建设备信息
device_info = {
    'DeviceID': userId,  # 使用userId作为DeviceID
    'MachineID': hashlib.sha256(userId.encode()).hexdigest()[:16],
    'PlatformCode': 'windows',
    'DeviceType': 'PC',
    'DeviceName': 'BSD-Essence',
    'DeviceModel': 'PC',
    'OSVersion': 'Windows NT 10.0.19045.0',
    'Architecture': 'x64',
    'Language': 'zh-CN',
    'Timezone': 'Asia/Shanghai',
    'DevicePublicKey': public_key_pem,
}

# 构建请求体
request_body = {
    'ClientID': CLIENT_ID,
    'ClientSecret': '',
    'RefreshToken': refresh_token,
    'DeviceInfo': device_info,
    'DeviceProof': device_proof,
    'IDEVersion': IDE_VERSION,
}

print(f'\n请求体:')
print(json.dumps(request_body, ensure_ascii=False, indent=2)[:1000])

# 发送请求
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(
    urllib.request.HTTPCookieProcessor(cookie_jar),
    urllib.request.HTTPSHandler(context=ssl_ctx)
)

print(f'\n--- 发送请求到 {AUTH_BASE}/trae/api/v3/oauth/ExchangeToken ---')
try:
    body_bytes = json.dumps(request_body).encode('utf-8')
    
    req = urllib.request.Request(
        f'{AUTH_BASE}/trae/api/v3/oauth/ExchangeToken',
        data=body_bytes,
        headers={
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'Accept': 'application/json',
        },
        method='POST'
    )
    
    resp = opener.open(req, timeout=10)
    resp_text = resp.read().decode('utf-8')
    print(f'HTTP {resp.status}')
    print(f'响应: {resp_text[:1000]}')
    
    # 解析响应
    try:
        result = json.loads(resp_text)
        print(f'\n解析结果:')
        print(json.dumps(result, ensure_ascii=False, indent=2)[:800])
        
        # 查找Token
        res_data = result.get('Result', result.get('data', {}))
        if isinstance(res_data, dict):
            new_token = res_data.get('Token', res_data.get('AccessToken', ''))
            new_refresh = res_data.get('RefreshToken', res_data.get('refresh_token', ''))
            
            if new_token:
                print(f'\n🎉 成功获取新Token!')
                print(f'Token: {new_token[:80]}...')
                if new_refresh:
                    print(f'新RefreshToken: {new_refresh}')
                    
                # 用新Token请求API
                print(f'\n--- 用新Token请求API ---')
                try:
                    api_body = json.dumps({
                        'model': 'doubao-pro-32k',
                        'query': '你好，请回复OK',
                        'stream': False,
                    }).encode()
                    
                    api_req = urllib.request.Request(
                        f'{API_BASE}/api/ide/v2/llm_raw_chat',
                        data=api_body,
                        headers={
                            'Content-Type': 'application/json',
                            'User-Agent': f'TraeCN/{IDE_VERSION}',
                            'Accept': 'text/event-stream',
                            'Authorization': f'Bearer {new_token}',
                        },
                        method='POST'
                    )
                    
                    api_resp = opener.open(api_req, timeout=15)
                    api_text = api_resp.read().decode('utf-8')
                    print(f'API响应: HTTP {api_resp.status}')
                    print(f'内容: {api_text[:500]}')
                    
                except urllib.error.HTTPError as e:
                    print(f'API错误 HTTP {e.code}: {e.read().decode()[:500]}')
                except Exception as e:
                    print(f'API错误: {e}')
                    
    except json.JSONDecodeError:
        print('JSON解析失败')
        
except urllib.error.HTTPError as e:
    error_body = e.read().decode()[:500]
    print(f'HTTP {e.code}: {error_body}')
    
    # 尝试解析错误详情
    try:
        err = json.loads(error_body)
        metadata = err.get('ResponseMetadata', {})
        error = metadata.get('Error', {})
        print(f'错误码: {error.get("Code", "N/A")}')
        print(f'错误信息: {error.get("Message", "N/A")}')
    except:
        pass
        
except Exception as e:
    print(f'错误: {e}')
    import traceback
    traceback.print_exc()
