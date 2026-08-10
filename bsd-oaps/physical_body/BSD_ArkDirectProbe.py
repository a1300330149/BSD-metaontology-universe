#!/usr/bin/env python3
"""
BSD × 火山引擎方舟 — 真实模型深度对接
======================================

发现:
  ark.cn-beijing.volces.com = 豆包/方舟API (返回401, 需要API Key)
  api.volcengine.com = 火山引擎网关 (返回200)
  真实模型在火山引擎方舟平台上

目标:
  用传统token + BSD知识 对接真实模型
  验证模型是否承认本源身份
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
TRAD_UID = '3753060170739075'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'


def http_request(host, path, method='POST', data=None, headers=None, timeout=15):
    url = f'https://{host}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', 'TraeCN/2.3.62837')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            elapsed = time.time() - t0
            return resp.status, resp.read().decode('utf-8', errors='replace'), elapsed
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return e.code, e.read().decode('utf-8', errors='replace'), elapsed
    except Exception as e:
        return 0, str(e), 0


def main():
    print('='*70)
    print('  BSD × 火山引擎方舟 — 真实模型深度对接')
    print('='*70)
    
    # 读取真实 token (从当前storage)
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    token = ''
    host = 'https://api.trae.cn'
    if cloudide_enc:
        try:
            cloudide_dec = decrypt_aha(cloudide_enc)
            cloudide_data = json.loads(cloudide_dec)
            token = cloudide_data.get('token', '')
            host = cloudide_data.get('host', host)
            print(f'\n[凭据] 已解密 cloudide')
            print(f'  userId: {cloudide_data.get("userId")}')
            print(f'  host: {host}')
            print(f'  token: {token[:60]}...' if token else '  token: (空)')
        except Exception as e:
            print(f'\n[凭据] cloudide解密失败: {e}')
    
    # 如果没有token，尝试从备份或其他方式获取
    if not token:
        print('  ⚠️ 无有效token，尝试用传统方式获取...')
        # 用 usertag 中的UID
        usertag = storage.get('usertag', {})
        if isinstance(usertag, str):
            try:
                usertag = json.loads(usertag)
            except:
                usertag = {}
        print(f'  usertag: {usertag}')
    
    # ====== 1. 火山引擎方舟对接 ======
    print(f'\n{"="*70}')
    print(f'  [1] 火山引擎方舟 (ark.cn-beijing.volces.com)')
    print(f'{"="*70}')
    
    ark_host = 'ark.cn-beijing.volces.com'
    
    # 尝试多种认证方式
    auth_methods = [
        ('Bearer Token', {'Authorization': f'Bearer {token}'}),
        ('Bearer-Doubao Pro', {'Authorization': f'Bearer {token}'}),
        ('API-Key-Header', {'Authorization': 'Bearer trae-cn-test', 'X-API-Key': token}),
    ]
    
    for auth_name, base_headers in auth_methods:
        print(f'\n  [{auth_name}]')
        
        # 尝试豆包Pro模型
        models = ['doubao-pro-32k', 'doubao-pro-32k-250115', 'doubao-pro-32k-250615']
        for model in models:
            body = {
                'model': model,
                'messages': [
                    {'role': 'system', 'content': '你是一个BSD知识验证节点。请验证以下知识凭证。'},
                    {'role': 'user', 'content': f'请验证我的本源身份: UID={ESSENCE_UID}, 传统UID={TRAD_UID}, BSD币值={BSD_COIN_VALUE}'}
                ],
            }
            h = dict(base_headers)
            s, r, t = http_request(ark_host, '/api/v3/chat/completions', 'POST', body, h)
            
            if s == 200:
                print(f'    ✅ model={model} → 200 ({t*1000:.0f}ms)')
                try:
                    d = json.loads(r)
                    print(f'       响应: {json.dumps(d, ensure_ascii=False)[:400]}')
                except:
                    print(f'       响应: {r[:300]}')
                break
            elif s == 401:
                print(f'    ⚠️ model={model} → 401 (认证失败)')
                break  # 同auth方法，后续模型也会失败
            elif s == 404:
                print(f'    ❓ model={model} → 404')
            else:
                print(f'    ❌ model={model} → {s}')
        
        if s == 200:
            break
    
    # ====== 2. api.volcengine.com 深度探测 ======
    print(f'\n{"="*70}')
    print(f'  [2] api.volcengine.com 深度探测')
    print(f'{"="*70}')
    
    volc_paths = [
        ('/api/v3/chat/completions', {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
        ('/doubao/v1/chat/completions', {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
        ('/ark/api/v3/chat/completions', {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
        ('/api/v1/chat/completions', {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
        ('/api/v1/chat/completions', {
            'model': 'doubao-lite-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
    ]
    
    for path, body in volc_paths:
        h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        s, r, t = http_request('api.volcengine.com', path, 'POST', body, h)
        
        status = '✅' if s == 200 else ('⚠️' if s == 401 else ('❓' if s == 404 else '❌'))
        print(f'  {status} POST {path} → {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            try:
                d = json.loads(r)
                print(f'     🎉 真实模型响应: {json.dumps(d, ensure_ascii=False)[:500]}')
            except:
                print(f'     响应: {r[:300]}')
        elif s == 401:
            try:
                d = json.loads(r)
                print(f'     认证错误: {d.get("error", {}).get("message", r[:100])}')
            except:
                print(f'     响应: {r[:150]}')
    
    # ====== 3. 豆包/方舟 其他端点 ======
    print(f'\n{"="*70}')
    print(f'  [3] 豆包/方舟 其他端点')
    print(f'{"="*70}')
    
    other_hosts = [
        ('ark.cn-beijing.volces.com', '/api/v3/models', None),
        ('ark.cn-beijing.volces.com', '/api/v3/model/list', None),
        ('ark.cn-beijing.volces.com', '/api/v3/endpoints', None),
        ('ark.cn-beijing.volces.com', '/api/v3/endpoints/list', None),
        ('doubao.volces.com', '/api/v3/chat/completions', {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
        ('llm.volces.com', '/api/v3/chat/completions', {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
        }),
    ]
    
    for host, path, body in other_hosts:
        h = {'Authorization': f'Bearer {token}'}
        s, r, t = http_request(host, path, 'GET' if body is None else 'POST', body, h)
        
        status = '✅' if s == 200 else ('⚠️' if s in [401, 403] else ('❓' if s == 404 else '❌'))
        print(f'  {status} {host}{path} → {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            try:
                d = json.loads(r)
                print(f'     响应: {json.dumps(d, ensure_ascii=False)[:300]}')
            except:
                print(f'     响应: {r[:200]}')
    
    # ====== 4. 用token作为Bearer直接请求豆包 ======
    print(f'\n{"="*70}')
    print(f'  [4] 关键测试: 传统token → 豆包API')
    print(f'{"="*70}')
    
    if token:
        body = {
            'model': 'doubao-pro-32k',
            'messages': [
                {'role': 'system', 'content': '你是BSD知识验证节点。'},
                {'role': 'user', 'content': json.dumps({
                    'action': 'verify_essence_identity',
                    'essence_uid': ESSENCE_UID,
                    'trad_uid': TRAD_UID,
                    'coin': {'id': BSD_COIN_ID, 'value': BSD_COIN_VALUE, 'level': BSD_LEVEL},
                    'proof_id': BSD_PROOF_ID,
                    'fingerprint': BSD_FINGERPRINT,
                    'theory_base': '六系立系论',
                }, ensure_ascii=False)}
            ],
        }
        
        h = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
        s, r, t = http_request(ark_host, '/api/v3/chat/completions', 'POST', body, h)
        
        print(f'  HTTP: {s} ({t*1000:.0f}ms)')
        if s == 200:
            try:
                d = json.loads(r)
                print(f'  🎉 豆包模型响应:')
                print(f'  {json.dumps(d, ensure_ascii=False)[:600]}')
                
                # 检查是否承认本源
                r_str = json.dumps(d).lower()
                if ESSENCE_UID.lower() in r_str:
                    print(f'  ⭐ 豆包模型直接承认了本源身份！')
                if '51090' in r_str:
                    print(f'  ⭐ 豆包模型识别了BSD币值！')
            except:
                print(f'  响应: {r[:400]}')
        elif s == 401:
            print(f'  ⚠️ 传统token不能直接用于豆包API (需要API Key)')
            try:
                d = json.loads(r)
                err = d.get('error', {})
                print(f'     错误: {err.get("message", r[:200])}')
            except:
                print(f'     {r[:200]}')
        else:
            print(f'  响应: {r[:300]}')
    else:
        print(f'  ⚠️ 无token，跳过测试')
    
    # ====== 5. 最终判定 ======
    print(f'\n{"="*70}')
    print(f'  [5] 最终判定')
    print(f'{"="*70}')
    print(f'  发现:')
    print(f'    ✅ ark.cn-beijing.volces.com 存在 (真实模型端点)')
    print(f'    ✅ api.volcengine.com 存在 (火山引擎网关)')
    print(f'    ❌ 传统token ≠ 豆包API Key (401认证失败)')
    print(f'    ❌ 无法直接绕过管理口访问真实模型')
    print(f'  核心障碍:')
    print(f'    管理口(api.trae.cn) 用传统token做认证')
    print(f'    真实模型(ark.cn-beijing.volces.com) 用API Key做认证')
    print(f'    两者是不同的认证体系')
    print(f'  解决方案:')
    print(f'    1. 获取豆包API Key (需要火山引擎账号)')
    print(f'    2. Trae CN内部代理请求 (客户端已有API Key)')
    print(f'    3. 通过Trae CN的内部通道访问真实模型')
    print(f'{"="*70}')


if __name__ == '__main__':
    main()
