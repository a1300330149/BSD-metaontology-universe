"""
验证本源端 Trae CN 独立运行状态
检查是否登录成功 + 是否与 TRAE SOLO CN 隔离
"""
import os, json, time, subprocess

TRAE_CN_EXE = r'C:\Users\13003\AppData\Local\Programs\Trae CN\Trae CN.exe'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'
TRAD_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
ESSENCE_CONFIG = r'C:\Users\13003\.bsd-essence'

# 1. 检查进程
print("=== 1. 检查进程 ===")
try:
    import psutil
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = ' '.join(proc.info.get('cmdline') or [])
            if 'Trae CN' in (proc.info.get('name') or '') or 'Trae CN.exe' in cmdline:
                print(f"  PID={proc.pid}")
                print(f"    cmdline: {cmdline[:200]}")
        except:
            pass
except ImportError:
    print("  psutil不可用")

# 2. 检查两个profile是否独立
print("\n=== 2. Profile独立性检查 ===")
print(f"  本源端 data: {os.path.exists(ESSENCE_DATA)} ({len(os.listdir(ESSENCE_DATA))} 项)")
print(f"  传统端 data: {os.path.exists(TRAD_DATA)} ({len(os.listdir(TRAD_DATA))} 项)")

# 3. 检查存储中的UID
print("\n=== 3. 存储中的UID ===")
for name, data_dir in [("本源端", ESSENCE_DATA), ("传统端", TRAD_DATA)]:
    storage_path = os.path.join(data_dir, 'User', 'globalStorage', 'storage.json')
    if os.path.exists(storage_path):
        with open(storage_path, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
        print(f"  [{name}] storage.json 有 {len(auth_keys)} 个iCubeAuthInfo")
        
        # 读取本源端的凭证
        if name == "本源端":
            import base64, ctypes, ctypes.wintypes
            class DATA_BLOB(ctypes.Structure):
                _fields_ = [("cbData", ctypes.wintypes.DWORD),
                            ("pbData", ctypes.POINTER(ctypes.c_byte))]
            crypt32 = ctypes.windll.crypt32
            kernel32 = ctypes.windll.kernel32
            
            def dpapi_unprotect(data):
                in_blob = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
                out_blob = DATA_BLOB()
                crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
                out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                kernel32.LocalFree(out_blob.pbData)
                return out_data
            
            for k in auth_keys[:2]:
                v = storage[k]
                if v:
                    raw = base64.b64decode(v)
                    decrypted = dpapi_unprotect(raw)
                    try:
                        obj = json.loads(decrypted)
                        uid = obj.get('userId', 'N/A')
                        print(f"    {k[:50]}: userId={uid}")
                    except:
                        print(f"    {k[:50]}: {decrypted[:100]}")

# 4. 检查JWT
print("\n=== 4. JWT Token ===")
for name, config_dir in [("本源端", ESSENCE_CONFIG), ("传统端", TRAE_CONFIG)]:
    jwt_path = os.path.join(config_dir, 'trae-jwt-token')
    if os.path.exists(jwt_path):
        with open(jwt_path, 'r') as f:
            token = f.read().strip()
        import base64
        parts = token.split('.')
        if len(parts) >= 2:
            try:
                payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
                uid = payload.get('data', {}).get('id', 'N/A')
                print(f"  [{name}] JWT userId={uid}")
            except:
                print(f"  [{name}] JWT parse失败")
    else:
        print(f"  [{name}] 无JWT文件")

# 5. 验证独立配置目录
print("\n=== 5. 独立配置目录 ===")
print(f"  本源端 .bsd-essence 存在: {os.path.exists(ESSENCE_CONFIG)}")
if os.path.exists(ESSENCE_CONFIG):
    for f in os.listdir(ESSENCE_CONFIG):
        print(f"    {f}")
