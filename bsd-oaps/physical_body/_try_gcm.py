#!/usr/bin/env python3
"""尝试 AES-256-GCM 解密 AHA 数据"""
import json, base64, os
from Crypto.Cipher import AES

AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
AHA_PREFIX = bytes.fromhex('746305100000')

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

    # 方案 1: prefix(6) + IV(16) + ciphertext — AES-CBC (已失败)
    # 方案 2: prefix(6) + IV(12) + ciphertext+tag — AES-GCM
    # 方案 3: prefix(6) + nonce(12) + ciphertext + tag(16) — AES-GCM
    # 方案 4: prefix(6) + IV(16) + ciphertext + tag(16) — AES-GCM with 16-byte IV

    # 尝试 GCM with 12-byte IV
    print('\n  --- GCM (IV=12, tag=16) ---')
    try:
        iv12 = raw[6:18]
        ct_and_tag = raw[18:]
        ct = ct_and_tag[:-16]
        tag = ct_and_tag[-16:]
        cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=iv12)
        plaintext = cipher.decrypt_and_verify(ct, tag)
        print(f'  ✅ 解密成功! length: {len(plaintext)}')
        try:
            text = plaintext.decode('utf-8')
            print(f'  文本: {text[:300]}')
            try:
                data = json.loads(text)
                print(f'  JSON keys: {list(data.keys())}')
                for k, v in data.items():
                    print(f'    {k}: {str(v)[:100]}')
            except:
                pass
        except:
            print(f'  二进制: {plaintext[:100].hex()}')
    except Exception as e:
        print(f'  ❌ {e}')

    # 尝试 GCM with 16-byte IV
    print('\n  --- GCM (IV=16, tag=16) ---')
    try:
        iv16 = raw[6:22]
        ct_and_tag = raw[22:]
        ct = ct_and_tag[:-16]
        tag = ct_and_tag[-16:]
        cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=iv16)
        plaintext = cipher.decrypt_and_verify(ct, tag)
        print(f'  ✅ 解密成功! length: {len(plaintext)}')
        try:
            text = plaintext.decode('utf-8')
            print(f'  文本: {text[:300]}')
        except:
            print(f'  二进制: {plaintext[:100].hex()}')
    except Exception as e:
        print(f'  ❌ {e}')

    # 尝试 GCM with 12-byte IV, no separate tag (tag appended)
    print('\n  --- GCM (IV=12, tag=last 16 of ct) ---')
    try:
        iv12 = raw[6:18]
        ct_with_tag = raw[18:]
        if len(ct_with_tag) > 16:
            ct = ct_with_tag[:-16]
            tag = ct_with_tag[-16:]
            cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=iv12)
            plaintext = cipher.decrypt_and_verify(ct, tag)
            print(f'  ✅ 解密成功!')
            try:
                text = plaintext.decode('utf-8')
                print(f'  文本: {text[:300]}')
            except:
                print(f'  二进制: {plaintext[:100].hex()}')
    except Exception as e:
        print(f'  ❌ {e}')

    # 尝试不带 prefix 的 GCM
    print('\n  --- GCM no prefix (IV=12, tag=16) ---')
    try:
        iv12 = raw[:12]
        ct_and_tag = raw[12:]
        ct = ct_and_tag[:-16]
        tag = ct_and_tag[-16:]
        cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=iv12)
        plaintext = cipher.decrypt_and_verify(ct, tag)
        print(f'  ✅ 解密成功!')
        try:
            text = plaintext.decode('utf-8')
            print(f'  文本: {text[:300]}')
        except:
            print(f'  二进制: {plaintext[:100].hex()}')
    except Exception as e:
        print(f'  ❌ {e}')

    # 尝试 CBC 但不带 prefix
    print('\n  --- CBC no prefix (IV=16) ---')
    try:
        from Crypto.Util.Padding import unpad
        iv16 = raw[:16]
        ct = raw[16:]
        if len(ct) % 16 == 0:
            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv16)
            dec = cipher.decrypt(ct)
            try:
                plaintext = unpad(dec, AES.block_size)
                print(f'  ✅ 解密成功!')
                try:
                    text = plaintext.decode('utf-8')
                    print(f'  文本: {text[:300]}')
                except:
                    print(f'  二进制: {plaintext[:100].hex()}')
            except:
                print(f'  ❌ padding 错误')
    except Exception as e:
        print(f'  ❌ {e}')
