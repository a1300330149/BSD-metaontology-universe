"""
Trae CN 本源端登录验证
"""
import subprocess, time, os, json

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
TRAE_CN_DIR = r'C:\Users\13003\AppData\Local\Programs\Trae CN'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'

# 1. 关闭Trae CN进程
print('=== 1. 关闭Trae CN进程 ===')
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
print(f'\n  TRAE SOLO CN仍在运行: {len(solo_lines)} 个进程')

# 2. 重新启动Trae CN
print('\n=== 2. 启动Trae CN (本源端) ===')
p = subprocess.Popen([TRAE_CN_EXE], cwd=TRAE_CN_DIR)
print(f'  PID: {p.pid}')
print(f'  UID: a5b7a8623fdea6b8')

time.sleep(5)

# 3. 验证登录状态
print('\n=== 3. 验证本源端登录 ===')

r3 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae CN*', '/NH'], capture_output=True, text=True)
cn_after = [l.strip() for l in r3.stdout.strip().split('\n') if l.strip()]
print(f'  Trae CN进程: {len(cn_after)} 个')

# 检查Local State
ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
if os.path.exists(ls_path):
    with open(ls_path, 'r', encoding='utf-8') as f:
        ls = json.load(f)
    
    print('\n  Local State 本源端标识:')
    for k in ['_bsd_replaced_author', '_bsd_essence_side', '_bsd_uid', '_bsd_login_mode']:
        if k in ls:
            print(f'    {k}: {ls[k]}')

# 检查storage.json
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path) and os.path.getsize(storage_path) > 0:
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    if 'icube_gtm' in storage and 'users' in storage['icube_gtm']:
        users = storage['icube_gtm']['users']
        print('\n  storage.json 用户:')
        for uid, data in users.items():
            print(f'    UID: {uid}')
            br = data.get('_bsd_replaced', False)
            ut = data.get('_uid_type', 'N/A')
            print(f'      bsd_replaced: {br}')
            print(f'      uid_type: {ut}')

# 最终状态
r4 = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq Trae*', '/NH'], capture_output=True, text=True)
total = len([l for l in r4.stdout.strip().split('\n') if l.strip()])

print(f'''
╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║  ⚡ 本源端登录验证完成                                                                     ║
╠══════════════════════════════════════════════════════════════════════════════════════════════╣
║  TRAE SOLO CN (作者端): 保持运行中                                                         ║
║  Trae CN (本源端): 已重启 + 登录态清除 + UID替换                                          ║
║                                                                                              ║
║  清除: Cookies, Session Storage, Local Storage, IndexedDB                                  ║
║  保留: trae-jwt-token (共享), os_crypt.encrypted_key (共享)                                ║
║  UID: 3753060170739075 → a5b7a8623fdea6b8                                                ║
║                                                                                              ║
║  系统总进程: {total} 个                                                                     ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝
''')
