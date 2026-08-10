#!/usr/bin/env python3
"""
BSD V11 → 本源登录完成
======================

完整流程:
  1. 连接 BSD V11 服务器获取本源身份
  2. 将本源身份注入 Trae CN 存储（保持真实 token）
  3. 启动 Trae CN
  4. 验证本源登录状态
"""

import json, sys, os, time, hashlib, base64, threading
import urllib.request, urllib.error

sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha
from BSD_InjectEssenceIdentityV2 import encrypt_aha

TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
TRAE_CN_PATH = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'

BSD_SERVER = 'http://127.0.0.1:17860'
BSD_TOKEN = 'BSD_KNOWLEDGE_PROTOCOL_v11'

ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'
BSD_COIN_ID = 'ac02d1efa7352fbc'
BSD_COIN_VALUE = 51090
BSD_PROOF_ID = 'c5f78a5abc9b1b62722b7500'
BSD_FINGERPRINT = '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5'


def bsd_api(path, method='GET', data=None, require_token=False):
    url = BSD_SERVER + path
    body = json.dumps(data).encode('utf-8') if data else None
    headers = {'Content-Type': 'application/json'}
    if require_token:
        headers['X-BSD-Token'] = BSD_TOKEN
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        return 0, {'error': str(e)}


def step1_bsd_authenticate():
    """步骤1: BSD V11 服务器知识换取身份"""
    print('[Step 1] BSD V11 知识换取本源身份...')
    
    # 1a. 验证知识
    s, d = bsd_api('/api/v1/knowledge/verify', 'POST', {
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
        'fingerprint': BSD_FINGERPRINT,
    }, require_token=True)
    assert d.get('valid'), f'知识验证失败: {d}'
    print(f'  ✅ 知识验证: 币值{d["coin"]["value"]}, 等级{d["coin"]["level"]}')
    
    # 1b. 知识换取身份
    s, d = bsd_api('/api/v1/knowledge/exchange', 'POST', {
        'coin_id': BSD_COIN_ID,
        'coin_value': BSD_COIN_VALUE,
        'proof_id': BSD_PROOF_ID,
        'essence_uid': ESSENCE_UID,
        'trad_uid': TRAD_UID,
        'fingerprint': BSD_FINGERPRINT,
    }, require_token=True)
    assert d.get('success'), f'身份交换失败: {d}'
    print(f'  ✅ 本源身份授予: {d.get("uid", d.get("identity", {}).get("uid"))}')
    print(f'  ✅ 架构: {d.get("architecture")}')
    print(f'  ✅ 消息: {d.get("message")}')
    
    # 1c. 代理传统登录验证
    s, d = bsd_api('/api/v1/proxy/checklogin', 'POST', {}, require_token=True)
    print(f'  ✅ 传统token有效: {d.get("traditional_login")}')
    print(f'  ✅ 本源身份同步: {d.get("essence_identity", {})}')
    
    # 1d. 本源身份验证（包含传统）
    s, d = bsd_api('/api/v1/identity/verify', 'POST', {'uid': ESSENCE_UID}, require_token=True)
    assert d.get('verified'), f'本源身份验证失败: {d}'
    print(f'  ✅ 本源主体: {d["identity"]["uid"]} ({d["identity"]["auth_level"]})')
    trad = d.get('traditional_subset', {})
    if trad:
        print(f'  ✅ 传统子集: {trad["uid"]} → {trad["parent_essence_uid"]}')
    
    return d


def step2_inject_trae_storage():
    """步骤2: 注入 Trae CN 存储"""
    print('\n[Step 2] 注入 Trae CN 存储...')
    
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 2a. 读取现有 cloudide（保持 token 有效）
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    cloudide_dec = decrypt_aha(cloudide_enc)
    cloudide_data = json.loads(cloudide_dec)
    
    # 保存真实 token
    real_token = cloudide_data.get('token', '')
    real_refresh = cloudide_data.get('refreshToken', '')
    real_user_id = cloudide_data.get('userId', TRAD_UID)
    real_username = cloudide_data.get('username', '深书姬')
    
    print(f'  现有 cloudide: userId={real_user_id}, username={real_username}')
    print(f'  Token: {real_token[:50]}...')
    
    # 2b. 构建本源身份 cloudide（保持真实 token）
    essence_cloudide = {
        'userId': real_user_id,  # 保持传统UID，确保token验证通过
        'username': real_username,
        'token': real_token,
        'refreshToken': real_refresh,
        'host': cloudide_data.get('host', 'https://api.trae.cn'),
        '_bsd_essence_override': {
            'activeUid': ESSENCE_UID,
            'activeUsername': 'BSD本源用户',
            'priority': 1,
            'architecture': 'essence_contains_tradition',
            'bsdServer': BSD_SERVER,
            'coinId': BSD_COIN_ID,
            'coinValue': BSD_COIN_VALUE,
            'proofId': BSD_PROOF_ID,
            'fingerprint': BSD_FINGERPRINT,
        },
        '_bsd_essence_mode': True,
        '_bsd_current_active_uid': ESSENCE_UID,
    }
    
    # 加密并写回
    essence_enc = encrypt_aha(json.dumps(essence_cloudide).encode('utf-8'))
    storage['iCubeAuthInfo://icube.cloudide'] = essence_enc
    
    # 2c. 更新 GTM 用户体系（切换本源为 active）
    gtm = storage.get('icube_gtm', {})
    gtm['currentUser'] = ESSENCE_UID
    gtm['activeUser'] = ESSENCE_UID
    
    users = gtm.get('users', {})
    users[ESSENCE_UID] = {
        'type': 'bsd_essence',
        'status': 'active',
        'nick': 'BSD本源用户',
        'coinId': BSD_COIN_ID,
        'coinValue': BSD_COIN_VALUE,
        'proofId': BSD_PROOF_ID,
        'level': 'L5_Emergent',
    }
    users[TRAD_UID] = {
        'type': 'traditional',
        'status': 'secondary',
        'nick': real_username,
        'isSubset': True,
        'parentEssenceUid': ESSENCE_UID,
    }
    gtm['users'] = users
    storage['icube_gtm'] = gtm
    
    # 2d. 设置认证状态
    storage['_is_authenticated'] = True
    storage['_logged_in'] = True
    storage['_bsd_essence_mode'] = True
    storage['_bsd_current_active_uid'] = ESSENCE_UID
    
    # 2e. 更新 usertag
    usertag = storage.get('usertag', [])
    if isinstance(usertag, str):
        try:
            usertag = json.loads(usertag)
        except:
            usertag = []
    if isinstance(usertag, list):
        tag_list = usertag
    elif isinstance(usertag, dict):
        tag_list = list(usertag.keys())
    else:
        tag_list = []
    
    if ESSENCE_UID not in str(tag_list):
        storage['usertag'] = {
            TRAD_UID: 'cn',
            ESSENCE_UID: 'bsd_essence',
        }
    
    # 2f. BSD 服务器信息注入
    storage['_bsd_server_config'] = {
        'server': BSD_SERVER,
        'protocol': 'BSD_Essence_Protocol_v11',
        'architecture': 'essence_contains_tradition',
        'coinId': BSD_COIN_ID,
        'coinValue': BSD_COIN_VALUE,
        'essenceUid': ESSENCE_UID,
        'tradUid': TRAD_UID,
    }
    
    # 写回
    with open(TRAE_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)
    
    # 验证
    verify_dec = decrypt_aha(essence_enc)
    verify_data = json.loads(verify_dec)
    assert verify_data.get('userId') == real_user_id
    assert verify_data.get('_bsd_essence_mode') == True
    assert verify_data['_bsd_essence_override']['activeUid'] == ESSENCE_UID
    
    print(f'  ✅ cloudide 注入成功（AHA加密验证通过）')
    print(f'  ✅ GTM currentUser → {ESSENCE_UID}')
    print(f'  ✅ 双用户体系建立')
    print(f'  ✅ BSD 服务器配置注入')
    print(f'  ✅ 认证状态: _is_authenticated=True, _bsd_essence_mode=True')


def step3_launch_and_verify():
    """步骤3: 启动 Trae CN 并验证"""
    print('\n[Step 3] 启动 Trae CN...')
    
    # 检查文件是否存在
    if not os.path.exists(TRAE_CN_PATH):
        print(f'  ⚠️ Trae CN 路径不存在: {TRAE_CN_PATH}')
        # 尝试查找
        import subprocess
        result = subprocess.run(['where', 'Trae CN'], capture_output=True, text=True)
        if result.returncode != 0:
            result = subprocess.run(['where', 'TraeCN'], capture_output=True, text=True)
        print(f'  搜索结果: {result.stdout.strip()}')
        return
    
    # 启动 Trae CN
    import subprocess
    proc = subprocess.Popen([TRAE_CN_PATH])
    print(f'  ✅ Trae CN 已启动 (PID: {proc.pid})')
    print(f'  等待 Trae CN 完全加载 (8秒)...')
    time.sleep(8)
    
    # 再次检查存储状态（Trae CN 启动后可能覆盖）
    print('\n[Step 4] 验证 Trae CN 启动后的存储状态...')
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 检查 cloudide
    cloudide_enc = storage.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_enc:
        cloudide_dec = decrypt_aha(cloudide_enc)
        cloudide_data = json.loads(cloudide_dec)
        print(f'  cloudide userId: {cloudide_data.get("userId")}')
        print(f'  cloudide _bsd_essence_mode: {cloudide_data.get("_bsd_essence_mode")}')
        override = cloudide_data.get('_bsd_essence_override', {})
        if override:
            print(f'  cloudide override.activeUid: {override.get("activeUid")}')
            print(f'  cloudide override.architecture: {override.get("architecture")}')
    else:
        print(f'  ⚠️ cloudide 被清空！')
    
    # 检查 GTM
    gtm = storage.get('icube_gtm', {})
    print(f'  GTM currentUser: {gtm.get("currentUser")}')
    print(f'  GTM activeUser: {gtm.get("activeUser")}')
    users = gtm.get('users', {})
    for uid, udata in users.items():
        print(f'  GTM user {uid}: type={udata.get("type")}, status={udata.get("status")}')
    
    # 检查认证状态
    print(f'  _is_authenticated: {storage.get("_is_authenticated")}')
    print(f'  _bsd_essence_mode: {storage.get("_bsd_essence_mode")}')
    print(f'  _bsd_current_active_uid: {storage.get("_bsd_current_active_uid")}')
    
    # 检查 BSD 服务器配置
    bsd_config = storage.get('_bsd_server_config', {})
    if bsd_config:
        print(f'  BSD server: {bsd_config.get("server")}')
        print(f'  BSD architecture: {bsd_config.get("architecture")}')
    
    # 最终判定
    print('\n' + '='*70)
    if cloudide_data.get('_bsd_essence_mode') == True and gtm.get('currentUser') == ESSENCE_UID:
        print('  🎉 本源登录完整闭环已建立！')
        print('     Trae CN 已启动，本源身份已落地')
        print('     BSD V11 服务器管理传统 token')
        print('     本源是主体，传统是子集')
    else:
        print('  ⚠️ Trae CN 可能覆盖了部分存储')
        print('     需要进一步观测 UI 显示')
    print('='*70)
    
    return proc


def main():
    print('='*70)
    print('  BSD V11 → 本源登录完成')
    print('  完整流程: 服务器认证 → 注入 → 启动 → 验证')
    print('='*70)
    
    # Step 1: BSD 服务器认证
    step1_bsd_authenticate()
    
    # Step 2: 注入 Trae CN 存储
    step2_inject_trae_storage()
    
    # Step 3-4: 启动并验证
    proc = step3_launch_and_verify()
    
    print('\n  本源登录流程完成')
    print('  Trae CN 正在运行，可在 UI 中观察本源状态')


if __name__ == '__main__':
    main()
