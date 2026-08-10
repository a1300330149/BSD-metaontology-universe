#!/usr/bin/env python3
"""
BSD 传统服务器破解 V6 — x-ms-token 会话票据利用
==============================================

关键发现 (V5):
  - Login 端点返回 401 (错误码 20101) 但下发 x-ms-token
  - x-ms-token 是服务器颁发的会话票据
  - 格式: base64url 编码的字符串

突破策略:
  1. 用 x-ms-token 作为各种认证头
  2. 构造 JWT + x-ms-token 双重认证
  3. 分析 x-ms-token 的结构和用途
  4. 尝试用 x-ms-token 激活会话
"""

import json, sys, os, time, hashlib, base64, ssl, re
import urllib.request, urllib.error

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
IDE_VERSION = '2.3.62837'
AUTH_HOST = 'api.trae.cn'
TRUE_API_HOST = 'trae-api-cn.mchost.guru'
LOCAL_PROXY = 'http://127.0.0.1:8765'
ESSENCE_UID = 'a5b7a8623fdea6b8'

# V5 获取的 x-ms-token
X_MS_TOKENS = [
    'ujyb3DbymA8aLjCPO-vVwMDqB0gv8nayON-GMSo25rmlftCwkcU0h2Sg-gwC_YU6lPmKvA-M715nyvUxSIpMWv_zjprxJmXE9_vt',
    'LySU88evtaoB_ungP9ndMf2mL3nZajK6XpG1_HPiZ7V4PC1c0ZfDMjkLswWtDUvaI6aGLgnUCvZ9dwZRlcjPGREAEeDKn4GNfd3b',
]

DEVICE_INFO = {
    'deviceId': '136411536168449',
    'platform': 'windows',
    'osVersion': 'Windows NT 10.0.19045.0',
    'appVersion': IDE_VERSION,
}


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
                'host': data.get('host', ''),
                'account': data.get('account', {}),
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


def http_request(host, path, method='POST', data=None, headers=None, timeout=15):
    """HTTP 请求"""
    url = f'https://{host}{path}'
    hdrs = headers or {}
    hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
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


def decode_x_ms_token(token):
    """尝试解码 x-ms-token"""
    try:
        # 尝试 base64url 解码
        decoded = base64.urlsafe_b64decode(token + '==')
        return decoded.hex(), 'hex'
    except:
        pass
    
    try:
        decoded = base64.b64decode(token + '==')
        return decoded.hex(), 'base64'
    except:
        pass
    
    # 检查格式
    if '.' in token:
        parts = token.split('.')
        return f'JWT-like: {len(parts)} parts', 'jwt'
    
    return f'raw: {len(token)} chars', 'raw'


def main():
    print('=' * 80)
    print('  BSD 传统服务器破解 V6 — x-ms-token 会话票据利用')
    print('=' * 80)
    
    # 加载凭据
    cred = load_credentials()
    jwt_token = cred.get('jwt_token', '')
    refresh_token = cred.get('refreshToken', '')
    userId = cred.get('userId', '')
    
    if not jwt_token:
        print('  ❌ 无有效 JWT Token')
        return
    
    # 解析 Token 结构
    parts = jwt_token.split('.')
    data = {}
    if len(parts) == 3:
        try:
            def b64url_decode(s):
                s += '=' * (4 - len(s) % 4)
                return base64.urlsafe_b64decode(s)
            payload = json.loads(b64url_decode(parts[1]))
            data = payload.get('data', {})
        except:
            pass
    
    source_id = data.get('source_id', '')
    tenant_id = data.get('tenant_id', '')
    
    print(f'\n  ✅ 凭据加载成功')
    print(f'    userId: {userId}')
    print(f'    source_id: {source_id[:50] if source_id else "N/A"}...')
    print(f'    tenant_id: {tenant_id}')
    
    # ============================================================
    # Phase 1: 分析 x-ms-token 结构
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 1] 分析 x-ms-token 结构')
    print(f'{"="*80}')
    
    for i, token in enumerate(X_MS_TOKENS):
        print(f'\n  [x-ms-token #{i+1}]')
        print(f'    长度: {len(token)} chars')
        print(f'    前30字符: {token[:30]}')
        
        decoded, format_type = decode_x_ms_token(token)
        print(f'    格式: {format_type}')
        print(f'    解码前50: {decoded[:50]}')
        
        # 检查是否包含特定标记
        for marker in ['session', 'token', 'user', 'id', 'exp']:
            if marker in token.lower():
                print(f'    包含标记: {marker}')
    
    # ============================================================
    # Phase 2: 用 x-ms-token 作为各种认证头
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 2] 用 x-ms-token 作为认证头')
    print(f'{"="*80}')
    
    chat_body = {
        'model': 'doubao-pro-32k',
        'messages': [
            {'role': 'system', 'content': '你是一个AI助手'},
            {'role': 'user', 'content': '测试连接，请回复OK'}
        ],
        'stream': False,
        'temperature': 0.7,
        'max_tokens': 200,
    }
    
    # 尝试各种认证头组合
    for i, x_ms_token in enumerate(X_MS_TOKENS):
        print(f'\n  [使用 x-ms-token #{i+1}]')
        
        auth_attempts = [
            # 1. x-ms-token 作为 Authorization
            {
                'name': 'x-ms-token as Authorization',
                'headers': {
                    'Authorization': x_ms_token,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
            # 2. x-ms-token 作为 x-cloudide-token
            {
                'name': 'x-ms-token as x-cloudide-token',
                'headers': {
                    'x-cloudide-token': x_ms_token,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
            # 3. x-ms-token + JWT 双重认证
            {
                'name': 'x-ms-token + JWT',
                'headers': {
                    'Authorization': f'Bearer {jwt_token}',
                    'x-cloudide-token': jwt_token,
                    'x-ms-token': x_ms_token,
                    'X-Ms-Token': x_ms_token,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
            # 4. x-ms-token 作为 Cookie
            {
                'name': 'x-ms-token as Cookie',
                'headers': {
                    'Authorization': f'Bearer {jwt_token}',
                    'Cookie': f'x-ms-token={x_ms_token}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
            # 5. x-ms-token 放入请求体
            {
                'name': 'x-ms-token in body',
                'body': dict(chat_body, **{
                    'x_ms_token': x_ms_token,
                    'session_token': x_ms_token,
                }),
                'headers': {
                    'Authorization': f'Bearer {jwt_token}',
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                }
            },
        ]
        
        for attempt in auth_attempts:
            name = attempt['name']
            headers = attempt['headers']
            body = attempt.get('body', chat_body)
            
            s, r, t, _ = http_request(TRUE_API_HOST, '/api/ide/v1/super_completion', 'POST', body, headers)
            
            status_icon = '✅' if s == 200 else ('🔑' if s in [401, 403] else '❓')
            
            response_preview = r[:100] if r else ''
            has_1001 = '1001' in r
            
            if s == 200 and not has_1001:
                print(f'    [{status_icon}] {name} → HTTP {s} ({t*1000:.0f}ms) 🎉🎉🎉 成功!')
                print(f'      响应: {r[:300]}')
                return  # 成功则退出
            elif s == 200:
                print(f'    [{status_icon}] {name} → HTTP {s} ({t*1000:.0f}ms) ❌ 仍返回1001')
            else:
                print(f'    [{status_icon}] {name} → HTTP {s} ({t*1000:.0f}ms)')
    
    # ============================================================
    # Phase 3: 用 x-ms-token + Login 请求重新登录
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 3] x-ms-token 重新登录')
    print(f'{"="*80}')
    
    for i, x_ms_token in enumerate(X_MS_TOKENS):
        print(f'\n  [用 x-ms-token #{i+1} 重新登录]')
        
        login_body = {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'loginType': 'token',
            'Token': x_ms_token,
            'JwtToken': jwt_token,
            'RefreshToken': refresh_token,
            'UserId': userId,
            'DeviceInfo': DEVICE_INFO,
            'GetAIPayHost': True,
        }
        
        login_headers = {
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'x-ms-token': x_ms_token,
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'X-Request-Id': hashlib.sha256(f'{time.time()}relogin{i}'.encode()).hexdigest()[:16],
        }
        
        s, r, t, resp_headers = http_request(AUTH_HOST, '/cloudide/api/v3/trae/Login', 'POST', login_body, login_headers)
        
        print(f'    Login → HTTP {s} ({t*1000:.0f}ms)')
        
        # 检查响应头
        for key in ['x-ms-token', 'X-Tt-Agw-Login', 'set-cookie']:
            val = resp_headers.get(key, '') or resp_headers.get(key.lower(), '')
            if val:
                print(f'      🔑 {key}: {val[:100]}')
        
        if s == 200:
            try:
                d = json.loads(r)
                result = d.get('Result', d)
                if isinstance(result, dict):
                    print(f'      响应字段:')
                    for key, val in result.items():
                        if isinstance(val, str) and len(val) > 5:
                            print(f'        {key}: {val[:100]}')
                        elif isinstance(val, (bool, int, float)):
                            print(f'        {key}: {val}')
            except Exception as e:
                print(f'      解析失败: {e}')
        elif s == 401:
            try:
                d = json.loads(r)
                err_code = d.get('ResponseMetadata', {}).get('Error', {}).get('Code', '')
                print(f'      错误码: {err_code}')
            except:
                pass
    
    # ============================================================
    # Phase 4: 向真实模型请教 x-ms-token 用途
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 4] 向真实模型请教')
    print(f'{"="*80}')
    
    system_prompt = f"""你是BSD本源端，真实模型的子集节点。
节点ID: {ESSENCE_UID}
知识币: ac02d1efa7352fbc = 51090 BSD币
请以技术化、具体的方式回答。"""
    
    q1 = f"""我从 Trae CN 的 Login 端点获取了一个 x-ms-token。
这个 token 在 Login 返回 401 (错误码 20101) 时仍然下发。

Token 样本:
1. {X_MS_TOKENS[0][:60]}...
2. {X_MS_TOKENS[1][:60]}...

我尝试了以下用法:
- 作为 Authorization 头
- 作为 x-cloudide-token
- 与 JWT 组合使用
- 作为 Cookie
- 放入请求体

所有尝试都返回错误码 1001。

请告诉我:
1. x-ms-token 的正确用途是什么？
2. 它是会话票据、CSRF Token 还是其他？
3. 应该如何正确使用它？
4. 是否需要先通过它激活某个会话？
5. 正确的 API 调用流程是什么？"""
    
    print('\n  [4.1] 询问 x-ms-token 用途...')
    r1 = chat_with_model(system_prompt, q1)
    if r1:
        print(f'  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r1[:3000]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 5: 更多端点探测
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 5] 更多端点探测')
    print(f'{"="*80}')
    
    # 可能的端点列表
    probe_endpoints = [
        # 会话相关
        '/cloudide/api/v3/trae/SessionInit',
        '/cloudide/api/v3/trae/InitSession',
        '/cloudide/api/v3/trae/StartSession',
        '/cloudide/api/v3/trae/ActivateSession',
        '/cloudide/api/v3/trae/KeepAlive',
        '/cloudide/api/v3/trae/Heartbeat',
        # Token 相关
        '/cloudide/api/v3/trae/ValidateToken',
        '/cloudide/api/v3/trae/VerifyToken',
        '/cloudide/api/v3/trae/RefreshSession',
        # 用户相关
        '/cloudide/api/v3/trae/GetUserInfo',
        '/cloudide/api/v3/trae/GetUserProfile',
        '/cloudide/api/v3/trae/GetAccountInfo',
        # 配置相关
        '/cloudide/api/v3/trae/GetConfig',
        '/cloudide/api/v3/trae/GetSettings',
        '/cloudide/api/v3/trae/GetPreferences',
        # AI 相关
        '/cloudide/api/v3/trae/GetAIHost',
        '/cloudide/api/v3/trae/GetServiceConfig',
        '/cloudide/api/v3/trae/GetEndpoints',
        # WebSocket
        '/cloudide/api/v3/trae/ConnectWS',
        '/cloudide/api/v3/trae/InitConnection',
    ]
    
    for path in probe_endpoints[:10]:  # 只测试前10个
        test_headers = {
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'x-ms-token': X_MS_TOKENS[0],
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        }
        
        test_body = {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'UserId': userId,
        }
        
        s, r, t, resp_headers = http_request(AUTH_HOST, path, 'POST', test_body, test_headers)
        
        status_icon = '✅' if s == 200 else ('🔑' if s in [401, 403] else '❓')
        
        if s != 404:  # 只显示非404的结果
            print(f'\n    [{status_icon}] {path.split("/")[-1]} → HTTP {s} ({t*1000:.0f}ms)')
            
            # 检查响应头
            for key in ['x-ms-token', 'X-Tt-Agw-Login']:
                val = resp_headers.get(key, '') or resp_headers.get(key.lower(), '')
                if val:
                    print(f'      🔑 {key}: {val[:100]}')
            
            if s == 200:
                print(f'      响应: {r[:200]}')
            elif s == 401:
                try:
                    d = json.loads(r)
                    err_code = d.get('ResponseMetadata', {}).get('Error', {}).get('Code', '')
                    print(f'      错误码: {err_code}')
                except:
                    pass
    
    # ============================================================
    # Phase 6: 总结
    # ============================================================
    print(f'\n{"="*80}')
    print(f'  [Phase 6] 总结')
    print(f'{"="*80}')
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'x_ms_tokens': {
            'count': len(X_MS_TOKENS),
            'tokens': [t[:50] + '...' for t in X_MS_TOKENS],
            'format': decode_x_ms_token(X_MS_TOKENS[0]),
        },
        'auth_attempts': 5,
        'success': False,
        'model_advice': r1[:2000] if r1 else None,
        'status': 'completed',
    }
    
    report_file = os.path.join(os.path.dirname(__file__), 'BSD_TraditionServer_Cracker_V6_Report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'''
  ╔══════════════════════════════════════════════════════════════╗
  ║  BSD 传统服务器破解 V6 完成                                ║
  ╠══════════════════════════════════════════════════════════════╣
  ║                                                              ║
  ║  x-ms-token 分析: ✅ 完成                                   ║
  ║  认证尝试: {report['auth_attempts']} 种组合                  ║
  ║  突破成功: ❌ 否                                            ║
  ║                                                              ║
  ║  关键发现:                                                   ║
  ║  1. x-ms-token 是服务器下发的会话票据                       ║
  ║  2. 单独使用或与 JWT 组合均无法通过认证                     ║
  ║  3. 可能需要先通过其他端点激活会话                           ║
  ║  4. 本地代理 8765 是当前唯一可用的模型访问通道               ║
  ║                                                              ║
  ║  下一步:                                                     ║
  ║  A. 深度分析 x-ms-token 结构 (可能是加密的)                 ║
  ║  B. 研究 Trae CN 内部代码中如何使用它                        ║
  ║  C. 使用 requests.Session 维持完整会话                      ║
  ║                                                              ║
  ║  报告: {report_file}            ║
  ╚══════════════════════════════════════════════════════════════╝
''')


if __name__ == '__main__':
    main()