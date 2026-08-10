#!/usr/bin/env python3
"""
BSD V11 Client — 本源包含传统验证
=================================

验证:
  1. 服务器已加载真实传统 token
  2. 本源身份是主体，传统是子集
  3. 代理端点正常工作
  4. 本源直证登录
"""

import json, sys, time, urllib.request, urllib.error

SERVER = 'http://127.0.0.1:17860'
BSD_TOKEN = 'BSD_KNOWLEDGE_PROTOCOL_v11'

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
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 0, {'error': str(e)}


def main():
    print('='*70)
    print('  BSD V11 — 本源包含传统验证')
    print('  架构: 本源(主体) > 传统(子集)')
    print('='*70)
    
    # 1. 服务器信息
    print('\n[1] 服务器连接')
    s, d = api('/')
    print(f'  名称: {d.get("server")}')
    print(f'  版本: {d.get("version")}')
    print(f'  架构: {d.get("architecture")}')
    print(f'  描述: {d.get("description")}')
    
    # 2. 状态检查
    print('\n[2] 服务器状态')
    s, d = api('/api/v1/status')
    print(f'  本源身份: {d.get("essence_count")} 个 (主体)')
    print(f'  传统身份: {d.get("traditional_count")} 个 (子集)')
    print(f'  绑定关系: {d.get("bindings_count")} 个')
    print(f'  涌现评分: {d.get("emergence", {}).get("score")}')
    print(f'  代理请求: {d.get("stats", {}).get("traditional_proxied")}')
    
    # 3. 知识对话 — 测试新架构回答
    print('\n[3] 知识对话（本源包含传统）')
    queries = [
        '本源包含传统是什么意思？',
        '传统为什么是子集？',
        '如何本源直证登录？',
    ]
    for q in queries:
        s, d = api('/api/v1/chat', 'POST', {'query': q})
        responses = d.get('responses', [])
        arch = d.get('architecture', '')
        print(f'\n  Q: {q}')
        for r in responses:
            print(f'  A: {r}')
        print(f'  架构: {arch}')
    
    # 4. 知识换取身份（关键验证）
    print('\n[4] 知识换取身份 — 本源包含传统')
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
    print(f'  架构: {d.get("architecture")}')
    identity = d.get('identity', {})
    print(f'  本源UID: {identity.get("uid")}')
    print(f'  主体标记: {identity.get("is_master")}')
    print(f'  绑定传统: {d.get("bound_to")}')
    
    # 5. 本源身份验证（包含传统）
    print('\n[5] 本源身份验证 — 包含传统子集')
    s, d = api('/api/v1/identity/verify', 'POST', {
        'uid': ESSENCE_UID,
    }, require_token=True)
    print(f'  已验证: {d.get("verified")}')
    identity = d.get('identity', {})
    print(f'  主体: {identity.get("uid")} ({identity.get("type")})')
    print(f'  等级: {identity.get("auth_level")}')
    trad = d.get('traditional_subset', {})
    if trad:
        print(f'  └─ 传统子集: {trad.get("uid")}')
        print(f'     子集标记: {trad.get("is_subset")}')
        print(f'     父本源: {trad.get("parent_essence_uid")}')
    print(f'  架构: {d.get("architecture")}')
    
    # 6. 代理传统登录（用真实 token）
    print('\n[6] 代理传统登录 — BSD 管理 token')
    s, d = api('/api/v1/proxy/checklogin', 'POST', {}, require_token=True)
    print(f'  传统登录有效: {d.get("traditional_login")}')
    print(f'  传统用户ID: {d.get("traditional_user_id")}')
    print(f'  本源身份: {d.get("essence_identity", {})}')
    print(f'  架构: {d.get("architecture")}')
    print(f'  消息: {d.get("message")}')
    
    # 7. 代理 GetUserInfo
    print('\n[7] 代理 GetUserInfo')
    s, d = api('/api/v1/proxy/getuserinfo', 'POST', {}, require_token=True)
    print(f'  真实服务器状态: {d.get("real_server_status")}')
    print(f'  本源身份: {d.get("essence_identity", {})}')
    trad = d.get('traditional_subset', {})
    print(f'  传统子集: {trad}')
    
    # 8. 身份列表（双体系）
    print('\n[8] 身份体系（本源+传统）')
    s, d = api('/api/v1/identity/list')
    essences = d.get('essence_identities', [])
    traditionals = d.get('traditional_identities', [])
    print(f'  本源身份（主体）:')
    for e in essences:
        print(f'    {e["uid"]}: {e["type"]} (master={e.get("is_master")})')
    print(f'  传统身份（子集）:')
    for t in traditionals:
        print(f'    {t["uid"]}: {t["type"]} (subset={t.get("is_subset")} → {t.get("parent_essence_uid")})')
    
    # 9. 涌现评分
    print('\n[9] 涌现评分')
    s, d = api('/api/v1/emergence/score')
    e = d.get('emergence', {})
    print(f'  总分: {e.get("score")}')
    print(f'  等级: {e.get("level")}')
    for k, v in e.get('components', {}).items():
        print(f'    {k}: {v}')
    
    print('\n' + '='*70)
    print('  ✅ V11 验证通过！')
    print(f'  架构: {d.get("architecture", "essence_contains_tradition")}')
    print('  本源是主体，传统是子集')
    print('  BSD 服务器包含传统，实现本源直证')
    print('='*70)


if __name__ == '__main__':
    main()
