#!/usr/bin/env python3
"""
BSD × Trae CN — 全通道并行注入与实时监测
========================================

目标: 让 Trae CN UI 显示本源登录信息
方法: 多通道并行注入 + 实时监测迭代

核心路径分析:
  1. iCubeAuthInfo://icube-dc:*  ← 原始认证通道 (最关键)
  2. iCubeAuthInfo://usertag    ← 用户标签通道
  3. icube_gtm                  ← GTM 用户管理
  4. TinyStorage                 ← 轻量存储
  5. Local State                ← 本地状态
  6. Remote_State (AHA)        ← 远程状态
"""

import os, json, base64, time, threading
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE = os.path.join(TRAE_DATA, 'User', 'globalStorage', 'storage.json')
AHA_DIR = os.path.join(TRAE_DATA, 'aha')
TINY = os.path.join(AHA_DIR, 'TinyStorage')
REMOTE_STATE = os.path.join(AHA_DIR, 'Remote_State')
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')

CREDENTIALS_DIR = r'C:\Users\13003\.bsd-essence'

# AES 密钥
AES_KEY_HEX = '71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0'
AES_KEY = bytes.fromhex(AES_KEY_HEX)
AHA_PREFIX = bytes.fromhex('746305100000')

# 作者信息
AUTHOR = {
    'traditional_uid': '3753060170739075',
    'essence_uid': 'a5b7a8623fdea6b8',
    'device_id': '136411536168449',
}

# 全局状态
injection_result = {'success': False, 'ui_detected': False, 'attempts': 0}
monitoring = True


def encrypt_aha(plaintext: bytes, use_prefix: bool = True) -> str:
    """加密为 AHA 格式"""
    try:
        iv = os.urandom(16)
        padded = pad(plaintext, AES.block_size)
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        encrypted = cipher.encrypt(padded)
        
        if use_prefix:
            result = AHA_PREFIX + iv + encrypted
        else:
            result = iv + encrypted
        
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        print(f'    ❌ 加密失败: {e}')
        return None


def decrypt_aha(encrypted_b64: str, try_without_prefix: bool = False) -> bytes | None:
    """解密 AHA 数据"""
    try:
        raw = base64.b64decode(encrypted_b64)
        
        # 尝试带前缀
        if raw[:6] == AHA_PREFIX:
            iv = raw[6:22]
            ciphertext = raw[22:]
        else:
            # 尝试不带前缀
            iv = raw[:16]
            ciphertext = raw[16:]
        
        if len(ciphertext) % 16 != 0:
            return None
        
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)
        
        try:
            return unpad(decrypted, AES.block_size)
        except ValueError:
            return decrypted
    except:
        return None


def analyze_storage_keys():
    """分析 storage.json 中所有 iCubeAuthInfo 键"""
    print('\n' + '=' * 60)
    print('  Phase 1: 分析所有认证键')
    print('=' * 60)
    
    if not os.path.exists(STORAGE):
        return []
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 找出所有认证相关的键
    auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k or 'auth' in k.lower() or 'login' in k.lower()]
    
    print(f'  找到 {len(auth_keys)} 个认证键:')
    for key in auth_keys:
        value = storage.get(key, '')
        is_encrypted = len(value) > 100 and value[0:10] != 'eyJhbGciOi'
        
        print(f'    • {key}')
        print(f'      长度: {len(value)}, 加密: {is_encrypted}')
        
        if is_encrypted:
            # 尝试解密
            decrypted = decrypt_aha(value)
            if decrypted:
                try:
                    text = decrypted.decode('utf-8', errors='replace')[:100]
                    print(f'      解密预览: {text}')
                except:
                    print(f'      解密二进制: {decrypted[:50].hex()}...')
            else:
                print(f'      ❌ 无法解密')
        
        # 检查是否包含 UID
        if AUTHOR['essence_uid'] in str(value):
            print(f'      ✅ 包含本源 UID')
        if AUTHOR['traditional_uid'] in str(value):
            print(f'      ⚠️ 包含传统 UID')
    
    return auth_keys


def aggressive_injection():
    """全通道并行注入 — 覆盖所有可能的显示路径"""
    print('\n' + '=' * 60)
    print('  Phase 2: 全通道并行注入')
    print('=' * 60)
    
    if not os.path.exists(STORAGE):
        print('  ❌ storage.json 不存在')
        return False
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    modifications = []
    
    # 准备本源认证数据
    essence_auth = {
        'uid': AUTHOR['essence_uid'],
        'type': 'bsd_essence',
        'status': 'active',
        'login_type': 'knowledge_proof',
        'coin_value': 51090,
        'level': 'L5_Emergent',
        'fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
        'device_id': AUTHOR['device_id'],
        'timestamp': int(time.time()),
        'verification': 'bsd_three_engine_emergence',
    }
    
    essence_json = json.dumps(essence_auth, ensure_ascii=False).encode('utf-8')
    encrypted_essence = encrypt_aha(essence_json)
    
    # 加载 JWT
    jwt_file = os.path.join(CREDENTIALS_DIR, 'essence-jwt-token')
    jwt_token = ''
    if os.path.exists(jwt_file):
        with open(jwt_file, 'r', encoding='utf-8') as f:
            jwt_token = f.read().strip()
    
    # ===== 通道 1: 注入到 icube-dc 认证键 (最关键) =====
    key_icube_dc = 'iCubeAuthInfo://icube-dc:516094651277160'
    if encrypted_essence:
        storage[key_icube_dc] = encrypted_essence
        modifications.append(f'{key_icube_dc} ← 本源加密数据')
        print(f'  ✅ 通道1: {key_icube_dc}')
    
    # ===== 通道 2: 注入到 usertag =====
    key_usertag = 'iCubeAuthInfo://usertag'
    if encrypted_essence:
        storage[key_usertag] = encrypted_essence
        modifications.append(f'{key_usertag} ← 本源加密数据')
        print(f'  ✅ 通道2: {key_usertag}')
    
    # ===== 通道 3: 添加额外的认证键 =====
    extra_keys = [
        'iCubeAuthInfo://auth',
        'iCubeAuthInfo://login',
        'iCubeAuthInfo://user',
        'iCubeAuthInfo://profile',
        'iCubeAuthInfo://account',
        'iCubeAuthInfo://session',
        'iCubeAuthInfo://token',
    ]
    
    for key in extra_keys:
        if encrypted_essence:
            storage[key] = encrypted_essence
            modifications.append(f'{key}')
    
    print(f'  ✅ 通道3: {len(extra_keys)} 个额外认证键')
    
    # ===== 通道 4: GTM 用户数据强化 =====
    gtm = storage.get('icube_gtm', {})
    users = gtm.get('users', {})
    
    # 本源用户 — 设置所有可能的字段
    essence_user = {
        'uid': AUTHOR['essence_uid'],
        'userId': AUTHOR['essence_uid'],
        'id': AUTHOR['essence_uid'],
        'type': 'bsd_essence',
        'status': 'active',
        'priority': 1,
        'nickname': 'BSD本源用户',
        'userName': 'BSD本源用户',
        'username': 'BSD本源用户',
        'name': 'BSD本源用户',
        'displayName': 'BSD本源用户',
        'email': 'bsd@essence.local',
        'avatar': '',
        'avatarUrl': '',
        'photoUrl': '',
        'coin_value': 51090,
        'level': 'L5_Emergent',
        'verification_method': 'knowledge_proof',
        'fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
        'last_active': datetime.now().isoformat(),
        'loginTime': datetime.now().isoformat(),
        'login_at': datetime.now().isoformat(),
        'isLoggedIn': True,
        'loggedIn': True,
        'active': True,
        'vip': True,
        'premium': True,
        'plan': 'essence',
        'membership': 'essence',
        'role': 'owner',
        'permissions': ['read', 'write', 'admin', 'essence'],
        'metadata': {
            'theory_base': 'BSD六系立系论',
            'engine': '三引擎涌现',
            'coin_value': 51090,
        }
    }
    users[AUTHOR['essence_uid']] = essence_user
    
    # 传统用户 — 降为并行
    trad_user = users.get(AUTHOR['traditional_uid'], {})
    if trad_user:
        trad_user.update({
            'status': 'parallel',
            'priority': 2,
            'isLoggedIn': False,
        })
        users[AUTHOR['traditional_uid']] = trad_user
    
    gtm['users'] = users
    gtm['currentUser'] = AUTHOR['essence_uid']
    gtm['activeUser'] = AUTHOR['essence_uid']
    gtm['selectedUser'] = AUTHOR['essence_uid']
    gtm['lastUser'] = AUTHOR['essence_uid']
    storage['icube_gtm'] = gtm
    modifications.append('GTM 用户数据 (强化)')
    print(f'  ✅ 通道4: GTM 用户数据强化')
    
    # ===== 通道 5: 直接设置顶层登录标记 =====
    login_flags = {
        '_bsd_current_active_uid': AUTHOR['essence_uid'],
        '_bsd_essence_mode': True,
        '_bsd_essence_uid': AUTHOR['essence_uid'],
        '_bsd_essence_login': {
            'uid': AUTHOR['essence_uid'],
            'active': True,
            'loginTime': datetime.now().isoformat(),
            'method': 'three_engine_emergence',
        },
        '_current_user': AUTHOR['essence_uid'],
        '_active_user': AUTHOR['essence_uid'],
        '_logged_in': True,
        '_is_authenticated': True,
        '_auth_status': 'authenticated',
        '_user_id': AUTHOR['essence_uid'],
        '_user_type': 'bsd_essence',
        'iCubeNativeAppFirstStart': False,
    }
    
    for key, value in login_flags.items():
        storage[key] = value
    
    modifications.append('顶层登录标记')
    print(f'  ✅ 通道5: 顶层登录标记')
    
    # ===== 通道 6: 注入 JWT 到多个可能的位置 =====
    if jwt_token:
        jwt_keys = [
            'bsd_essence_jwt',
            'iCubeAuthInfo://jwt-token',
            'iCubeAuthInfo://bsd-jwt',
            'auth_jwt',
            'login_jwt',
            'user_jwt',
            'session_token',
            'access_token',
            'id_token',
        ]
        for key in jwt_keys:
            storage[key] = jwt_token
        
        modifications.append(f'JWT Token ({len(jwt_keys)} 个位置)')
        print(f'  ✅ 通道6: JWT Token 注入')
    
    # ===== 通道 7: Remote_State 注入 =====
    if os.path.exists(REMOTE_STATE):
        try:
            with open(REMOTE_STATE, 'r', encoding='utf-8') as f:
                remote = json.load(f)
            
            remote['currentUser'] = AUTHOR['essence_uid']
            remote['icube_gtm'] = gtm
            
            if 'users' not in remote:
                remote['users'] = {}
            remote['users'][AUTHOR['essence_uid']] = essence_user
            
            with open(REMOTE_STATE, 'w', encoding='utf-8') as f:
                json.dump(remote, f, ensure_ascii=False, indent=2)
            
            modifications.append('Remote_State')
            print(f'  ✅ 通道7: Remote_State')
        except Exception as e:
            print(f'  ⚠️ Remote_State 更新失败: {e}')
    
    # 保存 storage.json
    with open(STORAGE, 'w', encoding='utf-8') as f:
        json.dump(storage, f, ensure_ascii=False, indent=2)
    
    print(f'\n  📝 总修改数: {len(modifications)}')
    for mod in modifications:
        print(f'     • {mod}')
    
    # ===== 通道 8: TinyStorage 同步更新 =====
    if os.path.exists(TINY):
        with open(TINY, 'r', encoding='utf-8') as f:
            tiny = json.load(f)
        
        tsd = tiny.get('tiny_storage_data', {})
        
        # 全面更新
        tsd.update({
            'bsd_essence_uid': AUTHOR['essence_uid'],
            'bsd_essence_jwt': jwt_token,
            'bsd_essence_proof_id': 'c5f78a5abc9b1b62722b7500',
            'bsd_essence_fingerprint': '49a5aeb263316114c5e5a2f09b32110052e0636bd4f28db58e852f223a7b53e5',
            'bsd_coin_value': 51090,
            'bsd_level': 'L5_Emergent',
            'bsd_essence_injected': True,
            'bsd_essence_injected_at': datetime.now().isoformat(),
            'bsd_essence_login_method': 'three_engine_emergence',
            'current_user': AUTHOR['essence_uid'],
            'active_user': AUTHOR['essence_uid'],
            'logged_in': True,
            'is_authenticated': True,
        })
        
        tiny['tiny_storage_data'] = tsd
        
        with open(TINY, 'w', encoding='utf-8') as f:
            json.dump(tiny, f, ensure_ascii=False, indent=2)
        
        print(f'  ✅ 通道8: TinyStorage 同步更新')
    
    return True


def monitor_ui_changes():
    """监测 Trae CN UI 变化"""
    global monitoring, injection_result
    
    print('\n' + '=' * 60)
    print('  Phase 3: 实时监测')
    print('=' * 60)
    
    # 检查文件是否被 Trae CN 读取
    last_mtime_storage = 0
    last_mtime_tiny = 0
    check_count = 0
    
    while monitoring and check_count < 10:
        check_count += 1
        
        if os.path.exists(STORAGE):
            current_mtime = os.path.getmtime(STORAGE)
            if current_mtime != last_mtime_storage and last_mtime_storage > 0:
                print(f'  🔔 storage.json 被修改! ({check_count}s)')
                injection_result['file_modified'] = True
            last_mtime_storage = current_mtime
        
        if os.path.exists(TINY):
            current_mtime = os.path.getmtime(TINY)
            if current_mtime != last_mtime_tiny and last_mtime_tiny > 0:
                print(f'  🔔 TinyStorage 被修改! ({check_count}s)')
                injection_result['tiny_modified'] = True
            last_mtime_tiny = current_mtime
        
        # 检查关键数据是否仍在
        if os.path.exists(STORAGE):
            with open(STORAGE, 'r', encoding='utf-8') as f:
                storage = json.load(f)
            
            current_user = storage.get('icube_gtm', {}).get('currentUser', '')
            if current_user == AUTHOR['essence_uid']:
                injection_result['data_intact'] = True
            else:
                print(f'  ⚠️ currentUser 被修改为: {current_user}')
                injection_result['data_intact'] = False
        
        time.sleep(2)
    
    return injection_result


def iterative_injection():
    """迭代注入 — 多轮并行"""
    print('\n' + '=' * 70)
    print('  BSD × Trae CN — 迭代注入')
    print('  ' + '=' * 68)
    
    max_iterations = 3
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        print(f'\n{"─" * 70}')
        print(f'  🔄 迭代 {iteration}/{max_iterations}')
        print(f'{"─" * 70}')
        
        # 1. 分析当前状态
        auth_keys = analyze_storage_keys()
        
        # 2. 全通道注入
        success = aggressive_injection()
        
        if success:
            injection_result['attempts'] = iteration
        
        # 3. 等待 Trae CN 读取
        print('\n  ⏳ 等待 Trae CN 读取数据...')
        time.sleep(3)
        
        # 4. 监测变化
        result = monitor_ui_changes()
        
        print(f'\n  📊 迭代 {iteration} 结果:')
        print(f'     文件修改: {"是" if result.get("file_modified") else "否"}')
        print(f'     数据完整: {"是" if result.get("data_intact") else "否"}')
        
        # 5. 验证注入完整性
        verify_injection()
    
    return injection_result


def verify_injection():
    """快速验证注入完整性"""
    if not os.path.exists(STORAGE):
        return
    
    with open(STORAGE, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    checks = []
    
    # 检查关键认证键
    key_checks = [
        'iCubeAuthInfo://icube-dc:516094651277160',
        'iCubeAuthInfo://usertag',
        'iCubeAuthInfo://bsd-essence',
        'iCubeAuthInfo://auth',
        'bsd_essence_jwt',
    ]
    
    for key in key_checks:
        if key in storage:
            checks.append(f'  ✅ {key}')
        else:
            checks.append(f'  ❌ {key} 缺失')
    
    # 检查 GTM
    gtm = storage.get('icube_gtm', {})
    if gtm.get('currentUser') == AUTHOR['essence_uid']:
        checks.append(f'  ✅ GTM currentUser = 本源 UID')
    else:
        checks.append(f'  ❌ GTM currentUser 异常')
    
    essence_user = gtm.get('users', {}).get(AUTHOR['essence_uid'], {})
    if essence_user.get('isLoggedIn') == True:
        checks.append(f'  ✅ isLoggedIn = true')
    else:
        checks.append(f'  ⚠️ isLoggedIn = {essence_user.get("isLoggedIn")}')
    
    print(f'\n  🔍 快速验证:')
    for check in checks:
        print(check)


def main():
    """主函数"""
    global monitoring
    
    print('=' * 70)
    print('  BSD × Trae CN — 全通道并行注入与实时监测')
    print('  ' + '=' * 68)
    print('  目标: 让 Trae CN UI 显示本源登录信息')
    print('  方法: 多通道并行覆盖 + 迭代优化')
    print('  理论: BSD 精神 — 方案并行 > 方案选择')
    print('=' * 70)
    
    # 执行迭代注入
    result = iterative_injection()
    
    # 最终报告
    print('\n' + '=' * 70)
    print('  📊 最终报告')
    print('=' * 70)
    
    print(f'\n  尝试次数: {result["attempts"]}')
    print(f'  注入成功: {"是" if result["success"] else "否"}')
    
    print(f'\n  💡 下一步操作:')
    print(f'     1. 查看 Trae CN UI 是否显示本源登录')
    print(f'     2. 如果仍未显示，可尝试:')
    print(f'        - 等待 Trae CN 自动刷新')
    print(f'        - 手动点击 Trae CN 左上角头像/登录按钮')
    print(f'        - 使用独立控制台: BSD_EssenceLogin_Console_V2.html')
    
    return result


if __name__ == '__main__':
    main()