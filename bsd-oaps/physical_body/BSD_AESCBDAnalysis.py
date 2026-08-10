"""
BSD AES-CBC加密实现深度分析
重点分析@1353024处的AES-CBC使用
"""
import os, re, json, base64

TRAE_CN_APP = r'C:\Users\13003\AppData\Local\Programs\Trae CN\resources\app'
MAIN_JS = os.path.join(TRAE_CN_APP, 'out', 'main.js')

TRAE_CN_DATA = r'C:\Users\13003\AppData\Roaming\Trae CN'
TRAE_CONFIG = r'C:\Users\13003\.trae-cn'

print("=" * 70)
print("  BSD AES-CBC加密深度分析")
print("=" * 70)

with open(MAIN_JS, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 深入分析@1353024处的代码
print("\n[1] 深入分析@1353024处的AES-CBC实现...")

# 获取更大的上下文
start = 1353024 - 3000
end = 1353024 + 3000
ctx = content[start:end]

# 查找关键函数
# 注意到: crypto.subtle.digest("SHA-512", t) 和 crypto.subtle.decrypt({name:"AES-CBC",iv:e},r,i)
print("  关键代码片段:")

# 查找解密函数
decrypt_funcs = [
    (r'function\s+\w+\s*\([^)]*\)\s*\{[^}]*crypto\.subtle\.decrypt[^}]*\}', '解密函数'),
    (r'async\s+function\s+\w+\s*\([^)]*\)\s*\{[^}]*crypto\.subtle[^}]*\}', '异步加密函数'),
    (r'crypto\.subtle\.decrypt\s*\([^)]+\)', 'decrypt调用'),
    (r'crypto\.subtle\.encrypt\s*\([^)]+\)', 'encrypt调用'),
]

for pat, name in decrypt_funcs:
    matches = list(re.finditer(pat, ctx, re.IGNORECASE))
    if matches:
        print(f"\n  [{name}] 找到 {len(matches)} 处:")
        for m in matches[:2]:
            func_ctx = ctx[max(0,m.start()-200):min(m.end()+300, len(ctx))]
            func_clean = func_ctx.replace('\n', ' ')[:500]
            print(f"    {func_clean}")

# 2. 分析整个加密模块结构
print("\n[2] 分析加密模块的整体结构...")

# 查找函数定义
func_patterns = [
    r'(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)\s*\{',
]

for pat in func_patterns:
    matches = list(re.finditer(pat, ctx))
    if matches:
        print(f"\n  找到 {len(matches)} 个函数定义:")
        for m in matches[:10]:
            func_name = m.group(1)
            params = m.group(2)
            print(f"    函数: {func_name}({params})")

# 3. 分析加密流程的完整链路
print("\n[3] 构建加密完整流程...")

# 分析关键函数
key_functions = {
    'l8': 'SHA-512哈希函数',
    'HIe': 'AES密钥处理',
    'VIe': 'AES-CBC解密',
    'JIe': 'AES-CBC加密',
    'KIe': 'IV生成',
    'qIe': '数据格式解析',
}

for func_name, desc in key_functions.items():
    # 搜索函数定义
    func_pattern = rf'function\s+{func_name}\s*\(([^)]*)\)'
    matches = list(re.finditer(func_pattern, ctx))
    
    if not matches:
        # 尝试在整个main.js中搜索
        matches = list(re.finditer(func_pattern, content))
    
    if matches:
        m = matches[0]
        # 获取函数体
        brace_start = content.find('{', m.end())
        if brace_start > 0:
            brace_count = 0
            brace_end = brace_start
            for i in range(brace_start, min(brace_start + 500, len(content))):
                if content[i] == '{':
                    brace_count += 1
                elif content[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        brace_end = i + 1
                        break
            
            func_body = content[m.start():brace_end]
            print(f"\n  [{func_name} - {desc}]")
            print(f"    函数签名: {func_name}({m.group(1)})")
            print(f"    函数体: {func_body.replace(chr(10), ' ')[:600]}")
            
            # 分析函数逻辑
            if 'digest' in func_body or 'SHA' in func_body:
                print(f"    → 使用SHA哈希")
            if 'AES' in func_body or 'CBC' in func_body:
                print(f"    → 使用AES-CBC")
            if 'importKey' in func_body:
                print(f"    → 导入密钥")
            if 'getRandomValues' in func_body:
                print(f"    → 生成随机值")

# 4. 基于代码分析构建正确的解密流程
print(f"\n\n{'='*70}")
print(f"  构建正确的解密流程")
print(f"{'='*70}")

# 分析iCubeAuthInfo的数据格式
storage_path = os.path.join(TRAE_CN_DATA, 'User', 'globalStorage', 'storage.json')
with open(storage_path, 'r', encoding='utf-8') as f:
    storage = json.load(f)

auth_keys = [k for k in storage.keys() if 'iCubeAuthInfo' in k]

print(f"\n  当前iCubeAuthInfo数量: {len(auth_keys)}")
print(f"\n  数据格式分析:")

for key_name in auth_keys[:1]:
    val = storage[key_name]
    raw = base64.b64decode(val)
    
    print(f"\n  [{key_name}]")
    print(f"    原始长度: {len(raw)} bytes")
    print(f"    字节分布:")
    
    # 分析头部结构
    print(f"      字节0-1: {raw[0]:02x} {raw[1]:02x} (可能版本号)")
    print(f"      字节2: {raw[2]:02x} (可能算法标识)")
    print(f"      字节3: {raw[3]:02x} (可能标志位)")
    print(f"      字节4-5: {raw[4]:02x} {raw[5]:02x}")
    
    # 检查是否是有效长度的倍数
    print(f"      长度是否为16的倍数: {len(raw) % 16 == 0}")
    print(f"      长度模16: {len(raw) % 16}")
    
    # 分析可能的IV位置
    print(f"\n    尝试识别IV位置:")
    
    # AES-CBC密文长度必须是16的倍数
    for iv_start in range(0, 50):
        remaining = len(raw) - iv_start
        if remaining > 32 and remaining % 16 == 0:
            print(f"      IV可能从{iv_start}字节开始 (剩余{remaining}字节，是16的倍数)")

# 5. 关键发现总结
print(f"\n\n{'='*70}")
print(f"  关键发现总结")
print(f"{'='*70}")
print("""
  基于代码分析的加密流程:
  
  1. 密钥派生:
     - 使用 SHA-512(dpapi解密后的encrypted_key) 作为密钥
     - 或者使用 MD5(nameShort) 作为密钥
  
  2. 加密流程:
     - 生成16字节随机IV (crypto.getRandomValues)
     - 使用 AES-CBC 加密
     - 数据格式: IV + 密文 (前16字节是IV，后面是密文)
  
  3. 解密流程:
     - 前16字节作为IV
     - 后面的作为密文
     - 使用相同密钥进行AES-CBC解密
  
  4. 数据格式:
     - iCubeAuthInfo以'7463051000'开头
     - 可能包含版本/算法信息
     - 实际加密数据可能在某个偏移之后
  
  下一步:
  - 确定头部的确切长度
  - 使用正确的密钥派生方式
  - 完整解密iCubeAuthInfo
""")
