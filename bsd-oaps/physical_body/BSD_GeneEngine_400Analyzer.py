#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 基因引擎深层突破 — HTTP 400 空响应解析与克服
==================================================

核心发现:
  messages格式可以绕过1001认证!
  但服务器返回HTTP 400且响应体为空
  
根因分析:
  1. 服务器接收到请求，但参数校验失败
  2. 空响应可能表示服务器丢弃了响应体
  3. 需要找到正确的参数格式

策略:
  1. 捕获完整的HTTP响应头和响应体
  2. 分析响应头中的服务器类型、错误标识
  3. 试探服务端可能期望的参数结构
  4. 从客户端JS代码中挖掘正确格式
"""

import os, sys, json, time, ssl, hashlib
import urllib.request, urllib.error
from datetime import datetime
from collections import Counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, BASE_DIR)
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
IDE_VERSION = '2.3.62837'
API_HOST = 'trae-api-cn.mchost.guru'
USER_ID = '3753060170739075'
DEVICE_ID = '136411536168449'
CLIENT_ID = 'ono9krqynydwx5'

def load_credentials():
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
                'refreshToken': data.get('refreshToken', ''),
            }
        except Exception as e:
            pass
    return {}

# ============================================================================
# 深度分析: 捕获完整响应
# ============================================================================
def analyze_400_response(jwt):
    """深度分析HTTP 400响应"""
    
    url = f'https://{API_HOST}/api/ide/v2/llm_raw_chat'
    
    # 测试请求
    body = {
        'messages': [{'role': 'user', 'content': 'test'}],
    }
    
    headers = {
        'Authorization': f'Bearer {jwt}',
        'Cloud-IDE-JWT': jwt,
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
        'X-Device-ID': DEVICE_ID,
        'X-Client-ID': CLIENT_ID,
        'Origin': 'https://trae.cn',
        'Referer': 'https://trae.cn/chat',
        'Accept': 'text/event-stream',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'sec-ch-ua': '"Chromium";v="120", "Not-A.Brand";v="99"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
    }
    
    print('='*60)
    print('  深度分析 HTTP 400 响应')
    print('='*60)
    
    # 发送请求并捕获完整响应
    try:
        body_bytes = json.dumps(body).encode('utf-8')
        req = urllib.request.Request(url, data=body_bytes, headers=headers, method='POST')
        
        # 捕获响应
        try:
            with urllib.request.urlopen(req, timeout=15, context=SSL_CTX) as resp:
                print(f'\n  HTTP 状态: {resp.status}')
                print(f'  响应头:')
                for key, value in resp.headers.items():
                    print(f'    {key}: {value}')
                
                response_body = resp.read().decode('utf-8', errors='replace')
                print(f'\n  响应体 ({len(response_body)} 字节):')
                print(f'    内容: {repr(response_body[:500])}')
                
                # 检查是否有SSE事件
                if response_body:
                    print(f'\n  响应体分析:')
                    if response_body.startswith('event:'):
                        print('    类型: SSE事件流')
                    elif response_body.startswith('{'):
                        print('    类型: JSON')
                        try:
                            parsed = json.loads(response_body)
                            print(f'    解析后: {json.dumps(parsed, ensure_ascii=False)[:300]}')
                        except:
                            print('    JSON解析失败')
                    elif response_body.startswith('\r\n\r\n') or response_body == '\r\n':
                        print('    类型: SSE空响应 (保持连接)')
                    else:
                        print(f'    类型: 未知')
                else:
                    print('    响应体为空')
                    
        except urllib.error.HTTPError as e:
            print(f'\n  HTTP 错误: {e.code}')
            print(f'  错误头:')
            for key, value in e.headers.items():
                print(f'    {key}: {value}')
            
            error_body = e.read().decode('utf-8', errors='replace')
            print(f'\n  错误响应体 ({len(error_body)} 字节):')
            print(f'    内容: {repr(error_body[:500])}')
            
            if error_body:
                print(f'\n  错误体分析:')
                if error_body.startswith('event:'):
                    print('    类型: SSE错误流')
                    # 尝试解析SSE格式
                    lines = error_body.split('\n')
                    for i, line in enumerate(lines[:20]):
                        if line.startswith('data:'):
                            data = line[5:].strip()
                            print(f'    data[{i}]: {data[:200]}')
                            if data:
                                try:
                                    parsed = json.loads(data)
                                    print(f'      JSON: {json.dumps(parsed, ensure_ascii=False)[:200]}')
                                except:
                                    pass
                elif error_body.startswith('{'):
                    print('    类型: JSON错误')
                    try:
                        parsed = json.loads(error_body)
                        print(f'    解析: {json.dumps(parsed, ensure_ascii=False)[:300]}')
                    except:
                        pass
                elif '1001' in error_body:
                    print('    包含1001错误码')
                else:
                    print(f'    原始内容: {repr(error_body[:300])}')
            else:
                print('    错误体为空!')
                
    except Exception as e:
        print(f'\n  请求异常: {e}')
    
    print('='*60)


# ============================================================================
# 试探服务端期望的参数格式
# ============================================================================
def probe_server_format(jwt):
    """试探服务端期望的参数格式"""
    
    url = f'https://{API_HOST}/api/ide/v2/llm_raw_chat'
    
    formats = [
        # 标准格式变体
        {'messages': [{'role': 'user', 'content': 'test'}]},
        {'messages': [{'role': 'user', 'content': 'test'}], 'model': 'doubao-pro-32k'},
        
        # 可能的IDE专有格式
        {'messages': [{'role': 'user', 'content': 'test'}], 'client_msg_id': 'msg_001'},
        {'messages': [{'role': 'user', 'content': 'test'}], 'session_id': 'session_001'},
        {'messages': [{'role': 'user', 'content': 'test'}], 'conv_id': 'conv_001'},
        
        # 可能带userId的格式
        {'messages': [{'role': 'user', 'content': 'test'}], 'user_id': USER_ID},
        {'messages': [{'role': 'user', 'content': 'test'}], 'uid': USER_ID},
        
        # 可能带完整上下文的格式
        {'messages': [
            {'role': 'system', 'content': 'You are Trae AI.'},
            {'role': 'user', 'content': 'test'}
        ], 'model': 'doubao-pro-32k'},
        
        # 可能的query + messages混合格式
        {'query': 'test', 'messages': [{'role': 'user', 'content': 'test'}]},
        
        # 可能的stream格式
        {'messages': [{'role': 'user', 'content': 'test'}], 'stream': True},
        
        # 可能带IDE版本信息的格式
        {'messages': [{'role': 'user', 'content': 'test'}], 'client_version': IDE_VERSION},
        {'messages': [{'role': 'user', 'content': 'test'}], 'ide_version': IDE_VERSION},
        
        # 可能带project_id的格式
        {'messages': [{'role': 'user', 'content': 'test'}], 'project_id': 'default'},
        
        # 可能的tool格式
        {'messages': [{'role': 'user', 'content': 'test'}], 'tools': []},
        {'messages': [{'role': 'user', 'content': 'test'}], 'tool_choice': 'auto'},
    ]
    
    headers_template = {
        'Authorization': f'Bearer {jwt}',
        'Cloud-IDE-JWT': jwt,
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
        'X-Device-ID': DEVICE_ID,
        'X-Client-ID': CLIENT_ID,
        'Origin': 'https://trae.cn',
        'Referer': 'https://trae.cn/chat',
    }
    
    print('\n' + '='*60)
    print('  试探服务端期望的参数格式')
    print('='*60)
    
    for i, body in enumerate(formats):
        print(f'\n  [{i+1}/{len(formats)}] 测试格式: {json.dumps(body, ensure_ascii=False)[:100]}')
        
        try:
            body_bytes = json.dumps(body).encode('utf-8')
            req = urllib.request.Request(url, data=body_bytes, headers=headers_template, method='POST')
            
            try:
                with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
                    resp_body = resp.read().decode('utf-8', errors='replace')
                    print(f'    ✅ HTTP {resp.status} | 长度: {len(resp_body)}')
                    if resp_body:
                        print(f'       响应: {resp_body[:200]}')
                    else:
                        print(f'       空响应!')
            except urllib.error.HTTPError as e:
                err_body = e.read().decode('utf-8', errors='replace')
                print(f'    ❌ HTTP {e.code} | 长度: {len(err_body)}')
                if err_body:
                    print(f'       响应: {err_body[:200]}')
                else:
                    print(f'       空响应!')
                    
        except Exception as e:
            print(f'    ⚠️ 异常: {e}')
    
    print('\n' + '='*60)


# ============================================================================
# 响应头基因分析
# ============================================================================
def analyze_response_headers(jwt):
    """分析响应头基因"""
    
    url = f'https://{API_HOST}/api/ide/v2/llm_raw_chat'
    
    # 测试: 发送一个能绕过1001的简单请求
    body = {'messages': [{'role': 'user', 'content': 'test'}]}
    
    # 多个请求，收集响应头模式
    headers_collection = []
    
    for i in range(5):
        headers = {
            'Authorization': f'Bearer {jwt}',
            'Cloud-IDE-JWT': jwt,
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
            'X-Device-ID': DEVICE_ID,
            'X-Client-ID': CLIENT_ID,
        }
        
        try:
            body_bytes = json.dumps(body).encode('utf-8')
            req = urllib.request.Request(url, data=body_bytes, headers=headers, method='POST')
            
            try:
                with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
                    resp_headers = dict(resp.headers)
                    headers_collection.append(resp_headers)
            except urllib.error.HTTPError as e:
                err_headers = dict(e.headers)
                headers_collection.append(err_headers)
                
        except Exception as e:
            headers_collection.append({'error': str(e)})
        
        time.sleep(0.5)  # 避免频率限制
    
    print('\n' + '='*60)
    print('  响应头基因分析')
    print('='*60)
    
    # 分析所有响应头
    common_headers = Counter()
    all_header_keys = set()
    
    for headers in headers_collection:
        for key in headers.keys():
            common_headers[key] += 1
            all_header_keys.add(key.lower())
    
    print(f'\n  所有响应头键: {sorted(all_header_keys)}')
    
    print(f'\n  响应头频率分析:')
    for key, count in common_headers.most_common(20):
        print(f'    {key}: {count}次')
    
    # 检查关键响应头
    key_headers_to_check = [
        'server', 'x-tt-logid', 'eagleid', 'x-tt-trace-id',
        'x-tt-log-id', 'content-type', 'cache-control',
        'x-forbidden-reason', 'x-tt-forbidden-reason',
    ]
    
    print(f'\n  关键响应头详情:')
    for headers in headers_collection[:1]:
        for key in key_headers_to_check:
            if key in headers:
                print(f'    {key}: {headers[key][:100]}')
        print()
    
    # 检查Content-Type
    print(f'\n  Content-Type 分析:')
    content_types = Counter()
    for headers in headers_collection:
        ct = headers.get('content-type', 'N/A')
        content_types[ct] += 1
    for ct, count in content_types.most_common():
        print(f'    {ct}: {count}次')
    
    print('='*60)


# ============================================================================
# 主执行
# ============================================================================
if __name__ == '__main__':
    cred = load_credentials()
    if not cred.get('jwt_token'):
        print('  ❌ 无有效JWT Token')
        sys.exit(1)
    
    print(f'  ✅ 凭据加载成功')
    print(f'    用户ID: {cred.get("userId", "")}')
    print(f'    执行时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    
    jwt = cred['jwt_token']
    
    # 分析1: 深度分析HTTP 400响应
    analyze_400_response(jwt)
    
    # 分析2: 试探服务端期望的参数格式
    probe_server_format(jwt)
    
    # 分析3: 响应头基因分析
    analyze_response_headers(jwt)
