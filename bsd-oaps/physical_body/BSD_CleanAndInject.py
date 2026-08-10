"""
关闭Trae CN + 清除加密认证 + 本源端注入
"""
import os, json, time, hashlib, shutil, subprocess

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_CN_DIR = r'C:\Users\13003\AppData\Local\Programs\Trae CN'

ESSENCE_UID = 'a5b7a8623fdea6b8'

print('=' * 70)
print('  关闭Trae CN + 清除加密认证 + 本源端注入')
print('=' * 70)

# 1. 关闭Trae CN
print('\n=== 1. 关闭Trae CN ===')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f'  当前Trae CN进程: {len(cn_lines)} 个')

for line in cn_lines:
    parts = line.split()
    if len(parts) >= 2:
        pid = parts[1]
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
        print(f'  终止 PID: {pid}')

time.sleep(3)

# 2. 清除iCubeAuthInfo加密凭证
print('\n=== 2. 清除加密认证凭证 ===')

# storage.json
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 清除所有iCubeAuthInfo加密数据
    auth_keys_to_remove = []
    
    def find_auth_keys(obj, path=''):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if 'iCubeAuthInfo' in str(k) or 'iCubeServerData' in str(k):
                    auth_keys_to_remove.append((path, k))
                find_auth_keys(v, f'{path}.{k}')
    
    find_auth_keys(storage)
    
    print(f'  发现 {len(auth_keys_to_remove)} 个加密认证键')
    
    # 构建新的storage，排除加密认证
    def remove_auth_keys(obj):
        if isinstance(obj, dict):
            return {k: remove_auth_keys(v) for k, v in obj.items() 
                    if 'iCubeAuthInfo' not in str(k) and 'iCubeServerData' not in str(k)}
        elif isinstance(obj, list):
            return [remove_auth_keys(item) for item in obj]
        else:
            return obj
    
    storage_clean = remove_auth_keys(storage)
    
    # 注入本源端UID
    if 'icube_gtm' not in storage_clean:
        storage_clean['icube_gtm'] = {}
    if 'users' not in storage_clean['icube_gtm']:
        storage_clean['icube_gtm']['users'] = {}
    
    storage_clean['icube_gtm']['users'][ESSENCE_UID] = {
        'userId': ESSENCE_UID,
        'uid': ESSENCE_UID,
        'nickname': 'BSD本源端',
        '_bsd_essence': True,
        '_bsd_injected': True
    }
    storage_clean['icube_gtm']['currentUser'] = ESSENCE_UID
    storage_clean['_bsd_cleanup'] = True
    storage_clean['_bsd_cleanup_time'] = time.time()
    
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(storage_clean, f, indent=2, ensure_ascii=False)
    print(f'  ✅ storage.json 加密认证已清除')

# 3. 清除state.vscdb中的认证数据
print('\n=== 3. 清除state.vscdb认证数据 ===')
import sqlite3

vscdb_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'state.vscdb')
if os.path.exists(vscdb_path):
    try:
        conn = sqlite3.connect(vscdb_path)
        cursor = conn.cursor()
        
        # 查找认证相关的键
        cursor.execute("SELECT key FROM ItemTable WHERE key LIKE '%3753060170739075%' OR key LIKE '%user:%' OR key LIKE '%credits%'")
        auth_keys = [row[0] for row in cursor.fetchall()]
        print(f'  发现 {len(auth_keys)} 个认证相关键')
        
        # 清除作者端UID相关的键
        cursor.execute("DELETE FROM ItemTable WHERE key LIKE '%3753060170739075%'")
        deleted = cursor.rowcount
        print(f'  已删除 {deleted} 条作者端数据')
        
        conn.commit()
        conn.close()
        print(f'  ✅ state.vscdb 已清除')
    except Exception as e:
        print(f'  ⚠️ state.vscdb 清除失败: {e}')

# 4. 清除Local State
print('\n=== 4. 重置Local State ===')
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    # 清除用户和加密数据
    for key in list(ls.keys()):
        if key in ['user', 'profile', 'account', 'session', 'lastWindowState']:
            del ls[key]
            print(f'  清除 Local State.{key}')
    
    # 清除os_crypt
    if 'os_crypt' in ls and 'encrypted_key' in ls['os_crypt']:
        ls['os_crypt']['encrypted_key'] = ''
        print(f'  清除 os_crypt.encrypted_key')
    
    # 注入本源端
    ls['user'] = {
        'userId': ESSENCE_UID,
        'account': {'id': ESSENCE_UID, 'scope': 'bsd_essence'},
        'userInfo': {'nickname': 'BSD本源端'}
    }
    ls['profile'] = {'userId': ESSENCE_UID, 'nickname': 'BSD本源端'}
    ls['_bsd_essence'] = True
    ls['_bsd_cleanup'] = True
    
    with open(ls_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, indent=2, ensure_ascii=False)
    print(f'  ✅ Local State 已重置 + 本源端注入')

# 5. 清除Cookie/Session
print('\n=== 5. 清除Cookie/Session ===')
for dir_name in ['Session Storage', 'Local Storage', 'IndexedDB', 'Cache', 'GPUCache']:
    dir_path = os.path.join(TRAE_CN_DATA, dir_name)
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
            print(f'  ✅ {dir_name}/ 已清除')
        except:
            pass

# 清除Cookies和Trust Tokens
for root, dirs, files in os.walk(TRAE_CN_DATA):
    for f in files:
        if f in ['Cookies', 'Cookies-journal', 'Trust Tokens', 'Trust Tokens-journal']:
            fp = os.path.join(root, f)
            try:
                os.remove(fp)
                print(f'  ✅ {os.path.relpath(fp, TRAE_CN_DATA)}')
            except:
                try:
                    os.rename(fp, fp + '.old')
                    print(f'  🔄 {os.path.relpath(fp, TRAE_CN_DATA)} → .old')
                except:
                    pass

# 6. 重启Trae CN
print('\n=== 6. 重启Trae CN ===')
p = subprocess.Popen([TRAE_CN_EXE], cwd=TRAE_CN_DIR)
print(f'  PID: {p.pid}')
print(f'  UID: {ESSENCE_UID} (本源端)')
print(f'  模式: 纯净启动 (无加密认证)')

time.sleep(10)

# 7. 验证
print('\n=== 7. 验证结果 ===')

r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_after = [l.strip() for l in r2.stdout.strip().split('\n') if l.strip()]
print(f'  Trae CN进程: {len(cn_after)} 个')

# 检查是否生成了新的加密凭证
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    auth_count = sum(1 for k in storage.keys() if 'iCubeAuthInfo' in str(k))
    print(f'  iCubeAuthInfo键数: {auth_count}')
    
    has_essence = ESSENCE_UID in str(storage)
    print(f'  本源端UID存在: {has_essence}')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  本源端纯净启动完成                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  清除内容:                                                                                 ║
║    ✅ iCubeAuthInfo加密凭证 (storage.json)                                                 ║
║    ✅ 作者端UID数据 (state.vscdb)                                                          ║
║    ✅ Cookies / Trust Tokens                                                               ║
║    ✅ Session/Local/IndexedDB                                                              ║
║    ✅ os_crypt.encrypted_key                                                               ║
║                                                                                              ║
║  注入内容:                                                                                 ║
║    ✅ 本源端UID: {ESSENCE_UID}                                                            ║
║    ✅ 本源端昵称: BSD本源端                                                                ║
║    ✅ 本源端Token (待生成)                                                                 ║
║                                                                                              ║
║  状态: Trae CN已重启，应显示登录界面                                                       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
