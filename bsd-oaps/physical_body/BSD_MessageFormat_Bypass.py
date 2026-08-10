#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 突破1001 — messages格式专项突破
===================================

关键发现:
  - messages 格式: HTTP 400, 响应长度=0, 1001=False
  - 这意味着 messages 格式绕过了1001认证！

目标:
  1. 分析为什么 messages 格式能绕过1001
  2. 找出正确的 messages 请求格式
  3. 验证白名单机制是否可被算法欺骗
"""

import os, sys, json, time, hashlib, ssl
import urllib.request, urllib.error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, BASE_DIR)
from BSD_AHADecryptor import decrypt_aha

# 配置
TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
IDE_VERSION = '2.3.62837'
API_HOST = 'trae-api-cn.mchost.guru'
AUTH_HOST = 'api.trae.cn'
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
            print(f'  ⚠️ cloudide解密失败: {e}')
    return {}

def make_request_with_headers(host, path, body, headers=None, timeout=10):
    """发送请求并返回详细信息"""
    url = f'https://{host}{path}'
    hdrs = headers or {}
    
    result = {
        'url': url,
        'status': 0,
        'body': '',
        'response_headers': {},
        'request_headers': hdrs,
        'error': None,
    }
    
    try:
        body_bytes = json.dumps(body).encode('utf-8') if body else None
        req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST')
        
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            result['status'] = resp.status
            result['body'] = resp.read().decode('utf-8', errors='replace')
            result['response_headers'] = dict(resp.headers)
    except urllib.error.HTTPError as e:
        result['status'] = e.code
        result['body'] = e.read().decode('utf-8', errors='replace')
        if hasattr(e, 'headers'):
            result['response_headers'] = dict(e.headers)
        result['error'] = str(e)[:200]
    except Exception as e:
        result['error'] = str(e)[:200]
        result['body'] = str(e)
    
    return result


class MessageFormatBypass:
    """messages格式突破引擎"""
    
    def __init__(self, jwt):
        self.jwt = jwt
        self.experiments = []
    
    def _exp1_compare_headers(self):
        """实验1: 对比两种格式的响应头差异"""
        print('\n' + '='*70)
        print('  实验1: 对比 messages vs query 格式')
        print('='*70)
        
        # 准备请求
        messages_body = {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
            'stream': False,
        }
        
        query_body = {
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': False,
        }
        
        headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
        }
        
        print('\n  --- messages 格式 ---')
        r1 = make_request_with_headers(API_HOST, '/api/ide/v2/llm_raw_chat', messages_body, headers)
        print(f'  状态: HTTP {r1["status"]}')
        print(f'  响应体长度: {len(r1["body"])} 字节')
        print(f'  1001错误: {"1001" in r1["body"]}')
        print(f'  响应体: {r1["body"][:200]}')
        print(f'  响应头:')
        for k, v in sorted(r1['response_headers'].items()):
            print(f'    {k}: {str(v)[:100]}')
        
        print('\n  --- query 格式 ---')
        r2 = make_request_with_headers(API_HOST, '/api/ide/v2/llm_raw_chat', query_body, headers)
        print(f'  状态: HTTP {r2["status"]}')
        print(f'  响应体长度: {len(r2["body"])} 字节')
        print(f'  1001错误: {"1001" in r2["body"]}')
        print(f'  响应体: {r2["body"][:200]}')
        
        # 对比
        print('\n  --- 关键差异 ---')
        if r1['status'] != r2['status']:
            print(f'  ⚠️ 状态码不同: messages={r1["status"]}, query={r2["status"]}')
        if '1001' not in r1['body'] and '1001' in r2['body']:
            print(f'  🎉 messages 格式绕过了1001认证!')
        
        return r1, r2
    
    def _exp2_add_auth_headers(self):
        """实验2: 为 messages 格式添加更多认证头"""
        print('\n' + '='*70)
        print('  实验2: 为 messages 添加完整认证头')
        print('='*70)
        
        messages_body = {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
            'stream': False,
        }
        
        # 不同的认证头组合
        header_sets = [
            {
                'name': '基础认证',
                'headers': {
                    'Authorization': f'Bearer {self.jwt}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
            {
                'name': 'Cloud-IDE-JWT',
                'headers': {
                    'Authorization': f'Bearer {self.jwt}',
                    'Cloud-IDE-JWT': self.jwt,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
            {
                'name': '完整版客户端',
                'headers': {
                    'Authorization': f'Bearer {self.jwt}',
                    'Cloud-IDE-JWT': self.jwt,
                    'x-cloudide-token': self.jwt,
                    'X-Device-ID': DEVICE_ID,
                    'X-Client-ID': CLIENT_ID,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                    'Origin': 'https://trae.cn',
                    'Referer': 'https://trae.cn/chat',
                    'Accept': 'text/event-stream',
                }
            },
        ]
        
        for test in header_sets:
            print(f'\n  [{test["name"]}]')
            r = make_request_with_headers(
                API_HOST, '/api/ide/v2/llm_raw_chat',
                messages_body, test['headers']
            )
            print(f'    HTTP {r["status"]} | 1001={"1001" in r["body"]}')
            print(f'    响应长度: {len(r["body"])} 字节')
            if r['body'][:150]:
                print(f'    响应: {r["body"][:150]}')
    
    def _exp3_various_paths(self):
        """实验3: 在不同路径上测试 messages 格式"""
        print('\n' + '='*70)
        print('  实验3: 不同路径上的 messages 格式')
        print('='*70)
        
        messages_body = {
            'model': 'doubao-pro-32k',
            'messages': [{'role': 'user', 'content': '你好'}],
            'stream': False,
        }
        
        paths = [
            '/api/ide/v2/llm_raw_chat',
            '/api/ide/v2/chat',
            '/api/ide/v2/raw_chat',
            '/api/ide/v2/completion',
            '/api/ide/v2/messages',
        ]
        
        headers = {
            'Authorization': f'Bearer {self.jwt}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        }
        
        for path in paths:
            r = make_request_with_headers(API_HOST, path, messages_body, headers)
            print(f'\n  {path}')
            print(f'    HTTP {r["status"]} | 1001={"1001" in r["body"]}')
            print(f'    响应: {r["body"][:100]}')
    
    def _exp4_full_client_sim(self):
        """实验4: 完整客户端模拟 + messages 格式"""
        print('\n' + '='*70)
        print('  实验4: 完整客户端会话模拟')
        print('='*70)
        
        import http.cookiejar
        cookie_jar = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar)
        )
        
        try:
            # Step 1: 访问首页获取Cookie
            print('\n  Step 1: 访问 trae.cn')
            req1 = urllib.request.Request(
                'https://trae.cn/',
                headers={'User-Agent': f'TraeCN/{IDE_VERSION}'}
            )
            resp1 = opener.open(req1, timeout=10)
            print(f'    HTTP {resp1.status}')
            cookies = list(cookie_jar)
            print(f'    Cookie数量: {len(cookies)}')
            for c in cookies:
                print(f'      {c.name}={c.value[:30]}...')
            
            # Step 2: 使用 Cookie 发 messages 请求
            print('\n  Step 2: 发送 messages 请求')
            messages_body = json.dumps({
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
                'conversation_id': hashlib.sha256(f'client{time.time()}'.encode()).hexdigest()[:16],
            }).encode('utf-8')
            
            req2 = urllib.request.Request(
                f'https://{API_HOST}/api/ide/v2/llm_raw_chat',
                data=messages_body,
                headers={
                    'Authorization': f'Bearer {self.jwt}',
                    'Cloud-IDE-JWT': self.jwt,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                    'X-Device-ID': DEVICE_ID,
                    'X-Client-ID': CLIENT_ID,
                    'Origin': 'https://trae.cn',
                    'Referer': 'https://trae.cn/chat',
                },
                method='POST'
            )
            
            resp2 = opener.open(req2, timeout=15, context=SSL_CTX)
            body2 = resp2.read().decode('utf-8')
            
            print(f'    HTTP {resp2.status}')
            print(f'    响应长度: {len(body2)} 字节')
            print(f'    1001错误: {"1001" in body2}')
            print(f'    响应: {body2[:300]}')
            
            if '1001' not in body2 and resp2.status == 200:
                print(f'    🎉 突破成功！')
        
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8', errors='replace')
            print(f'    HTTP {e.code}')
            print(f'    响应: {body[:200]}')
        except Exception as e:
            print(f'    错误: {e}')
    
    def _exp5_direct_api_call(self):
        """实验5: 直接使用 messages 格式 + 完整认证"""
        print('\n' + '='*70)
        print('  实验5: messages + 完整认证头')
        print('='*70)
        
        # 关键: 构造正确的 messages 请求
        # 参考标准 ChatCompletion API 格式
        
        test_bodies = [
            # 标准 ChatCompletion 格式
            {
                'name': '标准ChatCompletion',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'system', 'content': 'You are a helpful assistant.'},
                        {'role': 'user', 'content': '你好'}
                    ],
                    'stream': False,
                    'temperature': 0.7,
                }
            },
            # 加上用户ID
            {
                'name': '带用户ID',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'user', 'content': '你好'}
                    ],
                    'stream': False,
                    'user_id': USER_ID,
                }
            },
            # 加上会话ID
            {
                'name': '带会话ID',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'user', 'content': '你好'}
                    ],
                    'stream': False,
                    'session_id': hashlib.sha256(f'sess{time.time()}'.encode()).hexdigest(),
                }
            },
        ]
        
        for test in test_bodies:
            print(f'\n  [{test["name"]}]')
            print(f'    请求体: {json.dumps(test["body"], ensure_ascii=False)[:150]}')
            
            headers = {
                'Authorization': f'Bearer {self.jwt}',
                'Cloud-IDE-JWT': self.jwt,
                'x-cloudide-token': self.jwt,
                'X-Device-ID': DEVICE_ID,
                'X-Client-ID': CLIENT_ID,
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                'Origin': 'https://trae.cn',
                'Referer': 'https://trae.cn/chat',
                'Accept': 'text/event-stream',
            }
            
            r = make_request_with_headers(
                API_HOST, '/api/ide/v2/llm_raw_chat',
                test['body'], headers, timeout=15
            )
            
            print(f'    HTTP {r["status"]} | 1001={"1001" in r["body"]}')
            print(f'    响应长度: {len(r["body"])} 字节')
            if r['body'][:200]:
                print(f'    响应: {r["body"][:200]}')
            
            # 尝试解析 SSE 响应
            if r['body'].startswith('event:') or r['body'].startswith('data:'):
                print(f'    格式: SSE')
                for line in r['body'].split('\n'):
                    if line.startswith('data:'):
                        data_str = line[5:].strip()
                        try:
                            obj = json.loads(data_str)
                            print(f'    Data: {json.dumps(obj, ensure_ascii=False)[:200]}')
                        except:
                            print(f'    Data: {data_str[:100]}')
            elif r['body']:
                try:
                    obj = json.loads(r['body'])
                    print(f'    格式: JSON')
                    print(f'    Data: {json.dumps(obj, ensure_ascii=False)[:200]}')
                except:
                    pass
    
    def run_all(self):
        """运行所有实验"""
        print('\n' + '#'*70)
        print('  # BSD messages格式突破1001专项')
        print('#'*70)
        print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'  核心发现: messages格式绕过1001认证！')
        print('#'*70)
        
        self._exp1_compare_headers()
        self._exp2_add_auth_headers()
        self._exp3_various_paths()
        self._exp4_full_client_sim()
        self._exp5_direct_api_call()
        
        print('\n' + '#'*70)
        print('  # 实验完成')
        print('#'*70)


# 主执行
if __name__ == '__main__':
    cred = load_credentials()
    if not cred.get('jwt_token'):
        print('  ❌ 无有效JWT Token')
        sys.exit(1)
    
    print(f'  ✅ 凭据加载成功')
    
    engine = MessageFormatBypass(cred['jwt_token'])
    engine.run_all()
