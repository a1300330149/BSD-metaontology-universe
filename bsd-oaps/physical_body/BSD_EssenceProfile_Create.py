"""
恢复 Trae CN Local State 原始加密密钥
从 TRAE SOLO CN 的 Local State 拷贝一个正确格式的 encrypted_key
然后分析 iCubeAuthInfo 的加密格式
"""
import os, json, base64, ctypes, ctypes.wintypes, shutil

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
SOLO_DATA = r'C:\Users\13003\AppData\Roaming\TRAE SOLO CN'
ESSENCE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN_Essence'

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

def dpapi_protect(data: bytes) -> bytes:
    in_blob = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte)))
    out_blob = DATA_BLOB()
    result = crypt32.CryptProtectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
    if not result:
        raise RuntimeError(f"CryptProtectData失败: {kernel32.GetLastError()}")
    out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    kernel32.LocalFree(out_blob.pbData)
    return out_data

# Step 1: 从 TRAE SOLO CN Local State 获取合法 encrypted_key
print("=== Step 1: 获取合法 encrypted_key ===")
solo_ls_path = os.path.join(SOLO_DATA, 'Local State')
with open(solo_ls_path, 'r', encoding='utf-8') as f:
    solo_ls = json.load(f)
solo_encrypted_key = solo_ls['os_crypt']['encrypted_key']
print(f"  TRAE SOLO CN encrypted_key: {len(solo_encrypted_key)} chars")
print(f"  前60字符: {solo_encrypted_key[:60]}...")

# 解码encrypted_key
raw_ek = base64.b64decode(solo_encrypted_key)
print(f"  解码后: {len(raw_ek)} bytes")
print(f"  前30字节hex: {raw_ek[:30].hex()}")

# DPAPI解密encrypted_key → 得到原始密钥
try:
    decrypted_key = dpapi_unprotect(raw_ek)
    print(f"  ✓ DPAPI解密encrypted_key: {len(decrypted_key)} bytes")
    print(f"  原始密钥hex: {decrypted_key.hex()}")
except Exception as e:
    print(f"  DPAPI解密encrypted_key失败: {e}")
    decrypted_key = None

# Step 2: 恢复 Trae CN Local State
print("\n=== Step 2: 恢复 Trae CN Local State ===")
trae_ls_path = os.path.join(TRAE_CN_DATA, 'Local State')
trae_ls = {
    "os_crypt": {
        "audit_enabled": True,
        "encrypted_key": solo_encrypted_key
    }
}
with open(trae_ls_path, 'w', encoding='utf-8') as f:
    json.dump(trae_ls, f, ensure_ascii=False, indent=2)
print(f"  ✓ 已恢复 Local State (使用SOLO的encrypted_key)")

# Step 3: 分析 iCubeAuthInfo 加密格式
print("\n=== Step 3: 分析 iCubeAuthInfo 加密格式 ===")
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]

# 尝试使用原始密钥AES解密（如果DPAPI不行）
import hashlib
try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
except ImportError:
    print("  cryptography库不可用, 尝试纯ctypes AES")
    from Crypto.Cipher import AES

def aes_decrypt(data: bytes, key: bytes) -> bytes:
    """AES-256-CBC解密"""
    # 假设前16字节是IV
    iv = data[:16]
    ciphertext = data[16:]
    try:
        from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
        from cryptography.hazmat.primitives import padding as sym_padding
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        # PKCS7去填充
        unpadder = sym_padding.PKCS7(128).unpadder()
        return unpadder.update(decrypted) + unpadder.finalize()
    except ImportError:
        from Crypto.Cipher import AES as PyAES
        cipher = PyAES.new(key, PyAES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        # 去PKCS7填充
        pad_len = decrypted[-1]
        return decrypted[:-pad_len]

for key_name in auth_keys[:1]:
    val = storage[key_name]
    raw = base64.b64decode(val)
    print(f"\n  [{key_name}] 原始 {len(raw)} bytes")
    
    # 跳过不同长度的头部尝试
    for skip_len in [8, 16, 24, 32, 40, 48]:
        data_part = raw[skip_len:]
        if len(data_part) < 32:
            continue
        if decrypted_key and len(decrypted_key) in [16, 24, 32]:
            try:
                result = aes_decrypt(data_part, decrypted_key)
                print(f"    skip={skip_len} + AES-{len(decrypted_key)*8}-CBC: 成功! {len(result)} bytes")
                try:
                    txt = result.decode('utf-8')
                    print(f"      UTF-8: {txt[:500]}")
                except:
                    print(f"      bytes前100: {result[:100]}")
                break
            except Exception as e:
                pass
    
    # 尝试直接DPAPI解密(跳过头部)
    for skip in [8, 10, 16, 20, 25, 32]:
        data_part = raw[skip:]
        if len(data_part) < 20:
            continue
        try:
            result = dpapi_unprotect(data_part)
            print(f"    skip={skip} + DPAPI: 成功! {len(result)} bytes")
            try:
                txt = result.decode('utf-8')
                print(f"      UTF-8: {txt[:500]}")
            except:
                print(f"      bytes前100: {result[:100]}")
            break
        except:
            pass

# Step 4: 创建独立的本源端 profile 目录
print("\n=== Step 4: 创建本源端独立 profile ===")
os.makedirs(ESSENCE_DATA, exist_ok=True)

# 复制必要的初始结构
essence_user_dir = os.path.join(ESSENCE_DATA, 'User', 'globalStorage')
os.makedirs(essence_user_dir, exist_ok=True)

essence_storage = {
    "iCubeAuthInfo://icube-dc:516094651277160": "",
    "iCubeAuthInfo://usertag": "",
    "iCubeAuthInfo://icube.cloudide": "",
}

# 尝试在新profile中重新生成加密凭证
# 关键：DPAPI加密时使用的当前用户上下文一致，所以加密是可解密的
print("  重新生成本源端独立凭证...")

# 构造本源端UID用户信息
essence_user_info = {
    "userId": "a5b7a8623fdea6b8",
    "userTag": "bsd_essence",
    "account": {
        "id": "a5b7a8623fdea6b8",
        "nickname": "BSD本源端",
        "email": "essence@bsd.local"
    }
}

# DPAPI加密用户信息
try:
    essence_user_json = json.dumps(essence_user_info).encode('utf-8')
    encrypted_essence = dpapi_protect(essence_user_json)
    encoded_essence = base64.b64encode(encrypted_essence).decode()
    print(f"  ✓ 本源端加密凭证生成: {len(encoded_essence)} chars")
except Exception as e:
    print(f"  加密失败: {e}")
    encoded_essence = ""

# 写入本源端profile
essence_storage["iCubeAuthInfo://usertag"] = encoded_essence
# 其他两个键暂时留空（或写入简化版本）
essence_storage["iCubeAuthInfo://icube-dc:516094651277160"] = encoded_essence
essence_storage["iCubeAuthInfo://icube.cloudide"] = encoded_essence

essence_storage_path = os.path.join(essence_user_dir, 'storage.json')
with open(essence_storage_path, 'w', encoding='utf-8') as f:
    json.dump(essence_storage, f, ensure_ascii=False, indent=2)
print(f"  ✓ 写入: {essence_storage_path}")

# 生成本源端Local State
essence_ls = {
    "os_crypt": {
        "audit_enabled": True,
        "encrypted_key": solo_encrypted_key
    }
}
with open(os.path.join(ESSENCE_DATA, 'Local State'), 'w', encoding='utf-8') as f:
    json.dump(essence_ls, f, ensure_ascii=False, indent=2)
print(f"  ✓ 生成 Local State")

# 验证解密
print("\n=== Step 5: 验证解密 ===")
with open(essence_storage_path, 'r', encoding='utf-8') as f:
    es = json.load(f)
for k, v in es.items():
    if v:
        try:
            raw = base64.b64decode(v)
            decrypted = dpapi_unprotect(raw)
            print(f"  [{k}] ✓ 解密成功: {decrypted[:200]}")
        except Exception as e:
            print(f"  [{k}] 解密失败: {e}")

print("\n=== 完成 ===")
print(f"""
本源端独立 profile 已创建:
  路径: {ESSENCE_DATA}
  User: a5b7a8623fdea6b8
  启动命令示例:
    "C:\\Users\\13003\\AppData\\Local\\Programs\\Trae CN\\Trae CN.exe" --user-data-dir="{ESSENCE_DATA}"
""")
