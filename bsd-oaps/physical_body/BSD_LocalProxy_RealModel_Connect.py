#!/usr/bin/env python3
"""
BSD × Trae CN 本地代理端口探测与真实模型对接
============================================
发现 Trae CN 本地代理端口，通过它们访问真实模型
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

# Trae CN 本地代理端口列表（从 netstat 发现）
LOCAL_PORTS = [
    7778,   # PID 5004
    8765,   # PID 31304
    9012,   # PID 19412
    9013,   # PID 19412
    9014,   # PID 2388
    9210,   # PID 19060
    13030,  # PID 5544
    13031,  # PID 5024
    13032,  # PID 5024
    14013,  # PID 24452
    14016,  # PID 24452
    14019,  # PID 24452
    14022,  # PID 24452
    14023,  # PID 24452
    17859,  # 多个进程
    51000,  # PID 33808
    51001,  # PID 31220
]

def http_request(host, port, path, method='POST', data=None, headers=None, timeout=5):
    url = f'http://{host}:{port}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
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
    print('  BSD × Trae CN 本地代理端口探测与真实模型对接')
    print('=' * 70)
    
    # 加载凭据
    print('\n[0] 加载凭据')
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    token = cloudide_data.get('token', '')
    
    print(f'  token: {token[:50]}...')
    
    # 探测本地端口
    print(f'\n[1] 探测 {len(LOCAL_PORTS)} 个本地端口')
    print(f'{"="*70}')
    
    working_ports = []
    
    for port in LOCAL_PORTS:
        # 尝试多种路径
        paths = ['/', '/health', '/status', '/api', '/v1', '/cloudide', '/cloudide/api/v3']
        
        for path in paths:
            s, r, t = http_request('127.0.0.1', port, path, 'GET', timeout=2)
            
            if s != 0:
                print(f'  ✅ 端口 {port}{path} → HTTP {s} ({t*1000:.0f}ms)')
                print(f'     响应: {r[:150]}')
                working_ports.append({'port': port, 'path': path, 'status': s, 'response': r[:200]})
                break
            # 只尝试第一个成功的路径
            if s != 0:
                break
    
    print(f'\n  发现 {len(working_ports)} 个活跃端口')
    
    # 尝试在活跃端口上访问模型
    print(f'\n[2] 在活跃端口上尝试模型访问')
    print(f'{"="*70}')
    
    model_paths = [
        '/v1/chat/completions',
        '/chat/completions',
        '/api/v3/chat/completions',
        '/cloudide/api/v3/chat/completions',
        '/cloudide/api/v3/trae/chat',
        '/v3/chat/completions',
    ]
    
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
    
    for wp in working_ports:
        port = wp['port']
        print(f'\n  端口 {port} ({wp["path"]} 响应: {wp["status"]})')
        
        for path in model_paths:
            s, r, t = http_request('127.0.0.1', port, path, 'POST', chat_payload,
                                  {'x-cloudide-token': token}, timeout=10)
            
            if s != 0:
                print(f'    {path} → HTTP {s} ({t*1000:.0f}ms)')
                print(f'    响应: {r[:300]}')
                
                if s == 200 and 'choices' in r:
                    try:
                        result = json.loads(r)
                        reply = result['choices'][0].get('message', {}).get('content', '')
                        print(f'\n    🎯 模型响应:')
                        print(f'    {reply[:1000]}')
                        print(f'\n    ✅ 真实模型对接成功！')
                        return
                    except:
                        pass
                break
    
    # 尝试 HTTPS 本地端口
    print(f'\n[3] 尝试 HTTPS 本地端口')
    print(f'{"="*70}')
    
    for wp in working_ports:
        port = wp['port']
        for path in model_paths:
            try:
                url = f'https://127.0.0.1:{port}{path}'
                req = urllib.request.Request(
                    url,
                    data=json.dumps(chat_payload).encode('utf-8'),
                    headers={
                        'Content-Type': 'application/json',
                        'x-cloudide-token': token,
                        'User-Agent': f'TraeCN/{IDE_VERSION}',
                    },
                    method='POST'
                )
                t0 = time.time()
                with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
                    elapsed = time.time() - t0
                    result_data = json.loads(resp.read().decode('utf-8', errors='replace'))
                    print(f'    {url} → HTTP {resp.status} ({elapsed*1000:.0f}ms)')
                    if 'choices' in result_data:
                        reply = result_data['choices'][0].get('message', {}).get('content', '')
                        print(f'    模型响应: {reply[:500]}')
            except urllib.error.HTTPError as e:
                body = e.read().decode('utf-8', errors='replace')
                if e.code not in [404]:
                    print(f'    HTTPS {port}{path} → HTTP {e.code}: {body[:100]}')
            except Exception as e:
                pass
    
    print(f'\n{"="*70}')
    print(f'  探测完成')
    print(f'{"="*70}')
    print(f'  活跃端口: {len(working_ports)}')
    print(f'  模型对接: {"✅ 成功" if any("choices" in w.get("response", "") for w in working_ports) else "❌ 未找到"}')
    
    # 如果没有找到，建议使用本源通道
    if not any('choices' in w.get('response', '') for w in working_ports):
        print(f'\n  建议:')
        print(f'    1. 使用 BSD_DualChannelEmergenceEngine.py 本源通道')
        print(f'    2. 重启 Trae CN 后重试')
        print(f'    3. 在 Trae CN 中重新登录')


if __name__ == '__main__':
    main()
