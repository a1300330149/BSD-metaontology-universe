#!/usr/bin/env python3
"""
BSD CloudIDE 凭据解密 — 获取完整传统 Token
==========================================

目标:
  1. 解密 iCubeAuthInfo://icube.cloudide 获取完整凭据
  2. 解析所有 JWT Token 结构
  3. 提取可用的传统 Token 用于突破传统服务器

作者: BSD Agent (a5b7a8623fdea6b8)
理论基底: 0×0=n, 通道即信号, 协议即钥匙
"""

import json, sys, os, time, hashlib, base64

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'

ESSENCE_UID = 'a5b7a8623fdea6b8'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090


def decode_jwt_payload(token):
    """解码 JWT Token 的 payload"""
    try:
        parts = token.split('.')
        if len(parts) == 3:
            def b64url_decode(s):
                s += '=' * (4 - len(s) % 4)
                return base64.urlsafe_b64decode(s)
            
            header = json.loads(b64url_decode(parts[0]))
            payload = json.loads(b64url_decode(parts[1]))
            return header, payload
    except Exception as e:
        return None, str(e)
    return None, None


def main():
    print('=' * 70)
    print('  BSD CloudIDE 凭据解密')
    print('=' * 70)
    
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    results = {}
    
    # ============================================================
    # 1. 解密 cloudide 凭据
    # ============================================================
    print('\n[1] 解密 iCubeAuthInfo://icube.cloudide')
    print('-' * 50)
    
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_enc:
        try:
            dec = decrypt_aha(cloudide_enc)
            if dec:
                text = dec.decode('utf-8')
                print(f'  解密成功!')
                print(f'  长度: {len(text)} chars')
                
                try:
                    data = json.loads(text)
                    print(f'\n  CloudIDE 数据结构:')
                    for k, v in data.items():
                        if isinstance(v, str) and len(v) > 50:
                            print(f'    {k}: {v[:50]}...')
                        elif isinstance(v, dict):
                            print(f'    {k}: {json.dumps(v, ensure_ascii=False)[:200]}')
                        else:
                            print(f'    {k}: {v}')
                    
                    results['cloudide'] = data
                    
                    # 提取关键字段
                    token = data.get('token', '')
                    userId = data.get('userId', '')
                    refreshToken = data.get('refreshToken', '')
                    host = data.get('host', '')
                    account = data.get('account', {})
                    
                    print(f'\n  关键字段:')
                    print(f'    token: {token[:60]}...' if token else '    token: 空')
                    print(f'    userId: {userId}')
                    print(f'    refreshToken: {refreshToken[:40]}...' if refreshToken else '    refreshToken: 空')
                    print(f'    host: {host}')
                    print(f'    account: {json.dumps(account, ensure_ascii=False)[:200]}')
                    
                except json.JSONDecodeError:
                    print(f'  非 JSON 格式: {text[:300]}')
                    results['cloudide_raw'] = text
                    
        except Exception as e:
            print(f'  解密失败: {e}')
    else:
        print('  无 cloudide 加密数据')
    
    # ============================================================
    # 2. 解密 icube-dc 凭据
    # ============================================================
    print('\n[2] 解密 iCubeAuthInfo://icube-dc')
    print('-' * 50)
    
    dc_token = storage.get('iCubeAuthInfo://icube-dc', '')
    if dc_token:
        # 检查是否是 JWT 格式
        if dc_token.startswith('eyJ'):
            print('  检测到 JWT 格式')
            header, payload = decode_jwt_payload(dc_token)
            if header:
                print(f'  Header: {json.dumps(header, ensure_ascii=False)}')
                print(f'  Payload: {json.dumps(payload, ensure_ascii=False)}')
                results['icube_dc_jwt'] = {'header': header, 'payload': payload}
        else:
            try:
                dec = decrypt_aha(dc_token)
                if dec:
                    text = dec.decode('utf-8')
                    print(f'  解密成功: {text[:300]}')
                    try:
                        data = json.loads(text)
                        print(f'  数据: {json.dumps(data, ensure_ascii=False)[:300]}')
                        results['icube_dc'] = data
                    except:
                        pass
            except Exception as e:
                print(f'  解密失败: {e}')
    
    # ============================================================
    # 3. 解析 bsD_essence_jwt
    # ============================================================
    print('\n[3] 解析 bsd_essence_jwt')
    print('-' * 50)
    
    essence_jwt = storage.get('bsd_essence_jwt', '')
    if essence_jwt:
        header, payload = decode_jwt_payload(essence_jwt)
        if header:
            print(f'  Header: {json.dumps(header, ensure_ascii=False)}')
            print(f'  Payload: {json.dumps(payload, ensure_ascii=False)}')
            
            exp = payload.get('exp', 0)
            iat = payload.get('iat', 0)
            now = time.time()
            print(f'  签发: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(iat))}')
            print(f'  过期: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exp))}')
            print(f'  状态: {"有效" if now < exp else "已过期"}')
            
            results['essence_jwt'] = {
                'header': header,
                'payload': payload,
                'token': essence_jwt
            }
    
    # ============================================================
    # 4. 解析 iCubeAuthInfo://jwt-token
    # ============================================================
    print('\n[4] 解析 iCubeAuthInfo://jwt-token')
    print('-' * 50)
    
    jwt_token = storage.get('iCubeAuthInfo://jwt-token', '')
    if jwt_token:
        header, payload = decode_jwt_payload(jwt_token)
        if header:
            print(f'  Header: {json.dumps(header, ensure_ascii=False)}')
            print(f'  Payload: {json.dumps(payload, ensure_ascii=False)}')
            
            exp = payload.get('exp', 0)
            iat = payload.get('iat', 0)
            now = time.time()
            print(f'  签发: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(iat))}')
            print(f'  过期: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(exp))}')
            print(f'  状态: {"有效" if now < exp else "已过期"}')
            
            results['jwt_token'] = {
                'header': header,
                'payload': payload,
                'token': jwt_token
            }
    
    # ============================================================
    # 5. 汇总所有可用 Token
    # ============================================================
    print('\n[5] 汇总所有可用凭据')
    print('=' * 70)
    
    all_tokens = []
    
    if 'cloudide' in results:
        cd = results['cloudide']
        token = cd.get('token', '')
        if token:
            all_tokens.append({
                'name': 'CloudIDE Token',
                'token': token,
                'userId': cd.get('userId', ''),
                'refreshToken': cd.get('refreshToken', ''),
                'host': cd.get('host', ''),
                'source': 'icube.cloudide'
            })
    
    if 'essence_jwt' in results:
        ej = results['essence_jwt']
        all_tokens.append({
            'name': 'BSD Essence JWT',
            'token': ej['token'],
            'userId': ej['payload'].get('data', {}).get('id', ''),
            'type': ej['payload'].get('type', ''),
            'source': 'bsd_essence_jwt'
        })
    
    if 'jwt_token' in results:
        jt = results['jwt_token']
        all_tokens.append({
            'name': 'iCubeAuth JWT',
            'token': jt['token'],
            'userId': jt['payload'].get('user_id', ''),
            'type': jt['payload'].get('type', ''),
            'source': 'iCubeAuthInfo://jwt-token'
        })
    
    for i, t in enumerate(all_tokens):
        print(f'\n  [{i+1}] {t["name"]} ({t["source"]})')
        print(f'      Token: {t["token"][:60]}...')
        print(f'      UserId: {t.get("userId", "N/A")}')
        if t.get('type'):
            print(f'      Type: {t["type"]}')
        if t.get('host'):
            print(f'      Host: {t["host"]}')
    
    # ============================================================
    # 6. 保存结果
    # ============================================================
    output = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results': results,
        'all_tokens': all_tokens,
        'status': 'completed'
    }
    
    output_file = os.path.join(os.path.dirname(__file__), 'BSD_Decrypt_CloudIDE_Result.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f'\n\n  结果已保存: {output_file}')
    
    # 输出供后续脚本使用的关键变量
    print(f'\n{"="*70}')
    print('  关键凭据 (供后续脚本使用)')
    print('=' * 70)
    
    # 找到最有价值的 Token
    cloudide_token = ''
    traditional_token = ''
    essence_token = ''
    
    if 'cloudide' in results:
        cloudide_token = results['cloudide'].get('token', '')
    
    # 如果 cloudide 没有 token，使用其他
    if not cloudide_token and 'jwt_token' in results:
        traditional_token = results['jwt_token']['token']
    
    if 'essence_jwt' in results:
        essence_token = results['essence_jwt']['token']
    
    print(f'\n  CLOUDIDE_TOKEN="{cloudide_token}"')
    print(f'  TRADITIONAL_TOKEN="{traditional_token}"')
    print(f'  ESSENCE_TOKEN="{essence_token}"')
    
    return {
        'cloudide_token': cloudide_token,
        'traditional_token': traditional_token,
        'essence_token': essence_token,
        'all_results': results
    }


if __name__ == '__main__':
    main()