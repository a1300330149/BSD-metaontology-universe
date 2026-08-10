"""
深度分析 Trae CN 完整认证链路
定位DPAPI加密机制 + 所有存储位置
"""
import os, json, base64, sqlite3

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

# 检查Local State完整内容
local_state_path = os.path.join(TRAE_CN_DATA, 'Local State')
print("=== Local State 完整 ===")
with open(local_state_path, 'r', encoding='utf-8') as f:
    ls = json.load(f)
print(json.dumps(ls, ensure_ascii=False, indent=2))

# 检查 state.vscdb
vscdb_path = os.path.join(TRAE_CN_DATA, 'User', 'state.vscdb')
if os.path.exists(vscdb_path):
    print("\n=== state.vscdb tables ===")
    conn = sqlite3.connect(vscdb_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for t in tables:
        print(f"  table: {t[0]}")
    
    # 查找认证相关
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for table_name in [t[0] for t in tables]:
        try:
            cursor.execute(f"PRAGMA table_info({table_name})")
            cols = cursor.fetchall()
            print(f"\n  {table_name} columns: {[c[1] for c in cols]}")
            
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
            rows = cursor.fetchall()
            for row in rows[:3]:
                print(f"    {str(row)[:200]}")
        except Exception as e:
            pass
    conn.close()

# 检查 .trae-cn/bsd_* 文件
print("\n=== .trae-cn/bsd_* 认证相关 ===")
for fn in os.listdir(TRAE_CONFIG):
    if fn.startswith('bsd') and ('auth' in fn or 'login' in fn or 'essence' in fn or 'jwt' in fn):
        fp = os.path.join(TRAE_CONFIG, fn)
        with open(fp, 'r', encoding='utf-8') as f:
            content = f.read()
        print(f"\n  [{fn}] ({len(content)} bytes)")
        print(f"  {content[:400]}")

# 解密DPAPI
print("\n=== 尝试使用win32crypt解密DPAPI ===")
try:
    import win32crypt
    
    storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
    for key in auth_keys[:1]:
        val = storage[key]
        raw = base64.b64decode(val)
        print(f"\n  [{key}] raw={len(raw)} bytes")
        print(f"  前缀hex: {raw[:8].hex()}")
        
        # 尝试DPAPI解密
        try:
            decrypted = win32crypt.CryptUnprotectData(raw, None, None, None, 0)
            print(f"  ✓ DPAPI解密成功: {len(decrypted)} bytes")
            try:
                txt = decrypted.decode('utf-8')
                print(f"  UTF-8: {txt[:500]}")
            except:
                # 尝试JSON
                try:
                    obj = json.loads(decrypted)
                    print(f"  JSON: {json.dumps(obj, ensure_ascii=False)[:500]}")
                except:
                    print(f"  原始bytes: {decrypted[:200]}")
        except Exception as e:
            print(f"  DPAPI解密失败: {e}")
            
except ImportError:
    print("  win32crypt 不可用, 尝试 CryptUnprotectData via ctypes")
    import ctypes
    import ctypes.wintypes
    
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", ctypes.wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_byte))]
    
    pCryptUnprotectData = ctypes.windll.crypt32.CryptUnprotectData
    pCryptUnprotectData.restype = ctypes.wintypes.BOOL
    
    storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
    with open(storage_path, 'r', encoding='utf-8') as f:
        storage = json.load(f)
    
    auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
    for key in auth_keys[:1]:
        val = storage[key]
        raw = base64.b64decode(val)
        
        in_blob = DATA_BLOB(len(raw), ctypes.cast(ctypes.create_string_buffer(raw), ctypes.POINTER(ctypes.c_byte)))
        out_blob = DATA_BLOB()
        
        result = pCryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
        if result:
            decrypted = ctypes.string_at(out_blob.pbData, out_blob.cbData)
            print(f"\n  ✓ DPAPI解密成功: {len(decrypted)} bytes")
            try:
                txt = decrypted.decode('utf-8')
                print(f"  UTF-8: {txt[:600]}")
            except:
                try:
                    obj = json.loads(decrypted)
                    print(f"  JSON: {json.dumps(obj, ensure_ascii=False)[:600]}")
                except:
                    print(f"  原始bytes前300: {decrypted[:300]}")
            ctypes.windll.kernel32.LocalFree(out_blob.pbData)
        else:
            print(f"\n  CryptUnprotectData失败, error={ctypes.GetLastError()}")
