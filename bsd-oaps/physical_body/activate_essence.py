import os, json, hashlib, time, subprocess
from datetime import datetime

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'
ESSENCE_CONFIG = r'C:\Users\13003\.bsd-essence'
ESSENCE_UID = 'a5b7a8623fdea6b8'
SYNERGY = {'gain': 1.586, 'emergence': 0.92, 'permission': 'L5_Emergent', 'knowledge': 51090}

os.makedirs(os.path.join(ESSENCE_DATA, 'User', 'globalStorage'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'User', 'workspaceStorage'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'Cache'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'Code Cache'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'GPUCache'), exist_ok=True)
os.makedirs(os.path.join(ESSENCE_DATA, 'logs'), exist_ok=True)
os.makedirs(ESSENCE_CONFIG, exist_ok=True)

with open(os.path.join(ESSENCE_DATA, 'code.lock'), 'w') as f:
    f.write(str(os.getpid()))

marker = {'uid': ESSENCE_UID, 'identity': 'BSD_Essence', 'created_at': datetime.now().isoformat(), 'synergy': SYNERGY, 'version': 'V2.0-Essence-Exclusive'}
with open(os.path.join(ESSENCE_DATA, 'BSD_Essence_Marker.json'), 'w', encoding='utf-8') as f:
    json.dump(marker, f, ensure_ascii=False, indent=2)

ctx = {'uid': ESSENCE_UID, 'identity': 'BSD_Essence', 'permission_level': SYNERGY['permission'], 'knowledge_value': SYNERGY['knowledge'], 'synergy_gain': SYNERGY['gain'], 'emergence_level': SYNERGY['emergence'], 'theory_base': 'BSD六系立系论', 'axioms': ['0×0=n', '算力是能源', '六系立系']}
with open(os.path.join(ESSENCE_CONFIG, 'essence_context.json'), 'w', encoding='utf-8') as f:
    json.dump(ctx, f, ensure_ascii=False, indent=2)

fp_data = f"{ESSENCE_UID}:BSD_Essence:{datetime.now().isoformat()}"
fp = hashlib.sha256(f"{fp_data}:BSD六系立系论:0×0=n".encode()).hexdigest()
with open(os.path.join(ESSENCE_CONFIG, 'identity_fingerprint.json'), 'w', encoding='utf-8') as f:
    json.dump({'uid': ESSENCE_UID, 'fingerprint': fp, 'confidence': 0.95}, f, ensure_ascii=False, indent=2)

cred = {'ClientID': 'bsd_essence_client', 'UID': ESSENCE_UID, 'LoginType': 'bsd_essence', 'KnowledgeValue': SYNERGY['knowledge'], 'Signature': hashlib.sha256(f"{ESSENCE_UID}:{time.time()}:login".encode()).hexdigest()}
with open(os.path.join(ESSENCE_CONFIG, 'login_credentials.json'), 'w', encoding='utf-8') as f:
    json.dump(cred, f, ensure_ascii=False, indent=2)

print("ESSENCE_FILES_CREATED")
print(f"UID={ESSENCE_UID}")
print(f"PERMISSION={SYNERGY['permission']}")
print(f"SYNERGY={SYNERGY['gain']}x")
print(f"KNOWLEDGE={SYNERGY['knowledge']}")
print(f"FINGERPRINT={fp[:32]}")

if os.path.exists(TRAE_CN_EXE):
    proc = subprocess.Popen([TRAE_CN_EXE, f'--user-data-dir={ESSENCE_DATA}', '--no-sandbox', '--disable-gpu'], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"TRAE_CN_STARTED PID={proc.pid}")
    time.sleep(5)
    if proc.poll() is None:
        print("TRAE_CN_RUNNING")
    else:
        print(f"TRAE_CN_EXITED code={proc.returncode}")
else:
    print(f"TRAE_CN_NOT_FOUND")

print("ALL_DONE")