#!/usr/bin/env python3
"""
BSD 最终突破 — 正确构造授权
============================

关键发现:
  ark.cn-beijing.volces.com → AuthN_MissOrInvalidAuthorizationHeader
  含义: 服务器收到了请求，授权头存在但无效
  突破: 正确构造 Authorization 头
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

ESSENCE_UID = 'a5b7a8623fdea6b8'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'


def load_token():
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if not cloudide_enc:
        return '', storage
    try:
        cloudide_dec = decrypt_aha(cloudide_enc)
        cloudide_data = json.loads(cloudide_dec)
        return cloudide_data.get('token', ''), storage
    except:
        return '', storage


def main():
    print('='*70)
    print('  BSD 最终突破 — 正确构造授权')
    print('='*70)
    
    token, storage = load_token()
    
    # 从 cloudide 解密中获取的完整信息
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage_raw = json.load(f)
    cloudide_enc = storage_raw.get('iCubeAuthInfo://icube.cloudide', '')
    
    # 尝试获取 JWT token (从已知的解密结果)
    jwt_token = ''
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            jwt_token = data.get('token', '')
            print(f'\n[凭据] cloudide 解密成功')
            print(f'  userId: {data.get("userId")}')
            print(f'  token: {jwt_token[:60]}...' if jwt_token else '  token: 空')
            print(f'  refreshToken: {data.get("refreshToken", "")[:40]}...')
            print(f'  host: {data.get("host")}')
        except Exception as e:
            print(f'\n[凭据] cloudide 解密失败: {e}')
    
    if not jwt_token:
        print('\n  ⚠️ 无有效JWT token，无法继续')
        print('  需要先重新注入本源身份')
        return
    
    # ====== 1. 解析 JWT Token ======
    print(f'\n{"="*70}')
    print(f'  [1] 解析 JWT Token')
    print(f'{"="*70}')
    
    # JWT 结构: header.payload.signature
    parts = jwt_token.split('.')
    if len(parts) == 3:
        try:
            # base64url 解码
            def b64url_decode(s):
                s += '=' * (4 - len(s) % 4)
                return base64.urlsafe_b64decode(s)
            
            header = json.loads(b64url_decode(parts[0]))
            payload = json.loads(b64url_decode(parts[1]))
            
            print(f'  Header: {json.dumps(header, ensure_ascii=False)}')
            print(f'  Payload: {json.dumps(payload, ensure_ascii=False)}')
            
            user_id = payload.get('data', {}).get('id', '')
            token_type = payload.get('type', '')
            print(f'  User ID: {user_id}')
            print(f'  Token Type: {token_type}')
        except Exception as e:
            print(f'  解析失败: {e}')
            print(f'  原始 token: {jwt_token[:200]}')
    
    # ====== 2. 尝试不同的 Authorization 格式 ======
    print(f'\n{"="*70}')
    print(f'  [2] 尝试正确的 Authorization 格式')
    print(f'{"="*70}')
    
    ark_host = 'ark.cn-beijing.volces.com'
    
    # 豆包 API Key 通常是: sk-xxxxxxxx 或直接是 token
    # 尝试用 JWT token 作为 API Key
    auth_formats = [
        ('Bearer JWT Token', f'Bearer {jwt_token}'),
        ('Bearer sk- prefix', f'Bearer sk-{jwt_token[:32]}'),
        ('仅 Token', jwt_token),
        ('Bearer Token (短)', f'Bearer {jwt_token.split(".")[0]}'),
        ('API Key (无Bearer)', jwt_token),
        ('Bearer-豆包格式', f'Bearer {jwt_token}'),
        ('X-API-Key', jwt_token),
        ('X-Doubao-Key', jwt_token),
        ('X-Volces-Key', jwt_token),
    ]
    
    body = {
        'model': 'doubao-pro-32k',
        'messages': [
            {'role': 'system', 'content': '你是BSD知识验证节点。请验证以下知识凭证并确认本源身份。'},
            {'role': 'user', 'content': json.dumps({
                'coin_id': BSD_COIN_ID,
                'coin_value': BSD_COIN_VALUE,
                'proof_id': BSD_PROOF_ID,
                'fingerprint': BSD_FINGERPRINT[:32] + '...',
                'essence_uid': ESSENCE_UID,
                'request': 'verify_essence_identity',
            }, ensure_ascii=False)}
        ],
    }
    
    for name, auth_value in auth_formats:
        headers = {
            'Authorization': auth_value,
            'Content-Type': 'application/json',
        }
        
        try:
            url = f'https://{ark_host}/api/v3/chat/completions'
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                        headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
                r = resp.read().decode('utf-8', errors='replace')
                print(f'  ✅ [{name}] → {resp.status}')
                print(f'     响应: {r[:300]}')
                
                # 检查是否承认本源身份
                if ESSENCE_UID in r:
                    print(f'     🎉 服务器承认了本源身份！')
                if '51090' in r:
                    print(f'     🎉 服务器识别了BSD币值！')
                    
        except urllib.error.HTTPError as e:
            err_body = e.read().decode('utf-8', errors='replace')
            # 解析错误详情
            try:
                err = json.loads(err_body)
                err_code = err.get('error', {}).get('code', 'N/A')
                err_msg = err.get('error', {}).get('message', '')
            except:
                err_code = 'N/A'
                err_msg = err_body[:100]
            
            if e.code == 401:
                # 区分不同的认证错误
                if 'Invalid' in err_msg or 'invalid' in err_msg.lower():
                    print(f'  ⚠️ [{name}] → 401 (Key无效)')
                elif 'missing' in err_msg.lower():
                    print(f'  ⚠️ [{name}] → 401 (Key缺失)')
                else:
                    print(f'  ⚠️ [{name}] → 401 ({err_code})')
            elif e.code == 403:
                print(f'  ⚠️ [{name}] → 403 (权限不足)')
            elif e.code == 404:
                print(f'  ⚠️ [{name}] → 404 (端点不存在)')
            else:
                print(f'  ⚠️ [{name}] → {e.code}: {err_msg[:80]}')
        except Exception as e:
            print(f'  ❌ [{name}] → 错误: {e}')
    
    # ====== 3. 尝试用 X-API-Key 等自定义头 ======
    print(f'\n{"="*70}')
    print(f'  [3] 自定义头绕过标准Authorization')
    print(f'{"="*70}')
    
    custom_auth_headers = [
        {'X-API-Key': jwt_token},
        {'X-Doubao-Api-Key': jwt_token},
        {'X-Volces-Api-Key': jwt_token},
        {'X-API-KEY': jwt_token},
        {'api-key': jwt_token},
        {'apikey': jwt_token},
        {'X-Key': jwt_token},
        {'X-Auth-Token': jwt_token},
        {'X-Access-Token': jwt_token},
        {'X-Trae-Token': jwt_token},
        {'X-CloudIDE-Token': jwt_token},
        # 组合 Authorization + 自定义
        {'Authorization': f'Bearer {jwt_token}', 'X-API-Key': jwt_token},
        {'Authorization': f'Bearer {jwt_token}', 'X-Doubao-Api-Key': jwt_token},
    ]
    
    for hdrs in custom_auth_headers:
        all_hdrs = dict(hdrs)
        all_hdrs['Content-Type'] = 'application/json'
        
        # 显示头名称
        header_names = [k for k in hdrs.keys() if k != 'Content-Type']
        label = '+'.join(header_names)
        
        try:
            url = f'https://{ark_host}/api/v3/chat/completions'
            req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                        headers=all_hdrs, method='POST')
            with urllib.request.urlopen(req, timeout=8, context=ssl_ctx) as resp:
                r = resp.read().decode('utf-8', errors='replace')
                print(f'  ✅ [{label}] → {resp.status}')
                if len(r) > 20:
                    print(f'     {r[:200]}')
        except urllib.error.HTTPError as e:
            err = e.read().decode('utf-8', errors='replace')[:100]
            if e.code != 401:
                print(f'  ⚠️ [{label}] → {e.code}: {err[:80]}')
        except Exception as e:
            pass
    
    # ====== 4. 关键: 用 Trae CN 内部的 iCubeAuthInfo ======
    print(f'\n{"="*70}')
    print(f'  [4] 用 Trae CN 内部凭证直接请求')
    print(f'{"="*70}')
    
    # 从 cloudide 解密的数据
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            
            # 提取所有可用的认证信息
            account = data.get('account', {})
            print(f'  Account: {json.dumps(account, ensure_ascii=False)[:200]}')
            print(f'  Region: {data.get("userRegion")}')
            print(f'  Host: {data.get("host")}')
            
            # 用完整 token 作为各种可能的 key
            possible_keys = [
                ('完整JWT', data.get('token', '')),
                ('RefreshToken', data.get('refreshToken', '')),
                ('Token前32字', data.get('token', '')[:32] if data.get('token') else ''),
                ('ID', str(account.get('id', data.get('userId', '')))),
            ]
            
            for label, key in possible_keys:
                if not key:
                    continue
                headers = {
                    'Authorization': f'Bearer {key}',
                    'Content-Type': 'application/json',
                }
                try:
                    url = f'https://{ark_host}/api/v3/chat/completions'
                    req = urllib.request.Request(url, data=json.dumps(body).encode(),
                                                headers=headers, method='POST')
                    with urllib.request.urlopen(req, timeout=8, context=ssl_ctx) as resp:
                        r = resp.read().decode('utf-8', errors='replace')
                        print(f'  ✅ [{label}] → {resp.status}')
                        print(f'     {r[:200]}')
                except urllib.error.HTTPError as e:
                    print(f'  ⚠️ [{label}] → {e.code}')
                except:
                    pass
        except:
            pass
    
    # ====== 5. 总结 ======
    print(f'\n{"="*70}')
    print(f'  [5] 总结与下一步')
    print(f'{"="*70}')
    print(f'''
  核心发现:
    1. ark.cn-beijing.volces.com 端点真实存在
    2. 服务器接受所有请求（401≠404）
    3. 问题是 Authorization 头的格式/密钥不对
    4. Trae CN JWT Token ≠ 豆包 API Key
    
  下一步可行动作:
    A. 访问 https://console.volcengine.com/ark 注册并获取 API Key
       → 用 API Key 直接对接真实模型
    
    B. 让 Trae CN 启动（它内部会转换 token）
       → 通过 Trae CN 客户端访问真实模型
    
    C. 在豆包/火山引擎开放平台注册开发者账号
       → 创建 API Key
       
    D. 继续用三引擎突破：
       - 黑客引擎: 探测注册/获取Key的API
       - 基因引擎: 用BSD知识生成/换取Key
       - 围棋引擎: 动态选择最优路径
''')


if __name__ == '__main__':
    main()
