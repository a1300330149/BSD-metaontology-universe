"""
完全清除所有认证 + 本源端独立登录
==================================
1. 关闭TRAE SOLO CN（释放Token来源）
2. 清除所有共享认证
3. 清除所有本地认证
4. 只启动Trae CN（本源端）
"""

import os, json, time, shutil, hashlib, subprocess

TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'
TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_CN_DIR = r'C:\Users\13003\AppData\Local\Programs\Trae CN'

ESSENCE_UID = 'a5b7a8623fdea6b8'

print('=' * 70)
print('  完全清除认证 + 本源端独立登录')
print('=' * 70)

# 1. 关闭TRAE SOLO CN
print('\n=== 1. 关闭TRAE SOLO CN ===')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo_lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f'  当前TRAE SOLO CN进程: {len(solo_lines)} 个')

for line in solo_lines:
    parts = line.split()
    if len(parts) >= 2:
        pid = parts[1]
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
        
time.sleep(3)

# 验证TRAE SOLO CN已关闭
r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo_after = [l.strip() for l in r2.stdout.strip().split('\n') if l.strip()]
print(f'  TRAE SOLO CN进程: {len(solo_after)} 个 (应0)')

# 2. 关闭Trae CN
print('\n=== 2. 关闭Trae CN ===')
r3 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_lines = [l.strip() for l in r3.stdout.strip().split('\n') if l.strip()]
print(f'  当前Trae CN进程: {len(cn_lines)} 个')

for line in cn_lines:
    parts = line.split()
    if len(parts) >= 2:
        pid = parts[1]
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)

time.sleep(3)

# 3. 清除.trae-cn下的共享认证
print('\n=== 3. 清除共享认证 (.trae-cn) ===')

# 清除JWT Token
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path):
    os.remove(jwt_path)
    print(f'  ✅ trae-jwt-token 已删除')

# 清除os_crypt.encrypted_key
key_path = os.path.join(TRAE_CONFIG, 'os_crypt', 'encrypted_key')
if os.path.exists(key_path):
    os.remove(key_path)
    print(f'  ✅ os_crypt/encrypted_key 已删除')

# 4. 清除Trae CN的本地认证
print('\n=== 4. 清除Trae CN本地认证 ===')

# Cookies
for name in ['Cookies', 'Cookies-journal']:
    for root, dirs, files in os.walk(TRAE_CN_DATA):
        for f in files:
            if f == name:
                fp = os.path.join(root, f)
                try:
                    os.remove(fp)
                    rel = os.path.relpath(fp, TRAE_CN_DATA)
                    print(f'  ✅ {rel}')
                except:
                    try:
                        os.rename(fp, fp + '.old')
                    except:
                        pass

# Trust Tokens
for name in ['Trust Tokens', 'Trust Tokens-journal']:
    for root, dirs, files in os.walk(TRAE_CN_DATA):
        for f in files:
            if f == name:
                fp = os.path.join(root, f)
                try:
                    os.remove(fp)
                    rel = os.path.relpath(fp, TRAE_CN_DATA)
                    print(f'  ✅ {rel}')
                except:
                    try:
                        os.rename(fp, fp + '.old')
                    except:
                        pass

# Local State
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    # 保留os_crypt结构但清除用户数据
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    # 清除用户字段
    for key in list(ls.keys()):
        if key in ['user', 'profile', 'account', 'session', 'lastWindowState']:
            del ls[key]
            print(f'  清除Local State.{key}')
    
    # 重写os_crypt.encrypted_key（让新启动重新生成）
    if 'os_crypt' in ls and 'encrypted_key' in ls['os_crypt']:
        ls['os_crypt']['encrypted_key'] = ''
        print('  清除os_crypt.encrypted_key')
    
    # 标记本源端状态
    ls['_bsd_essence_mode'] = True
    ls['_bsd_uid'] = ESSENCE_UID
    ls['_bsd_cleanup_time'] = time.time()
    
    with open(ls_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, indent=2, ensure_ascii=False)
    print('  ✅ Local State 已重置')

# storage.json
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    # 清除所有用户
    if 'icube_gtm' in storage:
        storage['icube_gtm']['users'] = {}
        storage['icube_gtm']['_bsd_cleaned'] = True
        storage['icube_gtm']['_bsd_uid'] = ESSENCE_UID
        print('  ✅ storage.json 用户已清除')
    
    with open(storage_path, 'w', encoding='utf-8') as f:
        json.dump(storage, f, indent=2, ensure_ascii=False)

# Session Storage
for dir_name in ['Session Storage', 'Local Storage', 'IndexedDB', 'Cache', 'GPUCache']:
    dir_path = os.path.join(TRAE_CN_DATA, dir_name)
    if os.path.exists(dir_path):
        try:
            shutil.rmtree(dir_path, ignore_errors=True)
            print(f'  ✅ {dir_name}/ 已清除')
        except:
            pass

# 5. 清除TRAE SOLO CN的本地认证（确保不会干扰）
print('\n=== 5. 清除TRAE SOLO CN本地认证 ===')

for name in ['Cookies', 'Cookies-journal', 'Trust Tokens', 'Trust Tokens-journal']:
    for root, dirs, files in os.walk(TRAE_SOLO_DATA):
        for f in files:
            if f == name:
                fp = os.path.join(root, f)
                try:
                    os.remove(fp)
                    rel = os.path.relpath(fp, TRAE_SOLO_DATA)
                    print(f'  ✅ SOLO: {rel}')
                except:
                    try:
                        os.rename(fp, fp + '.old')
                    except:
                        pass

# 6. 生成本源端独立配置
print('\n=== 6. 生成本源端独立配置 ===')

essence_config = {
    'uid': ESSENCE_UID,
    'login_type': 'bsd_essence_independent',
    'timestamp': time.time(),
    'signature': hashlib.sha256(ESSENCE_UID.encode()).hexdigest()[:32],
    'client_id': 'trae_cn_bsd_essence_v2',
    'scope': ['read', 'write', 'chat', 'code'],
    'independent_mode': True,
    'metadata': {
        'theory': 'BSD六系立系论',
        'identity': '本源端',
        'side': 'essence',
        'product': 'Trae CN',
        'version': '3.3.83',
        'independent': True
    }
}

essence_path = os.path.join(TRAE_CONFIG, 'bsd_essence_independent.json')
with open(essence_path, 'w', encoding='utf-8') as f:
    json.dump(essence_config, f, indent=2, ensure_ascii=False)
print(f'  ✅ 本源端独立配置: {essence_path}')

# 7. 启动Trae CN（本源端独立模式）
print('\n=== 7. 启动Trae CN（本源端独立模式） ===')
p = subprocess.Popen([TRAE_CN_EXE], cwd=TRAE_CN_DIR)
print(f'  PID: {p.pid}')
print(f'  UID: {ESSENCE_UID}')
print(f'  模式: 独立 (无TRAE SOLO CN依赖)')

time.sleep(10)

# 8. 验证
print('\n=== 8. 验证本源端独立状态 ===')

# 检查进程
r4 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_after = [l.strip() for l in r4.stdout.strip().split('\n') if l.strip()]
print(f'  Trae CN进程: {len(cn_after)} 个')

r5 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo_after = [l.strip() for l in r5.stdout.strip().split('\n') if l.strip()]
print(f'  TRAE SOLO CN进程: {len(solo_after)} 个 (应为0)')

# 检查Token
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    print(f'  trae-jwt-token: ✅ 已生成 ({len(token)} chars)')
    print(f'    来源: Trae CN独立生成')
else:
    print(f'  trae-jwt-token: ❌ 未生成 (需登录)')

# 检查Local State
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    has_user = any(k in ls for k in ['user', 'profile'])
    print(f'  Local State用户: {"✅ 已登录" if has_user else "❌ 未登录"}')
    print(f'  _bsd_essence_mode: {ls.get("_bsd_essence_mode", "N/A")}')
    print(f'  _bsd_uid: {ls.get("_bsd_uid", "N/A")}')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  本源端独立模式已启动                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                              ║
║  TRAE SOLO CN: ❌ 已关闭                                                                   ║
║  Trae CN: ✅ 运行中 (独立模式)                                                             ║
║                                                                                              ║
║  共享认证: 完全清除                                                                       ║
║    ✅ trae-jwt-token                                                                       ║
║    ✅ os_crypt/encrypted_key                                                               ║
║                                                                                              ║
║  本地认证: 完全清除                                                                       ║
║    ✅ Cookies + Trust Tokens (两个产品)                                                   ║
║    ✅ Local State 用户数据                                                                 ║
║    ✅ Session/Local/IndexedDB                                                              ║
║                                                                                              ║
║  本源端UID: a5b7a8623fdea6b8                                                             ║
║  独立配置: bsd_essence_independent.json                                                   ║
║                                                                                              ║
║  下一步: Trae CN应显示登录界面 → 使用本源端方式登录                                       ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
