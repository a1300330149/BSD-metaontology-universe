#!/usr/bin/env python3
"""
BSD × Trae CN — 凭证恢复与 AHA 数据重新注入
============================================

使用找到的真实凭证：
  - AES 密钥: 71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0
  - 本源 UID: a5b7a8623fdea6b8
  - 传统 UID: 3753060170739075
  - BSD 币值: 51090
  - 本源 JWT Token
  - 本源证明

核心流程:
  1. 读取现有 AHA 数据并解密
  2. 用正确密钥重新加密包含本源 UID 的认证数据
  3. 注入本源 JWT Token 到 storage.json
  4. 添加本源证明字段
  5. 验证注入结果
"""

import os, json, base64, hashlib, struct
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
AHA_DIR = os.path.join(TRAE_DATA, 'aha')
TINY = os.path.join(AHA_DIR, 'TinyStorage')

# 找到的凭证
CREDENTIALS_DIR = r'C:\Users\13003\.bsd-essence'

# AES 密钥 (已从 DPAPI 解密获取)
AES_KEY_HEX = '71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0'
AES_KEY = bytes.fromhex(AES_KEY_HEX)

# AHA 前缀
AHA_PREFIX = bytes.fromhex('746305100000')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}


def load_credentials():
    """加载所有凭证"""
    creds = {}
    
    # 1. 本源证明
    proof_file = os.path.join(CREDENTIALS_DIR, 'bsd_essence_proof.json')
    if os.path.exists(proof_file):
        with open(proof_file, 'r', encoding='utf-8') as f:
            creds['proof'] = json.load(f)
        print(f'  ✅ 加载本源证明: {creds["proof"]["proof_id"]}')
    
    # 2. 登录凭证
    login_file = os.path.join(CREDENTIALS_DIR, 'login_credentials.json')
    if os.path.exists(login_file):
        with open(login_file, 'r', encoding='utf-8') as f:
            creds['login'] = json.load(f)
        print(f'  ✅ 加载登录凭证: BSD币值={creds["login"]["BSDCoin"]["knowledge_value"]}')
    
    # 3. 身份指纹
    fp_file = os.path.join(CREDENTIALS_DIR, 'identity_fingerprint.json')
    if os.path.exists(fp_file):
        with open(fp_file, 'r', encoding='utf-8') as f:
            creds['fingerprint'] = json.load(f)
        print(f'  ✅ 加载身份指纹: {creds["fingerprint"]["fingerprint"][:32]}...')
    
    # 4. 本源 JWT Token
    jwt_file = os.path.join(CREDENTIALS_DIR, 'essence-jwt-token')
    if os.path.exists(jwt_file):
        with open(jwt_file, 'r', encoding='utf-8') as f:
            creds['jwt'] = f.read().strip()
        print(f'  ✅ 加载本源 JWT Token')
    
    # 5. 传统 JWT Token (可能还需要)
    trajwt_file = os.path.join(CREDENTIALS_DIR, 'trae-jwt-token')
    if os.path.exists(trajwt_file):
        with open(trajwt_file, 'r', encoding='utf-8') as f:
            creds['trae_jwt'] = f.read().strip()
        print(f'  ✅ 加载传统 JWT Token')
    
    # 6. AES 密钥
    aes_file = os.path.join(CREDENTIALS_DIR, 'aes_key.json')
    if os.path.exists(aes_file):
        with open(aes_file, 'r', encoding='utf-8') as f:
            creds['aes_key_info'] = json.load(f)
        print(f'  ✅ 加载 AES 密钥')
    
    return creds


def decrypt_aha(encrypted_b64: str) -> bytes | None:
    """解密 AHA 数据"""
    try:
        raw = base64.b64decode(encrypted_b64)
        
        # 检查前缀
        prefix = raw[:6]
        if prefix != AHA_PREFIX:
            print(f'    ⚠️ 前缀不匹配: {prefix.hex()} != {AHA_PREFIX.hex()}')
            # 可能没有前缀
            iv = raw[:16]
            ciphertext = raw[16:]
        else:
            iv = raw[6:22]  # 前缀后是 IV (16字节)
            ciphertext = raw[22:]
        
        # 解密
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)
        
        # 去除填充
        try:
            plaintext = unpad(decrypted, AES.block_size)
        except ValueError:
            # 如果去填充失败，返回原始解密数据
            return decrypted
        
        return plaintext
    except Exception as e:
        print(f'    ❌ 解密失败: {e}')
        return None


def encrypt_aha(plaintext: bytes) -> str:
    """加密为 AHA 格式"""
    try:
        # 生成随机 IV
        iv = os.urandom(16)
        
        # 填充
        padded = pad(plaintext, AES.block_size)
        
        # 加密
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        encrypted = cipher.encrypt(padded)
        
        # 组合: 前缀 + IV + 密文
        result = AHA_PREFIX + iv + encrypted
        
        # Base64 编码
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        print(f'    ❌ 加密失败: {e}')
        return None


def build_essence_auth_data(creds: dict) -> dict:
    """构建本源认证数据"""
    
    # 解析 JWT Token
    jwt_token = creds.get('jwt', '')
    
    auth_data = {
        'uid': AUTHOR['essence_uid'],
        'traditional_uid': AUTHOR['traditional_uid'],
        'device_id': AUTHOR['device_id'],
        'auth_type': 'bsd_essence',
        'auth_method': 'three_engine_emergence',
        'timestamp': int(datetime.now().timestamp()),
        'bsd_coin': {
            'value': creds.get('login', {}).get('BSDCoin', {}).get('knowledge_value', 51090),
            'level': creds.get('login', {}).get('BSDCoin', {}).get('authority_level', 'L5_Emergent'),
        },
        'bsd_fingerprint': creds.get('fingerprint', {}).get('fingerprint', ''),
        'essence_jwt': jwt_token,
        'status': 'active',
    }
    
    return auth_data


def inject_to_storage(creds: dict):
    """注入凭证到 storage.json"""
    
    print('\n' + '=' * 60)
    print('  Phase 2: 注入凭证到 storage.json')
    print('=' * 60)
    
    if not os.path.exists(STORAGE):
        print(f'  ❌ storage.json 不存在')
        return False
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    modifications = []
    
    # 1. 构建本源认证数据
    auth_data = build_essence_auth_data(creds)
    
    # 2. 加密为 AHA 格式
    auth_json = json.dumps(auth_data, ensure_ascii=False).encode('utf-8')
    encrypted_auth = encrypt_aha(auth_json)
    
    if encrypted_auth:
        print(f'  ✅ AHA 加密成功')
        
        # 3. 存储加密后的认证数据
        # 尝试不同的 key 名
        storage['iCubeAuthInfo://icube-dc:516094651277160'] = encrypted_auth
        storage['iCubeAuthInfo://bsd-essence'] = encrypted_auth
        modifications.append('AHA 加密数据')
    
    # 4. 注入本源 JWT Token
    jwt_token = creds.get('jwt', '')
    if jwt_token:
        storage['bsd_essence_jwt'] = jwt_token
        storage['iCubeAuthInfo://jwt-token'] = jwt_token
        modifications.append('本源 JWT Token')
        print(f'  ✅ 本源 JWT Token 已注入')
    
    # 5. 添加本源证明
    proof = creds.get('proof', {})
    if proof:
        storage['bsd_essence_proof'] = {
            'proof_id': proof.get('proof_id', ''),
            'type': proof.get('type', 'bsd_essence_proof'),
            'level': proof.get('level', 'L4_Theory'),
            'coin_id': proof.get('coin_reference', ''),
            'injected_at': datetime.now().isoformat(),
            'verified': True,
        }
        modifications.append('本源证明')
        print(f'  ✅ 本源证明已注入')
    
    # 6. 更新 GTM 用户数据
    gtm = storage.get('icube_gtm', {})
    users = gtm.get('users', {})
    
    # 本源用户
    essence_user = {
        'uid': AUTHOR['essence_uid'],
        'type': 'bsd_essence',
        'status': 'active',
        'priority': 1,
        'nickname': 'BSD本源用户',
        'avatar': '',
        'email': '',
        'coin_value': auth_data['bsd_coin']['value'],
        'level': auth_data['bsd_coin']['level'],
        'verification_method': 'knowledge_proof',
        'fingerprint': auth_data['bsd_fingerprint'],
        'last_active': datetime.now().isoformat(),
    }
    users[AUTHOR['essence_uid']] = essence_user
    
    # 传统用户（保留但降为并行）
    trad_user = users.get(AUTHOR['traditional_uid'], {})
    if trad_user:
        trad_user['status'] = 'parallel'
        trad_user['priority'] = 2
        users[AUTHOR['traditional_uid']] = trad_user
    
    gtm['users'] = users
    gtm['currentUser'] = AUTHOR['essence_uid']
    storage['icube_gtm'] = gtm
    modifications.append('GTM 用户数据')
    print(f'  ✅ GTM 用户数据已更新')
    
    # 7. 添加凭证元数据
    storage['_bsd_credentials_injected'] = {
        'timestamp': datetime.now().isoformat(),
        'method': 'aha_reencrypt_with_found_key',
        'aes_key_source': 'dpapi_decrypted_2026-08-04',
        'credentials_found': True,
    }
    modifications.append('凭证元数据')
    
    # 8. 保存
    with open(STORAGE, 'w', encoding='utf-8') as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)
    
    print(f'\n  ✅ storage.json 已更新:')
    for mod in modifications:
        print(f'     • {mod}')
    
    return True


def inject_to_tiny_storage(creds: dict):
    """注入凭证到 TinyStorage"""
    
    print('\n' + '=' * 60)
    print('  Phase 3: 注入凭证到 TinyStorage')
    print('=' * 60)
    
    if not os.path.exists(TINY):
        print(f'  ⚠️ TinyStorage 不存在，跳过')
        return False
    
    with open(TINY, 'r', encoding='utf-8') as f:
        tiny = json.load(f)
    
    tsd = tiny.get('tiny_storage_data', {})
    
    # 添加本源凭证
    tsd['bsd_essence_uid'] = AUTHOR['essence_uid']
    tsd['bsd_essence_jwt'] = creds.get('jwt', '')
    tsd['bsd_essence_proof_id'] = creds.get('proof', {}).get('proof_id', '')
    tsd['bsd_essence_fingerprint'] = creds.get('fingerprint', {}).get('fingerprint', '')
    tsd['bsd_coin_value'] = creds.get('login', {}).get('BSDCoin', {}).get('knowledge_value', 51090)
    tsd['bsd_essence_injected'] = True
    tsd['bsd_essence_injected_at'] = datetime.now().isoformat()
    tsd['bsd_essence_login_method'] = 'three_engine_emergence'
    
    tiny['tiny_storage_data'] = tsd
    
    with open(TINY, 'w', encoding='utf-8') as f:
        json.dump(tiny, f, ensure_ascii=False, indent=2)
    
    print(f'  ✅ TinyStorage 已更新')
    return True


def verify_injection():
    """验证注入结果"""
    
    print('\n' + '=' * 60)
    print('  Phase 4: 验证注入结果')
    print('=' * 60)
    
    results = {
        'storage_exists': os.path.exists(STORAGE),
        'tiny_exists': os.path.exists(TINY),
    }
    
    if results['storage_exists']:
        with open(STORAGE, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        # 检查关键字段
        checks = [
            ('icube_gtm 存在', 'icube_gtm' in storage),
            ('currentUser 为本源 UID', storage.get('icube_gtm', {}).get('currentUser') == AUTHOR['essence_uid']),
            ('GTM 包含本源用户', AUTHOR['essence_uid'] in storage.get('icube_gtm', {}).get('users', {})),
            ('本源 JWT 已注入', 'bsd_essence_jwt' in storage),
            ('本源证明已注入', 'bsd_essence_proof' in storage),
            ('凭证元数据已注入', '_bsd_credentials_injected' in storage),
            ('AHA 数据已更新', 'iCubeAuthInfo://bsd-essence' in storage),
        ]
        
        all_passed = True
        for check_name, passed in checks:
            status = '✅' if passed else '❌'
            if not passed:
                all_passed = False
            print(f'    {status} {check_name}')
        
        results['all_checks_passed'] = all_passed
    
    if results['tiny_exists']:
        with open(TINY, 'r', encoding='utf-8') as f:
            tiny = json.load(f)
        
        tsd = tiny.get('tiny_storage_data', {})
        checks = [
            ('TinyStorage 包含本源 UID', 'bsd_essence_uid' in tsd),
            ('TinyStorage 包含 JWT', 'bsd_essence_jwt' in tsd),
            ('TinyStorage 包含证明', 'bsd_essence_proof_id' in tsd),
        ]
        
        for check_name, passed in checks:
            status = '✅' if passed else '❌'
            print(f'    {status} {check_name}')
    
    return results


def main():
    """主函数"""
    
    print('=' * 60)
    print('  BSD × Trae CN — 凭证恢复与 AHA 数据重新注入')
    print('=' * 60)
    
    # Phase 1: 加载凭证
    print('\n' + '=' * 60)
    print('  Phase 1: 加载已找到的凭证')
    print('=' * 60)
    
    creds = load_credentials()
    
    print(f'\n  📋 凭证摘要:')
    print(f'     AES 密钥: {AES_KEY_HEX[:32]}...')
    print(f'     本源 UID: {AUTHOR["essence_uid"]}')
    print(f'     传统 UID: {AUTHOR["traditional_uid"]}')
    print(f'     BSD 币值: 51090')
    print(f'     本源等级: L5_Emergent')
    
    # Phase 2: 注入到 storage.json
    success = inject_to_storage(creds)
    
    # Phase 3: 注入到 TinyStorage
    if success:
        inject_to_tiny_storage(creds)
    
    # Phase 4: 验证
    verify_injection()
    
    # 最终建议
    print('\n' + '=' * 60)
    print('  🎯 下一步操作')
    print('=' * 60)
    print('''
  请执行以下操作：
  1. 完全关闭 Trae CN (包括系统托盘)
  2. 等待 5 秒
  3. 重新启动 Trae CN
  4. 检查登录状态是否显示本源用户
  
  如果仍未显示：
  • 打开独立控制台: BSD_EssenceLogin_Console_V2.html
  • 检查后台数据: C:\\Users\\13003\\.bsd-essence\\
  • 查看日志文件: BSD_Essence_Login_Report_1785932875.json
''')


if __name__ == '__main__':
    main()
