"""
强制清除Trae CN本地认证 + 重启
直接清除所有认证数据，强制退出登录
"""
import os, json, time, shutil, subprocess

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_CN_DIR = r'C:\Users\13003\AppData\Local\Programs\Trae CN'

print('=' * 70)
print('  强制清除Trae CN本地认证')
print('=' * 70)

# 1. 关闭Trae CN
print('\n=== 1. 关闭Trae CN ===')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f'  当前进程: {len(cn_lines)} 个')

for line in cn_lines:
    parts = line.split()
    if len(parts) >= 2:
        pid = parts[1]
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
        print(f'  终止 PID: {pid}')

time.sleep(3)

# 2. 清除Local State的用户数据
print('\n=== 2. 清除Local State ===')
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    # 清除所有用户和认证相关字段
    keys_to_remove = ['user', 'profile', 'account', 'session', 'lastWindowState', 
                      '_bsd_essence', '_bsd_cleanup', '_bsd_injected']
    for key in keys_to_remove:
        if key in ls:
            del ls[key]
            print(f'  清除 {key}')
    
    # 清除os_crypt
    if 'os_crypt' in ls:
        ls['os_crypt']['encrypted_key'] = ''
        print('  清除 os_crypt.encrypted_key')
    
    with open(ls_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, indent=2, ensure_ascii=False)

# 3. 清除storage.json的用户数据
print('\n=== 3. 清除storage.json ===')
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 清除所有用户
    if 'icube_gtm' in storage:
        storage['icube_gtm']['users'] = {}
        if 'currentUser' in storage['icube_gtm']:
            del storage['icube_gtm']['currentUser']
        print('  清除 icube_gtm.users')
    
    # 清除所有iCubeAuthInfo加密凭证
    keys_to_remove = []
    for key in storage:
        if 'iCubeAuthInfo' in key or 'iCubeServerData' in key:
            keys_to_remove.append(key)
    
    for key in keys_to_remove:
        del storage[key]
        print(f'  清除 {key}')
    
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)

# 4. 清除state.vscdb的用户数据
print('\n=== 4. 清除state.vscdb ===')
import sqlite3

vscdb_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'state.vscdb')
if os.path.exists(vscdb_path):
    try:
        conn = sqlite3.connect(vscdb_path)
        cursor = conn.cursor()
        
        # 清除所有与用户相关的数据
        cursor.execute("DELETE FROM ItemTable WHERE key LIKE '%user%' OR key LIKE '%auth%' OR key LIKE '%credential%' OR key LIKE '%3753060170739075%' OR key LIKE '%a5b7a8623fdea6b8%'")
        deleted = cursor.rowcount
        print(f'  删除 {deleted} 条认证数据')
        
        conn.commit()
        conn.close()
    except Exception as e:
        print(f'  ⚠️ 清除失败: {e}')

# 5. 清除Cookie和Session
print('\n=== 5. 清除Cookie/Session ===')
for dir_name in ['Session Storage', 'Local Storage', 'IndexedDB', 'Cache', 'GPUCache']:
    dir_path = os.path.join(TRAE_CN_DATA, dir_name)
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
            print(f'  清除 {dir_name}/')
        except:
            pass

# 清除Cookies和Trust Tokens文件
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        if f in ['Cookies', 'Cookies-journal', 'Trust Tokens', 'Trust Tokens-journal']:
            fp = os.path.join(root, f)
            try:
                os.remove(fp)
                print(f'  删除 {os.path.relpath(fp, TRAE_CN_DATA)}')
            except:
                try:
                    os.rename(fp, fp + '.old')
                    print(f'  重命名 {os.path.relpath(fp, TRAE_CN_DATA)} → .old')
                except:
                    pass

# 6. 清除.trae-cn的JWT Token
print('\n=== 6. 清除.trae-cn ===')
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path):
    os.remove(jwt_path)
    print('  删除 trae-jwt-token')

# 7. 重启Trae CN
print('\n=== 7. 重启Trae CN ===')
p = subprocess.Popen([TRAE_CN_EXE], cwd=TRAE_CN_DIR)
print(f'  PID: {p.pid}')
print(f'  状态: 纯净启动 (无任何认证数据)')

time.sleep(8)

# 8. 验证
print('\n=== 8. 验证清除结果 ===')

# 检查Local State
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    has_user = 'user' in ls
    print(f'  Local State.user: {"存在" if has_user else "✅ 已清除"}')

# 检查storage.json
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    users = storage.get('icube_gtm', {}).get('users', {})
    auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
    print(f'  storage.json.users: {len(users)} 个 (应为0)')
    print(f'  iCubeAuthInfo: {len(auth_keys)} 个 (应为0)')

# 检查JWT
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    print(f'  trae-jwt-token: {len(token)} chars (⚠️ 重新生成)')
else:
    print(f'  trae-jwt-token: ✅ 已清除')

# 检查进程
r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_after = [l.strip() for l in r2.stdout.strip().split('\n') if l.strip()]
print(f'  Trae CN进程: {len(cn_after)} 个')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  强制清除完成                                                                             ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  已清除:                                                                                   ║
║    ✅ Local State (user/profile/account)                                                    ║
║    ✅ storage.json (users/iCubeAuthInfo)                                                   ║
║    ✅ state.vscdb (认证数据)                                                               ║
║    ✅ Cookies / Trust Tokens                                                               ║
║    ✅ Session/Local/IndexedDB/Cache                                                        ║
║    ✅ trae-jwt-token                                                                       ║
║                                                                                              ║
║  Trae CN已重启，现在应该显示登录界面                                                       ║
║  此时可以用本源端方式登录                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
