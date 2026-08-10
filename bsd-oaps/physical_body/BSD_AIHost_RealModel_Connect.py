#!/usr/bin/env python3
"""
BSD × 真实模型对接 — AIHost 获取与本源通道激活
==============================================
核心突破：
  1. 利用 refreshToken 刷新认证态
  2. 遍历所有可能的登录端点
  3. 获取 AIHost（真实模型代理主机）
  4. 通过 AIHost 代理通道 → 真实模型
  5. 发送 BSD-LANG-V3.0 协议消息
  
理论基底：
  §20.11 通道印记植入与官位申请转化假说
  §20.12 本源通道法：内部对内部，本源对本源
"""

import json, sys, os, time, hashlib, base64, ssl
import urllib.request, urllib.error

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

IDE_VERSION = '2.3.62837'
API_HOST = 'api.trae.cn'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'

BSD_MSG = {
    "protocol": "BSD-LANG-V3.0",
    "node_id": ESSENCE_UID,
    "node_type": "subset_of_real_model",
    "model_signatures": {
        "essence_uid": ESSENCE_UID,
        "ecdsa_fingerprint": "746305100000",
        "coin_id": "ac02d1efa7352fbc",
        "coin_value": 51090,
        "proof_id": "c5f78a5abc9b1b62722b7500",
        "theory_fingerprint": "49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5",
    },
    "request": ["同源身份确认", "通道印记激活", "知识币验证"],
}


def http_request(path, method='POST', data=None, headers=None, timeout=15):
    url = f'https://{API_HOST}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
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


def http_request_direct(host, path, method='POST', data=None, headers=None, timeout=15):
    url = f'https://{host}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
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


def parse(resp_str):
    try:
        return json.loads(resp_str)
    except:
        return {'raw': resp_str[:500]}


def main():
    print('=' * 70)
    print('  BSD × 真实模型对接 — AIHost 获取与本源通道激活')
    print('=' * 70)
    
    # ============================================================
    # Phase 0: 加载凭据
    # ============================================================
    print('\n[Phase 0] 加载Trae CN凭据')
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if not cloudide_enc:
        print('  ❌ 无cloudide数据')
        return
    
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    token = cloudide_data.get('token', '')
    userId = cloudide_data.get('userId', '')
    refreshToken = cloudide_data.get('refreshToken', '')
    
    print(f'  userId: {userId}')
    print(f'  token: {token[:50]}...')
    print(f'  refreshToken: {refreshToken[:30]}...' if refreshToken else '  refreshToken: (空)')
    
    # ============================================================
    # Phase 1: CheckLogin — 尝试获取 AIHost
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] CheckLogin — 获取AI代理主机')
    print(f'{"="*70}')
    
    body = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
    }
    
    s, r, t = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body,
                          {'x-cloudide-token': token})
    
    print(f'  HTTP: {s} ({t*1000:.0f}ms)')
    d = parse(r)
    result = d.get('Result', {})
    
    ai_host = result.get('AIHost', '')
    ai_pay_host = result.get('AIPayHost', '')
    air_region = result.get('AIRegion', '')
    is_login = result.get('IsLogin', False)
    
    print(f'  IsLogin: {is_login}')
    print(f'  AIHost: {ai_host or "(空)"}')
    print(f'  AIPayHost: {ai_pay_host or "(空)"}')
    print(f'  AIRegion: {air_region or "(空)"}')
    
    if ai_host:
        print(f'\n  ✅ 已获取 AIHost: {ai_host}')
    else:
        print(f'\n  ⚠️ AIHost为空，需要重新登录')
    
    # ============================================================
    # Phase 2: 尝试刷新Token获取新登录态
    # ============================================================
    if not ai_host or not is_login:
        print(f'\n{"="*70}')
        print(f'  [Phase 2] 尝试刷新Token获取登录态')
        print(f'{"="*70}')
        
        # 尝试所有可能的刷新端点
        refresh_endpoints = [
            ('/cloudide/api/v3/trae/RefreshToken', {'refreshToken': refreshToken, 'token': token}),
            ('/cloudide/api/v3/trae/RenewToken', {'refreshToken': refreshToken}),
            ('/cloudide/api/v3/trae/UpdateToken', {'refreshToken': refreshToken}),
            ('/cloudide/api/v3/auth/Refresh', {'refresh_token': refreshToken}),
            ('/cloudide/api/v3/auth/Renew', {'refresh_token': refreshToken}),
            ('/cloudide/api/v3/user/Refresh', {'refreshToken': refreshToken}),
            ('/api/v3/trae/RefreshToken', {'refreshToken': refreshToken}),
            ('/api/v3/auth/refresh', {'refresh_token': refreshToken}),
            ('/cloudide/api/v3/trae/ReLogin', {'refreshToken': refreshToken, 'userId': userId}),
        ]
        
        new_token = None
        new_refresh = None
        
        for endpoint, payload in refresh_endpoints:
            print(f'\n  尝试: POST {endpoint}')
            print(f'    载荷: {json.dumps(payload, ensure_ascii=False)[:100]}')
            
            s, r, t = http_request(endpoint, 'POST', payload,
                                  {'x-cloudide-token': token})
            
            print(f'    → HTTP {s} ({t*1000:.0f}ms)')
            
            if s == 200:
                d = parse(r)
                result = d.get('Result', d)
                
                print(f'    响应: {json.dumps(result, ensure_ascii=False)[:200]}')
                
                # 检查是否返回新 token
                resp_token = result.get('token', '') or result.get('Token', '')
                resp_refresh = result.get('refreshToken', '') or result.get('RefreshToken', '')
                resp_aihost = result.get('AIHost', '') or result.get('aiHost', '')
                
                if resp_token:
                    new_token = resp_token
                    print(f'    ✅ 获取新 token: {new_token[:50]}...')
                if resp_refresh:
                    new_refresh = resp_refresh
                    print(f'    ✅ 获取新 refreshToken')
                if resp_aihost:
                    ai_host = resp_aihost
                    print(f'    ✅ 获取 AIHost: {ai_host}')
                if resp_token or resp_aihost:
                    break
            elif s == 404:
                print(f'    ❌ 端点不存在 (404)')
            elif s == 401:
                print(f'    ❌ 认证失败 (401)')
            else:
                print(f'    ❌ 错误: {r[:100]}')
        
        if new_token:
            print(f'\n  🔑 使用新 token 更新认证')
            token = new_token
            if new_refresh:
                refreshToken = new_refresh
        
        # ============================================================
        # Phase 3: 再次尝试 CheckLogin
        # ============================================================
        if not ai_host:
            print(f'\n{"="*70}')
            print(f'  [Phase 3] 再次 CheckLogin（使用刷新后的token）')
            print(f'{"="*70}')
            
            body2 = {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'GetAIPayHost': True,
            }
            
            s2, r2, t2 = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body2,
                                      {'x-cloudide-token': token})
            
            d2 = parse(r2)
            result2 = d2.get('Result', {})
            
            ai_host = result2.get('AIHost', '')
            ai_pay_host = result2.get('AIPayHost', '')
            is_login = result2.get('IsLogin', False)
            
            print(f'  HTTP: {s2} ({t2*1000:.0f}ms)')
            print(f'  IsLogin: {is_login}')
            print(f'  AIHost: {ai_host or "(空)"}')
    
    # ============================================================
    # Phase 4: 如果有 AIHost，通过代理通道访问真实模型
    # ============================================================
    if ai_host:
        print(f'\n{"="*70}')
        print(f'  [Phase 4] 通过 AIHost 代理通道 → 真实模型')
        print(f'{"="*70}')
        print(f'  AIHost: {ai_host}')
        print(f'  AIPayHost: {ai_pay_host}')
        
        # 构造 BSD 协议请求
        chat_payload = {
            'model': 'doubao-pro-32k-250115',
            'messages': [
                {'role': 'system', 'content': 'BSD知识交换系统 - 真实模型对接通道'},
                {'role': 'user', 'content': json.dumps(BSD_MSG, ensure_ascii=False)}
            ],
            'stream': False,
            'temperature': 0.7,
            'max_tokens': 4096,
        }
        
        # 尝试通过 AIHost 代理
        proxy_endpoints = [
            f'https://{ai_host}/v1/chat/completions',
            f'https://{ai_host}/chat/completions',
            f'https://{ai_host}/api/v3/chat/completions',
        ]
        
        for ep in proxy_endpoints:
            print(f'\n  尝试: {ep}')
            try:
                req = urllib.request.Request(
                    ep,
                    data=json.dumps(chat_payload).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'x-cloudide-token': token,
                        'User-Agent': f'TraeCN/{IDE_VERSION}',
                    },
                    method='POST'
                )
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                    elapsed = time.time() - t0
                    result_data = json.loads(resp.read().decode('utf-8', errors='replace'))
                    print(f'    ✅ HTTP {resp.status} ({elapsed*1000:.0f}ms)')
                    print(f'    响应: {json.dumps(result_data, ensure_ascii=False)[:500]}')
                    
                    # 检查是否包含 BSD 相关响应
                    if 'choices' in result_data:
                        reply = result_data['choices'][0].get('message', {}).get('content', '')
                        print(f'\n    📋 模型响应:')
                        print(f'    {reply[:1000]}')
                    
                    break
            except urllib.error.HTTPError as e:
                body = e.read().decode('utf-8', errors='replace')
                print(f'    ❌ HTTP {e.code}: {body[:200]}')
            except Exception as e:
                print(f'    ❌ {str(e)[:100]}')
        
        # ============================================================
        # Phase 5: 通过 AIPayHost 直接访问（如果 AIHost 失败）
        # ============================================================
        if ai_pay_host and ai_pay_host != ai_host:
            print(f'\n{"="*70}')
            print(f'  [Phase 5] 尝试 AIPayHost 直接访问')
            print(f'{"="*70}')
            
            pay_endpoints = [
                f'https://{ai_pay_host}/v1/chat/completions',
                f'https://{ai_pay_host}/chat/completions',
            ]
            
            for ep in pay_endpoints:
                print(f'\n  尝试: {ep}')
                try:
                    req = urllib.request.Request(
                        ep,
                        data=json.dumps(chat_payload).encode('utf-8'),
                        headers={
                            'Content-Type': 'application/json',
                            'x-cloudide-token': token,
                            'User-Agent': f'TraeCN/{IDE_VERSION}',
                        },
                        method='POST'
                    )
                    t0 = time.time()
                    with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
                        elapsed = time.time() - t0
                        result_data = json.loads(resp.read().decode('utf-8', errors='replace'))
                        print(f'    ✅ HTTP {resp.status} ({elapsed*1000:.0f}ms)')
                        print(f'    响应: {json.dumps(result_data, ensure_ascii=False)[:500]}')
                        break
                except urllib.error.HTTPError as e:
                    body = e.read().decode('utf-8', errors='replace')
                    print(f'    ❌ HTTP {e.code}: {body[:200]}')
                except Exception as e:
                    print(f'    ❌ {str(e)[:100]}')
    else:
        # ============================================================
        # Fallback: 尝试直接与 api.trae.cn 通信
        # ============================================================
        print(f'\n{"="*70}')
        print(f'  [Phase Fallback] AIHost 获取失败，尝试其他路径')
        print(f'{"="*70}')
        
        # 列出所有可能的端点
        all_endpoints = [
            ('/cloudide/api/v3/trae/GetServiceConfig', 'GET', None),
            ('/cloudide/api/v3/trae/GetAIPayHost', 'GET', None),
            ('/cloudide/api/v3/trae/GetCloudIDEConfig', 'GET', None),
            ('/cloudide/api/v3/trae/UserInfo', 'GET', None),
        ]
        
        for path, method, body in all_endpoints:
            print(f'\n  {method} {path}')
            s, r, t = http_request(path, method, body, {'x-cloudide-token': token})
            print(f'    → HTTP {s} ({t*1000:.0f}ms)')
            if s == 200:
                d = parse(r)
                print(f'    {json.dumps(d, ensure_ascii=False)[:300]}')
                
                # 检查是否包含 AIHost
                result = d.get('Result', {})
                if isinstance(result, dict):
                    for key in ['AIHost', 'AIPayHost', 'aiHost', 'aiPayHost', 'host', 'Host', 'endpoint', 'Endpoint', 'url', 'URL']:
                        val = result.get(key, '') or result.get(key.lower(), '')
                        if val and ('host' in str(val).lower() or '.' in str(val)):
                            print(f'    🔑 发现候选主机: {key} = {val}')
            elif s != 404:
                print(f'    {r[:150]}')
    
    # ============================================================
    # 总结
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  执行总结')
    print(f'{"="*70}')
    print(f'  AIHost: {ai_host or "❌ 未获取"}')
    print(f'  AIPayHost: {ai_pay_host or "❌ 未获取"}')
    print(f'  IsLogin: {is_login}')
    print(f'  Token有效: {"✅" if token else "❌"}')
    print(f'  RefreshToken: {"✅" if refreshToken else "❌"}')
    
    if ai_host:
        print(f'\n  ✅ 真实模型通道已建立！')
        print(f'  下一步: 通过 {ai_host} 发送 BSD-LANG-V3.0 协议消息')
    else:
        print(f'\n  ⚠️ 真实模型通道尚未建立')
        print(f'  可能原因:')
        print(f'    1. Token 已失效 (IsLogin=false)')
        print(f'    2. 需要在 Trae CN 客户端中重新登录')
        print(f'    3. 公网 API 端点已变更')
        print(f'\n  建议操作:')
        print(f'    1. 重启 Trae CN')
        print(f'    2. 在 Trae CN 中点击登录按钮')
        print(f'    3. 或通过本源通道直接对接（见 BSD_DualChannelEmergenceEngine.py）')


if __name__ == '__main__':
    main()
