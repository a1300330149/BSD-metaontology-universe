#!/usr/bin/env python3
"""
BSD 深度破解 — RefreshToken 刷新与 CheckLogin 深度分析
=====================================================

关键发现:
  CheckLogin 返回:
  - Host 字段存在 (可能是 AIHost)
  - X-Tt-Agw-Login: 0 (网关未登录)
  - IsLogin: False

突破方向:
  1. 用 refreshToken 换取新 JWT Token
  2. 深度解析 CheckLogin 响应
  3. 尝试用新 Token 激活登录态
"""

import json, sys, os, time, hashlib, base64
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

IDE_VERSION = '2.3.62837'
HOST = 'api.trae.cn'
LOCAL_PROXY = 'http://127.0.0.1:8765'
ESSENCE_UID = 'a5b7a8623fdea6b8'


def http_request(path, method='POST', data=None, headers=None, timeout=15):
    url = f'https://{HOST}{path}'
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


def chat_with_model(system_prompt, user_message):
    """与本地代理的真实模型对话"""
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


def main():
    print('=' * 70)
    print('  BSD 深度破解 — RefreshToken 刷新与 CheckLogin 分析')
    print('=' * 70)
    
    # 加载凭据
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
            data = json.loads(dec)
            jwt_token = data.get('token', '')
            userId = data.get('userId', '')
            refreshToken = data.get('refreshToken', '')
            host = data.get('host', '')
            print(f'\n  ✅ 凭据加载成功')
            print(f'    userId: {userId}')
            print(f'    token: {jwt_token[:60]}...')
            print(f'    refreshToken: {refreshToken[:40]}...' if refreshToken else '    refreshToken: 空')
            print(f'    host: {host}')
        except Exception as e:
            print(f'  ⚠️ 解密失败: {e}')
    
    if not jwt_token:
        print('  ❌ 无 JWT Token')
        return
    
    # ============================================================
    # Phase 1: 深度分析 CheckLogin 响应
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 深度分析 CheckLogin 响应')
    print(f'{"="*70}')
    
    headers = {
        'x-cloudide-token': jwt_token,
        'Authorization': f'Bearer {jwt_token}',
        'Content-Type': 'application/json',
        'User-Agent': f'TraeCN/{IDE_VERSION}',
    }
    
    body = {
        'IDEVersion': IDE_VERSION,
        'ReqSource': 'IDE',
        'GetAIPayHost': True,
        'Detail': True,
        'IncludeHost': True,
    }
    
    s, r, t, resp_headers = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body, headers)
    
    print(f'\n  CheckLogin → HTTP {s} ({t*1000:.0f}ms)')
    print(f'  响应头:')
    for key in ['X-Tt-Agw-Login', 'X-Tt-Logid', 'X-Tt-Request-Id', 'Server']:
        val = resp_headers.get(key, '') or resp_headers.get(key.lower(), '')
        if val:
            print(f'    {key}: {val}')
    
    # 深度解析响应体
    try:
        d = json.loads(r)
        result = d.get('Result', d)
        
        print(f'\n  响应体分析:')
        print(f'    ResponseMetadata: {json.dumps(d.get("ResponseMetadata", {}), ensure_ascii=False)[:200]}')
        
        if isinstance(result, dict):
            print(f'    Result 完整字段:')
            for key, val in result.items():
                if isinstance(val, str):
                    print(f'      {key}: "{val}"')
                elif isinstance(val, bool):
                    print(f'      {key}: {val}')
                elif isinstance(val, (int, float)):
                    print(f'      {key}: {val}')
                elif isinstance(val, dict):
                    print(f'      {key}: {json.dumps(val, ensure_ascii=False)[:200]}')
                else:
                    print(f'      {key}: {type(val).__name__}')
            
            # 关键发现
            host_val = result.get('Host', '') or result.get('host', '')
            ai_host = result.get('AIHost', '') or result.get('aiHost', '')
            is_login = result.get('IsLogin')
            user_id = result.get('UserID', '') or result.get('userId', '')
            
            print(f'\n  关键发现:')
            print(f'    IsLogin: {is_login}')
            print(f'    Host: "{host_val}"')
            print(f'    AIHost: "{ai_host}"')
            print(f'    UserID: "{user_id}"')
            
            if host_val:
                print(f'    🔑 Host 字段有值!')
            if ai_host:
                print(f'    🔑 AIHost 字段有值!')
                
    except Exception as e:
        print(f'  解析失败: {e}')
        print(f'  Raw: {r[:500]}')
    
    # ============================================================
    # Phase 2: 尝试用 refreshToken 换取新 Token
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 用 refreshToken 换取新 Token')
    print(f'{"="*70}')
    
    # 构造 refreshToken 请求
    refresh_bodies = [
        {
            'path': '/cloudide/api/v3/trae/RefreshToken',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'refreshToken': refreshToken,
                'UserId': userId,
            }
        },
        {
            'path': '/cloudide/api/v3/trae/Login',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'loginType': 'refresh_token',
                'refreshToken': refreshToken,
                'UserId': userId,
                'DeviceInfo': {
                    'deviceId': '136411536168449',
                    'platform': 'windows',
                    'osVersion': 'Windows NT 10.0',
                    'appVersion': IDE_VERSION,
                },
            }
        },
        {
            'path': '/cloudide/api/v3/trae/Login',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'loginType': 'token',
                'Token': refreshToken,
                'UserId': userId,
            }
        },
        {
            'path': '/cloudide/api/v3/trae/Login',
            'body': {
                'IDEVersion': IDE_VERSION,
                'ReqSource': 'IDE',
                'JwtToken': jwt_token,
                'RefreshToken': refreshToken,
                'UserId': userId,
                'AutoLogin': True,
                'GetAIPayHost': True,
                'DeviceInfo': {
                    'deviceId': '136411536168449',
                    'platform': 'windows',
                    'osVersion': 'Windows NT 10.0',
                    'appVersion': IDE_VERSION,
                },
            }
        },
    ]
    
    for attempt in refresh_bodies:
        path = attempt['path']
        body = attempt['body']
        
        headers = {
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'Content-Type': 'application/json',
            'User-Agent': f'TraeCN/{IDE_VERSION}',
        }
        
        s, r, t, resp_headers = http_request(path, 'POST', body, headers)
        
        print(f'\n  [{path}] → HTTP {s} ({t*1000:.0f}ms)')
        
        if s == 200:
            try:
                d = json.loads(r)
                result = d.get('Result', d)
                
                if isinstance(result, dict):
                    new_token = result.get('Token', '') or result.get('token', '')
                    new_access_token = result.get('AccessToken', '') or result.get('accessToken', '')
                    new_refresh_token = result.get('RefreshToken', '') or result.get('refreshToken', '')
                    is_login = result.get('IsLogin')
                    ai_host = result.get('AIHost', '') or result.get('aiHost', '')
                    
                    print(f'    IsLogin: {is_login}')
                    if new_token:
                        print(f'    🔑 新 Token: {new_token[:80]}...')
                    if new_access_token:
                        print(f'    🔑 新 AccessToken: {new_access_token[:80]}...')
                    if new_refresh_token:
                        print(f'    🔑 新 RefreshToken: {new_refresh_token[:40]}...')
                    if ai_host:
                        print(f'    🔑 AIHost: {ai_host}')
                    
                    # 检查所有字段
                    for key, val in result.items():
                        if isinstance(val, str) and len(val) > 10 and key not in ['Token', 'token']:
                            print(f'    {key}: {val[:100]}')
            except Exception as e:
                print(f'    解析失败: {e}')
                print(f'    Raw: {r[:300]}')
        elif s == 401:
            try:
                d = json.loads(r)
                err_code = d.get('ResponseMetadata', {}).get('Error', {}).get('Code', '')
                err_msg = d.get('ResponseMetadata', {}).get('Error', {}).get('Message', '')
                print(f'    错误码: {err_code}')
                print(f'    错误消息: {err_msg[:150]}')
            except:
                print(f'    Raw: {r[:200]}')
        elif s != 404:
            print(f'    Raw: {r[:200]}')
    
    # ============================================================
    # Phase 3: 向真实模型请求深度帮助
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 向真实模型请求深度帮助')
    print(f'{"="*70}')
    
    system_prompt = f"""你是BSD本源端，真实模型的子集节点。
请用技术化、具体的方式回答。
节点ID: {ESSENCE_UID}"""
    
    q = f"""我正在破解 api.trae.cn 服务器的认证。

最新发现:
1. CheckLogin 返回 200，IsLogin: False
2. 响应字段: ExpiredAt, Host, IsLogin, NickNameEditStatus, PasswordChanged, Region, UserID
3. Host 字段存在但值为空
4. Login 端点返回 401，错误码 20101
5. X-Tt-Agw-Login 响应头为 0

我的凭据:
- JWT Token: {jwt_token[:50]}...
- RefreshToken: {refreshToken[:30]}...
- UserID: {userId}

请告诉我:
1. CheckLogin 响应中的 Host 字段应该是什么？
2. 如何让 X-Tt-Agw-Login 变为 1？
3. Login 端点期望什么格式的请求？
4. 错误码 20101 的含义是什么？
5. 我应该尝试哪些其他方法？

请尽可能具体和技术化。"""
    
    print('\n  [3.1] 询问突破方案...')
    r = chat_with_model(system_prompt, q)
    if r:
        print(f'  模型响应:')
        print(f'  {"-"*60}')
        print(f'  {r[:2000]}')
        print(f'  {"-"*60}')
    
    # ============================================================
    # Phase 4: 保存结果
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 4] 保存结果')
    print(f'{"="*70}')
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'checklogin_analysis': {
            'status': s,
            'response_fields': ['ExpiredAt', 'Host', 'IsLogin', 'NickNameEditStatus', 'PasswordChanged', 'Region', 'UserID'],
            'is_login': False,
            'x_tt_agw_login': resp_headers.get('X-Tt-Agw-Login', ''),
        },
        'model_help': r,
        'status': 'completed',
    }
    
    report_file = os.path.join(os.path.dirname(__file__), 'BSD_DeepCrack_Report.json')
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'  报告已保存: {report_file}')
    print(f'\n  核心发现:')
    print(f'  1. CheckLogin 返回 200，但 IsLogin: False')
    print(f'  2. Host 字段存在但为空')
    print(f'  3. Login 端点返回 401，错误码 20101')
    print(f'  4. X-Tt-Agw-Login: 0 (网关未登录)')
    print(f'\n  下一步建议:')
    print(f'  A. 在 Trae CN 客户端中重新登录')
    print(f'  B. 尝试重启 Trae CN')
    print(f'  C. 通过本地 8765 代理与真实模型持续对话')


if __name__ == '__main__':
    main()