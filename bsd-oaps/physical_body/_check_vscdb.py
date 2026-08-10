#!/usr/bin/env python3
"""检查 state.vscdb 和 icube.cloudide 键"""
import json, base64, os, sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
AHA_PREFIX = bytes.fromhex('746305100000')

def decrypt_aha(encrypted_b64):
    try:
        raw = base64.b64decode(encrypted_b64)
        if raw[:6] == AHA_PREFIX:
            iv = raw[6:22]
            ct = raw[22:]
        else:
            iv = raw[:16]
            ct = raw[16:]
        if len(ct) % 16 != 0:
            return None
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        dec = cipher.decrypt(ct)
        try:
            return unpad(dec, AES.block_size)
        except:
            return dec
    except:
        return None

# 1. 检查 icube.cloudide
bak_path = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\storage.json.bak_traditional'
with open(bak_path, 'r', encoding='utf-8') as f:
    bak = json.load(f)

cloudide = bak.get('iCubeAuthInfo://icube.cloudide', '')
print('=== iCubeAuthInfo://icube.cloudide ===')
print(f'  长度: {len(cloudide)}')
if cloudide:
    print(f'  前40: {cloudide[:40]}')
    pt = decrypt_aha(cloudide)
    if pt:
        try:
            text = pt.decode('utf-8')
            print(f'  解密成功! 文本:')
            print(f'  {text[:500]}')
            try:
                data = json.loads(text)
                print(f'\n  JSON keys: {list(data.keys())}')
                for k, v in data.items():
                    print(f'    {k}: {str(v)[:100]}')
            except:
                pass
        except:
            print(f'  二进制: {pt[:100].hex()}')
    else:
        print('  解密失败')

# 2. 检查 state.vscdb
print('\n=== state.vscdb ===')
db_path = r'C:\Users\13003\AppData\Roaming\Trae CN\User\globalStorage\state.vscdb'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 列出所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f'  表: {[t[0] for t in tables]}')

# 搜索包含 auth/user/login/iCube 的记录
for table in tables:
    tname = table[0]
    cursor.execute(f"SELECT key FROM {tname} WHERE key LIKE '%auth%' OR key LIKE '%user%' OR key LIKE '%login%' OR key LIKE '%iCube%' OR key LIKE '%token%'")
    rows = cursor.fetchall()
    if rows:
        print(f'\n  表 {tname} 中的相关键:')
        for row in rows:
            print(f'    {row[0]}')

# 搜索值中包含 UID 的记录
print('\n=== 搜索包含 UID 的记录 ===')
for table in tables:
    tname = table[0]
    try:
        cursor.execute(f"SELECT key, value FROM {tname}")
        for row in cursor.fetchall():
            val = str(row[1]) if row[1] else ''
            if '3753060170739075' in val or 'a5b7a8623fdea6b8' in val or 'iCubeAuthInfo' in val:
                print(f'  [{tname}] {row[0]}: {val[:100]}')
    except:
        pass

conn.close()

# 3. 检查备份中所有非 BSD 的键
print('\n=== 备份中所有键 (非 BSD) ===')
for k in sorted(bak.keys()):
    if 'bsd' not in k.lower() and '_' != k[0]:
        v = bak[k]
        if isinstance(v, str):
            print(f'  {k}: str({len(v)})')
        elif isinstance(v, dict):
            print(f'  {k}: dict({len(v)})')
        elif isinstance(v, bool):
            print(f'  {k}: {v}')
