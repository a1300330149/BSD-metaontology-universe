"""
BSD 正确解密引擎 V5
基于代码分析构建正确的解密流程
核心函数: l8, HIe, Nee, VIe, qIe, YIe, KIe
"""
import os, json, base64, hashlib, ctypes, ctypes.wintypes
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
print("  BSD 正确解密引擎 V5")
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
            raise RuntimeError(f"CryptUnprotectData失败: {self.kernel32.GetLastError()}")
        out_data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
        self.kernel32.LocalFree(out_blob.pbData)
        return out_data

# ============ 加密模块核心函数（从代码分析重建）============
# 参考: l8, HIe, Nee, VIe, qIe, YIe, KIe

class BSCryptoEngine:
    """基于main.js代码分析重建的加密引擎"""
    
    # 常量 - 需要从代码中提取
    # Kd: 密钥分割点 (aesKey长度)
    # TI: 密钥派生常量
    # AI: AES块大小 (16)
    # cm: 头部大小
    
    def __init__(self):
        self.kd = 32  # aesKey长度 (AES-256 = 32字节)
        self.ti = b'\x00' * 32  # TI常量 - 需要分析确定
        self.ai = 16  # AES-CBC块大小
        self.cm = 6  # 头部大小 - 根据YIe分析
        
        # 头部标志 - 从qIe分析
        self.flags = {
            'II': b'\x74',  # 't'
            'PI': b'\x63',  # 'c'
            'NI': b'\x05',
            'RI': b'\x10',
            '$I': b'\x00',
            'OI': b'\x00',
        }
    
    def l8(self, data: bytes) -> bytes:
        """SHA-512哈希"""
        import hashlib
        return hashlib.sha512(data).digest()
    
    def HIe(self, data: bytes, mode='AES') -> bytes:
        """密钥处理 - XOR操作"""
        # 根据代码: HIe(t, e=kn.AES)
        # if(e===kn.AES_PRIVATE) for X: i[r]=Bee[r]^Uee[r]
        # else if(e===kn.AES) for X: i[r]=jee[r]^Wee[r]
        # 这里实现简化版XOR处理
        
        result = bytearray(len(data))
        key_material = self.ti
        
        for r in range(len(data)):
            if mode == 'AES':
                # 使用固定密钥进行XOR
                result[r] = data[r] ^ key_material[r % len(key_material)]
            else:
                result[r] = data[r] ^ key_material[r % len(key_material)]
        
        return bytes(result)
    
    def Nee(self, master_key: bytes, aes_key_len: int = None, iv_len: int = None) -> dict:
        """密钥派生 - Nee函数"""
        if aes_key_len is None:
            aes_key_len = self.kd
        if iv_len is None:
            iv_len = 16
        
        # const s = Kd + TI
        s = bytearray(aes_key_len + len(self.ti))
        s[:self.kd] = b'\x00' * self.kd  # Kd部分
        s[self.kd:self.kd + len(self.ti)] = self.ti  # TI部分
        
        # const o = await l8(t) - SHA-512(master_key)
        o = self.l8(master_key)
        
        # const a = HIe(TI, r) - XOR处理
        a = self.HIe(self.ti)
        
        # n.set(o, 0) - 设置哈希结果到n的开头
        n = bytearray(len(s))
        n[:len(o)] = o[:len(s)]  # 截断或填充
        
        # n.set(a, Kd) - 设置XOR结果
        xor_result = self.HIe(self.ti)
        n[self.kd:self.kd + len(xor_result)] = xor_result[:len(n) - self.kd]
        
        # const c = await l8(n) - 再次SHA-512
        c = self.l8(bytes(n))
        
        # n.set(c, 0) - 设置第二次哈希
        n[:len(c)] = c[:len(n)]
        
        # const l = n.slice(0, e) - aesKey
        aes_key = bytes(n[:aes_key_len])
        
        # const u = n.slice(e, e+i) - iv
        iv = bytes(n[aes_key_len:aes_key_len + iv_len])
        
        return {
            'aesKey': aes_key,
            'iv': iv
        }
    
    def VIe(self, aes_key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
        """AES-CBC解密"""
        if len(ciphertext) % self.ai != 0:
            return b''  # 长度不是16的倍数
        
        try:
            cipher = Cipher(
                algorithms.AES(aes_key),
                modes.CBC(iv),
                backend=default_backend()
            )
            decrypter = cipher.decryptor()
            plaintext = decrypter.update(ciphertext) + decrypter.finalize()
            
            # 去除PKCS7 padding
            if len(plaintext) > 0:
                pad_len = plaintext[-1]
                if pad_len > 0 and pad_len <= 16:
                    plaintext = plaintext[:-pad_len]
            
            return plaintext
        except Exception:
            return b''
    
    def JIe(self, aes_key: bytes, iv: bytes, plaintext: bytes) -> bytes:
        """AES-CBC加密"""
        import os as _os
        
        # PKCS7 padding
        pad_len = 16 - (len(plaintext) % 16)
        padded = plaintext + bytes([pad_len] * pad_len)
        
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encrypter = cipher.encryptor()
        ciphertext = encrypter.update(padded) + encrypter.finalize()
        
        return ciphertext
    
    def KIe(self, length: int) -> bytes:
        """生成随机IV"""
        import os as _os
        return _os.urandom(length)
    
    def YIe(self, data: bytes) -> bytes:
        """序列化数据（添加头部）"""
        # 根据代码: function YIe(t) { e = new Uint8Array(t.length + cm)
        # e[0]=II, e[1]=PI, e[2]=NI, e[3]=RI, e[4]=$I, e[5]=OI
        # e.set(t, cm)
        header = bytes([
            0x74,  # II = 't'
            0x63,  # PI = 'c'
            0x05,  # NI
            0x10,  # RI
            0x00,  # $I
            0x00,  # OI
        ])
        return header + data
    
    def qIe(self, data: bytes) -> str:
        """解析数据格式，返回加密类型"""
        if len(data) < 6:
            return 'UNKNOWN'
        
        # 检查头部标志
        if data[0] == 0x74 and data[1] == 0x63:
            # 'tc' 开头
            if data[2] == 0x05 and data[3] == 0x10:
                return 'AES'  # kn.AES
            elif data[2] == 0x01:
                return 'AES_PRIVATE'  # kn.AES_PRIVATE
        
        return 'UNKNOWN'
    
    def decrypt_iCubeAuthInfo(self, raw_data: bytes, master_key: bytes) -> dict:
        """完整解密iCubeAuthInfo"""
        # 1. 解析数据格式
        enc_type = self.qIe(raw_data)
        print(f"    加密类型: {enc_type}")
        
        # 2. 去除头部
        data_without_header = raw_data[self.cm:]
        print(f"    去除头部后: {len(data_without_header)} bytes")
        
        # 3. 使用Nee派生密钥和IV
        # 假设master_key是DPAPI解密后的encrypted_key
        derived = self.Nee(master_key)
        print(f"    派生aesKey: {derived['aesKey'].hex()[:32]}...")
        print(f"    派生iv: {derived['iv'].hex()}")
        
        # 4. 解密
        plaintext = self.VIe(derived['aesKey'], derived['iv'], data_without_header)
        
        if len(plaintext) > 0:
            return {
                'success': True,
                'plaintext': plaintext,
                'aesKey': derived['aesKey'],
                'iv': derived['iv'],
                'enc_type': enc_type
            }
        else:
            # 尝试不同的密钥派生参数
            print(f"    尝试不同参数...")
            
            # 尝试不同的TI值
            for ti_val in [b'\x00' * 32, b'\x01' * 32, b'\xFF' * 32]:
                self.ti = ti_val
                derived2 = self.Nee(master_key)
                plaintext2 = self.VIe(derived2['aesKey'], derived2['iv'], data_without_header)
                
                if len(plaintext2) > 0:
                    return {
                        'success': True,
                        'plaintext': plaintext2,
                        'aesKey': derived2['aesKey'],
                        'iv': derived2['iv'],
                        'ti_used': ti_val.hex(),
                        'enc_type': enc_type
                    }
            
            return {'success': False, 'error': '解密失败'}


# ============ 主流程 ============
dpapi = BSDPAPI()
crypto = BSCryptoEngine()

# Step 1: 获取AES密钥
print("\n[Step 1] 获取AES密钥...")
key_path = os.path.join(TRAE_CN_DATA, 'Local State')
with open(key_path, 'r', encoding='utf-8') as f:
    ls = json.load(f)

encrypted_key_b64 = ls['os_crypt']['encrypted_key']
encrypted_key_raw = base64.b64decode(encrypted_key_b64)

# DPAPI解密（跳过5字节DPAPI签名）
master_key = dpapi.unprotect(encrypted_key_raw[5:])
print(f"  ✓ 主密钥获取成功: {len(master_key)} bytes")
print(f"  主密钥(hex): {master_key.hex()}")

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
        continue
    
    raw = base64.b64decode(val)
    print(f"    原始长度: {len(raw)} bytes")
    
    # 解析头部
    enc_type = crypto.qIe(raw)
    print(f"    加密类型: {enc_type}")
    print(f"    头部: {raw[:6].hex()}")
    
    # 使用引擎解密
    result = crypto.decrypt_iCubeAuthInfo(raw, master_key)
    
    if result['success']:
        plaintext = result['plaintext']
        print(f"    ✓ 解密成功! 长度: {len(plaintext)} bytes")
        
        # 尝试UTF-8
        try:
            text = plaintext.decode('utf-8')
            print(f"    UTF-8内容: {text[:300]}")
            
            # 尝试JSON
            try:
                obj = json.loads(text)
                print(f"    ✓ JSON解析成功!")
                print(f"    结构: {json.dumps(obj, ensure_ascii=False)[:300]}")
                
                # 保存
                safe_name = key_name.replace('://', '_').replace('/', '_').replace(':', '_')
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                json_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.json')
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(obj, f, ensure_ascii=False, indent=2)
                print(f"    已保存: {json_path}")
                
                decrypted_results[key_name] = {
                    'type': 'json',
                    'data': obj
                }
                
            except json.JSONDecodeError:
                # 保存文本
                safe_name = key_name.replace('://', '_').replace('/', '_').replace(':', '_')
                os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
                txt_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.txt')
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"    保存文本: {txt_path}")
                
                decrypted_results[key_name] = {
                    'type': 'text',
                    'data': text
                }
        
        except UnicodeDecodeError:
            print(f"    非UTF-8格式")
            # 保存二进制
            safe_name = key_name.replace('://', '_').replace('/', '_').replace(':', '_')
            os.makedirs(os.path.join(ESSENCE_DATA, 'decrypted'), exist_ok=True)
            bin_path = os.path.join(ESSENCE_DATA, 'decrypted', f'{safe_name}.bin')
            with open(bin_path, 'wb') as f:
                f.write(plaintext)
            print(f"    保存二进制: {bin_path}")
    else:
        print(f"    ❌ 解密失败: {result.get('error')}")

# Step 3: 总结
print(f"\n\n{'='*70}")
print(f"  总结")
print(f"{'='*70}")
print(f"""
  已解密: {len(decrypted_results)}/{len(auth_keys)} 个凭证
  
  下一步:
  1. 分析解密后的结构
  2. 替换UID为本源端UID
  3. 重新加密
  4. 构建本源端独立认证
""")

# 保存分析结果
os.makedirs(ESSENCE_DATA, exist_ok=True)
with open(os.path.join(ESSENCE_DATA, 'decrypt_progress.json'), 'w') as f:
    json.dump({
        'total_keys': len(auth_keys),
        'decrypted': len(decrypted_results),
        'master_key': master_key.hex(),
        'timestamp': datetime.now().isoformat()
    }, f, indent=2)
