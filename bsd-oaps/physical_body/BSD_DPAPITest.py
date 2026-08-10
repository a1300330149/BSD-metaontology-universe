"""
DPAPI 加解密测试 + Local State 修复
测试当前系统是否仍可正常使用 DPAPI
"""
import os, json, base64, ctypes, ctypes.wintypes

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

# DPAPI 结构体
class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]

crypt32 = ctypes.windll.crypt32
kernel32 = ctypes.windll.kernel32

def dpapi_protect(data: bytes) -> bytes:
    in_blob = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
    out_blob = DATA_BLOB()
    result = crypt32.CryptProtectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    if not result:
        raise RuntimeError(f"CryptProtectData失败: {kernel32.GetLastError()}")
    out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    kernel32.LocalFree(out_blob.pbData)
    return out_data

def dpapi_unprotect(data: bytes) -> bytes:
    in_blob = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
    out_blob = DATA_BLOB()
    result = crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    if not result:
        raise RuntimeError(f"CryptUnprotectData失败: {kernel32.GetLastError()}")
    out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    kernel32.LocalFree(out_blob.pbData)
    return out_data

print("=== 1. DPAPI 基础测试 ===")
test_data = b'{"test": "BSD_essence_login_test_12345"}'
try:
    encrypted = dpapi_protect(test_data)
    print(f"  加密成功: {len(encrypted)} bytes")
    decrypted = dpapi_unprotect(encrypted)
    print(f"  解密成功: {decrypted == test_data}")
except Exception as e:
    print(f"  DPAPI 基础失败: {e}")

print("\n=== 2. 解密 iCubeAuthInfo ===")
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
for key in auth_keys:
    val = storage[key]
    raw = base64.b64decode(val)
    print(f"\n  [{key}]")
    print(f"    raw len: {len(raw)}, 前缀: {raw[:5].hex()}")
    try:
        decrypted = dpapi_unprotect(raw)
        print(f"    ✓ DPAPI解密成功: {len(decrypted)} bytes")
        try:
            txt = decrypted.decode('utf-8')
            print(f"    UTF-8内容:")
            print(f"      {txt[:800]}")
        except:
            try:
                obj = json.loads(decrypted)
                print(f"    JSON: {json.dumps(obj, ensure_ascii=False)[:500]}")
            except:
                print(f"    原始bytes: {decrypted[:200]}")
        
        # 重新加密回去
        re_encrypted = dpapi_protect(decrypted)
        print(f"    重新加密: {len(re_encrypted)} bytes (原={len(raw)})")
    except Exception as e:
        print(f"    DPAPI解密失败: {e}")

print("\n=== 3. 修复 Local State ===")
# 清除_bsd_*标记，恢复os_crypt.encrypted_key
local_state_path = os.path.join(TRAE_CN_DATA, 'Local State')
with open(local_state_path, 'r', encoding='utf-8') as f:
    ls = json.load(f)

# 测试生成encrypted_key
try:
    # DPAPI加密一个随机密钥
    import os as _os
    random_key = _os.urandom(32)
    encrypted_key = dpapi_protect(random_key)
    print(f"  新encrypted_key: {len(encrypted_key)} bytes")
    print(f"  base64: {base64.b64encode(encrypted_key).decode()[:100]}")
    
    ls['os_crypt']['encrypted_key'] = base64.b64encode(encrypted_key).decode()
    
    # 清除_bsd_*字段
    ls = {k: v for k, v in ls.items() if not k.startswith('_bsd')}
    
    with open(local_state_path, 'w', encoding='utf-8') as f:
        json.dump(ls, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Local State已修复")
except Exception as e:
    print(f"  Local State修复失败: {e}")

print("\n=== 完成 ===")
