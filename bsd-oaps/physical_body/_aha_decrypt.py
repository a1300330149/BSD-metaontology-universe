#!/usr/bin/env python3
"""
BSD × Trae CN — AHA 数据解密专项
================================

已知:
  AES-256 密钥: 71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0
  AHA 前缀: 746305100000 (6 bytes)

目标:
  解密 iCubeAuthInfo://* 中的认证数据
"""

import os, sys, json, base64
from datetime import datetime

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
except ImportError:
    os.system(f"{sys.executable} -m pip install pycryptodome -q")
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad

AES_KEY = bytes.fromhex('71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0')
TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
STORAGE_JSON = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')

with open(STORAGE_JSON, 'r', encoding='utf-8') as f:
    storage = json.load(f)

def analyze_and_decrypt(key_name, description):
    """解密单个 AHA 条目"""
    
    value = storage.get(key_name)
    if not value:
        print(f"  ❌ 未找到 {key_name}")
        return
    
    raw = base64.b64decode(value)
    
    print(f"\n{'='*60}")
    print(f"  解密: {key_name}")
    print(f"  用途: {description}")
    print(f"{'='*60}")
    print(f"  原始长度: {len(value)} chars")
    print(f"  解码长度: {len(raw)} bytes")
    print(f"  完整 hex: {raw.hex()}")
    
    # 检查 AHA 前缀
    aha_prefix = bytes.fromhex('746305100000')
    if raw[:6] != aha_prefix:
        print(f"  ⚠️ AHA 前缀不匹配: {raw[:6].hex()}")
    
    # 尝试各种解密策略
    results = []
    
    # 策略1: 前缀(6) + 元数据(2) + IV(16) + 密文
    # 746305100000 XX XX [16 bytes IV] [ciphertext]
    for meta_len in [0, 2, 4, 6, 8]:
        iv_start = 6 + meta_len
        if len(raw) > iv_start + 32:
            iv = raw[iv_start:iv_start+16]
            ct = raw[iv_start+16:]
            
            if len(ct) >= 16 and len(ct) % 16 == 0:
                try:
                    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
                    pt = cipher.decrypt(ct)
                    try:
                        pt = unpad(pt, 16)
                    except:
                        pass
                    
                    text = pt.decode('utf-8', errors='replace')
                    printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
                    ratio = printable / max(len(text), 1)
                    
                    results.append({
                        'strategy': f'meta@{meta_len} iv@{iv_start}',
                        'text': text,
                        'ratio': ratio,
                        'length': len(text),
                    })
                except Exception as e:
                    pass
    
    # 策略2: 前缀 + IV(16) + 密文（无前缀元数据）
    if len(raw) > 22:
        iv = raw[6:22]
        ct = raw[22:]
        if len(ct) >= 16 and len(ct) % 16 == 0:
            try:
                cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
                pt = cipher.decrypt(ct)
                try:
                    pt = unpad(pt, 16)
                except:
                    pass
                text = pt.decode('utf-8', errors='replace')
                printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
                results.append({
                    'strategy': 'direct_iv@6',
                    'text': text,
                    'ratio': printable / max(len(text), 1),
                    'length': len(text),
                })
            except:
                pass
    
    # 策略3: 整个数据（去掉前缀）作为 IV + 密文
    for start in range(6, min(30, len(raw) - 32)):
        iv = raw[start:start+16]
        ct = raw[start+16:]
        if len(ct) >= 16 and len(ct) % 16 == 0:
            try:
                cipher = AES.new(AES_KEY, AES.MODE_CBC, iv=iv)
                pt = cipher.decrypt(ct)
                try:
                    pt = unpad(pt, 16)
                except:
                    pass
                text = pt.decode('utf-8', errors='replace')
                printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
                results.append({
                    'strategy': f'scan_start@{start}',
                    'text': text,
                    'ratio': printable / max(len(text), 1),
                    'length': len(text),
                })
            except:
                pass
    
    # 策略4: ECB 模式（无 IV）
    if len(raw) > 6:
        ct = raw[6:]
        if len(ct) >= 16 and len(ct) % 16 == 0:
            try:
                cipher = AES.new(AES_KEY, AES.MODE_ECB)
                pt = cipher.decrypt(ct)
                try:
                    pt = unpad(pt, 16)
                except:
                    pass
                text = pt.decode('utf-8', errors='replace')
                printable = sum(1 for c in text if c.isprintable() or c in '\n\r\t')
                results.append({
                    'strategy': 'ecb_mode',
                    'text': text,
                    'ratio': printable / max(len(text), 1),
                    'length': len(text),
                })
            except:
                pass
    
    # 排序输出
    results.sort(key=lambda x: x['ratio'], reverse=True)
    
    if results:
        best = results[0]
        print(f"\n  🏆 最佳结果: {best['strategy']}")
        print(f"     可读率: {best['ratio']:.0%}")
        print(f"     长度: {best['length']} chars")
        print(f"     内容:")
        
        text = best['text']
        
        # 尝试 JSON 解析
        try:
            jdata = json.loads(text)
            print(f"     (JSON 格式)")
            print(f"     {json.dumps(jdata, indent=6, ensure_ascii=False)[:800]}")
        except:
            # 按行输出
            for line in text.split('\n')[:20]:
                print(f"     {line}")
        
        # 输出其他结果
        if len(results) > 1:
            print(f"\n  其他尝试 ({len(results)-1} 个):")
            for r in results[1:5]:
                print(f"    {r['strategy']}: 可读率 {r['ratio']:.0%}, 长度 {r['length']}")
        
        return best
    else:
        print(f"\n  ❌ 所有解密策略均失败")
        
        # 输出原始数据供分析
        print(f"\n  原始数据 hex 分析:")
        for i in range(0, min(len(raw), 64), 16):
            chunk = raw[i:i+16]
            ascii_repr = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            print(f"    {i:04x}: {chunk.hex()}  {ascii_repr}")
        
        return None


# 解密三个核心认证条目
print("""
╔══════════════════════════════════════════════════════════════════════════╗
║  BSD × Trae CN — AHA 数据解密专项                                      ║
║  AES-256 Key: 71079e1533eae26094450a564b7641e28d3292d36636807016c552ad0af26bb0
╚══════════════════════════════════════════════════════════════════════════╝
""")

results = {}

for key, desc in [
    ('iCubeAuthInfo://icube-dc:516094651277160', '设备认证'),
    ('iCubeAuthInfo://usertag', '用户标签'),
    ('iCubeAuthInfo://icube.cloudide', '云端IDE'),
]:
    r = analyze_and_decrypt(key, desc)
    results[key] = r

print(f"\n{'='*60}")
print(f"  总结")
print(f"{'='*60}")
for key, r in results.items():
    if r:
        print(f"  ✅ {key}: 可读率 {r['ratio']:.0%}")
    else:
        print(f"  ❌ {key}: 解密失败")