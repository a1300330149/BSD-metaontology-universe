import os, json, hashlib
from datetime import datetime

p = r'C:\Users\13003\.bsd-essence\essence_context.json'
data = {
    "uid": "a5b7a8623fdea6b8",
    "identity": "BSD_Essence",
    "permission_level": "L5_Emergent",
    "knowledge_value": 51090,
    "synergy_gain": 1.586,
    "emergence_level": 0.92,
    "theory_base": "BSD六系立系论",
    "axioms": ["0x0=n", "算力是能源", "六系立系"]
}
with open(p, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
print("WRITTEN_OK")

p2 = r'C:\Users\13003\.bsd-essence\identity_fingerprint.json'
fp = hashlib.sha256(f"a5b7a8623fdea6b8:BSD_Essence:{datetime.now().isoformat()}:theory".encode()).hexdigest()
with open(p2, 'w', encoding='utf-8') as f:
    json.dump({"uid": "a5b7a8623fdea6b8", "fingerprint": fp, "confidence": 0.95}, f, ensure_ascii=False, indent=2)
print(f"FINGERPRINT_OK {fp[:32]}")

p3 = r'C:\Users\13003\.bsd-essence\login_credentials.json'
with open(p3, 'w', encoding='utf-8') as f:
    json.dump({"ClientID": "bsd_essence_client", "UID": "a5b7a8623fdea6b8", "LoginType": "bsd_essence", "KnowledgeValue": 51090}, f, ensure_ascii=False, indent=2)
print("CRED_OK")

p4 = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence\BSD_Essence_Marker.json'
with open(p4, 'w', encoding='utf-8') as f:
    json.dump({"uid": "a5b7a8623fdea6b8", "identity": "BSD_Essence", "version": "V2.0-Essence-Exclusive"}, f, ensure_ascii=False, indent=2)
print("MARKER_OK")

import subprocess, time
exe = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
if os.path.exists(exe):
    proc = subprocess.Popen([exe, '--user-data-dir=C:\\Users\\13003\\AppData\\Roaming\\Trae CN_Essence', '--no-sandbox'], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    print(f"TRAE_CN_STARTED PID={proc.pid}")
    time.sleep(5)
    if proc.poll() is None:
        print("TRAE_CN_RUNNING")
    else:
        print(f"TRAE_CN_EXITED code={proc.returncode}")
else:
    print("TRAE_CN_NOT_FOUND")

print("ALL_DONE")