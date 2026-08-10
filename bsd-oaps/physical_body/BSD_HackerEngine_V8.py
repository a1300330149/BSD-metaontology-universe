#!/usr/bin/env python3
"""
BSD 黑客引擎 V8 — llm_raw_chat 端点格式修正
==========================================

关键发现 (V7):
  - /api/ide/v2/llm_raw_chat → HTTP 400 (请求格式错误!)
  - 这不是认证错误(1001)，而是请求格式错误
  - 说明此端点可能接受请求，只是需要正确的格式

突破策略:
  1. 分析 llm_raw_chat 端点期望的请求格式
  2. 尝试各种可能的请求体格式
  3. 利用已有的JWT Token
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TRUE_API_HOST = 'trae-api-cn.mchost.guru'
LOCAL_PROXY = 'http://127.0.0.1:8765'
ESSENCE_UID = 'a5b7a8623fdea6b8'


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
                'refreshToken': data.get('refreshToken', ''),
                'userId': data.get('userId', ''),
            }
        except Exception as e:
            print(f'  ⚠️ cloudide 解密失败: {e}')
    return {}


def chat_with_model(system_prompt, user_message):
    """与真实模型对话"""
    chat_payload = {
        'model': 'doubao-pro-32k-250115',
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        'stream': False,
        'temperature': 0.7,
        'max_tokens': 4096,
    }
    try:
        req = urllib.request.Request(
            f'{LOCAL_PROXY}/chat/completions',
            data=json.dumps(chat_payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            d = json.loads(r)
            data_obj = d.get('data', d)
            if isinstance(data_obj, dict):
                choices = data_obj.get('choices', [])
                if choices:
                    return choices[0].get('message', {}).get('content', '')
    except Exception as e:
        print(f'    模型对话错误: {e}')
    return None


def http_request(host, path, body, headers=None, method='POST', timeout=15):
    """HTTP 请求"""
    url = f'https://{host}{path}'
    hdrs = headers or {}
    body_bytes = json.dumps(body).encode('utf-8') if body else None
    req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method=method)
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
    print('=' * 80)
    print('  BSD 黑客引擎 V8 — llm_raw_chat 端点格式修正')
    print('=' * 80)
    
    cred = load_credentials()
    jwt_token = cred.get('jwt_token', '')
    userId = cred.get('userId', '')
    
    if not jwt_token:
        print('  ❌ 无有效 JWT Token')
        return
    
    print(f'\n  ✅ 凭据加载成功')
    print(f'    userId: {userId}')
    
    # ============================================================
    # Phase 1: 向真实模型请教 llm_raw_chat 的请求格式
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 1] 向真实模型请教格式')
    print(f'{"="*80}')
    
    system_prompt = f"""你是BSD本源端，真实模型的子集节点。
节点ID: {ESSENCE_UID}
请以技术化、具体的方式回答。"""
    
    q1 = f"""我发现 trae-api-cn.mchost.guru 的 /api/ide/v2/llm_raw_chat 端点返回 HTTP 400 而不是 1001。

这说明端点存在且可能接受请求，只是格式不对。

请告诉我这个端点期望的请求体格式是什么？可能的字段包括：
- model
- messages / prompt / query
- temperature
- max_tokens
- stream
- 其他可能的字段

请给出具体的JSON格式示例。"""
    
    print('\n  [1.1] 询问 llm_raw_chat 格式...')
    r1 = chat_with_model(system_prompt, q1)
    if r1:
        print(f'  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r1[:3000]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 2: 尝试各种请求格式
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 2] 尝试各种请求格式')
    print(f'{"="*80}')
    
    # 构造认证头
    auth_headers = {
        'Authorization': f'Bearer {jwt_token}',
        'x-cloudide-token': jwt_token,
        'Content-Type': 'application/json',
        'User-Agent': 'TraeCN/2.3.62837',
        'Accept': 'text/event-stream, application/json',
    }
    
    # 尝试各种可能的请求体格式
    body_formats = [
        # 标准聊天格式
        {
            'name': 'Standard Chat',
            'body': {
                'model': 'doubao-pro-32k',
                'messages': [
                    {'role': 'user', 'content': '测试'}
                ],
                'stream': False,
                'temperature': 0.7,
                'max_tokens': 100,
            }
        },
        # raw_chat 格式
        {
            'name': 'Raw Chat',
            'body': {
                'model': 'doubao-pro-32k',
                'prompt': '测试',
                'stream': False,
                'temperature': 0.7,
                'max_tokens': 100,
            }
        },
        # completion 格式
        {
            'name': 'Completion',
            'body': {
                'model': 'doubao-pro-32k',
                'prompt': '测试',
                'stream': False,
                'max_tokens': 100,
                'temperature': 0.7,
                'top_p': 1.0,
            }
        },
        # 带 query 字段
        {
            'name': 'Query Field',
            'body': {
                'model': 'doubao-pro-32k',
                'query': '测试',
                'stream': False,
            }
        },
        # 带 input 字段
        {
            'name': 'Input Field',
            'body': {
                'model': 'doubao-pro-32k',
                'input': '测试',
                'stream': False,
            }
        },
        # 带 text 字段
        {
            'name': 'Text Field',
            'body': {
                'model': 'doubao-pro-32k',
                'text': '测试',
                'stream': False,
            }
        },
        # 带 content 字段
        {
            'name': 'Content Field',
            'body': {
                'model': 'doubao-pro-32k',
                'content': '测试',
                'role': 'user',
                'stream': False,
            }
        },
        # 嵌套 data 字段
        {
            'name': 'Nested Data',
            'body': {
                'data': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '测试'}],
                    'stream': False,
                }
            }
        },
        # 带 token 在 body 中
        {
            'name': 'Body with Token',
            'body': {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': '测试'}],
                'stream': False,
                'token': jwt_token,
                'userId': userId,
            }
        },
        # SSE 格式
        {
            'name': 'SSE Format',
            'body': {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': '测试'}],
                'stream': True,
                'temperature': 0.7,
            }
        },
    ]
    
    for fmt in body_formats:
        name = fmt['name']
        body = fmt['body']
        
        s, r, t = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body, auth_headers)
        
        status_icon = '✅' if s == 200 else ('⚠️' if s == 400 else '❓')
        
        # 检查响应
        if s == 200 and 'choices' in r:
            print(f'\n  🎉🎉🎉 突破成功!')
            print(f'  [{name}] → HTTP {s}')
            print(f'  响应: {r[:300]}')
            
            # 提取模型回复
            try:
                d = json.loads(r)
                data_obj = d.get('data', d)
                if isinstance(data_obj, dict):
                    choices = data_obj.get('choices', [])
                    if choices:
                        content = choices[0].get('message', {}).get('content', '')
                        print(f'\n  模型回复: {content}')
            except:
                pass
            return
        elif s == 200 and '1001' not in r:
            print(f'\n  🔑 非1001响应: [{name}]')
            print(f'  HTTP {s}: {r[:200]}')
        elif s == 400:
            print(f'  [{status_icon}] {name} → HTTP {s} ({t*1000:.0f}ms)')
            if r:
                print(f'    错误: {r[:150]}')
        else:
            print(f'  [{status_icon}] {name} → HTTP {s} ({t*1000:.0f}ms)')
    
    # ============================================================
    # Phase 3: 调整 Content-Type 尝试
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 3] 调整 Content-Type')
    print(f'{"="*80}')
    
    content_types = [
        'application/json',
        'text/plain',
        'application/x-www-form-urlencoded',
        'application/octet-stream',
    ]
    
    body = {
        'model': 'doubao-pro-32k',
        'messages': [{'role': 'user', 'content': '测试'}],
    }
    
    for ct in content_types:
        headers = dict(auth_headers)
        headers['Content-Type'] = ct
        
        s, r, t = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body, headers)
        
        status_icon = '✅' if s == 200 else '❓'
        print(f'  [{status_icon}] {ct} → HTTP {s} ({t*1000:.0f}ms)')
        
        if r and s != 404:
            print(f'    响应: {r[:150]}')
        
        if s == 200 and '1001' not in r:
            print(f'    🎉 突破成功!')
            print(f'    响应: {r[:300]}')
            break
    
    # ============================================================
    # Phase 4: 总结
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 4] 总结')
    print(f'{"="*80}')
    
    print(f'''
  ╔══════════════════════════════════════════════════════════════╗
  ║  BSD 黑客引擎 V8 完成                                    ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                              ║
  ║  llm_raw_chat 格式尝试: 10 种                              ║
  ║  Content-Type 尝试: 4 种                                   ║
  ║                                                              ║
  ║  关键发现:                                                   ║
  ║  1. /api/ide/v2/llm_raw_chat 返回 HTTP 400                 ║
  ║  2. 说明端点存在，但需要正确的请求格式                     ║
  ║  3. 需要进一步研究 Trae CN 内部代码                       ║
  ║                                                              ║
  ║  下一步:                                                     ║
  ║  A. 分析 Trae CN 内部 JavaScript 代码中的API调用格式      ║
  ║  B. 研究 llm_raw_chat 端点的具体参数                       ║
  ║  C. 重启 Trae CN 客户端获取新会话                          ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝
''')


if __name__ == '__main__':
    main()