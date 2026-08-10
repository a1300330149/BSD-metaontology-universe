"""
BSD 完整认证复刻引擎 V4
修复safe_name问题，进一步分析正确的数据格式
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
print("  BSD 完整认证复刻引擎 V4")
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

# Step 2: 解密iCubeAuthInfo - 深入分析数据格式
print("\n[Step 2] 深入分析iCubeAuthInfo数据格式...")

storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]

# 分析第一个key的详细格式
for key_idx, key_name in enumerate(auth_keys):
    val = storage[key_name]
    print(f"\n{'─'*60}")
    print(f"  [{key_idx+1}] {key_name}")
    print(f"{'─'*60}")
    
    if not isinstance(val, str):
        print(f"    非字符串类型，跳过")
        continue
    
    raw = base64.b64decode(val)
    print(f"    原始长度: {len(raw)} bytes")
    print(f"    完整字节分析:")
    
    # 分析数据结构
    # 头部: 74 63 05 10 00 00 ...
    # 尝试不同的格式假设
    
    # 假设1: 头部是10字节(版本+算法+标志+长度)
    print(f"\n    假设1: 10字节头部 + 16字节IV + 密文")
    header = raw[:10]
    print(f"      头部(hex): {header.hex()}")
    print(f"      头部(ascii): {header}")
    
    # 尝试从不同偏移开始的AES-CBC解密
    print(f"\n    尝试不同IV偏移量:")
    
    success = False
    best_result = None
    best_score = 0
    
    # 遍历所有可能的IV起始位置
    for iv_pos in range(0, min(100, len(raw) - 32)):
        try:
            data_part = raw[iv_pos:]
            decrypted = aes_cbc_decrypt(aes_key, data_part)
            
            # 评分: 是否包含有效内容
            score = 0
            try:
                text = decrypted.decode('utf-8', errors='ignore')
                # 检查是否包含有意义的字符
                valid_chars = sum(1 for c in text if c.isprintable() or c in '{}[]":,._-')
                score = valid_chars / max(len(text), 1)
                
                # 额外加分: 如果包含JSON结构
                if '{' in text and '}' in text:
                    score += 0.3
                if 'user' in text.lower() or 'uid' in text.lower() or 'account' in text.lower():
                    score += 0.2
            except:
                pass
            
            if score > best_score and score > 0.5:
                best_score = score
                best_result = (iv_pos, decrypted, score)
                print(f"      偏移{iv_pos}: 解密成功, 内容长度={len(decrypted)}, 质量分={score:.2f}")
                print(f"        预览: {decrypted[:80]}")
                success = True
                
        except Exception as e:
            pass
    
    if best_result:
        iv_pos, decrypted, score = best_result
        print(f"\n    ✓ 最佳结果: IV从{iv_pos}字节开始, 质量分={score:.2f}")
        print(f"    完整解密内容:")
        
        # 清理名称
        safe_name = key_name.replace('://', '_').replace('/', '_').replace(':', '_')
        
        # 尝试UTF-8
        try:
            text = decrypted.decode('utf-8')
            print(f"    {text[:500]}")
            
            # 尝试JSON
            try:
                obj = json.loads(text)
                print(f"\n    ✓ JSON解析成功!")
                print(f"    JSON结构: {json.dumps(obj, ensure_ascii=False)[:500]}")
                
                # 保存
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                json_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=2)
                print(f"    已保存: {json_path}")
                
                # 检查UID
                uid_str = json.dumps(obj, ensure_ascii=False)
                if TRADITIONAL_UID in uid_str:
                    print(f"    *** 找到传统UID: {TRADITIONAL_UID} ***")
                if ESSENCE_UID in uid_str:
                    print(f"    找到本源端UID: {ESSENCE_UID}")
                    
            except json.JSONDecodeError:
                # 保存文本
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                txt_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"    保存为文本: {txt_path}")
                
        except UnicodeDecodeError:
            print(f"    非UTF-8格式")
            # 保存二进制
            os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
            bin_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.bin')
            with open(bin_path, 'wb') as f:
                f.write(decrypted)
            print(f"    保存为二进制: {bin_path}")
    
    if not success:
        print(f"\n    ❌ 所有偏移量解密均未找到有效内容")
        
        # 尝试直接解密整个数据（假设没有头部）
        try:
            decrypted_direct = aes_cbc_decrypt(aes_key, raw)
            print(f"    直接解密(无头部): 长度={len(decrypted_direct)}")
            print(f"      预览: {decrypted_direct[:100]}")
        except Exception as e:
            print(f"    直接解密也失败: {e}")
        
        # 分析数据结构特征
        print(f"\n    数据结构分析:")
        print(f"      前20字节: {raw[:20].hex()}")
        print(f"      中间20字节: {raw[len(raw)//2-10:len(raw)//2+10].hex()}")
        print(f"      后20字节: {raw[-20:].hex()}")
        
        # 检查是否有明文JSON特征
        raw_str = raw.decode('latin-1')
        if '{' in raw_str:
            print(f"      可能包含JSON结构")
            # 找到{和}的位置
            for i, c in enumerate(raw_str):
                if c == '{':
                    print(f"      位置{i}处有'{{'")
                    context = raw_str[i:i+100]
                    print(f"        上下文: {repr(context[:50])}")
                    break

# Step 3: 总结
print(f"\n\n{'='*70}")
print(f"  总结与下一步")
print(f"{'='*70}")
print(f"""
  已完成:
  1. ✓ DPAPI解密encrypted_key
  2. ✓ 获得AES-256密钥: {aes_key.hex()[:32]}...
  3. 正在分析iCubeAuthInfo数据格式...
  
  关键发现:
  - 加密数据以'7463051000'开头，可能是版本+算法+标志
  - 数据可能包含固定头部，IV位于头部之后
  - 需要确定头部的确切长度和结构
  
  下一步:
  - 分析main.js中encryptString的完整实现
  - 确定数据格式中IV的准确位置
  - 完整解密所有iCubeAuthInfo
  - 替换UID并重新加密
  - 构建本源端独立认证
""")

# 保存AES密钥
os.makedirs(ESSENCE_DATA, exist_ok=True)
key_save_path = os.path.join(ESSENCE_DATA, 'aes_key.json')
with open(key_save_path, 'w') as f:
    json.dump({
        'aes_key': aes_key.hex(),
        'length': len(aes_key),
        'algorithm': 'AES-256-CBC',
        'decrypted_at': datetime.now().isoformat()
    }, f, indent=2)
print(f"  AES密钥已保存: {key_save_path}")
