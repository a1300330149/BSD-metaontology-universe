#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 解密深度调试
================================

目标: 找到正确的 AHA 解密方法
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

# 打印所有认证键的原始数据
for key in storage:
    if 'iCubeAuthInfo' in key:
        encrypted_b64 = storage[key]
        raw = base64.b64decode(encrypted_b64)
        
        print(f'\n{"="*60}')
        print(f'键: {key}')
        print(f'{"="*60}')
        print(f'总长度: {len(raw)} 字节')
        print(f'前 32 字节 hex: {raw[:32].hex()}')
        print(f'前 6 字节 (前缀): {raw[:6].hex()}')
        
        # 检查是否有 AHA 前缀
        aha_prefix = bytes.fromhex('746305100000')
        if raw[:6] == aha_prefix:
            print(f'✅ AHA 前缀匹配')
            print(f'  字节 6-8 (类型): {raw[6:8].hex()}')
            print(f'  字节 8-16: {raw[8:16].hex()}')
            print(f'  字节 16-32: {raw[16:32].hex()}')
            
            # 尝试多种 IV 位置
            for iv_pos in range(0, 32, 8):
                if len(raw) > iv_pos + 32:
                    iv = raw[iv_pos:iv_pos + 16]
                    ciphertext = raw[iv_pos + 16:]
                    
                    print(f'\n  尝试 IV@{iv_pos}:')
                    print(f'    IV: {iv.hex()}')
                    print(f'    密文长度: {len(ciphertext)}')
                    
                    if len(ciphertext) >= 16:
                        try:
                            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
                            decrypted = cipher.decrypt(ciphertext)
                            plaintext = unpad(decrypted, 16)
                            
                            print(f'    解密成功! 长度: {len(plaintext)}')
                            
                            # 检查是否可读
                            try:
                                text = plaintext.decode('utf-8')
                                print(f'    文本: {repr(text[:200])}')
                                
                                # 搜索 UID
                                for uid in ['3753060170739075', 'a5b7a8623fdea6b8']:
                                    if uid in text:
                                        print(f'    🎯 找到 UID: {uid}')
                                        
                            except:
                                print(f'    非文本格式')
                                print(f'    Hex: {plaintext[:64].hex()}')
                                
                        except Exception as e:
                            print(f'    解密失败: {e}')
        else:
            print(f'⚠️ 非标准 AHA 前缀')
            
            # 仍然尝试解密
            for iv_pos in range(0, min(32, len(raw) - 16), 8):
                if len(raw) > iv_pos + 32:
                    iv = raw[iv_pos:iv_pos + 16]
                    ciphertext = raw[iv_pos + 16:]
                    
                    if len(ciphertext) >= 16:
                        try:
                            cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
                            decrypted = cipher.decrypt(ciphertext)
                            plaintext = unpad(decrypted, 16)
                            
                            try:
                                text = plaintext.decode('utf-8', errors='replace')
                                ratio = sum(1 for c in text if c.isprintable() or c in '\n\r\t') / max(len(text), 1)
                                if ratio > 0.5:
                                    print(f'  ✅ IV@{iv_pos} 解密成功! 可读率 {ratio:.0%}')
                                    print(f'  内容: {text[:200]}')
                            except:
                                pass
                        except:
                            pass

print('\n' + '='*60)
print('调试完成')
print('='*60)