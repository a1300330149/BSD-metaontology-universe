"""
分析真实的 iCubeAuthInfo 完整字段结构
从传统UID已解密的auth中学习真实结构
"""
import os, json, base64, ctypes, ctypes.wintypes

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

# DPAPI
class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]

crypt32 = ctypes.windll.crypt32
kernel32 = ctypes.windll.kernel32

def dpapi_unprotect(data: bytes) -> bytes:
    in_blob = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
    out_blob = DATA_BLOB()
    result = crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    if not result:
        raise RuntimeError(f"CryptUnprotectData失败: {kernel32.GetLastError()}")
    out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    kernel32.LocalFree(out_blob.pbData)
    return out_data

# 读取当前 Trae CN storage
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
print(f"当前 Trae CN storage.json 中 {len(auth_keys)} 个 iCubeAuthInfo\n")

# 读取 JWT
jwt_path = os.path.join(TRAE_CONFIG, 'trae-jwt-token')
if os.path.exists(jwt_path):
    with open(jwt_path, 'r') as f:
        token = f.read().strip()
    parts = token.split('.')
    if len(parts) >= 2:
        payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
        print(f"JWT payload: {json.dumps(payload, ensure_ascii=False, indent=2)[:800]}")

# 读取 bsd_essence_user_info.json (本源端已注入的用户信息)
user_info_path = os.path.join(TRAE_CONFIG, 'bsd_essence_user_info.json')
if os.path.exists(user_info_path):
    with open(user_info_path, 'r', encoding='utf-8') as f:
        ui = json.load(f)
    print(f"\nbsd_essence_user_info.json:")
    print(json.dumps(ui, ensure_ascii=False, indent=2)[:800])

# 读取 bsd_essence_independent.json
indep_path = os.path.join(TRAE_CONFIG, 'bsd_essence_independent.json')
if os.path.exists(indep_path):
    with open(indep_path, 'r', encoding='utf-8') as f:
        indep = json.load(f)
    print(f"\nbsd_essence_independent.json:")
    print(json.dumps(indep, ensure_ascii=False, indent=2)[:800])

# 读取 bsd_essence_login.json
login_path = os.path.join(TRAE_CONFIG, 'bsd_essence_login.json')
if os.path.exists(login_path):
    with open(login_path, 'r', encoding='utf-8') as f:
        login = json.load(f)
    print(f"\nbsd_essence_login.json:")
    print(json.dumps(login, ensure_ascii=False, indent=2)[:800])
