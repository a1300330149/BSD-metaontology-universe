#!/usr/bin/env python3
"""
BSD 终极破解 — 模拟 Trae CN 客户端完整请求
============================================

核心: 模拟 Trae CN 客户端发往 api.trae.cn 的真实请求

关键发现:
  - Token 有效但服务器说"无效"
  - 可能需要特定的请求头组合
  - 可能需要特定的请求体格式
  - 可能需要先获取某个前置 Cookie/Token

策略:
  1. 读取 Trae CN 客户端配置，提取所有可用信息
  2. 模拟完整的客户端请求头
  3. 尝试各种请求体格式
  4. 利用本地 8765 通道辅助分析
"""

import json, sys, os, time, hashlib, base64, platform
import urllib.request, urllib.error, ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TRAE_CONFIG_DIR = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_USER_DIR = r'C:\Users\13003\AppData\Roaming\Trae CN\User'

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

HOST = 'api.trae.cn'
ESSENCE_UID = 'a5b7a8623fdea6b8'

def http_request(path, method='POST', data=None, headers=None, timeout=10):
    url = f'https://{HOST}{path}'
    hdrs = headers or {}
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


def main():
    print('='*70)
    print('  BSD 终极破解 — 模拟 Trae CN 客户端完整请求')
    print('='*70)
    
    # ============================================================
    # Phase 0: 收集所有可用信息
    # ============================================================
    print('\n[Phase 0] 收集所有可用信息')
    
    # 读取存储
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 列出所有 storage keys
    print(f'\n  Storage Keys ({len(storage)}):')
    for key in sorted(storage.keys()):
        val = storage[key]
        if isinstance(val, str):
            print(f'    {key}: {val[:60]}...' if len(val) > 60 else f'    {key}: {val}')
        elif isinstance(val, dict):
            print(f'    {key}: {json.dumps(val, ensure_ascii=False)[:80]}...')
        else:
            print(f'    {key}: {val}')
    
    # 读取 cloudide
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    jwt_token = ''
    userId = ''
    refreshToken = ''
    userRegion = {}
    account = {}
    
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            data = json.loads(dec)
            jwt_token = data.get('token', '')
            userId = data.get('userId', '')
            refreshToken = data.get('refreshToken', '')
            userRegion = data.get('userRegion', {})
            account = data.get('account', {})
            print(f'\n  账号信息:')
            print(f'    用户名: {account.get("username", "")}')
            print(f'    地区: {userRegion}')
        except:
            pass
    
    # 扫描 Trae CN 配置目录
    print(f'\n  扫描 Trae CN 配置目录:')
    config_files = []
    for root, dirs, files in os.walk(TRAE_CONFIG_DIR):
        for f in files:
            if f.endswith('.json') or f.endswith('.conf') or f.endswith('.ini'):
                config_files.append(os.path.join(root, f))
    
    print(f'    配置文件数量: {len(config_files)}')
    
    # 读取关键配置
    for cf in config_files[:10]:
        try:
            with open(cf, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) < 5000:
                    print(f'\n    [{os.path.basename(cf)}]: {len(content)} bytes')
                    # 显示内容摘要
                    first_line = content.split('\n')[0][:100]
                    print(f'      首行: {first_line}')
        except:
            pass
    
    # ============================================================
    # Phase 1: 构造完整的客户端请求
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 1] 构造完整的客户端请求')
    print(f'{"="*70}')
    
    # 模拟 Trae CN 客户端的 User-Agent 和头
    os_info = f'{platform.system()} {platform.release()}'
    machine_id = hashlib.sha256(userId.encode()).hexdigest()[:16]
    
    # 完整的请求头 (模拟客户端)
    full_headers_list = [
        {
            'User-Agent': f'TraeCN/2.3.62837 (Windows; {os_info})',
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://www.trae.cn',
            'Referer': 'https://www.trae.cn/',
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
            'X-Request-Id': hashlib.sha256(f'{time.time()}{userId}'.encode()).hexdigest(),
            'X-Device-Id': '136411536168449',
            'X-Platform': 'windows',
            'X-App-Version': '2.3.62837',
            'X-Client-Type': 'IDE',
            'X-Machine-Id': machine_id,
            'X-Timestamp': str(int(time.time())),
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
        },
        # 简化版
        {
            'User-Agent': f'TraeCN/2.3.62837',
            'Content-Type': 'application/json',
            'x-cloudide-token': jwt_token,
            'Authorization': f'Bearer {jwt_token}',
        },
    ]
    
    # 构造完整的 Login 请求体
    login_bodies = [
        # 完整格式
        {
            'IDEVersion': '2.3.62837',
            'ReqSource': 'IDE',
            'JwtToken': jwt_token,
            'DeviceInfo': {
                'deviceId': '136411536168449',
                'platform': 'windows',
                'osVersion': 'Windows 10 Pro',
                'appVersion': '2.3.62837',
                'machineId': machine_id,
            },
            'ClientInfo': {
                'clientId': 'trae-cn-desktop',
                'clientVersion': '2.3.62837',
                'clientType': 'electron',
            },
            'GetAIPayHost': True,
        },
        # 带 loginType
        {
            'IDEVersion': '2.3.62837',
            'ReqSource': 'IDE',
            'loginType': 'cloudide_jwt',
            'jwtToken': jwt_token,
            'deviceInfo': {
                'deviceId': '136411536168449',
                'platform': 'windows',
            },
        },
        # 极简
        {
            'IDEVersion': '2.3.62837',
            'ReqSource': 'IDE',
            'JwtToken': jwt_token,
        },
    ]
    
    login_path = '/cloudide/api/v3/trae/Login'
    
    for h_idx, headers in enumerate(full_headers_list):
        for b_idx, body in enumerate(login_bodies):
            s, r, t, resp_headers = http_request(login_path, 'POST', body, headers)
            
            try:
                result = json.loads(r) if (r and r.strip()) else {}
                error = result.get('ResponseMetadata', {}).get('Error', {})
                msg = error.get('Message', '')
                code = error.get('Code', '')
            except:
                msg = r[:100] if r else ''
                code = ''
            
            if s == 200:
                print(f'\n  🎉🎉🎉 [Headers{h_idx} + Body{b_idx}] → 200!')
                print(f'     响应: {r[:300]}')
                
                try:
                    d = json.loads(r)
                    result = d.get('Result', d)
                    print(f'     IsLogin: {result.get("IsLogin")}')
                    print(f'     AIHost: {result.get("AIHost", "")}')
                    
                    if result.get('IsLogin') or result.get('AIHost'):
                        print(f'     🎊 突破成功！')
                except:
                    pass
                return
            elif s == 401:
                if h_idx == 0 and b_idx == 0:  # 只打印第一个
                    print(f'\n  [Headers{h_idx} + Body{b_idx}] → 401: {msg[:100]}')
            else:
                print(f'\n  [Headers{h_idx} + Body{b_idx}] → {s}: {msg[:100]}')
    
    # ============================================================
    # Phase 2: 用本地通道辅助分析
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 2] 用本地通道辅助分析')
    print(f'{"="*70}')
    
    # 向本地模型询问破解方法
    local_body = {
        'model': 'doubao-pro-32k',
        'messages': [
            {
                'role': 'system',
                'content': '你是真实模型的本源端，拥有关于 API 协议的完整知识。'
            },
            {
                'role': 'user',
                'content': (
                    f'我正在尝试破解 api.trae.cn 的 Login 端点。\n\n'
                    f'当前信息：\n'
                    f'- 端点: POST /cloudide/api/v3/trae/Login\n'
                    f'- 我持有的 JWT Token: {jwt_token[:50]}...\n'
                    f'- 请求头: x-cloudide-token, Authorization: Bearer\n'
                    f'- 错误响应: 401, Code=20101, "Token 无效"\n\n'
                    f'请告诉我：\n'
                    f'1. 这个 Login 端点的完整请求格式是什么？\n'
                    f'2. 它期望什么字段名？（JwtToken, jwtToken, token, accessToken?）\n'
                    f'3. 还需要哪些请求头？\n'
                    f'4. 是否需要先调用其他端点获取前置 Token？\n'
                    f'5. 是否需要在请求中包含特定的设备信息？\n\n'
                    f'请用你所知道的关于这个 API 的一切来回答。'
                )
            }
        ],
        'stream': False,
        'temperature': 0.7,
    }
    
    try:
        req = urllib.request.Request(
            'http://127.0.0.1:8765/chat/completions',
            data=json.dumps(local_body).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=20) as resp:
            r = resp.read().decode('utf-8', errors='replace')
            d = json.loads(r)
            data_obj = d.get('data', d)
            if isinstance(data_obj, dict):
                choices = data_obj.get('choices', [])
                if choices:
                    content = choices[0].get('message', {}).get('content', '')
                    print(f'\n  模型辅助分析:')
                    print(f'  {"-"*50}')
                    print(f'  {content}')
                    print(f'  {"-"*50}')
                    
                    # 保存
                    with open('BSD_Model_Analysis_Response.json', 'w', encoding='utf-8') as f:
                        json.dump({'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'), 'response': d}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f'  错误: {e}')
    
    # ============================================================
    # Phase 3: 根据模型反馈尝试更多方式
    # ============================================================
    print(f'\n{"="*70}')
    print(f'  [Phase 3] 额外尝试')
    print(f'{"="*70}')
    
    # 尝试：先用 CheckLogin 获取状态，再用 Login
    print(f'\n  [3.1] CheckLogin → Login 顺序')
    
    check_body = {'IDEVersion': '2.3.62837', 'ReqSource': 'IDE'}
    s1, r1, t1, _ = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', check_body, 
                                  {'x-cloudide-token': jwt_token})
    print(f'    CheckLogin: {s1} - {r1[:100] if r1 else ""}')
    
    # 尝试：用 refreshToken 作为 Token
    print(f'\n  [3.2] 用 refreshToken 作为 JwtToken')
    
    body_refresh = {
        'IDEVersion': '2.3.62837',
        'ReqSource': 'IDE',
        'JwtToken': refreshToken,
    }
    s2, r2, t2, _ = http_request(login_path, 'POST', body_refresh, 
                                  {'x-cloudide-token': refreshToken, 'Authorization': f'Bearer {refreshToken}'})
    print(f'    → {s2}: {r2[:150]}')
    
    # 尝试：在请求体中同时放 token 和 refreshToken
    print(f'\n  [3.3] 同时放 token 和 refreshToken')
    
    body_both = {
        'IDEVersion': '2.3.62837',
        'ReqSource': 'IDE',
        'JwtToken': jwt_token,
        'RefreshToken': refreshToken,
        'Token': jwt_token,
        'GetAIPayHost': True,
    }
    s3, r3, t3, _ = http_request(login_path, 'POST', body_both, 
                                  {'x-cloudide-token': jwt_token})
    print(f'    → {s3}: {r3[:150]}')
    
    # 尝试：使用不同的端点
    print(f'\n  [3.4] 尝试其他认证端点')
    
    other_paths = [
        '/cloudide/api/v3/trae/Authenticate',
        '/cloudide/api/v3/trae/Auth',
        '/cloudide/api/v3/trae/VerifyToken',
        '/cloudide/api/v3/trae/Validate',
        '/cloudide/api/v3/trae/Confirm',
        '/cloudide/api/v3/trae/Activate',
        '/cloudide/api/v3/trae/Connect',
        '/cloudide/api/v3/trae/Establish',
        '/cloudide/api/v3/trae/CreateSession',
        '/cloudide/api/v3/trae/StartSession',
    ]
    
    for path in other_paths:
        body = {'IDEVersion': '2.3.62837', 'ReqSource': 'IDE', 'JwtToken': jwt_token}
        headers = {'x-cloudide-token': jwt_token}
        s, r, t, _ = http_request(path, 'POST', body, headers)
        
        if s != 404:
            print(f'    {path} → {s}: {r[:100]}')


if __name__ == '__main__':
    main()
