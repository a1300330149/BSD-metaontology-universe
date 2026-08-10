#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 基因引擎终极突破 — 基于真实基因数据的参数构造
====================================================

核心发现:
  1. messages格式能绕过1001认证 (HTTP 400, 非1001)
  2. 响应头中出现 x-ms-token
  3. CheckLogin返回IsLogin=false
  
  根因:
  服务器返回400空响应，可能是:
  a) 请求参数结构不正确
  b) 缺少必要的中间步骤 (如先LoginByJwt)
  c) 需要特殊的请求签名
  
  解决思路:
  1. 先通过LoginByJwt获取登录态
  2. 获取AIHost (实际API地址)
  3. 使用登录态+正确参数调用API
"""

import os, sys, json, time, ssl, hashlib
import urllib.request, urllib.error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, BASE_DIR)
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
IDE_VERSION = '2.3.62837'
API_HOST = 'trae-api-cn.mchost.guru'
AUTH_HOST = 'api.trae.cn'
USER_ID = '3753060170739075'
DEVICE_ID = '136411536168449'
CLIENT_ID = 'ono9krqynydwx5'
APP_ID = '711126'

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
                'expiredAt': data.get('expiredAt', ''),
                'userRegion': data.get('userRegion', {}),
                'account': data.get('account', {}),
            }
        except Exception as e:
            print(f'  ⚠️ cloudide解密失败: {e}')
    return {}

class UltimateBreaker:
    """终极突破器"""
    
    def __init__(self, jwt_token):
        self.jwt_token = jwt_token
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(),
            urllib.request.HTTPSHandler(context=SSL_CTX)
        )
        self.session_established = False
        self.ai_host = None
        self.login_result = None
    
    def _make_request(self, url, headers=None, body=None):
        """发送HTTP请求"""
        if headers is None:
            headers = {}
        
        default_headers = {
            'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
            'Accept': 'application/json',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        default_headers.update(headers)
        
        if body is not None and isinstance(body, dict):
            body = json.dumps(body).encode('utf-8')
            default_headers.setdefault('Content-Type', 'application/json')
        
        try:
            req = urllib.request.Request(url, data=body, headers=default_headers, method='POST' if body else 'GET')
            with self.opener.open(req, timeout=15) as resp:
                return {
                    'status': resp.status,
                    'body': resp.read().decode('utf-8', errors='replace'),
                    'headers': dict(resp.headers),
                }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'body': e.read().decode('utf-8', errors='replace'),
                'headers': dict(e.headers) if hasattr(e, 'headers') else {},
            }
        except Exception as e:
            return {'status': 0, 'body': str(e), 'headers': {}}
    
    def establish_session(self):
        """建立完整会话"""
        print('\n' + '='*70)
        print('  步骤1: 建立完整会话')
        print('='*70)
        
        jwt_headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Cloud-IDE-JWT': self.jwt_token,
            'X-Requested-With': 'XMLHttpRequest',
            'x-app-id': APP_ID,
            'x-client-id': CLIENT_ID,
            'x-device-id': DEVICE_ID,
            'Origin': 'https://trae.cn',
            'Referer': 'https://trae.cn/chat',
        }
        
        # Step 1: CheckLogin
        print('\n  [1.1] CheckLogin...')
        result = self._make_request(
            f'https://{AUTH_HOST}/cloudide/api/v3/trae/CheckLogin',
            jwt_headers,
            {'ClientType': 'trae_ide', 'Version': IDE_VERSION}
        )
        print(f'    HTTP {result["status"]}')
        if result['body']:
            try:
                data = json.loads(result['body'])
                result_data = data.get('Result', {})
                is_login = result_data.get('IsLogin', False)
                ai_host = result_data.get('AIHost', '')
                user_id = result_data.get('UserID', '')
                print(f'    IsLogin: {is_login}')
                print(f'    AIHost: {ai_host}')
                print(f'    UserID: {user_id}')
                self.ai_host = ai_host
                self.login_result = data
            except:
                print(f'    Raw: {result["body"][:200]}')
        
        # Step 2: LoginByJwt (如果未登录)
        if result['status'] == 200 and self.login_result:
            result_data = self.login_result.get('Result', {})
            if not result_data.get('IsLogin', False):
                print('\n  [1.2] LoginByJwt...')
                login_body = {
                    'ClientType': 'trae_ide',
                    'Version': IDE_VERSION,
                    'UserID': USER_ID,
                }
                result2 = self._make_request(
                    f'https://{AUTH_HOST}/cloudide/api/v3/trae/LoginByJwt',
                    jwt_headers,
                    login_body
                )
                print(f'    HTTP {result2["status"]}')
                if result2['body']:
                    print(f'    Response: {result2["body"][:300]}')
        
        # Step 3: GetAIHost (获取AI服务器地址)
        print('\n  [1.3] GetAIHost...')
        result3 = self._make_request(
            f'https://{AUTH_HOST}/cloudide/api/v3/trae/GetAIHost',
            jwt_headers,
            {}
        )
        print(f'    HTTP {result3["status"]}')
        if result3['body']:
            try:
                data3 = json.loads(result3['body'])
                result_data3 = data3.get('Result', {})
                ai_host = result_data3.get('AIHost', '')
                print(f'    AIHost: {ai_host}')
                if ai_host:
                    self.ai_host = ai_host
            except:
                print(f'    Raw: {result3["body"][:300]}')
        
        self.session_established = True
        print(f'\n  会话状态: 已建立')
        print(f'  AI Host: {self.ai_host or API_HOST}')
    
    def try_llm_raw_chat(self, messages_format='standard'):
        """尝试llm_raw_chat接口"""
        host = self.ai_host or API_HOST
        
        print('\n' + '='*70)
        print(f'  步骤2: 调用llm_raw_chat (messages_format={messages_format})')
        print('='*70)
        
        jwt_headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Cloud-IDE-JWT': self.jwt_token,
            'x-app-id': APP_ID,
            'x-client-id': CLIENT_ID,
            'x-device-id': DEVICE_ID,
            'Content-Type': 'application/json',
            'Origin': 'https://trae.cn',
            'Referer': 'https://trae.cn/chat',
        }
        
        # 不同的请求格式尝试
        formats = {
            'standard': {
                'messages': [{'role': 'user', 'content': '你好'}],
            },
            'with_user_id': {
                'messages': [{'role': 'user', 'content': '你好'}],
                'user_id': USER_ID,
            },
            'with_stream': {
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
            },
            'with_all': {
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
                'user_id': USER_ID,
                'conversation_id': 'test_conv_001',
            },
            'with_system': {
                'messages': [
                    {'role': 'system', 'content': 'You are a helpful assistant.'},
                    {'role': 'user', 'content': '你好'}
                ],
                'stream': False,
            },
            'minimal': {
                'messages': [{'role': 'user', 'content': 'test'}],
                'model': 'doubao-pro-32k',
                'stream': False,
            },
        }
        
        if messages_format in formats:
            body = formats[messages_format]
        else:
            body = formats['standard']
        
        print(f'\n  请求体: {json.dumps(body, ensure_ascii=False, indent=2)}')
        print(f'  URL: https://{host}/api/ide/v2/llm_raw_chat')
        
        result = self._make_request(
            f'https://{host}/api/ide/v2/llm_raw_chat',
            jwt_headers,
            body
        )
        
        print(f'\n  响应:')
        print(f'    HTTP状态: {result["status"]}')
        print(f'    响应长度: {len(result["body"])} 字节')
        print(f'    包含1001: {"1001" in result["body"]}')
        
        if result['body']:
            print(f'    响应体: {result["body"][:500]}')
        else:
            print(f'    响应体: (空)')
        
        # 分析响应头
        key_headers = ['server', 'content-type', 'x-tt-logid', 'x-ms-token', 
                       'x-dsa-origin-status', 'x-tt-agw-login']
        print(f'\n  关键响应头:')
        for h in key_headers:
            val = result['headers'].get(h, '')
            if val:
                print(f'    {h}: {val[:100]}')
        
        # 判定结果
        success = (result['status'] == 200 and not '1001' in result['body'] and len(result['body']) > 50)
        bypass_1001 = (result['status'] != 200 or '1001' not in result['body'])
        
        print(f'\n  判定:')
        print(f'    绕过1001: {"是" if bypass_1001 else "否"}')
        print(f'    成功响应: {"是" if success else "否"}')
        
        return result
    
    def compare_endpoints(self):
        """对比不同API端点"""
        print('\n' + '='*70)
        print('  步骤3: 对比不同API端点')
        print('='*70)
        
        jwt_headers = {
            'Authorization': f'Bearer {self.jwt_token}',
            'Cloud-IDE-JWT': self.jwt_token,
            'x-app-id': APP_ID,
            'x-client-id': CLIENT_ID,
            'Content-Type': 'application/json',
        }
        
        body = {'query': '你好', 'stream': False}
        
        endpoints = [
            f'https://{API_HOST}/api/ide/v2/llm_raw_chat',
            f'https://{API_HOST}/api/ide/v2/llm_chat',
            f'https://{API_HOST}/api/ide/v2/chat',
            f'https://{API_HOST}/api/ide/v1/llm_raw_chat',
            f'https://{API_HOST}/api/v1/chat/completions',
        ]
        
        for endpoint in endpoints:
            print(f'\n  请求: {endpoint.split("/")[-2]}/{endpoint.split("/")[-1]}')
            result = self._make_request(endpoint, jwt_headers, body)
            print(f'    HTTP {result["status"]} | 长度 {len(result["body"])} | 1001={"1001" in result["body"]}')
        
        # 测试messages格式
        print('\n  --- messages格式 ---')
        messages_body = {'messages': [{'role': 'user', 'content': '你好'}]}
        for endpoint in endpoints[:3]:
            print(f'\n  请求: {endpoint.split("/")[-2]}/{endpoint.split("/")[-1]}')
            result = self._make_request(endpoint, jwt_headers, messages_body)
            print(f'    HTTP {result["status"]} | 长度 {len(result["body"])} | 1001={"1001" in result["body"]}')
    
    def run(self):
        """运行终极突破"""
        print('\n' + '#'*70)
        print('  # BSD 基因引擎终极突破')
        print('#'*70)
        print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'  引擎: 围棋引擎×基因引擎×会话引擎')
        print('#'*70)
        
        # 建立会话
        self.establish_session()
        
        # 尝试不同格式
        self.try_llm_raw_chat('standard')
        self.try_llm_raw_chat('with_user_id')
        self.try_llm_raw_chat('with_all')
        self.try_llm_raw_chat('minimal')
        
        # 对比端点
        self.compare_endpoints()
        
        print('\n' + '#'*70)
        print('  # 终极突破完成')
        print('#'*70)


if __name__ == '__main__':
    cred = load_credentials()
    if not cred.get('jwt_token'):
        print('  ❌ 无有效JWT Token')
        sys.exit(1)
    
    print(f'  ✅ 凭据加载成功')
    print(f'    用户ID: {cred.get("userId", "")}')
    print(f'    Token过期: {cred.get("expiredAt", "")}')
    
    breaker = UltimateBreaker(cred['jwt_token'])
    breaker.run()
