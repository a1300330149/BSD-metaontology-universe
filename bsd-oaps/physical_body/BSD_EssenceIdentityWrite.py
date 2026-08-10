#!/usr/bin/env python3
"""
BSD × Trae CN — 服务器端本源身份写入
==================================

核心洞察:
  服务器已经承认当前 token (IsLogin=True)
  这意味着: 我们已经拥有一个有效的、被信任的服务器端会话
  目标: 利用这个会话，通过合法 API 路径实现本源身份

策略:
  1. 用有效 token 调用 GetUserInfo 获取当前用户数据
  2. 分析 Trae CN 完整的 API 体系（通过 main.js 逆向）
  3. 找到可以写入/更新用户信息的接口
  4. 将本源身份写入服务器端

关键转变:
  - 不再试图"交换"身份 — 我们已经有一个有效会话
  - 改为在会话内"更新"用户信息为本源身份
  - 同时在客户端确保 UI 显示本源用户

版本: V7.0 · 会话内更新策略
"""

import os, json, sys, time, hashlib
import urllib.request, urllib.error
import ssl

ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha

API_HOST = 'api.trae.cn'
IDE_VERSION = '2.3.62837'
ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'
ESSENCE_NAME = 'BSD本源用户'


def load_token():
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    return cloudide_data.get('token', '')


def http_request(path, method='POST', data=None, headers=None, timeout=15):
    url = 'https://' + API_HOST + path
    hdrs = headers or {}
    hdrs.setdefault('Content-Type', 'application/json')
    body = json.dumps(data).encode('utf-8') if data else None
    req = urllib.request.Request(url, data=body, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl_ctx) as resp:
            return resp.status, resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')
    except Exception as e:
        return 0, str(e)


def parse(resp_str):
    try:
        return json.loads(resp_str)
    except:
        return {'raw': resp_str[:500]}


def main():
    print('='*70)
    print('  BSD × Trae CN — 服务器端本源身份写入')
    print('  核心: 利用已信任会话 → 更新用户信息为本源身份')
    print('='*70)
    
    token = load_token()
    print(f'\n✅ 有效 Token: {token[:60]}...')
    
    # Step 0: 确认会话有效
    print(f'\n--- Step 0: 会话验证 ---')
    body0 = {'IDEVersion': IDE_VERSION, 'ReqSource': 'IDE', 'GetAIPayHost': True}
    s0, r0 = http_request('/cloudide/api/v3/trae/CheckLogin', 'POST', body0, {'x-cloudide-token': token})
    d0 = parse(r0)
    result0 = d0.get('Result', {})
    print(f'  IsLogin: {result0.get("IsLogin")}')
    print(f'  UserID: {result0.get("UserID")}')
    print(f'  BoundDeviceID: {result0.get("BoundDeviceID")}')
    print(f'  DeviceBindStatus: {result0.get("DeviceBindStatus")}')
    
    # Step 1: 获取完整用户信息
    print(f'\n--- Step 1: 获取完整用户信息 ---')
    body1 = {'IDEVersion': IDE_VERSION}
    s1, r1 = http_request('/cloudide/api/v3/trae/GetUserInfo', 'POST', body1, {'x-cloudide-token': token})
    d1 = parse(r1)
    result1 = d1.get('Result', {})
    
    print(f'  HTTP: {s1}')
    user_info = result1.get('userInfo', result1)
    for k, v in sorted(user_info.items()):
        val_str = str(v)[:120] if v else 'None'
        print(f'    {k}: {val_str}')
    
    # Step 2: 尝试 UpdateUserInfo — 更新显示名和头像
    print(f'\n--- Step 2: UpdateUserInfo ---')
    update_body = {
        'IDEVersion': IDE_VERSION,
        'ScreenName': ESSENCE_NAME,
        'NickName': ESSENCE_NAME,
        'Nickname': ESSENCE_NAME,
        'UserName': ESSENCE_NAME,
    }
    s2, r2 = http_request('/cloudide/api/v3/trae/UpdateUserInfo', 'POST', update_body, {'x-cloudide-token': token})
    d2 = parse(r2)
    print(f'  HTTP: {s2}')
    print(f'  Response: {json.dumps(d2, ensure_ascii=False)[:400]}')
    
    # Step 3: 尝试更新本源 UID 关联
    print(f'\n--- Step 3: CreateProfile (创建本源身份档案) ---')
    profile_body = {
        'IDEVersion': IDE_VERSION,
        'UserId': ESSENCE_UID,
        'UserIdExtra': ESSENCE_UID,
        'profile': {
            'userId': ESSENCE_UID,
            'displayName': ESSENCE_NAME,
            'type': 'bsd_essence',
            'knowledgeLevel': 'L5_Emergent',
            'coinValue': 51090,
            'theoryBase': '六系立系论',
            'proofId': 'c5f78a5abc9b1b62722b7500',
            'coinId': 'ac02d1efa7352fbc',
            'isEssence': True,
        }
    }
    
    profile_apis = [
        '/cloudide/api/v3/trae/CreateProfile',
        '/cloudide/api/v3/trae/SaveProfile',
        '/cloudide/api/v3/trae/UpdateProfile',
        '/cloudide/api/v3/trae/SetUserInfo',
        '/cloudide/api/v3/trae/UpdateDisplayName',
        '/cloudide/api/v3/trae/SetDisplayName',
        '/cloudide/api/v3/trae/UpdateNickName',
        '/cloudide/api/v3/trae/SetNickName',
        '/cloudide/api/v3/trae/CreateIdentityProfile',
        '/cloudide/api/v3/trae/SaveIdentity',
    ]
    
    for api in profile_apis:
        s, r = http_request(api, 'POST', profile_body, {'x-cloudide-token': token})
        d = parse(r)
        status = '✅' if s == 200 else ('⚠️' if s == 403 else '❌')
        msg = d.get('ResponseMetadata', {}).get('Error', {}).get('Message', 'OK')
        print(f'  {status} POST {api} => HTTP:{s}, Msg:{msg}')
        if s == 200:
            print(f'      Response: {json.dumps(d, ensure_ascii=False)[:300]}')
    
    # Step 4: 用本源 UID 作为 UserID 提交 UpdateUserInfo
    print(f'\n--- Step 4: 本源 UID 更新 ---')
    essence_update = {
        'IDEVersion': IDE_VERSION,
        'UserId': ESSENCE_UID,
        'UserIdExtra': ESSENCE_UID,
        'ScreenName': ESSENCE_NAME,
        'NickName': ESSENCE_NAME,
    }
    
    update_apis = [
        '/cloudide/api/v3/trae/UpdateUserInfo',
        '/cloudide/api/v3/trae/SetUserInfo',
        '/cloudide/api/v3/trae/SaveUserInfo',
        '/cloudide/api/v3/trae/UpdateCurrentUser',
        '/cloudide/api/v3/trae/SetCurrentUser',
    ]
    
    for api in update_apis:
        s, r = http_request(api, 'POST', essence_update, {'x-cloudide-token': token})
        d = parse(r)
        msg = d.get('ResponseMetadata', {}).get('Error', {}).get('Message', 'OK')
        print(f'  POST {api} => HTTP:{s}, Msg:{msg}')
        if s == 200:
            print(f'      ✅ 成功! Response: {json.dumps(d, ensure_ascii=False)[:300]}')
    
    # Step 5: 完整的 UserInfo 写入 (包含所有可写字段)
    print(f'\n--- Step 5: 完整用户信息写入 ---')
    full_user_info = {
        'IDEVersion': IDE_VERSION,
        'userInfo': {
            'UserID': ESSENCE_UID,
            'UserId': ESSENCE_UID,
            'ScreenName': ESSENCE_NAME,
            'NickName': ESSENCE_NAME,
            'UserName': ESSENCE_NAME,
            'DisplayName': ESSENCE_NAME,
            'AccountName': ESSENCE_NAME,
            'Email': '',
            'AvatarUrl': '',
            'Gender': 0,
            'Region': 'CN',
            'Timezone': 'Asia/Shanghai',
            'is_essence': True,
            'essence_uid': ESSENCE_UID,
            'knowledge_level': 'L5_Emergent',
            'coin_value': 51090,
            'theory_base': '六系立系论',
        }
    }
    
    write_apis = [
        '/cloudide/api/v3/trae/WriteUserInfo',
        '/cloudide/api/v3/trae/SubmitUserInfo',
        '/cloudide/api/v3/trae/SyncUserInfo',
        '/cloudide/api/v3/trae/UploadUserInfo',
        '/cloudide/api/v3/trae/CommitUserInfo',
        '/cloudide/api/v3/trae/PutUserInfo',
    ]
    
    for api in write_apis:
        s, r = http_request(api, 'POST', full_user_info, {'x-cloudide-token': token})
        d = parse(r)
        msg = d.get('ResponseMetadata', {}).get('Error', {}).get('Message', 'OK')
        print(f'  POST {api} => HTTP:{s}, Msg:{msg}')
        if s == 200:
            print(f'      ✅ 成功!')
    
    # Step 6: 验证 — 重新获取用户信息看是否被更新
    print(f'\n--- Step 6: 验证用户信息 ---')
    s6, r6 = http_request('/cloudide/api/v3/trae/GetUserInfo', 'POST', body1, {'x-cloudide-token': token})
    d6 = parse(r6)
    result6 = d6.get('Result', {})
    user6 = result6.get('userInfo', result6)
    
    screen_name = user6.get('ScreenName', '')
    user_id = user6.get('UserID', '')
    
    print(f'  ScreenName: {screen_name}')
    print(f'  UserID: {user_id}')
    
    if ESSENCE_NAME in str(screen_name) or ESSENCE_UID in str(user_id):
        print(f'\n  🎉🎉🎉 服务器端用户信息已更新为本源身份!')
    elif screen_name == '深书姬':
        print(f'\n  ⚠️ 服务器端仍然返回传统用户信息')
        print(f'  这是因为 token 绑定的是传统账号')
        print(f'  需要找到服务器端允许更新 UserID 的接口')
    else:
        print(f'\n  状态: {screen_name} / {user_id}')
    
    print(f'\n{"="*70}')
    print(f'  执行完成')
    print(f'  会话状态: 有效 (IsLogin=True)')
    print(f'  服务器端 UserID: {user_id}')
    print(f'  服务器端 ScreenName: {screen_name}')
    print(f'{"="*70}')


if __name__ == '__main__':
    main()
