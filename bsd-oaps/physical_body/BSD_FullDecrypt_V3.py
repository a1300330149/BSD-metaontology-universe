"""
BSD 完整认证复刻引擎 V3
成功解密encrypted_key，现在完整解密iCubeAuthInfo并复刻
[归属基底: 具现系🔴] [对应公理: α₃变化性公理]
"""
import os, json, base64, ctypes, ctypes.wintypes, hashlib, struct
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from datetime import datetime

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
ESSENCE_DATA = r'C:\Users\13003\.bsd-essence'
ESSENCE_PROFILE = r'C:\Users\13003\AppData\Roaming\BSDEssence'

TRADITIONAL_UID = '3753060170739075'
ESSENCE_UID = 'a5b7a8623fdea6b8'

print("=" * 70)
print("  BSD 完整认证复刻引擎 V3")
print("  [归属基底: 具现系🔴] [对应公理: α₃变化性公理]")
print("=" * 70)

# ============ DPAPI实现 ============
class BSDPAPI:
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [("cbData", ctypes.wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_byte))]
    
    def __init__(self):
        self.crypt32 = ctypes.windll.crypt32
        self.kernel32 = ctypes.windll.kernel32
    
    def unprotect(self, data: bytes) -> bytes:
        """DPAPI解密 - 注意：调用者需要先跳过5字节DPAPI签名"""
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
        # 添加DPAPI签名
        return b'DPAPI\x01\x00' + out_data

# ============ AES加解密 ============
def aes_cbc_decrypt(key: bytes, data: bytes) -> bytes:
    """AES-256-CBC解密
    数据格式: IV(16字节) + 密文
    """
    iv = data[:16]
    ciphertext = data[16:]
    
    cipher = Cipher(
        algorithms.AES(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decrypter = cipher.decryptor()
    plaintext = decrypter.update(ciphertext) + decrypter.finalize()
    
    # 去除PKCS7 padding
    pad_len = plaintext[-1]
    if pad_len > 0 and pad_len <= 16:
        plaintext = plaintext[:-pad_len]
    
    return plaintext

def aes_cbc_encrypt(key: bytes, plaintext: bytes) -> bytes:
    """AES-256-CBC加密
    返回格式: IV(16字节) + 密文
    """
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

# ============ 主流程 ============
dpapi = BSDPAPI()

# Step 1: 获取AES密钥
print("\n[Step 1] 获取AES密钥...")
key_path = os.path.join(TRAE_CN_DATA, 'Local State')
with open(key_path, 'r', encoding='utf-8') as f:
    ls = json.load(f)

encrypted_key_b64 = ls['os_crypt']['encrypted_key']
encrypted_key_raw = base64.b64decode(encrypted_key_b64)

# DPAPI解密（跳过5字节DPAPI签名）
aes_key = dpapi.unprotect(encrypted_key_raw[5:])
print(f"  ✓ AES密钥获取成功: {len(aes_key)} bytes")
print(f"  AES密钥(hex): {aes_key.hex()}")

# Step 2: 解密iCubeAuthInfo
print("\n[Step 2] 解密iCubeAuthInfo...")

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]

decrypted_results = {}

for key_name in auth_keys:
    val = storage[key_name]
    print(f"\n  [{key_name}]")
    
    if not isinstance(val, str):
        print(f"    非字符串类型")
        continue
    
    raw = base64.b64decode(val)
    print(f"    原始长度: {len(raw)} bytes")
    print(f"    头部: {raw[:10].hex()}")
    
    # 分析头部格式
    # 74 63 05 10 00 = 版本+算法+标志
    # 后面可能包含IV和密文
    header_size = 5  # 固定头部大小
    
    # 尝试不同的IV位置
    decrypted = None
    
    # 方式1: 头部后直接是IV
    if len(raw) > header_size + 32:
        try:
            data_part = raw[header_size:]
            decrypted = aes_cbc_decrypt(aes_key, data_part)
            print(f"    ✓ 解密成功(头部后={header_size}字节)!")
        except Exception as e:
            print(f"    尝试{header_size}字节偏移失败: {e}")
    
    # 方式2: 尝试其他偏移
    if decrypted is None:
        for offset in [0, 4, 5, 8, 10, 16, 20]:
            if len(raw) > offset + 32:
                try:
                    data_part = raw[offset:]
                    decrypted = aes_cbc_decrypt(aes_key, data_part)
                    print(f"    ✓ 解密成功(偏移={offset}字节)!")
                    break
                except:
                    pass
    
    # 方式3: 从尾部分析（假设密文在中间，IV在头部后）
    if decrypted is None and len(raw) > 32:
        # 假设最后16字节是padding后的标志
        for iv_start in range(0, min(100, len(raw) - 32)):
            try:
                data_part = raw[iv_start:]
                decrypted = aes_cbc_decrypt(aes_key, data_part)
                if len(decrypted) > 10:  # 至少有意义的内容
                    print(f"    ✓ 解密成功(IV从{iv_start}字节开始)!")
                    break
            except:
                pass
    
    if decrypted:
        # 尝试解析
        try:
            text = decrypted.decode('utf-8')
            print(f"    UTF-8内容: {text[:300]}")
            
            # 保存原始解密结果
            safe_name = key_name.replace('://', '_').replace('/', '_').replace(':', '_')
            decrypted_results[safe_name] = text
            
            # 尝试JSON解析
            try:
                obj = json.loads(text)
                print(f"    JSON结构:")
                print(f"    {json.dumps(obj, ensure_ascii=False)[:300]}")
                
                # 检查UID字段
                uid_found = False
                uid_fields = ['uid', 'userId', 'user_id', 'account', 'id', 'accountId']
                for field in uid_fields:
                    if field in str(obj):
                        uid_found = True
                        print(f"    !!! 找到UID相关字段")
                
                # 保存JSON
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                json_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=2)
                print(f"    已保存: {json_path}")
                
            except json.JSONDecodeError:
                # 可能需要修正
                try:
                    fixed_text = text.replace("'", '"')
                    obj2 = json.loads(fixed_text)
                    print(f"    修正后JSON: {json.dumps(obj2, ensure_ascii=False)[:300]}")
                    
                    os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                    json_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.json')
                    with open(json_path, 'w', encoding='utf-8') as f:
                        json.dump(obj2, f, ensure_ascii=False, indent=2)
                except:
                    # 保存原始文本
                    os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                    txt_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.txt')
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(text)
                    print(f"    已保存文本: {txt_path}")
        
        except UnicodeDecodeError:
            print(f"    非UTF-8: {decrypted[:100]}")
            
            # 尝试直接解析bytes
            try:
                obj = json.loads(decrypted)
                print(f"    JSON(直接): {json.dumps(obj, ensure_ascii=False)[:300]}")
                
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                json_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=2)
            except:
                # 保存原始bytes
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                bin_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.bin')
                with open(bin_path, 'wb') as f:
                    f.write(decrypted)
                print(f"    已保存二进制: {bin_path}")
    else:
        print(f"    ❌ 所有解密尝试失败")

# Step 3: 分析解密结果
print(f"\n\n{'='*70}")
print(f"  [Step 3] 分析解密结果")
print(f"{'='*70}")

print(f"\n  解密成功的键: {len(decrypted_results)}")
for name, content in decrypted_results.items():
    print(f"\n  [{name}]")
    print(f"    内容长度: {len(content)} chars")
    print(f"    前200字符: {content[:200]}")

# Step 4: 总结
print(f"\n\n{'='*70}")
print(f"  总结")
print(f"{'='*70}")
print(f"""
  已完成:
  1. ✓ DPAPI解密encrypted_key (跳过5字节DPAPI签名)
  2. ✓ 获得32字节AES-256密钥: {aes_key.hex()[:32]}...
  3. 正在解密iCubeAuthInfo...
  
  关键发现:
  - DPAPI加密格式: b'DPAPI\\x01\\x00' + 加密数据
  - 正确的解密方式: 跳过前5字节再调用CryptUnprotectData
  - 加密算法: AES-256-CBC
  - 数据格式: 头部(74 63 05 10 00) + IV(16B) + 密文
""")

# 保存AES密钥供后续使用
os.makedirs(ESSENCE_DATA, exist_ok=True)
key_save_path = os.path.join(ESSENCE_DATA, 'aes_key.json')
with open(key_save_path, 'w') as f:
    json.dump({
        'aes_key': aes_key.hex(),
        'length': len(aes_key),
        'algorithm': 'AES-256-CBC',
        'decrypted_at': datetime.now().isoformat()
    }, f, indent=2)
print(f"\n  AES密钥已保存: {key_save_path}")
