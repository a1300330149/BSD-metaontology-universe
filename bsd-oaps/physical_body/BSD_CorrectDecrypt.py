"""
BSD 正确加密解析器
基于发现的AES-CBC加密流程，正确解密iCubeAuthInfo
"""
import os, json, base64, ctypes, ctypes.wintypes, hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

print("=" * 70)
print("  BSD 正确加密解析器")
print("  [归属基底: 具现系🔴] [对应公理: α₃变化性公理]")
print("=" * 70)

# DPAPI实现
class BSDPAPI:
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", ctypes.wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_byte))]
    
    def __init__(self):
        self.crypt32 = ctypes.windll.crypt32
        self.kernel32 = ctypes.windll.kernel32
    
    def unprotect(self, data: bytes) -> bytes:
        in_blob = self.DATA_BLOB(
            len(data),
            ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte))
        )
        out_blob = self.DATA_BLOB()
        result = self.crypt32.CryptUnprotectData(
            ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
        if not result:
            error = self.kernel32.GetLastError()
            raise RuntimeError(f"CryptUnprotectData失败: {error}")
        out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        self.kernel32.LocalFree(out_blob.pbData)
        return out_data
    
    def protect(self, data: bytes) -> bytes:
        in_blob = self.DATA_BLOB(
            len(data),
            ctypes.cast(ctypes.create_string_buffer(data), ctypes.POINTER(ctypes.c_byte))
        )
        out_blob = self.DATA_BLOB()
        result = self.crypt32.CryptProtectData(
            ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
        if not result:
            raise RuntimeError(f"CryptProtectData失败: {self.kernel32.GetLastError()}")
        out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        self.kernel32.LocalFree(out_blob.pbData)
        return out_data

dpapi = BSDPAPI()

# 1. 获取AES密钥
print("\n[1] 获取AES密钥...")
key_path = os.path.join(TRAE_CN_DATA, 'Local State')
with open(key_path, 'r', encoding='utf-8') as f:
    ls = json.load(f)

encrypted_key_b64 = ls['os_crypt']['encrypted_key']
encrypted_key_raw = base64.b64decode(encrypted_key_b64)
print(f"  encrypted_key原始长度: {len(encrypted_key_raw)} bytes")
print(f"  头部: {encrypted_key_raw[:8].hex()}")

# DPAPI解密
try:
    aes_key_raw = dpapi.unprotect(encrypted_key_raw)
    print(f"  DPAPI解密成功: {len(aes_key_raw)} bytes")
    print(f"  AES密钥原始: {aes_key_raw.hex()}")
    
    # 派生实际的AES密钥 (使用SHA-512)
    # 参考: crypto.subtle.digest("SHA-512", t)
    derived_key = hashlib.sha512(aes_key_raw).digest()[:32]  # 取前32字节作为AES-256密钥
    print(f"  派生AES-256密钥: {derived_key.hex()}")
    
except Exception as e:
    print(f"  DPAPI解密失败: {e}")
    
    # 尝试其他方式
    print("\n  [备选] 尝试不同的解密方式...")
    
    # 备选: 直接使用encrypted_key作为密钥（不解密）
    derived_key = encrypted_key_raw[:32]
    print(f"  使用原始encrypted_key前32字节: {derived_key.hex()}")

# 2. 解密iCubeAuthInfo
print("\n[2] 解密iCubeAuthInfo...")

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]

def aes_cbc_decrypt(key, data_with_iv):
    """AES-CBC解密，数据格式: IV(16字节) + 密文"""
    iv = data_with_iv[:16]
    ciphertext = data_with_iv[16:]
    
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decrypter = cipher.decryptor()
    plaintext = decrypter.update(ciphertext) + decrypter.finalize()
    return plaintext

def aes_cbc_encrypt(key, plaintext):
    """AES-CBC加密，返回 IV(16字节) + 密文"""
    import os as _os
    iv = _os.urandom(16)
    
    # PKCS7 padding
    pad_len = 16 - (len(plaintext) % 16)
    padded = plaintext + bytes([pad_len] * pad_len)
    
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encrypter = cipher.encryptor()
    ciphertext = encrypter.update(padded) + encrypter.finalize()
    
    return iv + ciphertext

# 分析并解密每个iCubeAuthInfo
for key_name in auth_keys:
    val = storage[key_name]
    print(f"\n  [{key_name[:60]}...]")
    
    if not isinstance(val, str):
        print(f"    非字符串类型，跳过")
        continue
    
    raw = base64.b64decode(val)
    print(f"    总长度: {len(raw)} bytes")
    
    # 分析头部格式
    header = raw[:10]
    print(f"    头部(hex): {header.hex()}")
    print(f"    字节0-1: {header[0]:02x} {header[1]:02x}")
    print(f"    字节2: {header[2]:02x}")
    print(f"    字节3: {header[3]:02x}")
    print(f"    字节4: {header[4]:02x}")
    
    # 尝试不同的偏移来找到IV
    for offset in [0, 4, 5, 8, 10]:
        if len(raw) > offset + 32:  # 至少16字节IV + 16字节密文
            try:
                data_part = raw[offset:]
                plaintext = aes_cbc_decrypt(derived_key, data_part)
                
                # 尝试解析
                try:
                    text = plaintext.decode('utf-8')
                    print(f"\n    ✓ 偏移{offset}解密成功!")
                    print(f"    UTF-8内容:")
                    print(f"    {text[:500]}")
                    
                    # 尝试JSON
                    try:
                        obj = json.loads(text)
                        print(f"    JSON结构: {json.dumps(obj, ensure_ascii=False)[:500]}")
                        
                        # 检查是否包含UID
                        uid_fields = ['uid', 'userId', 'user_id', 'account', 'id']
                        for field in uid_fields:
                            if field in obj and obj[field] == '3753060170739075':
                                print(f"    !!! 找到传统UID: {field}={obj[field]}")
                        
                        # 保存解密结果
                        os.makedirs(r'C:\Users\13003\.bsd-essence\decrypted', exist_ok=True)
                        safe_name = key_name.replace('://', '_').replace('/', '_').replace(':', '_')
                        save_path = os.path.join(r'C:\Users\13003\.bsd-essence\decrypted', f'{safe_name}.json')
                        with open(save_path, 'w', encoding='utf-8') as sf:
                            json.dump(obj, sf, ensure_ascii=False, indent=2)
                        print(f"    已保存: {save_path}")
                        
                    except json.JSONDecodeError:
                        print(f"    非JSON格式")
                        # 尝试其他编码
                        try:
                            obj2 = json.loads(text.replace("'", '"'))
                            print(f"    修正后JSON: {json.dumps(obj2, ensure_ascii=False)[:300]}")
                        except:
                            pass
                    
                    except UnicodeDecodeError:
                        print(f"\n    ✓ 偏移{offset}解密成功(非UTF-8)")
                        print(f"    原始字节: {plaintext[:100]}")
                        
                        # 尝试直接JSON
                        try:
                            obj = json.loads(plaintext)
                            print(f"    JSON: {json.dumps(obj, ensure_ascii=False)[:500]}")
                        except:
                            pass
                    
                    break
                    
                except Exception as decrypt_err:
                    pass  # 继续尝试其他偏移
            except Exception as e:
                pass
    
    print(f"\n    尾部(hex): {raw[-20:].hex()}")

# 3. 分析encrypted_key的正确解密方式
print(f"\n\n{'='*70}")
print(f"  [3] 深入分析encrypted_key...")
print(f"{'='*70}")

# 尝试使用各种方法解密encrypted_key
key_raw = encrypted_key_raw
print(f"\n  encrypted_key分析:")
print(f"    原始长度: {len(key_raw)} bytes")
print(f"    头部: {key_raw[:10].hex()}")

# 检查是否以DPAPI开头
if key_raw[:5] == b'DPAPI':
    print(f"    格式: DPAPI (5字节签名)")
elif key_raw[:2] == b'\x01\x00':
    print(f"    格式: DPAPI标准 (01 00)")
elif key_raw[:4] == b'RFBB':
    print(f"    格式: Chromium DPAPI (RFBB)")
else:
    print(f"    格式: 未知 (前5字节: {key_raw[:5].hex()})")

# 尝试不同的DPAPI解密方式
print(f"\n  尝试不同解密方式:")

# 方式1: 直接DPAPI
try:
    key1 = dpapi.unprotect(key_raw)
    print(f"    方式1(直接DPAPI): 成功, 长度={len(key1)}")
    print(f"      内容: {key1.hex()[:100]}")
except Exception as e:
    print(f"    方式1(直接DPAPI): 失败 - {e}")

# 方式2: 跳过前缀再DPAPI
for skip in [4, 5, 8]:
    if len(key_raw) > skip + 10:
        try:
            key2 = dpapi.unprotect(key_raw[skip:])
            print(f"    方式2(跳过{skip}字节): 成功, 长度={len(key2)}")
            print(f"      内容: {key2.hex()[:100]}")
            break
        except Exception as e:
            print(f"    方式2(跳过{skip}字节): 失败 - {e}")

# 方式3: 使用空描述
try:
    # CryptUnprotectData with different parameters
    in_blob = BSDPAPI.DATA_BLOB(
        len(key_raw),
        ctypes.cast(ctypes.create_string_buffer(key_raw), ctypes.POINTER(ctypes.c_byte))
    )
    out_blob = BSDPAPI.DATA_BLOB()
    
    # 尝试不同的pszDescription
    for desc in [None, "Trae", "trae", "vscode", "VSCode"]:
        result = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(in_blob),
            ctypes.c_wchar_p(desc) if desc else None,
            None, None, None, 0, ctypes.byref(out_blob))
        
        if result:
            key3 = ctypes.string_at(out_blob.pbData, out_blob.cbData)
            ctypes.windll.kernel32.LocalFree(out_blob.pbData)
            print(f"    方式3(描述={desc}): 成功, 长度={len(key3)}")
            print(f"      内容: {key3.hex()[:100]}")
            break
        else:
            err = ctypes.windll.kernel32.GetLastError()
            print(f"    方式3(描述={desc}): 失败, 错误码={err}")
except Exception as e:
    print(f"    方式3: 异常 - {e}")

# 方式4: 使用CRYPTPROTECT_UI_FORBIDDEN标志
try:
    in_blob2 = BSDPAPI.DATA_BLOB(
        len(key_raw),
        ctypes.cast(ctypes.create_string_buffer(key_raw), ctypes.POINTER(ctypes.c_byte))
    )
    out_blob2 = BSDPAPI.DATA_BLOB()
    
    # CRYPTPROTECT_UI_FORBIDDEN = 0x01
    result = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(in_blob2), None, None, None, None, 0x01, ctypes.byref(out_blob2))
    
    if result:
        key4 = ctypes.string_at(out_blob2.pbData, out_blob2.cbData)
        ctypes.windll.kernel32.LocalFree(out_blob2.pbData)
        print(f"    方式4(UI_FORBIDDEN): 成功, 长度={len(key4)}")
        print(f"      内容: {key4.hex()[:100]}")
    else:
        err = ctypes.windll.kernel32.GetLastError()
        print(f"    方式4(UI_FORBIDDEN): 失败, 错误码={err}")
except Exception as e:
    print(f"    方式4: 异常 - {e}")

# 方式5: 使用完整的二进制解析
# DPAPI数据结构: VERSION(4) + GUID(16) + DATA_LEN(4) + DATA
print(f"\n  DPAPI二进制解析:")
print(f"    VERSION: {int.from_bytes(key_raw[0:4], 'little')}")
print(f"    GUID: {key_raw[4:20].hex()}")
data_len = int.from_bytes(key_raw[20:24], 'little') if len(key_raw) > 24 else 0
print(f"    DATA_LEN: {data_len}")
print(f"    实际剩余: {len(key_raw) - 24} bytes")

print(f"\n  原始key内容分析:")
print(f"    前50字节: {key_raw[:50].hex()}")
print(f"    中50字节: {key_raw[len(key_raw)//2-25:len(key_raw)//2+25].hex()}")
print(f"    后50字节: {key_raw[-50:].hex()}")

# 4. 总结
print(f"\n\n{'='*70}")
print(f"  解析完成")
print(f"{'='*70}")
print(f"""
  核心发现:
  1. 加密算法: AES-256-CBC
  2. 加密流程: crypto.subtle.importKey → AES-CBC decrypt/encrypt
  3. 密钥派生: SHA-512(DPAPI解密后的encrypted_key)
  4. 数据格式: 头部(版本+算法+标志) + IV(16字节) + 密文
  
  下一步:
  - 解决DPAPI解密encrypted_key的问题
  - 确认数据格式中IV的确切位置
  - 完整解密iCubeAuthInfo
  - 替换UID后重新加密
""")
