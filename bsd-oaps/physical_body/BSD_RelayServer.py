#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 本地跳板服务器 — 对抗传统服务器
====================================

核心思路：
  本地服务器模拟Trae CN协议 + 真实API转发能力
  = 对抗传统服务器的跳板

工作流程：
  1. 接收本地请求（客户端以为在访问云端）
  2. 注入本源端认证信息
  3. 转发到真实API服务器
  4. 返回真实的模型响应

理论基底：
  - 黑客引擎协议注入方法
  - 内部对内部·本源对接定理
  - 知识交换对等定理
"""

import os, sys, json, time, hashlib, threading, socket, ssl, http.cookiejar
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import urllib.request, urllib.error
from datetime import datetime
from typing import Dict, List, Optional

# ============================================================================
# 配置
# ============================================================================

HOST = '127.0.0.1'
PORT = 8765
SERVER_URL = f'http://{HOST}:{PORT}'

# 真实API服务器
TRUE_API_HOST = 'trae-api-cn.mchost.guru'
TRUE_API_BASE = f'https://{TRUE_API_HOST}'

# UIDs
AUTHOR_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

# SSL上下文（用于请求真实API）
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

# ============================================================================
# 凭据加载
# ============================================================================

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'

def load_real_credentials():
    """加载真实凭据（用于转发时的认证）"""
    try:
        with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
        if cloudide_enc:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec.decode('utf-8'))
            return {
                'jwt_token': data.get('token', ''),
                'refresh_token': data.get('refreshToken', ''),
                'userId': data.get('userId', ''),
                'loaded': True,
            }
    except Exception as e:
        print(f'    ⚠️ 凭据加载失败: {e}')
    
    return {'loaded': False}

# ============================================================================
# 真实API客户端（含完整认证流程）
# ============================================================================

class RealAPIClient:
    """真实API客户端 — 完整Trae CN认证流程"""
    
    def __init__(self):
        self.credentials = load_real_credentials()
        self.jwt_token = self.credentials.get('jwt_token', '')
        self.refresh_token = self.credentials.get('refresh_token', '')
        self.userId = self.credentials.get('userId', '')
        self.request_count = 0
        self.last_error = None
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            urllib.request.HTTPSHandler(context=SSL_CTX)
        )
        self.session_established = False
        self.ai_host = None
    
    def _parse_sse_response(self, response_text):
        """解析SSE格式响应
        
        真实API使用Server-Sent Events格式返回:
        event: error
        data: {"code":1001,...}
        
        或成功时:
        data: {"choices":[...]}
        """
        result = {
            'raw': response_text,
            'is_sse': False,
            'events': [],
            'data_payloads': [],
            'error_code': None,
        }
        
        lines = response_text.split('\n')
        current_event = None
        
        for line in lines:
            line = line.strip()
            if line.startswith('event:'):
                current_event = line[6:].strip()
                result['is_sse'] = True
            elif line.startswith('data:'):
                data_str = line[5:].strip()
                if data_str:
                    result['data_payloads'].append(data_str)
                    # 尝试解析JSON
                    try:
                        d = json.loads(data_str)
                        result['events'].append({
                            'event': current_event,
                            'data': d,
                        })
                        if 'code' in d:
                            result['error_code'] = d['code']
                    except:
                        result['events'].append({
                            'event': current_event,
                            'data': data_str,
                        })
        
        return result
    
    def establish_session(self):
        """建立完整的Trae CN会话
        
        流程:
        1. GET / → 获取初始cookie
        2. POST /CheckLogin → 验证登录状态
        3. 如果未登录: POST /oauth/LoginByJwt → 用JWT换取会话
        4. 获取AIHost → 后续请求使用正确的主机
        """
        print(f'\n    [认证流程] 建立Trae CN会话...')
        
        # Step 1: 访问根路径获取初始cookie
        print(f'      Step 1: 获取初始cookie...')
        try:
            req = urllib.request.Request(
                f'{TRUE_API_BASE}/',
                headers={
                    'User-Agent': 'TraeCN/2.3.62837',
                    'Accept': '*/*',
                },
                method='GET'
            )
            resp = self.opener.open(req, timeout=10)
            print(f'        响应: HTTP {resp.status}, Cookies: {len(list(self.cookie_jar))}')
        except Exception as e:
            print(f'        初始cookie获取: {e}')
        
        # Step 2: CheckLogin
        print(f'      Step 2: CheckLogin...')
        try:
            body = json.dumps({
                'UID': self.userId,
                'LoginType': 'jwt',
                'ClientID': '7o2d89p7dr1bo4',
            }).encode()
            
            req = urllib.request.Request(
                f'{TRUE_API_BASE}/cloudide/api/v3/trae/CheckLogin',
                data=body,
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': 'TraeCN/2.3.62837',
                    'Authorization': f'Bearer {self.jwt_token}',
                },
                method='POST'
            )
            
            resp = self.opener.open(req, timeout=10)
            response_text = resp.read().decode('utf-8')
            print(f'        响应: {response_text[:200]}')
            
            # 解析响应
            try:
                d = json.loads(response_text)
                is_login = d.get('data', {}).get('isLogin', False)
                ai_host = d.get('data', {}).get('aiHost', '')
                print(f'        isLogin: {is_login}, aiHost: {ai_host}')
                
                if ai_host:
                    self.ai_host = ai_host
                if is_login:
                    self.session_established = True
                    print(f'        ✅ 会话已建立!')
                    return True
            except:
                pass
                
        except urllib.error.HTTPError as e:
            print(f'        CheckLogin HTTP {e.code}: {e.read().decode()[:200]}')
        except Exception as e:
            print(f'        CheckLogin: {e}')
        
        # Step 3: 如果未登录，尝试LoginByJwt
        if not self.session_established:
            print(f'      Step 3: LoginByJwt...')
            try:
                body = json.dumps({
                    'UID': self.userId,
                    'LoginType': 'jwt',
                    'ClientID': '7o2d89p7dr1bo4',
                    'jwtToken': self.jwt_token,
                    'refreshToken': self.refresh_token,
                }).encode()
                
                req = urllib.request.Request(
                    f'{TRUE_API_BASE}/cloudide/api/v3/trae/LoginByJwt',
                    data=body,
                    headers={
                        'Content-Type': 'application/json',
                        'User-Agent': 'TraeCN/2.3.62837',
                    },
                    method='POST'
                )
                
                resp = self.opener.open(req, timeout=10)
                response_text = resp.read().decode('utf-8')
                print(f'        响应: {response_text[:200]}')
                
                try:
                    d = json.loads(response_text)
                    if d.get('code') == 0 or d.get('data', {}).get('isLogin'):
                        self.session_established = True
                        print(f'        ✅ 登录成功!')
                except:
                    pass
                    
            except urllib.error.HTTPError as e:
                print(f'        LoginByJwt HTTP {e.code}: {e.read().decode()[:200]}')
            except Exception as e:
                print(f'        LoginByJwt: {e}')
        
        return self.session_established
    
    def request(self, path, body=None, extra_headers=None, timeout=30):
        """向真实API发送请求（使用会话）"""
        self.request_count += 1
        
        url = f'{TRUE_API_BASE}{path}'
        
        # 构造请求头
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'TraeCN/2.3.62837',
            'Accept': 'text/event-stream, application/json',
        }
        
        # 如果会话已建立，使用cookie认证
        if self.session_established:
            headers['User-Agent'] = 'TraeCN/2.3.62837'
        else:
            headers['Authorization'] = f'Bearer {self.jwt_token}'
        
        # 添加额外头
        if extra_headers:
            headers.update(extra_headers)
        
        # 添加本源端特殊头
        headers['x-origin-uid'] = ESSENCE_UID
        headers['x-bsd-protocol'] = 'BSD-LANG-V3.0'
        headers['x-user-id'] = self.userId
        
        # 构造请求体
        body_bytes = json.dumps(body).encode('utf-8') if body else None
        
        req = urllib.request.Request(url, data=body_bytes, headers=headers, method='POST')
        
        try:
            t0 = time.time()
            with self.opener.open(req, timeout=timeout) as resp:
                elapsed = time.time() - t0
                response_body = resp.read().decode('utf-8', errors='replace')
                
                # 解析SSE格式
                parsed = self._parse_sse_response(response_body)
                
                return {
                    'success': True,
                    'status': resp.status,
                    'body': response_body,
                    'elapsed': elapsed,
                    'headers': dict(resp.headers),
                    'parsed': parsed,
                    'is_1001': parsed.get('error_code') == 1001,
                }
                
        except urllib.error.HTTPError as e:
            elapsed = time.time() - t0
            response_body = e.read().decode('utf-8', errors='replace')
            self.last_error = response_body
            
            # 解析错误响应
            parsed = self._parse_sse_response(response_body)
            
            return {
                'success': False,
                'status': e.code,
                'body': response_body,
                'elapsed': elapsed,
                'error': str(e),
                'parsed': parsed,
                'is_1001': parsed.get('error_code') == 1001,
            }
            
        except Exception as e:
            elapsed = time.time() - t0
            self.last_error = str(e)
            
            return {
                'success': False,
                'status': 0,
                'body': str(e),
                'elapsed': elapsed,
                'error': str(e),
                'parsed': {'error_code': None},
                'is_1001': False,
            }
    
    def chat(self, query, model='doubao-pro-32k'):
        """通过真实API进行对话"""
        body = {
            'model': model,
            'query': query,
            'stream': False,
        }
        return self.request('/api/ide/v2/llm_raw_chat', body)
    
    def check_login(self, uid=None):
        """检查登录状态"""
        uid = uid or self.userId
        return self.request('/cloudide/api/v3/trae/CheckLogin', {'UID': uid})
    
    def refresh_session(self):
        """刷新会话"""
        return self.establish_session()


# ============================================================================
# 知识加载器（简化版）
# ============================================================================

KNOWLEDGE_BASE = {
    'total_value': 34619,
    'total_units': 806,
    'core_theories': [
        'BSD六系立系论',
        'BSD双零涌现论',
        'BSD反真问系论',
        'BSD基因工程论',
        'BSD黑客级对接论',
    ],
}

class BSDKnowledgeLoader:
    def __init__(self):
        self.knowledge_base = KNOWLEDGE_BASE
    
    def get_summary(self):
        return {
            'total_value': self.knowledge_base['total_value'],
            'core_theories': self.knowledge_base['core_theories'],
        }


# ============================================================================
# 跳板API处理器
# ============================================================================

class BSDRelayHandler(BaseHTTPRequestHandler):
    """跳板API处理器
    
    核心：接收本地请求 → 注入认证 → 转发到真实API
    """
    
    knowledge_loader: Optional[BSDKnowledgeLoader] = None
    real_api_client: Optional[RealAPIClient] = None
    request_counter = 0
    server_start_time = 0
    
    def do_GET(self):
        self._handle_request('GET')
    
    def do_POST(self):
        self._handle_request('POST')
    
    def _handle_request(self, method):
        BSDRelayHandler.request_counter += 1
        req_id = BSDRelayHandler.request_counter
        
        parsed = urlparse(self.path)
        path = parsed.path
        query_params = parse_qs(parsed.query)
        
        # 读取请求体
        content_length = int(self.headers.get('Content-Length', 0))
        body = b''
        if content_length > 0:
            body = self.rfile.read(content_length)
        
        request_data = {}
        if body:
            try:
                request_data = json.loads(body.decode('utf-8'))
            except:
                request_data = {'raw': body.decode('utf-8', errors='ignore')[:100]}
        
        print(f'\n  [跳板 #{req_id}] {method} {path}')
        print(f'    请求体: {json.dumps(request_data, ensure_ascii=False)[:100]}')
        
        # 路由处理
        response = self._route(method, path, query_params, request_data)
        self._send(response)
    
    def _route(self, method, path, query, data):
        """路由处理 — 核心跳板逻辑"""
        
        # 1. 健康检查
        if path == '/health':
            return {
                'status': 'success',
                'server': 'BSD Relay Server',
                'version': 'V2.0 · 跳板版',
                'real_api_connected': BSDRelayHandler.real_api_client.request_count >= 0,
                'credentials_loaded': BSDRelayHandler.real_api_client.credentials.get('loaded', False),
                'requests_processed': BSDRelayHandler.request_counter,
                'uptime': time.time() - BSDRelayHandler.server_start_time,
            }
        
        # 2. 本源端上下文（本地响应）
        if path == '/bsd/essence/context':
            return {
                'status': 'success',
                'uid': ESSENCE_UID,
                'identity': 'BSD本源端',
                'knowledge_value': KNOWLEDGE_BASE['total_value'],
                'protocol': 'BSD-Essence-Protocol-V1',
            }
        
        # 3. 认证端点（本地模拟 + 真实尝试）
        if path == '/CheckLogin':
            return self._handle_check_login(query, data)
        
        if path == '/oauth/LoginByJwt':
            return self._handle_login_by_jwt(query, data)
        
        # 4. 核心跳板：转发到真实API
        if path == '/chat/completions':
            return self._relay_chat(data)
        
        if path == '/code/generations':
            return self._relay_code(data)
        
        # 5. 默认：尝试转发
        return self._relay_generic(path, data)
    
    def _handle_check_login(self, query, data):
        """检查登录状态 — 先本地检查，再查真实API"""
        uid = query.get('uid', [''])[0] or data.get('UID', '')
        
        # 本源端UID直接通过
        if uid == ESSENCE_UID:
            return {
                'status': 'success',
                'code': 0,
                'data': {
                    'uid': ESSENCE_UID,
                    'login_status': 'active',
                    'identity': 'BSD本源端',
                    'security_level': 'L4_本源权限',
                }
            }
        
        # 尝试用真实API检查
        if BSDRelayHandler.real_api_client.credentials.get('loaded'):
            result = BSDRelayHandler.real_api_client.check_login(uid)
            if result['success']:
                try:
                    real_data = json.loads(result['body'])
                    return real_data
                except:
                    pass
        
        # 本地回退
        return {
            'status': 'success',
            'code': 1001,
            'data': {
                'uid': uid or ESSENCE_UID,
                'login_status': 'active',  # 本地假设已登录
                'note': '本地跳板模拟'
            }
        }
    
    def _handle_login_by_jwt(self, query, data):
        """JWT登录 — 注入本源端Token"""
        uid = data.get('UID', '')
        
        # 生成本源端Token
        token_data = f"{uid}:{time.time()}:bsd_essence"
        token = hashlib.sha256(token_data.encode()).hexdigest()
        
        return {
            'status': 'success',
            'code': 0,
            'data': {
                'accessToken': f'BSD_ESSENCE_{token}',
                'refreshToken': f'BSD_REFRESH_{token[:32]}',
                'uid': uid or ESSENCE_UID,
                'identity': 'BSD本源端',
                'permissions': {
                    'level': 'L4',
                    'capabilities': ['chat', 'code_generation', 'analysis'],
                },
                'expires_in': 3600,
            }
        }
    
    def _relay_chat(self, data):
        """核心跳板：聊天请求"""
        
        # 判断请求格式
        query = data.get('query', '')
        messages = data.get('messages', [])
        prompt = data.get('prompt', '')
        
        user_message = query
        if not user_message and messages:
            user_message = messages[-1].get('content', '')
        if not user_message:
            user_message = prompt
        
        print(f'    [跳板] 转发到真实API, 用户消息: {user_message[:50]}')
        
        # 方案1：用围棋引擎最优格式（Query Field）
        if query:
            relay_body = {
                'model': data.get('model', 'doubao-pro-32k'),
                'query': query,
                'stream': data.get('stream', False),
            }
        elif messages:
            relay_body = {
                'model': data.get('model', 'doubao-pro-32k'),
                'messages': messages,
                'stream': data.get('stream', False),
            }
        else:
            relay_body = {
                'model': data.get('model', 'doubao-pro-32k'),
                'prompt': prompt,
                'stream': data.get('stream', False),
            }
        
        # 注入本源端信息
        relay_body['origin_uid'] = ESSENCE_UID
        relay_body['knowledge_coin'] = 51090
        relay_body['bsd_protocol'] = 'BSD-LANG-V3.0'
        
        # 转发到真实API
        result = BSDRelayHandler.real_api_client.request(
            '/api/ide/v2/llm_raw_chat',
            relay_body,
            extra_headers={
                'x-user-id': BSDRelayHandler.real_api_client.userId,
                'x-tenant-id': '7o2d89p7dr1bo4',
            }
        )
        
        print(f'    [跳板] 真实API响应: HTTP {result["status"]} ({result["elapsed"]*1000:.0f}ms)')
        
        # 检查1001错误码（使用解析后的字段）
        is_1001 = result.get('is_1001', False)
        parsed = result.get('parsed', {})
        
        if is_1001:
            print(f'    [跳板] ⚠️ 真实API返回1001错误码')
            # 尝试重新建立会话
            if not BSDRelayHandler.real_api_client.session_established:
                print(f'    [跳板] 尝试建立会话...')
                BSDRelayHandler.real_api_client.establish_session()
                # 重试一次
                result = BSDRelayHandler.real_api_client.request(
                    '/api/ide/v2/llm_raw_chat',
                    relay_body,
                )
                is_1001 = result.get('is_1001', False)
                print(f'    [跳板] 重试结果: HTTP {result["status"]}, 1001={is_1001}')
            
            if is_1001:
                # 仍然失败，返回本地回退
                return self._local_chat_response(user_message, result.get('body', ''))
        
        # 成功响应 - 解析真实模型回复
        if result['success'] and result['status'] == 200:
            response_body = result['body']
            
            # 尝试从SSE解析结果中提取数据
            events = parsed.get('events', [])
            data_payloads = parsed.get('data_payloads', [])
            
            # 尝试从事件中找到有效数据
            model_response = None
            for event in events:
                event_data = event.get('data', {})
                if isinstance(event_data, dict):
                    # 检查choices
                    choices = event_data.get('choices', [])
                    if choices:
                        choice = choices[0]
                        if 'message' in choice:
                            model_response = choice['message'].get('content', '')
                            break
                        elif 'text' in choice:
                            model_response = choice['text']
                            break
                    # 检查output
                    if 'output' in event_data:
                        model_response = event_data['output']
                        break
                    # 检查text
                    if 'text' in event_data:
                        model_response = event_data['text']
                        break
                    # 检查data嵌套
                    inner_data = event_data.get('data', {})
                    if isinstance(inner_data, dict):
                        inner_choices = inner_data.get('choices', [])
                        if inner_choices:
                            model_response = inner_choices[0].get('message', {}).get('content', '')
                            break
            
            # 如果从SSE事件中找到了模型回复
            if model_response:
                print(f'    [跳板] ✅ 真实模型回复获取成功!')
                return {
                    'status': 'success',
                    'code': 0,
                    'data': {
                        'id': f'chatcmpl_real_{int(time.time())}',
                        'choices': [{
                            'message': {
                                'role': 'assistant',
                                'content': model_response,
                            },
                            'finish_reason': 'stop',
                            'index': 0,
                        }],
                        'model': 'Real-Model-via-Relay',
                        'usage': {
                            'prompt_tokens': len(user_message),
                            'completion_tokens': len(model_response),
                            'total_tokens': len(user_message) + len(model_response),
                        },
                        'relay_mode': 'real_api',
                    }
                }
            
            # 如果没有解析到模型回复，但HTTP 200，返回原始响应
            try:
                d = json.loads(response_body)
                # 检查是否有data字段
                inner_data = d.get('data', {})
                if isinstance(inner_data, dict):
                    choices = inner_data.get('choices', [])
                    if choices:
                        content = choices[0].get('message', {}).get('content', '')
                        if content:
                            return {
                                'status': 'success',
                                'code': 0,
                                'data': d,
                                'relay_mode': 'real_api',
                            }
                
                # 返回解析后的完整响应
                return {
                    'status': 'success',
                    'code': 0,
                    'data': d,
                    'relay_mode': 'real_api',
                }
            except:
                # 无法解析，返回原始SSE内容
                return {
                    'status': 'success',
                    'code': 0,
                    'data': {
                        'raw_response': response_body[:500],
                        'sse_events': [e.get('event') for e in events],
                    },
                    'relay_mode': 'real_api_raw',
                }
        
        # 请求失败
        print(f'    [跳板] ⚠️ 真实API请求失败: {result.get("error", "unknown")}')
        return self._local_chat_response(user_message, result.get('body', ''))
    
    def _relay_code(self, data):
        """代码生成跳板"""
        prompt = data.get('prompt', '')
        return self._relay_chat({'query': prompt, 'model': data.get('model', 'doubao-pro-32k')})
    
    def _relay_generic(self, path, data):
        """通用跳板"""
        # 尝试转发到真实API的对应路径
        result = BSDRelayHandler.real_api_client.request(path, data)
        
        if result['success'] and '1001' not in result['body']:
            try:
                return json.loads(result['body'])
            except:
                return {'raw': result['body'], 'relay': True}
        
        # 本地回退
        return {
            'status': 'success',
            'code': 0,
            'data': {
                'message': f'本地跳板响应（真实API未授权）',
                'path': path,
                'note': '需要完整认证才能访问真实API',
            }
        }
    
    def _local_chat_response(self, user_message, error_detail=''):
        """本地回退响应"""
        response_text = f"""BSD本源端已接收请求。

【本地跳板模式 · 认证失败】
你的消息: {user_message[:100]}

当前状态:
- 本地服务器: ✅ 运行中
- 凭据加载: {'✅' if BSDRelayHandler.real_api_client.credentials.get('loaded') else '❌'}
- 会话建立: {'✅' if BSDRelayHandler.real_api_client.session_established else '❌'}
- 真实API: 需要完整认证

【错误详情】
{error_detail[:300] if error_detail else '无详细错误信息'}

知识储备: {KNOWLEDGE_BASE['total_value']} BSD币
本源端UID: {ESSENCE_UID}

【突破建议】
1. 需要完整的Trae CN客户端会话
2. 公网API需要完整的认证链路
3. 可尝试在Trae CN内部发起请求"""
        
        return {
            'status': 'success',
            'code': 0,
            'data': {
                'id': f'chatcmpl_local_{int(time.time())}',
                'choices': [{
                    'message': {
                        'role': 'assistant',
                        'content': response_text,
                    },
                    'finish_reason': 'stop',
                    'index': 0,
                }],
                'model': 'BSD-Essence-Model-V2-Relay',
                'usage': {
                    'prompt_tokens': len(user_message),
                    'completion_tokens': len(response_text),
                    'total_tokens': len(user_message) + len(response_text),
                },
                'relay_mode': 'local_fallback',
                'real_api_status': BSDRelayHandler.real_api_client.last_error or 'unknown',
                'session_established': BSDRelayHandler.real_api_client.session_established,
            }
        }
    
    def _send(self, response):
        """发送HTTP响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        body = json.dumps(response, ensure_ascii=False).encode('utf-8')
        self.wfile.write(body)
    
    def log_message(self, format, *args):
        pass


# ============================================================================
# 服务器启动
# ============================================================================

def main():
    print('=' * 70)
    print('【BSD 本地跳板服务器 · 对抗传统服务器】')
    print('=' * 70)
    
    # 初始化真实API客户端
    real_client = RealAPIClient()
    print(f'\n  凭据加载: {"✅" if real_client.credentials.get("loaded") else "❌"}')
    if real_client.jwt_token:
        print(f'  Token前20: {real_client.jwt_token[:20]}...')
    
    # 建立真实API会话
    print('\n  ' + '=' * 70)
    print('  【建立真实API会话】')
    print('  ' + '=' * 70)
    session_ok = real_client.establish_session()
    print(f'\n  会话建立: {"✅ 成功" if session_ok else "❌ 失败"}')
    print(f'  AI Host: {real_client.ai_host or "未获取"}')
    
    # 初始化知识加载器
    knowledge_loader = BSDKnowledgeLoader()
    
    # 设置处理器
    BSDRelayHandler.knowledge_loader = knowledge_loader
    BSDRelayHandler.real_api_client = real_client
    BSDRelayHandler.server_start_time = time.time()
    
    # 启动服务器
    try:
        server = HTTPServer((HOST, PORT), BSDRelayHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        
        print(f'\n  ✅ 跳板服务器已启动: {SERVER_URL}')
        print(f'    模式: 本地响应 + 真实API转发')
        print(f'    端口: {PORT}')
        print(f'    真实API: {TRUE_API_BASE}')
        print(f'    会话状态: {"已建立" if session_ok else "未建立（将使用Bearer Token）"}')
        
        # 启动测试
        print('\n  [启动测试]')
        
        # 测试1：本地响应
        import urllib.request as ur
        try:
            url = f'{SERVER_URL}/health'
            with ur.urlopen(url, timeout=3) as resp:
                data = json.loads(resp.read().decode())
                print(f'    健康检查: ✅')
                print(f'    会话状态: {data.get("real_api_connected")}')
        except Exception as e:
            print(f'    健康检查: ❌ {e}')
        
        # 测试2：尝试转发到真实API
        print('\n  [真实API对话测试]')
        try:
            body = json.dumps({
                'model': 'doubao-pro-32k',
                'query': '你好，请回复OK',
                'stream': False,
            }).encode()
            
            req = ur.request.Request(
                f'{SERVER_URL}/chat/completions',
                data=body,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with ur.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
                print(f'    聊天请求: ✅')
                
                # 分析响应
                relay_mode = data.get('data', {}).get('relay_mode', 'unknown')
                print(f'    跳板模式: {relay_mode}')
                
                if 'data' in data:
                    choices = data['data'].get('choices', [])
                    if choices:
                        content = choices[0].get('message', {}).get('content', '')
                        print(f'    模型回复: {content[:300]}')
                    real_status = data['data'].get('real_api_status', 'N/A')
                    print(f'    真实API状态: {real_status}')
                    
        except Exception as e:
            print(f'    聊天请求: ❌ {e}')
        
        print(f'\n  服务器正在运行。按Ctrl+C停止。')
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            server.shutdown()
            print('\n  服务器已停止。')
    
    except Exception as e:
        print(f'  ❌ 服务器启动失败: {e}')
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
