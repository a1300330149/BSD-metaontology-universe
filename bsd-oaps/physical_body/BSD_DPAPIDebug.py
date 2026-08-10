#!/usr/bin/env python3
"""
BSD × Trae CN — DPAPI 解密调试
==============================

调试 encrypted_key 的解密过程

版本: V1.0 · 2026-08-05
"""

import os, json, base64, ctypes
from datetime import datetime

# 路径
TRAE_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
LOCAL_STATE = os.path.join(TRAE_DATA, 'Local State')


def debug_dpapi():
    """调试 DPAPI 解密"""
    
    print('='*60)
    print('  BSD × Trae CN — DPAPI 解密调试')
    print('='*60)
    
    # 1. 读取 Local State
    with open(LOCAL_STATE, 'r', encoding='utf-8') as f:
        local_state = json.load(f)
    
    encrypted_key_b64 = local_state.get('os_crypt', {}).get('encrypted_key', '')
    
    print(f'\n  encrypted_key (base64): {encrypted_key_b64[:50]}...')
    
    encrypted_key = base64.b64decode(encrypted_key_b64)
    print(f'  encrypted_key 原始长度: {len(encrypted_key)} 字节')
    print(f'  前 20 字节: {encrypted_key[:20].hex()}')
    
    # 2. 分析 encrypted_key 格式
    # Windows DPAPI 加密的数据通常以 "DPAPI" 前缀开始
    # 或者是一个特定的二进制格式
    
    print(f'\n  📊 格式分析:')
    print(f'    第一个字节: 0x{encrypted_key[0]:02x}')
    
    # 检查是否有 BCRYPT 或 DPAPI 标志
    # Chrome/Trae CN 可能使用不同的加密方式
    
    # 3. 尝试不同的解密方式
    
    # 方式1: 直接 DPAPI 解密
    print(f'\n  尝试 1: 直接 DPAPI 解密')
    try:
        result = dpapi_decrypt(encrypted_key)
        print(f'  ✅ 成功! 长度: {len(result)} 字节')
        print(f'     内容: {result[:50]}...')
        return result
    except Exception as e:
        print(f'  ❌ 失败: {e}')
    
    # 方式2: 跳过前 N 字节再 DPAPI 解密
    # 有些实现会在 DPAPI 数据前添加标识
    print(f'\n  尝试 2: 跳过前缀再解密')
    for skip in [0, 4, 8, 16, 20]:
        if len(encrypted_key) > skip:
            try:
                data = encrypted_key[skip:]
                result = dpapi_decrypt(data)
                print(f'  ✅ 跳过 {skip} 字节成功! 长度: {len(result)} 字节')
                print(f'     内容: {result[:50]}...')
                return result
            except Exception as e:
                print(f'  跳过 {skip} 字节: ❌ {e}')
    
    # 方式3: 使用不同的熵
    print(f'\n  尝试 3: 使用不同的熵')
    
    # 熵的来源:
    # - 空熵
    # - product.json 中的应用标识
    # - 当前用户 SID
    
    entropy_options = [
        (b'', '空熵'),
        (b'Trae CN', '应用名'),
        (b'icube', '产品名'),
    ]
    
    for entropy, desc in entropy_options:
        try:
            result = dpapi_decrypt_with_entropy(encrypted_key, entropy)
            print(f'  ✅ {desc} 成功! 长度: {len(result)} 字节')
            print(f'     内容: {result[:50]}...')
            return result
        except Exception as e:
            print(f'  {desc}: ❌ {e}')
    
    # 方式4: 检查是否为 AES-GCM 加密
    print(f'\n  尝试 4: 分析是否为 AES-GCM 格式')
    # AES-GCM 格式: nonce(12) + ciphertext + tag(16)
    
    # 方式5: 使用 CryptUnprotectData 带额外参数
    print(f'\n  尝试 5: 不同的 flags')
    for flags in [0, 1, 2, 4]:
        try:
            result = dpapi_decrypt_with_flags(encrypted_key, flags)
            print(f'  ✅ flags={flags} 成功! 长度: {len(result)} 字节')
            return result
        except Exception as e:
            print(f'  flags={flags}: ❌ {e}')
    
    return None


def dpapi_decrypt(encrypted_data: bytes) -> bytes:
    """DPAPI 解密"""
    
    import ctypes
    
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ('cbData', ctypes.c_ulong),
            ('pbData', ctypes.c_void_p),
        ]
    
    p = ctypes.create_string_buffer(encrypted_data)
    blob_in = DATA_BLOB(len(encrypted_data), ctypes.addressof(p))
    blob_out = DATA_BLOB()
    
    result = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(blob_out)
    )
    
    if not result:
        error = ctypes.GetLastError()
        raise RuntimeError(f'CryptUnprotectData 失败: {error}')
    
    decrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    
    return decrypted


def dpapi_decrypt_with_entropy(encrypted_data: bytes, entropy: bytes) -> bytes:
    """带熵的 DPAPI 解密"""
    
    import ctypes
    
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ('cbData', ctypes.c_ulong),
            ('pbData', ctypes.c_void_p),
        ]
    
    p = ctypes.create_string_buffer(encrypted_data)
    blob_in = DATA_BLOB(len(encrypted_data), ctypes.addressof(p))
    
    e = ctypes.create_string_buffer(entropy)
    blob_entropy = DATA_BLOB(len(entropy), ctypes.addressof(e))
    
    blob_out = DATA_BLOB()
    
    result = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in),
        None,
        ctypes.byref(blob_entropy),  # entropy
        None,
        None,
        0,
        ctypes.byref(blob_out)
    )
    
    if not result:
        error = ctypes.GetLastError()
        raise RuntimeError(f'CryptUnprotectData 失败: {error}')
    
    decrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    
    return decrypted


def dpapi_decrypt_with_flags(encrypted_data: bytes, flags: int) -> bytes:
    """带 flags 的 DPAPI 解密"""
    
    import ctypes
    
    class DATA_BLOB(ctypes.Structure):
        _fields_ = [
            ('cbData', ctypes.c_ulong),
            ('pbData', ctypes.c_void_p),
        ]
    
    p = ctypes.create_string_buffer(encrypted_data)
    blob_in = DATA_BLOB(len(encrypted_data), ctypes.addressof(p))
    blob_out = DATA_BLOB()
    
    # CRYPTPROTECT_UI_FORBIDDEN = 1
    # CRYPTPROTECT_LOCAL_MACHINE = 4
    # CRYPTPROTECT_UTF8 = 200
    
    result = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in),
        None,
        None,
        None,
        None,
        flags,
        ctypes.byref(blob_out)
    )
    
    if not result:
        error = ctypes.GetLastError()
        raise RuntimeError(f'CryptUnprotectData 失败 (flags={flags}): {error}')
    
    decrypted = ctypes.string_at(blob_out.pbData, blob_out.cbData)
    ctypes.windll.kernel32.LocalFree(blob_out.pbData)
    
    return decrypted


if __name__ == '__main__':
    result = debug_dpapi()
    
    if result:
        print(f'\n  🎉 成功获取 AES 密钥!')
        print(f'     密钥: {result.hex()}')
        
        # 保存到文件供后续使用
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'bsd_aes_key.bin')
        with open(output_path, 'wb') as f:
            f.write(result)
        print(f'     已保存到: {output_path}')
    else:
        print(f'\n  ❌ 所有方法都失败了')
        print(f'     可能需要其他解密方式')