#!/usr/bin/env python3
"""
BSD × Trae CN — DPAPI 深度解密（含熵/Entropy）
================================================

Chromium encrypted_key 格式:
  Base64("DPAPI" + DPAPI_blob)
  
DPAPI_blob 结构:
  DWORD version = 1
  GUID providerGuid
  ... (CryptProtectData 输出)

关键：需要正确的熵 (Entropy) 才能解密
  Trae CN 的熵可能在 product.json 或 settings.json 中
"""

import os, sys, json, base64, ctypes
from ctypes import wintypes
from datetime import datetime

crypt32 = ctypes.windll.crypt32
kernel32 = ctypes.windll.kernel32

class DATA_BLOB(ctypes.Structure):
    _fields_ = [('cbData', wintypes.DWORD),
                ('pbData', ctypes.POINTER(ctypes.c_byte))]

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN'
STORAGE_JSON = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
LOCAL_STATE = os.path.join(TRAE_CN_DATA, 'Local State')


def dpapi_unprotect_with_entropy(encrypted_blob: bytes, entropy: bytes = None) -> bytes:
    """带熵的 DPAPI 解密"""
    
    in_blob = DATA_BLOB()
    in_blob.cbData = len(encrypted_blob)
    in_blob.pbData = ctypes.cast(
        ctypes.create_string_buffer(encrypted_blob),
        ctypes.POINTER(ctypes.c_byte)
    )
    
    out_blob = DATA_BLOB()
    
    entropy_blob = None
    p_entropy = None
    
    if entropy:
        entropy_blob = DATA_BLOB()
        entropy_blob.cbData = len(entropy)
        entropy_blob.pbData = ctypes.cast(
            ctypes.create_string_buffer(entropy),
            ctypes.POINTER(ctypes.c_byte)
        )
        p_entropy = ctypes.byref(entropy_blob)
    
    result = crypt32.CryptUnprotectData(
        ctypes.byref(in_blob),
        None,
        p_entropy,
        None,
        None,
        0,
        ctypes.byref(out_blob)
    )
    
    if not result:
        error = kernel32.GetLastError()
        raise Exception(f"CryptUnprotectData 错误: {error}")
    
    data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
    kernel32.LocalFree(out_blob.pbData)
    return data


def try_all_entropies():
    """尝试所有可能的熵值"""
    
    print("=" * 60)
    print("  DPAPI 深度解密 (含熵尝试)")
    print("=" * 60)
    
    # 读取 Local State
    with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    
    encrypted_key_b64 = local_state.get('os_crypt', {}).get('encrypted_key', '')
    encrypted_key = base64.b64decode(encrypted_key_b64)
    
    print(f"  encrypted_key 总长度: {len(encrypted_key)} 字节")
    
    # 分析结构
    if encrypted_key[:5] == b'DPAPI':
        print(f"  ✅ Chromium DPAPI 格式 (含 'DPAPI' 前缀)")
        dpapi_blob = encrypted_key[5:]  # 去掉 "DPAPI" 前缀
    else:
        print(f"  ⚠️ 非标准前缀: {encrypted_key[:10].hex()}")
        dpapi_blob = encrypted_key
    
    print(f"  DPAPI blob 长度: {len(dpapi_blob)} 字节")
    print(f"  BLOB 头部: {dpapi_blob[:24].hex()}")
    
    # 收集可能的熵值
    entropies_to_try = []
    
    # 1. 空熵
    entropies_to_try.append(('空熵 (None)', None))
    
    # 2. 从 Local State 获取
    os_crypt = local_state.get('os_crypt', {})
    for key in ['app_bound_encrypted_key', 'encrypted_key_suffix', 'bound_key']:
        if key in os_crypt:
            val = os_crypt[key]
            if isinstance(val, str):
                try:
                    entropies_to_try.append((f'os_crypt.{key}', base64.b64decode(val)))
                except:
                    entropies_to_try.append((f'os_crypt.{key} (raw)', val.encode('utf-8')))
    
    # 3. 从 product.json 获取应用 ID
    product_paths = [
        os.path.join(TRAE_CN_APP, 'resources', 'app', 'product.json'),
        os.path.join(TRAE_CN_APP, 'product.json'),
    ]
    
    for pp in product_paths:
        if os.path.exists(pp):
            with open(pp, 'r', encoding='utf-8') as f:
                product = json.load(f)
            
            # 可能的应用标识
            for key in ['codeServerKey', 'clientId', 'appId', 'id', 'name']:
                if key in product:
                    val = str(product[key])
                    entropies_to_try.append((f'product.{key}', val.encode('utf-8')))
                    print(f"    发现: product.json {key}={val}")
            
            break
    
    # 4. 从 settings.json 获取
    settings_path = os.path.join(TRAE_CN_DATA, 'User', 'settings.json')
    if os.path.exists(settings_path):
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        for key, val in settings.items():
            if 'agent' in key.lower() or 'ai' in key.lower() or 'trae' in key.lower():
                entropies_to_try.append((f'settings.{key}', str(val).encode('utf-8')))
    
    # 5. 设备 ID 作为熵
    device_ids = []
    storage_path = STORAGE_JSON
    if os.path.exists(storage_path):
        with open(storage_path, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        if 'storage.serviceMachineId' in storage:
            mid = storage['storage.serviceMachineId']
            entropies_to_try.append(('machineId', mid.encode('utf-8')))
            device_ids.append(mid)
        
        if 'telemetry.machineId' in storage:
            mid = storage['telemetry.machineId']
            entropies_to_try.append(('telemetry.machineId', mid.encode('utf-8')))
            device_ids.append(mid)
    
    # 尝试每种熵
    print(f"\n  尝试 {len(entropies_to_try)} 种熵值...")
    
    for name, entropy in entropies_to_try:
        try:
            if entropy:
                result = dpapi_unprotect_with_entropy(dpapi_blob, entropy)
            else:
                result = dpapi_unprotect_with_entropy(dpapi_blob)
            
            print(f"\n  ✅ 熵 '{name}' 成功!")
            print(f"     解密长度: {len(result)} 字节")
            print(f"     前32字节: {result[:32].hex()}")
            
            # 分析结果
            if len(result) == 32:
                print(f"     → AES-256 密钥")
                return result
            elif len(result) == 16:
                print(f"     → AES-128 密钥")
                return result
            else:
                print(f"     → 其他 ({len(result)} 字节)")
                return result
                
        except Exception as e:
            err_msg = str(e)
            if '13' in err_msg:
                status = "无效数据"
            elif '5' in err_msg:
                status = "拒绝访问"
            else:
                status = str(e)
            
            # 只显示前几个
            if entropies_to_try.index((name, entropy)) < 10:
                print(f"     ❌ {name}: {status}")
    
    print(f"\n  ❌ 所有 {len(entropies_to_try)} 种熵均失败")
    return None


def analyze_successful_decryption(result: bytes):
    """分析成功解密的结果"""
    
    if not result:
        return
    
    print(f"\n{'='*60}")
    print(f"  解密结果分析")
    print(f"{'='*60}")
    
    print(f"  长度: {len(result)} 字节")
    print(f"  Hex: {result.hex()}")
    
    # 如果是 32 字节 AES 密钥
    if len(result) == 32:
        print(f"  → 这是一个 AES-256 密钥!")
        
        # 尝试用此密钥解密 AHA 数据
        print(f"\n  尝试用此密钥解密 AHA 数据...")
        
        try:
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
        except ImportError:
            os.system(f"{sys.executable} -m pip install pycryptodome -q")
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
        
        # 读取 storage.json
        with open(STORAGE_JSON, 'r', encoding='utf-8') as f:
            storage = json.load(f)
        
        for key in ['iCubeAuthInfo://icube-dc:516094651277160']:
            if key in storage:
                raw = base64.b64decode(storage[key])
                
                # AHA 格式: 746305100000 + [meta] + [IV 16 bytes] + [ciphertext]
                if raw[:6] == bytes.fromhex('746305100000'):
                    for iv_offset in [6, 8, 12, 16]:
                        if len(raw) > iv_offset + 32:
                            iv = raw[iv_offset:iv_offset+16]
                            ct = raw[iv_offset+16:]
                            
                            if len(ct) >= 16 and len(ct) % 16 == 0:
                                try:
                                    cipher = AES.new(result, AES.MODE_CBC, iv=iv)
                                    pt = unpad(cipher.decrypt(ct), 16)
                                    text = pt.decode('utf-8', errors='replace')
                                    
                                    printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
                                    if printable / len(text) > 0.7:
                                        print(f"\n  ✅ AHA 解密成功! (iv@{iv_offset})")
                                        print(f"  明文: {text[:500]}")
                                        
                                        try:
                                            jdata = json.loads(text)
                                            print(f"  JSON 解析: {json.dumps(jdata, indent=2, ensure_ascii=False)[:300]}")
                                        except:
                                            pass
                                except:
                                    pass


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════╗
║  BSD × Trae CN — DPAPI 深度解密（含熵尝试）                           ║
╚══════════════════════════════════════════════════════════════════════════╝
    """)
    
    result = try_all_entropies()
    analyze_successful_decryption(result)

if __name__ == '__main__':
    main()