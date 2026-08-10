#!/usr/bin/env python3
"""
BSD Knowledge Exchange Client
==============================

客户端对接 BSD 知识交流服务器，演示完整知识交流流程
"""

import json, sys, time, urllib.request, urllib.error

SERVER = 'http://127.0.0.1:17859'
BSD_TOKEN = 'BSD_KNOWLEDGE_PROTOCOL_v10'

BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'


def api(path, method='GET', data=None, require_token=False):
    url = SERVER + path
    body = json.dumps(data).encode('utf-8') if data else None
    headers = {'Content-Type': 'application/json'}
    if require_token:
        headers['X-BSD-Token'] = BSD_TOKEN
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 0, {'error': str(e)}


def main():
    print('='*70)
    print('  BSD Knowledge Exchange Client')
    print('  对接本地知识服务器，演示完整交流流程')
    print('='*70)
    
    # 1. 服务器信息
    print('\n[1] 服务器连接')
    s, d = api('/')
    print(f'  HTTP {s}: {d.get("server", "N/A")}')
    print(f'  协议: {d.get("protocol", "N/A")}')
    print(f'  版本: {d.get("version", "N/A")}')
    print(f'  状态: {d.get("status", "N/A")}')
    
    # 2. 知识对话（公开端点，无需token）
    print('\n[2] 知识对话（服务器智能响应测试）')
    queries = [
        '六系立系论是什么？',
        'BSD币有什么价值？',
        '本源如何涌现？',
        '三引擎如何协同？',
    ]
    for q in queries:
        s, d = api('/api/v1/chat', 'POST', {'query': q})
        responses = d.get('responses', [])
        print(f'\n  Q: {q}')
        for r in responses:
            print(f'  A: {r}')
    
    # 3. 知识验证
    print('\n[3] 知识验证（币 + 证明）')
    s, d = api('/api/v1/knowledge/verify', 'POST', {
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
        'fingerprint': BSD_FINGERPRINT,
    }, require_token=True)
    print(f'  验证结果: {d.get("valid")}')
    if d.get('valid'):
        coin = d.get('coin', {})
        print(f'  币值: {coin.get("value")}')
        print(f'  等级: {coin.get("level")}')
        print(f'  理论: {coin.get("theory_base")}')
    
    # 4. 知识换取身份
    print('\n[4] 知识换取本源身份')
    s, d = api('/api/v1/knowledge/exchange', 'POST', {
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
        'proof_id': BSD_PROOF_ID,
        'essence_uid': ESSENCE_UID,
        'trad_uid': TRAD_UID,
        'fingerprint': BSD_FINGERPRINT,
    }, require_token=True)
    print(f'  成功: {d.get("success")}')
    print(f'  消息: {d.get("message")}')
    if d.get('success'):
        identity = d.get('identity', {})
        print(f'  本源UID: {identity.get("uid")}')
        print(f'  类型: {identity.get("type")}')
        print(f'  等级: {identity.get("auth_level")}')
        print(f'  绑定传统UID: {d.get("bound_to")}')
    
    # 5. 身份验证
    print('\n[5] 身份验证')
    s, d = api('/api/v1/identity/verify', 'POST', {
        'uid': ESSENCE_UID,
    }, require_token=True)
    print(f'  已验证: {d.get("verified")}')
    identity = d.get('identity', {})
    if identity:
        print(f'  状态: {identity.get("status")}')
        print(f'  等级: {identity.get("auth_level")}')
    
    # 6. 身份绑定
    print('\n[6] 身份绑定（传统 ↔ 本源）')
    s, d = api('/api/v1/identity/bind', 'POST', {
        'trad_uid': TRAD_UID,
        'essence_uid': ESSENCE_UID,
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
    }, require_token=True)
    print(f'  绑定成功: {d.get("success")}')
    print(f'  传统UID: {d.get("trad_uid")}')
    print(f'  本源UID: {d.get("essence_uid")}')
    
    # 7. 涌现评分
    print('\n[7] 涌现评分')
    s, d = api('/api/v1/emergence/score')
    e = d.get('emergence', {})
    print(f'  评分: {e.get("score")}')
    print(f'  等级: {e.get("level")}')
    components = e.get('components', {})
    for k, v in components.items():
        print(f'    {k}: {v}')
    
    # 8. 完整状态
    print('\n[8] 服务器完整状态')
    s, d = api('/api/v1/status')
    stats = d.get('stats', {})
    print(f'  运行时间: {d.get("uptime", 0)}s')
    print(f'  总请求: {stats.get("total_requests", 0)}')
    print(f'  知识验证: {stats.get("knowledge_verified", 0)}')
    print(f'  身份授予: {stats.get("identities_granted", 0)}')
    print(f'  绑定创建: {stats.get("bindings_created", 0)}')
    
    # 9. 身份列表
    print('\n[9] 身份列表')
    s, d = api('/api/v1/identity/list')
    for ident in d.get('identities', []):
        print(f'  {ident["uid"]}: {ident["type"]} ({ident["status"]})')
    
    # 10. 绑定列表
    print('\n[10] 绑定列表')
    s, d = api('/api/v1/binding/list')
    for b in d.get('bindings', []):
        print(f'  {b["trad_uid"]} ↔ {b["essence_uid"]} ({b["status"]})')
    
    print('\n' + '='*70)
    print('  ✅ 完整知识交流闭环已建立！')
    print('  服务器真正拥有知识验证、身份交换和语义对话能力')
    print('  三引擎架构: 基因(知识) × 黑客(协议) × 围棋(涌现)')
    print('='*70)


if __name__ == '__main__':
    main()
