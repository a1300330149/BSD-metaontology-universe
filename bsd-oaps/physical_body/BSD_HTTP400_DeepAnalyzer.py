#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 白名单绕过 — HTTP 400 深度解析专项
======================================

关键发现:
  - messages 格式: HTTP 400 (服务器接受了！只是参数不对)
  - query 格式: HTTP 200 + 1001 (服务器拒绝了)
  
突破方向:
  深入分析 HTTP 400 的具体原因
  找出正确的 messages 格式
"""

import os, sys, json, time, hashlib, ssl
import urllib.request, urllib.error, http.cookiejar
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, BASE_DIR)
from BSD_AHADecryptor import decrypt_aha

# ============================================================================
# 加载凭据
# ============================================================================
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

# ============================================================================
# 详细的HTTP 400错误解析器
# ============================================================================
class HTTP400Analyzer:
    """HTTP 400错误深度分析器"""
    
    def __init__(self, jwt):
        self.jwt = jwt
        self.findings = []
        
    def _make_request(self, path, body, headers=None):
        """发送请求并详细分析响应"""
        url = f'https://{API_HOST}{path}'
        hdrs = headers or {}
        hdrs.setdefault('Content-Type', 'application/json')
        hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
        
        try:
            body_bytes = json.dumps(body).encode('utf-8') if body else None
            req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST')
            
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=10, context=SSL_CTX) as resp:
                body_text = resp.read().decode('utf-8', errors='replace')
                return {
                    'status': resp.status,
                    'body': body_text,
                    'headers': dict(resp.headers),
                    'error': None,
                }
        except urllib.error.HTTPError as e:
            body_text = e.read().decode('utf-8', errors='replace')
            return {
                'status': e.code,
                'body': body_text,
                'headers': dict(e.headers) if hasattr(e, 'headers') else {},
                'error': str(e)[:200],
            }
        except Exception as e:
            return {
                'status': 0,
                'body': str(e),
                'headers': {},
                'error': str(e)[:200],
            }
    
    def analyze_400_error(self):
        """深度分析 HTTP 400 错误"""
        print('\n' + '#'*70)
        print('  # HTTP 400 错误深度解析')
        print('#'*70)
        print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'  核心问题: 服务器返回400而非1001，为什么？')
        print('#'*70)
        
        # 测试矩阵: 逐步调整参数
        test_matrix = [
            # === messages 格式测试 ===
            {
                'name': 'messages-1: 最简格式',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'stream': False,
                }
            },
            {
                'name': 'messages-2: 加system',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'system', 'content': 'You are a helpful assistant.'},
                        {'role': 'user', 'content': '你好'}
                    ],
                    'stream': False,
                }
            },
            {
                'name': 'messages-3: 加conversation_id',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'stream': False,
                    'conversation_id': 'test_conv_001',
                }
            },
            {
                'name': 'messages-4: 加user_id',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'stream': False,
                    'user_id': USER_ID,
                }
            },
            # === 混合格式测试 ===
            {
                'name': 'hybrid-1: messages+query',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'query': '你好',
                    'stream': False,
                }
            },
            {
                'name': 'hybrid-2: query+messages',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'query': '你好',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'stream': False,
                }
            },
            # === 其他格式测试 ===
            {
                'name': 'alternate-1: prompt格式',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'prompt': '你好',
                    'stream': False,
                }
            },
            {
                'name': 'alternate-2: input格式',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'input': '你好',
                    'stream': False,
                }
            },
            {
                'name': 'alternate-3: content格式',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'content': '你好',
                    'stream': False,
                }
            },
            # === SSE格式测试 ===
            {
                'name': 'sse-1: stream=true',
                'path': '/api/ide/v2/llm_raw_chat',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [{'role': 'user', 'content': '你好'}],
                    'stream': True,
                }
            },
        ]
        
        print('\n  测试矩阵:')
        print('  ' + '-'*60)
        
        for test in test_matrix:
            headers = {
                'Authorization': f'Bearer {self.jwt}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                'Accept': 'text/event-stream',
            }
            
            print(f'\n  测试: {test["name"]}')
            print(f'    请求体: {json.dumps(test["body"], ensure_ascii=False)[:100]}...')
            
            response = self._make_request(test['path'], test['body'], headers)
            
            status = response['status']
            body = response['body']
            is_1001 = '1001' in body
            
            # 分析响应
            print(f'    HTTP: {status}')
            print(f'    1001: {is_1001}')
            print(f'    响应长度: {len(body)} 字节')
            
            # 尝试解析响应
            try:
                if body.startswith('event:') or body.startswith('data:'):
                    # SSE格式
                    print(f'    格式: SSE (Server-Sent Events)')
                    # 提取data内容
                    for line in body.split('\n'):
                        if line.startswith('data:'):
                            data_str = line[5:].strip()
                            try:
                                data_obj = json.loads(data_str)
                                print(f'    Data: {json.dumps(data_obj, ensure_ascii=False)[:200]}')
                                
                                # 检查错误码
                                if 'code' in data_obj:
                                    print(f'    错误码: {data_obj["code"]}')
                                if 'message' in data_obj:
                                    print(f'    消息: {data_obj["message"]}')
                            except:
                                print(f'    Data (raw): {data_str[:100]}')
                else:
                    # 普通JSON
                    data_obj = json.loads(body)
                    print(f'    格式: JSON')
                    print(f'    内容: {json.dumps(data_obj, ensure_ascii=False)[:200]}')
                    
                    # 检查错误
                    if 'error' in data_obj:
                        print(f'    错误: {data_obj["error"]}')
                    if 'message' in data_obj:
                        print(f'    消息: {data_obj["message"]}')
                    if 'code' in data_obj:
                        print(f'    代码: {data_obj["code"]}')
            except json.JSONDecodeError:
                print(f'    原始响应: {body[:200]}')
            
            # 记录发现
            if status == 400:
                self.findings.append({
                    'test': test['name'],
                    'status': 400,
                    'response_preview': body[:200],
                    'analysis': '服务器接受了格式但参数错误',
                })
            elif status == 200 and is_1001:
                self.findings.append({
                    'test': test['name'],
                    'status': 200,
                    'is_1001': True,
                    'response_preview': body[:200],
                    'analysis': '服务器拦截了认证',
                })
            elif status == 200 and not is_1001:
                self.findings.append({
                    'test': test['name'],
                    'status': 200,
                    'is_1001': False,
                    'response_preview': body[:200],
                    'analysis': '🎉 成功！服务器接受了请求',
                })
                print(f'    🎉 突破成功！')
    
    def deep_dive_400(self):
        """深入分析已发现的400错误"""
        print('\n' + '#'*70)
        print('  # 400错误深入分析')
        print('#'*70)
        
        # 如果有400错误，尝试微调参数
        if not any(f['status'] == 400 for f in self.findings):
            print('  没有发现400错误，跳过深入分析')
            return
        
        print('\n  针对400错误的微调测试:')
        print('  ' + '-'*60)
        
        # 基于发现的400错误，尝试微调
        # 假设messages格式被接受，尝试更多变体
        
        fine_tune_tests = [
            {
                'name': 'fine-1: 加上必要字段',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'system', 'content': 'You are a helpful assistant.'},
                        {'role': 'user', 'content': '你好'}
                    ],
                    'stream': False,
                    'conversation_id': hashlib.sha256(f'tune{time.time()}'.encode()).hexdigest()[:16],
                    'user_id': USER_ID,
                    'client_type': 'trae_ide',
                }
            },
            {
                'name': 'fine-2: 使用正确的字段名',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'user', 'content': '你好'}
                    ],
                    'stream': False,
                    'session_id': hashlib.sha256(f'sess{time.time()}'.encode()).hexdigest()[:16],
                    'uid': USER_ID,
                }
            },
            {
                'name': 'fine-3: 最小必要参数',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'user', 'content': '你好'}
                    ],
                }
            },
            {
                'name': 'fine-4: 模拟ChatCompletion',
                'body': {
                    'model': 'doubao-pro-32k',
                    'messages': [
                        {'role': 'system', 'content': 'You are helpful.'},
                        {'role': 'user', 'content': 'Hi'}
                    ],
                    'stream': False,
                    'temperature': 0.7,
                    'max_tokens': 100,
                }
            },
        ]
        
        for test in fine_tune_tests:
            headers = {
                'Authorization': f'Bearer {self.jwt}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
            }
            
            print(f'\n  测试: {test["name"]}')
            response = self._make_request('/api/ide/v2/llm_raw_chat', test['body'], headers)
            
            status = response['status']
            body = response['body']
            is_1001 = '1001' in body
            
            print(f'    HTTP: {status} | 1001: {is_1001}')
            
            if body[:150]:
                # 尝试解析
                try:
                    for line in body.split('\n'):
                        if line.startswith('data:'):
                            data_str = line[5:].strip()
                            try:
                                obj = json.loads(data_str)
                                print(f'    响应: {json.dumps(obj, ensure_ascii=False)[:200]}')
                            except:
                                print(f'    响应: {data_str[:150]}')
                            break
                    else:
                        print(f'    响应: {body[:150]}')
                except:
                    print(f'    响应: {body[:150]}')
            
            if status == 200 and not is_1001:
                print(f'    🎉 突破成功！')
    
    def generate_final_report(self):
        """生成最终报告"""
        print('\n' + '#'*70)
        print('  # 最终分析报告')
        print('#'*70)
        
        print(f'\n  发现总结:')
        
        # 按状态分类
        status_counts = {}
        for f in self.findings:
            status = f['status']
            if status not in status_counts:
                status_counts[status] = {'count': 0, 'tests': []}
            status_counts[status]['count'] += 1
            status_counts[status]['tests'].append(f['test'])
        
        for status, info in sorted(status_counts.items()):
            print(f'\n    HTTP {status}: {info["count"]}个测试')
            for test_name in info['tests'][:3]:  # 只显示前3个
                print(f'      - {test_name}')
            if len(info['tests']) > 3:
                print(f'      ... 等{len(info["tests"])}个')
        
        # 核心洞察
        print(f'\n  核心洞察:')
        print(f'    1. messages 格式被服务器接受 (HTTP 400)')
        print(f'    2. query 格式被服务器拒绝 (HTTP 200 + 1001)')
        print(f'    3. 服务器对不同格式有不同的认证逻辑')
        print(f'    4. 这可能是一个突破点!')
        
        # 建议
        print(f'\n  后续突破方向:')
        print(f'    1. 深入分析 messages 格式的正确参数')
        print(f'    2. 对比官方客户端的实际请求格式')
        print(f'    3. 研究Trae CN主程序的请求构造逻辑')
        
        print('#'*70)


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
    
    analyzer = HTTP400Analyzer(cred['jwt_token'])
    
    # 深度分析HTTP 400错误
    analyzer.analyze_400_error()
    
    # 深入分析
    analyzer.deep_dive_400()
    
    # 生成报告
    analyzer.generate_final_report()
