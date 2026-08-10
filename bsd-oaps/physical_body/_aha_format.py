#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 解密后格式识别
====================================

AES-256 解密成功但内容不可读 → 可能是:
  1. Gzip/Zlib 压缩
  2. Protobuf 二进制格式
  3. 二次加密（不同密钥）
  4. MessagePack / FlatBuffers
"""

import os, sys, json, base64, zlib, gzip, struct
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE_JSON = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')

with open(STORAGE_JSON, 'r', encoding='utf-8') as f:
    storage = json.load(f)

def aes_decrypt(raw_data: bytes, iv_start: int = 6) -> bytes:
    """AES-256-CBC 解密"""
    iv = raw_data[iv_start:iv_start+16]
    ct = raw_data[iv_start+16:]
    if len(ct) >= 16 and len(ct) % 16 == 0:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
        pt = cipher.decrypt(ct)
        try:
            return unpad(pt, 16)
        except:
            return pt
    return None


def analyze_format(name, raw_data):
    """分析解密后的二进制格式"""
    
    print(f"\n{'='*60}")
    print(f"  格式分析: {name}")
    print(f"{'='*60}")
    
    decrypted = aes_decrypt(raw_data)
    if not decrypted:
        print("    ❌ AES 解密失败")
        return
    
    print(f"    解密长度: {len(decrypted)} 字节")
    print(f"    前32字节 hex: {decrypted[:32].hex()}")
    
    # 1. 检查压缩格式
    print(f"\n  [压缩格式检测]")
    
    # Gzip
    if decrypted[:2] == b'\x1f\x8b':
        print(f"    ✅ Gzip 压缩!")
        try:
            decompressed = gzip.decompress(decrypted)
            print(f"    解压后: {len(decompressed)} 字节")
            print(f"    内容: {decompressed[:500]}")
        except Exception as e:
            print(f"    解压失败: {e}")
    else:
        print(f"    ❌ 非 Gzip")
    
    # Zlib
    if decrypted[:2] == b'\x78\x9c' or decrypted[:2] == b'\x78\xda':
        print(f"    ✅ Zlib 压缩!")
        try:
            decompressed = zlib.decompress(decrypted)
            print(f"    解压后: {len(decompressed)} 字节")
            print(f"    内容: {decompressed[:500]}")
        except Exception as e:
            print(f"    解压失败: {e}")
    else:
        print(f"    ❌ 非 Zlib")
    
    # 2. 检查 JSON/文本
    try:
        text = decrypted.decode('utf-8')
        if text[0] in '{[' or '{"' in text[:50]:
            print(f"\n  [JSON 检测] ✅")
            try:
                jdata = json.loads(text)
                print(f"    {json.dumps(jdata, indent=6, ensure_ascii=False)[:800]}")
            except:
                print(f"    纯文本: {text[:500]}")
        else:
            printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
            print(f"\n  [文本检测] 可读率: {printable/len(text):.0%}")
    except:
        print(f"\n  [二进制数据] 非 UTF-8 文本")
    
    # 3. 检查 Protobuf 特征
    print(f"\n  [Protobuf 检测]")
    # Protobuf 消息以 tag+field_number 开始
    # 格式: (field_number << 3 | wire_type) 作为 varint
    if len(decrypted) > 4:
        first_byte = decrypted[0]
        field_num = first_byte >> 3
        wire_type = first_byte & 0x07
        
        print(f"    首字节: 0x{first_byte:02x}")
        print(f"    字段号: {field_num}")
        print(f"    Wire Type: {wire_type}")
        
        wire_types = {0: 'Varint', 1: '64-bit', 2: 'Length-delimited', 5: '32-bit'}
        wt_name = wire_types.get(wire_type, f'Unknown({wire_type})')
        print(f"    类型: {wt_name}")
        
        if wire_type == 2:  # Length-delimited
            # 读取长度
            length = 0
            shift = 0
            for i in range(min(5, len(decrypted)-1)):
                byte = decrypted[1+i]
                length |= (byte & 0x7F) << shift
                if not (byte & 0x80):
                    break
                shift += 7
            print(f"    长度前缀: {length}")
            if length > 0 and length < len(decrypted):
                inner = decrypted[1+shift//7+1 : 1+shift//7+1+length]  # rough
                print(f"    内部数据长度: {len(inner)}")
        
        # 如果是 Protobuf，可能内部有子消息
        print(f"    字节流分析:")
        for i in range(min(len(decrypted), 48)):
            b = decrypted[i]
            marker = ''
            if b == 0x08: marker = ' ← field 1 varint'
            elif b == 0x12: marker = ' ← field 2 string'
            elif b == 0x1a: marker = ' ← field 3 string'
            elif b == 0x22: marker = ' ← field 4 string'
            elif b == 0x0a: marker = ' ← field 1 string'
            elif b == 0x10: marker = ' ← field 2 varint'
            if i < 32:
                print(f"      [{i:3d}]: 0x{b:02x} ({b:3d}){marker}")
    
    # 4. 尝试二次 AES 解密（使用派生密钥）
    print(f"\n  [派生密钥尝试]")
    # 使用原始密钥的不同派生
    for salt_name, salt in [
        ('空', b''),
        ('AHA', b'AHA'),
        ('icube', b'icube'),
        ('auth', b'auth'),
    ]:
        derived = hashlib.pbkdf2_hmac('sha256', AES_KEY, salt, 1)
        try:
            cipher = AES.new(derived, AES.MODE_CBC, iv=decrypted[:16])
            pt = cipher.decrypt(decrypted[16:])
            text = pt.decode('utf-8', errors='replace')
            printable = sum(1 for c in text if c.isprintable())
            if printable / len(text) > 0.8:
                print(f"    ✅ 盐'{salt_name}' 成功!")
                print(f"       内容: {text[:300]}")
        except:
            pass
    
    print(f"    (未找到有效派生密钥)")


# 分析三个 AHA 条目
import hashlib

for key, name in [
    ('iCubeAuthInfo://icube-dc:516094651277160', '设备认证'),
    ('iCubeAuthInfo://usertag', '用户标签'),
    ('iCubeAuthInfo://icube.cloudide', '云端IDE'),
]:
    if key in storage:
        raw = base64.b64decode(storage[key])
        analyze_format(f"{name} ({key})", raw)

print(f"\n{'='*60}")
print(f"  总结")
print(f"{'='*60}")
print(f"""
  🔑 AES-256 密钥已获取: 71079e1533eae2609...
  📦 解密后数据: 非文本、非 JSON、非压缩
  
  💡 可能性排序:
  1. Protobuf 二进制序列化 (最可能)
     - Trae CN 使用 Protobuf 作为内部通信格式
     - 解密后是 Protobuf 编码的认证消息
     - 需要 .proto 文件才能正确解析
  
  2. 二次加密
     - 外层 AES-CBC 解密成功
     - 内层使用不同密钥加密
     - 密钥可能绑定到设备指纹
  
  3. 自定义二进制格式
     - AHA 自定义的 TLV 格式
     - 每个字段有类型+长度+值
""")