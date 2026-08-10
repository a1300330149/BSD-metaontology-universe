#!/usr/bin/env python3
"""
AHA 加密数据解密器 — 基于 Trae CN main.js 逆向
================================================
数据格式: [6字节前缀][32字节密钥材料][AES-128-CBC密文]
解密后: [64字节SHA-512哈希][实际数据]
"""
import json, base64, hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 常量 (来自 main.js byteCrypto.js)
CM = 6       # 前缀长度
VW = 32      # 密钥材料长度
KD = 64      # 哈希长度
TI = 64      # XOR 数据长度
AI = 16      # AES block size

# XOR 常量 (AES 模式)
jee = bytes([82,9,106,213,48,54,165,56,191,64,163,158,129,243,215,251,
             124,227,57,130,155,47,255,135,52,142,67,68,196,222,233,203,
             84,123,148,50,166,194,35,61,238,76,149,11,66,250,195,78,
             8,46,161,102,40,217,36,178,118,91,162,73,109,139,209,37])

Wee = bytes([31,221,168,51,136,7,199,49,177,18,16,89,39,128,236,95,
             96,81,127,169,25,181,74,13,45,229,122,159,147,201,156,239,
             160,224,59,77,174,42,245,176,200,235,187,60,131,83,153,97,
             23,43,4,126,186,119,214,38,225,105,20,99,85,33,12,125])


def sha512(data):
    return hashlib.sha512(data).digest()


def hie(t, aes_mode=True):
    """XOR 混淆"""
    result = bytearray(t)
    if aes_mode:
        for r in range(t):
            result[r] = jee[r] ^ Wee[r]
    return bytes(result)


def nee(key_material, aes_size=16, iv_size=16):
    """密钥派生: 从 32 字节 key material 派生 AES 密钥和 IV"""
    s = KD + TI  # 128
    n = bytearray(s)

    o = sha512(key_material)  # 64 bytes
    a = hie(TI, True)         # 64 bytes (XOR)

    n[0:64] = o       # SHA-512(key_material)
    n[64:128] = a     # XOR data

    c = sha512(n)     # 64 bytes
    n[0:64] = c       # 覆盖前 64 字节

    aes_key = bytes(n[0:aes_size])      # 16 bytes
    iv = bytes(n[aes_size:aes_size+iv_size])  # 16 bytes

    return aes_key, iv


def decrypt_aha(encrypted_b64):
    """解密 AHA 数据"""
    raw = base64.b64decode(encrypted_b64)

    # 检查前缀
    prefix = raw[:6]
    print(f'  前缀: {prefix.hex()} ({list(prefix)})')

    # 版本判断
    if prefix[0] == 116 and prefix[1] == 99 and prefix[2] == 5 and prefix[3] == 16 and prefix[4] == 0 and prefix[5] == 0:
        print('  版本: AES ✅')
    else:
        print(f'  版本: 未知 (前缀不匹配)')
        return None

    # 提取密钥材料和密文
    key_material = raw[CM:CM+VW]  # raw[6:38]
    ciphertext = raw[CM+VW:]      # raw[38:]

    print(f'  密钥材料: {key_material.hex()[:32]}... ({len(key_material)} bytes)')
    print(f'  密文长度: {len(ciphertext)} bytes (mod 16 = {len(ciphertext) % 16})')

    if len(ciphertext) % AI != 0:
        print('  ❌ 密文长度不是 16 的倍数')
        return None

    # 派生密钥
    aes_key, iv = nee(key_material)
    print(f'  AES-128 密钥: {aes_key.hex()}')
    print(f'  IV: {iv.hex()}')

    # AES-128-CBC 解密
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    decrypted = cipher.decrypt(ciphertext)

    try:
        plaintext = unpad(decrypted, AES.block_size)
    except ValueError:
        print('  ⚠️ PKCS7 unpad 失败，尝试直接使用')
        plaintext = decrypted

    print(f'  解密后长度: {len(plaintext)}')

    # 验证哈希
    if len(plaintext) > KD:
        stored_hash = plaintext[:KD]
        actual_data = plaintext[KD:]
        computed_hash = sha512(actual_data)

        if stored_hash == computed_hash:
            print(f'  ✅ 哈希验证通过!')
            return actual_data
        else:
            print(f'  ⚠️ 哈希验证失败')
            print(f'    存储的哈希: {stored_hash[:16].hex()}...')
            print(f'    计算的哈希: {computed_hash[:16].hex()}...')
            # 仍然返回数据
            return actual_data
    else:
        print(f'  解密数据太短 ({len(plaintext)} < {KD})')
        return plaintext


# 测试解密
bak_path = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json.bak_traditional'
with open(bak_path, 'r', encoding='utf-8') as f:
    bak = json.load(f)

for key_name in ['iCubeAuthInfo://icube-dc:516094651277160',
                  'iCubeAuthInfo://usertag',
                  'iCubeAuthInfo://icube.cloudide']:
    encrypted_b64 = bak.get(key_name, '')
    if not encrypted_b64:
        continue

    print(f'\n{"="*60}')
    print(f'解密: {key_name}')
    print(f'{"="*60}')

    plaintext = decrypt_aha(encrypted_b64)
    if plaintext:
        try:
            text = plaintext.decode('utf-8')
            print(f'\n  📄 解密内容 ({len(text)} chars):')
            print(f'  {text[:500]}')

            try:
                data = json.loads(text)
                print(f'\n  📋 JSON keys: {list(data.keys())}')
                for k, v in data.items():
                    print(f'    {k}: {str(v)[:150]}')
            except:
                print('  (非 JSON 格式)')
        except:
            print(f'  二进制: {plaintext[:100].hex()}')
