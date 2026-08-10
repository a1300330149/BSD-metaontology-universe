#!/usr/bin/env python3
"""
用 DPAPI 解密 iCubeAuthInfo 数据
"""
import json, base64, os, ctypes, ctypes.wintypes

AHA_PREFIX = bytes.fromhex('746305100000')

class DATA_BLOB(ctypes.Structure):
    _fields_ = [
        ('cbData', ctypes.wintypes.DWORD),
        ('pbData', ctypes.POINTER(ctypes.c_byte)),
    ]

def dpapi_decrypt(data: bytes) -> bytes:
    """使用 DPAPI 解密数据"""
    in_blob = DATA_BLOB(len(data), ctypes.cast(
        ctypes.create_string_buffer(data, len(data)),
        ctypes.POINTER(ctypes.c_byte)
    ))
    out_blob = DATA_BLOB()

    if not ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(in_blob),
        None,
        None,
        None,
        None,
        0,
        ctypes.byref(out_blob)
    ):
        error = ctypes.get_last_error()
        return None

    try:
        length = out_blob.cbData
        data = ctypes.string_at(out_blob.pbData, length)
        return data
    finally:
        ctypes.windll.kernel32.LocalFree(out_blob.pbData)

# 读取备份中的原始数据
bak_path = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json.bak_traditional'
with open(bak_path, 'r', encoding='utf-8') as f:
    bak = json.load(f)

keys_to_try = [
    'iCubeAuthInfo://icube-dc:516094651277160',
    'iCubeAuthInfo://usertag',
    'iCubeAuthInfo://icube.cloudide',
]

for key_name in keys_to_try:
    encrypted_b64 = bak.get(key_name, '')
    if not encrypted_b64:
        continue

    raw = base64.b64decode(encrypted_b64)
    print(f'\n=== {key_name} ===')
    print(f'  raw length: {len(raw)}')
    print(f'  prefix: {raw[:6].hex()}')

    # 方案 1: 去掉前缀，直接 DPAPI 解密
    print('\n  --- DPAPI (去前缀) ---')
    data_without_prefix = raw[6:]
    result = dpapi_decrypt(data_without_prefix)
    if result:
        print(f'  ✅ 解密成功! length: {len(result)}')
        try:
            text = result.decode('utf-8')
            print(f'  文本: {text[:500]}')
            try:
                data = json.loads(text)
                print(f'  JSON keys: {list(data.keys())}')
                for k, v in data.items():
                    print(f'    {k}: {str(v)[:150]}')
            except:
                pass
        except:
            print(f'  二进制: {result[:100].hex()}')
    else:
        print(f'  ❌ DPAPI 解密失败')

    # 方案 2: 不去前缀，直接 DPAPI 解密
    print('\n  --- DPAPI (带前缀) ---')
    result = dpapi_decrypt(raw)
    if result:
        print(f'  ✅ 解密成功! length: {len(result)}')
        try:
            text = result.decode('utf-8')
            print(f'  文本: {text[:500]}')
        except:
            print(f'  二进制: {result[:100].hex()}')
    else:
        print(f'  ❌ DPAPI 解密失败')

    # 方案 3: 去掉前4字节
    print('\n  --- DPAPI (去前4字节) ---')
    result = dpapi_decrypt(raw[4:])
    if result:
        print(f'  ✅ 解密成功!')
        try:
            text = result.decode('utf-8')
            print(f'  文本: {text[:300]}')
        except:
            print(f'  二进制: {result[:100].hex()}')
    else:
        print(f'  ❌ DPAPI 解密失败')
