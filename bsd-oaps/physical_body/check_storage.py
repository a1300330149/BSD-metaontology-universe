import os, json

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'

print("=== Trae CN data ===")
for item in os.listdir(TRAE_CN_DATA)[:15]:
    fp = os.path.join(TRAE_CN_DATA, item)
    kind = 'DIR' if os.path.isdir(fp) else 'FILE'
    print(f"  {kind}: {item}")

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
if os.path.exists(storage_path):
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    print("\n=== storage.json keys with iCubeAuthInfo ===")
    auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
    print(f"  count: {len(auth_keys)}")
    for k in auth_keys[:3]:
        v = storage[k]
        print(f"  key={k[:80]}...  value_keys={list(v.keys()) if isinstance(v, dict) else type(v).__name__}")
        if isinstance(v, dict):
            for kk in list(v.keys())[:5]:
                vv = v[kk]
                if isinstance(vv, str) and len(vv) > 80:
                    print(f"    {kk}: {vv[:80]}...")
                else:
                    print(f"    {kk}: {vv}")

print("\n=== .trae-cn ===")
for item in os.listdir(TRAE_CONFIG)[:20]:
    fp = os.path.join(TRAE_CONFIG, item)
    kind = 'DIR' if os.path.isdir(fp) else 'FILE'
    size = os.path.getsize(fp) if os.path.isfile(fp) else 0
    print(f"  {kind}: {item} ({size} bytes)")

jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path):
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    parts = token.split('.')
    print(f"\n=== trae-jwt-token: {len(parts)} parts ===")
    if len(parts) >= 2:
        import base64
        try:
            payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            print(f"  payload keys: {list(payload.keys())}")
            print(f"  data.id: {payload.get('data', {}).get('id')}")
            print(f"  exp: {payload.get('exp')}")
        except Exception as e:
            print(f"  decode error: {e}")
