#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 解密深度调试 V2
====================================

关键发现:
  数据减去 6 字节前缀后，长度恰好是 16 的倍数！
  这说明: prefix(6) + IV(16) + ciphertext(N*16)
  
  尝试: prefix[6] + iv[6:22] + ciphertext[22:]
"""

import os, sys, json, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# 路径
STORAGE = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'

# 已知密钥
AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')

# 读取 storage
with open(STORAGE, 'r', encoding='utf-8') as f:
    storage = json.load(f)

# 只处理关键的 icube-dc 键
key = 'iCubeAuthInfo://icube-dc:516094651277160'
encrypted_b64 = storage[key]
raw = base64.b64decode(encrypted_b64)

print(f'数据总长度: {len(raw)} 字节')
print(f'减去 6 字节前缀: {len(raw) - 6} 字节 ({(len(raw) - 6) / 16:.0f} blocks)')

# 结构: prefix(6) + iv(16) + ciphertext
prefix = raw[:6]
iv = raw[6:22]
ciphertext = raw[22:]

print(f'\n前缀 (6 bytes): {prefix.hex()}')
print(f'IV (16 bytes): {iv.hex()}')
print(f'密文 ({len(ciphertext)} bytes): 长度是16的倍数: {len(ciphertext) % 16 == 0}')

# 尝试解密
print('\n' + '='*60)
print('尝试 AES-256-CBC 解密')
print('='*60)

try:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
    decrypted = cipher.decrypt(ciphertext)
    
    print(f'解密成功! 原始长度: {len(decrypted)}')
    
    # 尝试去 padding
    try:
        plaintext = unpad(decrypted, 16)
        print(f'去填充成功! 明文长度: {len(plaintext)}')
        
        # 尝试解析
        try:
            text = plaintext.decode('utf-8')
            print(f'\n文本内容:')
            print(text[:2000])
            
            # 搜索 UID
            for uid in ['3753060170739075', 'a5b7a8623fdea6b8']:
                if uid in text:
                    print(f'\n🎯 找到 UID: {uid}')
                    idx = text.find(uid)
                    print(f'   位置: {idx}')
                    print(f'   上下文: ...{text[max(0,idx-20):idx+20]}...')
            
        except UnicodeDecodeError:
            print(f'\n非 UTF-8 文本')
            print(f'Hex 预览: {plaintext[:128].hex()}')
            
            # 尝试 latin-1
            try:
                text = plaintext.decode('latin-1')
                print(f'Latin-1: {text[:500]}')
            except:
                pass
                
    except ValueError as e:
        print(f'去填充失败: {e}')
        print(f'\n不去填充，尝试直接解析:')
        
        # 仍然尝试解析
        try:
            text = decrypted.decode('utf-8', errors='replace')
            print(f'文本: {text[:500]}')
        except:
            print(f'Hex: {decrypted[:128].hex()}')

except Exception as e:
    print(f'解密失败: {e}')
    
    # 尝试不同的 IV 位置
    print('\n' + '='*60)
    print('尝试不同的 IV 位置')
    print('='*60)
    
    for iv_start in range(0, 40, 2):
        for cipher_start in range(iv_start + 16, min(iv_start + 40, len(raw) - 16), 2):
            iv_try = raw[iv_start:iv_start + 16]
            ct_try = raw[cipher_start:]
            
            if len(ct_try) >= 32 and len(ct_try) % 16 == 0:
                try:
                    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv_try)
                    dec = cipher.decrypt(ct_try)
                    pt = unpad(dec, 16)
                    
                    try:
                        text = pt.decode('utf-8')
                        ratio = sum(1 for c in text if c.isprintable() or c in '\n\r\t') / max(len(text), 1)
                        if ratio > 0.6 and len(text) > 20:
                            print(f'  ✅ IV@{iv_start}→CT@{cipher_start}: 成功! 可读率 {ratio:.0%}')
                            print(f'     内容: {text[:200]}')
                            
                            for uid in ['3753060170739075', 'a5b7a8623fdea6b8']:
                                if uid in text:
                                    print(f'     🎯 UID: {uid}')
                    except:
                        pass
                except:
                    pass

print('\n' + '='*60)
print('调试完成')