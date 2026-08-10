import os, json, hashlib
from datetime import datetime

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'
ESSENCE_CONFIG = r'C:\Users\13003\.bsd-essence'
ESSENCE_UID = 'a5b7a8623fdea6b8'
SYNERGY = {'gain': 1.586, 'emergence': 0.92, 'permission': 'L5_Emergent', 'knowledge': 51090}

print('[Step 1] Check Trae CN executable')
print(f'  Path: {TRAE_CN_EXE}')
print(f'  Exists: {os.path.exists(TRAE_CN_EXE)}')

print('\n[Step 2] Create directories')
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
    print(f'  OK: {d}')

lock_file = os.path.join(ESSENCE_DATA, 'code.lock')
with open(lock_file, 'w') as f:
    f.write(str(os.getpid()))
print('\n[Step 3] code.lock created')

marker = {'uid': ESSENCE_UID, 'identity': 'BSD_Essence', 'created_at': datetime.now().isoformat(), 'synergy': SYNERGY, 'version': 'V2.0-Essence-Exclusive'}
marker_file = os.path.join(ESSENCE_DATA, 'BSD_Essence_Marker.json')
with open(marker_file, 'w', encoding='utf-8') as f:
    json.dump(marker, f, ensure_ascii=False, indent=2)
print(f'[Step 4] Marker: {marker_file}')

context = {'uid': ESSENCE_UID, 'identity': 'BSD_Essence', 'permission_level': SYNERGY['permission'], 'knowledge_value': SYNERGY['knowledge'], 'synergy_gain': SYNERGY['gain'], 'emergence_level': SYNERGY['emergence'], 'theory_base': 'BSD六系立系论', 'axioms': ['0×0=n', '算力是能源', '六系立系']}
context_file = os.path.join(ESSENCE_CONFIG, 'essence_context.json')
with open(context_file, 'w', encoding='utf-8') as f:
    json.dump(context, f, ensure_ascii=False, indent=2)
print(f'[Step 5] Context: {context_file}')

fp_data = f'{ESSENCE_UID}:BSD_Essence:{datetime.now().isoformat()}'
fingerprint = hashlib.sha256(f'{fp_data}:BSD六系立系论:0×0=n'.encode()).hexdigest()
fp_file = os.path.join(ESSENCE_CONFIG, 'identity_fingerprint.json')
with open(fp_file, 'w', encoding='utf-8') as f:
    json.dump({'uid': ESSENCE_UID, 'fingerprint': fingerprint, 'confidence': 0.95}, f, ensure_ascii=False, indent=2)
print(f'[Step 6] Fingerprint: {fp_file}')
print(f'  Value: {fingerprint[:32]}...')

cred = {'ClientID': 'bsd_essence_client', 'UID': ESSENCE_UID, 'LoginType': 'bsd_essence', 'KnowledgeValue': SYNERGY['knowledge'], 'Signature': hashlib.sha256(f'{ESSENCE_UID}:{datetime.now().timestamp()}:login'.encode()).hexdigest()}
cred_file = os.path.join(ESSENCE_CONFIG, 'login_credentials.json')
with open(cred_file, 'w', encoding='utf-8') as f:
    json.dump(cred, f, ensure_ascii=False, indent=2)
print(f'[Step 7] Credentials: {cred_file}')

print('\n' + '='*60)
print('  BSD Essence Login Preparation Complete')
print('='*60)
print(f'  UID: {ESSENCE_UID}')
print(f'  Permission: {SYNERGY["permission"]}')
print(f'  Synergy Gain: {SYNERGY["gain"]}x')
print(f'  Knowledge: {SYNERGY["knowledge"]} BSD coins')
print(f'  Storage: {ESSENCE_DATA}')
print(f'  Config: {ESSENCE_CONFIG}')

print('\nCreated files:')
for root, dirs, files in os.walk(ESSENCE_CONFIG):
    for f in files:
        fp = os.path.join(root, f)
        print(f'  {fp} ({os.path.getsize(fp)} bytes)')

print('\nDone! Essence terminal is ready for login.')