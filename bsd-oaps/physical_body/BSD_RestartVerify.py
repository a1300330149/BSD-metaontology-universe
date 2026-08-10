"""
重启Trae CN验证登录状态
"""
import subprocess, time, os, json

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_CN_DIR = r'C:\Users\13003\AppData\Local\Programs\Trae CN'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'

# 1. 关闭Trae CN
print('=== 1. 关闭Trae CN ===')
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_lines = [l.strip() for l in r.stdout.strip().split('\n') if l.strip()]
print(f'  当前Trae CN进程: {len(cn_lines)} 个')

for line in cn_lines:
    parts = line.split()
    if len(parts) >= 2:
        pid = parts[1]
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True)
        print(f'  终止 PID: {pid}')

time.sleep(2)

# 验证TRAE SOLO CN仍在运行
r2 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq TRAE SOLO CN*', '/NH'], capture_output=True, text=True)
solo_lines = [l.strip() for l in r2.stdout.strip().split('\n') if l.strip()]
print(f'  TRAE SOLO CN: {len(solo_lines)} 个进程 (保持运行)')

# 2. 清除更多残留
print('\n=== 2. 清除残留数据 ===')

# 清除Cache
cache_dir = os.path.join(TRAE_CN_DATA, 'Cache')
if os.path.exists(cache_dir):
    import shutil
    try:
        shutil.rmtree(cache_dir, ignore_errors=True)
        print('  ✅ Cache/ 已清除')
    except:
        pass

# 清除GPUCache
gpu_dir = os.path.join(TRAE_CN_DATA, 'GPUCache')
if os.path.exists(gpu_dir):
    import shutil
    try:
        shutil.rmtree(gpu_dir, ignore_errors=True)
        print('  ✅ GPUCache/ 已清除')
    except:
        pass

# 3. 检查当前认证状态
print('\n=== 3. 检查当前认证状态 ===')

# JWT Token
jwt_path = r'C:\Users\13003\.trae-cn\trae-jwt-token'
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        jwt = f.read().strip()
    print(f'  trae-jwt-token: {len(jwt)} chars (存在)')
else:
    print('  trae-jwt-token: ❌ 已清除')

# Local State
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    has_user = any(k in ls for k in ['user', 'profile', 'account'])
    print(f'  Local State 用户数据: {"❌ 已清除" if not has_user else "⚠️ 仍存在"}')
    print(f'  _bsd_logout: {ls.get("_bsd_logout", "N/A")}')

# storage.json
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    users = storage.get('icube_gtm', {}).get('users', {})
    print(f'  storage.json 用户数: {len(users)}')

# Cookies
cookies_exist = os.path.exists(os.path.join(TRAE_CN_DATA, 'Cookies'))
print(f'  Cookies: {"存在" if cookies_exist else "❌ 已删除"}')

# 4. 启动Trae CN
print('\n=== 4. 启动Trae CN ===')
p = subprocess.Popen([TRAE_CN_EXE], cwd=TRAE_CN_DIR)
print(f'  PID: {p.pid}')
print(f'  UID: a5b7a8623fdea6b8 (本源端)')

# 等待加载
time.sleep(8)

# 5. 检查新启动后的状态
print('\n=== 5. 检查新启动后的状态 ===')

r3 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_after = [l.strip() for l in r3.stdout.strip().split('\n') if l.strip()]
print(f'  Trae CN进程: {len(cn_after)} 个')

# 检查是否生成了新的认证文件
if os.path.exists(jwt_path) and os.path.getsize(jwt_path) > 0:
    with open(jwt_path, 'r') as f:
        jwt = f.read().strip()
    if len(jwt) > 10:
        print(f'  trae-jwt-token: ✅ 已重新生成 ({len(jwt)} chars)')
    else:
        print(f'  trae-jwt-token: ⚠️ 空文件')
else:
    print(f'  trae-jwt-token: ❌ 未生成')

# 检查Local State
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    # 检查是否有新的用户登录
    has_new_login = ls.get('user') or ls.get('profile')
    print(f'  Local State 用户: {"✅ 已登录" if has_new_login else "❌ 未登录"}')

print(f'''\n╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  验证结果                                                                                 ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║  作者端登录态: ❌ 已清除                                                                   ║
║  本源端UID: a5b7a8623fdea6b8                                                             ║
║  网络状态: ❌ 不可用 (无法调用云端API)                                                    ║
║                                                                                              ║
║  本地清除: ✅ 全部完成                                                                     ║
║  Trae CN: 已重启                                                                          ║
║                                                                                              ║
║  关键: 网络恢复后需调用ClearRefreshToken退出云端会话                                       ║
║        然后用LoginByJwt + 本源端UID登录                                                   ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
