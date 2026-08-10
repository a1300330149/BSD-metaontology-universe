"""
BSD 加密深度解析器 V2
深入分析Cu.decryptString的实现和加密格式
"""
import os, json, base64, re, hashlib

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

print("=" * 70)
print("  BSD 加密深度解析器 V2")
print("=" * 70)

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 查找Cu.encryptString/decryptString的完整实现
print("\n[1] 分析Cu.encryptString/decryptString实现...")

# 找到EncryptionMainService相关代码
encryption_pattern = r'EncryptionMainService'
matches = list(re.finditer(encryption_pattern, content))
print(f"  找到 {len(matches)} 处EncryptionMainService")

# 找到Cu对象的定义
# 搜索包含decryptString的更大上下文
decrypt_ctx_pattern = r'(\w+)\.decryptString\s*=|(\w+)\.prototype\.decryptString'
matches2 = list(re.finditer(decrypt_ctx_pattern, content))
print(f"  decryptString定义位置: {len(matches2)}")

# 查找Cu的导入/定义
cu_patterns = [
    r'import\s+\{[^}]*Cu[^}]*\}\s+from',
    r'const\s+Cu\s*=|var\s+Cu\s*=|let\s+Cu\s*=',
    r'Cu\s*=',
    r'from.*Cu',
]

for pat in cu_patterns:
    matches = list(re.finditer(pat, content))
    if matches:
        print(f"\n  [{pat[:50]}] 找到 {len(matches)} 处")
        for m in matches[:2]:
            ctx = content[max(0,m.start()-100):m.end()+100]
            ctx_clean = ctx.replace('\n', ' ')[:300]
            print(f"    @{m.start()}: {ctx_clean}")

# 2. 分析实际加密数据格式
print("\n\n[2] 分析加密数据格式 (7463开头)...")

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]

# 分析每个加密数据的结构
for key in auth_keys:
    val = storage[key]
    if isinstance(val, str):
        raw = base64.b64decode(val)
        
        print(f"\n  [{key[:50]}...]")
        print(f"    总长度: {len(raw)} bytes")
        print(f"    头部10字节(hex): {raw[:10].hex()}")
        
        # 尝试解析头部结构
        # 格式猜测: 74 63 05 10 00 ...
        # 可能是: 版本号(2) + 算法标识(1) + 标志位(1) + 长度(?) + ...
        
        header = raw[:10]
        print(f"    解析头部:")
        print(f"      字节0-1: {header[0]:02x} {header[1]:02x} (可能版本号)")
        print(f"      字节2: {header[2]:02x} (可能算法标识)")
        print(f"      字节3: {header[3]:02x} (可能标志位)")
        print(f"      字节4: {header[4]:02x} (可能预留)")
        
        # 尝试不同的解析方式
        if len(raw) > 100:
            print(f"    中间部分(字节50-60): {raw[50:60].hex()}")
            print(f"    尾部(最后20字节): {raw[-20:].hex()}")
        
        # 尝试AES-GCM格式解析
        # AES-GCM通常: IV(12字节) + Ciphertext + Tag(16字节)
        # 或者: Salt + IV + Ciphertext + Tag
        
        # 假设头部后是实际的加密数据
        # 尝试跳过头部直接解密
        try:
            from cryptography.hazmat.primitives.ciphers.aead import AESGCM
            
            # 尝试使用encrypted_key解密
            key_path = os.path.join(TRAE_CN_DATA, 'Local State')
            with open(key_path, 'r', encoding='utf-8') as kf:
                ls = json.load(kf)
            
            if 'os_crypt' in ls:
                encrypted_key_b64 = ls['os_crypt'].get('encrypted_key', '')
                encrypted_key_raw = base64.b64decode(encrypted_key_b64)
                
                # DPAPI解密key
                import ctypes
                import ctypes.wintypes
                
                class DATA_BLOB(ctypes.Structure):
                    _fields_ = [("cbData", ctypes.wintypes.DWORD),
                                ("pbData", ctypes.POINTER(ctypes.c_byte))]
                
                crypt32 = ctypes.windll.crypt32
                kernel32 = ctypes.windll.kernel32
                
                try:
                    in_blob = DATA_BLOB(
                        len(encrypted_key_raw),
                        ctypes.cast(ctypes.create_string_buffer(encrypted_key_raw), 
                                   ctypes.POINTER(ctypes.c_byte))
                    )
                    out_blob = DATA_BLOB()
                    result = crypt32.CryptUnprotectData(
                        ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
                    
                    if result:
                        aes_key = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                        kernel32.LocalFree(out_blob.pbData)
                        print(f"    AES密钥获取成功: {len(aes_key)} bytes")
                        print(f"    AES密钥(hex): {aes_key[:32].hex()}")
                        
                        # 尝试不同的AES-GCM解密方式
                        # 方式1: 数据前12字节为IV
                        if len(raw) > 28:  # 12字节IV + 至少1字节密文 + 16字节Tag
                            iv = raw[:12]
                            ciphertext_with_tag = raw[12:]
                            try:
                                aesgcm = AESGCM(aes_key[:32])
                                decrypted = aesgcm.decrypt(iv, ciphertext_with_tag, None)
                                print(f"    ✓ AES-GCM解密成功(方式1): {len(decrypted)} bytes")
                                try:
                                    txt = decrypted.decode('utf-8')
                                    print(f"    UTF-8内容: {txt[:300]}")
                                    # 尝试JSON
                                    obj = json.loads(txt)
                                    print(f"    JSON对象: {json.dumps(obj, ensure_ascii=False)[:300]}")
                                except:
                                    print(f"    非UTF-8: {decrypted[:100]}")
                            except Exception as e1:
                                print(f"    方式1失败: {e1}")
                        
                        # 方式2: 跳过5字节头部
                        if len(raw) > 33:
                            iv2 = raw[5:17]
                            ciphertext_with_tag2 = raw[17:]
                            try:
                                aesgcm2 = AESGCM(aes_key[:32])
                                decrypted2 = aesgcm2.decrypt(iv2, ciphertext_with_tag2, None)
                                print(f"    ✓ AES-GCM解密成功(方式2): {len(decrypted2)} bytes")
                                try:
                                    txt2 = decrypted2.decode('utf-8')
                                    print(f"    UTF-8内容: {txt2[:300]}")
                                    obj2 = json.loads(txt2)
                                    print(f"    JSON对象: {json.dumps(obj2, ensure_ascii=False)[:300]}")
                                except:
                                    pass
                            except Exception as e2:
                                print(f"    方式2失败: {e2}")
                        
                        # 方式3: 尝试偏移不同
                        for offset in [0, 4, 5, 8, 10]:
                            if len(raw) > offset + 28:
                                iv3 = raw[offset:offset+12]
                                ciphertext_with_tag3 = raw[offset+12:]
                                try:
                                    aesgcm3 = AESGCM(aes_key[:32])
                                    decrypted3 = aesgcm3.decrypt(iv3, ciphertext_with_tag3, None)
                                    print(f"    ✓ AES-GCM解密成功(偏移{offset}): {len(decrypted3)} bytes")
                                    try:
                                        txt3 = decrypted3.decode('utf-8')
                                        print(f"    UTF-8内容: {txt3[:200]}")
                                        obj3 = json.loads(txt3)
                                        print(f"    JSON: {json.dumps(obj3, ensure_ascii=False)[:200]}")
                                        break
                                    except:
                                        pass
                                except:
                                    pass
                        
                except Exception as dpapi_err:
                    print(f"    DPAPI解密失败: {dpapi_err}")
                    print(f"    错误码: {kernel32.GetLastError()}")
        except ImportError:
            print(f"    cryptography库未安装，跳过AES解密尝试")
        except Exception as e:
            print(f"    解密尝试失败: {e}")

# 3. 更深入查找加密实现
print("\n\n[3] 深入查找加密实现...")

# 查找crypto相关代码
crypto_patterns = [
    r'class.*Crypto[^{]*\{',
    r'crypto\.subtle|SubtleCrypto',
    r'AESGCM|aes-gcm|AES_GCM',
    r'createDecipher|createCipher',
    r'createDecipheriv|createCipheriv',
    r'GCM|gcm',
]

for pat in crypto_patterns:
    matches = list(re.finditer(pat, content))
    if matches and len(matches) < 20:
        print(f"\n  [{pat}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            ctx = content[max(0,m.start()-80):min(m.end()+200, len(content))]
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{m.start()}: {ctx_clean}")

# 4. 查找具体的加密密钥派生逻辑
print("\n\n[4] 查找密钥派生逻辑...")

kdf_patterns = [
    r'scrypt|pbkdf2|PBKDF2|deriveKey|deriveBits',
    r'keyDerivation|key_derivation',
    r'importKey|import_key',
    r'wrapKey|unwrapKey',
]

for pat in kdf_patterns:
    matches = list(re.finditer(pat, content))
    if matches and len(matches) < 20:
        print(f"\n  [{pat}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            ctx = content[max(0,m.start()-80):min(m.end()+200, len(content))]
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{m.start()}: {ctx_clean}")

print("\n" + "=" * 70)
print("  解析完成")
print("=" * 70)
