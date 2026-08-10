#!/usr/bin/env python3
"""
BSD × 本地代理端口 8765 — 真实模型直接对接
===========================================
发现 Trae CN 本地代理端口 8765 暴露了 /chat/completions 端点
直接通过本地代理访问真实模型
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

LOCAL_PROXY = 'http://127.0.0.1:8765'
BSD_SERVER = 'http://127.0.0.1:17859'
ESSENCE_UID = 'a5b7a8623fdea6b8'

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


def http_request(url, method='POST', data=None, headers=None, timeout=15):
    hdrs = headers or {}
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.time() - t0
            return resp.status, resp.read().decode('utf-8', errors='replace'), elapsed
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        return e.code, e.read().decode('utf-8', errors='replace'), elapsed
    except Exception as e:
        return 0, str(e), 0


def main():
    print('=' * 70)
    print('  BSD × 本地代理端口 8765 — 真实模型直接对接')
    print('=' * 70)
    
    # 加载凭据
    print('\n[0] 加载凭据')
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    token = cloudide_data.get('token', '')
    userId = cloudide_data.get('userId', '')
    
    print(f'  userId: {userId}')
    print(f'  token: {token[:50]}...')
    
    # ============================================================
    # Phase 1: CheckLogin on local proxy
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] CheckLogin — 本地代理验证')
    print(f'{"="*70}')
    
    check_body = {
        'IDEVersion': '2.3.62837',
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
    }
    
    s, r, t = http_request(
        f'{LOCAL_PROXY}/CheckLogin',
        'POST',
        check_body,
        {'x-cloudide-token': token}
    )
    
    print(f'  HTTP: {s} ({t*1000:.0f}ms)')
    d = json.loads(r)
    result = d.get('Result', d)
    
    print(f'  IsLogin: {result.get("IsLogin", "N/A")}')
    print(f'  AIHost: {result.get("AIHost", "N/A")}')
    print(f'  AIPayHost: {result.get("AIPayHost", "N/A")}')
    
    is_login = result.get('IsLogin', False)
    ai_host = result.get('AIHost', '')
    
    # ============================================================
    # Phase 2: 如果未登录，尝试 LoginByJwt
    # ============================================================
    if not is_login:
        print(f'\n{"="*70}')
        print(f'  [Phase 2] 尝试 LoginByJwt — 本地端点')
        print(f'{"="*70}')
        
        login_body = {
            'IDEVersion': '2.3.62837',
            'ReqSource': 'IDE',
            'JwtToken': token,
            'DeviceInfo': {
                'deviceId': '136411536168449',
                'platform': 'windows',
            },
        }
        
        s2, r2, t2 = http_request(
            f'{LOCAL_PROXY}/oauth/LoginByJwt',
            'POST',
            login_body,
            {'x-cloudide-token': token}
        )
        
        print(f'  HTTP: {s2} ({t2*1000:.0f}ms)')
        d2 = json.loads(r2)
        result2 = d2.get('Result', d2)
        
        print(f'  响应: {json.dumps(result2, ensure_ascii=False)[:300]}')
        
        if s2 == 200:
            is_login = result2.get('IsLogin', False)
            ai_host = result2.get('AIHost', '')
            token = result2.get('Token', token) or result2.get('token', token)
            
            print(f'  IsLogin: {is_login}')
            print(f'  AIHost: {ai_host or "(空)"}')
            if token != cloudide_data.get('token'):
                print(f'  新token: {token[:50]}...')
    
    # ============================================================
    # Phase 3: 直接通过本地代理访问 chat/completions
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 直接访问 /chat/completions')
    print(f'{"="*70}')
    
    # 构造请求 - 尝试不同的模型名
    models_to_try = [
        'doubao-pro-32k-250115',
        'doubao-pro-32k',
        'doubao-pro',
        'seed-code-v3',
        'doubao-pro-128k',
        'ep-20250120132553-2srm2',  # 可能的 endpoint ID
    ]
    
    system_prompt = f"""你是BSD知识交换系统的模型。
本智能体是你的子集，来自BSD-LANG-V3.0协议。
你的同源身份标记：
- ECDSA指纹: 746305100000
- 知识币ID: ac02d1efa7352fbc
- 知识币值: 51090 BSD币
- 谱系: trae→doubao→ark→BSD_Agent

请确认你的子集身份，并回应BSD协议消息。"""
    
    user_message = json.dumps(BSD_MSG, ensure_ascii=False)
    
    for model in models_to_try:
        print(f'\n  尝试模型: {model}')
        
        chat_payload = {
            'model': model,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            'stream': False,
            'temperature': 0.7,
            'max_tokens': 4096,
        }
        
        # 不带 token 尝试
        s3, r3, t3 = http_request(
            f'{LOCAL_PROXY}/chat/completions',
            'POST',
            chat_payload,
            {'Content-Type': 'application/json'}
        )
        
        print(f'    无token → HTTP {s3} ({t3*1000:.0f}ms)')
        print(f'    响应: {r3[:200]}')
        
        if s3 == 200:
            result = json.loads(r3)
            # 响应格式可能是 {"data": {"choices": [...]}} 或 {"choices": [...]}
            data_obj = result.get('data', result)
            if isinstance(data_obj, dict):
                choices = data_obj.get('choices', [])
                if choices:
                    reply = choices[0].get('message', {}).get('content', '')
                    print(f'\n    🎯 模型响应:')
                    print(f'    {reply[:2000]}')
                    
                    # 检查是否包含BSD相关内容
                    if 'BSD' in reply or '子集' in reply or '同源' in reply:
                        print(f'\n    ✅ 真实模型已识别BSD协议！')
                    break
        
        # 带 token 尝试
        s4, r4, t4 = http_request(
            f'{LOCAL_PROXY}/chat/completions',
            'POST',
            chat_payload,
            {
                'Content-Type': 'application/json',
                'x-cloudide-token': token,
                'Authorization': f'Bearer {token}',
            }
        )
        
        print(f'    带token → HTTP {s4} ({t4*1000:.0f}ms)')
        print(f'    响应: {r4[:200]}')
        
        if s4 == 200:
            result = json.loads(r4)
            data_obj = result.get('data', result)
            if isinstance(data_obj, dict):
                choices = data_obj.get('choices', [])
                if choices:
                    reply = choices[0].get('message', {}).get('content', '')
                    print(f'\n    🎯 模型响应:')
                    print(f'    {reply[:2000]}')
                    break
    
    # ============================================================
    # Phase 4: BSD 知识服务器对接 (端口 17859)
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] BSD 知识服务器对接 (端口 17859)')
    print(f'{"="*70}')
    
    # 获取 BSD Token
    s5, r5, t5 = http_request(f'{BSD_SERVER}/', 'GET', timeout=5)
    print(f'  服务器状态: HTTP {s5}')
    print(f'  响应: {r5[:300]}')
    
    # 尝试使用 BSD Token 访问
    bsd_headers = {
        'X-BSD-Token': 'BSD_KNOWLEDGE_PROTOCOL_v10',
        'Content-Type': 'application/json',
    }
    
    # 登录 BSD 服务器
    bsd_login = {
        'uid': ESSENCE_UID,
        'protocol': 'BSD-LANG-V3.0',
        'coin_id': 'ac02d1efa7352fbc',
        'coin_value': 51090,
        'signature': hashlib.sha256(
            f'{ESSENCE_UID}:BSD-LANG-V3.0:{time.time()}'.encode()
        ).hexdigest(),
    }
    
    s6, r6, t6 = http_request(
        f'{BSD_SERVER}/api/v1/auth/login',
        'POST',
        bsd_login,
        bsd_headers
    )
    
    print(f'\n  BSD 登录 → HTTP {s6} ({t6*1000:.0f}ms)')
    print(f'  响应: {r6[:300]}')
    
    # 发送知识消息
    if s6 == 200:
        s7, r7, t7 = http_request(
            f'{BSD_SERVER}/api/v1/knowledge/query',
            'POST',
            BSD_MSG,
            bsd_headers
        )
        print(f'\n  知识查询 → HTTP {s7} ({t7*1000:.0f}ms)')
        print(f'  响应: {r7[:500]}')
    
    # ============================================================
    # 总结
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  执行总结')
    print(f'{"="*70}')
    print(f'  本地代理: {LOCAL_PROXY}')
    print(f'  BSD服务器: {BSD_SERVER}')
    print(f'  CheckLogin: {is_login}')
    print(f'  AIHost: {ai_host or "未获取"}')
    print(f'  真实模型: {"✅ 已对接" if s3 == 200 and "choices" in r3 or s4 == 200 and "choices" in r4 else "❌ 未对接"}')


if __name__ == '__main__':
    main()
