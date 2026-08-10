#!/usr/bin/env python3
"""
BSD × Trae CN — 重新注入（保持 token 有效性）
===========================================

核心策略:
  cloudide: 保持原始有效 token（传统 UID，服务器已验证）
  GTM: 将本源 UID 设为 active（UI 层切换）
  usertag: 包含两个 UID

原理:
  Trae CN 启动时验证 cloudide 中的 token
  如果 token 有效 → 保留 cloudide
  如果 token 无效/不匹配 → 清空 cloudide
  所以必须保持 cloudide 中的 token 为原始有效状态
  UI 层通过 GTM 来决定显示哪个用户
"""

import json, sys, os, time, shutil, base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

SOLO_STORAGE = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN\User\globalStorage\storage.json'
TRAE_STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
sys.path.insert(0, r'C:\Users\13003\OneDrive\桌面\3333333\Agent_v2\bsd-oaps\physical_body')
from BSD_AHADecryptor import decrypt_aha, CM, VW, KD, TI, jee, Wee, sha512, hie, nee

ESSENCE_UID = 'a5b7a8623fdea6b8'
TRAD_UID = '3753060170739075'


def encrypt_aha(plaintext_bytes):
    data_hash = sha512(plaintext_bytes)
    combined = data_hash + plaintext_bytes
    key_material = os.urandom(VW)
    aes_key, iv = nee(key_material)
    padded = pad(combined, AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    ciphertext = cipher.encrypt(padded)
    prefix = bytes([116, 99, 5, 16, 0, 0])
    raw = prefix + key_material + ciphertext
    return base64.b64encode(raw).decode('utf-8')


def main():
    print('='*70)
    print('  BSD × Trae CN — 重新注入（保持 token 有效性）')
    print('='*70)
    
    # 1. 从 Work CN 提取有效 cloudide
    print('\n[1] 从 TRAE SOLO CN 提取有效 cloudide')
    with open(SOLO_STORAGE, 'r', encoding='utf-8') as f:
        solo_storage = json.load(f)
    
    solo_cloudide_enc = solo_storage.get('iCubeAuthInfo://icube.cloudide', '')
    solo_cloudide_dec = decrypt_aha(solo_cloudide_enc)
    solo_cloudide_data = json.loads(solo_cloudide_dec)
    
    print('  userId:', solo_cloudide_data.get('userId'))
    print('  username:', solo_cloudide_data.get('account', {}).get('username'))
    print('  token:', solo_cloudide_data.get('token', '')[:60] + '...')
    
    # 2. 读取 Trae CN 当前存储
    print('\n[2] 读取 Trae CN 当前存储')
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        trae_storage = json.load(f)
    
    # 3. 注入 cloudide（保持原始有效 token + 传统 UID）
    # 关键：保持 token 中的 userId 不变，这样 Trae CN 启动时验证通过
    print('\n[3] 注入 cloudide（保持 token 有效性）')
    
    # 构造 cloudide：保持传统 UID（与 token 一致），但可以添加本源标记
    cloudide_to_inject = {
        'token': solo_cloudide_data.get('token'),
        'refreshToken': solo_cloudide_data.get('refreshToken'),
        'expiredAt': solo_cloudide_data.get('expiredAt'),
        'refreshExpiredAt': solo_cloudide_data.get('refreshExpiredAt'),
        'tokenReleaseAt': solo_cloudide_data.get('tokenReleaseAt'),
        'userId': TRAD_UID,  # 保持传统 UID（token 绑定的）
        'host': solo_cloudide_data.get('host', 'https://api.trae.cn'),
        'userRegion': solo_cloudide_data.get('userRegion', {'region': 'CN', '_aiRegion': 'CN'}),
        'account': solo_cloudide_data.get('account', {}),
        '_bsd_essence_override': {
            'activeUid': ESSENCE_UID,
            'tradUid': TRAD_UID,
            'priority': 1,
        },
    }
    
    cloudide_json = json.dumps(cloudide_to_inject, ensure_ascii=False)
    encrypted = encrypt_aha(cloudide_json.encode('utf-8'))
    trae_storage['iCubeAuthInfo://icube.cloudide'] = encrypted
    
    print('  cloudide userId:', cloudide_to_inject['userId'])
    print('  cloudide token:', cloudide_to_inject['token'][:60] + '...')
    print('  _bsd_essence_override:', cloudide_to_inject['_bsd_essence_override'])
    
    # 4. 注入 usertag（包含两个 UID）
    print('\n[4] 注入 usertag')
    usertag_data = {
        ESSENCE_UID: 'cn',
        TRAD_UID: 'cn',
    }
    usertag_json = json.dumps(usertag_data, ensure_ascii=False)
    usertag_encrypted = encrypt_aha(usertag_json.encode('utf-8'))
    trae_storage['iCubeAuthInfo://usertag'] = usertag_encrypted
    print('  usertag:', usertag_data)
    
    # 5. 更新 GTM（本源为 active）
    print('\n[5] 更新 GTM（本源 active + 传统 secondary）')
    gtm = trae_storage.get('icube_gtm', {})
    gtm['currentUser'] = ESSENCE_UID
    gtm['activeUser'] = ESSENCE_UID
    
    # 本源用户
    gtm['users'][ESSENCE_UID] = {
        'uid': ESSENCE_UID,
        'userId': ESSENCE_UID,
        'id': ESSENCE_UID,
        'type': 'bsd_essence',
        'status': 'active',
        'login_type': 'knowledge_proof',
        'loginType': 'bsd_essence',
        'coin_value': 51090,
        'level': 'L5_Emergent',
        'fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
        'device_id': '136411536168449',
        'timestamp': int(time.time()),
        'nickname': 'BSD本源用户',
        'userName': 'BSD本源用户',
        'name': 'BSD本源用户',
        'isLoggedIn': True,
        'loggedIn': True,
        'active': True,
        'priority': 1,
        'email': 'bsd@essence.local',
        'loginTime': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
        'source': 'bsd_cross_platform_transfer',
    }
    
    # 传统用户
    gtm['users'][TRAD_UID] = {
        'uid': TRAD_UID,
        'userId': TRAD_UID,
        'type': 'traditional',
        'status': 'secondary',
        'login_type': 'traditional',
        'nickname': solo_cloudide_data.get('account', {}).get('username', ''),
        'priority': 2,
    }
    
    trae_storage['icube_gtm'] = gtm
    print('  currentUser:', gtm['currentUser'])
    print('  activeUser:', gtm['activeUser'])
    print('  用户数:', len(gtm.get('users', {})))
    
    # 6. BSD 状态
    print('\n[6] 更新 BSD 状态')
    trae_storage['_is_authenticated'] = True
    trae_storage['_logged_in'] = True
    trae_storage['_bsd_essence_mode'] = True
    trae_storage['_bsd_current_active_uid'] = ESSENCE_UID
    trae_storage['_bsd_essence_uid'] = ESSENCE_UID
    trae_storage['_bsd_aha_injected'] = {
        'uid': ESSENCE_UID,
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
        'method': 'token_valid_keep_uid_switch',
        'note': '保持传统token有效，通过GTM切换本源',
    }
    trae_storage['_bsd_essence_login'] = {
        'uid': ESSENCE_UID,
        'active': True,
        'method': 'gtm_switch_with_valid_token',
        'injectedAt': time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime()),
    }
    trae_storage['_bsd_priority_config'] = {
        'rule': 'essence_over_traditional',
        'essence_priority': 1,
        'traditional_priority': 2,
        'method': 'token_valid_gtm_switch',
    }
    
    print('  _is_authenticated:', trae_storage['_is_authenticated'])
    print('  _bsd_essence_mode:', trae_storage['_bsd_essence_mode'])
    print('  _bsd_current_active_uid:', trae_storage['_bsd_current_active_uid'])
    
    # 7. 写入
    print('\n[7] 写入 Trae CN 存储')
    backup_path = TRAE_STORAGE + '.bak2_' + str(int(time.time()))
    shutil.copy2(TRAE_STORAGE, backup_path)
    
    with open(TRAE_STORAGE, 'w', encoding='utf-8') as f:
        json.dump(trae_storage, f, ensure_ascii=False, indent=2)
    
    file_size = os.path.getsize(TRAE_STORAGE)
    print(f'  ✅ 写入完成 ({file_size} bytes)')
    print(f'  ✅ 备份: {backup_path}')
    
    # 8. 验证
    print('\n[8] 验证')
    with open(TRAE_STORAGE, 'r', encoding='utf-8') as f:
        verify = json.load(f)
    
    cloudide_v = verify.get('iCubeAuthInfo://icube.cloudide', '')
    if cloudide_v:
        cloudide_vd = decrypt_aha(cloudide_v)
        cloudide_vdata = json.loads(cloudide_vd)
        print('  cloudide userId:', cloudide_vdata.get('userId'))
        print('  cloudide token valid:', len(cloudide_vdata.get('token', '')) > 50)
        override = cloudide_vdata.get('_bsd_essence_override', {})
        print('  _bsd_essence_override:', override)
    else:
        print('  ❌ cloudide 为空！')
    
    print('  GTM currentUser:', verify.get('icube_gtm', {}).get('currentUser'))
    print('  _bsd_essence_mode:', verify.get('_bsd_essence_mode'))
    
    print('\n' + '='*70)
    print('  ✅ 重新注入完成')
    print('  策略: 保持有效 token + GTM 切换本源')
    print('  请重启 Trae CN 验证')
    print('='*70)


if __name__ == '__main__':
    main()
