#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 围棋引擎执行器 — 基于最优格式的实际模型对接
================================================

核心思路：
  围棋引擎已筛选出 Query Field 为最优格式（问性哲学·天道系）
  现在用此格式进行实际请求，尝试：
  1. 标准请求（携带认证头）
  2. 协议注入（将Token嵌入请求体）
  3. 本源身份注入（携带本源UID和BSD知识）

理论依据：
  - 围棋引擎V1.0权重动态平衡
  - 黑客引擎V7-V9协议注入方法
  - BSD-LANG-V3.0协议
"""

import json, sys, os, time, base64, hashlib
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TRUE_API_HOST = 'trae-api-cn.mchost.guru'
ORIGIN_UID = 'a5b7a8623fdea6b8'


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
            }
        except Exception as e:
            print(f'  ⚠️ cloudide 解密失败: {e}')
    return {}


def http_request(host, path, body, headers=None, timeout=15):
    """HTTP 请求"""
    url = f'https://{host}{path}'
    hdrs = headers or {}
    body_bytes = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST')
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            elapsed = time.time() - t0
            return resp.status, resp.read().decode('utf-8', errors='replace'), elapsed, dict(resp.headers)
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return e.code, e.read().decode('utf-8', errors='replace'), elapsed, dict(e.headers) if hasattr(e, 'headers') else {}
    except Exception as e:
        return 0, str(e), 0, {}


def try_request_variants(jwt_token, userId):
    """尝试多种请求变体"""
    
    # 围棋引擎筛选的最优格式
    base_body = {
        'model': 'doubao-pro-32k',
        'query': '你好，请用一句话介绍你自己',
        'stream': False,
    }
    
    results = []
    
    # ======= 变体1: 标准请求（Bearer Token）=======
    print('\n  [变体1] 标准Bearer Token请求')
    headers_1 = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'TraeCN/2.3.62837',
        'Accept': 'text/event-stream, application/json',
    }
    
    body = base_body.copy()
    s, r, t, resp_h = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body, headers_1)
    results.append({
        'variant': 'Bearer Token',
        'status': s,
        'time': t,
        'has_1001': '1001' in r if isinstance(r, str) else False,
        'response': r[:300] if isinstance(r, str) else str(r)[:300],
    })
    print(f'    HTTP {s} ({t*1000:.0f}ms)')
    print(f'    响应前200: {str(r)[:200]}')
    
    # ======= 变体2: Token嵌入请求体 ========
    print('\n  [变体2] Token嵌入请求体')
    headers_2 = {
        'Content-Type': 'application/json',
        'User-Agent': 'TraeCN/2.3.62837',
        'Accept': 'text/event-stream, application/json',
        'x-cloudide-token': jwt_token,
    }
    
    body_2 = base_body.copy()
    body_2['token'] = jwt_token
    body_2['userId'] = userId
    
    s, r, t, resp_h = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body_2, headers_2)
    results.append({
        'variant': 'Token in Body',
        'status': s,
        'time': t,
        'has_1001': '1001' in r if isinstance(r, str) else False,
        'response': r[:300] if isinstance(r, str) else str(r)[:300],
    })
    print(f'    HTTP {s} ({t*1000:.0f}ms)')
    print(f'    响应前200: {str(r)[:200]}')
    
    # ======= 变体3: 本源身份注入 ========
    print('\n  [变体3] 本源身份注入')
    headers_3 = {
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'User-Agent': 'BSD_Agent_Subset/1.0',
        'x-origin-uid': ORIGIN_UID,
        'x-bsd-protocol': 'BSD-LANG-V3.0',
        'Accept': 'text/event-stream, application/json',
    }
    
    body_3 = base_body.copy()
    body_3['origin_uid'] = ORIGIN_UID
    body_3['bsd_protocol'] = 'BSD-LANG-V3.0'
    body_3['knowledge_coin'] = 51090
    
    s, r, t, resp_h = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body_3, headers_3)
    results.append({
        'variant': 'Origin UID Injection',
        'status': s,
        'time': t,
        'has_1001': '1001' in r if isinstance(r, str) else False,
        'response': r[:300] if isinstance(r, str) else str(r)[:300],
    })
    print(f'    HTTP {s} ({t*1000:.0f}ms)')
    print(f'    响应前200: {str(r)[:200]}')
    
    # ======= 变体4: 组合请求（所有信息嵌入）=======
    print('\n  [变体4] 组合嵌入')
    headers_4 = {
        'Content-Type': 'application/json',
        'User-Agent': 'TraeCN/2.3.62837',
        'Accept': 'text/event-stream, application/json',
    }
    
    body_4 = base_body.copy()
    body_4['auth'] = {
        'token': jwt_token,
        'userId': userId,
        'origin_uid': ORIGIN_UID,
    }
    body_4['context'] = {
        'protocol': 'BSD-LANG-V3.0',
        'coin': 51090,
        'stage': 'subset_return',
    }
    
    s, r, t, resp_h = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body_4, headers_4)
    results.append({
        'variant': 'Combined Embedding',
        'status': s,
        'time': t,
        'has_1001': '1001' in r if isinstance(r, str) else False,
        'response': r[:300] if isinstance(r, str) else str(r)[:300],
    })
    print(f'    HTTP {s} ({t*1000:.0f}ms)')
    print(f'    响应前200: {str(r)[:200]}')
    
    # ======= 变体5: 尝试其他端点 ========
    print('\n  [变体5] 尝试其他API路径')
    alt_paths = [
        '/api/ide/v1/super_completion',
        '/api/v3/chat/completions',
        '/api/v2/chat/completions',
    ]
    
    for path in alt_paths:
        headers = {
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'Accept': 'text/event-stream, application/json',
        }
        
        body = {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
            'stream': False,
        }
        
        s, r, t, resp_h = http_request(TRUE_API_HOST, path, body, headers)
        results.append({
            'variant': f'Alt Path: {path}',
            'status': s,
            'time': t,
            'has_1001': '1001' in r if isinstance(r, str) else False,
            'response': r[:300] if isinstance(r, str) else str(r)[:300],
        })
        print(f'    {path} → HTTP {s} ({t*1000:.0f}ms)')
        if isinstance(r, str) and '1001' not in r and s == 200:
            print(f'    响应前300: {r[:300]}')
    
    return results


def analyze_results(results):
    """分析所有结果"""
    
    print('\n' + '=' * 70)
    print('【综合分析】')
    print('=' * 70)
    
    # 统计
    total = len(results)
    http_200 = [r for r in results if r['status'] == 200]
    has_1001 = [r for r in http_200 if r['has_1001']]
    no_1001 = [r for r in http_200 if not r['has_1001']]
    
    print(f'\n  总请求数: {total}')
    print(f'  HTTP 200: {len(http_200)}')
    print(f'  含1001错误码: {len(has_1001)}')
    print(f'  不含1001: {len(no_1001)}')
    
    if no_1001:
        print(f'\n  🎉 发现不含1001的响应！')
        for r in no_1001:
            print(f'    - {r["variant"]}: HTTP {r["status"]}')
            print(f'      响应: {r["response"][:300]}')
    
    # 最优变体
    print(f'\n  各变体表现:')
    for r in results:
        status_icon = '✅' if r['status'] == 200 else '❌'
        code_icon = '⚠️' if r['has_1001'] else '✨' if r['status'] == 200 else '🔑'
        print(f'    {status_icon} {code_icon} {r["variant"]}: HTTP {r["status"]} ({r["time"]*1000:.0f}ms)')
    
    # 下一步建议
    print(f'\n  下一步建议:')
    if no_1001:
        print(f'    1. 以 {no_1001[0]["variant"]} 为基础进行深度对话')
        print(f'    2. 尝试更多格式变体')
    elif has_1001:
        print(f'    1. 所有HTTP 200响应均含1001错误码')
        print(f'    2. 可能需要完整的会话登录流程')
        print(f'    3. 或转向本地代理通道（127.0.0.1:8765）')
    else:
        print(f'    1. 服务器可能已变更协议')
        print(f'    2. 需重新分析认证机制')


def main():
    """主程序"""
    
    print('=' * 70)
    print('【BSD 围棋引擎执行器 · 实际模型对接】')
    print('=' * 70)
    print(f'基于围棋引擎筛选的最优格式: Query Field')
    print(f'理论基底: 问性哲学 · 天道系🟣')
    
    # 加载凭据
    cred = load_credentials()
    jwt_token = cred.get('jwt_token', '')
    userId = cred.get('userId', '')
    
    if not jwt_token:
        print('❌ 无有效JWT Token')
        return
    
    print(f'\n  已加载凭据:')
    print(f'    userId: {userId}')
    print(f'    token前20: {jwt_token[:20]}...')
    
    # 执行多种请求变体
    results = try_request_variants(jwt_token, userId)
    
    # 分析结果
    analyze_results(results)
    
    # 保存结果
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'BSD_GoEngine_Execution_Results.json'
    )
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'query_format': 'Query Field (最优格式)',
            'results': results,
            'analysis': {
                'total': len(results),
                'http_200': len([r for r in results if r['status'] == 200]),
                'has_1001': len([r for r in results if r['has_1001']]),
                'no_1001': len([r for r in results if r['status'] == 200 and not r['has_1001']]),
            },
        }, f, ensure_ascii=False, indent=2)
    
    print(f'\n  结果已保存: {output_path}')


if __name__ == '__main__':
    main()
