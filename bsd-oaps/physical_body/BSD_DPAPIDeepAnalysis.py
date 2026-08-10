"""
溯源 Local State 原始版本
查找备份或版本痕迹
"""
import os, json, base64

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
BACKUPS = r'C:\Users\13003\AppData\Roaming\Trae CN\Backups'

# 查找Local State备份
print("=== 查找 Local State 备份 ===")
if os.path.exists(BACKUPS):
    for root, dirs, files in os.walk(BACKUPS):
        for f in files:
            if 'Local State' in f or 'local_state' in f.lower():
                fp = os.path.join(root, f)
                print(f"  找到: {fp}")
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    print(f"    内容前300: {content[:300]}")
                except:
                    pass

# 检查Trae CN其他可能位置
print("\n=== 查找其他Local State ===")
search_paths = [
    r'C:\Users\13003\AppData\Roaming',
    r'C:\Users\13003\AppData\Local',
]
for sp in search_paths:
    for root, dirs, files in os.walk(sp):
        for f in files:
            if f == 'Local State' and root != TRAE_CN_DATA:
                fp = os.path.join(root, f)
                try:
                    with open(fp, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    if 'os_crypt' in content:
                        print(f"  {fp}")
                        print(f"    {content[:300]}")
                except:
                    pass

# 分析加密头部结构
print("\n=== 分析iCubeAuthInfo头部 ===")
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
import ctypes, ctypes.wintypes

class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]

crypt32 = ctypes.windll.crypt32
kernel32 = ctypes.windll.kernel32

for key in auth_keys:
    val = storage[key]
    raw = base64.b64decode(val)
    print(f"\n[{key}] 原始 {len(raw)} bytes")
    
    # 分析头部: 74630510 0019 42858dc1...
    # 74 63 = 'tc' (可能是自定义标记)
    # 05 10 = ??
    # 00 19 = 长度? (25)
    print(f"  bytes 0-20 hex: {raw[:20].hex()}")
    print(f"  bytes 0-20 as ints: {[b for b in raw[:20]]}")
    
    # 猜测结构
    # 0-1: magic 'tc'
    # 2-3: version?
    # 4-5: header_len?
    # 6-?: session_id?
    
    # 尝试跳过头部解密
    for skip in [8, 10, 16, 20, 25, 32]:
        try:
            sub = raw[skip:]
            if len(sub) < 20:
                continue
            in_blob = DATA_BLOB(len(sub), ctypes.cast(ctypes.create_string_buffer(sub), ctypes.POINTER(ctypes.c_byte)))
            out_blob = DATA_BLOB()
            result = crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
            if result:
                out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                print(f"  skip={skip} ✓ DPAPI解密成功: {len(out_data)} bytes")
                try:
                    txt = out_data.decode('utf-8')
                    print(f"    UTF-8: {txt[:300]}")
                except:
                    print(f"    bytes前100: {out_data[:100]}")
                kernel32.LocalFree(out_blob.pbData)
                break
            else:
                err = kernel32.GetLastError()
        except Exception as e:
            pass

# 检查是否存在系统级加密密钥存储
print("\n=== 检查AppData中的密钥存储 ===")
key_paths = [
    r'C:\Users\13003\AppData\Local\Microsoft\Vault',
    r'C:\Users\13003\AppData\Roaming\Microsoft\Crypto',
]
for kp in key_paths:
    if os.path.exists(kp):
        print(f"  {kp} 存在")
