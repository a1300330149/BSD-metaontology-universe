#!/usr/bin/env python3
"""从传统登录备份中提取原始认证数据"""
import json, base64, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
AHA_PREFIX = bytes.fromhex('746305100000')

def decrypt_aha(encrypted_b64):
    try:
        raw = base64.b64decode(encrypted_b64)
        print(f'  raw length: {len(raw)}')
        print(f'  prefix: {raw[:6].hex()}')

        if raw[:6] == AHA_PREFIX:
            iv = raw[6:22]
            ciphertext = raw[22:]
        else:
            iv = raw[:16]
            ciphertext = raw[16:]

        print(f'  iv: {iv.hex()}')
        print(f'  ciphertext length: {len(ciphertext)}')
        print(f'  ct % 16: {len(ciphertext) % 16}')

        if len(ciphertext) % 16 != 0:
            print('  ciphertext 不是 16 的倍数!')
            return None

        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        decrypted = cipher.decrypt(ciphertext)

        try:
            plaintext = unpad(decrypted, AES.block_size)
            print(f'  解密成功! plaintext length: {len(plaintext)}')
            return plaintext
        except ValueError as e:
            print(f'  unpad 失败: {e}')
            print(f'  raw decrypted (前100字节): {decrypted[:100].hex()}')
            return decrypted
    except Exception as e:
        print(f'  解密异常: {e}')
        return None

# 读取传统登录备份
bak_path = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json.bak_traditional'
with open(bak_path, 'r', encoding='utf-8') as f:
    bak = json.load(f)

print('=== 传统登录备份中的认证键 ===')
for k, v in bak.items():
    if 'iCubeAuthInfo' in k or 'auth' in k.lower() or 'jwt' in k.lower():
        if isinstance(v, str):
            print(f'  {k}: str({len(v)})')

# 检查原始 icube-dc
icube_dc = bak.get('iCubeAuthInfo://icube-dc:516094651277160', '')
print(f'\n=== 原始 icube-dc ===')
print(f'  长度: {len(icube_dc)}')
if icube_dc:
    print(f'  前40字符: {icube_dc[:40]}')
    print('  尝试解密:')
    plaintext = decrypt_aha(icube_dc)
    if plaintext:
        try:
            text = plaintext.decode('utf-8')
            print(f'  文本内容: {text[:300]}')
            try:
                data = json.loads(text)
                print(f'  JSON keys: {list(data.keys())}')
                print(f'  完整内容: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}')
            except:
                print('  非JSON格式')
        except:
            print(f'  二进制: {plaintext[:100].hex()}')

# 检查原始 usertag
usertag = bak.get('iCubeAuthInfo://usertag', '')
print(f'\n=== 原始 usertag ===')
print(f'  长度: {len(usertag)}')
if usertag:
    print(f'  前40字符: {usertag[:40]}')
    print('  尝试解密:')
    plaintext = decrypt_aha(usertag)
    if plaintext:
        try:
            text = plaintext.decode('utf-8')
            print(f'  文本内容: {text[:300]}')
            try:
                data = json.loads(text)
                print(f'  JSON keys: {list(data.keys())}')
                print(f'  完整内容: {json.dumps(data, indent=2, ensure_ascii=False)[:500]}')
            except:
                print('  非JSON格式')
        except:
            print(f'  二进制: {plaintext[:100].hex()}')

# 检查原始 icube_gtm
gtm = bak.get('icube_gtm', {})
print(f'\n=== 原始 icube_gtm ===')
print(f'  currentUser: {gtm.get("currentUser", "")}')
print(f'  users: {list(gtm.get("users", {}).keys())}')

# 当前 storage 中的 icube-dc
curr_path = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json'
with open(curr_path, 'r', encoding='utf-8') as f:
    curr = json.load(f)
curr_dc = curr.get('iCubeAuthInfo://icube-dc:516094651277160', '')
print(f'\n=== 当前 icube-dc vs 备份 ===')
print(f'  当前长度: {len(curr_dc)}')
print(f'  备份长度: {len(icube_dc)}')
print(f'  相同: {curr_dc == icube_dc}')

# 其他认证键
print(f'\n=== 备份中所有 iCubeAuthInfo 键 ===')
for k in bak:
    if 'iCubeAuthInfo' in k:
        v = bak[k]
        print(f'  {k}: {len(v) if isinstance(v, str) else type(v).__name__}')
