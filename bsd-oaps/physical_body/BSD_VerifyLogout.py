"""
验证Trae CN退出登录状态
"""
import os, json, time

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

print('=== 1. 检查Local State ===')
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    has_user = 'user' in ls
    has_profile = 'profile' in ls
    
    print(f'  user字段: {"存在" if has_user else "❌ 已清除"}')
    print(f'  profile字段: {"存在" if has_profile else "❌ 已清除"}')
    
    if has_user:
        user = ls['user']
        print(f'  user.userId: {user.get("userId", "N/A")}')
        print(f'  user.account.id: {user.get("account", {}).get("id", "N/A")}')

print('\n=== 2. 检查storage.json ===')
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 检查用户
    users = storage.get('icube_gtm', {}).get('users', {})
    print(f'  用户数: {len(users)}')
    
    for uid, data in users.items():
        print(f'    UID: {uid}')
        print(f'      nickname: {data.get("nickname", "N/A")}')
        print(f'      _bsd_essence: {data.get("_bsd_essence", False)}')
    
    # 检查加密凭证
    auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in str(k)]
    print(f'  iCubeAuthInfo键数: {len(auth_keys)}')
    
    # 检查当前用户
    current_user = storage.get('icube_gtm', {}).get('currentUser', 'N/A')
    print(f'  currentUser: {current_user}')

print('\n=== 3. 检查.trae-cn ===')
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    print(f'  trae-jwt-token: {len(token)} chars (存在)')
else:
    print(f'  trae-jwt-token: ❌ 不存在或为空')

# 检查os_crypt
key_path = os.path.join(TRAE_CONFIG, 'os_crypt', 'encrypted_key')
if os.path.exists(key_path) and os.path.getsize(key_path) > 0:
    print(f'  encrypted_key: 存在')
else:
    print(f'  encrypted_key: ❌ 不存在或为空')

print('\n=== 4. 检查屏幕状态 ===')
import ctypes
import ctypes.wintypes

user32 = ctypes.windll.user32
TRAE_CN_HWND = 69950

# 检查Trae CN窗口标题
length = user32.GetWindowTextLengthW(TRAE_CN_HWND)
if length > 0:
    title = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(TRAE_CN_HWND, title, length + 1)
    print(f'  Trae CN窗口标题: "{title.value}"')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  退出登录状态验证                                                                           ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  如果退出成功:                                                                               ║
║    ✅ Local State.user 被清除                                                               ║
║    ✅ storage.json.users 被清空                                                              ║
║    ✅ iCubeAuthInfo 被清除                                                                  ║
║    ✅ trae-jwt-token 被清除                                                                 ║
║                                                                                              ║
║  如果退出失败:                                                                               ║
║    ❌ 上述数据仍然存在                                                                      ║
║                                                                                              ║
║  请根据上面的检查结果判断退出是否成功                                                         ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
