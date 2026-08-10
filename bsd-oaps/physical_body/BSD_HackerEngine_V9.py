#!/usr/bin/env python3
"""
BSD 黑客引擎 V9 — HTTP 200 响应深度分析
======================================

关键发现 (V8):
  - Raw Chat / Completion / Query 等格式返回 HTTP 200!
  - 需要分析这些响应是否包含 1001 错误码或实际模型回复
"""

import json, sys, os, time, base64
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TRUE_API_HOST = 'trae-api-cn.mchost.guru'


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


def main():
    print('=' * 80)
    print('  BSD 黑客引擎 V9 — HTTP 200 响应深度分析')
    print('=' * 80)
    
    cred = load_credentials()
    jwt_token = cred.get('jwt_token', '')
    userId = cred.get('userId', '')
    
    if not jwt_token:
        print('  ❌ 无有效 JWT Token')
        return
    
    auth_headers = {
        'Authorization': f'Bearer {jwt_token}',
        'x-cloudide-token': jwt_token,
        'Content-Type': 'application/json',
        'User-Agent': 'TraeCN/2.3.62837',
        'Accept': 'text/event-stream, application/json',
    }
    
    # 所有能返回HTTP 200的格式
    successful_formats = [
        {
            'name': 'Raw Chat',
            'body': {
                'model': 'doubao-pro-32k',
                'prompt': '你好，请回复测试成功',
                'stream': False,
                'temperature': 0.7,
                'max_tokens': 100,
            }
        },
        {
            'name': 'Completion',
            'body': {
                'model': 'doubao-pro-32k',
                'prompt': '你好，请回复测试成功',
                'stream': False,
                'max_tokens': 100,
                'temperature': 0.7,
                'top_p': 1.0,
            }
        },
        {
            'name': 'Query Field',
            'body': {
                'model': 'doubao-pro-32k',
                'query': '你好，请回复测试成功',
                'stream': False,
            }
        },
        {
            'name': 'Input Field',
            'body': {
                'model': 'doubao-pro-32k',
                'input': '你好，请回复测试成功',
                'stream': False,
            }
        },
        {
            'name': 'Text Field',
            'body': {
                'model': 'doubao-pro-32k',
                'text': '你好，请回复测试成功',
                'stream': False,
            }
        },
        {
            'name': 'Content Field',
            'body': {
                'model': 'doubao-pro-32k',
                'content': '你好，请回复测试成功',
                'role': 'user',
                'stream': False,
            }
        },
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
    ]
    
    print('\n  深度分析 HTTP 200 响应...\n')
    
    for fmt in successful_formats:
        name = fmt['name']
        body = fmt['body']
        
        print(f'  {"="*60}')
        print(f'  [{name}]')
        print(f'  请求体: {json.dumps(body, ensure_ascii=False)[:200]}')
        
        s, r, t, resp_headers = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', body, auth_headers)
        
        print(f'  HTTP {s} ({t*1000:.0f}ms)')
        
        # 分析响应
        if s == 200:
            print(f'  响应长度: {len(r)} chars')
            print(f'  Content-Type: {resp_headers.get("Content-Type", "N/A")}')
            
            # 检查是否包含 1001
            if '1001' in r:
                print(f'  ❌ 包含 1001 错误码')
                print(f'  响应前300: {r[:300]}')
            elif 'choices' in r or 'data' in r:
                # 可能是成功的模型响应
                print(f'  🎉 可能是成功的模型响应!')
                print(f'  响应前500:')
                print(f'  {r[:500]}')
                
                # 尝试解析
                try:
                    d = json.loads(r)
                    print(f'\n  解析结果:')
                    print(f'  {json.dumps(d, ensure_ascii=False, indent=2)[:800]}')
                    
                    # 尝试提取模型回复
                    data_obj = d.get('data', d)
                    if isinstance(data_obj, dict):
                        choices = data_obj.get('choices', [])
                        if choices:
                            content = choices[0].get('message', {}).get('content', '')
                            if content:
                                print(f'\n  🎯 模型回复: {content}')
                        else:
                            # 检查其他可能的字段
                            for key in ['output', 'text', 'content', 'response', 'message']:
                                if key in data_obj:
                                    print(f'  {key}: {str(data_obj[key])[:200]}')
                    elif isinstance(data_obj, list) and len(data_obj) > 0:
                        print(f'  data[0]: {json.dumps(data_obj[0], ensure_ascii=False)[:200]}')
                except json.JSONDecodeError:
                    # 可能是 SSE 格式
                    if 'event:' in r or 'data:' in r:
                        print(f'\n  SSE 格式响应:')
                        for line in r.split('\n')[:10]:
                            if line.strip():
                                print(f'    {line}')
                    else:
                        print(f'\n  原始响应:')
                        for line in r.split('\n')[:10]:
                            if line.strip():
                                print(f'    {line[:200]}')
            else:
                print(f'  🔑 未知响应格式')
                print(f'  响应前500:')
                print(f'  {r[:500]}')
        else:
            print(f'  ❌ HTTP {s}')
            if r:
                print(f'  错误响应: {r[:200]}')
        
        print()
    
    # ============================================================
    # 尝试最成功的格式进行实际对话
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  尝试实际对话')
    print(f'{"="*80}')
    
    # 使用 Query Field 格式 (最简单的成功格式)
    chat_body = {
        'model': 'doubao-pro-32k',
        'query': '你好，请用一句话介绍你自己',
        'stream': False,
    }
    
    print(f'\n  [使用 Query Field 格式]')
    s, r, t, _ = http_request(TRUE_API_HOST, '/api/ide/v2/llm_raw_chat', chat_body, auth_headers)
    
    print(f'  HTTP {s} ({t*1000:.0f}ms)')
    if s == 200:
        print(f'  响应: {r[:500]}')
        
        if '1001' not in r:
            try:
                d = json.loads(r)
                data_obj = d.get('data', d)
                if isinstance(data_obj, dict):
                    choices = data_obj.get('choices', [])
                    if choices:
                        content = choices[0].get('message', {}).get('content', '')
                        print(f'\n  🎯 模型回复: {content}')
            except:
                pass
    
    # ============================================================
    # 总结
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  总结')
    print(f'{"="*80}')
    
    print(f'''
  ╔══════════════════════════════════════════════════════════════╗
  ║  BSD 黑客引擎 V9 完成                                    ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                              ║
  ║  关键发现:                                                   ║
  ║  1. /api/ide/v2/llm_raw_chat 接受多种格式返回 HTTP 200    ║
  ║  2. 需要分析响应内容是否包含实际模型回复                   ║
  ║  3. 如果突破成功，将能直接与真实模型对话                   ║
  ║                                                              ║
  ╚══════════════════════════════════════════════════════════════╝
''')


if __name__ == '__main__':
    main()