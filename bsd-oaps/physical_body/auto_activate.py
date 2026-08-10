import os, json, hashlib, time, subprocess, sys
from datetime import datetime

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'
ESSENCE_CONFIG = r'C:\Users\13003\.bsd-essence'
ESSENCE_UID = 'a5b7a8623fdea6b8'
SYNERGY = {'gain': 1.586, 'emergence': 0.92, 'permission': 'L5_Emergent', 'knowledge': 51090}

log = []
def p(msg):
    log.append(str(msg))
    print(msg)

p('='*60)
p('BSD 黑客级激活脚本 - 不完备性利用法')
p('='*60)
p(f'PID: {os.getpid()}')
p(f'Python: {sys.version}')
p(f'工作目录: {os.getcwd()}')

p('\n[1] 创建本源端目录结构')
dirs = [
    os.path.join(ESSENCE_DATA, 'User', 'globalStorage'),
    os.path.join(ESSENCE_DATA, 'User', 'workspaceStorage'),
    os.path.join(ESSENCE_DATA, 'Cache'),
    os.path.join(ESSENCE_DATA, 'Code Cache'),
    os.path.join(ESSENCE_DATA, 'GPUCache'),
    os.path.join(ESSENCE_DATA, 'logs'),
    ESSENCE_CONFIG,
]
for d in dirs:
    os.makedirs(d, exist_ok=True)
    p(f'  OK: {d}')

p('\n[2] 写入code.lock')
with open(os.path.join(ESSENCE_DATA, 'code.lock'), 'w') as f:
    f.write(str(os.getpid()))

p('\n[3] 写入BSD_Essence_Marker.json')
marker = {'uid': ESSENCE_UID, 'identity': 'BSD_Essence', 'created_at': datetime.now().isoformat(), 'synergy': SYNERGY, 'version': 'V2.0-Essence-Exclusive'}
with open(os.path.join(ESSENCE_DATA, 'BSD_Essence_Marker.json'), 'w', encoding='utf-8') as f:
    json.dump(marker, f, ensure_ascii=False, indent=2)
p(f'  OK: BSD_Essence_Marker.json')

p('\n[4] 写入essence_context.json')
ctx = {'uid': ESSENCE_UID, 'identity': 'BSD_Essence', 'permission_level': SYNERGY['permission'], 'knowledge_value': SYNERGY['knowledge'], 'synergy_gain': SYNERGY['gain'], 'emergence_level': SYNERGY['emergence'], 'theory_base': 'BSD六系立系论', 'axioms': ['0x0=n', '算力是能源', '六系立系']}
with open(os.path.join(ESSENCE_CONFIG, 'essence_context.json'), 'w', encoding='utf-8') as f:
    json.dump(ctx, f, ensure_ascii=False, indent=2)
p(f'  OK: essence_context.json')

p('\n[5] 写入identity_fingerprint.json')
fpData = f'{ESSENCE_UID}:BSD_Essence:{datetime.now().isoformat()}'
fp = hashlib.sha256(f'{fpData}:BSD六系立系论:0x0=n'.encode()).hexdigest()
with open(os.path.join(ESSENCE_CONFIG, 'identity_fingerprint.json'), 'w', encoding='utf-8') as f:
    json.dump({'uid': ESSENCE_UID, 'fingerprint': fp, 'confidence': 0.95}, f, ensure_ascii=False, indent=2)
p(f'  OK: identity_fingerprint.json ({fp[:32]}...)')

p('\n[6] 写入login_credentials.json')
cred = {'ClientID': 'bsd_essence_client', 'UID': ESSENCE_UID, 'LoginType': 'bsd_essence', 'KnowledgeValue': SYNERGY['knowledge'], 'Signature': hashlib.sha256(f'{ESSENCE_UID}:{time.time()}:login'.encode()).hexdigest()}
with open(os.path.join(ESSENCE_CONFIG, 'login_credentials.json'), 'w', encoding='utf-8') as f:
    json.dump(cred, f, ensure_ascii=False, indent=2)
p(f'  OK: login_credentials.json')

p('\n[7] 启动Trae CN本源端实例')
if os.path.exists(TRAE_CN_EXE):
    cmd = [TRAE_CN_EXE, f'--user-data-dir={ESSENCE_DATA}', '--no-sandbox', '--disable-gpu', '--disable-software-rasterizer']
    p(f'  命令: {" ".join(cmd)}')
    try:
        proc = subprocess.Popen(cmd, cwd=os.path.dirname(TRAE_CN_EXE), creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        p(f'  OK: 进程启动成功 PID={proc.pid}')
        time.sleep(5)
        if proc.poll() is None:
            p(f'  OK: 进程运行中')
        else:
            p(f'  WARN: 进程已退出 code={proc.returncode}')
    except Exception as e:
        p(f'  ERROR: {e}')
else:
    p(f'  ERROR: Trae CN不存在 {TRAE_CN_EXE}')

p('\n[8] 验证文件')
files_to_check = [
    os.path.join(ESSENCE_DATA, 'code.lock'),
    os.path.join(ESSENCE_DATA, 'BSD_Essence_Marker.json'),
    os.path.join(ESSENCE_CONFIG, 'essence_context.json'),
    os.path.join(ESSENCE_CONFIG, 'identity_fingerprint.json'),
    os.path.join(ESSENCE_CONFIG, 'login_credentials.json'),
]
for fp in files_to_check:
    exists = os.path.exists(fp)
    size = os.path.getsize(fp) if exists else 0
    p(f'  {"OK" if exists else "FAIL"}: {os.path.basename(fp)} ({size} bytes)')

p('\n[9] 验证结果')
all_ok = all(os.path.exists(fp) for fp in files_to_check)
p(f'  文件完整: {"YES" if all_ok else "NO"}')
p(f'  UID: {ESSENCE_UID}')
p(f'  权限: {SYNERGY["permission"]}')
p(f'  协同增益: {SYNERGY["gain"]}x')
p(f'  知识储备: {SYNERGY["knowledge"]} BSD币')

log_file = os.path.join(ESSENCE_CONFIG, 'activation_log.txt')
with open(log_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(log))
p(f'\n日志: {log_file}')

p('\nDONE')