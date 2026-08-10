"""
BSD 深度加密分析器
深入理解Trae CN内部的加密/解密机制
学习encrypted_key如何解密iCubeAuthInfo
"""
import os, json, base64, re

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

print("=" * 70)
print("  BSD 深度加密分析器")
print("=" * 70)

# 1. 读取main.js分析加密流程
print("\n[1] 分析main.js中的加密逻辑...")
with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 搜索os_crypt相关代码
patterns_to_find = [
    (r'os_crypt', 'os_crypt'),
    (r'encrypted_key', 'encrypted_key'),
    (r'iCubeAuthInfo', 'iCubeAuthInfo'),
    (r'CryptProtectData|CryptUnprotectData', 'DPAPI'),
    (r'decryptString|encryptString', '加解密函数'),
    (r'keytar|keytar', 'keytar'),
    (r'getPassword|setPassword', '密码存储'),
]

for pattern, name in patterns_to_find:
    matches = [(m.start(), content[max(0, m.start()-60):m.end()+200])
               for m in re.finditer(pattern, content, re.IGNORECASE)]
    if matches:
        print(f"\n  [{name}] 找到 {len(matches)} 处 (显示前3个):")
        for pos, ctx in matches[:3]:
            ctx_clean = ctx.replace('\n', ' ')[:350]
            print(f"    @{pos}: {ctx_clean}")

# 2. 分析实际的加密数据格式
print("\n\n[2] 分析iCubeAuthInfo的实际加密格式...")
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]
print(f"  iCubeAuthInfo keys: {len(auth_keys)}")

for key in auth_keys:
    val = storage[key]
    print(f"\n  [{key[:60]}...]")
    
    if isinstance(val, str):
        print(f"    类型: str, 长度: {len(val)}")
        print(f"    前100字符: {val[:100]}")
        
        # Base64解码
        try:
            raw = base64.b64decode(val)
            print(f"    Base64解码: {len(raw)} bytes")
            print(f"    前20字节(hex): {raw[:20].hex()}")
            
            # 检查各种格式
            if raw[:5] == b'DPAPI':
                print(f"    格式: DPAPI (以DPAPI开头)")
            elif raw[:2] == b'\x01\x00':
                print(f"    格式: DPAPI标准头 (01 00)")
            elif raw[:4] == b'RFBB':
                print(f"    格式: Chromium DPAPI (RFBB)")
            else:
                print(f"    格式: 未知 (前5字节: {raw[:5].hex()})")
            
            # 尝试UTF-8
            try:
                txt = raw.decode('utf-8')
                print(f"    UTF-8内容: {txt[:300]}")
            except:
                print(f"    非UTF-8文本")
            
            # 尝试JSON
            try:
                obj = json.loads(raw)
                print(f"    JSON: {json.dumps(obj, ensure_ascii=False)[:300]}")
            except:
                print(f"    非JSON格式")
                
        except Exception as e:
            print(f"    Base64解码失败: {e}")
            # 可能是明文JSON
            try:
                obj = json.loads(val)
                print(f"    明文JSON: {json.dumps(obj, ensure_ascii=False)[:300]}")
            except:
                print(f"    非标准格式")
    
    elif isinstance(val, dict):
        print(f"    类型: dict, 键: {list(val.keys())[:10]}")
        for k in list(val.keys())[:5]:
            v = val[k]
            if isinstance(v, str):
                print(f"      {k}: {v[:100] if len(v) > 100 else v}")
            else:
                print(f"      {k}: {v}")

# 3. 分析encrypted_key
print("\n\n[3] 分析encrypted_key的格式...")
local_state_path = os.path.join(TRAE_CN_DATA, 'Local State')
with open(local_state_path, 'r', encoding='utf-8') as f:
    ls = json.load(f)

if 'os_crypt' in ls:
    encrypted_key = ls['os_crypt'].get('encrypted_key', '')
    print(f"  encrypted_key存在: {bool(encrypted_key)}")
    print(f"  长度: {len(encrypted_key)} chars")
    print(f"  前80字符: {encrypted_key[:80]}")
    
    # Base64解码
    try:
        raw_key = base64.b64decode(encrypted_key)
        print(f"  Base64解码: {len(raw_key)} bytes")
        print(f"  前20字节(hex): {raw_key[:20].hex()}")
        
        # 检查格式
        if raw_key[:5] == b'DPAPI':
            print(f"  格式: DPAPI (以DPAPI开头)")
        elif raw_key[:2] == b'\x01\x00':
            print(f"  格式: DPAPI标准头")
        elif raw_key[:4] == b'RFBB':
            print(f"  格式: Chromium DPAPI (RFBB)")
        elif raw_key[:3] == b'v10' or raw_key[:3] == b'v11':
            print(f"  格式: Chrome版本化DPAPI (v10/v11)")
        else:
            print(f"  格式: 未知 (前5字节: {raw_key[:5].hex()})")
            
        # DPAPI解密encrypted_key
        import ctypes
        import ctypes.wintypes
        
        class DATA_BLOB(ctypes.Structure):
            _fields_ = [("cbData", ctypes.wintypes.DWORD),
                        ("pbData", ctypes.POINTER(ctypes.c_byte))]
        
        crypt32 = ctypes.windll.crypt32
        kernel32 = ctypes.windll.kernel32
        
        try:
            in_blob = DATA_BLOB(
                len(raw_key),
                ctypes.cast(ctypes.create_string_buffer(raw_key), ctypes.POINTER(ctypes.c_byte))
            )
            out_blob = DATA_BLOB()
            result = crypt32.CryptUnprotectData(
                ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob))
            
            if result:
                decrypted_key = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                kernel32.LocalFree(out_blob.pbData)
                print(f"  DPAPI解密成功: {len(decrypted_key)} bytes")
                print(f"  解密后的key(hex): {decrypted_key[:32].hex()}...")
                
                # 这就是AES密钥
                aes_key = decrypted_key[:32]  # AES-256需要32字节
                print(f"  AES-256密钥: {aes_key.hex()}")
            else:
                print(f"  DPAPI解密失败: {kernel32.GetLastError()}")
        except Exception as e:
            print(f"  DPAPI解密异常: {e}")
            
    except Exception as e:
        print(f"  Base64解码失败: {e}")

# 4. 深入分析main.js中解密iCubeAuthInfo的完整流程
print("\n\n[4] 分析iCubeAuthInfo的解密流程...")

# 查找decryptString或类似的函数
decrypt_patterns = [
    r'decryptString[^}]{0,500}',
    r'decrypt[^}]{0,300}iCubeAuthInfo[^}]{0,300}',
    r'async.*decrypt[^}]{0,500}',
    r'class.*Crypt[^}]{0,1000}',
    r'AES[^}]{0,300}decrypt[^}]{0,300}',
]

for pat in decrypt_patterns:
    matches = list(re.finditer(pat, content, re.IGNORECASE))
    if matches:
        print(f"\n  [{pat[:40]}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            ctx = content[m.start():min(m.end()+200, len(content))]
            ctx_clean = ctx.replace('\n', ' ')[:400]
            print(f"    @{m.start()}: {ctx_clean}")

print("\n" + "=" * 70)
print("  分析完成")
print("=" * 70)
print("""
  核心发现预期:
  1. encrypted_key 使用DPAPI加密，解密后得到AES-256密钥
  2. iCubeAuthInfo 使用AES-GCM或类似算法加密
  3. 解密流程: DPAPI解密encrypted_key → 得到AES密钥 → AES解密iCubeAuthInfo
  4. 需要找到AES解密的具体参数（模式、IV等）
""")
